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
    second_chapter = Chapter(subject_id=subject.id, subcategory_id=category.id, name="Profit and Loss", slug="profit-and-loss", is_active=True)
    db_session.add_all([chapter, second_chapter])
    db_session.flush()

    def seed_questions(target: Chapter, levels, prefix: str, is_pyq: bool = False):
        for difficulty in levels:
            for n in range(12):
                question = Question(chapter_id=target.id, question_text=f"{prefix} {difficulty.value} {n}", difficulty=difficulty, is_pyq=is_pyq, is_active=True, explanation=f"Explanation {n}")
                db_session.add(question)
                db_session.flush()
                for idx, key in enumerate("ABCD"):
                    db_session.add(QuestionOption(question_id=question.id, option_key=key, option_text=f"Option {key}", display_order=idx, is_correct=key == "A"))

    seed_questions(chapter, [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD], "Maths")
    seed_questions(second_chapter, [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD], "Maths second")
    seed_questions(chapter, [Difficulty.HARD], "Maths PYQ", is_pyq=True)

    extra = {}
    for name, slug in (("Reasoning", "reasoning"), ("GK / GS", "gk-gs"), ("English", "english")):
        other_subject = Subject(exam_id=exam.id, name=name, slug=slug, is_active=True)
        db_session.add(other_subject)
        db_session.flush()
        first = Chapter(subject_id=other_subject.id, name=f"{name} chapter 1", slug=f"{slug}-1", is_active=True)
        second = Chapter(subject_id=other_subject.id, name=f"{name} chapter 2", slug=f"{slug}-2", is_active=True)
        db_session.add_all([first, second])
        db_session.flush()
        seed_questions(first, [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD], slug)
        seed_questions(second, [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD], f"{slug} second")
        extra[slug] = {"subject": other_subject, "chapter": first, "second_chapter": second}
    db_session.commit()
    return {
        "user": user,
        "other": other,
        "exam": exam,
        "subject": subject,
        "category": category,
        "chapter": chapter,
        "second_chapter": second_chapter,
        "extra": extra,
        "headers": {"Authorization": f"Bearer {create_access_token(user.id)}"},
        "other_headers": {"Authorization": f"Bearer {create_access_token(other.id)}"},
    }


def create_payload(records, count=10):
    return {
        "exam_id": str(records["exam"].id),
        "subject_id": str(records["subject"].id),
        "subcategory_id": str(records["category"].id),
        "chapter_id": str(records["chapter"].id),
        "test_type": "CHAPTER_WISE",
        "difficulty": "EASY",
        "question_count": count,
    }


def ensure_percentage_test_pool(db_session: Session, chapter: Chapter):
    """Provide 30 ordinary questions per difficulty for count-option integration tests."""
    for difficulty in (Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD):
        existing = db_session.query(Question).filter_by(
            chapter_id=chapter.id, difficulty=difficulty, is_active=True, is_pyq=False,
        ).count()
        for index in range(existing, 30):
            question = Question(
                chapter_id=chapter.id,
                question_text=f"Percentage {difficulty.value} pool fixture item {index}",
                difficulty=difficulty,
                is_pyq=False,
                is_active=True,
                explanation="Fixture explanation.",
            )
            db_session.add(question)
            db_session.flush()
            db_session.add_all(
                QuestionOption(
                    question_id=question.id,
                    option_key=key,
                    option_text=f"Fixture {index} option {key}",
                    display_order=position,
                    is_correct=key == "A",
                )
                for position, key in enumerate("ABCD", start=1)
            )
    db_session.commit()


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


@pytest.mark.parametrize(
    "subject_slug,test_type,difficulty",
    [
        ("maths", "CHAPTER_WISE", "EASY"),
        ("maths", "MISCELLANEOUS", "HARD"),
        ("reasoning", "CHAPTER_WISE", "MEDIUM"),
        ("reasoning", "MISCELLANEOUS", "HARD"),
        ("gk-gs", "CHAPTER_WISE", None),
        ("gk-gs", "MISCELLANEOUS", None),
        ("english", "CHAPTER_WISE", None),
        ("english", "MISCELLANEOUS", None),
    ],
)
def test_supported_subject_test_type_and_difficulty_combinations(client, test_setup, db_session, subject_slug, test_type, difficulty):
    if subject_slug == "maths":
        subject = test_setup["subject"]
        chapter = test_setup["chapter"]
    else:
        subject = test_setup["extra"][subject_slug]["subject"]
        chapter = test_setup["extra"][subject_slug]["chapter"]
    payload = {
        "exam_id": str(test_setup["exam"].id),
        "subject_id": str(subject.id),
        "test_type": test_type,
        "chapter_id": str(chapter.id) if test_type == "CHAPTER_WISE" else None,
        "difficulty": difficulty,
        "question_count": 10,
    }
    response = client.post("/api/tests", json=payload, headers=test_setup["headers"])
    assert response.status_code == 201, response.text
    assert response.json()["test_type"] == test_type
    assert response.json()["chapter_id"] == (str(chapter.id) if test_type == "CHAPTER_WISE" else None)
    from app.models import TestAttempt, TestQuestion
    attempt = db_session.get(TestAttempt, uuid.UUID(response.json()["id"]))
    assert attempt.difficulty == (Difficulty(difficulty) if difficulty else None)
    selected = db_session.query(TestQuestion).filter_by(test_attempt_id=attempt.id).all()
    for row in selected:
        question = row.question
        assert question.chapter.subject_id == subject.id
        if test_type == "CHAPTER_WISE":
            assert question.chapter_id == chapter.id
        if difficulty:
            assert question.difficulty == Difficulty(difficulty)


def test_chapterwise_requires_chapter_and_rejects_chapter_from_another_subject(client, test_setup):
    payload = create_payload(test_setup)
    payload.pop("chapter_id")
    response = client.post("/api/tests", json=payload, headers=test_setup["headers"])
    assert response.status_code == 422
    assert "chapter is required" in response.json()["detail"].lower()

    payload = create_payload(test_setup)
    payload["chapter_id"] = str(test_setup["extra"]["english"]["chapter"].id)
    response = client.post("/api/tests", json=payload, headers=test_setup["headers"])
    assert response.status_code == 422
    assert "selected active subject" in response.json()["detail"].lower()


def test_miscellaneous_can_sample_multiple_chapters_from_selected_subject(client, test_setup, db_session):
    payload = create_payload(test_setup, 20)
    payload.update(test_type="MISCELLANEOUS", chapter_id=None, subcategory_id=None, difficulty="EASY")
    response = client.post("/api/tests", json=payload, headers=test_setup["headers"])
    assert response.status_code == 201, response.text
    from app.models import TestQuestion
    rows = db_session.query(TestQuestion).filter_by(test_attempt_id=uuid.UUID(response.json()["id"])).all()
    assert {row.question.chapter_id for row in rows} == {test_setup["chapter"].id, test_setup["second_chapter"].id}
    assert all(row.question.chapter.subject_id == test_setup["subject"].id for row in rows)


def test_miscellaneous_rejects_chapter_and_keeps_questions_in_selected_subject(client, test_setup):
    payload = create_payload(test_setup)
    payload.update(test_type="MISCELLANEOUS", difficulty="HARD")
    payload["chapter_id"] = str(test_setup["chapter"].id)
    response = client.post("/api/tests", json=payload, headers=test_setup["headers"])
    assert response.status_code == 422
    payload["chapter_id"] = None
    payload["subcategory_id"] = None
    payload["subject_id"] = str(test_setup["extra"]["english"]["subject"].id)
    payload["difficulty"] = None
    response = client.post("/api/tests", json=payload, headers=test_setup["headers"])
    assert response.status_code == 201, response.text


def test_maths_supports_mixed_difficulty_ordinary_tests_and_other_subjects_reject_difficulty(client, test_setup):
    payload = create_payload(test_setup)
    payload["difficulty"] = None
    response = client.post("/api/tests", json=payload, headers=test_setup["headers"])
    assert response.status_code == 201, response.text
    body = response.json()
    assert len(body["questions"]) == 10
    assert "correct_option" not in body["questions"][0]
    payload["subject_id"] = str(test_setup["extra"]["english"]["subject"].id)
    payload["chapter_id"] = str(test_setup["extra"]["english"]["chapter"].id)
    payload["difficulty"] = "EASY"
    response = client.post("/api/tests", json=payload, headers=test_setup["headers"])
    assert response.status_code == 422


def test_mixed_difficulty_percentage_selection_supports_all_standard_counts(client, test_setup, db_session):
    payload = create_payload(test_setup, 10)
    payload["difficulty"] = None
    params = {key: value for key, value in payload.items() if key != "question_count"}
    params.pop("difficulty")
    availability = client.get("/api/tests/availability", params=params, headers=test_setup["headers"])
    assert availability.status_code == 200
    assert availability.json()["allowed_question_counts"] == [10, 15, 20, 25]
    for count in (10, 15, 20, 25):
        payload["question_count"] = count
        started = client.post("/api/tests", json=payload, headers=test_setup["headers"])
        assert started.status_code == 201, started.text
        active = started.json()
        questions = active["questions"]
        assert len(questions) == count
        assert len({item["question_text"] for item in questions}) == count
        assert all("correct_option" not in item and "explanation" not in item for item in questions)
        assert all("is_correct" not in option for item in questions for option in item["options"])
        from app.models import TestAttempt, TestQuestion
        attempt = db_session.get(TestAttempt, uuid.UUID(active["id"]))
        rows = db_session.query(TestQuestion).filter_by(test_attempt_id=attempt.id).all()
        assert len({row.question_id for row in rows}) == count
        assert all(not row.question.is_pyq for row in rows)
        assert client.post(f"/api/tests/{active['id']}/submit", headers=test_setup["headers"]).status_code == 200


@pytest.mark.parametrize("difficulty", ["EASY", "MEDIUM", "HARD"])
@pytest.mark.parametrize("count", [10, 15, 20, 25])
def test_percentage_difficulty_selection_has_distinct_ordinary_question_counts(
    client, test_setup, db_session, difficulty, count,
):
    ensure_percentage_test_pool(db_session, test_setup["chapter"])
    payload = create_payload(test_setup, count)
    payload["difficulty"] = difficulty
    response = client.post("/api/tests", json=payload, headers=test_setup["headers"])
    assert response.status_code == 201, response.text
    active = response.json()
    assert active["question_count"] == count
    assert active["duration_seconds"] == count * 36
    assert len(active["questions"]) == count
    assert all("correct_option" not in q and "explanation" not in q for q in active["questions"])
    from app.models import TestAttempt, TestQuestion
    attempt = db_session.get(TestAttempt, uuid.UUID(active["id"]))
    rows = db_session.query(TestQuestion).filter_by(test_attempt_id=attempt.id).all()
    assert len(rows) == count
    assert len({row.question_id for row in rows}) == count
    assert all(not row.question.is_pyq and row.question.difficulty.value == difficulty for row in rows)


def test_percentage_attempt_order_persists_on_refresh_and_resamples_on_new_attempt(client, test_setup, db_session):
    ensure_percentage_test_pool(db_session, test_setup["chapter"])
    payload = create_payload(test_setup, 25)
    payload["difficulty"] = "HARD"
    headers = test_setup["headers"]
    first = client.post("/api/tests", json=payload, headers=headers)
    second = client.post("/api/tests", json=payload, headers=headers)
    assert first.status_code == second.status_code == 201
    first_body, second_body = first.json(), second.json()
    first_order = [item["question_text"] for item in first_body["questions"]]
    second_order = [item["question_text"] for item in second_body["questions"]]
    assert first_order != second_order
    refreshed = client.get(f"/api/tests/{first_body['id']}", headers=headers)
    assert refreshed.status_code == 200
    assert [item["question_text"] for item in refreshed.json()["questions"]] == first_order


def test_pyq_selection_is_separate_from_difficulty(client, test_setup, db_session):
    payload = create_payload(test_setup)
    payload["difficulty"] = "PYQ"
    response = client.post("/api/tests", json=payload, headers=test_setup["headers"])
    assert response.status_code == 201, response.text
    from app.models import TestAttempt, TestQuestion
    attempt = db_session.get(TestAttempt, uuid.UUID(response.json()["id"]))
    assert attempt.is_pyq is True
    assert attempt.difficulty is None
    rows = db_session.query(TestQuestion).filter_by(test_attempt_id=attempt.id).all()
    assert len(rows) == 10
    assert all(row.question.is_pyq for row in rows)


def test_legacy_attempt_without_test_type_remains_readable_as_chapterwise(client, test_setup, db_session):
    created = client.post("/api/tests", json=create_payload(test_setup), headers=test_setup["headers"]).json()
    from app.models import TestAttempt
    attempt = db_session.get(TestAttempt, uuid.UUID(created["id"]))
    attempt.test_type = None
    db_session.commit()
    response = client.get(f"/api/tests/{created['id']}", headers=test_setup["headers"])
    assert response.status_code == 200
    assert response.json()["test_type"] == "CHAPTER_WISE"


def test_availability_reports_count_for_subject_wide_miscellaneous(client, test_setup):
    response = client.get("/api/tests/availability", params={
        "exam_id": str(test_setup["exam"].id),
        "subject_id": str(test_setup["subject"].id),
        "test_type": "MISCELLANEOUS",
        "difficulty": "EASY",
        "question_count": 20,
    }, headers=test_setup["headers"])
    assert response.status_code == 200, response.text
    assert response.json()["available_question_count"] == 24
    assert response.json()["can_satisfy_request"] is True


@pytest.fixture
def science_pool_setup(client: TestClient, db_session: Session):
    user = User(email="science-pool@example.com", password_hash="unused", is_active=True)
    exam = Exam(name="SSC", slug="ssc", is_active=True)
    db_session.add_all([user, exam])
    db_session.flush()
    subject = Subject(exam_id=exam.id, name="GK / GS", slug="gk-gs", is_active=True)
    db_session.add(subject)
    db_session.flush()
    chapter = Chapter(subject_id=subject.id, name="Science pool", slug="science-pool", is_active=True)
    db_session.add(chapter)
    db_session.commit()
    return {
        "user": user,
        "exam": exam,
        "subject": subject,
        "chapter": chapter,
        "headers": {"Authorization": f"Bearer {create_access_token(user.id)}"},
    }


@pytest.mark.parametrize("pool_size", [0, 1, 6, 9, 10, 11, 12])
@pytest.mark.parametrize("is_pyq", [False, True], ids=["ordinary", "pyq"])
def test_science_test_uses_small_verified_pool_without_mixing_modes(
    client: TestClient, science_pool_setup, db_session: Session, pool_size: int, is_pyq: bool,
):
    chapter = Chapter(
        subject_id=science_pool_setup["subject"].id,
        name=f"Small pool {pool_size} {is_pyq}",
        slug=f"small-pool-{pool_size}-{is_pyq}",
        is_active=True,
    )
    db_session.add(chapter)
    db_session.flush()
    for index in range(pool_size):
        question = Question(
            chapter_id=chapter.id,
            question_text=f"Verified {('PYQ' if is_pyq else 'ordinary')} question {index}",
            explanation="Shown only after submission.",
            difficulty=Difficulty.MEDIUM,
            is_pyq=is_pyq,
            pyq_year=2020 if is_pyq else None,
            is_active=True,
        )
        db_session.add(question)
        db_session.flush()
        for order, key in enumerate("ABCD", start=1):
            db_session.add(QuestionOption(
                question_id=question.id,
                option_key=key,
                option_text=f"Option {key}",
                display_order=order,
                is_correct=key == "A",
            ))
    db_session.commit()

    level = "PYQ" if is_pyq else None
    params = {
        "exam_id": str(science_pool_setup["exam"].id),
        "subject_id": str(science_pool_setup["subject"].id),
        "test_type": "CHAPTER_WISE",
        "chapter_id": str(chapter.id),
    }
    if level:
        params["difficulty"] = level
    availability = client.get("/api/tests/availability", params=params, headers=science_pool_setup["headers"])
    assert availability.status_code == 200, availability.text
    body = availability.json()
    assert body["available_question_count"] == pool_size
    expected_counts = [count for count in (10, 15, 20, 25) if count <= pool_size]
    if 0 < pool_size <= 25 and pool_size not in expected_counts:
        expected_counts.append(pool_size)
    assert body["allowed_question_counts"] == sorted(expected_counts)

    if pool_size == 0:
        params["question_count"] = 1
        unavailable = client.get("/api/tests/availability", params=params, headers=science_pool_setup["headers"])
        assert unavailable.json()["can_satisfy_request"] is False
        payload = {
            **{key: value for key, value in params.items() if key != "question_count"},
            "subcategory_id": None,
            "difficulty": level,
            "question_count": 1,
        }
        rejected = client.post("/api/tests", json=payload, headers=science_pool_setup["headers"])
        assert rejected.status_code == 409
        assert "0 eligible active questions" in rejected.json()["detail"]
        return

    count = pool_size if pool_size <= 12 else 10
    payload = {
        **params,
        "subcategory_id": None,
        "difficulty": level,
        "question_count": count,
    }
    started = client.post("/api/tests", json=payload, headers=science_pool_setup["headers"])
    assert started.status_code == 201, started.text
    active = started.json()
    assert active["question_count"] == count
    assert active["duration_seconds"] == count * 36
    assert len(active["questions"]) == count
    assert "correct_option" not in active["questions"][0]
    assert "explanation" not in active["questions"][0]

    saved = client.put(
        f"/api/tests/{active['id']}/questions/{active['questions'][0]['test_question_id']}/answer",
        json={"selected_option": "A"},
        headers=science_pool_setup["headers"],
    )
    assert saved.status_code == 200
    result = client.post(f"/api/tests/{active['id']}/submit", headers=science_pool_setup["headers"])
    assert result.status_code == 200
    assert result.json()["question_count"] == count
    review = client.get(f"/api/tests/{active['id']}/result", headers=science_pool_setup["headers"])
    assert review.status_code == 200
    assert len(review.json()["review"]) == count
    assert all(question["is_correct"] is (index == 0) for index, question in enumerate(review.json()["review"]))


@pytest.mark.parametrize("pool_size", [0, 1, 6, 9, 10, 11, 12])
@pytest.mark.parametrize("is_pyq", [False, True], ids=["ordinary", "pyq"])
def test_science_short_pool_selection_service_isolated_from_http_client(
    db_session: Session, pool_size: int, is_pyq: bool,
):
    from fastapi import HTTPException
    from app.models import TestAttempt
    from app.schemas.tests import TestCreate
    from app.services.test_service import create_test, get_test_availability, save_answer, submit_test
    from app.routers.tests import _current, test_result

    user = User(email=f"science-{pool_size}-{is_pyq}@example.com", password_hash="unused", is_active=True)
    exam = Exam(name="SSC", slug="ssc", is_active=True)
    db_session.add_all([user, exam])
    db_session.flush()
    subject = Subject(exam_id=exam.id, name="GK / GS", slug="gk-gs", is_active=True)
    db_session.add(subject)
    db_session.flush()
    chapter = Chapter(subject_id=subject.id, name="Science", slug="science", is_active=True)
    db_session.add(chapter)
    db_session.flush()
    for index in range(pool_size):
        question = Question(
            chapter_id=chapter.id,
            question_text=f"{'PYQ' if is_pyq else 'ordinary'} {index}",
            explanation="Verified explanation",
            difficulty=Difficulty.MEDIUM,
            is_pyq=is_pyq,
            pyq_year=2020 if is_pyq else None,
            is_active=True,
        )
        db_session.add(question)
        db_session.flush()
        for order, key in enumerate("ABCD", start=1):
            db_session.add(QuestionOption(
                question_id=question.id,
                option_key=key,
                option_text=f"Option {key}",
                display_order=order,
                is_correct=(key == "A"),
            ))
    for index in range(3):
        question = Question(
            chapter_id=chapter.id,
            question_text=f"opposite mode {index}",
            explanation="Must not enter this test.",
            difficulty=Difficulty.MEDIUM,
            is_pyq=not is_pyq,
            pyq_year=None if is_pyq else 2020,
            is_active=True,
        )
        db_session.add(question)
        db_session.flush()
        for order, key in enumerate("ABCD", start=1):
            db_session.add(QuestionOption(
                question_id=question.id,
                option_key=key,
                option_text=f"Option {key}",
                display_order=order,
                is_correct=(key == "A"),
            ))
    db_session.commit()

    selected_mode = "PYQ" if is_pyq else None
    availability = get_test_availability(
        db_session, exam.id, subject.id, "CHAPTER_WISE", chapter.id, None, selected_mode,
    )
    assert availability["available_question_count"] == pool_size
    expected_counts = [count for count in (10, 15, 20, 25) if count <= pool_size]
    if 0 < pool_size <= 25 and pool_size not in expected_counts:
        expected_counts.append(pool_size)
    assert availability["allowed_question_counts"] == sorted(expected_counts)
    payload_count = pool_size if 0 < pool_size <= 12 else 10
    payload = TestCreate(
        exam_id=exam.id,
        subject_id=subject.id,
        test_type="CHAPTER_WISE",
        chapter_id=chapter.id,
        difficulty=selected_mode,
        question_count=payload_count,
    )
    if pool_size == 0:
        with pytest.raises(HTTPException) as error:
            create_test(db_session, user.id, payload)
        assert error.value.status_code == 409
        assert db_session.query(TestAttempt).count() == 0
        return

    attempt = create_test(db_session, user.id, payload)
    active = _current(attempt, db_session)
    assert active.question_count == payload_count
    assert active.duration_seconds == payload_count * 36
    assert active.difficulty == selected_mode
    assert "correct_option" not in active.questions[0].model_dump()
    assert "explanation" not in active.questions[0].model_dump()
    from app.models import TestQuestion
    first = db_session.query(TestQuestion).filter_by(test_attempt_id=attempt.id).order_by(TestQuestion.question_order).first()
    selected_rows = db_session.query(TestQuestion).filter_by(test_attempt_id=attempt.id).all()
    assert all(row.question.is_pyq is is_pyq for row in selected_rows)
    save_answer(db_session, attempt.id, first.id, "A", user.id)
    finished = submit_test(db_session, attempt.id, user.id)
    reviewed = test_result(attempt.id, user, db_session)
    assert finished.question_count == payload_count
    assert len(reviewed.review) == payload_count
    assert reviewed.review[0].correct_option == "A"
    assert reviewed.review[0].explanation == "Verified explanation"
