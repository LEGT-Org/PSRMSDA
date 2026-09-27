from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.shared.dependencies.email_service import get_email_service
from app.shared.email.provider import EmailService
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
    email_service: Annotated[
        EmailService,
        Depends(get_email_service)
    ],
    db: Annotated[
        Session, 
        Depends(get_db)
    ]
) -> UserService:

    return UserService(
        repository=repository,
        email_service=email_service, 
        db=db
    )