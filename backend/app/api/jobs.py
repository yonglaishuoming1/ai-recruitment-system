import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.job import Job
from app.schemas import (
    JobCreate,
    JobUpdate,
    JobResponse,
    PaginatedResponse,
)

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("", response_model=PaginatedResponse)
async def list_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    department: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Job)
    if status:
        query = query.where(Job.status == status)
    if department:
        query = query.where(Job.department == department)
    query = query.order_by(Job.created_at.desc())

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    items = result.scalars().all()

    return PaginatedResponse(
        total=total,
        page=(skip // limit) + 1,
        page_size=limit,
        items=[JobResponse.model_validate(j) for j in items],
    )


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobResponse.model_validate(job)


@router.post("", response_model=JobResponse, status_code=201)
async def create_job(data: JobCreate, db: AsyncSession = Depends(get_db)):
    job = Job(**data.model_dump())
    db.add(job)
    await db.flush()
    await db.refresh(job)
    return JobResponse.model_validate(job)


@router.patch("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: uuid.UUID,
    data: JobUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(job, key, value)

    await db.flush()
    await db.refresh(job)
    return JobResponse.model_validate(job)


@router.delete("/{job_id}", status_code=204)
async def delete_job(job_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    await db.delete(job)
