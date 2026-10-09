from datetime import date
from fastapi import APIRouter, Query, status

from app.modules.service_request.dependency import (
    ServiceRequestService,
    ValidateCSRF,
    CurrentUser
)

from app.modules.service_request.schema import (
    ServiceRequestPageListResponse,
    ServiceRequestDetailsResponse,
    LLMDiagnosticRequestPreview,
    CustomerRequestPreview,
    ServiceRequestResponse,
    ConfirmServiceRequest,
    CancelServiceRequest,
    UserSchema
)

            
router = APIRouter(
    prefix="/service-requests",
    tags=["Service Requests"]
)


@router.get(
    "/list",
    response_model=ServiceRequestPageListResponse,
    status_code=status.HTTP_200_OK
)
def list_of_service_requests(
    current_user: CurrentUser,
    service: ServiceRequestService,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = Query(None),
    status: str | None = Query(None),
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
async def ai_diagnosis(
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
def confirm_request(
    request: ConfirmServiceRequest,
    service: ServiceRequestService,
    current_user: CurrentUser,
    _: ValidateCSRF
) -> ServiceRequestResponse:

    return service.confirm_request(
        user_id=current_user.id,
        request=request
    )


@router.post(
    "/cancel",
    status_code=status.HTTP_204_NO_CONTENT,
)
def cancel_request(
    request: CancelServiceRequest,
    service: ServiceRequestService,
    current_user: CurrentUser,
    _: ValidateCSRF
) -> None:

    service.cancel_request(request.service_request_id)


@router.post(
    "/cancel/unload",
    status_code=status.HTTP_204_NO_CONTENT,
)
def cancel_request_on_unload(
    request: CancelServiceRequest,
    service: ServiceRequestService,
    _: ValidateCSRF
) -> None:

    service.cancel_request(request.service_request_id)


@router.get(
    "/{service_request_id}/detail",
    response_model=ServiceRequestDetailsResponse,
    status_code=status.HTTP_200_OK
)
def service_request_detail(
    service_request_id: int,
    service: ServiceRequestService,
) -> ServiceRequestDetailsResponse:

    return service.get_service_request_details(service_request_id)

