from typing import Literal
from fastapi import APIRouter, Query, status

from app.modules.procurement_alert.schema import (
    ProcurementAlertResolutionRequest,
    ProcurementAlertPageListResponse,
    ProcurementAlertResponse,
    ProcurementAlertType
)

from app.modules.procurement_alert.dependency import (
    ProcurementAlertService,
    ValidateCSRF,
    AdminUser
)


router = APIRouter(
    prefix="/procurement-alerts",
    tags=["Procurement Alerts"]
)


@router.get(
    "/list",
    response_model=ProcurementAlertPageListResponse,
    status_code=status.HTTP_200_OK
)
def get_procurement_alerts(
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


@router.patch(
    "/{alert_id}/resolution",
    status_code=status.HTTP_200_OK,
)
def update_procurement_alert_resolution(
    alert_id: int,
    request: ProcurementAlertResolutionRequest,
    service: ProcurementAlertService,
    current_user: AdminUser,
) -> dict[str, str]:

    service.update_resolution(
        alert_id=alert_id,
        is_resolved=request.is_resolved,
    )

    return {
        "message": (
            f"Procurement alert {alert_id} has been "
            f"{'resolved' if request.is_resolved else 'reopened'}."
        )
    }