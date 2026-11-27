"""Authentication, session, and password recovery tests.

Covers password/Google-independent signup, normalized email uniqueness, Argon2id
verification, revocable JWT sessions, safe login errors, password setup/recovery
expiry and single use, and the no-email-provider contract.
"""

from datetime import datetime, timedelta, timezone
from urllib.parse import parse_qs, urlsplit
import uuid

import pytest
from fastapi.testclient import TestClient
from jose import JWTError, jwt
from sqlalchemy import func, select, update
from sqlalchemy.orm import Session

from app.auth.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from app.config import settings
from app.models import AuthSession, PasswordResetToken, User


REGISTER_PAYLOAD = {
    "full_name": "Aspirant Rahul",
    "email": "rahul.ssc@example.com",
    "password": "Password123",
    "confirm_password": "Password123",
}


def _register(client: TestClient, **overrides):
    payload = {**REGISTER_PAYLOAD, **overrides}
    return client.post("/api/auth/register", json=payload)


def _auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


class FakeEmailSender:
    """Captures generated reset URLs without sending real mail."""

    def __init__(self) -> None:
        self.messages: list[tuple[str, str]] = []

    def send_password_reset(self, to_email: str, reset_url: str) -> bool:
        self.messages.append((to_email, reset_url))
        return True


# ---------------------------------------------------------------------------
# Security utility tests
# ---------------------------------------------------------------------------

def test_password_hashing_and_verification():
    password = "SecurePassword123"
    hashed = hash_password(password)

    assert hashed != password
    assert hashed.startswith("$argon2id$")
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword123", hashed) is False
    assert verify_password("", hashed) is False


def test_jwt_contains_required_revocation_claims():
    user_id = uuid.uuid4()
    token = create_access_token(user_id)
    payload = decode_access_token(token)

    assert payload["sub"] == str(user_id)
    assert payload["iss"] == settings.JWT_ISSUER
    assert payload["aud"] == settings.JWT_AUDIENCE
    assert payload["type"] == "access"
    assert len(payload["jti"]) == 64
    assert "iat" in payload and "exp" in payload


def test_jwt_expired_token_is_rejected():
    token = create_access_token(uuid.uuid4(), expires_delta=timedelta(minutes=-10))
    with pytest.raises(JWTError):
        decode_access_token(token)


def test_jwt_invalid_token_is_rejected():
    with pytest.raises(JWTError):
        decode_access_token("not.a.valid.jwt.token")


def test_jwt_wrong_issuer_or_audience_is_rejected():
    now = datetime.now(timezone.utc)
    common = {
        "sub": str(uuid.uuid4()),
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=5)).timestamp()),
        "jti": "a" * 64,
        "type": "access",
    }
    wrong_issuer = jwt.encode(
        {**common, "iss": "attacker", "aud": settings.JWT_AUDIENCE},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    wrong_audience = jwt.encode(
        {**common, "iss": settings.JWT_ISSUER, "aud": "another-app"},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    with pytest.raises(JWTError):
        decode_access_token(wrong_issuer)
    with pytest.raises(JWTError):
        decode_access_token(wrong_audience)


# ---------------------------------------------------------------------------
# Signup tests
# ---------------------------------------------------------------------------

def test_successful_registration_issues_session_and_hides_secrets(client, db_session):
    response = _register(client)

    assert response.status_code == 201
    data = response.json()
    user = data["user"]
    assert user["email"] == REGISTER_PAYLOAD["email"]
    assert user["full_name"] == REGISTER_PAYLOAD["full_name"]
    assert user["is_active"] is True
    assert user["is_admin"] is False
    assert user["has_password"] is True
    assert "access_token" in data
    for forbidden in ("password", "password_hash", "confirm_password"):
        assert forbidden not in data
        assert forbidden not in user

    user = db_session.scalar(select(User).where(User.email == REGISTER_PAYLOAD["email"]))
    assert user is not None
    assert user.email_normalized == REGISTER_PAYLOAD["email"]
    assert user.password_hash.startswith("$argon2id$")
    assert user.password_hash != REGISTER_PAYLOAD["password"]
    assert verify_password(REGISTER_PAYLOAD["password"], user.password_hash)
    assert db_session.scalar(select(func.count(AuthSession.id))) == 1


def test_registration_never_accepts_admin_flag(client, db_session):
    response = _register(client, is_admin=True)
    assert response.status_code == 201
    assert response.json()["user"]["is_admin"] is False
    user = db_session.scalar(select(User).where(User.email == REGISTER_PAYLOAD["email"]))
    assert user.is_admin is False


def test_duplicate_email_is_rejected_after_normalization(client):
    first = _register(client, email="Mixed.Case@Example.COM")
    assert first.status_code == 201
    second = _register(
        client,
        email="mixed.case@example.com",
        password="OtherPassword456",
        confirm_password="OtherPassword456",
    )
    assert second.status_code == 409
    assert "already exists" in second.json()["detail"].lower()


def test_registration_validation_rules(client):
    blank_name = _register(client, full_name="   ")
    assert blank_name.status_code == 422

    mismatch = _register(client, confirm_password="Different123")
    assert mismatch.status_code == 422

    for weak in ("Pass1", "PasswordOnly", "1234567890"):
        response = _register(client, password=weak, confirm_password=weak)
        assert response.status_code == 422


def test_registration_email_is_normalized(client):
    response = _register(client, email="  USER.Caps@Example.COM  ")
    assert response.status_code == 201
    assert response.json()["user"]["email"] == "user.caps@example.com"


# ---------------------------------------------------------------------------
# Login, profile, and session tests
# ---------------------------------------------------------------------------

def test_successful_login(client):
    assert _register(client).status_code == 201
    response = client.post("/api/auth/login", json={
        "email": " RAHUL.SSC@EXAMPLE.COM ",
        "password": REGISTER_PAYLOAD["password"],
    })
    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == REGISTER_PAYLOAD["email"]
    assert "password_hash" not in data["user"]


def test_invalid_unknown_and_no_password_logins_are_uniform(client, db_session):
    assert _register(client).status_code == 201

    bad_password = client.post("/api/auth/login", json={
        "email": REGISTER_PAYLOAD["email"], "password": "WrongPassword999"
    })
    unknown = client.post("/api/auth/login", json={
        "email": "nobody@example.com", "password": "WrongPassword999"
    })
    db_session.add(User(email="provider-only@example.com", password_hash=None))
    db_session.commit()
    no_password = client.post("/api/auth/login", json={
        "email": "provider-only@example.com", "password": "WrongPassword999"
    })

    for response in (bad_password, unknown, no_password):
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid email or password"


def test_inactive_user_login_is_uniformly_rejected(client, db_session):
    db_session.add(User(
        email="inactive@example.com",
        full_name="Inactive User",
        password_hash=hash_password("Password123"),
        is_active=False,
    ))
    db_session.commit()
    response = client.post("/api/auth/login", json={
        "email": "inactive@example.com", "password": "Password123"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_me_accepts_only_valid_unrevoked_tokens(client):
    registered = _register(client)
    token = registered.json()["access_token"]
    response = client.get("/api/auth/me", headers=_auth_header(token))
    assert response.status_code == 200
    assert response.json()["id"] == registered.json()["user"]["id"]
    assert "password_hash" not in response.json()

    assert client.get("/api/auth/me").status_code in (401, 403)
    assert client.get("/api/auth/me", headers=_auth_header("forged.invalid.token")).status_code == 401

    user_id = registered.json()["user"]["id"]
    expired = create_access_token(user_id, expires_delta=timedelta(minutes=-30))
    assert client.get("/api/auth/me", headers=_auth_header(expired)).status_code == 401


def test_logout_revokes_only_the_current_session(client, db_session):
    registered = _register(client)
    token = registered.json()["access_token"]
    user_id = registered.json()["user"]["id"]

    login = client.post("/api/auth/login", json={
        "email": REGISTER_PAYLOAD["email"], "password": REGISTER_PAYLOAD["password"]
    })
    second_token = login.json()["access_token"]

    assert client.post("/api/auth/logout", headers=_auth_header(token)).status_code == 200
    assert client.get("/api/auth/me", headers=_auth_header(token)).status_code == 401
    assert client.get("/api/auth/me", headers=_auth_header(second_token)).status_code == 200
    assert db_session.scalar(select(func.count(AuthSession.id)).where(
        AuthSession.user_id == uuid.UUID(user_id), AuthSession.revoked_at.is_(None)
    )) == 1


# ---------------------------------------------------------------------------
# Password setup / recovery tests
# ---------------------------------------------------------------------------

def test_reset_request_without_email_provider_reports_unavailable(client, db_session, monkeypatch):
    monkeypatch.setattr(settings, "EMAIL_PROVIDER", "none")
    assert _register(client).status_code == 201

    response = client.post("/api/auth/password-reset/request", json={
        "email": REGISTER_PAYLOAD["email"]
    })
    assert response.status_code == 200
    message = response.json()["message"].lower()
    assert "not configured" in message or "unavailable" in message
    assert "sent" not in message
    assert db_session.scalar(select(func.count(PasswordResetToken.id))) == 0


def test_reset_request_does_not_suggest_unconfigured_google(client, monkeypatch):
    monkeypatch.setattr(settings, "EMAIL_PROVIDER", "none")
    monkeypatch.setattr(settings, "GOOGLE_CLIENT_ID", None)
    monkeypatch.setattr(settings, "GOOGLE_CLIENT_SECRET", None)
    monkeypatch.setattr(settings, "GOOGLE_REDIRECT_URI", None)

    response = client.post("/api/auth/password-reset/request", json={
        "email": REGISTER_PAYLOAD["email"]
    })
    assert response.status_code == 200
    message = response.json()["message"].lower()
    assert "google" not in message
    assert "contact an administrator" in message
    assert "sent" not in message


def test_reset_token_is_hashed_delivered_once_and_single_use(client, db_session, monkeypatch):
    sender = FakeEmailSender()
    monkeypatch.setattr(settings, "EMAIL_PROVIDER", "smtp")
    monkeypatch.setattr("app.services.auth_service.get_email_sender", lambda: sender)

    registered = _register(client)
    assert client.post("/api/auth/password-reset/request", json={
        "email": REGISTER_PAYLOAD["email"]
    }).status_code == 200

    assert len(sender.messages) == 1
    to_email, reset_url = sender.messages[0]
    assert to_email == REGISTER_PAYLOAD["email"]
    assert reset_url.startswith(settings.PASSWORD_RESET_URL)
    token = parse_qs(urlsplit(reset_url).query)["token"][0]

    record = db_session.scalar(select(PasswordResetToken))
    assert record is not None
    assert record.token_hash != token
    assert record.token_hash == __import__("hashlib").sha256(token.encode()).hexdigest()
    assert token not in str(record)
    assert record.used_at is None

    old_session = registered.json()["access_token"]
    confirm = client.post("/api/auth/password-reset/confirm", json={
        "token": token,
        "new_password": "BrandNewPassword123",
        "confirm_password": "BrandNewPassword123",
    })
    assert confirm.status_code == 200
    assert confirm.json()["user"]["has_password"] is True

    db_session.expire_all()
    user = db_session.scalar(select(User).where(User.email == REGISTER_PAYLOAD["email"]))
    assert verify_password("BrandNewPassword123", user.password_hash)
    assert db_session.scalar(select(PasswordResetToken.used_at)) is not None
    assert client.get("/api/auth/me", headers=_auth_header(old_session)).status_code == 401

    replay = client.post("/api/auth/password-reset/confirm", json={
        "token": token,
        "new_password": "AnotherPassword123",
        "confirm_password": "AnotherPassword123",
    })
    assert replay.status_code == 400


def test_reset_token_expiry_is_enforced(client, db_session, monkeypatch):
    sender = FakeEmailSender()
    monkeypatch.setattr(settings, "EMAIL_PROVIDER", "smtp")
    monkeypatch.setattr("app.services.auth_service.get_email_sender", lambda: sender)
    assert _register(client).status_code == 201
    assert client.post("/api/auth/password-reset/request", json={
        "email": REGISTER_PAYLOAD["email"]
    }).status_code == 200
    token = parse_qs(urlsplit(sender.messages[0][1]).query)["token"][0]

    db_session.execute(
        update(PasswordResetToken).values(
            expires_at=datetime.now(timezone.utc) - timedelta(seconds=1)
        )
    )
    db_session.commit()

    response = client.post("/api/auth/password-reset/confirm", json={
        "token": token,
        "new_password": "ExpiredPassword123",
        "confirm_password": "ExpiredPassword123",
    })
    assert response.status_code == 400
    assert db_session.scalar(select(PasswordResetToken.used_at)) is None


def test_reset_request_does_not_enumerate_unknown_emails(client, db_session, monkeypatch):
    sender = FakeEmailSender()
    monkeypatch.setattr(settings, "EMAIL_PROVIDER", "smtp")
    monkeypatch.setattr("app.services.auth_service.get_email_sender", lambda: sender)
    assert _register(client).status_code == 201

    known = client.post("/api/auth/password-reset/request", json={"email": REGISTER_PAYLOAD["email"]})
    unknown = client.post("/api/auth/password-reset/request", json={"email": "missing@example.com"})
    assert known.status_code == unknown.status_code == 200
    assert known.json() == unknown.json()
    assert len(sender.messages) == 1
