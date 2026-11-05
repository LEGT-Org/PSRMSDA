from datetime import datetime
from enum import StrEnum

from pydantic import (
    BaseModel,
    ConfigDict,
    field_validator,
)


class ProcurementAlertType(StrEnum):

    FINALIZED_REQUEST = "Finalized Request"
    REQUEST_STAGE = "Request Stage"
    PART_SELECTED = "Part Selected"
    NO_PART_MATCH = "No Part Match"
    PART_NOT_FOUND = "Part Not Found"
    INSUFFICIENT_STOCK = "Insufficient Stock"


class LowStockPartSnapshot(BaseModel):

    part_id: int
    part_name: str
    stock_quantity: int


class ProcurementAlertSchema(BaseModel):

    request_id: int | None = None
    part_id: int | None = None
    part_name_snapshot: str | None = None
    low_stock_parts_snapshot: list[dict] | None = None

    is_resolved: bool = False
    created_at: datetime
    alert_type: ProcurementAlertType
    alert_message: str | None = None


class ProcurementAlertResolutionRequest(BaseModel):

    is_resolved: bool


class ProcurementAlertResponse(BaseModel):

    id: int
    request_id: int | None
    part_id: int | None
    part_name_snapshot: str | None
    low_stock_parts_snapshot: list[LowStockPartSnapshot] | None = None

    alert_type: str
    alert_message: str | None
    is_resolved: bool
    created_at: datetime

    @field_validator("alert_type", mode="before")
    @classmethod
    def serialize_alert_type(cls, value):
        return value.value if hasattr(value, "value") else value

    model_config = ConfigDict(from_attributes=True)


class ProcurementAlertPageListResponse(BaseModel):

    items: list[ProcurementAlertResponse]
    page: int
    limit: int
    total: int
    pages: int
    total_alerts: int
    unresolved_alerts: int
    resolved_alerts: int


class RecentActivityItem(BaseModel):

    id: int
    description: str
    time: datetime


class RecentActivitiesResponse(BaseModel):

    items: list[RecentActivityItem]


class LowStockCheckResponse(BaseModel):

    message: str
    alert_created: bool
    total_low_stock_parts: int
    alert: ProcurementAlertResponse | None = None
