from math import ceil
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.modules.procurement_alert.repository import ProcurementAlertRepository
from app.modules.procurement_alert.model import ProcurementAlert

from app.modules.procurement_alert.schema import (
    ProcurementAlertPageListResponse,
    RecentActivitiesResponse,
    ProcurementAlertSchema,
    ProcurementAlertType,
    RecentActivityItem
)

from app.shared.exception import (
    ProcurementAlertIsAlreadyBeenResolvedError,
    ProcurementAlertDoesNotExistError,
    ProcurementAlertFailedError,
)


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
            created_at=data.created_at,
            updated_at=data.created_at
        )

        try:

            self.repository.create(procurement_alert)
            self.db.flush()

            return procurement_alert

        except Exception as error:

            print(error)

            raise ProcurementAlertFailedError() from error


    def get_procurement_alerts(
        self,
        page: int,
        limit: int,
        search: str | None = None,
        is_resolved: bool | None = None,
        alert_type: ProcurementAlertType | None = None,
    ) -> ProcurementAlertPageListResponse:

        alerts, total = self.repository.get_all(
            page=page,
            limit=limit,
            search=search,
            is_resolved=is_resolved,
            alert_type=alert_type,
        )

        summary = self.repository.get_summary()

        pages = ceil(total / limit) if total else 0

        return {
            "items": alerts,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": pages,
            **summary
        }


    def get_recent_activities(
        self
    ) -> RecentActivitiesResponse:

        alerts = self.repository.get_recent_activities()

        return RecentActivitiesResponse(
            items=[
                RecentActivityItem(
                    id=alert.id,
                    description=alert.alert_message,
                    time=alert.created_at,
                )
                for alert in alerts
            ]
        )


    def update_resolution(
        self,
        alert_id: int,
        is_resolved: bool,
    ) -> None:

        now = datetime.now(timezone.utc).replace(tzinfo=None)
        alert = self.repository.get_by_id(alert_id)

        if alert.is_resolved == is_resolved:
            return

        if alert is None:
            raise ProcurementAlertDoesNotExistError(
                detail=f"Procurement alert {alert_id} not found.",
            )

        if alert.is_resolved == True:
            raise ProcurementAlertIsAlreadyBeenResolvedError()

        try:

            self.repository.update(
                stored_procurement_alert=alert,
                is_resolved=is_resolved,
                now=now
            )

            self.db.commit()
            self.db.refresh(alert)

        except Exception as error:

            self.db.rollback()

            print(error)
            raise ProcurementAlertFailedError() from error