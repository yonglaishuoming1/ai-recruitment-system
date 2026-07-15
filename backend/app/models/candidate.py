import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Text, DateTime, Enum as SAEnum
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
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="姓名")
    phone: Mapped[Optional[str]] = mapped_column(String(20), comment="手机号")
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, comment="邮箱")
    resume_text: Mapped[Optional[str]] = mapped_column(Text, comment="简历文本内容")
    resume_url: Mapped[Optional[str]] = mapped_column(Text, comment="简历文件地址")
    status: Mapped[CandidateStatus] = mapped_column(
        SAEnum(CandidateStatus), default=CandidateStatus.NEW, nullable=False, comment="候选人状态"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now, comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now, onupdate=datetime.now, comment="更新时间"
    )

    interviews: Mapped[list["Interview"]] = relationship(
        back_populates="candidate", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Candidate {self.name} ({self.email})>"
