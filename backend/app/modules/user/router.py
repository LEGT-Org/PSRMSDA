from fastapi import (
    APIRouter,  
    status, 
    Query
)

from app.modules.user.schema import (
    UserPageListResponse,
    UserResponse, 
    UserCreate
)

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


@router.get(
    "/list",
    response_model=UserPageListResponse,
    status_code=status.HTTP_200_OK
)
def get_users(
    current_user:  AdminUser,
    service: UserService,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = Query(None),
    role: str | None = Query(None),
    status: str | None = Query(None),
):

    return service.get_all_users(
        page=page,
        limit=limit,
        search=search,
        role=role,
        status=status,
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

    return {
        "message": f"User {user_id} has been successfully promoted"
    }


@router.patch(
    "/admin/{user_id}/demote",
    status_code=status.HTTP_200_OK
)
def promote_user(
    user_id: int,
    service: UserService,
    current_user: AdminUser
) -> None:

    service.demote_user(
        user_id=user_id,
        actor_id=current_user.id
    )

    return {
        "message": f"User {user_id} has been successfully demoted"
    }


@router.patch(
    "/admin/{user_id}/enable",
    status_code=status.HTTP_200_OK
)
def enable_user(
    user_id: int,
    service: UserService,
    current_user: AdminUser
) -> None:

    service.enable_user(user_id)

    return {
        "message": f"User {user_id} has been successfully enabled"
    }


@router.patch(
    "/admin/{user_id}/disable",
    status_code=status.HTTP_200_OK  
)
def disable_user(
    user_id: int,
    service: UserService,
    current_user: AdminUser
) -> None:

    service.disable_user(
        user_id=user_id,
        actor_id=current_user.id    
    )

    return {
        "message": f"User {user_id} has been temporarily disabled"
    }


@router.patch(
    "/admin/{user_id}/delete",
    status_code=status.HTTP_200_OK
)
def delete_user(
    user_id: int,
    service: UserService,
    current_user: AdminUser
) -> dict[str, str]:

    service.delete_user(
        user_id=user_id,
        actor_id=current_user.id
    )

    return {
        "message": f"User {user_id} has been permanently deleted"
    }
