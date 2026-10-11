from datetime import date, time, datetime, timedelta
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.modules.service_request.schema import ServiceRequestStatus
from app.modules.service_request.model import ServiceRequest
from app.modules.llm_diagnosis.model import LLMDiagnosis
from app.modules.request_part.model import RequestPart
from app.modules.customer.model import Customer
from app.modules.user.model import User

from app.modules.service_request.schema import LLMDiagnosisStatusPreview


class ServiceRequestRepository:

    def __init__(self, db: Session):

        self.db = db

    def create(
        self, 
        service_request: ServiceRequest
    ) -> ServiceRequest:

        self.db.add(service_request)
        return service_request


    def get_all(
        self,
        page: int,
        limit: int,
        search: str | None = None,
        status: str | None = None,
        created_date: date | None = None,
    ) -> tuple[list[ServiceRequest], int]:

        statement = (
            select(ServiceRequest)
            .join(Customer, ServiceRequest.customer_id == Customer.id)
            .join(User, ServiceRequest.user_id == User.id)
            .join(ServiceRequest.llm_diagnosis)
            .where(LLMDiagnosis.status != LLMDiagnosisStatusPreview.DRAFT)
        )

        if search:
            search_value = f"%{search.strip()}%"

            statement = statement.where(
                or_(
                    ServiceRequest.device_type.ilike(search_value),
                    ServiceRequest.device_brand.ilike(search_value),
                    ServiceRequest.device_model.ilike(search_value),

                    Customer.first_name.ilike(search_value),
                    Customer.last_name.ilike(search_value),

                    User.first_name.ilike(search_value),
                    User.last_name.ilike(search_value),
                )
        )

        if status:
            statement = statement.where(ServiceRequest.status == status,)

        if created_date:
            start_date = datetime.combine(created_date, time.min)
            end_date = start_date + timedelta(days=1)

            statement = statement.where(
                ServiceRequest.created_at >= start_date,
                ServiceRequest.created_at < end_date,
            )

        count_statement = select(func.count()).select_from(statement.subquery())
        total = self.db.scalar(count_statement) or 0

        statement = (statement
            .order_by(ServiceRequest.created_at.desc())
            .offset((page - 1) * limit)
            .limit(limit)
        )

        service_requests = list(self.db.scalars(statement).all())

        return service_requests, total

        
    def get_specific_detail(
        self,
        service_request_id: int
    ) -> ServiceRequest:

        statement = (
            select(ServiceRequest)
            .join(Customer, ServiceRequest.customer_id == Customer.id)
            .join(User, ServiceRequest.user_id == User.id)
            .outerjoin(LLMDiagnosis, LLMDiagnosis.request_id == ServiceRequest.id)
            .outerjoin(RequestPart, RequestPart.request_id == ServiceRequest.id)
            .where(ServiceRequest.id == service_request_id)
        )

        return self.db.execute(statement).scalars().first()


    def get_by_id(
        self,
        service_request_id: int
    ) -> ServiceRequest:

        statement = select(ServiceRequest).where(ServiceRequest.id == service_request_id)

        return self.db.scalar(statement)
        

    def update_service_request(
        self,
        now: datetime,
        stored_service_request: ServiceRequest,
        final_status: ServiceRequestStatus,
        technician_notes: str | None = None
    ) -> None:

        stored_service_request.technician_notes = technician_notes
        stored_service_request.status = final_status
        stored_service_request.updated_at = now


    def final_confirmation(
        self,
        now: datetime,
        approved_by: int,
        stored_service_request: ServiceRequest,
        final_status: ServiceRequestStatus,
    ) -> None:

        stored_service_request.status = final_status
        stored_service_request.approved_by_id = approved_by
        stored_service_request.updated_at = now

