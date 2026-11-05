"""Pydantic schemas for authentication and authorization.

Ensures strict input validation, email normalization, password constraints,
and safe user output representations (never exposing password hashes).
"""

from datetime import datetime
import re
import uuid
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class RegisterRequest(BaseModel):
    """Schema for user signup requests."""

    full_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="User's full name",
    )
    email: EmailStr = Field(
        ...,
        description="Valid email address for login and account management",
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Plaintext password (minimum 8 characters)",
    )
    invitation_code: str | None = Field(default=None, min_length=32, max_length=128)

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        """Strip whitespace and lowercase email."""
        if isinstance(v, str):
            return v.strip().lower()
        return v

    @field_validator("full_name")
    @classmethod
    def clean_full_name(cls, v: str) -> str:
        """Strip extra whitespace from full name."""
        cleaned = " ".join(v.split())
        if not cleaned:
            raise ValueError("Full name cannot be blank")
        return cleaned

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Enforce password strength: at least 8 chars, at least one letter, and at least one number."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Za-z]", v):
            raise ValueError("Password must contain at least one letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one number")
        return v


class LoginRequest(BaseModel):
    """Schema for user login requests."""

    email: EmailStr = Field(
        ...,
        description="Registered email address",
    )
    password: str = Field(
        ...,
        min_length=1,
        description="User password",
    )

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        """Strip whitespace and lowercase email."""
        if isinstance(v, str):
            return v.strip().lower()
        return v


class UserResponse(BaseModel):
    """Safe public user information schema (never exposes password hashes)."""

    id: uuid.UUID
    email: str
    full_name: str | None = None
    is_active: bool
    is_admin: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    """Schema returned upon successful authentication."""

    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class BetaInvitationBatchRequest(BaseModel):
    emails: list[EmailStr] = Field(min_length=1, max_length=200)
    expires_in_days: int = Field(default=14, ge=1, le=30)

    @field_validator("emails")
    @classmethod
    def normalize_emails(cls, values: list[EmailStr]) -> list[EmailStr]:
        normalized = [str(value).strip().lower() for value in values]
        if len(set(map(str, normalized))) != len(normalized):
            raise ValueError("Invitation email addresses must be unique")
        return normalized


class BetaInvitationCreated(BaseModel):
    email: str
    invitation_code: str
    expires_at: datetime


class BetaInvitationBatchResponse(BaseModel):
    invitations: list[BetaInvitationCreated]
    total_accounts: int
    pending_invitations: int
    remaining_slots: int


class GenericInvitationBatchRequest(BaseModel):
    count: Literal[50] = 50
    expires_in_days: int = Field(default=14, ge=1, le=30)


class GenericInvitationCreated(BaseModel):
    id: uuid.UUID
    invitation_code: str
    expires_at: datetime


class GenericInvitationBatchResponse(BaseModel):
    invitations: list[GenericInvitationCreated]
    expires_at: datetime
    total_accounts: int
    pending_invitations: int
    remaining_slots: int


class GenericInvitationStatus(BaseModel):
    available: int
    redeemed: int
    expired: int
    revoked: int


class GenericInvitationListItem(BaseModel):
    id: uuid.UUID
    status: Literal["available", "redeemed", "expired", "revoked"]
    expires_at: datetime
    redeemed_at: datetime | None
    revoked_at: datetime | None
    created_at: datetime


class AccountActivationUpdate(BaseModel):
    is_active: bool
