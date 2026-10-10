"""Test engine API coverage for selection, ownership, timers and scoring."""

from datetime import datetime, timedelta, timezone
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.auth.security import create_access_token
from app.models import Chapter, Difficulty, Exam, Question, QuestionOption, Subject, Subcategory, User


@pytest.fixture
def test_setup(db_session: Session):
    user = User(email="test-taker@example.com", password_hash="unused", is_active=True)
    other = User(email="other-taker@example.com", password_hash="unused", is_active=True)
    exam = Exam(name="SSC", slug="ssc", is_active=True)
    db_session.add_all([user, other, exam])
    db_session.flush()
    subject = Subject(exam_id=exam.id, name="Maths", slug="maths", is_active=True)
    db_session.add(subject)
    db_session.flush()
    category = Subcategory(subject_id=subject.id, name="Arithmetic", slug="arithmetic", is_active=True)
    db_session.add(category)
    db_session.flush()
    chapter = Chapter(subject_id=subject.id, subcategory_id=category.id, name="Percentage", slug="percentage", is_active=True)
    db_session.add(chapter)
    db_session.flush()
    for n in range(12):
        question = Question(chapter_id=chapter.id, question_text=f"Question {n}", difficulty=Difficulty.EASY, is_pyq=False, is_active=True, explanation=f"Explanation {n}")
        db_session.add(question)
        db_session.flush()
        for idx, key in enumerate("ABCD"):
            db_session.add(QuestionOption(question_id=question.id, option_key=key, option_text=f"Option {key}", display_order=idx, is_correct=key == "A"))
    db_session.commit()
    return {
        "user": user,
        "other": other,
        "exam": exam,
        "subject": subject,
        "category": category,
        "chapter": chapter,
        "headers": {"Authorization": f"Bearer {create_access_token(user.id)}"},
        "other_headers": {"Authorization": f"Bearer {create_access_token(other.id)}"},
    }


def create_payload(records, count=10):
    return {
        "exam_id": str(records["exam"].id),
        "subject_id": str(records["subject"].id),
        "subcategory_id": str(records["category"].id),
        "chapter_id": str(records["chapter"].id),
        "difficulty": "EASY",
        "question_count": count,
    }


def test_create_test_selects_random_distinct_questions_and_hides_answers(client: TestClient, test_setup):
    response = client.post("/api/tests", json=create_payload(test_setup), headers=test_setup["headers"])
    assert response.status_code == 201, response.text
    body = response.json()
    assert body["question_count"] == 10
    assert body["duration_seconds"] == 360
    assert len({q["test_question_id"] for q in body["questions"]}) == 10
    assert len({q["question_text"] for q in body["questions"]}) == 10
    assert "correct_option" not in body["questions"][0]
    assert "explanation" not in body["questions"][0]
    assert "is_correct" not in body["questions"][0]["options"][0]


def test_insufficient_questions_does_not_create_partial_session(client: TestClient, test_setup, db_session):
    response = client.post("/api/tests", json=create_payload(test_setup, 15), headers=test_setup["headers"])
    assert response.status_code == 409
    from app.models import TestAttempt
    assert db_session.query(TestAttempt).count() == 0


def test_requires_auth_and_enforces_ownership(client: TestClient, test_setup):
    assert client.post("/api/tests", json=create_payload(test_setup)).status_code in (401, 403)
    created = client.post("/api/tests", json=create_payload(test_setup), headers=test_setup["headers"]).json()
    assert client.get(f"/api/tests/{created['id']}", headers=test_setup["other_headers"]).status_code == 404


def test_save_change_submit_and_score_correct_incorrect_unanswered(client: TestClient, test_setup):
    created = client.post("/api/tests", json=create_payload(test_setup), headers=test_setup["headers"]).json()
    questions = created["questions"]
    first = client.put(f"/api/tests/{created['id']}/questions/{questions[0]['test_question_id']}/answer", json={"selected_option": "A"}, headers=test_setup["headers"])
    assert first.status_code == 200
    changed = client.put(f"/api/tests/{created['id']}/questions/{questions[0]['test_question_id']}/answer", json={"selected_option": "B"}, headers=test_setup["headers"])
    assert changed.status_code == 200
    restored = client.put(f"/api/tests/{created['id']}/questions/{questions[0]['test_question_id']}/answer", json={"selected_option": "A"}, headers=test_setup["headers"])
    assert restored.status_code == 200
    wrong = client.put(f"/api/tests/{created['id']}/questions/{questions[1]['test_question_id']}/answer", json={"selected_option": "B"}, headers=test_setup["headers"])
    assert wrong.status_code == 200
    result = client.post(f"/api/tests/{created['id']}/submit", headers=test_setup["headers"])
    assert result.status_code == 200, result.text
    body = result.json()
    assert body["attempted_count"] == 2
    assert body["correct_count"] == 1
    assert body["wrong_count"] == 1
    assert body["unanswered_count"] == 8
    assert body["score"] == 1.5
    assert client.put(f"/api/tests/{created['id']}/questions/{questions[0]['test_question_id']}/answer", json={"selected_option": "A"}, headers=test_setup["headers"]).status_code == 409
    assert client.post(f"/api/tests/{created['id']}/submit", headers=test_setup["headers"]).json()["score"] == 1.5


def test_negative_score_is_not_clamped(client: TestClient, test_setup):
    created = client.post("/api/tests", json=create_payload(test_setup), headers=test_setup["headers"]).json()
    for question in created["questions"][:4]:
        response = client.put(
            f"/api/tests/{created['id']}/questions/{question['test_question_id']}/answer",
            json={"selected_option": "B"}, headers=test_setup["headers"],
        )
        assert response.status_code == 200
    result = client.post(f"/api/tests/{created['id']}/submit", headers=test_setup["headers"])
    assert result.json()["score"] == -2


def test_timeout_auto_submits_and_result_reveals_answers(client: TestClient, test_setup, db_session: Session):
    created = client.post("/api/tests", json=create_payload(test_setup), headers=test_setup["headers"]).json()
    from app.models import TestAttempt, TestQuestion
    attempt = db_session.get(TestAttempt, uuid.UUID(created["id"]))
    attempt.started_at = datetime.now(timezone.utc) - timedelta(seconds=400)
    db_session.commit()
    active = client.get(f"/api/tests/{created['id']}", headers=test_setup["headers"])
    assert active.status_code == 200
    assert active.json()["status"] == "AUTO_SUBMITTED"
    assert "correct_option" not in active.json()["questions"][0]
    result = client.get(f"/api/tests/{created['id']}/result", headers=test_setup["headers"])
    assert result.status_code == 200
    assert len(result.json()["review"]) == 10
    assert result.json()["review"][0]["correct_option"] == "A"


def test_rejects_category_chapter_mismatch(client: TestClient, test_setup):
    payload = create_payload(test_setup)
    payload["subcategory_id"] = str(uuid.uuid4())
    response = client.post("/api/tests", json=payload, headers=test_setup["headers"])
    assert response.status_code == 422


def test_dashboard_history_is_user_scoped(client: TestClient, test_setup):
    created = client.post("/api/tests", json=create_payload(test_setup), headers=test_setup["headers"]).json()
    client.post(f"/api/tests/{created['id']}/submit", headers=test_setup["headers"])
    history = client.get("/api/tests/history/me", headers=test_setup["headers"])
    assert history.status_code == 200
    assert history.json()["tests_attempted"] == 1
    other_history = client.get("/api/tests/history/me", headers=test_setup["other_headers"])
    assert other_history.json()["tests_attempted"] == 0
