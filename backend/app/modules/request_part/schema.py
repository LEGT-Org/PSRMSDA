from pydantic import BaseModel, Field


class RequestPartSchema(BaseModel):

    request_id: int
    part_id: int
    quantity: int
    part_name_snapshot: str
    is_stock_validated: bool


class RequestPartUsage(BaseModel):
    
    request_part_id: int
    part_used: bool
    quantity_used: int = Field(ge=0)
