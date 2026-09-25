from __future__ import annotations
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    ForeignKey,
    DateTime, 
    Numeric, 
    String,
    Text
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database import Base


class SparePart(Base):

    __tablename__ = "spare_parts"

    id: Mapped[int] = mapped_column(primary_key=True)
    part_name: Mapped[str] = mapped_column(String(255), nullable=False)
    device_model: Mapped[str] = mapped_column(Text, nullable=True)
    device_brand: Mapped[str] = mapped_column(Text, nullable=True)
    specifications: Mapped[str] = mapped_column(Text, nullable=True)
    stock_quality: Mapped[int] = mapped_column(nullable=True)
    unit_cost: Mapped[Decimal] = mapped_column(Numeric(10, 2),nullable=True)
    shelf_location: Mapped[str] = mapped_column(String(255), nullable=False)
    image_url: Mapped[str] = mapped_column(String(255), nullable=True)

    # Foreign Key
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    # Timestamp
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Relationship (Category Table)
    categories: Mapped["Category"] = relationship(back_populates="spare_parts")
    request_parts: Mapped[list["RequestPart"]] = relationship(back_populates="spare_parts")
    procurement_alerts: Mapped[list["ProcurementAlert"]] = relationship(back_populates="spare_parts")