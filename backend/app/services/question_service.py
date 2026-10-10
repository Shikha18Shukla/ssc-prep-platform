"""Authenticated question-bank management operations."""

import uuid
import unicodedata

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models import Difficulty, Question, QuestionOption
from app.schemas.questions import QuestionUpdate


def list_questions(
    db: Session,
    chapter_id: uuid.UUID | None,
    difficulty: Difficulty | None,
    is_pyq: bool | None,
    include_inactive: bool,
    offset: int,
    limit: int,
) -> tuple[int, list[Question]]:
    query = select(Question)
    count_query = select(func.count(Question.id))
    if chapter_id is not None:
        query = query.where(Question.chapter_id == chapter_id)
        count_query = count_query.where(Question.chapter_id == chapter_id)
    if difficulty is not None:
        query = query.where(Question.difficulty == difficulty)
        count_query = count_query.where(Question.difficulty == difficulty)
    if is_pyq is not None:
        query = query.where(Question.is_pyq.is_(is_pyq))
        count_query = count_query.where(Question.is_pyq.is_(is_pyq))
    if not include_inactive:
        query = query.where(Question.is_active.is_(True))
        count_query = count_query.where(Question.is_active.is_(True))
    total = db.scalar(count_query) or 0
    items = list(
        db.execute(
            query.options(selectinload(Question.options))
            .order_by(Question.created_at.desc(), Question.id)
            .offset(offset)
            .limit(limit)
        ).scalars().all()
    )
    return total, items


def get_question(db: Session, question_id: uuid.UUID) -> Question | None:
    return db.execute(
        select(Question)
        .options(selectinload(Question.options))
        .where(Question.id == question_id)
    ).scalar_one_or_none()


def update_question(db: Session, question: Question, values: QuestionUpdate) -> Question:
    cleaned_text = values.question_text.strip()
    normalized = " ".join(unicodedata.normalize("NFKC", cleaned_text).casefold().split())
    existing_texts = db.execute(
        select(Question.question_text).where(
            Question.chapter_id == question.chapter_id,
            Question.id != question.id,
        )
    ).scalars().all()
    if any(
        normalized == " ".join(unicodedata.normalize("NFKC", text).casefold().split())
        for text in existing_texts
    ):
        raise ValueError("Another question in this chapter already has the same normalized text")

    question.question_text = cleaned_text
    question.explanation = values.explanation.strip() if values.explanation else None
    question.difficulty = values.difficulty
    question.is_pyq = values.is_pyq
    question.pyq_year = values.pyq_year
    question.pyq_exam_name = values.pyq_exam_name.strip() if values.pyq_exam_name else None
    question.source = values.source.strip() if values.source else None
    by_key = {option.option_key: option for option in question.options}
    for display_order, option_data in enumerate(values.options, start=1):
        option = by_key[option_data.option_key]
        option.option_text = option_data.option_text.strip()
        option.is_correct = option_data.is_correct
        option.display_order = display_order
    db.commit()
    db.refresh(question)
    return question
