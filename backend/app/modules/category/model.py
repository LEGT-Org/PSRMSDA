from __future__ import annotations

from sqlalchemy import String, Text, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database import Base


class Category(Base):

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(server_default=text("0"))

    # Foreign Key (Parent category id, self referencing key)
    parent_category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id"),
        nullable=True
    )

    # Relationship (To itself and SparePart Table)
    children: Mapped[list["Category"]] = relationship(back_populates="parent")
    parent: Mapped["Category | None"] = relationship(
        back_populates="children",
        remote_side="Category.id"
    )

    spare_parts: Mapped[list["SparePart"]] = relationship(back_populates="categories")