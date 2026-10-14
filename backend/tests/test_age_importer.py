"""Focused database-service tests for the reviewed Age batch."""
import json
from collections import Counter

import pytest
from sqlalchemy import event, func, select
from sqlalchemy.exc import IntegrityError

from app.models import Chapter, Exam, Question, QuestionOption, Subject, Subcategory
from app.services.question_import_service import import_questions
from scripts.import_age_verified_batch import BATCH, load_batch, plan_missing


@pytest.fixture
def age_catalog(db_session):
    exam = Exam(name="SSC", slug="ssc", is_active=True)
    db_session.add(exam)
    db_session.flush()
    subject = Subject(exam_id=exam.id, name="Maths", slug="maths", is_active=True)
    db_session.add(subject)
    db_session.flush()
    category = Subcategory(subject_id=subject.id, name="Arithmetic Maths", slug="arithmetic-maths", is_active=True)
    db_session.add(category)
    db_session.flush()
    chapter = Chapter(subject_id=subject.id, subcategory_id=category.id, name="Age", slug="age", is_active=True)
    db_session.add(chapter)
    db_session.commit()
    return chapter


def test_plan_respects_targets_and_selects_exact_batch():
    records = load_batch()
    assert len(records) == 90
    assert Counter(row["difficulty"] for row in records) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    assert plan_missing(records, []) == records


def test_service_dry_run_import_and_rerun_are_idempotent(db_session, age_catalog):
    data = BATCH.read_bytes()
    preview = import_questions(db_session, data, "application/json", BATCH.name, True)
    assert preview.aborted is False and preview.errors == []
    assert preview.would_import == 90 and preview.duplicates == 0
    assert db_session.scalar(select(func.count(Question.id))) == 0

    imported = import_questions(db_session, data, "application/json", BATCH.name, False)
    assert imported.imported == 90 and imported.errors == []
    rows = db_session.scalars(select(Question).where(Question.chapter_id == age_catalog.id)).all()
    assert Counter(row.difficulty.value for row in rows) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    assert all(row.is_active and not row.is_pyq for row in rows)
    assert plan_missing(load_batch(), rows) == []

    rerun = import_questions(db_session, data, "application/json", BATCH.name, False)
    assert rerun.imported == 0 and rerun.duplicates == 90
    assert db_session.scalar(select(func.count(Question.id))) == 90


def test_unrecognized_integrity_failure_is_raised_and_rolled_back(db_session, age_catalog):
    record = load_batch()[0]
    failure = IntegrityError("simulated unrelated constraint", {}, RuntimeError("not duplicate"))

    def fail_flush(_session, _flush_context, _instances):
        raise failure

    event.listen(db_session, "before_flush", fail_flush)
    try:
        with pytest.raises(IntegrityError, match="simulated unrelated constraint"):
            import_questions(db_session, json.dumps({"questions": [record]}).encode(), "application/json", "test.json", False)
    finally:
        event.remove(db_session, "before_flush", fail_flush)
    assert db_session.scalar(select(func.count(Question.id))) == 0
    assert db_session.scalar(select(func.count(QuestionOption.id))) == 0
