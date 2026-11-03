"""CH-19 source, answer, schema, determinism, conflict, and import checks."""
import hashlib
import json
import sys
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path
from types import SimpleNamespace

import pytest
from sqlalchemy import func, select

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
from app.auth.security import create_access_token
from app.models import Chapter, Exam, Question, Subject, User
from app.services.question_import_service import import_questions
from scripts import build_insert_missing_number_artifacts as builder
from scripts.import_insert_missing_number_verified_batch import (
    BATCH, LEDGER, ORIGINAL, duplicate_scan, load_artifacts, verify_existing,
)

LEDGER_PATH = LEDGER
SOURCE_REVIEW = BASE / "data" / "insert_missing_number_source_review.json"


@pytest.fixture
def insert_missing_number_catalog(db_session):
    exam = Exam(name="SSC", slug="ssc", is_active=True)
    db_session.add(exam)
    db_session.flush()
    subject = Subject(exam_id=exam.id, name="Reasoning", slug="reasoning", is_active=True)
    db_session.add(subject)
    db_session.flush()
    chapter = Chapter(subject_id=subject.id, subcategory_id=None, name="Insert the Missing Number", slug="insert-the-missing-number", is_active=True)
    db_session.add(chapter)
    db_session.commit()
    return chapter


def records():
    return json.loads(BATCH.read_text(encoding="utf-8"))["questions"], json.loads(LEDGER_PATH.read_text(encoding="utf-8"))


def test_batch_metadata_options_ledger_distribution_and_original_provenance():
    rows, ledger = records()
    assert len(rows) == len(ledger) == 30
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 10, "MEDIUM": 10, "HARD": 10}
    assert Counter(row["correct_option"] for row in rows) == {"A": 7, "B": 8, "C": 7, "D": 8}
    assert Counter("original" if row["source"] == ORIGINAL else "source" for row in rows) == {"source": 14, "original": 16}
    for index, (row, audit) in enumerate(zip(rows, ledger), 1):
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == ("reasoning", None, "insert-the-missing-number")
        assert row["is_pyq"] is False and row["pyq_year"] is None and row["pyq_exam_name"] is None
        assert row["question_text"].strip() and row["explanation"].strip()
        assert row["difficulty"] in {"EASY", "MEDIUM", "HARD"}
        assert set(row["options"]) == set("ABCD")
        assert len({value.casefold().strip() for value in row["options"].values()}) == 4
        assert row["correct_option"] in row["options"]
        assert row["options"][row["correct_option"]] == audit["expected_answer"]
        assert audit["id"] == f"imn-{index:03d}" and audit["row"] == index
        assert audit["options"] == row["options"] and audit["correct_option"] == row["correct_option"]
        assert audit["difficulty"] == row["difficulty"] and audit["source"] == row["source"]
        assert audit["verification_status"] == "independently_verified" and audit["independent_reasoning"]
        assert row["source"] == ORIGINAL or "page " in row["source"] and "exam/year not stated" in row["source"]


def test_independent_answer_checkpoints_and_explanations():
    rows, ledger = records()
    # Independently re-solved checkpoints cover each distinct arithmetic family.
    expected = {
        "imn-001": "26", "imn-002": "120", "imn-003": "32", "imn-004": "35", "imn-005": "16",
        "imn-006": "11", "imn-007": "19", "imn-008": "26", "imn-009": "54", "imn-010": "120",
        "imn-011": "622", "imn-012": "30", "imn-013": "129", "imn-014": "88", "imn-015": "48",
        "imn-016": "41", "imn-017": "120", "imn-018": "6", "imn-019": "43", "imn-020": "48",
        "imn-021": "165", "imn-022": "36", "imn-023": "2744", "imn-024": "32", "imn-025": "11",
        "imn-026": "53", "imn-027": "119", "imn-028": "244", "imn-029": "92", "imn-030": "600",
    }
    assert len(rows) == 30
    assert {entry["id"]: entry["expected_answer"] for entry in ledger} == expected
    for row, audit in zip(rows, ledger):
        assert row["explanation"] == audit["independent_reasoning"]
        assert row["options"][row["correct_option"]] == expected[audit["id"]]
        assert len(set(row["options"].values())) == 4


def test_page_by_page_source_review_and_duplicate_screen():
    rows, _ = records()
    review = json.loads(SOURCE_REVIEW.read_text(encoding="utf-8"))
    assert review["pages_reviewed"] == list(range(1, 28))
    assert [page["page"] for page in review["page_review"]] == list(range(1, 28))
    assert len({entry["pattern"] for entry in json.loads(LEDGER_PATH.read_text(encoding="utf-8"))}) == 30
    stems = [" ".join(row["question_text"].casefold().split()) for row in rows]
    assert len(stems) == len(set(stems))
    for i, stem in enumerate(stems):
        assert all(SequenceMatcher(None, stem, other).ratio() < 0.92 for other in stems[:i])
    duplicate_scan(rows, [SimpleNamespace(id="no-collision", question_text="An unrelated reasoning question.")])
    with pytest.raises(ValueError, match="Duplicate scan conflict"):
        duplicate_scan(rows, [SimpleNamespace(id="dup", question_text=rows[0]["question_text"])])


def test_builder_is_deterministic():
    builder.build()
    before = [hashlib.sha256(path.read_bytes()).hexdigest() for path in (BATCH, LEDGER_PATH, SOURCE_REVIEW)]
    builder.build()
    after = [hashlib.sha256(path.read_bytes()).hexdigest() for path in (BATCH, LEDGER_PATH, SOURCE_REVIEW)]
    assert before == after


def test_guarded_conflict_detection_rejects_existing_record_mismatch():
    rows = load_artifacts()
    row = rows[0]
    existing = SimpleNamespace(
        question_text=row["question_text"], explanation="different explanation", difficulty=SimpleNamespace(value=row["difficulty"]),
        is_pyq=False, is_active=True, source=row["source"],
        options=[SimpleNamespace(option_key=k, option_text=v, is_correct=k == row["correct_option"]) for k, v in row["options"].items()],
    )
    with pytest.raises(ValueError, match="conflicts with canonical"):
        verify_existing(rows, [existing])


def test_import_dry_run_commit_replay_and_conflict_rollback(db_session, insert_missing_number_catalog):
    rows = load_artifacts()
    payload = BATCH.read_bytes()
    preview = import_questions(db_session, payload, "application/json", BATCH.name, True)
    assert not preview.aborted and not preview.errors and preview.would_import == 30 and preview.duplicates == 0
    assert db_session.scalar(select(func.count(Question.id))) == 0
    imported = import_questions(db_session, payload, "application/json", BATCH.name, False)
    assert imported.imported == 30 and imported.duplicates == 0 and not imported.errors
    replay = import_questions(db_session, payload, "application/json", BATCH.name, True)
    assert replay.would_import == 0 and replay.duplicates == 30 and not replay.aborted
    assert db_session.scalar(select(func.count(Question.id))) == 30
    existing = db_session.scalars(select(Question).where(Question.chapter_id == insert_missing_number_catalog.id)).first()
    existing.explanation = "conflicting value"
    db_session.commit()
    with pytest.raises(ValueError, match="conflicts with canonical"):
        verify_existing(rows, [existing])
    assert db_session.scalar(select(func.count(Question.id))) == 30


def test_authenticated_catalog_availability_and_exam_session_flow(client, db_session, insert_missing_number_catalog):
    rows = load_artifacts()
    import_questions(db_session, BATCH.read_bytes(), "application/json", BATCH.name, False)
    user = User(email="ch19-test-taker@example.com", password_hash="unused", is_active=True)
    db_session.add(user)
    db_session.commit()
    headers = {"Authorization": f"Bearer {create_access_token(user.id)}"}
    exam = db_session.scalar(select(Exam).where(Exam.slug == "ssc"))
    subject = db_session.scalar(select(Subject).where(Subject.slug == "reasoning"))

    subjects = client.get(f"/api/exams/{exam.id}/subjects", headers=headers)
    assert subjects.status_code == 200
    assert any(item["id"] == str(subject.id) and item["slug"] == "reasoning" for item in subjects.json())
    chapters = client.get(f"/api/exams/subjects/{subject.id}/chapters", headers=headers)
    assert chapters.status_code == 200
    assert any(item["id"] == str(insert_missing_number_catalog.id) and item["slug"] == "insert-the-missing-number" for item in chapters.json())

    for level in ("EASY", "MEDIUM", "HARD"):
        availability = client.get(f"/api/exams/chapters/{insert_missing_number_catalog.id}/availability", params={"level": level, "question_count": 10}, headers=headers)
        assert availability.status_code == 200
        assert availability.json()["available_question_count"] == 10
        assert availability.json()["can_satisfy_request"] is True
        payload = {"exam_id": str(exam.id), "subject_id": str(subject.id), "chapter_id": str(insert_missing_number_catalog.id), "test_type": "CHAPTER_WISE", "difficulty": level, "question_count": 10}
        started = client.post("/api/tests", json=payload, headers=headers)
        assert started.status_code == 201, started.text
        active = started.json()
        assert len(active["questions"]) == 10
        allowed_stems = {row["question_text"] for row in rows if row["difficulty"] == level}
        assert {question["question_text"] for question in active["questions"]} <= allowed_stems
        assert all(len(question["options"]) == 4 for question in active["questions"])
        assert active["duration_seconds"] == 360
        assert client.post(f"/api/tests/{active['id']}/submit", headers=headers).status_code == 200

    pyq = client.get(f"/api/exams/chapters/{insert_missing_number_catalog.id}/availability", params={"level": "PYQ", "question_count": 10}, headers=headers)
    assert pyq.status_code == 200 and pyq.json()["available_question_count"] == 0
    assert pyq.json()["allowed_question_counts"] == [] and pyq.json()["can_satisfy_request"] is False

    mixed_params = {"exam_id": str(exam.id), "subject_id": str(subject.id), "chapter_id": str(insert_missing_number_catalog.id), "test_type": "CHAPTER_WISE", "question_count": 10}
    mixed_availability = client.get("/api/tests/availability", params=mixed_params, headers=headers)
    assert mixed_availability.status_code == 200 and mixed_availability.json()["available_question_count"] == 30
    assert mixed_availability.json()["allowed_question_counts"] == [10, 15, 20, 25]
    mixed = client.post("/api/tests", json={**mixed_params, "difficulty": None}, headers=headers)
    assert mixed.status_code == 201
    assert all(question["question_text"] in {row["question_text"] for row in rows} for question in mixed.json()["questions"])
    assert client.post(f"/api/tests/{mixed.json()['id']}/submit", headers=headers).status_code == 200

    hard_payload = {"exam_id": str(exam.id), "subject_id": str(subject.id), "chapter_id": str(insert_missing_number_catalog.id), "test_type": "CHAPTER_WISE", "difficulty": "HARD", "question_count": 10}
    attempt_response = client.post("/api/tests", json=hard_payload, headers=headers)
    assert attempt_response.status_code == 201
    active = attempt_response.json()
    first, second = active["questions"][:2]
    first_row = next(row for row in rows if row["question_text"] == first["question_text"])
    second_row = next(row for row in rows if row["question_text"] == second["question_text"])
    correct_key = first_row["correct_option"]
    wrong_key = next(key for key in "ABCD" if key != second_row["correct_option"])
    for item, key in ((first, correct_key), (second, wrong_key)):
        saved = client.put(f"/api/tests/{active['id']}/questions/{item['test_question_id']}/answer", json={"selected_option": key}, headers=headers)
        assert saved.status_code == 200
    reload = client.get(f"/api/tests/{active['id']}", headers=headers)
    assert reload.status_code == 200
    assert [item["selected_option"] for item in reload.json()["questions"][:2]] == [correct_key, wrong_key]
    submitted = client.post(f"/api/tests/{active['id']}/submit", headers=headers)
    assert submitted.status_code == 200
    assert submitted.json()["correct_count"] == 1 and submitted.json()["wrong_count"] == 1
    assert submitted.json()["unanswered_count"] == 8 and submitted.json()["score"] == 1.5
    result = client.get(f"/api/tests/{active['id']}/result", headers=headers)
    assert result.status_code == 200 and len(result.json()["review"]) == 10
    for review in result.json()["review"]:
        expected = next(row for row in rows if row["question_text"] == review["question_text"])
        assert review["correct_option"] == expected["correct_option"]
        assert review["explanation"] == expected["explanation"]
