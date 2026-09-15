from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.shared.session import get_db

from app.modules.auth.service.refresh_token import RefreshTokenService
from app.modules.auth.repository import RefreshTokenRepository


def get_refresh_token_repository(
    db: Annotated[
        Session,
        Depends(get_db)
    ]
) -> RefreshTokenRepository:

    return RefreshTokenRepository(db)


def get_refresh_token_service(
    repository: Annotated[
        RefreshTokenRepository,
        Depends(get_refresh_token_repository)
    ]
) -> RefreshTokenService:

    return RefreshTokenService(repository)