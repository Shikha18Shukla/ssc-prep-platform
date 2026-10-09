"""Schemas for the authenticated exam catalog and practice selection."""

from enum import Enum
from datetime import datetime
from typing import Literal
import uuid

from pydantic import BaseModel


class PracticeLevel(str, Enum):
    """Selectable practice modes; PYQ is independent of difficulty."""

    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"
    PYQ = "PYQ"


QuestionCount = Literal[10, 15, 20, 25]


class SubcategoryRead(BaseModel):
    id: uuid.UUID
    subject_id: uuid.UUID
    name: str
    slug: str
    description: str | None = None
    display_order: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ChapterAvailability(BaseModel):
    chapter_id: uuid.UUID
    level: PracticeLevel
    available_question_count: int
    allowed_question_counts: list[QuestionCount]
    requested_question_count: QuestionCount | None = None
    can_satisfy_request: bool | None = None
