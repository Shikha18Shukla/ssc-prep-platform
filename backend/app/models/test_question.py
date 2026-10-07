"""TestQuestion model."""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, UniqueConstraint, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.question import Question
    from app.models.test_attempt import TestAttempt
    from app.models.user_answer import UserAnswer


class TestQuestion(Base):
    """Preserves the randomized question assignment and exact ordering for a specific test attempt."""

    __tablename__ = "test_questions"
    __table_args__ = (
        UniqueConstraint(
            "test_attempt_id",
            "question_order",
            name="uq_test_attempt_question_order",
        ),
        UniqueConstraint(
            "test_attempt_id",
            "question_id",
            name="uq_test_attempt_question",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )
    test_attempt_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("test_attempts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    question_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("questions.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    question_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Relationships
    test_attempt: Mapped["TestAttempt"] = relationship(
        "TestAttempt",
        back_populates="test_questions",
    )
    question: Mapped["Question"] = relationship(
        "Question",
        back_populates="test_questions",
    )
    user_answers: Mapped[list["UserAnswer"]] = relationship(
        "UserAnswer",
        back_populates="test_question",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<TestQuestion id={self.id} attempt={self.test_attempt_id} order={self.question_order}>"
