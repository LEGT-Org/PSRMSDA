from typing import Literal
from fastapi import (
    APIRouter, 
    Request,
    status,
    Query
)

from app.shared.rate_limiter import limiter

from app.modules.procurement_alert.schema import (
    ProcurementAlertResolutionRequest,
    ProcurementAlertPageListResponse,
    ProcurementAlertResponse,
    RecentActivitiesResponse,
    LowStockCheckResponse,
    ProcurementAlertType
)

from app.modules.procurement_alert.dependency import (
    ProcurementAlertService,
    ValidateCSRF,
    AdminUser
)


router = APIRouter(
    prefix="/procurement-alerts",
    tags=["Procurement Alert"]
)


@router.get(
    "/recent",
    response_model=RecentActivitiesResponse,
    status_code=status.HTTP_200_OK
)
@limiter.limit("120/minute")
def recent_activities(
    request: Request,
    service: ProcurementAlertService,
    current_user: AdminUser
) -> RecentActivitiesResponse:

    return service.get_recent_activities()


@router.get(
    "/list",
    response_model=ProcurementAlertPageListResponse,
    status_code=status.HTTP_200_OK
)
@limiter.limit("120/minute")
def get_procurement_alerts(
    request: Request,
    service: ProcurementAlertService,
    current_user: AdminUser,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = Query(None, max_length=100),
    resolution: Literal["all", "unresolved", "resolved"] = "all",
    alert_type: ProcurementAlertType | None = Query(None),
) -> dict:

    is_resolved = {
        "all": None,
        "unresolved": False,
        "resolved": True,
    }[resolution]

    return service.get_procurement_alerts(
        page=page,
        limit=limit,
        search=search,
        is_resolved=is_resolved,
        alert_type=alert_type,
    )


@router.post(
    "/check-stock",
    response_model=LowStockCheckResponse,
    status_code=status.HTTP_200_OK,
)
@limiter.limit("15/minute")
def check_low_stock(
    request: Request,
    service: ProcurementAlertService,
    current_user: AdminUser,
    _: ValidateCSRF,
    threshold: int = Query(5, ge=0),
) -> LowStockCheckResponse:

    return service.check_low_stock(
        threshold=threshold
    )


@router.patch(
    "/{alert_id}/resolution",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("30/minute")
def update_procurement_alert_resolution(
    request: Request,
    alert_id: int,
    data: ProcurementAlertResolutionRequest,
    service: ProcurementAlertService,
    current_user: AdminUser,
    _:ValidateCSRF,
) -> dict[str, str]:

    service.update_resolution(
        alert_id=alert_id,
        is_resolved=data.is_resolved,
    )

    return {
        "message": (
            f"Procurement alert {alert_id} has been "
            f"{'resolved' if data.is_resolved else 'reopened'}."
        )
    }


@router.get(
    "/{alert_id}",
    response_model=ProcurementAlertResponse,
    status_code=status.HTTP_200_OK,
)
@limiter.limit("120/minute")
def get_procurement_alert_by_id(
    request: Request,
    alert_id: int,
    service: ProcurementAlertService,
    current_user: AdminUser,
) -> ProcurementAlertResponse:

    return service.get_procurement_alert_by_id(
        alert_id=alert_id
    )