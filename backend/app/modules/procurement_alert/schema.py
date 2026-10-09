from datetime import datetime
from enum import StrEnum
from pydantic import BaseModel


class ProcurementAlertType(StrEnum):

    REQUEST_STAGE = "Request Stage"
    PART_SELECTED = "Part Selected"
    NO_PART_MATCH = "No Part Match"
    PART_NOT_FOUND = "Part Not Found"
    INSUFFICIENT_STOCK = "Insufficient Stock"


class ProcurementAlertSchema(BaseModel):

    alert_message: str
    alert_type: ProcurementAlertType
    is_resolved: bool
    request_id: int
    part_id: int
    part_name_snapshot: str
    created_at: datetime