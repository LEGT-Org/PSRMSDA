from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    ForeignKey,
    DateTime, 
    Numeric, 
    String,
    Text, 
    Enum,
    JSON
)

from app.shared.database import Base
from app.modules.llm_diagnosis.schema import LLMDiagnosisStatus

class LLMDiagnosis(Base):

    __tablename__ = "llm_diagnosis"

    id: Mapped[int] = mapped_column(primary_key=True)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    prompt: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    raw_output: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    confidence: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    parsed_output: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    status: Mapped[LLMDiagnosisStatus] = mapped_column(
        Enum(
            LLMDiagnosisStatus,
            name="llm_diagnosis_status"
        ),
        server_default=LLMDiagnosisStatus.DRAFT,
        nullable=False
    )

    # Foreign Key
    request_id: Mapped[int] = mapped_column(ForeignKey("service_requests.id"))

    # Timestamp
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Relationship
    service_requests: Mapped["ServiceRequest"] = relationship(back_populates="llm_diagnosis")
