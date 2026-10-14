from datetime import datetime
from sqlalchemy import select, cast, func, or_, select, String
from sqlalchemy.orm import Session

from app.modules.procurement_alert.model import ProcurementAlert
from app.modules.procurement_alert.schema import ProcurementAlertType


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


    def get_all(
        self,
        page: int,
        limit: int,
        search: str | None = None,
        is_resolved: bool | None = None,
        alert_type: ProcurementAlertType | None = None,
    ) -> tuple[list[ProcurementAlert], int]:

        statement = select(ProcurementAlert)

        if search and search.strip():
            search_value = f"%{search.strip()}%"

            statement = statement.where(
                or_(
                    ProcurementAlert.alert_message.ilike(search_value),
                    ProcurementAlert.part_name_snapshot.ilike(search_value),
                    cast(ProcurementAlert.request_id, String).ilike(search_value),
                )
            )

        if is_resolved is not None:
            statement = statement.where(
                ProcurementAlert.is_resolved.is_(is_resolved)
            )

        if alert_type is not None:
            statement = statement.where(
                ProcurementAlert.alert_type == alert_type
            )

        # Count records matching the current filters.
        count_statement = (
            select(func.count())
            .select_from(statement.subquery())
        )

        total = self.db.scalar(count_statement) or 0

        # Fetch only the requested page.
        statement = (
            statement
            .order_by(
                ProcurementAlert.created_at.desc(),
                ProcurementAlert.id.desc(),
            )
            .offset((page - 1) * limit)
            .limit(limit)
        )

        alerts = list(self.db.scalars(statement).all())

        return alerts, total


    def get_summary(
        self
    ) -> dict[str, int]:

        total_alerts = self.db.scalar(select(func.count()).select_from(ProcurementAlert)) or 0
        unresolved_alerts = self.db.scalar(
            select(func.count())
            .select_from(ProcurementAlert)
            .where(ProcurementAlert.is_resolved.is_(False))
        ) or 0

        resolved_alerts = self.db.scalar(
            select(func.count())
            .select_from(ProcurementAlert)
            .where(ProcurementAlert.is_resolved.is_(True))
        ) or 0

        return {
            "total_alerts": total_alerts,
            "unresolved_alerts": unresolved_alerts,
            "resolved_alerts": resolved_alerts,
        }


    def get_by_id(
        self,
        alert_id: int,
    ) -> ProcurementAlert | None:

        statement = select(ProcurementAlert).where(
            ProcurementAlert.id == alert_id
        )

        return self.db.scalar(statement)


    def update(
        self,
        stored_procurement_alert: ProcurementAlert,
        is_resolved: bool,
        now: datetime
    ) -> None:

        stored_procurement_alert.is_resolved = is_resolved
        stored_procurement_alert.updated_at = now