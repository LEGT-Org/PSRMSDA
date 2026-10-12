from datetime import datetime
from enum import StrEnum
from pydantic import BaseModel


class ProcurementAlertType(StrEnum):

    FINALIZED_REQUEST = "Finalized Request"
    REQUEST_STAGE = "Request Stage"
    PART_SELECTED = "Part Selected"
    NO_PART_MATCH = "No Part Match"
    PART_NOT_FOUND = "Part Not Found"
    INSUFFICIENT_STOCK = "Insufficient Stock"


class ProcurementAlertSchema(BaseModel):

    request_id: int
    part_id: int | None = None
    part_name_snapshot: str | None = None
    is_resolved: bool = False
    created_at: datetime
    alert_type: ProcurementAlertType
    alert_message: str | None = None