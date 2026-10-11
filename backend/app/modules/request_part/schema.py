from pydantic import BaseModel, Field


class RequestPartSchema(BaseModel):

    request_id: int
    part_id: int
    quantity: int | None = None
    part_name_snapshot: str
    is_stock_validated: bool = False



class RequestPartUsage(BaseModel):
    
    request_part_id: int
    part_used: bool
    quantity_used: int | None = Field(default=None, ge=0)
