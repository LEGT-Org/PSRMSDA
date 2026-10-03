from sqlalchemy import select
from sqlalchemy.orm import Session

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
