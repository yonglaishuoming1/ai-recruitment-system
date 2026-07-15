import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.feedback import Feedback
from app.schemas import (
    FeedbackCreate,
    FeedbackUpdate,
    FeedbackResponse,
    PaginatedResponse,
)

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.get("/interview/{interview_id}", response_model=PaginatedResponse)
async def list_feedback_by_interview(
    interview_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(Feedback)
        .where(Feedback.interview_id == interview_id)
        .order_by(Feedback.created_at.desc())
    )

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    result = await db.execute(query)
    items = result.scalars().all()

    return PaginatedResponse(
        total=total,
        page=1,
        page_size=total or 20,
        items=[FeedbackResponse.model_validate(f) for f in items],
    )


@router.post("", response_model=FeedbackResponse, status_code=201)
async def create_feedback(data: FeedbackCreate, db: AsyncSession = Depends(get_db)):
    feedback = Feedback(**data.model_dump())
    db.add(feedback)
    await db.flush()
    await db.refresh(feedback)
    return FeedbackResponse.model_validate(feedback)


@router.patch("/{feedback_id}", response_model=FeedbackResponse)
async def update_feedback(
    feedback_id: uuid.UUID,
    data: FeedbackUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Feedback).where(Feedback.id == feedback_id))
    feedback = result.scalar_one_or_none()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(feedback, key, value)

    await db.flush()
    await db.refresh(feedback)
    return FeedbackResponse.model_validate(feedback)


@router.delete("/{feedback_id}", status_code=204)
async def delete_feedback(
    feedback_id: uuid.UUID, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Feedback).where(Feedback.id == feedback_id))
    feedback = result.scalar_one_or_none()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    await db.delete(feedback)
