"""Pydantic schemas for authentication and authorization.

Ensures strict input validation, email normalization, password constraints,
and safe user output representations (never exposing password hashes).
"""

from datetime import datetime
import re
import uuid

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
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    """Schema returned upon successful authentication."""

    access_token: str
    token_type: str = "bearer"
    user: UserResponse
