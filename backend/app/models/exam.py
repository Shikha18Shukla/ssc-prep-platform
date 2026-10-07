"""Exam model."""

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.subject import Subject
    from app.models.test_attempt import TestAttempt


class Exam(Base, TimestampMixin):
    """Competitive exam category (e.g., SSC, Railway, Banking, Police)."""

    __tablename__ = "exams"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    slug: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # Relationships
    subjects: Mapped[list["Subject"]] = relationship(
        "Subject",
        back_populates="exam",
        cascade="all, delete-orphan",
        order_by="Subject.display_order",
    )
    test_attempts: Mapped[list["TestAttempt"]] = relationship(
        "TestAttempt",
        back_populates="exam",
    )

    def __repr__(self) -> str:
        return f"<Exam id={self.id} slug={self.slug!r} is_active={self.is_active}>"
