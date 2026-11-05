from enum import StrEnum
from decimal import Decimal
from datetime import datetime
from pydantic import (
    field_validator,
    ConfigDict, 
    BaseModel, 
    Field, 
)

from app.modules.procurement_alert.schema import ProcurementAlertType


class ProcurementAlertTypePreview(StrEnum):

    FINALIZED_REQUEST = ProcurementAlertType.FINALIZED_REQUEST
    REQUEST_STAGE = ProcurementAlertType.REQUEST_STAGE
    PART_SELECTED = ProcurementAlertType.PART_SELECTED
    NO_PART_MATCH = ProcurementAlertType.NO_PART_MATCH
    PART_NOT_FOUND = ProcurementAlertType.PART_NOT_FOUND
    INSUFFICIENT_STOCK = ProcurementAlertType.INSUFFICIENT_STOCK


class SparePartCreateRequest(BaseModel):

    part_name: str
    device_model: str | None = None
    device_brand: str | None = None
    specifications: str | None = None
    stock_quantity: int | None = Field(default=None, ge=0)
    unit_cost: Decimal | None = Field(default=None, ge=0)
    shelf_location: str
    image_url: str | None = None
    category_id: int


class SparePartUpdateRequest(BaseModel):

    part_name: str | None = None
    device_model: str | None = None
    device_brand: str | None = None
    specifications: str | None = None
    stock_quantity: int | None = Field(default=None, ge=0)
    unit_cost: Decimal | None = Field(default=None, ge=0)
    shelf_location: str | None = None
    image_url: str | None = None
    category_id: int | None = None


class SparePartUpdateResponse(BaseModel):

    id: int
    message: str


class SparePartResponse(BaseModel):

    id: int
    part_name: str
    part_code: str
    device_model: str | None
    device_brand: str | None
    specifications: str | None
    stock_quantity: int | None
    unit_cost: Decimal | None
    shelf_location: str
    image_url: str | None
    category_id: int
    category_name: str

    model_config = ConfigDict(from_attributes=True) 

class SparePartListResponse(BaseModel):

    items: list[SparePartResponse]
    total: int
    page: int
    limit: int
    pages: int


class ProcurementAlertRequest(BaseModel):

    request_id: int
    part_id: int | None = None
    part_name_snapshot: str | None = None
    low_stock_parts_snapshot: list[dict] | None = None
    is_resolved: bool = False
    created_at: datetime
    alert_type: ProcurementAlertType
    alert_message: str | None = None