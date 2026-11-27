"""User model."""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.test_attempt import TestAttempt


class User(Base, TimestampMixin):
    """Local user account.

    Password hashes are Argon2id strings when a local password exists. A null
    hash is valid for accounts that use a verified external identity only.
    """

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    email_normalized: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    password_hash: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    password_changed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    full_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    # Explicitly granted by an operator; never accepted from public auth payloads.
    is_admin: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        server_default="false",
    )

    # Relationships
    test_attempts: Mapped[list["TestAttempt"]] = relationship(
        "TestAttempt",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    @validates("email")
    def normalize_email(self, _key: str, value: str) -> str:
        """Keep local storage and lookup keys consistently normalized."""
        normalized = value.strip().lower()
        self.email_normalized = normalized
        return normalized

    @property
    def has_password(self) -> bool:
        """Whether this account can authenticate with a local password."""
        return bool(self.password_hash)

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email!r}>"
