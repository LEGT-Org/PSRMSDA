from sqlalchemy.orm import Session

from app.shared.exception import ProcurementAlertFailedError

from app.modules.procurement_alert.repository import ProcurementAlertRepository
from app.modules.procurement_alert.schema import ProcurementAlertSchema
from app.modules.procurement_alert.model import ProcurementAlert


class ProcurementAlertService:

    def __init__(
        self,
        repository: ProcurementAlertRepository,
        db: Session
    ):

        self.repository = repository
        self.db = db


    def create_procurement_alert(
        self,
        data: ProcurementAlertSchema
    ) -> ProcurementAlert:

        procurement_alert = ProcurementAlert(
            request_id=data.request_id,
            part_id=data.part_id,
            part_name_snapshot=data.part_name_snapshot,
            alert_message=data.alert_message,
            alert_type=data.alert_type,
            is_resolved=data.is_resolved,
            created_at=data.created_at
        )

        try:

            self.repository.create(procurement_alert)
            self.db.commit()
            self.db.refresh(procurement_alert)

            return procurement_alert

        except Exception as error:

            self.db.rollback()
            raise ProcurementAlertFailedError() from error