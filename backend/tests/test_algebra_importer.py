"""Transactional planning, idempotency, and row-preservation checks for Algebra."""
from collections import Counter

import pytest
from sqlalchemy import func, select

from app.models import Chapter, Difficulty, Exam, Question, QuestionOption, Subject, Subcategory
from app.services.question_import_service import import_questions
from scripts.import_algebra_verified_batch import BATCH, load_batch, plan_missing


@pytest.fixture
def algebra_catalog(db_session):
    exam = Exam(name="SSC", slug="ssc", is_active=True)
    db_session.add(exam)
    db_session.flush()
    subject = Subject(exam_id=exam.id, name="Maths", slug="maths", is_active=True)
    db_session.add(subject)
    db_session.flush()
    category = Subcategory(subject_id=subject.id, name="Advanced Maths", slug="advanced-maths", is_active=True)
    db_session.add(category)
    db_session.flush()
    chapter = Chapter(subject_id=subject.id, subcategory_id=category.id, name="Algebra", slug="algebra", is_active=True)
    db_session.add(chapter)
    db_session.commit()
    return chapter


def test_planner_targets_30_per_level_without_touching_other_rows():
    rows = load_batch()
    assert len(rows) == 90
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    assert plan_missing(rows, []) == rows


def test_dry_run_import_replay_and_existing_row_preservation(db_session, algebra_catalog):
    data = BATCH.read_bytes()
    preview = import_questions(db_session, data, "application/json", BATCH.name, True)
    assert not preview.aborted and not preview.errors and preview.would_import == 90 and preview.duplicates == 0
    assert db_session.scalar(select(func.count(Question.id))) == 0

    result = import_questions(db_session, data, "application/json", BATCH.name, False)
    assert result.imported == 90 and result.duplicates == 0 and not result.errors
    rows = db_session.scalars(select(Question).where(Question.chapter_id == algebra_catalog.id)).all()
    assert Counter(question.difficulty.value for question in rows) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    assert all(question.is_active and not question.is_pyq for question in rows)
    assert plan_missing(load_batch(), rows) == []

    replay = import_questions(db_session, data, "application/json", BATCH.name, False)
    assert replay.imported == 0 and replay.duplicates == 90
    assert db_session.scalar(select(func.count(Question.id))) == 90


def test_existing_batch_match_is_preserved(db_session, algebra_catalog):
    row = load_batch()[0]
    options = [
        QuestionOption(option_key=key, option_text=row["options"][key], is_correct=key == row["correct_option"], display_order=index)
        for index, key in enumerate("ABCD", start=1)
    ]
    existing = Question(
        chapter_id=algebra_catalog.id,
        question_text=row["question_text"],
        explanation=row["explanation"],
        difficulty=Difficulty(row["difficulty"]),
        is_pyq=False,
        is_active=True,
        source=row["source"],
        options=options,
    )
    db_session.add(existing)
    db_session.commit()
    selected = plan_missing(load_batch(), [existing])
    assert len(selected) == 89
    assert row["question_text"] not in {candidate["question_text"] for candidate in selected}
