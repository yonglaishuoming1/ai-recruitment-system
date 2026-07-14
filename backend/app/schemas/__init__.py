import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


# ── Candidate ──
class CandidateBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    position: str
    resume_url: Optional[str] = None
    notes: Optional[str] = None


class CandidateCreate(CandidateBase):
    pass


class CandidateUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    position: Optional[str] = None
    status: Optional[str] = None
    resume_url: Optional[str] = None
    ai_score: Optional[float] = None
    notes: Optional[str] = None


class CandidateResponse(CandidateBase):
    id: uuid.UUID
    status: str
    ai_score: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CandidateListResponse(BaseModel):
    total: int
    items: list[CandidateResponse]


# ── Job ──
class JobBase(BaseModel):
    title: str
    department: str
    location: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    salary_range: Optional[str] = None
    headcount: int = 1


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    title: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    salary_range: Optional[str] = None
    headcount: Optional[int] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None


class JobResponse(JobBase):
    id: uuid.UUID
    status: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Interview ──
class InterviewBase(BaseModel):
    candidate_id: uuid.UUID
    job_id: Optional[uuid.UUID] = None
    interview_type: str
    scheduled_at: datetime
    duration_minutes: int = 60
    interviewer: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None


class InterviewCreate(InterviewBase):
    pass


class InterviewUpdate(BaseModel):
    status: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    interviewer: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None
    feedback: Optional[str] = None
    rating: Optional[int] = None


class InterviewResponse(InterviewBase):
    id: uuid.UUID
    status: str
    feedback: Optional[str] = None
    rating: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
