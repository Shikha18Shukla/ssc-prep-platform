"""Health check endpoint."""

from fastapi import APIRouter
from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from pathlib import Path
from alembic.config import Config
from alembic.script import ScriptDirectory
from app.database.session import engine

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


@router.get("/ready")
def readiness_check() -> dict[str, str]:
    """Return ready only when the database is reachable at the application's head revision."""
    try:
        migration_config = Config(str(Path(__file__).resolve().parents[2] / "alembic.ini"))
        expected_revision = ScriptDirectory.from_config(migration_config).get_current_head()
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            actual_revision = connection.execute(text("SELECT version_num FROM alembic_version")).scalar_one_or_none()
            if actual_revision != expected_revision:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Database schema is not at the required revision",
                )
            if settings.BETA_INVITATIONS_REQUIRED:
                capacity = connection.execute(text("SELECT max_accounts FROM beta_capacity WHERE id = 1")).scalar_one_or_none()
                if capacity is None or capacity > 200:
                    raise HTTPException(
                        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        detail="Beta account capacity is not configured",
                    )
    except HTTPException:
        raise
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database or required schema unavailable") from exc
    return {"status": "ready", "service": settings.APP_NAME, "version": settings.APP_VERSION}
