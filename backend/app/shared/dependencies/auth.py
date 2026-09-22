import jwt

from typing import Annotated
from collections.abc import Callable
from fastapi import Depends, HTTPException, status

from app.shared.dependencies.user import get_user_repository, get_user_service
from app.shared.security.jwt import decode_access_token
from app.shared.security.oauth2 import oauth2_scheme

from app.modules.auth.service.auth import AuthService
from app.modules.user.repository import UserRepository
from app.modules.user.service import UserService
from app.modules.user.schema import UserRole
from app.modules.user.model import User


def get_auth_service(
    user_service: UserService = Depends(get_user_service)
) -> AuthService:

    return AuthService(user_service)

def get_current_user(
    token: Annotated[
        str,
        Depends(oauth2_scheme)
    ],
    repository: Annotated[
        UserRepository,
        Depends(get_user_repository)
    ]
) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    try:

        payload = decode_access_token(token)
        subject = payload.get("sub")

        if subject is None:
            raise credentials_exception

        user_id = int(subject)

    except (jwt.InvalidTokenError, ValueError):

        raise credentials_exception

    user = repository.get_by_id(user_id)

    if user is None:
        raise credentials_exception

    return user


def require_role(require_role: UserRole) -> Callable:

    def dependency(
        current_user: Annotated[
            User,
            Depends(get_current_user)
        ]
    ) -> User:

        if current_user.role != require_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )

    return dependency
