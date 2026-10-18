from fastapi import APIRouter, Request, status

from app.modules.category.schema import (
    CategoryResponse, 
    CategoryRequest,
    ChildCategory
)

from app.modules.category.dependency import (
    CategoryService,
    ValidateCSRF,
    CurrentUser,
    AdminUser
)

from app.shared.rate_limiter import limiter


router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.get(
    "/list",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
)
@limiter.limit("120/minute")
def get_categories(
    request: Request,
    service: CategoryService,
    current_user: CurrentUser
) -> list[CategoryResponse]:

    return service.get_list_of_categories()


@router.post(
    "/create",
    response_model=ChildCategory,
    status_code=status.HTTP_201_CREATED
)
@limiter.limit("30/minute")
def add_new_category(
    request: Request,
    data: CategoryRequest,
    service: CategoryService,
    current_user: AdminUser
) -> ChildCategory:

    return service.create_new_category(
        request=data
    )
