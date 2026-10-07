"""Question and QuestionOption models."""

import enum
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    Enum as SAEnum,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.chapter import Chapter
    from app.models.test_question import TestQuestion


class Difficulty(str, enum.Enum):
    """Question difficulty levels.

    PYQ is NOT a difficulty level. It is tracked separately via
    `is_pyq` and `pyq_year`.
    """

    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


class Question(Base, TimestampMixin):
    """MCQ question entity supporting full Unicode (Hindi/Devanagari)."""

    __tablename__ = "questions"
    __table_args__ = (
        Index(
            "ix_questions_chapter_diff_pyq_active",
            "chapter_id",
            "difficulty",
            "is_pyq",
            "is_active",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )
    chapter_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("chapters.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    question_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    explanation: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    difficulty: Mapped[Difficulty] = mapped_column(
        SAEnum(Difficulty, name="difficulty_level"),
        nullable=False,
        index=True,
    )
    is_pyq: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
    )
    pyq_year: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        index=True,
    )
    pyq_exam_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    source: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        index=True,
    )

    # Relationships
    chapter: Mapped["Chapter"] = relationship(
        "Chapter",
        back_populates="questions",
    )
    options: Mapped[list["QuestionOption"]] = relationship(
        "QuestionOption",
        back_populates="question",
        cascade="all, delete-orphan",
        order_by="QuestionOption.display_order",
    )
    test_questions: Mapped[list["TestQuestion"]] = relationship(
        "TestQuestion",
        back_populates="question",
    )

    def __repr__(self) -> str:
        return f"<Question id={self.id} difficulty={self.difficulty} is_pyq={self.is_pyq}>"


class QuestionOption(Base):
    """Individual option for an MCQ question (e.g., A, B, C, D)."""

    __tablename__ = "question_options"
    __table_args__ = (
        UniqueConstraint("question_id", "option_key", name="uq_question_option_key"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )
    question_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    option_key: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )
    option_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    display_order: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )
    is_correct: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # Relationships
    question: Mapped["Question"] = relationship(
        "Question",
        back_populates="options",
    )

    def __repr__(self) -> str:
        return f"<QuestionOption id={self.id} key={self.option_key!r} is_correct={self.is_correct}>"
