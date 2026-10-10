"""Schemas for protected question bank management endpoints."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.models.question import Difficulty


class QuestionOptionInput(BaseModel):
    option_key: str = Field(pattern="^[A-D]$")
    option_text: str = Field(min_length=1)
    is_correct: bool = False
    display_order: int = Field(default=1, ge=1, le=4)


class QuestionUpdate(BaseModel):
    question_text: str = Field(min_length=1)
    explanation: str | None = None
    difficulty: Difficulty
    is_pyq: bool = False
    pyq_year: int | None = Field(default=None, ge=1950, le=2100)
    pyq_exam_name: str | None = Field(default=None, max_length=100)
    source: str | None = Field(default=None, max_length=255)
    options: list[QuestionOptionInput] = Field(min_length=4, max_length=4)

    @field_validator("pyq_exam_name", mode="before")
    @classmethod
    def normalize_pyq_exam_name(cls, value):
        """Normalize a missing or whitespace-only exam name to NULL."""
        if isinstance(value, str):
            return value.strip() or None
        return value

    @model_validator(mode="after")
    def validate_options_and_pyq(self):
        keys = [option.option_key for option in self.options]
        if set(keys) != {"A", "B", "C", "D"}:
            raise ValueError("Options must have exactly one each of A, B, C, and D")
        if sum(option.is_correct for option in self.options) != 1:
            raise ValueError("Exactly one option must be correct")
        if any(not option.option_text.strip() for option in self.options):
            raise ValueError("Option text cannot be blank")
        if self.is_pyq and self.pyq_year is None:
            raise ValueError("PYQs require pyq_year")
        if not self.is_pyq and (self.pyq_year is not None or self.pyq_exam_name is not None):
            raise ValueError("Non-PYQs must not include PYQ metadata")
        return self


class QuestionOptionManagementRead(BaseModel):
    id: uuid.UUID
    option_key: str
    option_text: str
    is_correct: bool
    display_order: int
    model_config = ConfigDict(from_attributes=True)


class QuestionManagementRead(BaseModel):
    id: uuid.UUID
    chapter_id: uuid.UUID
    question_text: str
    explanation: str | None
    difficulty: Difficulty
    is_pyq: bool
    pyq_year: int | None
    pyq_exam_name: str | None
    source: str | None
    is_active: bool
    options: list[QuestionOptionManagementRead]
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class QuestionStatusUpdate(BaseModel):
    is_active: bool


class ImportIssue(BaseModel):
    row: int
    field: str | None = None
    message: str


class QuestionImportSummary(BaseModel):
    total_records: int
    imported: int
    rejected: int
    duplicates: int
    dry_run: bool
    would_import: int
    aborted: bool
    errors: list[ImportIssue]
    duplicate_rows: list[int]


class QuestionListResponse(BaseModel):
    total: int
    offset: int
    limit: int
    items: list[QuestionManagementRead]
