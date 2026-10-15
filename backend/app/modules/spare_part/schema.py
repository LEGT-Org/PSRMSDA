from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


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