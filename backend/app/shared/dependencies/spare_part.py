from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.shared.dependencies.category import get_category_service
from app.shared.session import get_db

from app.modules.spare_part.repository import SparePartRepository
from app.modules.spare_part.service import SparePartService
from app.modules.category.service import CategoryService


def get_spare_part_provider(
    db: Annotated[
        Session,
        Depends(get_db)
    ]
) -> SparePartRepository:

    return SparePartRepository(db)


def get_spare_part_service(
    repository: Annotated[
        SparePartRepository,
        Depends(get_spare_part_provider)
    ],
    category_interface: Annotated[
        CategoryService,
        Depends(get_category_service)
    ],
    db: Annotated[
        Session,
        Depends(get_db)
    ]
) -> SparePartService:

    return SparePartService(
        repository=repository,
        category_interface=category_interface,
        db=db
    )