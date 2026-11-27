"""Account administration, scoped catalog, rate limits, and production config tests."""

from datetime import datetime, timezone
import uuid

from fastapi import HTTPException
import pytest
from pydantic import ValidationError
from sqlalchemy import func, select

from app.auth.security import create_access_token
from app.config import Settings, settings
from app.models import AuthSession, RateLimitWindow, Subcategory, Chapter, Exam, Subject, User
from app.security.rate_limit import enforce_rate_limit
from app.services.auth_service import issue_session, revoke_user_sessions
from app.services.catalog_service import (
    get_chapter_availability,
    list_active_chapters_for_selection,
    list_active_exams,
    list_active_subjects,
    list_active_subcategories,
)
from app.services.beta_scope import chapter_is_in_beta, subject_is_in_beta


def _user(db_session, email: str, *, is_admin: bool = False) -> User:
    user = User(email=email, password_hash=None, is_active=True, is_admin=is_admin)
    db_session.add(user)
    db_session.commit()
    return user


def test_admin_can_deactivate_account_and_revoke_all_sessions(client, db_session):
    admin = _user(db_session, "admin@example.test", is_admin=True)
    student = _user(db_session, "student@example.test")
    admin_headers = {"Authorization": f"Bearer {create_access_token(admin.id)}"}
    _, expires_at = issue_session(db_session, student)
    active_session = db_session.scalar(select(AuthSession).where(
        AuthSession.user_id == student.id, AuthSession.revoked_at.is_(None)
    ))
    assert active_session is not None

    response = client.patch(
        f"/api/admin/users/{student.id}/activation",
        headers=admin_headers,
        json={"is_active": False},
    )
    assert response.status_code == 200
    assert response.json()["is_active"] is False

    db_session.expire_all()
    student = db_session.get(User, student.id)
    assert student.is_active is False
    revoked = db_session.scalar(select(AuthSession).where(AuthSession.id == active_session.id))
    assert revoked.revoked_at is not None

    profile = client.get(
        "/api/auth/me", headers={"Authorization": f"Bearer {create_access_token(student.id)}"}
    )
    assert profile.status_code == 403


def test_regular_user_cannot_use_admin_endpoints(client, db_session):
    student = _user(db_session, "ordinary-student@example.test")
    target = _user(db_session, "target-student@example.test")
    response = client.patch(
        f"/api/admin/users/{target.id}/activation",
        headers={"Authorization": f"Bearer {create_access_token(student.id)}"},
        json={"is_active": False},
    )
    assert response.status_code == 403


def test_admin_cannot_deactivate_self_or_last_admin(client, db_session):
    admin = _user(db_session, "only-admin@example.test", is_admin=True)
    headers = {"Authorization": f"Bearer {create_access_token(admin.id)}"}
    self_response = client.patch(
        f"/api/admin/users/{admin.id}/activation", headers=headers, json={"is_active": False}
    )
    assert self_response.status_code == 409

    other_admin = _user(db_session, "second-admin@example.test", is_admin=True)
    db_session.delete(other_admin)
    db_session.commit()
    last_admin_response = client.patch(
        f"/api/admin/users/{admin.id}/activation", headers=headers, json={"is_active": False}
    )
    assert last_admin_response.status_code == 409


def test_revoke_user_sessions_is_idempotent(db_session):
    user = _user(db_session, "revoke@example.test")
    issue_session(db_session, user)
    issue_session(db_session, user)
    revoke_user_sessions(db_session, user.id)
    assert db_session.scalar(select(func.count(AuthSession.id)).where(
        AuthSession.user_id == user.id, AuthSession.revoked_at.is_(None)
    )) == 0
    revoke_user_sessions(db_session, user.id)
    assert db_session.scalar(select(func.count(AuthSession.id))) == 2


def test_database_rate_limit_returns_retry_after(db_session):
    enforce_rate_limit(db_session, "unit-test:identity", limit=1, window_seconds=60)
    with pytest.raises(HTTPException) as exc:
        enforce_rate_limit(db_session, "unit-test:identity", limit=1, window_seconds=60)
    assert exc.value.status_code == 429
    assert int(exc.value.headers["Retry-After"]) in range(1, 61)
    assert db_session.query(RateLimitWindow).count() == 1


def test_production_catalog_scope_only_exposes_math_reasoning_and_science(client, db_session):
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(settings, "BETA_CATALOG_SCOPE", True)
    try:
        exam = Exam(name="SSC", slug="ssc", is_active=True)
        db_session.add(exam)
        db_session.flush()
        subjects_by_slug = {}
        for slug, name in (("maths", "Maths"), ("reasoning", "Reasoning"), ("gk-gs", "GK / GS"), ("english", "English")):
            subject = Subject(exam_id=exam.id, name=name, slug=slug, is_active=True)
            db_session.add(subject)
            db_session.flush()
            subjects_by_slug[slug] = subject
        science = Subcategory(subject_id=subjects_by_slug["gk-gs"].id, name="Science", slug="science", is_active=True)
        computer = Subcategory(subject_id=subjects_by_slug["gk-gs"].id, name="Computer", slug="computer", is_active=True)
        db_session.add_all([science, computer])
        db_session.flush()
        science_chapter = Chapter(subject_id=science.subject_id, subcategory_id=science.id, name="Cell", slug="cell", is_active=True)
        computer_chapter = Chapter(subject_id=computer.subject_id, subcategory_id=computer.id, name="Basics", slug="basics", is_active=True)
        english_chapter = Chapter(subject_id=subjects_by_slug["english"].id, name="Parts of Speech", slug="parts-of-speech", is_active=True)
        db_session.add_all([science_chapter, computer_chapter, english_chapter])
        user = _user(db_session, "scope-student@example.test")
        db_session.commit()
        token = create_access_token(user.id)
        assert [item.slug for item in list_active_exams(db_session)] == ["ssc"]
        assert {item.slug for item in list_active_subjects(db_session, exam.id)} == {
            "maths", "reasoning", "gk-gs"
        }
        assert [item.slug for item in list_active_subcategories(db_session, science.subject_id)] == ["science"]
        assert [item.slug for item in list_active_chapters_for_selection(db_session, science.subject_id)] == ["cell"]

        response = client.post(
            "/api/tests",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "exam_id": str(exam.id),
                "subject_id": str(subjects_by_slug["english"].id),
                "test_type": "CHAPTER_WISE",
                "chapter_id": str(english_chapter.id),
                "difficulty": None,
                "question_count": 10,
            },
        )
        assert response.status_code == 404
    finally:
        monkeypatch.undo()


def test_beta_chapter_scope_is_disabled_outside_production():
    monkeypatch = pytest.MonkeyPatch()
    try:
        monkeypatch.setattr(settings, "BETA_CATALOG_SCOPE", False)
        assert chapter_is_in_beta("ssc", "gk-gs", None)
        monkeypatch.setattr(settings, "BETA_CATALOG_SCOPE", True)
        assert chapter_is_in_beta("ssc", "gk-gs", "science")
        assert not chapter_is_in_beta("ssc", "gk-gs", None)
    finally:
        monkeypatch.undo()


@pytest.mark.parametrize("exam_slug", ["banking-po", "banking-clerk", "banking-others"])
def test_banking_scope_allows_only_configured_subjects(exam_slug):
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(settings, "BETA_CATALOG_SCOPE", True)
    try:
        from app.database.banking_catalog import BANKING_SUBJECTS

        allowed_subjects = {subject_slug for _, subject_slug, _ in BANKING_SUBJECTS}
        assert all(subject_is_in_beta(exam_slug, slug) for slug in allowed_subjects)
        assert not subject_is_in_beta(exam_slug, "unlisted-internal-subject")
        assert not subject_is_in_beta(exam_slug, "gk-gs")
    finally:
        monkeypatch.undo()


def test_direct_banking_catalog_and_test_selection_reject_unlisted_subject(db_session):
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(settings, "BETA_CATALOG_SCOPE", True)
    try:
        from app.routers.catalog import (
            get_availability,
            get_chapters,
            get_subcategories,
            get_subject_chapter_counts,
        )
        from app.schemas.catalog import PracticeLevel
        from app.services.test_service import _selection

        exam = Exam(name="Banking Clerk", slug="banking-clerk", is_active=True)
        db_session.add(exam)
        db_session.flush()
        subject = Subject(
            exam_id=exam.id,
            name="Unlisted internal subject",
            slug="unlisted-internal-subject",
            is_active=True,
        )
        db_session.add(subject)
        db_session.flush()
        chapter = Chapter(
            subject_id=subject.id, name="Internal chapter", slug="internal-chapter", is_active=True
        )
        db_session.add(chapter)
        db_session.commit()

        for endpoint_call in (
            lambda: get_subcategories(subject.id, db_session),
            lambda: get_chapters(subject.id, None, db_session),
            lambda: get_subject_chapter_counts(subject.id, db_session),
            lambda: get_availability(chapter.id, PracticeLevel.EASY, None, db_session),
        ):
            with pytest.raises(HTTPException) as exc:
                endpoint_call()
            assert exc.value.status_code == 404

        with pytest.raises(HTTPException) as exc:
            _selection(db_session, exam.id, subject.id, "CHAPTER_WISE", chapter.id, None, None)
        assert exc.value.status_code == 404
    finally:
        monkeypatch.undo()


@pytest.mark.parametrize("origin", [
    "*",
    "https://example.com/path",
    "https://user@example.com",
    "https://example.com?redirect=elsewhere",
    "https://*.example.com",
    "https://example.com:bad",
    "http://example.com",
    "https://localhost",
])
def test_production_cors_requires_exact_https_origin(origin):
    with pytest.raises(ValidationError):
        Settings(
            _env_file=None,
            ENVIRONMENT="production",
            SECRET_KEY="test-secret-key-that-is-long-enough-for-production",
            DATABASE_URL="postgresql+psycopg://app:password@db.example.net:5432/ssc?sslmode=verify-full",
            CORS_ORIGINS=[origin],
            BETA_CATALOG_SCOPE=True,
        )


def test_production_google_config_must_be_complete():
    base = dict(
        _env_file=None,
        ENVIRONMENT="production",
        SECRET_KEY="test-secret-key-that-is-long-enough-for-production",
        DATABASE_URL="postgresql+psycopg://app:password@db.example.net:5432/ssc?sslmode=verify-full",
        CORS_ORIGINS=["https://prep.example.com"],
        BETA_CATALOG_SCOPE=True,
    )
    with pytest.raises(ValidationError):
        Settings(**base, GOOGLE_CLIENT_ID="client.apps.googleusercontent.com")
    with pytest.raises(ValidationError):
        Settings(
            **base,
            GOOGLE_CLIENT_ID="client.apps.googleusercontent.com",
            GOOGLE_CLIENT_SECRET="secret",
            GOOGLE_REDIRECT_URI="http://api.example.com/api/auth/google/callback",
        )
    with pytest.raises(ValidationError):
        Settings(
            **base,
            GOOGLE_CLIENT_ID="client.apps.googleusercontent.com",
            GOOGLE_CLIENT_SECRET="secret",
            GOOGLE_REDIRECT_URI="https://api.example.com/wrong/callback",
        )


def test_production_email_provider_requires_complete_smtp_config():
    base = dict(
        _env_file=None,
        ENVIRONMENT="production",
        SECRET_KEY="test-secret-key-that-is-long-enough-for-production",
        DATABASE_URL="postgresql+psycopg://app:password@db.example.net:5432/ssc?sslmode=verify-full",
        CORS_ORIGINS=["https://prep.example.com"],
        BETA_CATALOG_SCOPE=True,
        EMAIL_PROVIDER="smtp",
    )
    with pytest.raises(ValidationError):
        Settings(**base, SMTP_HOST="smtp.example.com")
