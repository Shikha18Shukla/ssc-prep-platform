"""FastAPI application entry point."""

import logging
import traceback
import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.routers import admin, auth, catalog, health, questions, tests

logger = logging.getLogger("ssc_prep.api")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    application = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="API for SSC Prep Platform — Competitive Exam Preparation",
        docs_url="/api/docs" if settings.ENVIRONMENT.strip().lower() != "production" else None,
        redoc_url="/api/redoc" if settings.ENVIRONMENT.strip().lower() != "production" else None,
        openapi_url="/api/openapi.json" if settings.ENVIRONMENT.strip().lower() != "production" else None,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=False,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
    )

    @application.middleware("http")
    async def add_request_context(request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        return response

    @application.exception_handler(Exception)
    async def safe_unhandled_error(request: Request, exc: Exception):
        request_id = getattr(request.state, "request_id", "unavailable")
        route = getattr(request.scope.get("route"), "path", "unmatched")
        frames = traceback.extract_tb(exc.__traceback__) if exc.__traceback__ else []
        safe_frames = " > ".join(
            f"{frame.filename.rsplit('/', 1)[-1].rsplit(chr(92), 1)[-1]}:{frame.name}:{frame.lineno}"
            for frame in frames[-8:]
        )
        logger.error(
            "Unhandled API exception request_id=%s route=%s exception_type=%s frames=%s",
            request_id,
            route,
            type(exc).__name__,
            safe_frames,
        )
        return JSONResponse(
            status_code=500,
            content={"detail": "An unexpected server error occurred.", "request_id": request_id},
            headers={"X-Request-ID": request_id},
        )

    application.include_router(health.router, prefix="/api", tags=["Health"])
    application.include_router(auth.router, prefix="/api")
    application.include_router(admin.router, prefix="/api")
    application.include_router(catalog.router, prefix="/api")
    application.include_router(questions.router, prefix="/api")
    application.include_router(tests.router, prefix="/api")

    return application


app = create_app()
