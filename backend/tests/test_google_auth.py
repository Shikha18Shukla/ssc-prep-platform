"""Google OAuth authorization-code flow tests.

All provider calls are stubbed: no real Google credentials, tokens, network
requests, or client secrets are used. These tests verify state/cookie binding,
PKCE, signed ID-token checks, verified-email enforcement, account linking, and
single-use callback exchange.
"""

from datetime import datetime, timedelta, timezone
from urllib.parse import parse_qs, urlsplit
import base64

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.auth.security import sha256_hex
from app.config import settings
from app.models import OAuthExchangeCode, OAuthIdentity, OAuthState, User
from app.services import google_auth_service as google_service


REDIRECT_URI = "http://testserver/api/auth/google/callback"
CLIENT_ID = "client-id.apps.googleusercontent.com"
PROVIDER_CONTEXT: dict[str, str] = {"nonce": "test-nonce"}


class StubResponse:
    def __init__(self, payload: dict) -> None:
        self._payload = payload
        self.status_code = 200

    def json(self) -> dict:
        return self._payload

    def raise_for_status(self) -> None:
        return None


@pytest.fixture
def google_config(monkeypatch):
    monkeypatch.setattr(settings, "GOOGLE_CLIENT_ID", CLIENT_ID)
    monkeypatch.setattr(settings, "GOOGLE_CLIENT_SECRET", "server-side-secret")
    monkeypatch.setattr(settings, "GOOGLE_REDIRECT_URI", REDIRECT_URI)
    monkeypatch.setattr(settings, "GOOGLE_SUCCESS_REDIRECT_URL", "/auth/google/complete")
    monkeypatch.setattr(settings, "GOOGLE_COOKIE_SECURE", False)
    monkeypatch.setattr(settings, "GOOGLE_COOKIE_SAMESITE", "lax")
    # Each test generates a fresh RSA key; do not reuse another test's JWKS.
    google_service._jwks_cache = None
    PROVIDER_CONTEXT["nonce"] = "test-nonce"
    yield settings
    google_service._jwks_cache = None
    PROVIDER_CONTEXT["nonce"] = "test-nonce"


@pytest.fixture
def google_identity():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    numbers = private_key.public_key().public_numbers()

    def encode_int(value: int) -> str:
        return base64.urlsafe_b64encode(
            value.to_bytes((value.bit_length() + 7) // 8, "big")
        ).decode("ascii").rstrip("=")

    jwk = {
        "kty": "RSA",
        "kid": "test-key",
        "use": "sig",
        "alg": "RS256",
        "n": encode_int(numbers.n),
        "e": encode_int(numbers.e),
    }
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    def make_token(**overrides) -> str:
        kid = overrides.pop("_kid", "test-key")
        now = datetime.now(timezone.utc)
        claims = {
            "sub": "google-stable-subject-1",
            "email": "google.student@example.com",
            "email_verified": True,
            "name": "Google Student",
            "iss": "https://accounts.google.com",
            "aud": CLIENT_ID,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=5)).timestamp()),
            "nonce": PROVIDER_CONTEXT["nonce"],
        }
        claims.update(overrides)
        return jwt.encode(claims, pem, algorithm="RS256", headers={"kid": kid})

    return jwk, make_token


def _stub_provider(monkeypatch, jwk: dict, id_token, captured: dict | None = None):
    def fake_get(url, timeout):
        assert url == google_service.GOOGLE_JWKS_URL
        return StubResponse({"keys": [jwk]})

    def fake_post(url, data, timeout):
        assert url == google_service.GOOGLE_TOKEN_URL
        assert data["grant_type"] == "authorization_code"
        assert data["client_id"] == CLIENT_ID
        assert data["client_secret"] == settings.GOOGLE_CLIENT_SECRET
        assert data["redirect_uri"] == REDIRECT_URI
        assert data["code_verifier"]
        if captured is not None:
            captured.update(data)
        token = id_token() if callable(id_token) else id_token
        return StubResponse({"id_token": token})

    monkeypatch.setattr(google_service.httpx, "get", fake_get)
    monkeypatch.setattr(google_service.httpx, "post", fake_post)


def _start_params(url: str) -> dict[str, str]:
    return {key: values[0] for key, values in parse_qs(urlsplit(url).query).items()}


# ---------------------------------------------------------------------------
# Authorization request construction
# ---------------------------------------------------------------------------

def test_authorization_request_uses_state_nonce_and_pkce(db_session, google_config):
    url, browser_key = google_service.build_authorization_url(db_session)
    params = _start_params(url)

    assert url.startswith(google_service.GOOGLE_AUTH_URL)
    assert params["response_type"] == "code"
    assert params["client_id"] == CLIENT_ID
    assert params["redirect_uri"] == REDIRECT_URI
    assert params["scope"] == google_service.GOOGLE_SCOPES
    assert params["code_challenge_method"] == "S256"
    assert len(params["state"]) >= 32
    assert len(params["nonce"]) >= 32
    assert len(params["code_challenge"]) >= 40
    assert "client_secret" not in params
    assert "access_token" not in params

    state = db_session.scalar(select(OAuthState))
    assert state is not None
    assert state.state_hash == sha256_hex(params["state"])
    assert state.browser_key_hash == sha256_hex(browser_key)
    assert state.nonce_hash == sha256_hex(params["nonce"])
    assert state.redirect_uri == REDIRECT_URI
    assert state.code_verifier not in url


def test_google_not_configured_returns_safe_error(client: TestClient, monkeypatch):
    monkeypatch.setattr(settings, "GOOGLE_CLIENT_ID", None)
    monkeypatch.setattr(settings, "GOOGLE_CLIENT_SECRET", None)
    monkeypatch.setattr(settings, "GOOGLE_REDIRECT_URI", None)
    response = client.get("/api/auth/google/start")
    assert response.status_code == 503
    assert "not configured" in response.json()["detail"].lower()


def test_oauth_cookie_outlives_state_and_exchange_code(client: TestClient, google_config):
    response = client.get("/api/auth/google/start")
    assert response.status_code == 200
    set_cookie = response.headers["set-cookie"].lower()
    expected = settings.GOOGLE_STATE_TTL_SECONDS + settings.GOOGLE_EXCHANGE_TTL_SECONDS
    assert f"max-age={expected}" in set_cookie


# ---------------------------------------------------------------------------
# ID-token verification
# ---------------------------------------------------------------------------

def test_id_token_verification_accepts_signed_claims(monkeypatch, google_config, google_identity):
    jwk, make_token = google_identity
    _stub_provider(monkeypatch, jwk, make_token())
    token = make_token()
    claims = google_service.verify_google_id_token(token, sha256_hex("test-nonce"))
    assert claims["sub"] == "google-stable-subject-1"
    assert claims["email"] == "google.student@example.com"


def test_id_token_verification_rejects_bad_nonce_email_issuer_and_audience(
    monkeypatch, google_config, google_identity
):
    jwk, make_token = google_identity
    valid_token = make_token()
    tampered = valid_token[:-1] + ("A" if valid_token[-1] != "A" else "B")

    cases = [
        (valid_token, sha256_hex("wrong-nonce"), None),
        (make_token(email_verified=False), sha256_hex("test-nonce"), "verified"),
        (make_token(iss="https://evil.example.com"), sha256_hex("test-nonce"), None),
        (make_token(aud="another-client"), sha256_hex("test-nonce"), None),
        (make_token(nonce=None), sha256_hex("test-nonce"), None),
        (tampered, sha256_hex("test-nonce"), None),
        (make_token(_kid="unknown-key"), sha256_hex("test-nonce"), None),
    ]
    for token, nonce_hash, expected_detail in cases:
        _stub_provider(monkeypatch, jwk, token)
        with pytest.raises(google_service.GoogleAuthError) as exc:
            google_service.verify_google_id_token(token, nonce_hash)
        if expected_detail:
            assert expected_detail in exc.value.detail


def test_callback_rejects_runtime_redirect_uri_change(
    db_session, monkeypatch, google_config, google_identity
):
    jwk, make_token = google_identity
    _stub_provider(monkeypatch, jwk, make_token())
    authorization_url, browser_key = google_service.build_authorization_url(db_session)
    state = _start_params(authorization_url)["state"]
    monkeypatch.setattr(
        settings,
        "GOOGLE_REDIRECT_URI",
        "http://testserver/api/auth/google/callback-changed",
    )

    with pytest.raises(google_service.GoogleAuthError):
        google_service.complete_google_callback(db_session, "provider-code", state, browser_key)


# ---------------------------------------------------------------------------
# Account creation and linking
# ---------------------------------------------------------------------------

def test_google_user_creation_and_existing_identity_login(db_session, google_config):
    claims = {
        "sub": "google-stable-subject-1",
        "email": "google.student@example.com",
        "email_verified": True,
        "name": "Google Student",
    }
    first = google_service.link_or_create_user(db_session, claims)
    assert first.password_hash is None
    assert first.has_password is False
    assert first.email_normalized == "google.student@example.com"

    second = google_service.link_or_create_user(db_session, claims)
    assert second.id == first.id
    assert db_session.scalar(select(func.count(User.id))) == 1
    identity = db_session.scalar(select(OAuthIdentity))
    assert identity.provider == "google"
    assert identity.provider_user_id == claims["sub"]
    assert identity.email_verified is True


def test_google_links_existing_password_account_by_verified_email(db_session, google_config):
    from app.auth.security import hash_password

    existing = User(
        email="existing.student@example.com",
        full_name="Existing Student",
        password_hash=hash_password("Password123"),
    )
    db_session.add(existing)
    db_session.commit()

    linked = google_service.link_or_create_user(db_session, {
        "sub": "google-stable-subject-2",
        "email": " EXISTING.STUDENT@EXAMPLE.COM ",
        "email_verified": True,
    })
    assert linked.id == existing.id
    assert linked.has_password is True
    assert db_session.scalar(select(func.count(User.id))) == 1
    assert db_session.scalar(select(func.count(OAuthIdentity.id))) == 1


def test_concurrent_google_signup_same_email_recovers_without_server_error(
    db_session, google_config, monkeypatch
):
    existing = User(
        email="race.student@example.com",
        full_name="Race Student",
        password_hash=None,
        is_active=True,
    )
    db_session.add(existing)
    db_session.commit()

    original_lookup = google_service._user_by_email
    calls = {"count": 0}

    def first_lookup_misses(db, email):
        calls["count"] += 1
        if calls["count"] == 1:
            return None
        return original_lookup(db, email)

    monkeypatch.setattr(google_service, "_user_by_email", first_lookup_misses)
    linked = google_service.link_or_create_user(db_session, {
        "sub": "google-race-subject",
        "email": "RACE.STUDENT@EXAMPLE.COM",
        "email_verified": True,
    })
    assert linked.id == existing.id
    assert db_session.scalar(select(func.count(User.id))) == 1
    identity = db_session.scalar(select(OAuthIdentity))
    assert identity.provider_user_id == "google-race-subject"
    assert identity.user_id == existing.id


def test_unverified_email_cannot_create_or_link(db_session, google_config):
    with pytest.raises(google_service.GoogleAuthError):
        google_service.link_or_create_user(db_session, {
            "sub": "unverified-subject",
            "email": "unverified@example.com",
            "email_verified": False,
        })
    assert db_session.scalar(select(func.count(User.id))) == 0


# ---------------------------------------------------------------------------
# Callback and exchange codes
# ---------------------------------------------------------------------------

def test_callback_and_exchange_are_single_use_and_browser_bound(
    db_session, monkeypatch, google_config, google_identity
):
    jwk, make_token = google_identity
    _stub_provider(monkeypatch, jwk, lambda: make_token())

    authorization_url, browser_key = google_service.build_authorization_url(db_session)
    start_params = _start_params(authorization_url)
    state = start_params["state"]
    PROVIDER_CONTEXT["nonce"] = start_params["nonce"]

    exchange_code = google_service.complete_google_callback(
        db_session, "one-time-google-code", state, browser_key
    )
    assert len(exchange_code) >= 32
    record = db_session.scalar(select(OAuthExchangeCode))
    assert record.code_hash == sha256_hex(exchange_code)
    assert exchange_code not in record.code_hash

    with pytest.raises(google_service.GoogleAuthError):
        google_service.complete_google_callback(
            db_session, "replayed-google-code", state, browser_key
        )

    with pytest.raises(google_service.GoogleAuthError):
        google_service.exchange_google_code(db_session, exchange_code, "wrong-browser-key")

    token, user = google_service.exchange_google_code(db_session, exchange_code, browser_key)
    assert token
    assert user.email == "google.student@example.com"
    with pytest.raises(google_service.GoogleAuthError):
        google_service.exchange_google_code(db_session, exchange_code, browser_key)


def test_google_flow_end_to_end_has_no_token_in_redirect(
    client: TestClient, db_session, monkeypatch, google_config, google_identity
):
    jwk, make_token = google_identity
    captured: dict = {}
    _stub_provider(monkeypatch, jwk, lambda: make_token(), captured)

    start = client.get("/api/auth/google/start")
    assert start.status_code == 200
    params = _start_params(start.json()["authorization_url"])
    PROVIDER_CONTEXT["nonce"] = params["nonce"]
    assert google_service.GOOGLE_COOKIE_NAME in client.cookies

    callback = client.get(
        "/api/auth/google/callback",
        params={"code": "provider-code", "state": params["state"]},
        follow_redirects=False,
    )
    assert callback.status_code == 303
    location = callback.headers["location"]
    assert "access_token" not in location
    assert "id_token" not in location
    assert "client_secret" not in location
    query = parse_qs(urlsplit(location).query)
    assert "code" in query
    assert "error" not in query

    exchanged = client.post("/api/auth/google/exchange", json={"code": query["code"][0]})
    assert exchanged.status_code == 200
    token = exchanged.json()["access_token"]
    assert exchanged.json()["user"]["has_password"] is False
    profile = client.get(
        "/api/auth/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert profile.status_code == 200
    assert db_session.scalar(select(func.count(User.id))) == 1
    assert captured["code"] == "provider-code"
    assert captured["grant_type"] == "authorization_code"

    replay = client.post("/api/auth/google/exchange", json={"code": query["code"][0]})
    assert replay.status_code == 401


def test_callback_without_matching_cookie_is_rejected(
    client: TestClient, monkeypatch, google_config, google_identity
):
    jwk, make_token = google_identity
    _stub_provider(monkeypatch, jwk, make_token())
    start = client.get("/api/auth/google/start")
    state = _start_params(start.json()["authorization_url"])["state"]
    client.cookies.clear()

    callback = client.get(
        "/api/auth/google/callback",
        params={"code": "provider-code", "state": state},
        follow_redirects=False,
    )
    assert callback.status_code == 303
    assert "error=google_signin_failed" in callback.headers["location"]
    assert "code=" not in callback.headers["location"]
