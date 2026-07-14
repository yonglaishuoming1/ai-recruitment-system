import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.candidate import Candidate, CandidateStatus
from app.schemas import (
    CandidateCreate,
    CandidateUpdate,
    CandidateResponse,
    CandidateListResponse,
)

router = APIRouter(prefix="/candidates", tags=["candidates"])


@router.get("", response_model=CandidateListResponse)
async def list_candidates(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Candidate)
    if status:
        query = query.where(Candidate.status == status)
    if search:
        query = query.where(
            Candidate.name.ilike(f"%{search}%")
            | Candidate.email.ilike(f"%{search}%")
            | Candidate.position.ilike(f"%{search}%")
        )
    query = query.order_by(Candidate.created_at.desc())

    # Count
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    # Paginate
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    items = result.scalars().all()

    return CandidateListResponse(
        total=total,
        items=[CandidateResponse.model_validate(c) for c in items],
    )


@router.get("/{candidate_id}", response_model=CandidateResponse)
async def get_candidate(candidate_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Candidate).where(Candidate.id == candidate_id))
    candidate = result.scalar_one_or_none()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return CandidateResponse.model_validate(candidate)


@router.post("", response_model=CandidateResponse, status_code=201)
async def create_candidate(data: CandidateCreate, db: AsyncSession = Depends(get_db)):
    candidate = Candidate(**data.model_dump())
    db.add(candidate)
    await db.flush()
    await db.refresh(candidate)
    return CandidateResponse.model_validate(candidate)


@router.patch("/{candidate_id}", response_model=CandidateResponse)
async def update_candidate(
    candidate_id: uuid.UUID,
    data: CandidateUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Candidate).where(Candidate.id == candidate_id))
    candidate = result.scalar_one_or_none()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(candidate, key, value)

    await db.flush()
    await db.refresh(candidate)
    return CandidateResponse.model_validate(candidate)


@router.delete("/{candidate_id}", status_code=204)
async def delete_candidate(
    candidate_id: uuid.UUID, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Candidate).where(Candidate.id == candidate_id))
    candidate = result.scalar_one_or_none()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    await db.delete(candidate)
