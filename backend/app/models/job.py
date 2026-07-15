import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Text, DateTime, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

import enum


class JobStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    CLOSED = "closed"


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False, comment="职位名称")
    department: Mapped[str] = mapped_column(String(100), nullable=False, comment="所属部门")
    jd_text: Mapped[Optional[str]] = mapped_column(Text, comment="职位描述文本")
    competency_model: Mapped[Optional[dict]] = mapped_column(
        JSONB, comment="胜任力模型 (JSON)"
    )
    status: Mapped[JobStatus] = mapped_column(
        SAEnum(JobStatus), default=JobStatus.DRAFT, nullable=False, comment="职位状态"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now, comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now, onupdate=datetime.now, comment="更新时间"
    )

    interviews: Mapped[list["Interview"]] = relationship(
        back_populates="job", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Job {self.title} ({self.department})>"
