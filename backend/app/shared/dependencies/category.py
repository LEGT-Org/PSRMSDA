from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.shared.session import get_db

from app.modules.category.repository import CategoryRepository
from app.modules.category.service import CategoryService


def get_category_repository(
    db: Annotated[
        Session,
        Depends(get_db)
    ]
) -> CategoryRepository:

    return CategoryRepository(db)


def get_category_service(
    repository: Annotated[
        CategoryRepository,
        Depends(get_category_repository)
    ],
    db: Annotated[
        Session,
        Depends(get_db)
    ]
) -> CategoryService:

    return CategoryService(
        repository=repository,
        db=db
    )
