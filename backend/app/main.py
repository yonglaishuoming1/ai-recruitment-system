from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine, Base
from app.api import candidates_router, jobs_router, interviews_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables (for development; use Alembic in production)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/health")
async def health_check():
    return {"status": "ok", "version": settings.APP_VERSION}


# Routers
app.include_router(candidates_router, prefix="/api/v1")
app.include_router(jobs_router, prefix="/api/v1")
app.include_router(interviews_router, prefix="/api/v1")
