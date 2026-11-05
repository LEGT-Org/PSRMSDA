from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.shared.dependencies.procurement_alert import get_procurement_alert_service
from app.shared.dependencies.category import get_category_service
from app.shared.session import get_db

from app.modules.spare_part.repository import SparePartRepository
from app.modules.spare_part.service import SparePartService
from app.modules.category.service import CategoryService
from app.modules.procurement_alert.service import ProcurementAlertService


def get_spare_part_repository(
    db: Annotated[
        Session,
        Depends(get_db)
    ]
) -> SparePartRepository:

    return SparePartRepository(db)


def get_spare_part_service(
    repository: Annotated[
        SparePartRepository,
        Depends(get_spare_part_repository)
    ],
    category_interface: Annotated[
        CategoryService,
        Depends(get_category_service)
    ],
    procurement_alert_interface: Annotated[
        ProcurementAlertService,
        Depends(get_procurement_alert_service)
    ],
    db: Annotated[
        Session,
        Depends(get_db)
    ]
) -> SparePartService:

    return SparePartService(
        repository=repository,
        category_interface=category_interface,
        procurement_alert_interface=procurement_alert_interface,
        db=db
    )
