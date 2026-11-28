"""Server-side Google OAuth 2.0 authorization-code flow.

The frontend never supplies an identity, email, ID token, access token, client
secret, or redirect URI. It only follows the backend-generated authorization
URL and posts back the short-lived opaque exchange code created after the
callback has verified Google's signed ID token.
"""

from datetime import datetime, timedelta, timezone
import logging
import re
import threading
import time
from typing import Any
from urllib.parse import urlencode

import httpx
from jose import JWTError, jwt
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.security import (
    create_access_token,
    create_pkce_pair,
    decode_access_token,
    secure_url_token,
    sha256_hex,
    tokens_equal,
)
from app.config import settings
from app.models import AuthSession, OAuthExchangeCode, OAuthIdentity, OAuthState, User

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_JWKS_URL = "https://www.googleapis.com/oauth2/v3/certs"
GOOGLE_ISSUERS = frozenset({"accounts.google.com", "https://accounts.google.com"})
GOOGLE_COOKIE_NAME = "ssc_google_oauth"
GOOGLE_SCOPES = "openid email profile"

logger = logging.getLogger("ssc_prep.google_oauth")
_OPAQUE_VALUE_RE = re.compile(r"[A-Za-z0-9_-]{32,}")
_CONTROL_CHAR_RE = re.compile(r"[\x00-\x1f\x7f]")
_SENSITIVE_ASSIGNMENT_RE = re.compile(
    r"(?i)\b(client_secret|code|id_token|access_token|refresh_token|"
    r"state|nonce|code_verifier|redirect_uri|assertion)\s*=\s*[^\s,;]+"
)


def _sanitize_provider_error(value: object, limit: int = 200) -> str | None:
    """Reduce a provider error to a short, non-sensitive log value."""
    if not isinstance(value, str):
        return None
    cleaned = _CONTROL_CHAR_RE.sub(" ", value)
    cleaned = _SENSITIVE_ASSIGNMENT_RE.sub(
        lambda match: f"{match.group(1)}=[REDACTED]", cleaned
    )
    cleaned = _OPAQUE_VALUE_RE.sub("[REDACTED]", cleaned)
    cleaned = " ".join(cleaned.split())
    return cleaned[:limit] or None


def _log_token_response(response: Any, *, id_token_present: bool) -> None:
    """Log only safe metadata from Google's token endpoint."""
    payload = None
    try:
        payload = response.json()
    except Exception:
        pass
    error_code = None
    error_description = None
    if isinstance(payload, dict):
        error_code = _sanitize_provider_error(payload.get("error"), limit=80)
        error_description = _sanitize_provider_error(
            payload.get("error_description"), limit=200
        )
    logger.warning(
        "Google token endpoint status=%s google_error=%s "
        "google_error_description=%s id_token_present=%s",
        response.status_code,
        error_code or "-",
        error_description or "-",
        id_token_present,
    )


_jwks_cache: tuple[float, list[dict[str, Any]]] | None = None
_jwks_lock = threading.Lock()


class GoogleAuthError(Exception):
    """Safe, non-sensitive OAuth failure with an API status code."""

    def __init__(self, detail: str = "Google sign-in could not be completed", status_code: int = 401):
        super().__init__(detail)
        self.detail = detail
        self.status_code = status_code


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _as_utc(value: datetime) -> datetime:
    return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value


def _google_config() -> tuple[str, str, str]:
    if not settings.google_is_configured():
        raise GoogleAuthError("Google sign-in is not configured", 503)
    return (
        settings.GOOGLE_CLIENT_ID or "",
        settings.GOOGLE_CLIENT_SECRET or "",
        settings.GOOGLE_REDIRECT_URI or "",
    )


def _user_by_email(db: Session, email: str) -> User | None:
    return db.execute(
        select(User).where(User.email_normalized == email.strip().lower())
    ).scalar_one_or_none()


def build_authorization_url(db: Session) -> tuple[str, str]:
    """Persist single-use OAuth state and return `(authorization_url, browser_key)`."""
    client_id, _, redirect_uri = _google_config()
    state = secure_url_token(32)
    nonce = secure_url_token(32)
    browser_key = secure_url_token(32)
    code_verifier, code_challenge = create_pkce_pair()

    db.add(OAuthState(
        state_hash=sha256_hex(state),
        browser_key_hash=sha256_hex(browser_key),
        nonce_hash=sha256_hex(nonce),
        code_verifier=code_verifier,
        redirect_uri=redirect_uri,
        expires_at=_now() + timedelta(seconds=settings.GOOGLE_STATE_TTL_SECONDS),
    ))
    db.commit()

    query = urlencode({
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": GOOGLE_SCOPES,
        "state": state,
        "nonce": nonce,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "access_type": "online",
        "prompt": "select_account",
    })
    return f"{GOOGLE_AUTH_URL}?{query}", browser_key


def _consume_state(db: Session, state: str, browser_key: str) -> OAuthState:
    state_hash = sha256_hex(state)
    browser_hash = sha256_hex(browser_key)
    query = select(OAuthState).where(OAuthState.state_hash == state_hash)
    if db.bind.dialect.name == "postgresql":
        query = query.with_for_update()
    record = db.execute(query).scalar_one_or_none()

    invalid = GoogleAuthError("Invalid or expired Google sign-in state")
    if (
        record is None
        or record.used_at is not None
        or _as_utc(record.expires_at) <= _now()
        or not tokens_equal(record.browser_key_hash, browser_hash)
        or record.redirect_uri != (settings.GOOGLE_REDIRECT_URI or "")
    ):
        raise invalid

    record.used_at = _now()
    db.commit()
    return record


def fetch_google_jwks() -> list[dict[str, Any]]:
    """Fetch and briefly cache Google's public signing keys."""
    global _jwks_cache
    current = time.monotonic()
    if _jwks_cache is not None and current - _jwks_cache[0] < 3600:
        return _jwks_cache[1]
    with _jwks_lock:
        if _jwks_cache is not None and time.monotonic() - _jwks_cache[0] < 3600:
            return _jwks_cache[1]
        try:
            response = httpx.get(GOOGLE_JWKS_URL, timeout=10)
            response.raise_for_status()
            keys = response.json().get("keys")
        except Exception as exc:
            status = getattr(getattr(exc, "response", None), "status_code", None)
            logger.warning(
                "Google JWKS fetch failed exception=%s status=%s",
                type(exc).__name__,
                status if status is not None else "-",
            )
            raise GoogleAuthError("Google sign-in is temporarily unavailable", 503) from None
        if not isinstance(keys, list) or not keys:
            logger.warning("Google JWKS response contained no usable keys")
            raise GoogleAuthError("Google sign-in is temporarily unavailable", 503)
        _jwks_cache = (time.monotonic(), keys)
        return keys


def exchange_authorization_code(
    code: str, code_verifier: str, redirect_uri: str
) -> tuple[str, str | None]:
    """Return the ID token and access token; the latter is used only for at_hash."""
    client_id, client_secret, configured_redirect = _google_config()
    if redirect_uri != configured_redirect:
        raise GoogleAuthError("Invalid Google sign-in redirect")
    try:
        response = httpx.post(
            GOOGLE_TOKEN_URL,
            data={
                "code": code,
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code",
                "code_verifier": code_verifier,
            },
            timeout=10,
        )
    except Exception as exc:
        logger.warning("Google token request failed before response exception=%s", type(exc).__name__)
        raise GoogleAuthError() from None

    try:
        payload = response.json()
    except Exception:
        payload = None
    id_token = payload.get("id_token") if isinstance(payload, dict) else None
    id_token_present = isinstance(id_token, str) and bool(id_token)
    _log_token_response(response, id_token_present=id_token_present)

    if response.status_code >= 400:
        raise GoogleAuthError()
    if not id_token_present:
        raise GoogleAuthError()

    access_token = payload.get("access_token") if isinstance(payload, dict) else None
    if not isinstance(access_token, str) or not access_token:
        access_token = None
    return id_token, access_token


def verify_google_id_token(
    id_token: str,
    expected_nonce_hash: str,
    access_token: str | None = None,
) -> dict[str, Any]:
    """Verify Google signature and claims; access_token is used only for at_hash."""
    client_id, _, _ = _google_config()

    def reject(
        stage: str,
        detail: str = "Google sign-in could not be completed",
        status_code: int = 401,
        exc: Exception | None = None,
    ) -> None:
        if exc is None:
            logger.warning("Google ID token rejected at stage=%s", stage)
        else:
            reason = _sanitize_provider_error(str(exc), limit=200) or "-"
            logger.warning(
                "Google ID token rejected at stage=%s exception=%s reason=%s",
                stage,
                type(exc).__name__,
                reason,
            )
        raise GoogleAuthError(detail, status_code)

    try:
        header = jwt.get_unverified_header(id_token)
        unverified = jwt.get_unverified_claims(id_token)
    except JWTError as exc:
        reject("token_parse", exc=exc)

    issuer = unverified.get("iss")
    if issuer not in GOOGLE_ISSUERS:
        reject("issuer")
    key_id = header.get("kid")
    signing_key = next(
        (key for key in fetch_google_jwks() if key.get("kid") == key_id),
        None,
    )
    if signing_key is None:
        reject("jwks_kid")

    try:
        claims = jwt.decode(
            id_token,
            signing_key,
            algorithms=["RS256"],
            audience=client_id,
            issuer=issuer,
            access_token=access_token,
            options={"require": ["sub", "email", "email_verified", "exp", "iat", "iss", "aud"]},
        )
    except JWTError as exc:
        reject("signature_or_claims", exc=exc)

    audience = claims.get("aud")
    authorized_party = claims.get("azp")
    if isinstance(audience, str):
        audience_matches = audience == client_id
    elif isinstance(audience, list):
        audience_matches = client_id in audience
    else:
        audience_matches = False
    if not audience_matches:
        reject("audience")
    if authorized_party is not None and authorized_party != client_id:
        reject("authorized_party")
    if isinstance(audience, list) and authorized_party is None:
        reject("authorized_party")

    nonce = claims.get("nonce")
    if not isinstance(nonce, str) or not tokens_equal(sha256_hex(nonce), expected_nonce_hash):
        reject("nonce")
    if claims.get("email_verified") is not True:
        reject("email_verified", "A verified Google email address is required", 403)
    if not isinstance(claims.get("sub"), str) or not claims["sub"]:
        reject("subject")
    return claims


def link_or_create_user(db: Session, claims: dict[str, Any]) -> User:
    """Create a Google user or link a verified identity to an existing user."""
    provider_user_id = claims["sub"]
    email = str(claims["email"]).strip().lower()
    identity = db.execute(
        select(OAuthIdentity).where(
            OAuthIdentity.provider == "google",
            OAuthIdentity.provider_user_id == provider_user_id,
        )
    ).scalar_one_or_none()

    if identity is not None:
        user = db.get(User, identity.user_id)
        if user is None or not user.is_active:
            raise GoogleAuthError("This account is not available", 403)
        return user

    if claims.get("email_verified") is not True:
        raise GoogleAuthError("A verified Google email address is required", 403)

    user = _user_by_email(db, email)
    if user is None:
        name = str(claims.get("name") or "").strip()[:255] or None
        user = User(
            email=email,
            full_name=name,
            password_hash=None,
            password_changed_at=None,
            is_active=True,
        )
    elif not user.is_active:
        raise GoogleAuthError("This account is not available", 403)

    identity_values = dict(
        provider="google",
        provider_user_id=provider_user_id,
        provider_email=email,
        email_verified=True,
    )

    def identity_by_subject() -> OAuthIdentity | None:
        return db.execute(
            select(OAuthIdentity).where(
                OAuthIdentity.provider == "google",
                OAuthIdentity.provider_user_id == provider_user_id,
            )
        ).scalar_one_or_none()

    try:
        # Both the user insert and identity insert can race, so keep them in
        # the same guarded transaction instead of flushing the user first.
        db.add(user)
        db.flush()
        db.add(OAuthIdentity(user_id=user.id, **identity_values))
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError as exc:
        db.rollback()
        # A concurrent request may have created the identity or claimed the
        # verified email first. Recover by identity, then by email; never turn
        # a normal concurrency conflict into a raw 500.
        identity = identity_by_subject()
        if identity is not None:
            linked = db.get(User, identity.user_id)
            if linked is not None and linked.is_active:
                return linked

        existing = _user_by_email(db, email)
        if existing is None or not existing.is_active:
            raise GoogleAuthError() from None

        user = existing
        has_google_identity = db.scalar(
            select(OAuthIdentity.id).where(
                OAuthIdentity.user_id == existing.id,
                OAuthIdentity.provider == "google",
            )
        ) is not None
        if not has_google_identity:
            db.add(OAuthIdentity(user_id=existing.id, **identity_values))
            try:
                db.commit()
            except IntegrityError:
                db.rollback()
                identity = identity_by_subject()
                linked = db.get(User, identity.user_id) if identity is not None else None
                if linked is not None and linked.is_active:
                    return linked
                raise GoogleAuthError() from None
        db.refresh(user)
        return user
    except Exception:
        db.rollback()
        raise


def complete_google_callback(
    db: Session,
    code: str | None,
    state: str | None,
    browser_key: str | None,
) -> str:
    """Validate OAuth callback inputs and return an opaque exchange code."""
    if not code or not state or not browser_key:
        logger.warning("Google OAuth callback rejected at stage=input_validation")
        raise GoogleAuthError("Invalid Google sign-in callback")

    def log_failure(stage: str, exc: Exception) -> None:
        logger.warning(
            "Google OAuth callback failed at stage=%s exception=%s detail=%s",
            stage,
            type(exc).__name__,
            getattr(exc, "detail", "-"),
        )

    try:
        record = _consume_state(db, state, browser_key)
    except Exception as exc:
        log_failure("state", exc)
        raise
    try:
        id_token, access_token = exchange_authorization_code(
            code, record.code_verifier, record.redirect_uri
        )
    except Exception as exc:
        log_failure("token_exchange", exc)
        raise
    try:
        claims = verify_google_id_token(id_token, record.nonce_hash, access_token)
    except Exception as exc:
        log_failure("id_token_verification", exc)
        raise
    try:
        user = link_or_create_user(db, claims)
    except Exception as exc:
        log_failure("user_link", exc)
        raise

    plaintext = secure_url_token(32)
    try:
        db.add(OAuthExchangeCode(
            code_hash=sha256_hex(plaintext),
            user_id=user.id,
            browser_key_hash=sha256_hex(browser_key),
            expires_at=_now() + timedelta(seconds=settings.GOOGLE_EXCHANGE_TTL_SECONDS),
        ))
        db.commit()
    except Exception as exc:
        db.rollback()
        log_failure("exchange_code", exc)
        raise
    return plaintext


def exchange_google_code(db: Session, code: str, browser_key: str | None) -> tuple[str, User]:
    """Consume the opaque callback code and issue a normal revocable session."""
    if not code or not browser_key:
        raise GoogleAuthError("Invalid Google sign-in exchange")
    code_hash = sha256_hex(code.strip())
    browser_hash = sha256_hex(browser_key)
    query = select(OAuthExchangeCode).where(OAuthExchangeCode.code_hash == code_hash)
    if db.bind.dialect.name == "postgresql":
        query = query.with_for_update()
    record = db.execute(query).scalar_one_or_none()

    invalid = GoogleAuthError("Invalid or expired Google sign-in exchange")
    if (
        record is None
        or record.used_at is not None
        or _as_utc(record.expires_at) <= _now()
        or not tokens_equal(record.browser_key_hash, browser_hash)
    ):
        raise invalid

    user = db.get(User, record.user_id)
    if user is None or not user.is_active:
        raise GoogleAuthError("This account is not available", 403)

    record.used_at = _now()
    token = create_access_token(user.id)
    payload = decode_access_token(token)
    expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    db.add(AuthSession(id=payload["jti"], user_id=user.id, expires_at=expires_at))
    db.commit()
    return token, user
