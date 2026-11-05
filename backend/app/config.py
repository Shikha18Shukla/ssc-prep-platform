"""Application configuration using environment variables."""

from pydantic_settings import BaseSettings
from pydantic import field_validator, model_validator
from urllib.parse import urlsplit
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
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5432/ssc_prep"
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT_SECONDS: int = 30
    DB_POOL_RECYCLE_SECONDS: int = 1800
    BETA_INVITATIONS_REQUIRED: bool = False
    BETA_CATALOG_SCOPE: bool = False
    RATE_LIMIT_CLEANUP_SECONDS: int = 900

    # JWT Authentication (to be implemented in a later stage)
    SECRET_KEY: str = "change-this-secret-key-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

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
                try:
                    parsed_origin = urlsplit(origin)
                    port = parsed_origin.port
                except ValueError as exc:
                    raise ValueError("Each production CORS_ORIGINS entry must be an exact HTTPS origin") from exc
                if (parsed_origin.scheme != "https" or not parsed_origin.hostname
                        or parsed_origin.username or parsed_origin.password
                        or parsed_origin.path or parsed_origin.query or parsed_origin.fragment
                        or "*" in parsed_origin.hostname
                        or "localhost" in parsed_origin.hostname.lower()
                        or (port is not None and not 1 <= port <= 65535)):
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
            if not self.BETA_INVITATIONS_REQUIRED:
                raise ValueError("BETA_INVITATIONS_REQUIRED must be true in production")
            if not self.BETA_CATALOG_SCOPE:
                raise ValueError("BETA_CATALOG_SCOPE must be true in production")
            if self.ACCESS_TOKEN_EXPIRE_MINUTES < 5 or self.ACCESS_TOKEN_EXPIRE_MINUTES > 60:
                raise ValueError("Production access tokens must expire between 5 and 60 minutes")
        if min(self.DB_POOL_SIZE, self.DB_POOL_TIMEOUT_SECONDS, self.DB_POOL_RECYCLE_SECONDS) < 1 or self.DB_MAX_OVERFLOW < 0:
            raise ValueError("Database pool settings must be positive (overflow may be zero)")
        if self.RATE_LIMIT_CLEANUP_SECONDS < 60:
            raise ValueError("RATE_LIMIT_CLEANUP_SECONDS must be at least 60")
        return self

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


settings = Settings()
