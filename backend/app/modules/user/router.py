from fastapi import APIRouter, status

from app.modules.user.schema import UserCreate, UserResponse
from app.modules.user.dependency import ValidateCSRF, UserService, AdminUser


router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.post(
    "/admin/register", 
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    data: UserCreate,
    service: UserService,
    _: ValidateCSRF
):

    return service.create_user(data)
