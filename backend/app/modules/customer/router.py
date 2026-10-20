from fastapi import (
    APIRouter, 
    Response,
    Request, 
    status,
    Query
)

from app.shared.rate_limiter import limiter

from app.modules.customer.dependency import (
    CustomerService,
    ValidateCSRF,
    CurrentUser,
    AdminUser
)

from app.modules.customer.schema import (
    CustomerPageListResponse,
    CustomerUpdateResponse,
    CustomerCreateRequest,
    CustomerUpdateRequest,
    CustomerResponse
)

router = APIRouter(
    prefix="/customers",
    tags=["Customer"]
)


@router.get(
    "/counts",
    response_model=dict[str, int],
    status_code=status.HTTP_200_OK
)
@limiter.limit("120/minute")
def customers_counts_dashboard(
    request: Request,
    current_user: AdminUser,
    service: CustomerService
) -> dict[str, int]:

    return {
        "total_customers": service.get_customer_counts()
    }


@router.get(
    "/list",
    response_model=CustomerPageListResponse,
    status_code=status.HTTP_200_OK
)
@limiter.limit("120/minute")
def get_customers(
    request: Request,
    current_user: CurrentUser,
    service: CustomerService,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    search: str | None = Query(default=None),
) -> CustomerPageListResponse:

    return service.get_list_of_customers(
        page=page,
        limit=limit,
        search=search,
    )


@router.post(
    "/create",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("30/minute")
def create_customer(
    request: Request,
    data: CustomerCreateRequest,
    service: CustomerService,
    current_user: CurrentUser,
    _:ValidateCSRF,
) -> CustomerResponse:

    return service.create_customer(
        actor_id=current_user.id,
        request=data
    )


@router.get(
    "/{customer_id}/details",
    response_model=CustomerResponse,
    status_code=status.HTTP_200_OK
)
@limiter.limit("120/minute")
def get_customer(
    request: Request,
    customer_id: int,
    service: CustomerService,
    current_user: CurrentUser,
) -> CustomerResponse:

    return service.get_customer(customer_id)


@router.patch(
    "/{customer_id}/update",
    response_model=CustomerUpdateResponse,
    status_code=status.HTTP_200_OK
)
@limiter.limit("30/minute")
def update_customer(
    request: Request,
    customer_id: int,
    data: CustomerUpdateRequest,
    service: CustomerService,
    current_user: CurrentUser,
    _:ValidateCSRF,
) -> CustomerUpdateResponse:

    service.update_customer(
        customer_id=customer_id,
        actor_id=current_user.id,
        request=data
    )

    return CustomerUpdateResponse(
        id=customer_id,
        message="Customer details update has been successful."
    )


@router.delete(
    "/{customer_id}/delete",
    status_code=status.HTTP_204_NO_CONTENT,
)
@limiter.limit("10/minute")
def delete_customer(
    request: Request,
    customer_id: int,
    service: CustomerService,
    current_user: AdminUser,
    _:ValidateCSRF,
) -> None:

    service.delete_customer(
        customer_id=customer_id,
        actor_id=current_user.id
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)



