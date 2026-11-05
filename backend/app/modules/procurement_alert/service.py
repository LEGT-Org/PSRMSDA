from math import ceil
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.modules.procurement_alert.repository import ProcurementAlertRepository
from app.modules.spare_part.repository import SparePartRepository
from app.modules.procurement_alert.model import ProcurementAlert

from app.modules.procurement_alert.schema import (
    ProcurementAlertPageListResponse,
    RecentActivitiesResponse,
    ProcurementAlertSchema,
    LowStockCheckResponse,
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
        db: Session,
        repository: ProcurementAlertRepository,
    ):

        self.repository = repository
        self.spare_part_interface = SparePartRepository(db)
        self.db = db


    def create_procurement_alert(
        self,
        data: ProcurementAlertSchema
    ) -> ProcurementAlert:

        procurement_alert = ProcurementAlert(
            request_id=data.request_id,
            part_id=data.part_id,
            part_name_snapshot=data.part_name_snapshot,
            low_stock_parts_snapshot=data.low_stock_parts_snapshot,
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

        return ProcurementAlertPageListResponse(
            items=alerts,
            total=total,
            page=page,
            limit=limit,
            pages=pages,
            **summary,
        )


    def get_procurement_alert_by_id(
        self,
        alert_id: int,
    ) -> ProcurementAlert:

        procurement_alert = self.repository.get_by_id(
            alert_id=alert_id
        )

        if not procurement_alert:
            raise ProcurementAlertDoesNotExistError()

        return procurement_alert


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

        alert = self.repository.get_by_id(alert_id)

        if alert is None:
            raise ProcurementAlertDoesNotExistError(
                detail=f"Procurement alert {alert_id} not found.",
            )

        if alert.is_resolved == is_resolved:
            return

        if alert.is_resolved:
            raise ProcurementAlertIsAlreadyBeenResolvedError()

        now = datetime.now(timezone.utc).replace(tzinfo=None)

        try:
            self.repository.update(
                stored_procurement_alert=alert,
                is_resolved=is_resolved,
                now=now,
            )

            self.db.commit()
            self.db.refresh(alert)

        except Exception as error:
            self.db.rollback()
            print(error)
            raise ProcurementAlertFailedError() from error


    def check_low_stock(
        self,
        threshold: int = 5,
    ) -> LowStockCheckResponse:

        now = datetime.now(timezone.utc).replace(tzinfo=None)

        try:

            # 1. Retrieve all low-stock spare parts.
            low_stock_parts = self.spare_part_interface.get_low_stocks(
                threshold=threshold
            )

            # 2. No low-stock parts found.
            if not low_stock_parts:

                return LowStockCheckResponse(
                    message="No low-stock spare parts found.",
                    alert_created=False,
                    total_low_stock_parts=0,
                    alert=None,
                )

            # 3. Build the snapshot.
            low_stock_snapshot = [
                {
                    "part_id": part.id,
                    "part_name": part.part_name,
                    "stock_quantity": part.stock_quantity,
                }
                for part in low_stock_parts
            ]

            # 4. Build the alert message.
            alert_message = (
                f"{len(low_stock_parts)} spare part(s) "
                f"have reached or fallen below the stock threshold "
                f"of {threshold}."
            )

            # 5. Find an existing unresolved low-stock alert.
            existing_alert = (
                self.repository.get_unresolved_low_stock_alert()
            )

            alert_created = False

            if existing_alert:

                # 6. Update the existing alert.
                self.repository.update_low_stock_snapshot(
                    stored_procurement_alert=existing_alert,
                    low_stock_parts_snapshot=low_stock_snapshot,
                    alert_message=alert_message,
                    now=now,
                )

                procurement_alert = existing_alert

            else:

                # 7. Create one new procurement alert.
                procurement_alert = ProcurementAlert(
                    request_id=None,
                    part_id=None,
                    part_name_snapshot=None,
                    low_stock_parts_snapshot=low_stock_snapshot,
                    alert_message=alert_message,
                    alert_type=ProcurementAlertType.INSUFFICIENT_STOCK,
                    is_resolved=False,
                    created_at=now,
                    updated_at=now,
                )

                self.repository.create(procurement_alert)

                alert_created = True

            # 8. Save the transaction.
            self.db.commit()
            self.db.refresh(procurement_alert)

            return LowStockCheckResponse(
                message=(
                    "Low-stock procurement alert created."
                    if alert_created
                    else "Existing low-stock procurement alert updated."
                ),
                alert_created=alert_created,
                total_low_stock_parts=len(low_stock_parts),
                alert=procurement_alert,
            )

        except Exception as error:

            self.db.rollback()

            print(error)

            raise ProcurementAlertFailedError() from error


    def sync_inventory_stock_alert(
        self,
        part_id: int,
        part_name: str,
        stock_quantity: int,
    ) -> None:

        now = datetime.now(timezone.utc).replace(tzinfo=None)

        try:
            existing_alert = (
                self.repository.get_unresolved_inventory_alert(
                    part_id=part_id
                )
            )

            # Stock is sufficient: resolve an existing individual alert.
            if stock_quantity > 5:

                if existing_alert:
                    self.repository.update(
                        stored_procurement_alert=existing_alert,
                        is_resolved=True,
                        now=now,
                    )

                return

            # Determine the alert message.
            if stock_quantity == 0:
                alert_message = (
                    f"Spare part {part_name} "
                    f"(ID: {part_id}) is out of stock."
                )
            else:
                alert_message = (
                    f"Spare part {part_name} "
                    f"(ID: {part_id}) has low stock. "
                    f"Remaining quantity: {stock_quantity}."
                )

            # Update an existing unresolved alert.
            if existing_alert:

                self.repository.update_inventory_alert(
                    stored_procurement_alert=existing_alert,
                    alert_message=alert_message,
                    now=now,
                )

                return

            # Create a new individual inventory alert.
            self.create_procurement_alert(
                data=ProcurementAlertSchema(
                    request_id=None,
                    part_id=part_id,
                    part_name_snapshot=part_name,
                    low_stock_parts_snapshot=None,
                    alert_message=alert_message,
                    alert_type=ProcurementAlertType.INSUFFICIENT_STOCK,
                    is_resolved=False,
                    created_at=now,
                )
            )

        except ProcurementAlertFailedError:
            raise

        except Exception as error:
            print(error)
            raise ProcurementAlertFailedError() from error