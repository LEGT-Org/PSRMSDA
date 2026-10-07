from __future__ import annotations
from datetime import datetime

from sqlalchemy import DateTime, String, Enum, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.modules.user.schema import UserRole
from app.shared.database import Base


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=True)
    token_hash: Mapped[str] = mapped_column(String(255), nullable=True)
    email_verified: Mapped[bool] = mapped_column(server_default=text("0"))
    is_active: Mapped[bool] = mapped_column(server_default=text("0"))

    role: Mapped[UserRole] = mapped_column(
        Enum(
            UserRole,
            name="user_role",
            values_callable=lambda enum_class: [member.value for member in enum_class]
        ),
        server_default=UserRole.USER.value,
        nullable=False
    )
    

    # Timestamp
    token_expire: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Relationship
    service_requests: Mapped[list["ServiceRequest"]] = relationship(back_populates="users")