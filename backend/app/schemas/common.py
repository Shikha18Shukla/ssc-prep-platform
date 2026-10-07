"""Basic Pydantic schemas for database entities."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.question import Difficulty
from app.models.test_attempt import TestAttemptStatus


class UserBase(BaseModel):
    """Base user attributes."""

    email: EmailStr
    full_name: str | None = None
    is_active: bool = True


class UserRead(UserBase):
    """User read schema."""

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ExamBase(BaseModel):
    """Base exam attributes."""

    name: str
    slug: str
    description: str | None = None
    is_active: bool = False


class ExamRead(ExamBase):
    """Exam read schema."""

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SubjectBase(BaseModel):
    """Base subject attributes."""

    name: str
    slug: str
    description: str | None = None
    display_order: int = 0
    is_active: bool = True


class SubjectRead(SubjectBase):
    """Subject read schema."""

    id: uuid.UUID
    exam_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChapterBase(BaseModel):
    """Base chapter attributes."""

    name: str
    slug: str
    description: str | None = None
    display_order: int = 0
    is_active: bool = True


class ChapterRead(ChapterBase):
    """Chapter read schema."""

    id: uuid.UUID
    subject_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class QuestionOptionBase(BaseModel):
    """Base question option attributes."""

    option_key: str
    option_text: str
    display_order: int = 1
    is_correct: bool = False


class QuestionOptionRead(QuestionOptionBase):
    """Question option read schema."""

    id: uuid.UUID
    question_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class QuestionBase(BaseModel):
    """Base question attributes."""

    question_text: str
    explanation: str | None = None
    difficulty: Difficulty
    is_pyq: bool = False
    pyq_year: int | None = None
    pyq_exam_name: str | None = None
    source: str | None = None
    is_active: bool = True


class QuestionRead(QuestionBase):
    """Question read schema."""

    id: uuid.UUID
    chapter_id: uuid.UUID
    options: list[QuestionOptionRead] = []
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TestAttemptBase(BaseModel):
    """Base test attempt attributes."""

    question_count: int
    duration_seconds: int
    difficulty: Difficulty | None = None
    is_pyq: bool = False


class TestAttemptRead(TestAttemptBase):
    """Test attempt read schema."""

    id: uuid.UUID
    user_id: uuid.UUID
    exam_id: uuid.UUID
    subject_id: uuid.UUID
    chapter_id: uuid.UUID | None = None
    status: TestAttemptStatus
    score: float | None = None
    correct_count: int
    wrong_count: int
    unanswered_count: int
    time_taken_seconds: int | None = None
    started_at: datetime
    submitted_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
