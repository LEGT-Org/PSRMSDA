from datetime import date
from fastapi import (
    APIRouter, 
    Request,
    status,
    Query
)

from app.shared.rate_limiter import limiter

from app.modules.service_request.dependency import (
    ServiceRequestService,
    ValidateCSRF,
    CurrentUser
)

from app.modules.service_request.schema import (
    ServiceRequestDashboardResponse,
    ServiceRequestPageListResponse,
    ServiceRequestDetailsResponse,
    RecentServiceRequestsResponse,
    ServiceRequestFinalizeRequest,
    LLMDiagnosticRequestPreview,
    ServiceRequestStatusUpdate,
    CustomerRequestPreview,
    ServiceRequestResponse,
    ConfirmServiceRequest,
    CancelServiceRequest,
    ServiceRequestStatus,
    UserSchema
)

            
router = APIRouter(
    prefix="/service-requests",
    tags=["Service Request"]
)


@router.get(
    "/counts",
    response_model=ServiceRequestDashboardResponse,
    status_code=status.HTTP_200_OK
)
@limiter.limit("120/minute")
def service_request_counts_dashboard(
    request: Request,
    current_user: CurrentUser,
    service: ServiceRequestService
) -> ServiceRequestDashboardResponse:

    return service.get_service_request_counts()


@router.get(
    "/recent",
    response_model=RecentServiceRequestsResponse,
    status_code=status.HTTP_200_OK
)
@limiter.limit("120/minute")
def recent_service_requests(
    request: Request,
    current_user: CurrentUser,
    service: ServiceRequestService
) -> RecentServiceRequestsResponse:

    return service.get_recent_service_requests()


@router.get(
    "/list",
    response_model=ServiceRequestPageListResponse,
    status_code=status.HTTP_200_OK
)
@limiter.limit("120/minute")
def list_of_service_requests(
    request: Request,
    current_user: CurrentUser,
    service: ServiceRequestService,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = Query(None),
    status: ServiceRequestStatus | None = Query(None),
    created_date: date | None = Query(None),
) -> ServiceRequestPageListResponse:

    return service.get_all_service_requests(
        page=page,
        limit=limit,
        search=search,
        status=status,
        created_date=created_date
    )


@router.post(
    "/diagnose",
    response_model=ServiceRequestResponse,
    status_code=status.HTTP_201_CREATED
)
@limiter.limit("5/minute")
async def ai_diagnosis(
    request: Request,
    service: ServiceRequestService,
    llm_diagnosis_request: LLMDiagnosticRequestPreview,
    customer_data: CustomerRequestPreview,
    current_user: CurrentUser,
    _: ValidateCSRF
) -> ServiceRequestResponse:
    
    return await service.run_ai_diagnosis(
        user=current_user,
        request=llm_diagnosis_request,
        customer_data=customer_data
    )


@router.post(
    "/confirm",
    response_model=ServiceRequestResponse,
    status_code=status.HTTP_200_OK,
)
@limiter.limit("5/minute")
def confirm_request(
    request: Request,
    data: ConfirmServiceRequest,
    service: ServiceRequestService,
    current_user: CurrentUser,
    _: ValidateCSRF
) -> ServiceRequestResponse:

    return service.confirm_request(
        user_id=current_user.id,
        request=data
    )


@router.post(
    "/cancel",
    status_code=status.HTTP_204_NO_CONTENT,
)
@limiter.limit("120/minute")
def cancel_request(
    request: Request,
    data: CancelServiceRequest,
    service: ServiceRequestService,
    current_user: CurrentUser,
    _: ValidateCSRF
) -> None:

    service.cancel_request(data.service_request_id)


@router.post(
    "/cancel/unload",
    status_code=status.HTTP_204_NO_CONTENT,
)
@limiter.limit("120/minute")
def cancel_request_on_unload(
    request: Request,
    data: CancelServiceRequest,
    service: ServiceRequestService,
    _: ValidateCSRF
) -> None:

    service.cancel_request(data.service_request_id)


@router.get(
    "/{service_request_id}/detail",
    response_model=ServiceRequestDetailsResponse,
    status_code=status.HTTP_200_OK
)
@limiter.limit("120/minute")
def service_request_detail(
    request: Request,
    service_request_id: int,
    service: ServiceRequestService,
    current_user: CurrentUser
) -> ServiceRequestDetailsResponse:

    return service.get_service_request_details(service_request_id)


@router.post(
    "/{service_request_id}/final-confirmation",
    status_code=status.HTTP_200_OK
)
@limiter.limit("5/minute")
def finalized_service_request(
    request: Request,
    service_request_id: int,
    data: ServiceRequestFinalizeRequest,
    service: ServiceRequestService,
    current_user: CurrentUser
) -> dict[str, str]:

    service.final_service_request_confirmation(
        service_request_id=service_request_id,
        approved_by=current_user,
        request_data=data
    )

    return {
        "message": (
            f"Service request {service_request_id} "
            f"status has been finalized into {data.status.value}."
        )
    }


@router.patch(
    "/{service_request_id}/status",
    status_code=status.HTTP_200_OK
)
@limiter.limit("30/minute")
def update_service_request_status(
    request: Request,
    service_request_id: int,
    data: ServiceRequestStatusUpdate,
    service: ServiceRequestService,
    current_user: CurrentUser
) -> dict[str, str]:

    service.update_service_request_status(
        service_request_id=service_request_id,
        status=data.status,
        updated_by=current_user
    )

    return {
        "message": (
            f"Service request {service_request_id} "
            f"status updated to {data.status.value}."
        )
    }


