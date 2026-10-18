from math import ceil
from datetime import date, datetime, timezone
from sqlalchemy.orm import Session

from app.modules.service_request.helper import build_service_request_response
from app.modules.service_request.repository import ServiceRequestRepository
from app.modules.service_request.model import ServiceRequest
from app.modules.service_request.schema import (
    ServiceRequestPageListResponse,
    ServiceRequestDetailsResponse,
    ServiceRequestFinalizeRequest,
    CustomerServiceRequestDetails,
    LLMDiagnosticRequestPreview,
    ProcurementAlertTypePreview,
    ServiceRequestListResponse,
    UserServiceRequestDetails,
    LLMDiagnosisStatusPreview,
    LLMRecommendedSparePart,
    ProcurementAlertRequest,
    MatchedSparePartPreview,
    ServiceRequestResponse,
    CustomerRequestPreview,
    ConfirmServiceRequest,
    ServiceRequestStatus,
    RequestPartDetails,
    RequestPartRequest,
    UserRolePreview,
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
    EmailService,
    EmailMessage
)

from app.shared.exception import (
    ServiceRequestStatusCanOnlyBeCompletedOrUnsuccessfulError,
    RequestPartQuantityUsedMustGreaterThanZeroError,
    ServiceRequestStatusCanOnlyModifiedAgainError,
    RequestPartInvalidUsageConfirmationError,
    RequestPartQuantityUsedMustBeZeroError,
    ServiceRequestStatusIsNotPendingError,
    ServiceRequestDoesNotExistError,
    RequestPartDuplicationError,
    ServiceRequestFailedError,
    EmailServiceFailedError
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

            matched_spare_parts = []
            llm_recommended_part = None

            if llm_recommendation is not None:
                
                matched_parts = self.spare_part_interface.search_matched_spare_part(
                    part_name=llm_recommendation.component,
                    device_type=service_request.device_type
                )

                print("LLM recommendation:", llm_recommendation.component)
                print("Device type:", service_request.device_type)
                print("Matched parts:", [
                    part.part_name for part in matched_parts
                ])

                for part in matched_parts:
                    in_stock = (
                        part.stock_quantity is not None
                        and part.stock_quantity >= 1
                    )

                    matched_spare_parts.append(
                      MatchedSparePartPreview(
                            part_id=part.id,
                            part_name=part.part_name,
                            part_code=part.part_code,
                            device_model=part.device_model,
                            device_brand=part.device_brand,
                            specifications=part.specifications,
                            unit_cost=part.unit_cost,
                            stock_quantity=part.stock_quantity,
                            shelf_location=part.shelf_location,
                            image_url=part.image_url,
                            category_name=part.categories.name,
                            is_available=in_stock,
                        )
                    )

                llm_recommended_part = LLMRecommendedSparePart(
                    llm_component=llm_recommendation.component,
                    llm_reason=llm_recommendation.reason,
                    compatibility_requirements=(
                        llm_recommendation.compatibility_requirements
                    ),
                )

            print("Matched parts count:", len(matched_spare_parts))
            print("Matched parts response:", matched_spare_parts)
                
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
                matched_parts=matched_spare_parts,
                created_at=service_request.created_at
            )

        except Exception as error:

            self.db.rollback()

            print(f"Diagnosis failed: {error}")
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
                customer = service_request.customers

            llm_diagnosis = service_request.llm_diagnosis

            if (
                llm_diagnosis is not None
                and request.diagnosis_verdict is not None
            ):
                llm_diagnosis.status = request.diagnosis_verdict.ACCEPTED

            if not request.selected_parts:
                self.procurement_alert_interface.create_procurement_alert(
                    data=ProcurementAlertRequest(
                        request_id=service_request.id,
                        part_id=None,
                        part_name_snapshot=None,
                        is_resolved=False,
                        created_at=now,
                        alert_type=ProcurementAlertTypePreview.NO_PART_MATCH,
                        alert_message=(
                            f"Service Request No. {service_request.id} "
                            "has no selected spare parts. Admin review is required."
                        ),
                    )
                )

            for selection in request.selected_parts:

                if selection.part_id is None:
                    
                    self.request_part_interface.create_request(
                        data=RequestPartRequest(
                            request_id=service_request.id,
                            part_id=None,
                            quantity=None,
                            quantity_used=None,
                            part_name_snapshot=selection.part_name,
                            is_stock_validated=False,
                            part_used=False
                        )
                    )

                    self.procurement_alert_interface.create_procurement_alert(
                        data=ProcurementAlertRequest(
                            request_id=service_request.id,
                            part_id=None,
                            part_name_snapshot=selection.part_name,
                            is_resolved=False,
                            created_at=now,
                            alert_type=ProcurementAlertTypePreview.NO_PART_MATCH,
                            alert_message=(
                                f"Service Request No. {service_request.id} created by "
                                f"{service_request.user_id} needs {selection.part_name} "
                                f"which no suitable part matches the recommendation "
                                f"on the spare part inventory"
                            ),
                        )
                    )

                    continue

                part = self.spare_part_interface.get_spare_part_specific_details(selection.part_id)

                if part is None:

                    self.procurement_alert_interface.create_procurement_alert(
                        data=ProcurementAlertRequest(
                            request_id=service_request.id,
                            part_id=None,
                            part_name_snapshot=selection.part_name,
                            is_resolved=False,
                            created_at=now,
                            alert_type=ProcurementAlertTypePreview.PART_NOT_FOUND,
                            alert_message=(
                                f"Service Request No. {service_request.id} created by "
                                f"{service_request.user_id} needs {selection.part_name} "
                                f"which requested part record doesn't exist on the "
                                f"spare part inventory"
                            )
                        )
                    )

                    continue


                in_stock = (
                    part.stock_quantity is not None
                    and part.stock_quantity >= selection.quantity
                )

                self.request_part_interface.create_request(
                    data=RequestPartRequest(
                        request_id=service_request.id,
                        part_id=part.id,
                        quantity=selection.quantity,
                        quantity_used=None,
                        part_name_snapshot=part.part_name,
                        is_stock_validated=in_stock,
                        part_used=False
                    )
                )

                alert_type = (
                    ProcurementAlertTypePreview.PART_SELECTED
                    if in_stock
                    else ProcurementAlertTypePreview.INSUFFICIENT_STOCK
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
                    data=ProcurementAlertRequest(
                        request_id=service_request.id,
                        part_id=part.id,
                        part_name_snapshot=part.part_name,
                        is_resolved=False,
                        created_at=now,
                        alert_type=alert_type,
                        alert_message=alert_message
                    )
                )

            self.repository.update_service_request(
                now=now,
                stored_service_request=service_request,
                final_status=request.final_status,
                technician_notes=request.technician_notes
            )

            self.procurement_alert_interface.create_procurement_alert(
                data=ProcurementAlertRequest(
                    request_id=service_request.id,
                    part_id=None,
                    part_name_snapshot=(
                        llm_diagnosis.llm_recommendation.component
                        if (
                            llm_diagnosis is not None
                            and llm_diagnosis.llm_recommendation is not None
                        )
                        else None
                    ),
                    is_resolved=False,
                    created_at=now,
                    alert_type=ProcurementAlertTypePreview.REQUEST_STAGE,
                    alert_message=(
                        f"Service Request No. {service_request.id}, created by "
                        f"user {service_request.user_id}, has been confirmed "
                        "and is ready for admin review."
                    ),
                )
            )

            self.db.commit()
            self.db.refresh(service_request)

            try:

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
                    fault_description=service_request.fault_description,
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

            except Exception as email_error:

                print(f"Failed to send finalization email: {email_error}")
                raise EmailServiceFailedError() from error

            self.email_service.send(message)

            llm_recommendation = None
            matched_spare_parts = []
            llm_recommended_part = None

            if llm_diagnosis is not None:
                llm_recommendation = llm_diagnosis.llm_recommendation

            if llm_recommendation is not None:
                matched_parts = self.spare_part_interface.search_matched_spare_part(
                    part_name=llm_recommendation.component,
                    device_type=service_request.device_type
                )

                for part in matched_parts:
                    in_stock = (
                        part.stock_quantity is not None
                        and part.stock_quantity >= 1
                    )

                    matched_spare_parts.append(
                        MatchedSparePartPreview(
                            part_id=part.id,
                            part_name=part.part_name,
                            part_code=part.part_code,
                            device_model=part.device_model,
                            device_brand=part.device_brand,
                            specifications=part.specifications,
                            unit_cost=part.unit_cost,
                            stock_quantity=part.stock_quantity,
                            shelf_location=part.shelf_location,
                            image_url=part.image_url,
                            category_name=part.categories.name,
                            is_available=in_stock,
                        )
                    )

                llm_recommended_part = LLMRecommendedSparePart(
                    llm_component=llm_recommendation.component,
                    llm_reason=llm_recommendation.reason,
                    compatibility_requirements=(
                        llm_recommendation.compatibility_requirements
                    ),
                )


            return build_service_request_response(
                service_request=service_request,
                matched_parts=matched_spare_parts
            )

        except (
            ServiceRequestStatusIsNotPendingError,
            ServiceRequestDoesNotExistError
        ):

            self.db.rollback()
            raise

        except Exception as error:

            self.db.rollback()

            print(f"Confirm service request failed: {error}")
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
                    detail=f"Service request {service_request_id} not found"
                )

            if service_request.status in {
                ServiceRequestStatus.COMPLETED,
                ServiceRequestStatus.UNSUCCESSFUL,
            }:
                raise ServiceRequestStatusIsNotPendingError(
                    detail=(
                        f"Cannot cancel request in "
                        f"status {service_request.status}"
                    )
                )

            now = datetime.now(timezone.utc).replace(tzinfo=None)

            diagnostic_status = "No AI diagnosis"

            if service_request.llm_diagnosis is not None:
                service_request.llm_diagnosis.status = (LLMDiagnosisStatusPreview.REJECTED)
                diagnostic_status = (service_request.llm_diagnosis.status.value)

            self.procurement_alert_interface.create_procurement_alert(
                data=ProcurementAlertRequest(
                    request_id=service_request.id,
                    part_id=None,
                    part_name_snapshot=(
                        service_request.llm_diagnosis.llm_recommendation.component
                        if (
                            service_request.llm_diagnosis is not None
                            and service_request.llm_diagnosis.llm_recommendation is not None
                        )
                        else None
                    ),
                    is_resolved=False,
                    created_at=now,
                    alert_type=ProcurementAlertTypePreview.REQUEST_STAGE,
                    alert_message=(
                        f"Service Request No. {service_request.id}, created by "
                        f"user {service_request.user_id}, has been cancelled. "
                        f"Diagnostic status: {diagnostic_status}."
                    ),
                )
            )

            self.repository.cancel_service_request(
                now=now,
                stored_service_request=service_request,
                final_status=ServiceRequestStatus.UNSUCCESSFUL,
                technician_notes=None,
            )

            self.db.commit()

        except (
            ServiceRequestStatusIsNotPendingError,
            ServiceRequestDoesNotExistError
        ):

            self.db.rollback()
            raise

        except Exception as error:

            self.db.rollback()

            print(f"Cancel service request failed: {error}")
            raise ServiceRequestFailedError() from error


    """  
    
        Get the List of Service Request
    
    """
    
    def get_all_service_requests(
        self,
        page: int,
        limit: int,
        search: str | None = None,
        status: ServiceRequestStatus | None = None,
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


    """  
    
        Get the Service Request Details
    
    """

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
                id=request_part.id,
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
            diagnosis=(
                service_request.llm_diagnosis.response
                if service_request.llm_diagnosis
                else None
            ),
            customer=customer_detail,
            technician=technician_detail,
            requested_part=requested_part_detail
        )

        return item


    """  
    
        Finalize Service Request
    
    """

    def final_service_request_confirmation(
        self,
        approved_by: UserSchema,
        service_request_id: int,
        request_data: ServiceRequestFinalizeRequest
    ) -> None:

        try:

            now = datetime.now(timezone.utc).replace(tzinfo=None)
            stored_service_request = self.repository.get_by_id(service_request_id)

            if stored_service_request is None:
                raise ServiceRequestDoesNotExistError(
                    detail=f"Service request {service_request_id} not found"
                )

            final_statuses = {
                ServiceRequestStatus.COMPLETED,
                ServiceRequestStatus.UNSUCCESSFUL
            }

            is_admin = approved_by.role == UserRolePreview.ADMIN
            is_finalized = stored_service_request.status in final_statuses

            if request_data.status not in final_statuses:
                raise ServiceRequestStatusCanOnlyBeCompletedOrUnsuccessfulError(
                    detail=(
                        "Final confirmation status can only be "
                        f"{ServiceRequestStatus.COMPLETED} or "
                        f"{ServiceRequestStatus.UNSUCCESSFUL}."
                    )
                )

            if is_finalized and not is_admin:
                raise ServiceRequestStatusCanOnlyModifiedAgain(
                    detail=(
                        f"Service request {service_request_id} has already "
                        f"been finalized."
                    )
                )

            usage_by_id = {
                item.request_part_id: item
                for item in request_data.parts_usage
            }

            if len(usage_by_id) != len(request_data.parts_usage):
                raise RequestPartDuplicationError()

            request_data_part_ids = {
                item.request_part_id
                for item in request_data.parts_usage
            }

            request_parts_by_id = {
                request_part.id: request_part
                for request_part in stored_service_request.request_parts
            }

            if set(usage_by_id) != set(request_parts_by_id):
                raise RequestPartInvalidUsageConfirmationError()

            for usage in request_data.parts_usage:
                if usage.part_used and (
                    usage.quantity_used is None 
                    or usage.quantity_used <= 0
                ):
                    raise RequestPartQuantityUsedMustGreaterThanZeroError()

                if not usage.part_used and usage.quantity_used != 0:
                    raise RequestPartQuantityUsedMustBeZeroError()

            request_parts_to_update = [
                request_part
                for request_part in stored_service_request.request_parts
                if request_part.id in request_data_part_ids
            ]

            for request_part in request_parts_to_update:
                usage = usage_by_id[request_part.id]

                previous_quantity = (
                    request_part.quantity_used
                    if request_part.parts_used and request_part.quantity_used is not None
                    else 0
                )

                new_quantity = (
                    usage.quantity_used
                    if usage.part_used and usage.quantity_used is not None
                    else 0
                )

                quantity_difference = new_quantity - previous_quantity

                if quantity_difference != 0 and request_part.part_id is not None:

                    if quantity_difference > 0:
                        remaining_stock = self.spare_part_interface.deduct_spare_part_quantity(
                            part_id=request_part.part_id,
                            quantity_used=quantity_difference,
                        )

                        if remaining_stock <= 0:
                            self.procurement_alert_interface.create_procurement_alert(
                                data=ProcurementAlertRequest(
                                    request_id=stored_service_request.id,
                                    part_id=request_part.part_id,
                                    part_name_snapshot=request_part.part_name_snapshot,
                                    is_resolved=False,
                                    created_at=now,
                                    alert_type=ProcurementAlertTypePreview.FINALIZED_REQUEST,
                                    alert_message=(
                                        f"Spare part '{request_part.part_name_snapshot}' is out of stock "
                                        f"after finalizing service request No. {stored_service_request.id}."
                                    ),
                                )
                            )

                    else:
                        self.spare_part_interface.add_spare_part_quantity(
                            part_id=request_part.part_id,
                            quantity_used=abs(quantity_difference),
                        )

                request_part.parts_used = usage.part_used
                request_part.quantity_used = usage.quantity_used

            self.repository.final_confirmation(
                now=now,
                approved_by=approved_by.id,
                stored_service_request=stored_service_request,
                final_status=request_data.status
            )

            self.procurement_alert_interface.create_procurement_alert(
                data=ProcurementAlertRequest(
                    request_id=stored_service_request.id,
                    part_id=None,
                    part_name_snapshot=None,
                    is_resolved=False,
                    created_at=now,
                    alert_type=ProcurementAlertTypePreview.FINALIZED_REQUEST,
                    alert_message=(
                        f"Service request No. {stored_service_request.id} "
                        f"has been finalized as {request_data.status.value}."
                    ),
                )
            )


            self.db.commit()
            self.db.refresh(stored_service_request)

            try:
                
                html = self.email_renderer.render(
                    "service_request.html",
                    preheader="Your service request has been finalized.",
                    company_name="Lightyear Electrical Goods Trading",
                    address="60 Burgos Street, Brgy. 3, Calamba City, 4027, Laguna, Philippines",
                    first_name=stored_service_request.customers.first_name,
                    last_name=stored_service_request.customers.last_name,
                    intro="Your service request has been finalized.",
                    service_request_id=stored_service_request.id,
                    device_type=stored_service_request.device_type,
                    device_brand=stored_service_request.device_brand,
                    device_model=stored_service_request.device_model,
                    status=stored_service_request.status.value,
                    fault_description=stored_service_request.fault_description,
                    notice_title="Final Service Request Status",
                    notice_body=(
                        "Good news! Your device is repaired and ready to be picked up. "
                        "Please visit our store to collect your device."
                        if stored_service_request.status == ServiceRequestStatus.COMPLETED
                        else (
                            "Your service request has been marked as unsuccessful. "
                            "Please contact our team to discuss the results and next steps."
                        )
                    ),
                    regards="Thanks,",
                    team="The LEGT Team",
                    footer=(
                        "This is an automated message. "
                        "Please do not reply directly to this email."
                    ),
                )

                message = EmailMessage(
                    to=stored_service_request.customers.email,
                    subject="Service Request Finalized",
                    body=(
                        "Your service request has been finalized.\n\n"
                        f"Service Request #: {stored_service_request.id}\n"
                        f"Device: {stored_service_request.device_type}\n"
                        f"Brand: {stored_service_request.device_brand}\n"
                        f"Model: {stored_service_request.device_model}\n"
                        f"Status: {stored_service_request.status.value}\n\n"
                        "Please contact our team if you have any questions."
                    ),
                    html=html,
                )

                self.email_service.send(message)

            except Exception as email_error:

                print(f"Failed to send finalization email: {email_error}")
                raise EmailServiceFailedError() from error

        except (
            ServiceRequestStatusCanOnlyBeCompletedOrUnsuccessfulError,
            RequestPartQuantityUsedMustGreaterThanZeroError,
            ServiceRequestStatusCanOnlyModifiedAgainError,
            RequestPartInvalidUsageConfirmationError,
            RequestPartQuantityUsedMustBeZeroError,
            ServiceRequestDoesNotExistError,
            RequestPartDuplicationError,
        ):

            self.db.rollback()
            raise

        except Exception as error:

            self.db.rollback()

            print(f"Status final confirmation failed: {error}")
            raise ServiceRequestFailedError() from error


    """  
    
        Update Reqular Service Request Status

    """

    def update_service_request_status(
        self,
        service_request_id: int,
        status: ServiceRequestStatus,
        updated_by: UserSchema,
    ) -> None:

        try:

            service_request = self.repository.get_by_id(service_request_id)

            if service_request is None:
                raise ServiceRequestDoesNotExistError(
                    detail=f"Service request {service_request_id} not found"
                )

            final_statuses = {
                ServiceRequestStatus.COMPLETED,
                ServiceRequestStatus.UNSUCCESSFUL,
            }

            regular_statuses = {
                ServiceRequestStatus.PENDING,
                ServiceRequestStatus.IN_PROGRESS,
                ServiceRequestStatus.FOR_FURTHER_INSPECTION,
            }

            # Final statuses must go through final confirmation.
            if status not in regular_statuses:
                raise ServiceRequestStatusCanOnlyBeCompletedOrUnsuccessfulError(
                    detail=(
                        "Completed and Unsuccessful must be set through "
                        "the final-confirmation endpoint."
                    )
                )

            is_finalized = service_request.status in final_statuses
            is_admin = updated_by.role == UserRolePreview.ADMIN
            now = datetime.now(timezone.utc).replace(tzinfo=None)

            if service_request.status == status:
                return

            # Only admins can reopen finalized requests, and only as In Progress.
            if is_finalized:

                if not is_admin:
                    raise ServiceRequestStatusCanOnlyModifiedAgainError(
                        detail=(
                            f"Service request {service_request_id} "
                            "has already been finalized."
                        )
                    )

                if status != ServiceRequestStatus.IN_PROGRESS:
                    raise ServiceRequestStatusCanOnlyModifiedAgainError(
                        detail=(
                            "A finalized service request can only be "
                            "reopened as In Progress."
                        )
                    )

                self.repository.update_service_request(
                    now=now,
                    stored_service_request=service_request,
                    final_status=status,
                    technician_notes=service_request.technician_notes,
                )

                self.procurement_alert_interface.create_procurement_alert(
                    ProcurementAlertRequest(
                        request_id=service_request_id,
                        part_id=None,
                        part_name_snapshot=None,
                        alert_type=ProcurementAlertTypePreview.REQUEST_STAGE,
                        alert_message=(
                            f"Service Request No. {service_request_id} "
                            f"has been reopened by an admin and set to "
                            f"{status.value}."
                        ),
                        created_at=now,
                    )
                )

                self.db.commit()

                return

            self.repository.update_service_request(
                now=now,
                stored_service_request=service_request,
                final_status=status,
                technician_notes=service_request.technician_notes,
            )

            self.procurement_alert_interface.create_procurement_alert(
                ProcurementAlertRequest(
                    request_id=service_request_id,
                    part_id=None,
                    part_name_snapshot=None,
                    alert_type=ProcurementAlertTypePreview.REQUEST_STAGE,
                    alert_message=(
                        f"Service Request No. {service_request_id} "
                        f"status updated to {status.value}."
                    ),
                    created_at=now,
                )
            )

            self.db.commit()

        except (
            ServiceRequestStatusCanOnlyBeCompletedOrUnsuccessfulError,
            ServiceRequestStatusCanOnlyModifiedAgainError,
            ServiceRequestDoesNotExistError
        ):

            print(ServiceRequestStatusCanOnlyBeCompletedOrUnsuccessfulError)
            print(ServiceRequestStatusCanOnlyModifiedAgainError)
            print(ServiceRequestDoesNotExistError)

            self.db.rollback()
            raise

        except Exception as error:

            self.db.rollback()

            print(f"Status update failed: {error}") 
            raise ServiceRequestFailedError() from error