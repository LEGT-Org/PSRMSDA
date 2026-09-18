from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.shared.session import get_db
from app.modules.user.repository import UserRepository
from app.modules.user.service import UserService


def get_user_repository(
    db: Annotated[
        Session, 
        Depends(get_db)
    ]
) -> UserRepository:

    return UserRepository(db)


def get_user_service(
    repository: Annotated[
        UserRepository,
        Depends(get_user_repository)
    ],
    db: Annotated[
        Session, 
        Depends(get_db)
    ]
) -> UserService:

    return UserService(
        repository=repository, 
        db=db
    )