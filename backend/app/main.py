"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import health


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    application = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="API for SSC Prep Platform — Competitive Exam Preparation",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(health.router, prefix="/api", tags=["Health"])

    return application


app = create_app()
