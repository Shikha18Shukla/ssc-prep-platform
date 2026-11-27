"""Password hashing, token helpers, and internal JWT validation.

Uses Argon2id for password hashing and python-jose for signed internal JWTs.
Never logs passwords or returns password hashes in API responses.
"""

from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import secrets
from typing import Any
import uuid

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError
from jose import JWTError, jwt

from app.config import settings

# Initialize Argon2id password hasher with secure defaults
_hasher = PasswordHasher()
_DUMMY_PASSWORD_HASH = _hasher.hash("constant-time-user-lookup-dummy-password")

_RESERVED_CLAIMS = frozenset({"sub", "iat", "exp", "jti", "iss", "aud", "type"})


def hash_password(password: str) -> str:
    """Hash a plaintext password using Argon2id."""
    return _hasher.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against an Argon2id hash."""
    try:
        return _hasher.verify(hashed_password, plain_password)
    except (VerifyMismatchError, InvalidHashError):
        return False


def verify_unknown_user_password(plain_password: str) -> None:
    """Spend a password-hash verification for unknown/no-password accounts too."""
    verify_password(plain_password, _DUMMY_PASSWORD_HASH)


def sha256_hex(value: str) -> str:
    """Hash an opaque token or code for storage and constant-time lookup."""
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def secure_hex(nbytes: int = 32) -> str:
    """Generate a high-entropy opaque identifier."""
    return secrets.token_hex(nbytes)


def secure_url_token(nbytes: int = 32) -> str:
    """Generate a high-entropy URL-safe opaque token."""
    return secrets.token_urlsafe(nbytes)


def tokens_equal(left: str, right: str) -> bool:
    """Compare hashes or state values without timing leakage."""
    return hmac.compare_digest(left, right)


def create_pkce_pair() -> tuple[str, str]:
    """Return a PKCE S256 `(code_verifier, code_challenge)` pair."""
    verifier = secure_url_token(48)
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    challenge = base64_urlencode(digest)
    return verifier, challenge


def base64_urlencode(raw: bytes) -> str:
    """Base64url encode without padding."""
    import base64

    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def create_access_token(
    user_id: uuid.UUID | str,
    expires_delta: timedelta | None = None,
    extra_claims: dict[str, Any] | None = None,
) -> str:
    """Create a signed access token with a revocation-ready `jti` claim."""
    now = datetime.now(timezone.utc)
    expire = (
        now + expires_delta
        if expires_delta is not None
        else now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    jti = secure_hex(32)

    payload: dict[str, Any] = {
        "sub": str(user_id),
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "jti": jti,
        "iss": settings.JWT_ISSUER,
        "aud": settings.JWT_AUDIENCE,
        "type": "access",
    }

    if extra_claims:
        payload.update(
            {key: value for key, value in extra_claims.items() if key not in _RESERVED_CLAIMS}
        )

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    """Decode and validate a signed internal access token.

    Signature, algorithm, expiry, issuer, audience, and all security claims are
    required. Revocation is checked separately against ``auth_sessions``.
    """
    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
        audience=settings.JWT_AUDIENCE,
        issuer=settings.JWT_ISSUER,
        options={"require": ["sub", "iat", "exp", "jti", "iss", "aud", "type"]},
    )


__all__ = [
    "JWTError",
    "base64_urlencode",
    "create_access_token",
    "create_pkce_pair",
    "decode_access_token",
    "hash_password",
    "secure_hex",
    "secure_url_token",
    "sha256_hex",
    "tokens_equal",
    "verify_password",
    "verify_unknown_user_password",
]
