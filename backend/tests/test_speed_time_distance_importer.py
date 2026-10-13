"""Focused integration tests for Speed, Time & Distance batch import behavior."""
import json
from collections import Counter

import pytest
from sqlalchemy import event, func, select
from sqlalchemy.exc import IntegrityError

from app.models import Chapter, Exam, Question, QuestionOption, Subject, Subcategory
from app.services.question_import_service import import_questions
from scripts.import_speed_time_distance_verified_batch import BATCH, load_batch, plan_missing


@pytest.fixture
def speed_distance_catalog(db_session):
    exam = Exam(name="SSC", slug="ssc", is_active=True)
    db_session.add(exam)
    db_session.flush()
    subject = Subject(exam_id=exam.id, name="Maths", slug="maths", is_active=True)
    db_session.add(subject)
    db_session.flush()
    category = Subcategory(subject_id=subject.id, name="Arithmetic Maths", slug="arithmetic-maths", is_active=True)
    db_session.add(category)
    db_session.flush()
    chapter = Chapter(
        subject_id=subject.id, subcategory_id=category.id,
        name="Speed Time & Distance", slug="speed-time-and-distance", is_active=True,
    )
    db_session.add(chapter)
    db_session.commit()
    return chapter


def test_importer_plans_exact_balanced_original_bank():
    records = load_batch()
    assert len(records) == 90
    assert Counter(row["difficulty"] for row in records) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    assert all(row["is_pyq"] is False and row["source"] == "Original SSC-style practice question" for row in records)
    assert plan_missing(records, []) == records


def test_import_service_dry_run_import_and_rerun_are_idempotent(db_session, speed_distance_catalog):
    data = BATCH.read_bytes()
    preview = import_questions(db_session, data, "application/json", BATCH.name, True)
    assert preview.aborted is False and preview.errors == []
    assert preview.would_import == 90 and preview.duplicates == 0
    assert db_session.scalar(select(func.count(Question.id))) == 0

    imported = import_questions(db_session, data, "application/json", BATCH.name, False)
    assert imported.imported == 90 and imported.errors == []
    rows = db_session.scalars(select(Question).where(Question.chapter_id == speed_distance_catalog.id)).all()
    assert Counter(row.difficulty.value for row in rows) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    assert all(row.is_active and not row.is_pyq for row in rows)
    assert plan_missing(load_batch(), rows) == []

    rerun = import_questions(db_session, data, "application/json", BATCH.name, False)
    assert rerun.imported == 0 and rerun.duplicates == 90
    assert db_session.scalar(select(func.count(Question.id))) == 90


def test_unrecognized_integrity_error_is_raised_and_rolls_back(db_session, speed_distance_catalog):
    record = load_batch()[0]
    failure = IntegrityError("simulated unrelated integrity constraint", {}, RuntimeError("not a duplicate"))

    def fail_flush(_session, _flush_context, _instances):
        raise failure

    event.listen(db_session, "before_flush", fail_flush)
    try:
        with pytest.raises(IntegrityError, match="simulated unrelated integrity constraint"):
            import_questions(
                db_session, json.dumps({"questions": [record]}).encode(),
                "application/json", "test.json", False,
            )
    finally:
        event.remove(db_session, "before_flush", fail_flush)
    assert db_session.scalar(select(func.count(Question.id))) == 0
    assert db_session.scalar(select(func.count(QuestionOption.id))) == 0
