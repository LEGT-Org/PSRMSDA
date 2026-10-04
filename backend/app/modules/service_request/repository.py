from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.service_request.schema import ServiceRequestStatus
from app.modules.service_request.model import ServiceRequest


class ServiceRequestRepository:

    def __init__(self, db: Session):

        self.db = db

    def create(
        self, 
        service_request: ServiceRequest
    ) -> ServiceRequest:

        self.db.add(service_request)
        return service_request


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

