from app.api.candidates import router as candidates_router
from app.api.jobs import router as jobs_router
from app.api.interviews import router as interviews_router
from app.api.feedback import router as feedback_router

__all__ = ["candidates_router", "jobs_router", "interviews_router", "feedback_router"]
