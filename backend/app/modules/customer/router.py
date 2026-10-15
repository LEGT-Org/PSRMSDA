from fastapi import APIRouter, Query, Response, status

from app.modules.customer.dependency import (
    CustomerService,
    ValidateCSRF,
    CurrentUser,
    AdminUser
)

from app.modules.customer.schema import (
    CustomerPageListResponse,
    CustomerCreateRequest,
    CustomerUpdateRequest,
    CustomerResponse
)

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@router.get(
    "/list",
    response_model=CustomerPageListResponse,
    status_code=status.HTTP_200_OK
)
def get_customers(
    current_user: CurrentUser,
    service: CustomerService,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    search: str | None = Query(default=None),
) -> CustomerPageListResponse:

    return service.get_customers(
        page=page,
        limit=limit,
        search=search,
    )


@router.post(
    "/create",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_customer(
    request: CustomerCreateRequest,
    service: CustomerService,
    current_user: CurrentUser,
    _:ValidateCSRF,
) -> CustomerResponse:

    return service.create_customer(
        actor_id=current_user.id,
        request=request
    )


@router.get(
    "/{customer_id}/details",
    response_model=CustomerResponse,
    status_code=status.HTTP_200_OK
)
def get_customer(
    customer_id: int,
    service: CustomerService,
    current_user: CurrentUser,
) -> CustomerResponse:

    return service.get_customer(customer_id)


@router.patch(
    "/{customer_id}/update",
    response_model=CustomerResponse,
    status_code=status.HTTP_200_OK
)
def update_customer(
    customer_id: int,
    request: CustomerUpdateRequest,
    service: CustomerService,
    current_user: CurrentUser,
    _:ValidateCSRF,
) -> dict:

    service.update_customer(
        customer_id=customer_id,
        actor_id=current_user.id,
        request=request
    )

    return {
        "message": "Customer details update has been successful."
    }


@router.delete(
    "/{customer_id}/delete",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_customer(
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



