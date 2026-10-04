from datetime import datetime
from pydantic import BaseModel


class ProcurementAlertSchema(BaseModel):

    alert_message: str
    is_resolved: bool
    request_id: int
    part_id: int
    part_name_snapshot: str
    created_at: datetime