from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.shared.session import get_db

from app.modules.procurement_alert.repository import ProcurementAlertRepository
from app.modules.procurement_alert.service import ProcurementAlertService


def get_procurement_alert_repository(
    db: Annotated[
        Session,
        Depends(get_db)
    ]
) -> ProcurementAlertRepository:

    return ProcurementAlertRepository(db)


def get_procurement_alert_service(
    repository: Annotated[
        ProcurementAlertRepository,
        Depends(get_procurement_alert_repository)
    ],
    db: Annotated[
        Session,
        Depends(get_db)
    ]
) -> ProcurementAlertService:

    return ProcurementAlertService(
        repository=repository,
        db=db
    )