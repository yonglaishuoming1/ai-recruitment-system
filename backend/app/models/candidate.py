import uuid
from datetime import date, datetime
from typing import Optional

from sqlalchemy import String, Text, Date, DateTime, Float, Enum as SAEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

import enum


class CandidateStatus(str, enum.Enum):
    NEW = "new"
    SCREENING = "screening"
    INTERVIEWING = "interviewing"
    OFFERED = "offered"
    HIRED = "hired"
    REJECTED = "rejected"


class Candidate(Base):
    __tablename__ = "candidates"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    position: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[CandidateStatus] = mapped_column(
        SAEnum(CandidateStatus), default=CandidateStatus.NEW, nullable=False
    )
    resume_url: Mapped[Optional[str]] = mapped_column(Text)
    ai_score: Mapped[Optional[float]] = mapped_column(Float)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now, onupdate=datetime.now
    )

    # Relationships
    interviews: Mapped[list["Interview"]] = relationship(
        back_populates="candidate", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Candidate {self.name} ({self.email})>"
