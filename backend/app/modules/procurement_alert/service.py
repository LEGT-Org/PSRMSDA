from sqlalchemy.orm import Session

from app.modules.procurement_alert.repository import ProcurementAlertRepository
from app.modules.procurement_alert.interface import (
    ServiceRequestInterface,
    SparePartInterface
)


class ProcurementAlertService:

    def __init__(
        self,
        repository: ProcurementAlertRepository,
        db: Session
    ):

        self.repository = repository
        self.db = db