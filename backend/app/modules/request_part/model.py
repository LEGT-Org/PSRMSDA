from __future__ import annotations

from sqlalchemy import String, Boolean, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database import Base


class RequestPart(Base):

    __tablename__ = "request_parts"

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int | None] = mapped_column(nullable=True)
    quantity_used: Mapped[int | None] = mapped_column(nullable=True)
    part_name_snapshot: Mapped[str] = mapped_column(String(255), nullable=False)
    is_stock_validated: Mapped[bool] = mapped_column(server_default=text("0"))
    parts_used: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=None)

    # Foreign Key
    request_id: Mapped[int] = mapped_column(ForeignKey("service_requests.id"))
    part_id: Mapped[int] = mapped_column(ForeignKey("spare_parts.id"))

    # Relationship
    service_requests: Mapped["ServiceRequest"] = relationship(back_populates="request_parts")
    spare_parts: Mapped["SparePart"] = relationship(back_populates="request_parts")