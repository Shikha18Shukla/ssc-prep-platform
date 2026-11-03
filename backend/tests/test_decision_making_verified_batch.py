"""CH-20 source, evaluator, importer, duplicate, and authenticated API regressions."""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

import pytest
from sqlalchemy import func, select

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
from app.auth.security import create_access_token
from app.models import Chapter, Difficulty, Exam, Question, QuestionOption, Subject, User
from app.services.question_import_service import import_questions
from scripts import build_decision_making_artifacts as builder
from scripts.import_decision_making_verified_batch import BATCH, LEDGER, duplicate_scan, load_artifacts, verify_existing

DATA = BASE / "data"
SOURCE_REVIEW = DATA / "decision_making_source_review.json"


@pytest.fixture
def decision_making_catalog(db_session):
    exam = Exam(name="SSC", slug="ssc", is_active=True)
    db_session.add(exam)
    db_session.flush()
    subject = Subject(exam_id=exam.id, name="Reasoning", slug="reasoning", is_active=True)
    db_session.add(subject)
    db_session.flush()
    chapter = Chapter(subject_id=subject.id, subcategory_id=None, name="Decision Making", slug="decision-making", is_active=True)
    other = Chapter(subject_id=subject.id, subcategory_id=None, name="Existing Chapter", slug="existing-chapter", is_active=True)
    db_session.add_all([chapter, other])
    db_session.flush()
    preserved = Question(chapter_id=other.id, question_text="Unrelated pre-existing chapter record", explanation="Preserve this question.", difficulty=Difficulty.EASY, is_pyq=False, is_active=True, source="Existing source.", options=[
        QuestionOption(option_key="A", option_text="Correct", display_order=0, is_correct=True),
        QuestionOption(option_key="B", option_text="Wrong B", display_order=1, is_correct=False),
        QuestionOption(option_key="C", option_text="Wrong C", display_order=2, is_correct=False),
        QuestionOption(option_key="D", option_text="Wrong D", display_order=3, is_correct=False),
    ])
    db_session.add(preserved)
    db_session.commit()
    return exam, subject, chapter, other, preserved


def _records():
    return json.loads(BATCH.read_text(encoding="utf-8"))["questions"], json.loads(LEDGER.read_text(encoding="utf-8"))


def test_batch_schema_source_provenance_and_balanced_answer_positions():
    rows = load_artifacts()
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    assert len(rows) == len(ledger) == 34
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 11, "MEDIUM": 12, "HARD": 11}
    assert Counter(item["category"] for item in ledger) == {"ELIGIBILITY": 18, "SITUATIONAL": 16}
    assert Counter(row["correct_option"] for row in rows) == {"A": 9, "B": 9, "C": 8, "D": 8}
    assert Counter(item["original_question"] for item in ledger) == {False: 26, True: 8}
    assert [item["id"] for item in ledger] == [f"dm-{number:03d}" for number in range(1, 35)]
    for row, audit in zip(rows, ledger):
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == ("reasoning", None, "decision-making")
        assert row["is_pyq"] is False and row["pyq_year"] is None and row["pyq_exam_name"] is None
        assert row["question_text"].strip() and row["explanation"].strip()
        assert len({option.strip().casefold() for option in row["options"].values()}) == 4
        assert row["options"][row["correct_option"]] == audit["correct_answer"]
        assert audit["question"] == row["question_text"] and audit["difficulty"] == row["difficulty"]
        assert audit["independent_reasoning"] == row["explanation"] and audit["verification_status"] == "independently_verified"
        assert row["source"] == builder.ORIGINAL if audit["original_question"] else "page " in row["source"] and "exam/year not stated" in row["source"]


def test_all_eligibility_cases_match_independent_rule_evaluator():
    rows, ledger = _records()
    eligibility = [item for item in ledger if item["category"] == "ELIGIBILITY"]
    assert len(eligibility) == 18
    for row, audit in zip(rows, ledger):
        if audit["category"] != "ELIGIBILITY":
            continue
        case = audit["eligibility"]
        result = builder.evaluate_candidate(case["candidate"], case["criteria"], case["referrals"])
        assert result == case["evaluator_result"]
        assert result["outcome"] == case["expected_outcome"]
        assert row["options"][row["correct_option"]] == audit["correct_answer"]


def test_eligibility_age_marks_experience_and_referral_boundaries():
    criteria = [
        {"name": "age", "field": "age_years", "op": "between_inclusive", "minimum": 24, "maximum": 30},
        {"name": "marks", "field": "marks", "op": "gte", "value": 50},
        {"name": "experience", "field": "experience_months", "op": "gte", "value": 6},
    ]
    exact_min_age = {"date_of_birth": "2002-10-01", "as_of": "2026-10-01", "marks": 50, "experience_start": "2026-04-01", "experience_as_of": "2026-10-01"}
    assert builder.evaluate_candidate(exact_min_age, criteria)["outcome"] == "SELECT"
    exact_max_age = {**exact_min_age, "date_of_birth": "1996-10-01"}
    assert builder.evaluate_candidate(exact_max_age, criteria)["outcome"] == "SELECT"
    one_day_under_min = {**exact_min_age, "date_of_birth": "2002-10-02"}
    assert builder.evaluate_candidate(one_day_under_min, criteria)["outcome"] == "REJECT"
    one_day_over_max = {**exact_min_age, "date_of_birth": "1995-09-30"}
    assert builder.evaluate_candidate(one_day_over_max, criteria)["outcome"] == "REJECT"
    one_day_short_experience = {**exact_min_age, "experience_start": "2026-04-02"}
    assert builder.evaluate_candidate(one_day_short_experience, criteria)["outcome"] == "REJECT"
    exact_min_experience = {**exact_min_age, "experience_start": "2026-04-01"}
    assert builder.evaluate_candidate(exact_min_experience, criteria)["outcome"] == "SELECT"
    exact_min_marks = {**exact_min_age, "marks": 50}
    assert builder.evaluate_candidate(exact_min_marks, criteria)["outcome"] == "SELECT"
    below_marks = {**exact_min_age, "marks": 49.99}
    assert builder.evaluate_candidate(below_marks, criteria)["outcome"] == "REJECT"


def test_referral_requires_exactly_the_exceptional_failure_and_all_safeguards():
    criteria = [
        {"name": "degree", "field": "degree", "op": "eq", "value": True},
        {"name": "experience", "field": "experience_months", "op": "gte", "value": 12},
    ]
    referral = [{"failed_criteria": ["experience"], "authority": "Principal", "when": [{"field": "diploma", "op": "eq", "value": True}]}]
    facts = {"degree": True, "experience_months": 0, "diploma": True}
    assert builder.evaluate_candidate(facts, criteria, referral)["authority"] == "Principal"
    assert builder.evaluate_candidate({**facts, "diploma": False}, criteria, referral)["outcome"] == "REJECT"
    assert builder.evaluate_candidate({**facts, "degree": False}, criteria, referral)["outcome"] == "REJECT"
    assert builder.evaluate_candidate({**facts, "degree": None}, criteria, referral)["outcome"] == "INSUFFICIENT"
    assert builder.evaluate_candidate({"degree": True, "experience_months": 12, "diploma": False}, criteria, referral)["outcome"] == "SELECT"


def test_source_review_covers_all_46_pages_and_rejected_items():
    review = json.loads(SOURCE_REVIEW.read_text(encoding="utf-8"))
    assert review["pages_reviewed"] == 46
    pages = review["page_reviews"]
    assert len(pages) == 46
    assert Counter(page["status"] for page in pages) == {"accepted_question": 26, "accepted_context": 5, "rejected": 4, "reference": 11}
    assert review["accepted_source_question_count"] == 26
    assert review["original_question_count"] == 8
    assert review["rejected_source_question_count"] == 4


def test_duplicate_scan_rejects_exact_and_near_match_but_accepts_distinct_item():
    rows = load_artifacts()
    duplicate_scan(rows, [SimpleNamespace(id="other", question_text="A wholly unrelated puzzle about number patterns.")])
    with pytest.raises(ValueError, match="Duplicate scan conflict"):
        duplicate_scan(rows, [SimpleNamespace(id="exact", question_text=rows[0]["question_text"])])
    with pytest.raises(ValueError, match="Duplicate scan conflict"):
        duplicate_scan(rows, [SimpleNamespace(id="near", question_text=rows[0]["question_text"] + " ")])


def test_builder_output_is_deterministic(tmp_path):
    builder.DATA = tmp_path
    builder.build()
    names = ["decision_making_verified_batch.json", "decision_making_answer_ledger.json", "decision_making_source_review.json", "decision_making_review_report.json", "decision_making_review_report.md"]
    before = {name: hashlib.sha256((tmp_path / name).read_bytes()).hexdigest() for name in names}
    builder.build()
    after = {name: hashlib.sha256((tmp_path / name).read_bytes()).hexdigest() for name in names}
    assert before == after


def test_import_dry_run_replay_conflict_and_unrelated_chapter_preservation(db_session, decision_making_catalog):
    _, _, chapter, other, preserved = decision_making_catalog
    rows = load_artifacts()
    payload = BATCH.read_bytes()
    preview = import_questions(db_session, payload, "application/json", BATCH.name, True)
    assert not preview.aborted and not preview.errors and not preview.rejected
    assert preview.would_import == 34 and preview.duplicates == 0
    assert db_session.scalar(select(func.count(Question.id)).where(Question.chapter_id == chapter.id)) == 0
    imported = import_questions(db_session, payload, "application/json", BATCH.name, False)
    assert imported.imported == 34 and imported.duplicates == 0 and not imported.errors
    replay = import_questions(db_session, payload, "application/json", BATCH.name, True)
    assert replay.would_import == 0 and replay.duplicates == 34 and not replay.aborted and not replay.errors
    db_session.flush()
    live = db_session.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
    verify_existing(rows, live)
    assert len(live) == 34
    assert db_session.scalar(select(func.count(Question.id)).where(Question.chapter_id == other.id)) == 1
    assert db_session.get(Question, preserved.id).question_text == "Unrelated pre-existing chapter record"
    live[0].explanation = "Conflicting manual edit"
    with pytest.raises(ValueError, match="conflicts with the canonical"):
        verify_existing(rows, live)


def test_authenticated_api_difficulty_mixed_and_exam_review_flow(client, db_session, decision_making_catalog):
    exam, subject, chapter, other, _ = decision_making_catalog
    rows = load_artifacts()
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    import_questions(db_session, BATCH.read_bytes(), "application/json", BATCH.name, False)
    db_session.flush()
    user = User(email="ch20-test-taker@example.com", password_hash="unused", is_active=True)
    db_session.add(user)
    db_session.commit()
    headers = {"Authorization": f"Bearer {create_access_token(user.id)}"}
    subjects = client.get(f"/api/exams/{exam.id}/subjects", headers=headers)
    assert subjects.status_code == 200 and any(item["slug"] == "reasoning" for item in subjects.json())
    chapters = client.get(f"/api/exams/subjects/{subject.id}/chapters", headers=headers)
    assert chapters.status_code == 200
    assert any(item["id"] == str(chapter.id) and item["slug"] == "decision-making" for item in chapters.json())

    for level, expected in (("EASY", 11), ("MEDIUM", 12), ("HARD", 11)):
        availability = client.get(f"/api/exams/chapters/{chapter.id}/availability", params={"level": level, "question_count": 10}, headers=headers)
        assert availability.status_code == 200 and availability.json()["available_question_count"] == expected
        assert availability.json()["can_satisfy_request"] is True
        start = client.post("/api/tests", json={"exam_id": str(exam.id), "subject_id": str(subject.id), "chapter_id": str(chapter.id), "test_type": "CHAPTER_WISE", "difficulty": level, "question_count": 10}, headers=headers)
        assert start.status_code == 201, start.text
        active = start.json()
        allowed = {row["question_text"] for row in rows if row["difficulty"] == level}
        assert len(active["questions"]) == 10 and active["duration_seconds"] == 360
        assert {q["question_text"] for q in active["questions"]} <= allowed
        assert all(len(q["options"]) == 4 and all("is_correct" not in o for o in q["options"]) for q in active["questions"])
        client.post(f"/api/tests/{active['id']}/submit", headers=headers)

    pyq = client.get(f"/api/exams/chapters/{chapter.id}/availability", params={"level": "PYQ", "question_count": 10}, headers=headers)
    assert pyq.status_code == 200 and pyq.json()["available_question_count"] == 0
    assert pyq.json()["allowed_question_counts"] == [] and pyq.json()["can_satisfy_request"] is False
    mixed_args = {"exam_id": str(exam.id), "subject_id": str(subject.id), "chapter_id": str(chapter.id), "test_type": "CHAPTER_WISE", "question_count": 10}
    availability = client.get("/api/tests/availability", params=mixed_args, headers=headers)
    assert availability.status_code == 200 and availability.json()["available_question_count"] == 34
    mixed = client.post("/api/tests", json=mixed_args, headers=headers)
    assert mixed.status_code == 201
    assert all(q["question_text"] in {row["question_text"] for row in rows} for q in mixed.json()["questions"])
    client.post(f"/api/tests/{mixed.json()['id']}/submit", headers=headers)

    hard_start = client.post("/api/tests", json={**mixed_args, "difficulty": "HARD"}, headers=headers)
    assert hard_start.status_code == 201
    active = hard_start.json()
    selected = active["questions"][:2]
    answers = []
    for index, question in enumerate(selected):
        canonical = next(row for row in rows if row["question_text"] == question["question_text"])
        key = canonical["correct_option"] if index == 0 else next(key for key in "ABCD" if key != canonical["correct_option"])
        answers.append((question, key))
        saved = client.put(f"/api/tests/{active['id']}/questions/{question['test_question_id']}/answer", json={"selected_option": key}, headers=headers)
        assert saved.status_code == 200
    reloaded = client.get(f"/api/tests/{active['id']}", headers=headers)
    assert reloaded.status_code == 200
    by_id = {q["test_question_id"]: q for q in reloaded.json()["questions"]}
    assert all(by_id[question["test_question_id"]]["selected_option"] == key for question, key in answers)
    submitted = client.post(f"/api/tests/{active['id']}/submit", headers=headers)
    assert submitted.status_code == 200 and submitted.json()["correct_count"] == 1 and submitted.json()["wrong_count"] == 1
    assert submitted.json()["unanswered_count"] == 8 and submitted.json()["score"] == 1.5
    result = client.get(f"/api/tests/{active['id']}/result", headers=headers)
    assert result.status_code == 200 and len(result.json()["review"]) == 10
    audit_by_question = {row["question_text"]: audit for row, audit in zip(rows, ledger)}
    for item in result.json()["review"]:
        expected = next(row for row in rows if row["question_text"] == item["question_text"])
        assert item["correct_option"] == expected["correct_option"]
        assert item["explanation"] == expected["explanation"]
        if audit_by_question[item["question_text"]]["category"] == "ELIGIBILITY":
            assert "Rules:" in item["question_text"] and "Case:" in item["question_text"]
    assert db_session.scalar(select(func.count(Question.id)).where(Question.chapter_id == other.id)) == 1
