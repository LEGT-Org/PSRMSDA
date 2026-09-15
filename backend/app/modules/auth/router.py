from typing import Annotated 

from fastapi import (
    APIRouter, 
    Depends, 
    HTTPException, 
    status
)
 
from app.shared.dependencies.auth import get_auth_service, get_current_user
from app.shared.dependencies.refresh_token import get_refresh_token_service
from app.shared.exception import (
    EmailAlreadyExistsError, 
    InvalidCredentialsError
)

from app.modules.user.model import User

from app.modules.auth.schema import (
    UserResponse,
    UserCreate,
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest 
)
from app.modules.auth.service.refresh_token import RefreshTokenService
from app.modules.auth.service.auth import AuthService
from app.modules.auth.security.jwt import create_access_token 


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register", 
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    data: UserCreate,
    service: Annotated[
        AuthService,
        Depends(get_auth_service)
    ]
):

    try:

        return service.register(data)

    except EmailAlreadyExistsError:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )