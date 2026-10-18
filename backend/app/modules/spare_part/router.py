from fastapi import (
    APIRouter, 
    Response, 
    Request,
    status,
    Query,
)

from app.shared.rate_limiter import limiter

from app.modules.spare_part.schema import (
    SparePartUpdateResponse,
    SparePartCreateRequest,
    SparePartUpdateRequest,
    SparePartListResponse,
    SparePartResponse,
)

from app.modules.spare_part.dependency import (
    SparePartService,
    ValidateCSRF,
    CurrentUser,
    AdminUser
)


router = APIRouter(
    prefix="/spare-parts",
    tags=["Spare Part"]
)


@router.get(
    "/list",
    response_model=SparePartListResponse,
    status_code=status.HTTP_200_OK
)
@limiter.limit("120/minute")
def get_spare_parts(
    request: Request,
    service: SparePartService,
    current_user: CurrentUser,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    search: str | None = Query(default=None),
    category_id: int | None = Query(default=None, ge=1),
    parent_category_id: int | None = Query(default=None, ge=1),
) -> SparePartListResponse:

    return service.get_list_of_spare_parts(
        page=page,
        limit=limit,
        search=search,
        category_id=category_id,
        parent_category_id=parent_category_id
    )


@router.get(
    "/{part_id}/details",
    response_model=SparePartResponse,
    status_code=status.HTTP_200_OK
)
@limiter.limit("120/minute")
def get_spare_part(
    request: Request,
    part_id: int,
    service: SparePartService,
    current_user: CurrentUser,
) -> SparePartResponse:

    return service.get_spare_part_specific_details(part_id)


@router.post(
    "/create",
    response_model=SparePartResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("30/minute")
def create_spare_part(
    request: Request,
    data: SparePartCreateRequest,
    service: SparePartService,
    current_user: CurrentUser,
) -> SparePartResponse:

    return service.create_spare_part(
        request=data,
        user_id=current_user.id,
    )


@router.patch(
    "/{part_id}/update",
    response_model=SparePartUpdateResponse,
    status_code=status.HTTP_200_OK,
)
@limiter.limit("30/minute")
def update_spare_part(
    request: Request,
    part_id: int,
    data: SparePartUpdateRequest,
    service: SparePartService,
    current_user: CurrentUser,
) -> SparePartUpdateResponse:

    service.update_spare_part(
        part_id=part_id,
        request=data,
        actor_id=current_user.id,
    )

    return SparePartUpdateResponse(
        id=part_id,
        message="Spare part update has been successfully."
    )

@router.delete(
    "/{part_id}/delete",
    status_code=status.HTTP_204_NO_CONTENT,
)
@limiter.limit("10/minute")
def delete_spare_part(
    request: Request,
    part_id: int,
    service: SparePartService,
    current_user: AdminUser,
):

    service.delete_spare_part(
        part_id=part_id,
        actor_id=current_user.id,
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)