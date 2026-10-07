"""Password hashing and JWT token utilities.

Uses Argon2id (via argon2-cffi) for password hashing and python-jose for JWT tokens.
Never logs passwords or returns password hashes in API responses.
"""

from datetime import datetime, timedelta, timezone
from typing import Any
import uuid

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError
from jose import JWTError, jwt

from app.config import settings

# Initialize Argon2id password hasher with secure defaults
_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    """Hash a plaintext password using Argon2id.

    Args:
        password: Raw plaintext password to hash.

    Returns:
        Argon2id password hash string.
    """
    return _hasher.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against an Argon2id hash.

    Args:
        plain_password: Raw plaintext password to check.
        hashed_password: Stored Argon2id hash.

    Returns:
        True if password matches, False otherwise.
    """
    try:
        return _hasher.verify(hashed_password, plain_password)
    except (VerifyMismatchError, InvalidHashError):
        return False


def create_access_token(
    user_id: uuid.UUID | str,
    expires_delta: timedelta | None = None,
    extra_claims: dict[str, Any] | None = None,
) -> str:
    """Create a signed JWT access token.

    Args:
        user_id: User identifier to store in the `sub` claim.
        expires_delta: Optional custom token expiration time.
        extra_claims: Optional non-sensitive additional claims.

    Returns:
        Encoded JWT token string.
    """
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload: dict[str, Any] = {
        "sub": str(user_id),
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }

    if extra_claims:
        # Prevent overriding critical claims
        claims_to_add = {
            k: v for k, v in extra_claims.items() if k not in ("sub", "iat", "exp")
        }
        payload.update(claims_to_add)

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    """Decode and validate a signed JWT access token.

    Args:
        token: Encoded JWT token string.

    Returns:
        Decoded payload dictionary.

    Raises:
        JWTError: If token is invalid, expired, or signature does not match.
    """
    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )
