"""Focused artifact and Calendar difficulty-availability regression checks."""

import json
import unicodedata
import calendar
from collections import Counter
from datetime import date
from difflib import SequenceMatcher
from pathlib import Path

from app.auth.security import create_access_token
from app.models import Chapter, Difficulty, Exam, Question, QuestionOption, Subject, User

BASE = Path(__file__).resolve().parents[1]
BATCH = BASE / "data" / "calendar_verified_batch.json"
LEDGER = BASE / "data" / "calendar_answer_ledger.json"
ORIGINAL = "Original SSC-style practice question"


def norm(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def records():
    return json.loads(BATCH.read_text(encoding="utf-8"))["questions"], json.loads(LEDGER.read_text(encoding="utf-8"))


def test_batch_has_30_aligned_valid_normal_questions():
    rows, ledger = records()
    assert len(rows) == len(ledger) == 30
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 10, "MEDIUM": 10, "HARD": 10}
    assert Counter("original" if row["source"] == ORIGINAL else "pdf" for row in rows) == {"pdf": 9, "original": 21}
    for i, (row, audit) in enumerate(zip(rows, ledger), 1):
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == ("reasoning", None, "calendar-recorded")
        assert row["is_pyq"] is False and row["pyq_year"] is None and row["pyq_exam_name"] is None
        assert row["question_text"].strip() and row["explanation"].strip() and len(row["source"]) <= 255
        assert row["difficulty"] in {"EASY", "MEDIUM", "HARD"}
        options = row["options"]
        assert set(options) == set("ABCD") and all(value.strip() for value in options.values())
        assert len({norm(value) for value in options.values()}) == 4
        assert row["correct_option"] in options
        assert audit["question_id"] == f"calendar-{i:03}" and audit["row"] == i
        assert audit["question"] == row["question_text"]
        assert audit["expected_answer"] == options[row["correct_option"]]
        assert audit["correct_option"] == row["correct_option"]
        assert audit["difficulty"] == row["difficulty"] and audit["source"] == row["source"]
        assert audit["independent_reasoning"].strip() and audit["option_review"].strip()
        assert audit["validation_status"].startswith("PASS")
        if row["source"] == ORIGINAL:
            assert audit["source_type"] == "original" and audit["source_pdf"] is None and audit["source_page"] is None
        else:
            assert audit["source_type"] == "pdf-derived"
            assert audit["source_pdf"] in row["source"] and isinstance(audit["source_page"], int)


def test_stems_signatures_and_series_artifact_comparison_are_unique():
    rows, ledger = records()
    stems = [norm(row["question_text"]) for row in rows]
    assert len(set(stems)) == 30
    signatures = [audit["concept_signature"] for audit in ledger]
    assert all(signatures) and len(set(signatures)) == 30
    for i, stem in enumerate(stems):
        assert all(SequenceMatcher(None, stem, prior).ratio() < 0.97 for prior in stems[:i])
    paths = list((BASE / "data").glob("*.json")) + [BASE.parent / "maximum_and_minimum_value_verified_batch.json"]
    for path in paths:
        if path == BATCH or not path.exists():
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        prior_rows = payload.get("questions", []) if isinstance(payload, dict) else []
        for prior in prior_rows if isinstance(prior_rows, list) else []:
            if not isinstance(prior, dict) or prior.get("subject_slug") != "reasoning":
                continue
            candidate = norm(prior.get("question_text", ""))
            assert candidate not in set(stems), f"Exact duplicate in {path.name}: {candidate}"
            assert all(SequenceMatcher(None, candidate, stem).ratio() < 0.97 for stem in stems), f"Near duplicate in {path.name}: {candidate}"


def test_independent_gregorian_calculation_checkpoints():
    rows, _ = records()
    keyed = {row["question_text"]: row["options"][row["correct_option"]] for row in rows}
    assert date(1995, 3, 26).strftime("%A") == keyed["What day of the week was 26 March 1995?"]
    assert date(2005, 2, 12).strftime("%A") == "Saturday"
    days = (date(2017, 5, 24) - date(2005, 2, 12)).days
    weekday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    assert weekday[(weekday.index("Saturday") + days) % 7] == keyed["If 12 February 2005 was Saturday, what day of the week was 24 May 2017?"]
    assert (date(2000, 3, 1) - date(1900, 3, 1)).days == int(keyed["How many days elapse from 1 March 1900 to 1 March 2000?"].replace(",", ""))
    assert (date(2100, 1, 1) - date(2000, 1, 1)).days % 7 == 6
    assert (date(2025, 1, 1) - date(2024, 1, 1)).days == 366
    assert sum(date(2025, month, 1).weekday() == calendar.SATURDAY for month in range(1, 13)) == int(
        keyed["In 2025, how many months begin on a Saturday?"]
    )


def test_calendar_chapter_availability_api_exposes_ten_each_level(client, db_session):
    exam = Exam(name="SSC", slug="ssc", is_active=True)
    db_session.add(exam)
    db_session.flush()
    subject = Subject(exam_id=exam.id, name="Reasoning", slug="reasoning", is_active=True)
    db_session.add(subject)
    db_session.flush()
    chapter = Chapter(subject_id=subject.id, name="Calendar (Recorded)", slug="calendar-recorded", is_active=True)
    db_session.add(chapter)
    user = User(email="calendar-availability@example.com", password_hash="not-used", is_active=True)
    db_session.add(user)
    db_session.flush()
    for difficulty in (Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD):
        for number in range(10):
            question = Question(
                chapter_id=chapter.id,
                question_text=f"{difficulty.value} test question {number}",
                explanation="A test explanation.",
                difficulty=difficulty,
                is_pyq=False,
                is_active=True,
            )
            db_session.add(question)
            db_session.flush()
            db_session.add_all([
                QuestionOption(question_id=question.id, option_key=key, option_text=f"{key}{number}", display_order=i, is_correct=(i == 1))
                for i, key in enumerate("ABCD", 1)
            ])
    db_session.commit()
    headers = {"Authorization": f"Bearer {create_access_token(user_id=user.id)}"}
    for level in ("EASY", "MEDIUM", "HARD"):
        response = client.get(
            f"/api/exams/chapters/{chapter.id}/availability",
            params={"level": level, "question_count": 10},
            headers=headers,
        )
        assert response.status_code == 200
        assert response.json()["available_question_count"] == 10
        assert response.json()["allowed_question_counts"] == [10]
        assert response.json()["can_satisfy_request"] is True
