"""API route handlers."""

from app.routers import auth, catalog, health

__all__ = [
    "auth",
    "catalog",
    "health",
]
