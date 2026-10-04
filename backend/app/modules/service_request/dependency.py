from typing import Annotated

from fastapi import Depends

from app.modules.service_request.service import ServiceRequestService
from app.modules.user.model import User

from app.shared.dependencies.service_request import get_service_request_service
from app.shared.dependencies.auth import get_current_user
from app.shared.security.csrf import validate_csrf


ValidateCSRF = Annotated[None, Depends(validate_csrf)]
ServiceRequestService = Annotated[ServiceRequestService, Depends(get_service_request_service)]
CurrentUser = Annotated[User, Depends(get_current_user)]