from fastapi import (
    APIRouter, 
    Response,
    Request, 
    status
)

from app.modules.auth.schema import (
    ResetPasswordRequest,
    SetPasswordRequest,
    TokenResponse, 
    AuthResponse, 
    LoginRequest
)

from app.modules.auth.dependency import (
    RefreshTokenService,
    ValidateCSRF,
    RefreshToken,
    AuthService
)

from app.shared.security.csrf import generate_csrf_token
from app.shared.security.jwt import create_access_token
from app.shared.exception import NoRefreshTokenError
from app.shared.rate_limiter import limiter
from app.shared.config import settings 


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.get(
    "/csrf",
    status_code=status.HTTP_200_OK
)
def get_csrf_token(response: Response):

    csrf_token = generate_csrf_token();
    
    response.set_cookie(
        key="csrf_token",
        value=csrf_token,
        httponly=settings.cookie.allowed_csrf_httponly,
        secure=settings.cookie.allowed_secure,
        samesite=settings.cookie.allowed_samesite,
        path="/"
    )

    return {
        "csrf_token": csrf_token
    }


@router.post(
    "/set-password",
    status_code=status.HTTP_200_OK
)
@limiter.limit("15/minute")
def set_password(
    request: Request,
    data: SetPasswordRequest,
    service: AuthService,
    _: ValidateCSRF
):

    service.auth_set_password(data)

    return {
        "message": "Registration successful"
    }


@router.post(
    "/reset-password",
    status_code=status.HTTP_200_OK
)
@limiter.limit("15/minute")
def reset_password(
    request: Request,
    email: ResetPasswordRequest,
    service: AuthService,
    _:ValidateCSRF
):

    service.auth_reset_password(email.reset_password_email)

    return {
        "message": "Reset password successful"
    }
    

@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK
)
@limiter.limit("15/minute")
def login(
    request: Request,
    response: Response,
    form_data: LoginRequest,
    service: AuthService,
    refresh_token_service: RefreshTokenService,
    _: ValidateCSRF
):

    user = service.authenticate_user(form_data.email, form_data.password)
    access_token = create_access_token(user.id, user.role)
    refresh_token = refresh_token_service.create_token(user.id)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=settings.cookie.allowed_refresh_httponly,
        secure=settings.cookie.allowed_secure,
        samesite=settings.cookie.allowed_samesite,
        path="/auth"
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer"
    )


@router.post(
    "/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK
)
@limiter.limit("30/minute")
def refresh(
    request: Request,
    response: Response,
    service: AuthService,
    refresh_token_service: RefreshTokenService,
    refresh_token: RefreshToken,
    _: ValidateCSRF
):

    if refresh_token is None:
        raise NoRefreshTokenError()
        
    user_id, new_refresh_token = refresh_token_service.rotate_token(refresh_token)
    user = service.auth_get_user_by_id(user_id);
    new_access_token = create_access_token(user.id, user.role)

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=settings.cookie.allowed_refresh_httponly,
        secure=settings.cookie.allowed_secure,
        samesite=settings.cookie.allowed_samesite,
        path="/auth"
    )

    return TokenResponse(
        access_token=new_access_token,
        token_type="bearer"
    )


@router.post(
    "/revoke",
    status_code=status.HTTP_200_OK
)
@limiter.limit("15/minute")
def revoke(
    request: Request,
    response: Response,
    refresh_token_service: RefreshTokenService,
    refresh_token: RefreshToken,
    _: ValidateCSRF
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

    finally:
        response.delete_cookie(
            key="refresh_token",
            path="/auth"
        )

    return {
        "message": "Successfully logged out"
    }