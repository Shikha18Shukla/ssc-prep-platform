"""Question import and protected management API tests."""

import json
import uuid
import csv
import io
from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import event, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.security import create_access_token
from app.models import Chapter, Difficulty, Exam, Question, QuestionOption, Subject, Subcategory, User


@pytest.fixture
def question_headers(db_session: Session) -> dict[str, str]:
    user = User(email="question-bank@example.com", password_hash="not-used", is_active=True, is_admin=True)
    db_session.add(user)
    db_session.commit()
    return {"Authorization": f"Bearer {create_access_token(user_id=user.id)}"}


@pytest.fixture
def question_catalog(db_session: Session) -> dict[str, object]:
    exam = Exam(name="SSC", slug="ssc", is_active=True)
    db_session.add(exam)
    db_session.flush()
    subject = Subject(exam_id=exam.id, name="Maths", slug="maths", is_active=True)
    db_session.add(subject)
    db_session.flush()
    category = Subcategory(subject_id=subject.id, name="Arithmetic", slug="arithmetic", is_active=True)
    db_session.add(category)
    db_session.flush()
    chapter = Chapter(
        subject_id=subject.id,
        subcategory_id=category.id,
        name="Number System",
        slug="number-system",
        is_active=True,
    )
    direct_chapter = Chapter(
        subject_id=subject.id,
        name="Direct Chapter",
        slug="direct-chapter",
        is_active=True,
    )
    db_session.add_all([chapter, direct_chapter])
    db_session.commit()
    return {"exam": exam, "subject": subject, "category": category, "chapter": chapter, "direct_chapter": direct_chapter}


def record(chapter_catalog: dict[str, object], **updates) -> dict:
    row = {
        "subject_slug": "maths",
        "subcategory_slug": "arithmetic",
        "chapter_slug": "number-system",
        "question_text": "Illustrative placeholder question text",
        "option_a": "Illustrative option A",
        "option_b": "Illustrative option B",
        "option_c": "Illustrative option C",
        "option_d": "Illustrative option D",
        "correct_option": "B",
        "explanation": "Illustrative explanation",
        "difficulty": "EASY",
        "is_pyq": False,
        "pyq_year": "",
        "pyq_exam_name": "",
        "source": "test fixture only",
    }
    row.update(updates)
    return row


def post_json(client, headers, rows, dry_run=True):
    return client.post(
        f"/api/questions/import?dry_run={'true' if dry_run else 'false'}",
        headers=headers,
        files={"file": ("questions.json", json.dumps({"questions": rows}), "application/json")},
    )


def option_values() -> list[dict]:
    return [
        {"option_key": key, "option_text": f"Corrected option {key}", "is_correct": key == "C", "display_order": idx}
        for idx, key in enumerate("ABCD", start=1)
    ]


def test_import_requires_authentication(client: TestClient, question_catalog: dict[str, object]) -> None:
    response = client.post(
        "/api/questions/import",
        files={"file": ("empty.csv", "", "text/csv")},
    )
    assert response.status_code in (401, 403)


def test_authenticated_student_cannot_import_or_manage_questions(
    client: TestClient,
    db_session: Session,
    question_catalog: dict[str, object],
) -> None:
    student = User(email="student@example.com", password_hash="not-used", is_active=True, is_admin=False)
    db_session.add(student)
    db_session.commit()
    headers = {"Authorization": f"Bearer {create_access_token(user_id=student.id)}"}
    upload = client.post(
        "/api/questions/import?dry_run=false",
        headers=headers,
        files={"file": ("questions.json", json.dumps({"questions": [record(question_catalog)]}), "application/json")},
    )
    assert upload.status_code == 403
    assert upload.json()["detail"] == "Administrator access required"
    assert client.get("/api/questions", headers=headers).status_code == 403
    assert db_session.scalar(select(func.count(Question.id))) == 0


def test_valid_json_import_and_dry_run_are_atomic(
    client: TestClient,
    db_session: Session,
    question_headers: dict[str, str],
    question_catalog: dict[str, object],
) -> None:
    item = record(question_catalog)
    preview = post_json(client, question_headers, [item], dry_run=True)
    assert preview.status_code == 200, preview.text
    assert preview.json()["would_import"] == 1
    assert preview.json()["imported"] == 0
    assert db_session.scalar(select(func.count(Question.id))) == 0

    committed = post_json(client, question_headers, [item], dry_run=False)
    assert committed.status_code == 200, committed.text
    assert committed.json()["imported"] == 1
    saved = db_session.execute(select(Question)).scalar_one()
    assert saved.chapter_id == question_catalog["chapter"].id
    assert len(saved.options) == 4
    assert sum(option.is_correct for option in saved.options) == 1
    assert next(option for option in saved.options if option.is_correct).option_key == "B"


def test_csv_import_and_row_numbered_invalid_options(
    client: TestClient,
    db_session: Session,
    question_headers: dict[str, str],
    question_catalog: dict[str, object],
) -> None:
    valid = record(question_catalog)
    headers = list(valid)
    csv_text = ",".join(headers) + "\n" + ",".join(str(valid[key]) for key in headers)
    response = client.post(
        "/api/questions/import?dry_run=false",
        headers=question_headers,
        files={"file": ("questions.csv", csv_text, "text/csv")},
    )
    assert response.status_code == 200, response.text
    assert response.json()["imported"] == 1

    invalid = record(question_catalog, option_d="", correct_option="Z")
    rejected = post_json(client, question_headers, [invalid], dry_run=False)
    assert rejected.status_code == 200
    result = rejected.json()
    assert result["aborted"] is True
    assert result["imported"] == 0
    assert result["rejected"] == 1
    assert {item["field"] for item in result["errors"]} >= {"option_d", "correct_option"}
    assert all(item["row"] == 1 for item in result["errors"])
    assert db_session.scalar(select(func.count(Question.id))) == 1

    invalid_csv = record(question_catalog, option_d="", correct_option="Z")
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(invalid_csv))
    writer.writeheader()
    writer.writerow(invalid_csv)
    csv_rejected = client.post(
        "/api/questions/import?dry_run=false",
        headers=question_headers,
        files={"file": ("invalid.csv", output.getvalue(), "text/csv")},
    )
    assert csv_rejected.status_code == 200
    assert {item["row"] for item in csv_rejected.json()["errors"]} == {2}


def test_wrong_subject_category_chapter_and_pyq_metadata_are_rejected(
    client: TestClient,
    db_session: Session,
    question_headers: dict[str, str],
    question_catalog: dict[str, object],
) -> None:
    wrong_parent = record(question_catalog, chapter_slug="direct-chapter")
    unknown_chapter = record(question_catalog, chapter_slug="not-a-chapter")
    unknown_subject = record(question_catalog, subject_slug="not-a-subject")
    bad_pyq = record(question_catalog, is_pyq=True, pyq_year="", pyq_exam_name="")
    bad_difficulty = record(question_catalog, difficulty="EXPERT")
    response = post_json(client, question_headers, [wrong_parent, unknown_chapter, unknown_subject, bad_pyq, bad_difficulty], dry_run=False)
    assert response.status_code == 200
    result = response.json()
    assert result["imported"] == 0
    assert result["rejected"] == 5
    fields = {item["field"] for item in result["errors"]}
    assert {"subject_slug", "subcategory_slug", "chapter_slug", "pyq_year", "difficulty"} <= fields
    assert "pyq_exam_name" not in fields
    assert db_session.scalar(select(func.count(Question.id))) == 0

    malformed_options = record(
        question_catalog,
        options={"A": "one", "B": "two", "C": "three", "D": "four", "E": "extra"},
    )
    invalid_shape = post_json(client, question_headers, [malformed_options], dry_run=False)
    assert invalid_shape.status_code == 200
    assert invalid_shape.json()["errors"][0]["field"] == "options"
    assert db_session.scalar(select(func.count(Question.id))) == 0


def test_valid_pyq_metadata_passes_dry_run_without_creating_rows(
    client: TestClient,
    db_session: Session,
    question_headers: dict[str, str],
    question_catalog: dict[str, object],
) -> None:
    pyq = record(
        question_catalog,
        is_pyq=True,
        pyq_year=date.today().year,
        pyq_exam_name="Illustrative exam name (test only)",
    )
    response = post_json(client, question_headers, [pyq], dry_run=True)
    assert response.status_code == 200
    assert response.json()["would_import"] == 1
    assert db_session.scalar(select(func.count(Question.id))) == 0

    named_pyq = {**pyq, "question_text": "PYQ with supplied exam name"}
    committed = post_json(client, question_headers, [named_pyq], dry_run=False)
    assert committed.status_code == 200, committed.text
    saved = db_session.execute(select(Question)).scalar_one()
    assert saved.is_pyq is True
    assert saved.pyq_year == date.today().year
    assert saved.pyq_exam_name == "Illustrative exam name (test only)"


def test_pyq_with_known_year_and_unknown_exam_passes_json_and_csv_dry_runs(
    client: TestClient,
    db_session: Session,
    question_headers: dict[str, str],
    question_catalog: dict[str, object],
) -> None:
    pyq = record(
        question_catalog,
        is_pyq=True,
        pyq_year=date.today().year,
        pyq_exam_name="   ",
        question_text="PYQ with unknown exam name: JSON preview",
    )
    json_preview = post_json(client, question_headers, [pyq], dry_run=True)
    assert json_preview.status_code == 200, json_preview.text
    assert json_preview.json()["aborted"] is False
    assert json_preview.json()["would_import"] == 1
    assert json_preview.json()["errors"] == []
    assert db_session.scalar(select(func.count(Question.id))) == 0

    csv_pyq = {**pyq, "question_text": "PYQ with unknown exam name: CSV preview", "pyq_exam_name": ""}
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(csv_pyq))
    writer.writeheader()
    writer.writerow(csv_pyq)
    csv_preview = client.post(
        "/api/questions/import?dry_run=true",
        headers=question_headers,
        files={"file": ("unknown-exam-pyq.csv", output.getvalue(), "text/csv")},
    )
    assert csv_preview.status_code == 200, csv_preview.text
    assert csv_preview.json()["aborted"] is False
    assert csv_preview.json()["would_import"] == 1
    assert csv_preview.json()["errors"] == []
    assert db_session.scalar(select(func.count(Question.id))) == 0


def test_pyq_with_unknown_exam_commits_as_null_in_isolated_test_database(
    client: TestClient,
    db_session: Session,
    question_headers: dict[str, str],
    question_catalog: dict[str, object],
) -> None:
    pyq = record(
        question_catalog,
        is_pyq=True,
        pyq_year=date.today().year,
        pyq_exam_name="",
    )
    response = post_json(client, question_headers, [pyq], dry_run=False)
    assert response.status_code == 200, response.text
    assert response.json()["imported"] == 1
    saved = db_session.execute(select(Question)).scalar_one()
    assert saved.is_pyq is True
    assert saved.pyq_year == date.today().year
    assert saved.pyq_exam_name is None


@pytest.mark.parametrize("pyq_year", ["", "not-a-year", "1800", str(date.today().year + 1)])
def test_pyq_without_valid_year_is_rejected_even_if_exam_name_is_unknown(
    client: TestClient,
    db_session: Session,
    question_headers: dict[str, str],
    question_catalog: dict[str, object],
    pyq_year: str,
) -> None:
    pyq = record(question_catalog, is_pyq=True, pyq_year=pyq_year, pyq_exam_name="")
    response = post_json(client, question_headers, [pyq], dry_run=True)
    assert response.status_code == 200
    assert response.json()["aborted"] is True
    assert {issue["field"] for issue in response.json()["errors"]} == {"pyq_year"}
    assert db_session.scalar(select(func.count(Question.id))) == 0


@pytest.mark.parametrize("metadata", [{"pyq_year": str(date.today().year)}, {"pyq_exam_name": "Named exam"}])
def test_non_pyq_with_any_pyq_metadata_remains_rejected(
    client: TestClient,
    db_session: Session,
    question_headers: dict[str, str],
    question_catalog: dict[str, object],
    metadata: dict[str, str],
) -> None:
    response = post_json(client, question_headers, [record(question_catalog, **metadata)], dry_run=True)
    assert response.status_code == 200
    assert response.json()["aborted"] is True
    assert response.json()["errors"][0]["field"] == "pyq_year"
    assert db_session.scalar(select(func.count(Question.id))) == 0


def test_pyq_exam_name_length_limit_remains_in_force(
    client: TestClient,
    question_headers: dict[str, str],
    question_catalog: dict[str, object],
) -> None:
    pyq = record(
        question_catalog,
        is_pyq=True,
        pyq_year=date.today().year,
        pyq_exam_name="x" * 101,
    )
    response = post_json(client, question_headers, [pyq], dry_run=True)
    assert response.status_code == 200
    assert response.json()["aborted"] is True
    assert response.json()["errors"][0]["field"] == "pyq_exam_name"


def test_question_management_updates_allow_blank_exam_name_but_require_year(
    client: TestClient,
    db_session: Session,
    question_headers: dict[str, str],
    question_catalog: dict[str, object],
) -> None:
    question = Question(
        chapter_id=question_catalog["chapter"].id,
        question_text="Question to update with unknown PYQ exam",
        difficulty=Difficulty.EASY,
        is_pyq=False,
        is_active=True,
    )
    question.options = [
        QuestionOption(
            option_key=key,
            option_text=f"Option {key}",
            display_order=position,
            is_correct=key == "B",
        )
        for position, key in enumerate("ABCD", start=1)
    ]
    db_session.add(question)
    db_session.commit()

    values = {
        "question_text": question.question_text,
        "explanation": None,
        "difficulty": "EASY",
        "is_pyq": True,
        "pyq_year": date.today().year,
        "source": "unit test",
        "options": [
            {"option_key": key, "option_text": f"Option {key}", "is_correct": key == "B", "display_order": position}
            for position, key in enumerate("ABCD", start=1)
        ],
    }
    for exam_name in (None, "", "   "):
        response = client.put(
            f"/api/questions/{question.id}",
            headers=question_headers,
            json={**values, "pyq_exam_name": exam_name},
        )
        assert response.status_code == 200, response.text
        assert response.json()["is_pyq"] is True
        assert response.json()["pyq_year"] == date.today().year
        assert response.json()["pyq_exam_name"] is None

    named_exam = client.put(
        f"/api/questions/{question.id}",
        headers=question_headers,
        json={**values, "pyq_exam_name": "  SSC CGL  "},
    )
    assert named_exam.status_code == 200
    assert named_exam.json()["pyq_exam_name"] == "SSC CGL"

    missing_year = client.put(
        f"/api/questions/{question.id}",
        headers=question_headers,
        json={**values, "pyq_year": None, "pyq_exam_name": None},
    )
    assert missing_year.status_code == 422
    invalid_year = client.put(
        f"/api/questions/{question.id}",
        headers=question_headers,
        json={**values, "pyq_year": 1949, "pyq_exam_name": None},
    )
    assert invalid_year.status_code == 422
    too_long_name = client.put(
        f"/api/questions/{question.id}",
        headers=question_headers,
        json={**values, "pyq_exam_name": "x" * 101},
    )
    assert too_long_name.status_code == 422
    non_pyq_metadata = client.put(
        f"/api/questions/{question.id}",
        headers=question_headers,
        json={**values, "is_pyq": False, "pyq_exam_name": None},
    )
    assert non_pyq_metadata.status_code == 422


def test_existing_and_in_file_duplicates_are_reported_without_overwrite(
    client: TestClient,
    db_session: Session,
    question_headers: dict[str, str],
    question_catalog: dict[str, object],
) -> None:
    first = record(question_catalog)
    committed = post_json(client, question_headers, [first], dry_run=False)
    assert committed.json()["imported"] == 1
    original = db_session.execute(select(Question)).scalar_one()
    duplicate = record(question_catalog, question_text="  ILLUSTRATIVE   PLACEHOLDER QUESTION TEXT ")
    second_duplicate = record(question_catalog, question_text="Illustrative placeholder question text")
    new_record = record(question_catalog, question_text="A separate illustrative placeholder")
    response = post_json(client, question_headers, [duplicate, second_duplicate, new_record], dry_run=False)
    assert response.status_code == 200
    assert response.json()["duplicates"] == 2
    assert response.json()["duplicate_rows"] == [1, 2]
    assert response.json()["imported"] == 1
    db_session.refresh(original)
    assert original.question_text == first["question_text"]
    assert db_session.scalar(select(func.count(Question.id))) == 2


def test_commit_failure_rolls_back_all_questions(
    client: TestClient,
    db_session: Session,
    question_headers: dict[str, str],
    question_catalog: dict[str, object],
) -> None:
    def fail_flush(_session, _flush_context, _instances):
        raise IntegrityError("simulated failure", {}, RuntimeError("constraint"))

    event.listen(db_session, "before_flush", fail_flush)
    try:
        response = post_json(client, question_headers, [record(question_catalog)], dry_run=False)
    finally:
        event.remove(db_session, "before_flush", fail_flush)
    assert response.status_code == 409
    assert db_session.scalar(select(func.count(Question.id))) == 0
    assert db_session.scalar(select(func.count(QuestionOption.id))) == 0


def test_management_filters_updates_status_and_keeps_answers_out_of_catalog(
    client: TestClient,
    db_session: Session,
    question_headers: dict[str, str],
    question_catalog: dict[str, object],
) -> None:
    imported = post_json(client, question_headers, [record(question_catalog)], dry_run=False)
    question_id = imported.json()
    saved = db_session.execute(select(Question)).scalar_one()
    list_response = client.get(
        "/api/questions?chapter_id=" + str(question_catalog["chapter"].id) + "&difficulty=EASY&is_pyq=false",
        headers=question_headers,
    )
    assert list_response.status_code == 200
    assert list_response.json()["total"] == 1
    assert list_response.json()["items"][0]["options"][1]["is_correct"] is True

    correction = {
        "question_text": "Corrected placeholder text",
        "explanation": "Corrected placeholder explanation",
        "difficulty": "MEDIUM",
        "is_pyq": False,
        "pyq_year": None,
        "pyq_exam_name": None,
        "source": "corrected import",
        "options": option_values(),
    }
    detail = client.put(f"/api/questions/{saved.id}", json=correction, headers=question_headers)
    assert detail.status_code == 200, detail.text
    assert detail.json()["question_text"] == "Corrected placeholder text"
    assert next(option for option in detail.json()["options"] if option["is_correct"])["option_key"] == "C"
    status_response = client.patch(
        f"/api/questions/{saved.id}/status", json={"is_active": False}, headers=question_headers
    )
    assert status_response.status_code == 200
    assert status_response.json()["is_active"] is False
    assert client.get("/api/exams/chapters/" + str(question_catalog["chapter"].id) + "/availability?level=EASY", headers=question_headers).json()["available_question_count"] == 0
    assert client.get("/api/questions/" + str(uuid.uuid4()), headers=question_headers).status_code == 404
    assert "options" not in client.get(
        f"/api/exams/chapters/{question_catalog['chapter'].id}/availability?level=EASY",
        headers=question_headers,
    ).json()
    assert client.get("/api/questions").status_code in (401, 403)
