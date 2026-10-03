from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.shared.session import get_db

from app.modules.request_part.repository import RequestPartRepository
from app.modules.request_part.service import RequestPartService


def get_request_part_provider(
    db: Annotated[
        Session,
        Depends(get_db)
    ]
) -> RequestPartRepository:

    return RequestPartRepository(db)


def get_request_part_service(
    repository: Annotated[
        RequestPartRepository,
        Depends(get_request_part_provider)
    ],
    db: Annotated[
        Session,
        Depends(get_db)
    ]
) -> RequestPartService:

    return RequestPartService(
        repository=repository,
        db=db
    )