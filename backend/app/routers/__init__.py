"""API route handlers."""

from app.routers import auth, catalog, health, questions, tests

__all__ = [
    "auth",
    "catalog",
    "health",
    "questions",
    "tests",
]
