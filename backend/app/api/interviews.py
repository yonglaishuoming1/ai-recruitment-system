import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.core.database import get_db
from app.models.interview import Interview, InterviewStatus
from app.models.candidate import Candidate
from app.schemas import (
    InterviewCreate,
    InterviewUpdate,
    InterviewResponse,
)

router = APIRouter(prefix="/interviews", tags=["interviews"])


@router.get("")
async def list_interviews(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    candidate_id: Optional[uuid.UUID] = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Interview)
    if status:
        query = query.where(Interview.status == status)
    if candidate_id:
        query = query.where(Interview.candidate_id == candidate_id)
    query = query.order_by(Interview.scheduled_at.desc())

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    items = result.scalars().all()

    return {
        "total": total,
        "items": [InterviewResponse.model_validate(i) for i in items],
    }


@router.get("/{interview_id}", response_model=InterviewResponse)
async def get_interview(
    interview_id: uuid.UUID, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Interview).where(Interview.id == interview_id)
    )
    interview = result.scalar_one_or_none()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    return InterviewResponse.model_validate(interview)


@router.post("", response_model=InterviewResponse, status_code=201)
async def create_interview(
    data: InterviewCreate, db: AsyncSession = Depends(get_db)
):
    # Verify candidate exists
    result = await db.execute(
        select(Candidate).where(Candidate.id == data.candidate_id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Candidate not found")

    interview = Interview(**data.model_dump())
    db.add(interview)
    await db.flush()
    await db.refresh(interview)
    return InterviewResponse.model_validate(interview)


@router.patch("/{interview_id}", response_model=InterviewResponse)
async def update_interview(
    interview_id: uuid.UUID,
    data: InterviewUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Interview).where(Interview.id == interview_id)
    )
    interview = result.scalar_one_or_none()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(interview, key, value)
    await db.flush()
    await db.refresh(interview)
    return InterviewResponse.model_validate(interview)


@router.delete("/{interview_id}", status_code=204)
async def delete_interview(
    interview_id: uuid.UUID, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Interview).where(Interview.id == interview_id)
    )
    interview = result.scalar_one_or_none()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    await db.delete(interview)
