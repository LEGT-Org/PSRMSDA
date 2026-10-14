from typing import Annotated

from fastapi import Depends

from app.modules.user.model import User
from app.modules.user.schema import UserRole
from app.modules.customer.service import Customer

from app.shared.dependencies.customer import get_customer_service
from app.shared.dependencies.auth import require_role, get_current_user
from app.shared.security.csrf import validate_csrf


CustomerService = Annotated[Customer, Depends(get_customer_service)]
AdminUser = Annotated[User, Depends(require_role(UserRole.ADMIN))]
CurrentUser = Annotated[User, Depends(get_current_user)]
ValidateCSRF = Annotated[None, Depends(validate_csrf)]