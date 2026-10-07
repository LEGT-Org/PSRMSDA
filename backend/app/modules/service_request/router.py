from fastapi import APIRouter, status

from app.modules.service_request.dependency import (
    ServiceRequestService,
    ValidateCSRF,
    CurrentUser
)

from app.modules.service_request.schema import (
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

