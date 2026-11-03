"""Source, schema, answer, deduplication, availability and exam-flow checks."""

import json
import unicodedata
import uuid
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

from app.auth.security import create_access_token
from app.models import Chapter, Difficulty, Exam, Question, QuestionOption, Subject, User

BASE = Path(__file__).resolve().parents[1]
BATCH = BASE / "data" / "venn_diagram_verified_batch.json"
LEDGER = BASE / "data" / "venn_diagram_answer_ledger.json"
ORIGINAL = "Original SSC-style practice question"


def norm(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def records():
    return json.loads(BATCH.read_text(encoding="utf-8"))["questions"], json.loads(LEDGER.read_text(encoding="utf-8"))


def seed_chapter_bank(db_session):
    rows, _ = records()
    exam = Exam(name="SSC", slug="ssc", is_active=True)
    db_session.add(exam)
    db_session.flush()
    subject = Subject(exam_id=exam.id, name="Reasoning", slug="reasoning", is_active=True)
    db_session.add(subject)
    db_session.flush()
    chapter = Chapter(subject_id=subject.id, name="Venn Diagram", slug="venn-diagram", is_active=True)
    db_session.add(chapter)
    user = User(email="venn-test@example.com", password_hash="not-used", is_active=True)
    db_session.add(user)
    db_session.flush()
    for row in rows:
        question = Question(
            chapter_id=chapter.id,
            question_text=row["question_text"],
            explanation=row["explanation"],
            difficulty=Difficulty(row["difficulty"]),
            is_pyq=False,
            is_active=True,
            source=row["source"],
        )
        db_session.add(question)
        db_session.flush()
        db_session.add_all([
            QuestionOption(
                question_id=question.id,
                option_key=key,
                option_text=value,
                display_order=index,
                is_correct=(key == row["correct_option"]),
            )
            for index, (key, value) in enumerate(row["options"].items(), 1)
        ])
    db_session.commit()
    return exam, subject, chapter, user


def test_batch_has_30_valid_unique_normal_questions_and_complete_ledger():
    rows, ledger = records()
    selected = [entry for entry in ledger if entry["record_type"] == "selected_question"]
    rejected = [entry for entry in ledger if entry["record_type"] == "rejected_source_prompt"]
    assert len(rows) == len(selected) == 30
    assert len(rejected) == 12
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 10, "MEDIUM": 10, "HARD": 10}
    assert Counter("original" if row["source"] == ORIGINAL else "pdf" for row in rows) == {"pdf": 13, "original": 17}
    assert Counter(entry["question_category"] for entry in selected) == {"logical_classification": 12, "numerical": 18}
    assert Counter(entry["set_count"] for entry in selected) == {2: 5, 3: 21, 4: 4}
    for index, (row, audit) in enumerate(zip(rows, selected), 1):
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == ("reasoning", None, "venn-diagram")
        assert row["is_pyq"] is False and row["pyq_year"] is None and row["pyq_exam_name"] is None
        assert row["question_text"].strip() and row["explanation"].strip() and len(row["source"]) <= 255
        options = row["options"]
        assert set(options) == set("ABCD") and all(value.strip() for value in options.values())
        assert len({norm(value) for value in options.values()}) == 4
        assert row["correct_option"] in options
        assert audit["question_id"] == f"venn-{index:03}" and audit["row"] == index
        assert audit["question"] == row["question_text"] and audit["options"] == options
        assert audit["expected_answer"] == options[row["correct_option"]]
        assert audit["correct_option"] == row["correct_option"]
        assert audit["difficulty"] == row["difficulty"] and audit["source"] == row["source"]
        assert audit["is_pyq"] is False and audit["independent_verification"].strip()
        assert audit["validation_status"].startswith("PASS")
        if row["source"] == ORIGINAL:
            assert audit["source_type"] == "original" and audit["source_pdf"] is None and audit["source_page"] is None
        else:
            assert audit["source_type"] == "pdf-derived" and audit["source_pdf"] in row["source"]
            assert isinstance(audit["source_page"], int)
    assert all(entry["rejection_reason"].strip() and entry["source_pdf"] and entry["source_page"] for entry in rejected)


def test_batch_stems_and_problem_signatures_are_unique_against_reasoning_batches():
    rows, ledger = records()
    selected = [entry for entry in ledger if entry["record_type"] == "selected_question"]
    stems = [norm(row["question_text"]) for row in rows]
    signatures = [entry["concept_signature"] for entry in selected]
    assert len(set(stems)) == len(rows) and len(set(signatures)) == len(rows)
    language_variants = {
        "languages_exactly_one_source_diagram",
        "languages_exactly_two_source_diagram",
        "languages_all_three_source_diagram",
    }
    for index, stem in enumerate(stems):
        for prior_index, prior in enumerate(stems[:index]):
            left, right = stem, prior
            if signatures[index] in language_variants and signatures[prior_index] in language_variants:
                # These are three separate source questions using the same diagram;
                # their short requests are expected to share nearly all wording.
                left = left[left.rfind("how many people speak"):]
                right = right[right.rfind("how many people speak"):]
                assert left != right
                continue
            assert SequenceMatcher(None, left, right).ratio() < 0.94
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
            assert all(SequenceMatcher(None, candidate, stem).ratio() < 0.94 for stem in stems), f"Near duplicate in {path.name}: {candidate}"


def test_independent_two_and_three_set_answer_checkpoints():
    rows, _ = records()
    answers = {row["question_text"]: row["options"][row["correct_option"]] for row in rows}
    assert 46 + 39 - 17 == int(answers["In a survey, 46 people chose A, 39 chose B, and 17 chose both. How many chose at least one of A or B?"])
    assert 150 - 28 == 122
    assert 86 + 72 - 122 == int(answers["Of 150 people, 86 drink tea, 72 drink coffee, and 28 drink neither. How many drink both tea and coffee?"])
    assert 58 - 31 == int(answers["In a class, 72 study Mathematics, 58 study Science, and 31 study both. How many study Science only?"])
    assert 55 + 48 - 78 == 25 and (55 - 25) + (48 - 25) == int(answers["Of 90 people, 55 belong to A and 48 to B. If 78 belong to at least one set, how many belong to exactly one set?"])
    assert 75 - 30 - 25 + 10 == int(answers["Set A has 75 members. The inclusive totals are A∩B=30 and A∩C=25, while A∩B∩C=10. How many are in A only?"])
    union = 110 + 100 + 90 - 40 - 35 - 30 + 15
    assert union == 210 and 240 - union == int(answers["In a survey of 240 people, A=110, B=100, C=90; inclusive AB=40, AC=35, BC=30; all three=15. How many belong to none of the sets?"])
    assert 12 + 6 == int(answers["A survey diagram shows A-only 10, B-only 12, C-only 8, AB-only 4, AC-only 3, BC-only 5, all three 2, and outside all sets 6. How many are neither A nor C?"])
    assert sum((14, 11, 9, 6, 5, 4, 3)) == int(answers["Three sets have disjoint region counts: A-only 14, B-only 11, C-only 9, AB-only 6, AC-only 5, BC-only 4, and all three 3. How many belong to at least one set?"])


def test_availability_and_full_hard_exam_flow(client, db_session):
    from app.models import TestQuestion

    exam, subject, chapter, user = seed_chapter_bank(db_session)
    headers = {"Authorization": f"Bearer {create_access_token(user_id=user.id)}"}
    catalog = client.get(f"/api/exams/subjects/{subject.id}/chapters", headers=headers)
    assert catalog.status_code == 200
    assert any(entry["id"] == str(chapter.id) and entry["slug"] == "venn-diagram" for entry in catalog.json())
    for level in ("EASY", "MEDIUM", "HARD"):
        response = client.get(
            f"/api/exams/chapters/{chapter.id}/availability",
            params={"level": level, "question_count": 10}, headers=headers,
        )
        assert response.status_code == 200
        assert response.json()["available_question_count"] == 10
        assert response.json()["allowed_question_counts"] == [10]
        assert response.json()["can_satisfy_request"] is True
    mixed = client.get("/api/tests/availability", params={
        "exam_id": str(exam.id), "subject_id": str(subject.id),
        "test_type": "CHAPTER_WISE", "chapter_id": str(chapter.id),
    }, headers=headers)
    assert mixed.status_code == 200
    assert mixed.json()["available_question_count"] == 30
    assert mixed.json()["allowed_question_counts"] == [10, 15, 20, 25]
    pyq = client.get(f"/api/exams/chapters/{chapter.id}/availability", params={"level": "PYQ"}, headers=headers)
    assert pyq.status_code == 200 and pyq.json()["available_question_count"] == 0

    started = client.post("/api/tests", json={
        "exam_id": str(exam.id), "subject_id": str(subject.id),
        "test_type": "CHAPTER_WISE", "chapter_id": str(chapter.id),
        "difficulty": "HARD", "question_count": 10,
    }, headers=headers)
    assert started.status_code == 201, started.text
    attempt = started.json()
    assert attempt["question_count"] == 10 and attempt["duration_seconds"] == 360
    assert len(attempt["questions"]) == 10
    assert all("correct_option" not in q and "explanation" not in q for q in attempt["questions"])
    by_stem = {row["question_text"]: row for row in records()[0] if row["difficulty"] == "HARD"}
    for presented in attempt["questions"]:
        row = by_stem[presented["question_text"]]
        saved = client.put(
            f"/api/tests/{attempt['id']}/questions/{presented['test_question_id']}/answer",
            json={"selected_option": row["correct_option"]}, headers=headers,
        )
        assert saved.status_code == 200
    resumed = client.get(f"/api/tests/{attempt['id']}", headers=headers)
    assert resumed.status_code == 200 and all(q["selected_option"] for q in resumed.json()["questions"])
    assert db_session.query(TestQuestion).filter_by(test_attempt_id=uuid.UUID(attempt["id"])).count() == 10
    submitted = client.post(f"/api/tests/{attempt['id']}/submit", headers=headers)
    assert submitted.status_code == 200
    assert submitted.json()["correct_count"] == 10 and submitted.json()["wrong_count"] == 0
    result = client.get(f"/api/tests/{attempt['id']}/result", headers=headers)
    assert result.status_code == 200 and len(result.json()["review"]) == 10
    assert all(item["is_correct"] and item["explanation"] and item["correct_option"] for item in result.json()["review"])
