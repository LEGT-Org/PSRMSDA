from __future__ import annotations
from datetime import datetime

from sqlalchemy import (
    ForeignKey, 
    DateTime, 
    String,
    Enum, 
    text
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.modules.procurement_alert.schema import ProcurementAlertType
from app.shared.database import Base


class ProcurementAlert(Base):

    __tablename__ = "procurement_alerts"

    id: Mapped[int] = mapped_column(primary_key=True)
    alert_message: Mapped[str] = mapped_column(String(255), nullable=True)
    part_name_snapshot: Mapped[str] = mapped_column(String(255), nullable=True)
    is_resolved: Mapped[bool] = mapped_column(server_default=text("0"))

    alert_type: Mapped[ProcurementAlertType] = mapped_column(
        Enum(
            ProcurementAlertType,
            name="procurement_alert_type",
            values_callable=lambda enum_class: [member.value for member in enum_class]
        ),
        server_default=ProcurementAlertType.PART_SELECTED.value,
        nullable=False
    )

    # Foreign Key
    request_id: Mapped[int] = mapped_column(ForeignKey("service_requests.id"), nullable=False)
    part_id: Mapped[int] = mapped_column(ForeignKey("spare_parts.id"), nullable=True)

    # Timestamp
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Relationship
    service_requests: Mapped["ServiceRequest"] = relationship(back_populates="procurement_alerts")
    spare_parts: Mapped["SparePart"] = relationship(back_populates="procurement_alerts")