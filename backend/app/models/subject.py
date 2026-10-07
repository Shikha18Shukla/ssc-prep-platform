"""Subject model."""

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.chapter import Chapter
    from app.models.exam import Exam
    from app.models.test_attempt import TestAttempt


class Subject(Base, TimestampMixin):
    """Subject within an exam (e.g., GK/GS, Maths, English, Reasoning)."""

    __tablename__ = "subjects"
    __table_args__ = (
        UniqueConstraint("exam_id", "slug", name="uq_subject_exam_slug"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )
    exam_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("exams.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    slug: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    display_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # Relationships
    exam: Mapped["Exam"] = relationship(
        "Exam",
        back_populates="subjects",
    )
    chapters: Mapped[list["Chapter"]] = relationship(
        "Chapter",
        back_populates="subject",
        cascade="all, delete-orphan",
        order_by="Chapter.display_order",
    )
    test_attempts: Mapped[list["TestAttempt"]] = relationship(
        "TestAttempt",
        back_populates="subject",
    )

    def __repr__(self) -> str:
        return f"<Subject id={self.id} slug={self.slug!r} exam_id={self.exam_id}>"
