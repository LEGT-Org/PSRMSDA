from math import ceil
from datetime import date, datetime, timezone
from sqlalchemy.orm import Session

from app.modules.service_request.helper import build_service_request_response
from app.modules.service_request.repository import ServiceRequestRepository
from app.modules.service_request.model import ServiceRequest
from app.modules.service_request.schema import (
    ServiceRequestPageListResponse,
    ServiceRequestDetailsResponse,
    CustomerServiceRequestDetails,
    LLMDiagnosticRequestPreview,
    ProcurementAlertTypeReview,
    ServiceRequestListResponse,
    UserServiceRequestDetails,
    LLMRecommendedSparePart,
    MatchedSparePartPreview,
    ServiceRequestResponse,
    CustomerRequestPreview,
    ConfirmServiceRequest,
    ServiceRequestStatus,
    RequestPartDetails,
    UserSchema 
)

from app.modules.service_request.interface import (
    ProcurementAlertInterface,
    LLMDiagnosisInterface,
    RequestPartInterface,
    SparePartInterface,
    CustomerInterface
)

from app.shared.infrastructure.email import (
    JinjaEmailRendered,
    EmailService
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
        email_renderer: JinjaEmailRendered,
        email_service: EmailService,
        db: Session
    ):

        self.repository = repository
        self.llm_diagnosis_interface = llm_diagnosis_interface
        self.procurement_alert_interface = procurement_alert_interface
        self.request_part_interface = request_part_interface
        self.spare_part_interface = spare_part_interface
        self.customer_interface = customer_interface
        self.email_renderer = email_renderer
        self.email_service = email_service
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
            
        try:

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
                sop_instructions=llm_diagnosis.parsed_output["standard_operating_procedure"],
                status=ServiceRequestStatus.PENDING,
                created_at=now,
                updated_at=now
            )

            self.repository.create(service_request)
            self.db.flush()

            llm_diagnosis.request_id = service_request.id

            self.llm_diagnosis_interface.stage(llm_diagnosis)

            llm_recommendation = llm_diagnosis.llm_recommendation

            matched_parts = []

            if llm_recommendation is not None:
                matched_parts = self.spare_part_interface.search_matched_spare_part(llm_recommendation.component)

                in_stock = (
                    matched_parts.stock_quantity is not None
                    and matched_parts.stock_quantity >= 1
                )

                matched_spare_parts = MatchedSparePartPreview(
                    part_id=matched_parts.id,
                    part_name=matched_parts.name,
                    part_code=matched_parts.part_code,
                    device_model=matched_parts.device_model,
                    device_brand=matched_parts.device_brand,
                    specifications=matched_parts.specifications,
                    unit_cost=matched_parts.unit_cost,
                    stock_quantity=matched_parts.stock_quantity,
                    shelf_location=matched_parts.shelf_location,
                    image_url=matched_parts.image_url,
                    category_name=matched_parts.categories.name,
                    is_available=in_stock
                )

                llm_recommended_part = LLMRecommendedSparePart(
                    llm_component=llm_recommendation.component,
                    llm_reason=llm_recommendation.reason,
                    compatibility_requirements=llm_recommendation.compatibility_requirements
                )

                self.procurement_alert_interface.create_procurement_alert(
                    request_id=service_request.id,
                    part_id=None,
                    part_name_snapshot=llm_recommendation.component,
                    is_resolved=False,
                    created_at=now,
                    alert_type=ProcurementAlertTypeReview.alert.REQUEST_STAGE,
                    alert_message=(
                        f"Service Request No. {service_request.id} created by "
                        f"{service_request.user_id} has been staged and ready to "
                        f"be review."
                    ),
                )

            else:
                matched_spare_parts = []
                llm_recommended_part = None

            self.db.commit()
            self.db.refresh(service_request)
            self.db.refresh(llm_diagnosis)

            return ServiceRequestResponse(
                service_request_id=service_request.id,
                diagnosis_id=llm_diagnosis.id,
                customer_id=customer.id,
                status=ServiceRequestStatus.PENDING,
                diagnosis=llm_diagnosis.response,
                llm_recommended_part=llm_recommended_part,
                matched_part=matched_spare_parts,
                created_at=service_request.created_at
            )

        except Exception as error:

            print(error)

            self.db.rollback()
            raise ServiceRequestFailedError() from error


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
        user_id: int,
        request: ConfirmServiceRequest
    ) -> ServiceRequestResponse:

        try:

            now = datetime.now(timezone.utc).replace(tzinfo=None)

            # --------------------------------
            # Find existing staged request
            # --------------------------------

            service_request = None

            if request.service_request_id is not None:

                service_request = self.repository.get_by_id(request.service_request_id)

                if service_request is None:

                    raise ServiceRequestDoesNotExistError(
                        detail=(
                            f"Service request "
                            f"{request.service_request_id} not found"
                        )
                    )

                if service_request.status != ServiceRequestStatus.PENDING:

                    raise ServiceRequestStatusIsNotPendingError(
                        detail=(
                            f"Cannot confirm request in "
                            f"status {service_request.status}"
                        )
                    )

            # --------------------------------
            # Create request if it doesn't exist
            # --------------------------------

            if service_request is None:

                customer = self.customer_interface.find_or_create_customer(customer_request=request.customer_data)

                service_request = ServiceRequest(
                    customer_id=customer.id,
                    user_id=user_id,
                    device_type=request.device_type,
                    device_brand=request.device_brand,
                    device_model=request.device_model,
                    fault_description=request.fault_descriptions,
                    status=ServiceRequestStatus.PENDING,
                    created_at=now,
                    updated_at=now,
                )

                self.repository.create(service_request)
                self.db.flush()

            else:
                customer = service_request.customer

            # --------------------------------
            # Optional AI diagnosis
            # --------------------------------

            llm_diagnosis = service_request.llm_diagnosis

            if (
                llm_diagnosis is not None
                and request.diagnosis_verdict is not None
            ):
                llm_diagnosis.status = request.diagnosis_verdict

            # --------------------------------
            # Selected parts
            # --------------------------------

            for selection in request.selected_parts:

                if selection.part_id is None:
                    
                    self.request_part_interface.create_request(
                        request_id=service_request.id,
                        part_id=None,
                        part_name_snapshot=selection.part_name,
                        quantity=None,
                        is_stock_validated=False,
                    )

                    self.procurement_alert_interface.create_procurement_alert(
                        request_id=service_request.id,
                        part_id=None,
                        part_name_snapshot=selection.part_name,
                        is_resolved=False,
                        created_at=now,
                        alert_type=ProcurementAlertTypeReview.alert.NO_PART_MATCH,
                        alert_message=(
                            f"Service Request No. {service_request.id} created by "
                            f"{service_request.user_id} needs {selection.part_name} "
                            f"which no suitable part matches the recommendation "
                            f"on the spare part inventory"
                        ),
                    )

                    continue

                part = self.spare_part_interface.get_spare_part_by_id(selection.part_id)

                if part is None:

                    self.procurement_alert_interface.create_procurement_alert(
                        request_id=service_request.id,
                        part_id=None,
                        part_name_snapshot=selection.part_name,
                        is_resolved=False,
                        created_at=now,
                        alert_type=ProcurementAlertTypeReview.alert.PART_NOT_FOUND,
                        alert_message=(
                            f"Service Request No. {service_request.id} created by "
                            f"{service_request.user_id} needs {selection.part_name} "
                            f"which requested part record doesn't exist on the "
                            f"spare part inventory"
                        ),
                    )

                    continue


                in_stock = (
                    part.stock_quantity is not None
                    and part.stock_quantity >= selection.quantity
                )

                self.request_part_interface.create_request(
                    request_id=service_request.id,
                    part_id=part.id,
                    part_name_snapshot=part.part_name,
                    quantity=selection.quantity,
                    is_stock_validated=in_stock,
                )

                alert_type = (
                    ProcurementAlertTypeReview.alert.PART_SELECTED
                    if in_stock
                    else ProcurementAlertTypeReview.alert.INSUFFICIENT_STOCK
                )

                if in_stock:
                    alert_message = (
                        f"Service Request No. {service_request.id} requires "
                        f"{part.part_name} ({part.part_code}) "
                        f"from {part.shelf_location}."
                    )
                else:
                    alert_message = (
                        f"Service Request No. {service_request.id} requires "
                        f"{selection.quantity} units of {part.part_name} "
                        f"({part.part_code}), but available stock is insufficient."
                    )

                self.procurement_alert_interface.create_procurement_alert(
                    request_id=service_request.id,
                    part_id=part.id,
                    part_name_snapshot=part.part_name,
                    is_resolved=False,
                    created_at=now,
                    alert_type=alert_type,
                    alert_message=alert_message,
                )

            # --------------------------------
            # Finalize request
            # --------------------------------

            self.repository.update_service_request(
                now=now,
                stored_service_request=service_request,
                final_status=request.final_status,
                technician_notes=request.technician_notes
            )

            self.db.commit()
            self.db.refresh(service_request)

            # --------------------------------
            # Notify Customer Through Email
            # --------------------------------

            html = self.email_renderer.render(
                "service_request.html",

                preheader="Your service request has been created.",
                company_name="Lightyear Electrical Goods Trading",
                address="60 Burgos Street, Brgy. 3, Calamba City, 4027, Laguna, Philippines",
                first_name=customer.first_name,
                last_name=customer.last_name,
                intro="Your service request has been successfully created.",
                service_request_id=service_request.id,
                device_type=service_request.device_type,
                device_brand=service_request.device_brand,
                device_model=service_request.device_model,
                status=service_request.status,
                fault_description=service_request.fault_descriptions,
                notice_title="What happens next?",
                notice_body="A technician will review your service request and proceed with the necessary inspection.",
                regards="Thanks,",
                team="The LEGT Team",
                footer="This is an automated message. Please do not reply directly to this email."
            )

            message = EmailMessage(
                to=customer.email,
                subject="Service Request Created",
                body=(
                    "Your service request has been successfully created.\n\n"
                    f"Service Request #: {service_request.id}\n"
                    f"Device: {service_request.device_type}\n"
                    f"Brand: {service_request.device_brand}\n"
                    f"Model: {service_request.device_model}\n"
                    f"Status: {service_request.status}\n\n"
                    "Please wait for our team to contact you for further assistance."
                ),
                    html=html
            )

            # --------------------------------
            # Prepare the Matched Items
            # --------------------------------

            llm_recommendation = None
            matched_parts = []

            if llm_diagnosis is not None:
                llm_recommendation = llm_diagnosis.llm_recommendation

                if llm_recommendation is not None:
                    matched_parts = self.spare_part_interface.search_matched_spare_part(llm_recommendation.component)

                    in_stock = (
                        matched_parts.stock_quantity is not None
                        and matched_parts.stock_quantity >= 1
                    )

                    matched_spare_parts = MatchedSparePartPreview(
                        part_id=matched_parts.id,
                        part_name=matched_parts.name,
                        part_code=matched_parts.part_code,
                        device_model=matched_parts.device_model,
                        device_brand=matched_parts.device_brand,
                        specifications=matched_parts.specifications,
                        unit_cost=matched_parts.unit_cost,
                        stock_quantity=matched_parts.stock_quantity,
                        shelf_location=matched_parts.shelf_location,
                        image_url=matched_parts.image_url,
                        category_name=matched_parts.categories.name,
                        is_available=in_stock
                    )

                else:
                    matched_spare_parts = []


            return build_service_request_response(
                service_request=service_request,
                matched_parts=matched_spare_parts
            )

        except (
            ServiceRequestDoesNotExistError,
            ServiceRequestStatusIsNotPendingError
        ):

            self.db.rollback()
            raise

        except Exception as error:
            
            print(error)

            self.db.rollback()
            raise ServiceRequestFailedError() from error


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

            service_request = self.repository.get_by_id(
                service_request_id
            )

            if service_request is None:
                raise ServiceRequestDoesNotExistError(
                    detail=(
                        f"Service request "
                        f"{service_request_id} not found"
                    )
                )

            if service_request.status in (
                ServiceRequestStatus.COMPLETED,
                ServiceRequestStatus.UNSUCCESSFUL,
            ):
                raise ServiceRequestStatusIsNotPendingError(
                    detail=(
                        f"Cannot cancel request in "
                        f"status {service_request.status}"
                    )
                )

            now = datetime.now(timezone.utc).replace(tzinfo=None)

            diagnostic_status = "No AI diagnosis"

            if service_request.llm_diagnosis is not None:
                service_request.llm_diagnosis.status = (
                    DiagnosisVerdict.REJECTED
                )

                diagnostic_status = str(
                    service_request.llm_diagnosis.status
                )

            self.procurement_alert_interface.cancel_by_request(
                request_id=service_request.id,
                alert_message=(
                    f"Service Request No. {service_request.id} created by "
                    f"{service_request.user_id} with a diagnostic status of "
                    f"{diagnostic_status} has been cancelled."
                )
            )

            self.repository.update_service_request(
                now=now,
                stored_service_request=service_request,
                final_status=ServiceRequestStatus.UNSUCCESSFUL,
                technician_notes=None
            )

            self.db.commit()

        except (
            ServiceRequestDoesNotExistError, 
            ServiceRequestStatusIsNotPendingError
        ):
            self.db.rollback()
            raise

        except Exception as error:
            self.db.rollback()
            raise ServiceRequestFailedError() from error


    
    def get_all_service_requests(
        self,
        page: int,
        limit: int,
        search: str | None = None,
        status: str | None = None,
        created_date: date | None = None,
    ) -> ServiceRequestPageListResponse:
    
        service_requests, total = self.repository.get_all(
            page=page,
            limit=limit,
            search=search,
            status=status,
            created_date=created_date
        )

        items = [
            ServiceRequestListResponse(
                id=service_request.id,
                customer_name=(
                    f"{service_request.customers.first_name} "
                    f"{service_request.customers.last_name}"
                ),
                device_type=service_request.device_type,
                device_brand=service_request.device_brand,
                device_model=service_request.device_model,
                technician_name=(
                    f"{service_request.users.first_name} "
                    f"{service_request.users.last_name}"
                ),
                created_at=service_request.created_at,
                status=service_request.status,
            )
            for service_request in service_requests
        ]

        pages = ceil(total / limit) if total else 0

        return {
            "items": items,
            "page": page,
            "limit": limit,
            "total": total,
            "pages": pages,
        }


    def get_service_request_details(
        self,
        service_request_id: int
    ) -> ServiceRequestDetailsResponse:

        service_request = self.repository.get_specific_detail(service_request_id)

        customer_detail = CustomerServiceRequestDetails(
            id=service_request.customers.id,
            name=(
                f"{service_request.customers.first_name} "
                f"{service_request.customers.last_name}"
            )
        )

        technician_detail = UserServiceRequestDetails(
            id=service_request.users.id,
            name=(
                f"{service_request.users.first_name} "
                f"{service_request.users.last_name}"
            )
        )

        requested_part_detail = [
            RequestPartDetails(
                quantity=request_part.quantity,
                part_name=request_part.part_name_snapshot,
                validated=request_part.is_stock_validated,
            )
            for request_part in service_request.request_parts
        ]

        item = ServiceRequestDetailsResponse(
            id=service_request.id,
            device_type=service_request.device_type,
            device_brand=service_request.device_brand,
            device_model=service_request.device_model,
            fault_descriptions=service_request.fault_description,
            status=service_request.status,
            diagnosis=service_request.llm_diagnosis.response,
            customer=customer_detail,
            technician=technician_detail,
            requested_part=requested_part_detail
        )

        return item