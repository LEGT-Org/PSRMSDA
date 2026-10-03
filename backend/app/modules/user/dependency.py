from typing import Annotated

from fastapi import Depends

from app.modules.user.service import UserService
from app.modules.user.schema import UserRole
from app.modules.user.model import User

from app.shared.dependencies.user import get_user_service
from app.shared.dependencies.auth import require_role, get_current_user
from app.shared.security.csrf import validate_csrf


ValidateCSRF = Annotated[None, Depends(validate_csrf)]
UserService = Annotated[UserService, Depends(get_user_service)]
CurrentUser = Annotated[User, Depends(get_current_user)]
AdminUser = Annotated[User, Depends(require_role(UserRole.ADMIN))]