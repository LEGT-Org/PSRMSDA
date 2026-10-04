from __future__ import annotations
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    ForeignKey,
    DateTime, 
    String, 
    Text, 
    Enum,
    JSON
)

from app.shared.database import Base
from app.modules.service_request.schema import ServiceRequestStatus


class ServiceRequest(Base):

    __tablename__ = "service_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    device_type: Mapped[str] = mapped_column(String(255), nullable=False)
    device_model: Mapped[str] = mapped_column(String(255), nullable=False)
    device_brand: Mapped[str] = mapped_column(String(255), nullable=False)
    fault_description: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    technician_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    sop_instructions: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    status: Mapped[ServiceRequestStatus] = mapped_column(
        Enum(
            ServiceRequestStatus,
            name="service_request_status"
        ),
        server_default=ServiceRequestStatus.PENDING
    )

    # Foreign Key
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # Timestamp
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Relationship
    users: Mapped["User"] = relationship(back_populates="service_requests")
    customers: Mapped["Customer"] = relationship(back_populates="service_requests")
    llm_diagnosis: Mapped[Optional["LLMDiagnosis"]] = relationship(back_populates="service_requests", uselist=False)
    request_parts: Mapped[list["RequestPart"]] = relationship(back_populates="service_requests")
    procurement_alerts: Mapped[list["ProcurementAlert"]] = relationship(back_populates="service_requests")