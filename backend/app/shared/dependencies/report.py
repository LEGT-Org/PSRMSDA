from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.shared.session import get_db

from app.modules.report.repository import ReportRepository
from app.modules.report.service import ReportService


def get_report_repository(
    db: Annotated[
        Session,
        Depends(get_db)
    ]
) -> ReportRepository:

    return ReportRepository(db)


def get_report_service(
    repository: Annotated[
        ReportRepository,
        Depends(get_report_repository)
    ],
    db: Annotated[
        Session,
        Depends(get_db)
    ]
) -> ReportService:

    return ReportService(
        repository=repository,
        db=db
    )
