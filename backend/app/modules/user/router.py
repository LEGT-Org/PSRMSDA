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
    _: ValidateCSRF
):

    return service.create_user(data)


@router.patch(
    "/admin/{user_id}/promote",
    status_code=status.HTTP_200_OK
)
def promote_user(
    user_id: int,
    service: UserService,
    current_user: AdminUser
) -> None:

    service.promote_user(user_id)


@router.patch(
    "/admin/{user_id}/demote",
    status_code=status.HTTP_200_OK
)
def promote_user(
    user_id: int,
    service: UserService,
    current_user: AdminUser
) -> None:

    service.demote_user(user_id)


@router.patch(
    "/admin/{user_id}/enable",
    status_code=status.HTTP_200_OK
)
def disable_user(
    user_id: int,
    service: UserService,
    current_user: AdminUser
) -> None:

    service.enable_user(user_id)


@router.patch(
    "/admin/{user_id}/disable",
    status_code=status.HTTP_204_NO_CONTENT
)
def disable_user(
    user_id: int,
    service: UserService,
    current_user: AdminUser
) -> None:

    service.disable_user(user_id)
