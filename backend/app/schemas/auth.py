"""Pydantic schemas for password and Google authentication.

Output schemas never expose password hashes, reset tokens, OAuth codes, state,
nonces, PKCE verifiers, or provider credentials.
"""

from datetime import datetime
import re
import uuid

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator


PASSWORD_PATTERN_LETTER = re.compile(r"[A-Za-z]")
PASSWORD_PATTERN_DIGIT = re.compile(r"\d")


def _validate_password_strength(value: str) -> str:
    """Enforce the local password policy shared by signup and recovery."""
    if len(value) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if len(value) > 128:
        raise ValueError("Password must be at most 128 characters long")
    if not PASSWORD_PATTERN_LETTER.search(value):
        raise ValueError("Password must contain at least one letter")
    if not PASSWORD_PATTERN_DIGIT.search(value):
        raise ValueError("Password must contain at least one number")
    return value


class RegisterRequest(BaseModel):
    """Email/password signup request with explicit confirmation."""

    full_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str = Field(..., min_length=8, max_length=128)

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.strip().lower() if isinstance(value, str) else value

    @field_validator("full_name")
    @classmethod
    def clean_full_name(cls, value: str) -> str:
        cleaned = " ".join(value.split())
        if not cleaned:
            raise ValueError("Full name cannot be blank")
        return cleaned

    @field_validator("password", "confirm_password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        return _validate_password_strength(value)

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


class LoginRequest(BaseModel):
    """Email/password login request."""

    email: EmailStr
    password: str = Field(..., min_length=1, max_length=128)

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.strip().lower() if isinstance(value, str) else value


class PasswordResetRequest(BaseModel):
    """Request a single-use password setup/recovery link."""

    email: EmailStr

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.strip().lower() if isinstance(value, str) else value


class PasswordResetConfirm(BaseModel):
    """Complete password setup/recovery with a single-use token."""

    token: str = Field(..., min_length=20, max_length=256)
    new_password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str = Field(..., min_length=8, max_length=128)

    @field_validator("new_password", "confirm_password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        return _validate_password_strength(value)

    @model_validator(mode="after")
    def passwords_match(self):
        if self.new_password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


class GoogleExchangeRequest(BaseModel):
    """One-time opaque code returned to the OAuth callback page."""

    code: str = Field(..., min_length=20, max_length=256)


class UserResponse(BaseModel):
    """Safe public user information; never includes secrets."""

    id: uuid.UUID
    email: str
    full_name: str | None = None
    is_active: bool
    is_admin: bool
    has_password: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    """Session response after signup, login, or Google sign-in."""

    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class GoogleStartResponse(BaseModel):
    """Authorization URL for the configured Google OAuth client."""

    authorization_url: str


class MessageResponse(BaseModel):
    """Generic, non-enumerating response message."""

    message: str


class AccountActivationUpdate(BaseModel):
    """Operator-controlled account activation state."""

    is_active: bool
