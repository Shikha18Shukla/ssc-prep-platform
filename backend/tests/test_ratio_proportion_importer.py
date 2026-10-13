"""Focused integration checks for the Ratio & Proportion importer."""
import json
from collections import Counter

import pytest
from sqlalchemy import event, func, select
from sqlalchemy.exc import IntegrityError

from app.models import Chapter, Exam, Question, QuestionOption, Subject, Subcategory
from app.services.question_import_service import import_questions
from scripts.import_ratio_proportion_verified_batch import BATCH, load_batch


@pytest.fixture
def ratio_catalog(db_session):
    exam = Exam(name="SSC", slug="ssc", is_active=True)
    db_session.add(exam)
    db_session.flush()
    subject = Subject(exam_id=exam.id, name="Maths", slug="maths", is_active=True)
    db_session.add(subject)
    db_session.flush()
    category = Subcategory(subject_id=subject.id, name="Arithmetic Maths", slug="arithmetic-maths", is_active=True)
    db_session.add(category)
    db_session.flush()
    chapter = Chapter(subject_id=subject.id, subcategory_id=category.id, name="Ratio & Proportion", slug="ratio-and-proportion", is_active=True)
    db_session.add(chapter)
    db_session.commit()
    return chapter


def test_combined_batch_schema_count_difficulty_and_ordinary_provenance():
    questions = load_batch()
    assert len(questions) == 90
    assert Counter(row["difficulty"] for row in questions) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    assert all(row["is_pyq"] is False and row["source"] == "Original SSC-style practice question" for row in questions)
    assert all(set(row["options"]) == {"A", "B", "C", "D"} for row in questions)


def test_importer_service_dry_run_commit_and_rerun_are_idempotent(db_session, ratio_catalog):
    data = BATCH.read_bytes()
    preview = import_questions(db_session, data, "application/json", BATCH.name, True)
    assert preview.aborted is False and preview.errors == []
    assert preview.would_import == 90 and preview.duplicates == 0
    assert db_session.scalar(select(func.count(Question.id))) == 0

    imported = import_questions(db_session, data, "application/json", BATCH.name, False)
    assert imported.imported == 90 and imported.errors == []
    rows = db_session.scalars(select(Question).where(Question.chapter_id == ratio_catalog.id)).all()
    assert Counter(row.difficulty.value for row in rows) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    assert all(row.is_active and not row.is_pyq for row in rows)

    rerun = import_questions(db_session, data, "application/json", BATCH.name, False)
    assert rerun.imported == 0 and rerun.duplicates == 90
    assert db_session.scalar(select(func.count(Question.id))) == 90


def test_unrecognized_integrity_failure_is_raised_and_transaction_rolls_back(db_session, ratio_catalog):
    record = load_batch()[0]
    bad_constraint = IntegrityError("simulated unrelated constraint", {}, RuntimeError("not duplicate"))

    def fail_flush(_session, _flush_context, _instances):
        raise bad_constraint

    event.listen(db_session, "before_flush", fail_flush)
    try:
        with pytest.raises(IntegrityError, match="simulated unrelated constraint"):
            import_questions(db_session, json.dumps({"questions": [record]}, ensure_ascii=False).encode(), "application/json", "test.json", False)
    finally:
        event.remove(db_session, "before_flush", fail_flush)
    assert db_session.scalar(select(func.count(Question.id))) == 0
    assert db_session.scalar(select(func.count(QuestionOption.id))) == 0
