import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    interview_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("interviews.id"), nullable=False, comment="面试 ID"
    )
    dimension_scores: Mapped[Optional[dict]] = mapped_column(
        JSONB, comment="各维度评分 (JSON)"
    )
    comment: Mapped[Optional[str]] = mapped_column(Text, comment="评语")
    evaluator: Mapped[Optional[str]] = mapped_column(String(100), comment="评价人")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now, comment="创建时间"
    )

    interview: Mapped["Interview"] = relationship(back_populates="feedbacks")

    def __repr__(self) -> str:
        return f"<Feedback interview={self.interview_id} evaluator={self.evaluator}>"
