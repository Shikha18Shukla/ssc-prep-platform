"""TestAttempt model."""

import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SAEnum,
    Float,
    ForeignKey,
    Index,
    Integer,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin
from app.models.question import Difficulty

if TYPE_CHECKING:
    from app.models.chapter import Chapter
    from app.models.exam import Exam
    from app.models.subject import Subject
    from app.models.test_question import TestQuestion
    from app.models.user import User
    from app.models.user_answer import UserAnswer


class TestAttemptStatus(str, enum.Enum):
    """Test attempt lifecycle status."""

    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    AUTO_SUBMITTED = "AUTO_SUBMITTED"


class TestAttempt(Base, TimestampMixin):
    """Represents a user's timed MCQ test session (in-progress, completed, or auto-submitted)."""

    __tablename__ = "test_attempts"
    __table_args__ = (
        Index("ix_test_attempts_user_created", "user_id", "created_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    exam_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("exams.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    subject_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("subjects.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    chapter_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid,
        ForeignKey("chapters.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    difficulty: Mapped[Difficulty | None] = mapped_column(
        SAEnum(Difficulty, name="difficulty_level"),
        nullable=True,
    )
    is_pyq: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    question_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    duration_seconds: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    submitted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    status: Mapped[TestAttemptStatus] = mapped_column(
        SAEnum(TestAttemptStatus, name="test_attempt_status"),
        default=TestAttemptStatus.IN_PROGRESS,
        nullable=False,
        index=True,
    )
    score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    correct_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    wrong_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    unanswered_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    time_taken_seconds: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="test_attempts",
    )
    exam: Mapped["Exam"] = relationship(
        "Exam",
        back_populates="test_attempts",
    )
    subject: Mapped["Subject"] = relationship(
        "Subject",
        back_populates="test_attempts",
    )
    chapter: Mapped["Chapter | None"] = relationship(
        "Chapter",
        back_populates="test_attempts",
    )
    test_questions: Mapped[list["TestQuestion"]] = relationship(
        "TestQuestion",
        back_populates="test_attempt",
        cascade="all, delete-orphan",
        order_by="TestQuestion.question_order",
    )
    user_answers: Mapped[list["UserAnswer"]] = relationship(
        "UserAnswer",
        back_populates="test_attempt",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<TestAttempt id={self.id} status={self.status} score={self.score}>"
