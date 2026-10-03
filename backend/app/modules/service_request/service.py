from sqlalchemy.orm import Session

from app.modules.service_request.repository import ServiceRequestRepository
from app.modules.service_request.schema import (
    LLMDiagnosticRequestPreview, 
    CustomerRequestPreview
)

from app.modules.service_request.interface import (
    LLMDiagnosisInterface,
    CustomerInterface
)


class ServiceRequestService:

    def __init__(
        self,
        repository: ServiceRequestRepository,
        llm_diagnosis_interface: LLMDiagnosisInterface,
        customer_interface: CustomerInterface,
        db: Session
    ):

        self.repository = repository
        self.llm_diagnosis_interface = llm_diagnosis_interface
        self.customer_interface = customer_interface
        self.db = db

    
    async def run_ai_diagnosis(
        self,
        request: LLMDiagnosticRequestPreview,
        customer_data: CustomerRequestPreview
    )