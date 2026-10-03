from fastapi import APIRouter, status

from app.modules.user.schema import UserCreate, UserResponse
from app.modules.user.dependency import (
    ValidateCSRF, 
    UserService,
    CurrentUser, 
    AdminUser
)


router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK   
)
def get_me(current_user: CurrentUser):

    return current_user


@router.post(
    "/admin/register", 
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    data: UserCreate,
    service: UserService,
    current_user: AdminUser,
    _: ValidateCSRF
):

    return service.create_user(data)
