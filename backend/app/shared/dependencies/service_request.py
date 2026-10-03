from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.shared.dependencies.llm_diagnosis import get_llm_diagnosis_service
from app.shared.dependencies.customer import get_customer_service
from app.shared.session import get_db

from app.modules.service_request.repository import ServiceRequestRepository
from app.modules.service_request.service import ServiceRequestService
from app.modules.llm_diagnosis.service import LLMDiagnosisService
from app.modules.customer.service import CustomerService


def get_service_request_provider(
    db: Annotated[
        Session,
        Depends(get_db)
    ]
) -> ServiceRequestRepository:

    return ServiceRequestRepository(db)


def get_service_request_service(
    repository: Annotated[
        ServiceRequestService,
        Depends(get_service_request_provider)
    ],
    llm_diagnosis_interface: Annotated[
        LLMDiagnosisService,
        Depends(get_llm_diagnosis_service)
    ],
    customer_interface: Annotated[
        CustomerService,
        Depends(get_customer_service)
    ],
    db: Annotated[
        Session,
        Depends(get_db)
    ]
) -> ServiceRequestService:

    return ServiceRequestService(
        repository=repository,
        llm_diagnosis_interface=llm_diagnosis_interface,
        customer_interface=customer_interface,
        db=db
    )