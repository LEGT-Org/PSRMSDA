from pydantic import BaseModel


class RequestPartSchema(BaseModel):

    request_id: int
    part_id: int
    quantity: int
    part_name_snapshot: str
    is_stock_validated: bool