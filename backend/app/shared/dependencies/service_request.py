from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.shared.dependencies.external_service.email_service import get_email_service, get_email_renderer
from app.shared.dependencies.procurement_alert import get_procurement_alert_service
from app.shared.infrastructure.email import EmailService, JinjaEmailRendered
from app.shared.dependencies.llm_diagnosis import get_llm_diagnosis_service
from app.shared.dependencies.request_part import get_request_part_service
from app.shared.dependencies.spare_part import get_spare_part_service
from app.shared.dependencies.customer import get_customer_service
from app.shared.dependencies.user import get_user_service
from app.shared.session import get_db

from app.modules.service_request.repository import ServiceRequestRepository
from app.modules.procurement_alert.service import ProcurementAlertService
from app.modules.service_request.service import ServiceRequestService
from app.modules.llm_diagnosis.service import LLMDiagnosisService
from app.modules.request_part.service import RequestPartService
from app.modules.spare_part.service import SparePartService
from app.modules.customer.service import CustomerService


def get_service_request_repository(
    db: Annotated[
        Session,
        Depends(get_db)
    ]
) -> ServiceRequestRepository:

    return ServiceRequestRepository(db)


def get_service_request_service(
    repository: Annotated[
        ServiceRequestService,
        Depends(get_service_request_repository)
    ],
    llm_diagnosis_interface: Annotated[
        LLMDiagnosisService,
        Depends(get_llm_diagnosis_service)
    ],
    procurement_alert_interface: Annotated[
        ProcurementAlertService,
        Depends(get_procurement_alert_service)
    ],
    request_part_interface: Annotated[
        RequestPartService,
        Depends(get_request_part_service)
    ],
    spare_part_interface: Annotated[
        SparePartService,
        Depends(get_spare_part_service)
    ],
    customer_interface: Annotated[
        CustomerService,
        Depends(get_customer_service)
    ],
    email_service: Annotated[
        EmailService,
        Depends(get_email_service)
    ],
    email_renderer: Annotated[
        JinjaEmailRendered,
        Depends(get_email_renderer)
    ],
    db: Annotated[
        Session,
        Depends(get_db)
    ]
) -> ServiceRequestService:

    return ServiceRequestService(
        repository=repository,
        llm_diagnosis_interface=llm_diagnosis_interface,
        procurement_alert_interface=procurement_alert_interface,
        request_part_interface=request_part_interface,
        spare_part_interface=spare_part_interface,
        customer_interface=customer_interface,
        email_renderer=email_renderer,
        email_service=email_service,
        db=db
    )