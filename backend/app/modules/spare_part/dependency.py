from typing import Annotated

from fastapi import Depends

from app.modules.user.model import User
from app.modules.user.schema import UserRole
from app.modules.spare_part.service import SparePart

from app.shared.dependencies.spare_part import get_spare_part_service
from app.shared.dependencies.auth import require_role, get_current_user
from app.shared.security.csrf import validate_csrf


SparePartService = Annotated[SparePart, Depends(get_spare_part_service)]
AdminUser = Annotated[User, Depends(require_role(UserRole.ADMIN))]
CurrentUser = Annotated[User, Depends(get_current_user)]
ValidateCSRF = Annotated[None, Depends(validate_csrf)]