import json
from collections import Counter

import pytest
from sqlalchemy import func, select

from app.models import Chapter, Difficulty, Exam, Question, QuestionOption, Subject, Subcategory
from app.services.question_import_service import import_questions
from scripts.import_time_and_work_verified_batch import BATCH, load_batch, plan_missing


@pytest.fixture
def time_work_catalog(db_session):
    exam = Exam(name="SSC", slug="ssc", is_active=True)
    db_session.add(exam)
    db_session.flush()
    subject = Subject(exam_id=exam.id, name="Maths", slug="maths", is_active=True)
    db_session.add(subject)
    db_session.flush()
    category = Subcategory(subject_id=subject.id, name="Arithmetic Maths", slug="arithmetic-maths", is_active=True)
    db_session.add(category)
    db_session.flush()
    chapter = Chapter(subject_id=subject.id, subcategory_id=category.id, name="Time & Work", slug="time-and-work", is_active=True)
    db_session.add(chapter)
    db_session.commit()
    return chapter


def test_planner_targets_all_difficulties_and_preserves_existing_rows():
    rows = load_batch()
    assert len(rows) == 90
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    assert plan_missing(rows, []) == rows


def test_dry_run_import_and_replay_are_idempotent(db_session, time_work_catalog):
    data = BATCH.read_bytes()
    preview = import_questions(db_session, data, "application/json", BATCH.name, True)
    assert not preview.aborted and not preview.errors and preview.would_import == 90 and preview.duplicates == 0
    assert db_session.scalar(select(func.count(Question.id))) == 0
    imported = import_questions(db_session, data, "application/json", BATCH.name, False)
    assert imported.imported == 90 and imported.duplicates == 0 and not imported.errors
    rows = db_session.scalars(select(Question).where(Question.chapter_id == time_work_catalog.id)).all()
    assert Counter(row.difficulty.value for row in rows) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    assert all(row.is_active and not row.is_pyq for row in rows)
    assert plan_missing(load_batch(), rows) == []
    replay = import_questions(db_session, data, "application/json", BATCH.name, False)
    assert replay.imported == 0 and replay.duplicates == 90 and not replay.errors


def test_planner_preserves_matching_existing_question(db_session, time_work_catalog):
    row = load_batch()[0]
    options = [QuestionOption(option_key=key, option_text=row["options"][key], is_correct=key == row["correct_option"], display_order=index) for index, key in enumerate("ABCD", 1)]
    question = Question(chapter_id=time_work_catalog.id, question_text=row["question_text"], explanation=row["explanation"], difficulty=Difficulty(row["difficulty"]), is_pyq=False, is_active=True, source=row["source"], options=options)
    db_session.add(question)
    db_session.commit()
    selected = plan_missing(load_batch(), [question])
    assert len(selected) == 89
    assert row["question_text"] not in {item["question_text"] for item in selected}


def test_planner_rejects_conflicting_existing_exact_match(db_session, time_work_catalog):
    row = load_batch()[0]
    options = [QuestionOption(option_key=key, option_text=("wrong" if key == row["correct_option"] else row["options"][key]), is_correct=key == row["correct_option"], display_order=index) for index, key in enumerate("ABCD", 1)]
    question = Question(chapter_id=time_work_catalog.id, question_text=row["question_text"], explanation=row["explanation"], difficulty=Difficulty(row["difficulty"]), is_pyq=False, is_active=True, source=row["source"], options=options)
    db_session.add(question)
    db_session.commit()
    with pytest.raises(ValueError, match="conflicts with batch"):
        plan_missing(load_batch(), [question])
