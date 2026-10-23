from typing import Annotated

from fastapi import Depends

from app.modules.user.model import User
from app.modules.user.schema import UserRole
from app.modules.report.service import ReportService

from app.shared.dependencies.auth import require_role, get_current_user
from app.shared.dependencies.report import get_report_service
from app.shared.security.csrf import validate_csrf


ReportService = Annotated[ReportService, Depends(get_report_service)]
AdminUser = Annotated[User, Depends(require_role(UserRole.ADMIN))]
CurrentUser = Annotated[User, Depends(get_current_user)]
ValidateCSRF = Annotated[None, Depends(validate_csrf)]