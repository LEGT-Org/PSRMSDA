from typing import Annotated 

from fastapi import (
    APIRouter, 
    Depends, 
    HTTPException, 
    Response,
    Cookie,
    status
)

from app.shared.config import settings 
from app.shared.dependencies.auth import get_auth_service, get_current_user
from app.shared.dependencies.refresh_token import get_refresh_token_service
from app.shared.exception import (
    EmailAlreadyExistsError, 
    InvalidCredentialsError,
    InvalidEmailAddressError,
    InvalidNameError,
    NameMustBeTwoToFiftyCharacterError,
    NameOnlyContainAlphabeticCharacterError,
    InvalidRefreshTokenError,
    ExpiredRefreshTokenError
)


from app.modules.auth.service.refresh_token import RefreshTokenService
from app.modules.auth.service.auth import AuthService
from app.modules.auth.security.jwt import create_access_token
from app.modules.auth.security.csrf import generate_csrf_token,validate_csrf 
from app.modules.auth.schema import (
    UserResponse,
    UserCreate,
    LoginRequest,
    TokenResponse,
)


from app.modules.user import User


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK   
)
def get_me(
    current_user: Annotated[
        User,
        Depends(get_current_user)
    ]
):

    return current_user


@router.get(
    "/csrf",
    status_code=status.HTTP_200_OK
)
def get_csrf_token(response: Response):

    csrf_token = generate_csrf_token();
    
    response.set_cookie(
        key="csrf_token",
        value=csrf_token,
        httponly=settings.allowed_csrf_httponly,
        secure=settings.allowed_secure,
        samesite=settings.allowed_samesite,
        path="/"
    )

    return {
        "csrf_token": csrf_token
    }


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
    ],
    _: Annotated[None, Depends(validate_csrf)] = None
):

    try:

        return service.register(data)

    except EmailAlreadyExistsError:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists."
        )

    except InvalidEmailAddressError:

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Invalid email address."
        )

    except InvalidNameError:

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Name cannot be empty."
        )

    except NameMustBeTwoToFiftyCharacterError:

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Name must be between 2 and 50 characters."
        )

    except NameOnlyContainAlphabeticCharacterError:

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Name can only contain alphabetic characters, spaces, hypens, and apostrophes."
        )


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK
)
def login(
    response: Response,
    form_data: LoginRequest,
    service: Annotated[
        AuthService,
        Depends(get_auth_service)
    ],
    refresh_token_service: Annotated[
        RefreshTokenService,
        Depends(get_refresh_token_service)
    ],
    _: Annotated[None, Depends(validate_csrf)] = None
):

    try:

        user = service.authenticate_user(form_data.email, form_data.password)
        access_token = create_access_token(user.id, user.role)
        refresh_token = refresh_token_service.create_token(user.id)

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=settings.allowed_refresh_httponly,
            secure=settings.allowed_secure,
            samesite=settings.allowed_samesite,
            path="/auth"
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer"
        )

    except InvalidCredentialsError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )


@router.post(
    "/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK
)
def refresh(
    response: Response,
    service: Annotated[
        AuthService,
        Depends(get_auth_service)
    ],
    refresh_token_service: Annotated[
        RefreshTokenService,
        Depends(get_refresh_token_service)
    ] = None,
    refresh_token: Annotated[str | None, Cookie()] = None,
    _: Annotated[None, Depends(validate_csrf)] = None
):

    if refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No cookie received"
        )

    try:
        
        user_id, new_refresh_token = refresh_token_service.rotate_token(refresh_token)
        user = service.auth_get_user_by_id(user_id);
        new_access_token = create_access_token(user.id, user.role)

        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            httponly=settings.allowed_refresh_httponly,
            secure=settings.allowed_secure,
            samesite=settings.allowed_samesite,
            path="/auth"
        )

        return TokenResponse(
            access_token=new_access_token,
            token_type="bearer"
        ) 

    except InvalidRefreshTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    except ExpiredRefreshTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired refresh token"
        )


@router.post(
    "/revoke",
    status_code=status.HTTP_200_OK
)
def revoke(
    response: Response,
    refresh_token_service: Annotated[
        RefreshTokenService,
        Depends(get_refresh_token_service)
    ] = None,
    refresh_token: Annotated[str | None, Cookie()] = None,
    _: Annotated[None, Depends(validate_csrf)] = None
):

    if not refresh_token:
        response.delete_cookie(
            key="refresh_token",
            path="/auth"
        )

        return {
            "message": "Successfully logged out"
        }

    try:

        refresh_token_service.revoke_token(refresh_token)

    except InvalidRefreshToken:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    except ExpiredRefreshTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired refresh token"
        )

    finally:
        response.delete_cookie(
            key="refresh_token",
            path="/auth"
        )

    return {
        "message": "Successfully logged out"
    }