from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.modules.service_request.helper import build_service_request_response
from app.modules.service_request.repository import ServiceRequestRepository
from app.modules.service_request.model import ServiceRequest
from app.modules.service_request.schema import (
    LLMDiagnosticRequestPreview,
    ServiceRequestResponse,
    CustomerRequestPreview,
    ConfirmServiceRequest,
    ServiceRequestStatus,
    UserSchema 
)

from app.modules.service_request.interface import (
    ProcurementAlertInterface,
    LLMDiagnosisInterface,
    RequestPartInterface,
    SparePartInterface,
    CustomerInterface
)

from app.shared.exception import (
    ServiceRequestStatusIsNotPendingError,
    ServiceRequestDoesNotExistError,
    ServiceRequestFailedError
)


class ServiceRequestService:

    def __init__(
        self,
        repository: ServiceRequestRepository,
        llm_diagnosis_interface: LLMDiagnosisInterface,
        procurement_alert_interface: ProcurementAlertInterface,
        request_part_interface: RequestPartInterface,
        spare_part_interface: SparePartInterface,
        customer_interface: CustomerInterface,
        db: Session
    ):

        self.repository = repository
        self.llm_diagnosis_interface = llm_diagnosis_interface
        self.procurement_alert_interface = procurement_alert_interface
        self.request_part_interface = request_part_interface
        self.spare_part_interface = spare_part_interface
        self.customer_interface = customer_interface
        self.db = db

    
    """  
    
        Staging the Customer Info, LLM Diagnosis, Find the Matched Spare Parts, and Service Request.
        Ready to be validate by the technician.
    
    """

    async def run_ai_diagnosis(
        self,
        user: UserSchema,
        request: LLMDiagnosticRequestPreview,
        customer_data: CustomerRequestPreview
    ) -> ServiceRequestResponse:
            
        customer = self.customer_interface.find_or_create_customer(customer_request=customer_data)
        llm_diagnosis = await self.llm_diagnosis_interface.analyze(request=request)
        now = datetime.now(timezone.utc).replace(tzinfo=None)

        service_request = ServiceRequest(
            customer_id=customer.id,
            user_id=user.id,
            device_type=request.device_type,
            device_brand=request.device_brand,
            device_model=request.device_model,
            fault_description=request.fault_descriptions,
            status=ServiceRequestStatus.PENDING,
            created_at=now,
            updated_at=now
        )

        self.repository.create(service_request)
        self.db.flush()

        llm_diagnosis.request_id = service_request.id
        self.llm_diagnosis_interface.stage(llm_diagnosis)

        self.db.commit()
        self.db.refresh(service_request)
        self.db.refresh(llm_diagnosis)

        llm_recommendation = llm_diagnosis.llm_recommendation
        
        matched_parts = []
        if llm_recommendation is not None:
            matched_parts = self.spare_part_interface.search_matched_spare_part(
                llm_recommendation.component
            )

        return ServiceRequestResponse(
            service_request_id=service_request.id,
            diagnosis_id=llm_diagnosis.id,
            customer_id=customer.id,
            status=ServiceRequestStatus.PENDING,
            diagnosis=llm_diagnosis.response,
            confidence=llm_diagnosis.confidence,
            model=llm_diagnosis.model,
            llm_recommended_part=llm_recommendation,
            matched_part=matched_parts,
            created_at=service_request.created_at
        )


    """  
    
        Confirm the Service Request From the Frontend.
        Then Validate the Field the User Returns to.

        - Links the selected parts (from the catalog or as snapshots).
        - Creates a procurement alert for each confirmed part.
        - Updates the service request status.
        - Updates the LLM diagnosis verdict (ACCEPTED / REJECTED).
    
    """

    def confirm_request(
        self,
        service_request_id: int,
        request: ConfirmServiceRequest
    ) -> ServiceRequestResponse:

        try:
            
            service_request = self.repository.get_by_id(service_request_id)

            if service_request is None:
                raise ServiceRequestDoesNotExistError(
                    detail=f"Service request {service_request_id} not found"
                )

            if service_request.status != ServiceRequestStatus.PENDING:
                raise ServiceRequestStatusIsNotPendingError(
                    detail=f"Cannot confirm request in status {service_request.status}"
                )

            now = datetime.now(timezone.utc).replace(tzinfo=None)

            if service_request.llm_diagnosis is not None:
                service_request.llm_diagnosis.status = request.diagnosis_verdict

            for selection in request.selected_parts:

                part = (
                    self.spare_part_interface.get_spare_part_by_id(selection.part_id)
                    if selection.part_id is not None
                    else None
                )

                if part is None:

                    self.request_part_interface.create_request(
                        request_id=service_request.id,
                        part_id=None,
                        part_name_snapshot=selection.part_name,
                        quantity=selection.quantity,
                        is_stock_validated=False,
                    )

                    self.procurement_alert_interface.create_procurement_alert(
                        request_id=service_request.id,
                        part_id=None,
                        part_name_snapshot=selection.part_name,
                        is_resolved=False,
                        created_at=now,
                        alert_message=(
                            f"Service Request #{service_request.id} created by "
                            f"{service_request.user_id} needs {selection.part_name} "
                            f"which does not exist in spare part stock."
                        ),
                    )

                    continue

                in_stock = (
                    part.stock_quality is not None
                    and part.stock_quality >= selection.quantity
                )

                self.request_part_interface.create_request(
                    request_id=service_request.id,
                    part_id=part.id,
                    part_name_snapshot=part.part_name,
                    quantity=selection.quantity,
                    is_stock_validated=in_stock,
                )

                self.procurement_alert_interface.create_procurement_alert(
                    request_id=service_request.id,
                    part_id=part.id,
                    part_name_snapshot=part.part_name,
                    is_resolved=False,
                    created_at=now,
                    alert_message=(
                        f"Service Request #{service_request.id} created by "
                        f"{service_request.user_id} needs {part.part_name} "
                        f"({part.part_code}) from {part.shelf_location}."
                    ),
                )

            self.repository.update_service_request(
                now=now,
                stored_service_request=service_request,
                final_status=request.final_status,
                technician_notes=request.technician_notes
            )

            self.db.commit()
            self.db.refresh(service_request)

            llm_recommendation = llm_diagnosis.llm_recommendation

            matched_parts = []
            if llm_recommendation is not None:
                matched_parts = spare_part_interface.search_matched_spare_part(
                    llm_recommendation.component,
                )

            return build_service_request_response(
                service_request=service_request,
                matched_parts=matched_parts    
            )

        except Exception:

            self.db.roolback()
            raise ServiceRequestFailedError()


    """  

        Cancel the Service Request from the Frontend.
        Tnen Change the State of Service Request.

        - Marks the request UNSUCCESSFUL (or CANCELLED).
        - Marks the LLM diagnosis REJECTED.
        - Cancels any open procurement alerts for this request. 
    
    """

    def cancel_request(
        self,
        service_request_id: int
    ) -> None:

        try:
            
            service_request = self.repository.get_by_id(service_request_id)

            if service_request is None:
                raise ServiceRequestDoesNotExistError(
                    detail=f"Service request {service_request_id} not found"
                )


            if service_request.status in (
                ServiceRequestStatus.COMPLETED,
                ServiceRequestStatus.UNSUCCESSFUL,
            ):
                raise ServiceRequestStatusIsNotPendingError(
                    detail=f"Cannot cancel request in status {service_request.status}"
                )

            now = datetime.now(timezone.utc).replace(tzinfo=None)

            if service_request.llm_diagnosis is not None:
                service_request.llm_diagnosis.status = ConfirmServiceRequest.diagnosis_verdict.REJECTED

            self.procurement_alert_interface.cancel_by_request(
                request_id=service_request.id,
                alert_message=(
                    f"Service Request #{service_request.id} created by "
                    f"{service_request.user_id} with a diagnostic status of "
                    f"{service_request.llm_diagnosis.status} has been cancelled."
                )
            )

            self.repository.update_service_request(
                now=now,
                stored_service_request=service_request,
                final_status=ConfirmServiceRequest.final_status.UNSUCCESSFUL,
                technician_notes=None
            )

            self.db.commit()
        
        except Exception:
            
            self.db.rollback()
            raise ServiceRequestFailedError()