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
    InvalidCredentialsError,
    InvalidEmailAddressError,
    InvalidNameError,
    NameMustBeTwoToFiftyCharacterError,
    NameOnlyContainAlphabeticCharacter
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

    except NameOnlyContainAlphabeticCharacter:

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
    form_data: LoginRequest,
    service: Annotated[
        AuthService,
        Depends(get_auth_service)
    ],
    refresh_token_service: Annotated[
        RefreshTokenService,
        Depends(get_refresh_token_service)
    ]
):

    try:

        user = service.authenticate_user(form_data.email, form_data.password)
        access_token = create_access_token(user.id)
        refresh_token = (refresh_token_service.create_token(user.id))

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )

    except InvalidCredentialsError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )


@router.get(
    "/me",
    response_model=UserResponse
)
def get_ne(
    current_user: Annotated[
        User,
        Depends(get_current_user)
    ]
):

    return current_user