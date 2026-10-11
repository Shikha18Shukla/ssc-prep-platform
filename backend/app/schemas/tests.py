"""Schemas for the authenticated test-taking lifecycle."""

import uuid
from datetime import datetime

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.models.test_attempt import TestAttemptStatus


class TestCreate(BaseModel):
    exam_id: uuid.UUID
    subject_id: uuid.UUID
    subcategory_id: uuid.UUID | None = None
    test_type: Literal["CHAPTER_WISE", "MISCELLANEOUS"]
    chapter_id: uuid.UUID | None = None
    # PYQ is an independent selection mode, not a difficulty level.
    difficulty: str | None = None
    question_count: int = Field(ge=1, le=25)


class TestAvailabilityRead(BaseModel):
    available_question_count: int
    allowed_question_counts: list[int]
    can_satisfy_request: bool


class TestOption(BaseModel):
    option_key: str
    option_text: str

    model_config = ConfigDict(from_attributes=True)


class ActiveTestQuestion(BaseModel):
    test_question_id: uuid.UUID
    question_order: int
    question_text: str
    options: list[TestOption]
    selected_option: str | None = None


class ActiveTestRead(BaseModel):
    id: uuid.UUID
    exam_id: uuid.UUID
    subject_id: uuid.UUID
    chapter_id: uuid.UUID | None
    test_type: Literal["CHAPTER_WISE", "MISCELLANEOUS"]
    difficulty: str | None
    question_count: int
    duration_seconds: int
    started_at: datetime
    deadline_at: datetime
    status: TestAttemptStatus
    questions: list[ActiveTestQuestion]


class AnswerUpdate(BaseModel):
    selected_option: str = Field(pattern="^[A-D]$")


class TestSummary(BaseModel):
    id: uuid.UUID
    status: TestAttemptStatus
    question_count: int
    attempted_count: int
    unanswered_count: int
    correct_count: int | None
    wrong_count: int | None
    score: float | None
    scoring_pending: bool
    duration_seconds: int
    time_taken_seconds: int | None
    started_at: datetime
    submitted_at: datetime | None


class ReviewQuestion(BaseModel):
    question_order: int
    question_text: str
    options: list[TestOption]
    selected_option: str | None
    correct_option: str
    explanation: str | None
    is_correct: bool


class TestResultRead(TestSummary):
    review: list[ReviewQuestion]


class DashboardHistory(BaseModel):
    tests_attempted: int
    average_score: float | None
    best_score: float | None
    previous_tests: list[TestSummary]
