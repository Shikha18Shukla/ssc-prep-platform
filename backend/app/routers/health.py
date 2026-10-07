"""Health check endpoint."""

from fastapi import APIRouter

from app.config import settings

router = APIRouter()


@router.get("/health")
async def health_check() -> dict[str, str]:
    """Check if the API is running and healthy."""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }
