from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.procurement_alert.model import ProcurementAlert


class ProcurementAlertRepository:

    def __init__(
        self,
        db: Session
    ):

        self.db = db

    def create(
        self,
        procurement_alert: ProcurementAlert
    ) -> ProcurementAlert:

        self.db.add(procurement_alert)
        return procurement_alert