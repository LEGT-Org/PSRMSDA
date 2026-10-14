from typing import Annotated

from fastapi import Depends

from app.modules.user.model import User
from app.modules.user.schema import UserRole
from app.modules.procurement_alert.service import ProcurementAlertService

from app.shared.dependencies.procurement_alert import get_procurement_alert_service
from app.shared.dependencies.auth import require_role
from app.shared.security.csrf import validate_csrf


ProcurementAlertService = Annotated[ProcurementAlertService, Depends(get_procurement_alert_service)]
AdminUser = Annotated[User, Depends(require_role(UserRole.ADMIN))]
ValidateCSRF = Annotated[None, Depends(validate_csrf)]