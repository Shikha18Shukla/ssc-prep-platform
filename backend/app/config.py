"""Application configuration using environment variables."""

from typing import Literal
from urllib.parse import urlsplit

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings
from sqlalchemy.engine import make_url
from sqlalchemy.exc import ArgumentError


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "SSC Prep Platform"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # Database
    DATABASE_URL: str = "postgresql+psycopg://<user>:<password>@localhost:5432/<database>"
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT_SECONDS: int = 30
    DB_POOL_RECYCLE_SECONDS: int = 1800
    BETA_CATALOG_SCOPE: bool = False
    RATE_LIMIT_CLEANUP_SECONDS: int = 900

    # JWT authentication
    SECRET_KEY: str = "change-this-secret-key-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_ISSUER: str = "ssc-prep-platform"
    JWT_AUDIENCE: str = "ssc-prep-web"

    # Google OAuth 2.0 authorization-code flow. All values are server-side only.
    GOOGLE_CLIENT_ID: str | None = None
    GOOGLE_CLIENT_SECRET: str | None = None
    GOOGLE_REDIRECT_URI: str | None = None
    GOOGLE_SUCCESS_REDIRECT_URL: str = "http://localhost:5173/auth/google/complete"
    GOOGLE_COOKIE_SECURE: bool = False
    GOOGLE_COOKIE_SAMESITE: Literal["lax", "none"] = "lax"
    GOOGLE_STATE_TTL_SECONDS: int = 600
    GOOGLE_EXCHANGE_TTL_SECONDS: int = 300

    # Password setup/recovery delivery. "none" never claims an email was sent.
    EMAIL_PROVIDER: Literal["none", "smtp"] = "none"
    PASSWORD_RESET_URL: str = "http://localhost:5173/reset-password"
    PASSWORD_RESET_TTL_SECONDS: int = 1800
    SMTP_HOST: str | None = None
    SMTP_PORT: int = 587
    SMTP_USERNAME: str | None = None
    SMTP_PASSWORD: str | None = None
    SMTP_FROM_EMAIL: str | None = None
    SMTP_USE_TLS: bool = True
    SMTP_USE_STARTTLS: bool = True

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:5173"]

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def normalize_postgresql_driver(cls, value):
        """Select psycopg 3 when a provider supplies a generic PostgreSQL URL."""
        if not isinstance(value, str):
            return value
        try:
            url = make_url(value)
        except (ArgumentError, TypeError, ValueError):
            # Preserve malformed text for the production validator to reject
            # with its safe DATABASE_URL error rather than exposing parser data.
            return value
        if url.drivername in {"postgresql", "postgres"}:
            return url.set(drivername="postgresql+psycopg").render_as_string(
                hide_password=False
            )
        return value

    @staticmethod
    def _is_placeholder(value: str | None) -> bool:
        return value is None or not value.strip() or "<" in value or ">" in value

    @staticmethod
    def _is_exact_https_url(value: str | None) -> bool:
        if not value:
            return False
        try:
            parsed = urlsplit(value)
        except ValueError:
            return False
        port = parsed.port
        return (
            parsed.scheme == "https"
            and bool(parsed.hostname)
            and not parsed.username
            and not parsed.password
            and not parsed.query
            and not parsed.fragment
            and "*" not in parsed.hostname
            and "localhost" not in parsed.hostname.lower()
            and (port is None or 1 <= port <= 65535)
        )

    @classmethod
    def _is_exact_https_origin(cls, value: str | None) -> bool:
        if not value:
            return False
        return cls._is_exact_https_url(value) and not urlsplit(value).path.rstrip("/")

    def google_is_configured(self) -> bool:
        """Return True only when every required server-side Google value exists."""
        return all([
            not self._is_placeholder(self.GOOGLE_CLIENT_ID),
            not self._is_placeholder(self.GOOGLE_CLIENT_SECRET),
            not self._is_placeholder(self.GOOGLE_REDIRECT_URI),
        ])

    @model_validator(mode="after")
    def validate_production_settings(self):
        if self.ENVIRONMENT.strip().lower() == "production":
            if self.SECRET_KEY == "change-this-secret-key-in-production" or len(self.SECRET_KEY) < 32 or "<" in self.SECRET_KEY:
                raise ValueError("Production SECRET_KEY must be a unique value of at least 32 characters")
            if self.DEBUG:
                raise ValueError("DEBUG must be false in production")
            if not self.CORS_ORIGINS:
                raise ValueError("Production CORS_ORIGINS must contain explicit HTTPS origins")
            for origin in self.CORS_ORIGINS:
                if not self._is_exact_https_origin(origin):
                    raise ValueError("Each production CORS_ORIGINS entry must be an exact HTTPS origin")
            try:
                database_url = make_url(self.DATABASE_URL)
            except Exception as exc:
                raise ValueError("DATABASE_URL must be a valid PostgreSQL connection URL") from exc
            if (database_url.drivername != "postgresql+psycopg" or not database_url.host
                    or database_url.host.lower() in {"localhost", "127.0.0.1", "::1"}
                    or not database_url.username or not database_url.password
                    or database_url.query.get("sslmode") not in {"require", "verify-ca", "verify-full"}):
                raise ValueError("Production DATABASE_URL must target managed PostgreSQL over TLS")
            if not self.BETA_CATALOG_SCOPE:
                raise ValueError("BETA_CATALOG_SCOPE must be true in production")
            if self.ACCESS_TOKEN_EXPIRE_MINUTES < 5 or self.ACCESS_TOKEN_EXPIRE_MINUTES > 60:
                raise ValueError("Production access tokens must expire between 5 and 60 minutes")
            google_values = [
                self.GOOGLE_CLIENT_ID,
                self.GOOGLE_CLIENT_SECRET,
                self.GOOGLE_REDIRECT_URI,
            ]
            if any(not self._is_placeholder(value) for value in google_values) and not self.google_is_configured():
                raise ValueError("Google OAuth requires client ID, client secret, and redirect URI together")
            if self.google_is_configured():
                if not self._is_exact_https_url(self.GOOGLE_REDIRECT_URI):
                    raise ValueError("Production GOOGLE_REDIRECT_URI must be an exact HTTPS URL")
                redirect_path = urlsplit(self.GOOGLE_REDIRECT_URI).path.rstrip("/")
                if redirect_path != "/api/auth/google/callback":
                    raise ValueError("GOOGLE_REDIRECT_URI must point to the exact backend callback path")
                if not self._is_exact_https_url(self.GOOGLE_SUCCESS_REDIRECT_URL):
                    raise ValueError("Production GOOGLE_SUCCESS_REDIRECT_URL must be an exact HTTPS URL")
                if not self.GOOGLE_COOKIE_SECURE:
                    raise ValueError("GOOGLE_COOKIE_SECURE must be true in production when Google OAuth is enabled")
                if self.GOOGLE_COOKIE_SAMESITE != "none":
                    raise ValueError("GOOGLE_COOKIE_SAMESITE must be 'none' for cross-origin production OAuth")
            if self.EMAIL_PROVIDER == "smtp":
                if any(self._is_placeholder(value) for value in [
                    self.SMTP_HOST, self.SMTP_USERNAME, self.SMTP_PASSWORD, self.SMTP_FROM_EMAIL
                ]):
                    raise ValueError("SMTP email delivery requires host, username, password, and sender")
                if not self._is_exact_https_url(self.PASSWORD_RESET_URL):
                    raise ValueError("Production PASSWORD_RESET_URL must be an exact HTTPS URL")
        if min(self.DB_POOL_SIZE, self.DB_POOL_TIMEOUT_SECONDS, self.DB_POOL_RECYCLE_SECONDS) < 1 or self.DB_MAX_OVERFLOW < 0:
            raise ValueError("Database pool settings must be positive (overflow may be zero)")
        if self.RATE_LIMIT_CLEANUP_SECONDS < 60:
            raise ValueError("RATE_LIMIT_CLEANUP_SECONDS must be at least 60")
        if not 60 <= self.GOOGLE_STATE_TTL_SECONDS <= 900:
            raise ValueError("GOOGLE_STATE_TTL_SECONDS must be between 60 and 900")
        if not 60 <= self.GOOGLE_EXCHANGE_TTL_SECONDS <= 600:
            raise ValueError("GOOGLE_EXCHANGE_TTL_SECONDS must be between 60 and 600")
        if not 300 <= self.PASSWORD_RESET_TTL_SECONDS <= 86400:
            raise ValueError("PASSWORD_RESET_TTL_SECONDS must be between 300 and 86400")
        if not 1 <= self.SMTP_PORT <= 65535:
            raise ValueError("SMTP_PORT must be a valid port")
        return self

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


settings = Settings()
