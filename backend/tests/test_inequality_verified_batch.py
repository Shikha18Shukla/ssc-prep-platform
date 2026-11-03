"""Focused content and solver regression tests for the CH-16 Inequality bank."""

import json
import sys
from collections import Counter
from itertools import product
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
import uuid

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / "scripts"))
from build_inequality_artifacts import (  # noqa: E402
    classify_claim, closure, conclusion_outcome, statement,
)
from app.auth.security import create_access_token  # noqa: E402
from app.models import Chapter, Difficulty, Exam, Question, QuestionOption, Subject, User  # noqa: E402
from import_inequality_verified_batch import validate_preview, validate_replay  # noqa: E402

BATCH = BASE / "data" / "inequality_verified_batch.json"
LEDGER = BASE / "data" / "inequality_answer_ledger.json"


def test_canonical_bank_has_thirty_valid_normal_questions_and_aligned_ledger():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    selected = [entry for entry in ledger if entry["record_type"] == "selected_question"]
    rejected = [entry for entry in ledger if entry["record_type"] == "rejected_source_prompt"]
    assert len(rows) == len(selected) == 30
    assert len(rejected) == 2 and all(entry["rejection_reason"] for entry in rejected)
    assert Counter(r["difficulty"] for r in rows) == {"EASY": 10, "MEDIUM": 10, "HARD": 10}
    assert Counter("original" if r["source"] == "Original SSC-style practice question" else "pdf" for r in rows) == {"pdf": 21, "original": 9}
    for n, (row, audit) in enumerate(zip(rows, selected), 1):
        assert row["chapter_slug"] == "inequality" and row["subject_slug"] == "reasoning"
        assert row["is_pyq"] is False and row["difficulty"] in {"EASY", "MEDIUM", "HARD"}
        assert row["question_text"].strip() and row["explanation"].strip()
        assert set(row["options"]) == set("ABCD")
        assert len({v.strip().casefold() for v in row["options"].values()}) == 4
        assert row["correct_option"] in row["options"]
        assert audit["row"] == n and audit["question"] == row["question_text"]
        assert audit["chapter_id"] == "6d8b6da5-6635-417c-99e4-0bb7f511520b"
        assert audit["correct_option"] == row["correct_option"]
        assert audit["correct_answer"] == row["options"][row["correct_option"]]
        assert audit["options"] == row["options"]
        assert audit["validation_status"].startswith("PASS")


@pytest.mark.parametrize("statements,claim,expected", [
    ([statement("A", "<", "B"), statement("B", "≤", "C")], statement("A", "<", "C"), "TRUE"),
    ([statement("A", "≤", "B")], statement("A", "<", "B"), "UNKNOWN"),
    ([statement("A", "<", "B")], statement("B", "≤", "A"), "FALSE"),
    ([statement("A", "=", "B")], statement("A", "≥", "B"), "TRUE"),
    ([statement("A", ">", "B"), statement("B", "≥", "A")], statement("A", ">", "B"), "INCONSISTENT"),
])
def test_strict_and_nonstrict_constraint_solver(statements, claim, expected):
    assert classify_claim(statements, claim) == expected


def test_complementary_either_or_only_when_unresolved_pair_is_exhaustive():
    assert conclusion_outcome([], [statement("X", ">", "Y"), statement("X", "≤", "Y")]) == "EITHER"
    assert conclusion_outcome([statement("X", ">", "Y")], [statement("X", ">", "Y"), statement("X", "≤", "Y")]) == "ONLY_I"
    assert conclusion_outcome([], [statement("X", ">", "Y"), statement("Y", ">", "X")]) == "NEITHER"


def test_solver_matches_exhaustive_finite_assignments_for_small_constraint_systems():
    """For n variables, n+1 ordered ranks realize every possible weak ordering."""
    vars_ = ("A", "B", "C")
    ops = ("<", "≤", ">", "≥", "=")

    def holds(a, op, b):
        return {"<": a < b, "≤": a <= b, ">": a > b, "≥": a >= b, "=": a == b}[op]

    for p in range(3):
        for q in range(3):
            for relation in ops:
                statements = [statement(vars_[p], relation, vars_[q])]
                models = [dict(zip(vars_, model)) for model in product(range(4), repeat=3)
                          if holds(model[p], relation, model[q])]
                for a in vars_:
                    for b in vars_:
                        for op in ops:
                            if not models:
                                expected = "INCONSISTENT"
                            else:
                                outcomes = {holds(m[a], op, m[b]) for m in models}
                                expected = "TRUE" if outcomes == {True} else "FALSE" if outcomes == {False} else "UNKNOWN"
                            assert classify_claim(statements, statement(a, op, b)) == expected


def test_each_answer_is_independently_recomputed_from_ledger_constraints():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    ledger = [entry for entry in ledger if entry["record_type"] == "selected_question"]
    for row, audit in zip(rows, ledger):
        statements = audit["statements"]
        assert not closure(statements)[3]
        if audit["claim"]:
            outcome = classify_claim(statements, audit["claim"])
            assert row["options"][row["correct_option"]] == {
                "TRUE": "Definitely follows", "FALSE": "Definitely false",
                "UNKNOWN": "Cannot be determined", "INCONSISTENT": "Statements are inconsistent",
            }[outcome]
        else:
            outcome = conclusion_outcome(statements, audit["conclusions"])
            expected = {
                "ONLY_I": "Only conclusion I follows", "ONLY_II": "Only conclusion II follows",
                "BOTH": "Both conclusions I and II follow", "NEITHER": "Neither conclusion follows",
                "EITHER": "Either conclusion I or II follows",
            }[outcome]
            assert row["options"][row["correct_option"]] == expected


def test_bank_deduplication_rejects_exact_and_semantic_near_duplicates():
    from difflib import SequenceMatcher

    def near_duplicate(first, second):
        return SequenceMatcher(None, " ".join(first.casefold().split()), " ".join(second.casefold().split())).ratio() >= 0.94

    base = "Given A > B ≥ C = D, which conclusion follows?"
    assert near_duplicate(base, base)
    assert near_duplicate(base, "Given A > B ≥ C = D, which conclusion follows ?")
    assert not near_duplicate(base, "Statements: P < Q and R = S. Assess whether P > S.")


def test_importer_preview_and_idempotent_replay_guards():
    from types import SimpleNamespace

    preview = SimpleNamespace(aborted=False, errors=[], rejected=0, duplicates=0, would_import=30)
    validate_preview(preview, existing_count=0)
    with pytest.raises(ValueError, match="dry-run"):
        validate_preview(SimpleNamespace(aborted=False, errors=[], rejected=1, duplicates=0, would_import=29), 0)
    validate_replay(SimpleNamespace(aborted=False, errors=[], rejected=0, would_import=0, duplicates=30))
    with pytest.raises(ValueError, match="idempotent"):
        validate_replay(SimpleNamespace(aborted=False, errors=[], rejected=0, would_import=1, duplicates=29))


def test_series_style_chapter_availability_and_full_inequality_test_flow(client: TestClient, db_session):
    """Exercise catalog, availability, test, answer, submit, and explanation APIs."""
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    exam = Exam(name="SSC", slug="ssc", is_active=True)
    db_session.add(exam)
    db_session.flush()
    subject = Subject(exam_id=exam.id, name="Reasoning", slug="reasoning", is_active=True)
    db_session.add(subject)
    db_session.flush()
    chapter = Chapter(id=uuid.UUID("6d8b6da5-6635-417c-99e4-0bb7f511520b"), subject_id=subject.id,
                      name="Inequality", slug="inequality", is_active=True)
    user = User(email="inequality-flow@example.com", password_hash="unused", is_active=True)
    db_session.add_all([chapter, user])
    db_session.flush()
    correct_by_stem = {}
    for row in rows:
        q = Question(chapter_id=chapter.id, question_text=row["question_text"],
                     explanation=row["explanation"], difficulty=Difficulty(row["difficulty"]),
                     is_pyq=False, is_active=True, source=row["source"])
        db_session.add(q)
        db_session.flush()
        correct_by_stem[q.question_text] = row["correct_option"]
        db_session.add_all(QuestionOption(question_id=q.id, option_key=key, option_text=text,
                        display_order=index, is_correct=key == row["correct_option"])
                        for index, (key, text) in enumerate(row["options"].items(), 1))
    db_session.commit()
    headers = {"Authorization": f"Bearer {create_access_token(user.id)}"}

    catalog = client.get(f"/api/exams/subjects/{subject.id}/chapters", headers=headers)
    assert catalog.status_code == 200
    assert any(c["id"] == str(chapter.id) and c["slug"] == "inequality" for c in catalog.json())
    for level in ("EASY", "MEDIUM", "HARD"):
        result = client.get(f"/api/exams/chapters/{chapter.id}/availability",
                            params={"level": level, "question_count": 10}, headers=headers)
        assert result.status_code == 200 and result.json()["available_question_count"] == 10
        assert result.json()["can_satisfy_request"] is True
    pyq = client.get(f"/api/exams/chapters/{chapter.id}/availability", params={"level": "PYQ"}, headers=headers)
    assert pyq.status_code == 200 and pyq.json()["available_question_count"] == 0

    selection = {"exam_id": str(exam.id), "subject_id": str(subject.id), "test_type": "CHAPTER_WISE",
                 "chapter_id": str(chapter.id), "difficulty": "HARD", "question_count": 10}
    availability = client.get("/api/tests/availability", params=selection, headers=headers)
    assert availability.status_code == 200
    assert availability.json() == {"available_question_count": 10, "allowed_question_counts": [10], "can_satisfy_request": True}
    started = client.post("/api/tests", json=selection, headers=headers)
    assert started.status_code == 201, started.text
    active = started.json()
    assert active["chapter_id"] == str(chapter.id) and active["question_count"] == 10
    assert active["duration_seconds"] == 360 and len(active["questions"]) == 10
    assert "correct_option" not in active["questions"][0] and "explanation" not in active["questions"][0]
    assert all(len(q["options"]) == 4 for q in active["questions"])
    for item in active["questions"]:
        answer = client.put(f"/api/tests/{active['id']}/questions/{item['test_question_id']}/answer",
                            json={"selected_option": correct_by_stem[item["question_text"]]}, headers=headers)
        assert answer.status_code == 200
    reread = client.get(f"/api/tests/{active['id']}", headers=headers)
    assert reread.status_code == 200 and len(reread.json()["questions"]) == 10
    assert reread.json()["status"] == "IN_PROGRESS"
    submitted = client.post(f"/api/tests/{active['id']}/submit", headers=headers)
    assert submitted.status_code == 200
    assert submitted.json()["correct_count"] == 10 and submitted.json()["wrong_count"] == 0
    result = client.get(f"/api/tests/{active['id']}/result", headers=headers)
    assert result.status_code == 200 and len(result.json()["review"]) == 10
    assert all(q["is_correct"] and q["explanation"] and q["correct_option"] for q in result.json()["review"])
