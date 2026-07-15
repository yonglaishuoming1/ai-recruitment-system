import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Text, DateTime, Integer, Enum as SAEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

import enum


class InterviewStatus(str, enum.Enum):
    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"


class Interview(Base):
    __tablename__ = "interviews"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("candidates.id"), nullable=False, comment="候选人 ID"
    )
    job_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("jobs.id"), comment="职位 ID"
    )
    round: Mapped[int] = mapped_column(Integer, default=1, comment="面试轮次")
    interviewer: Mapped[Optional[str]] = mapped_column(String(100), comment="面试官")
    scheduled_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, comment="面试时间"
    )
    status: Mapped[InterviewStatus] = mapped_column(
        SAEnum(InterviewStatus),
        default=InterviewStatus.PENDING,
        nullable=False,
        comment="面试结果",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now, comment="创建时间"
    )

    candidate: Mapped["Candidate"] = relationship(back_populates="interviews")
    job: Mapped[Optional["Job"]] = relationship(back_populates="interviews")
    feedbacks: Mapped[list["Feedback"]] = relationship(
        back_populates="interview", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Interview round={self.round} status={self.status.value}>"
