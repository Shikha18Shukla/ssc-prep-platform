"""Base model class and mixins for all SQLAlchemy models."""

from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all database models.

    All models inherit from this class so that Alembic can discover
    them through ``Base.metadata``.
    """

    pass


class TimestampMixin:
    """Adds timezone-aware ``created_at`` and ``updated_at`` columns.

    ``created_at`` is set automatically on INSERT via ``server_default``.
    ``updated_at`` is refreshed on every UPDATE via SQLAlchemy's
    ``onupdate`` hook.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
