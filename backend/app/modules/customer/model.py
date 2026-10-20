from __future__ import annotations
from datetime import datetime

from sqlalchemy import DateTime, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database import Base


class Customer(Base):

    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True, unique=True)
    phone_number: Mapped[str] = mapped_column(String(16), nullable=False)

    # Foreign Key
    last_modified_by_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    # Timestamp
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Relationship
    users: Mapped["User | None"] = relationship(foreign_keys=[last_modified_by_id])
    service_requests: Mapped[list["ServiceRequest"]] = relationship(back_populates="customers")
