"""UserAnswer model."""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.test_attempt import TestAttempt
    from app.models.test_question import TestQuestion


class UserAnswer(Base):
    """Records a user's selected answer for a specific test question during an attempt."""

    __tablename__ = "user_answers"
    __table_args__ = (
        UniqueConstraint(
            "test_attempt_id",
            "test_question_id",
            name="uq_test_attempt_test_question_answer",
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
    test_question_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("test_questions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    selected_option: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )
    is_correct: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
    )
    is_answered: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    answered_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Relationships
    test_attempt: Mapped["TestAttempt"] = relationship(
        "TestAttempt",
        back_populates="user_answers",
    )
    test_question: Mapped["TestQuestion"] = relationship(
        "TestQuestion",
        back_populates="user_answers",
    )

    def __repr__(self) -> str:
        return (
            f"<UserAnswer id={self.id} option={self.selected_option!r} is_answered={self.is_answered}>"
        )
