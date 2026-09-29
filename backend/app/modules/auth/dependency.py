from typing import Annotated

from fastapi import Depends, Cookie

from app.modules.auth.service.refresh_token import RefreshTokenService
from app.modules.auth.service.auth import AuthService
from app.modules.user.model import User

from app.shared.dependencies.auth import get_auth_service, get_current_user
from app.shared.dependencies.refresh_token import get_refresh_token_service
from app.shared.security.csrf import generate_csrf_token, validate_csrf 
from app.shared.security.jwt import create_access_token


ValidateCSRF = Annotated[None, Depends(validate_csrf)]
RefreshToken = Annotated[str | None, Cookie()]
CurrentUser = Annotated[User, Depends(get_current_user)]
AuthService = Annotated[AuthService, Depends(get_auth_service)]
RefreshTokenService = Annotated[RefreshTokenService, Depends(get_refresh_token_service)]