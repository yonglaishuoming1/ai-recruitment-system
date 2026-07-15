import uuid
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, EmailStr, Field


# ===== Candidate =====
class CandidateBase(BaseModel):
    name: str = Field(..., max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    email: str = Field(..., max_length=255)
    resume_text: Optional[str] = None
    resume_url: Optional[str] = None
    status: Optional[str] = "new"


class CandidateCreate(CandidateBase):
    pass


class CandidateUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    resume_text: Optional[str] = None
    resume_url: Optional[str] = None
    status: Optional[str] = None


class CandidateResponse(CandidateBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ===== Job =====
class JobBase(BaseModel):
    title: str = Field(..., max_length=200)
    department: str = Field(..., max_length=100)
    jd_text: Optional[str] = None
    competency_model: Optional[dict[str, Any]] = None
    status: Optional[str] = "draft"


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    title: Optional[str] = None
    department: Optional[str] = None
    jd_text: Optional[str] = None
    competency_model: Optional[dict[str, Any]] = None
    status: Optional[str] = None


class JobResponse(JobBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ===== Interview =====
class InterviewBase(BaseModel):
    candidate_id: uuid.UUID
    job_id: Optional[uuid.UUID] = None
    round: int = 1
    interviewer: Optional[str] = None
    scheduled_time: datetime
    status: Optional[str] = "pending"


class InterviewCreate(InterviewBase):
    pass


class InterviewUpdate(BaseModel):
    round: Optional[int] = None
    interviewer: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    status: Optional[str] = None


class InterviewResponse(InterviewBase):
    id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}


# ===== Feedback =====
class FeedbackBase(BaseModel):
    interview_id: uuid.UUID
    dimension_scores: Optional[dict[str, Any]] = None
    comment: Optional[str] = None
    evaluator: Optional[str] = None


class FeedbackCreate(FeedbackBase):
    pass


class FeedbackUpdate(BaseModel):
    dimension_scores: Optional[dict[str, Any]] = None
    comment: Optional[str] = None
    evaluator: Optional[str] = None


class FeedbackResponse(FeedbackBase):
    id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}


# ===== Pagination =====
class PaginatedResponse(BaseModel):
    items: list[Any]
    total: int
    page: int
    page_size: int
