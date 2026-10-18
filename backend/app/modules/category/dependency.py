from typing import Annotated

from fastapi import Depends

from app.modules.user.model import User
from app.modules.user.schema import UserRole
from app.modules.category.service import Category

from app.shared.dependencies.category import get_category_service
from app.shared.dependencies.auth import require_role, get_current_user
from app.shared.security.csrf import validate_csrf


CategoryService = Annotated[Category, Depends(get_category_service)]
CurrentUser = Annotated[User, Depends(get_current_user)]
ValidateCSRF = Annotated[None, Depends(validate_csrf)]
AdminUser = Annotated[User, Depends(require_role(UserRole.ADMIN))]