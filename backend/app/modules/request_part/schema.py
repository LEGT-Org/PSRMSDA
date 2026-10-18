from pydantic import BaseModel, Field


class RequestPartSchema(BaseModel):

    request_id: int
    part_id: int
    quantity: int | None = None
    quantity_used: int | None = None
    part_name_snapshot: str
    is_stock_validated: bool = False
    part_used: bool | None = None



class RequestPartUsage(BaseModel):
    
    request_part_id: int
    part_used: bool
    quantity_used: int | None = Field(default=None, ge=0)
