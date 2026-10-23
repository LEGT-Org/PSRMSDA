from typing import Literal
from fastapi import (
    APIRouter,  
    Response,
    Request, 
    status,
    Query
)

from app.shared.rate_limiter import limiter

from app.modules.user.schema import (
    UserPageListResponse,
    UserResponse,
    UserCreate,
    UserRole 
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
@limiter.limit("120/minute")
def get_me(
    request: Request,
    current_user: CurrentUser
) -> UserResponse:

    return current_user


@router.get(
    "/counts",
    response_model=dict[str, int],
    status_code=status.HTTP_200_OK
)
@limiter.limit("120/minute")
def get_active_users(
    request: Request,
    current_user: AdminUser,
    service: UserService
) -> dict[str, int]:

    return {
        "total_active_users": service.get_active_user_counts()
    }


@router.get(
    "/list",
    response_model=UserPageListResponse,
    status_code=status.HTTP_200_OK
)
@limiter.limit("120/minute")
def get_users(
    request: Request,
    current_user:  AdminUser,
    service: UserService,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = Query(None),
    role: UserRole | None = Query(None),
    status: Literal["all", "active", "disabled"] = "all",
) -> dict:

    status_filter = {
        "all": None,
        "active": "active",
        "disabled": "disabled",
    }[status]

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
@limiter.limit("15/minute")
def register(
    request: Request,
    data: UserCreate,
    service: UserService,
    current_user: AdminUser,
    _: ValidateCSRF
):

    return service.create_user(
        data=data,
        actor_id=current_user.id
    )


@router.patch(
    "/admin/{user_id}/promote",
    status_code=status.HTTP_200_OK
)
@limiter.limit("30/minute")
def promote_user(
    request: Request,
    user_id: int,
    service: UserService,
    current_user: AdminUser
) -> None:

    service.promote_user(
        user_id=user_id,
        actor_id=current_user.id
    )

    return {
        "message": f"User {user_id} has been successfully promoted"
    }


@router.patch(
    "/admin/{user_id}/demote",
    status_code=status.HTTP_200_OK
)
@limiter.limit("30/minute")
def promote_user(
    request: Request,
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
@limiter.limit("30/minute")
def enable_user(
    request: Request,
    user_id: int,
    service: UserService,
    current_user: AdminUser
) -> None:

    service.enable_user(
        user_id=user_id,
        actor_id=current_user.id
    )

    return {
        "message": f"User {user_id} has been successfully enabled"
    }


@router.patch(
    "/admin/{user_id}/disable",
    status_code=status.HTTP_200_OK  
)
@limiter.limit("30/minute")
def disable_user(
    request: Request,
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


@router.delete(
    "/admin/{user_id}/delete",
    status_code=status.HTTP_204_NO_CONTENT
)
@limiter.limit("10/minute")
def delete_user(
    request: Request,
    user_id: int,
    service: UserService,
    current_user: AdminUser
) -> None:

    service.delete_user(
        user_id=user_id,
        actor_id=current_user.id
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)