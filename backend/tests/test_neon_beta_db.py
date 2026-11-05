"""Credential-free tests for Neon beta URL normalization and guards."""

import pytest
from sqlalchemy import create_engine

from app.config import Settings
from app.scripts.neon_beta_db import BetaDatabaseError, beta_url_from_environment


POOLED_HOST = "ep-cool-breeze-123-pooler.us-east-2.aws.neon.tech"


@pytest.mark.parametrize("scheme", ["postgresql://", "postgres://"])
def test_standard_neon_url_is_normalized_to_psycopg3(monkeypatch, scheme):
    monkeypatch.setenv(
        "DATABASE_URL",
        f"{scheme}neondb_owner:p%40ss%3Aword@{POOLED_HOST}/neondb"
        "?sslmode=require&channel_binding=require",
    )

    url = beta_url_from_environment()

    assert url.drivername == "postgresql+psycopg"
    assert url.password == "p@ss:word"
    assert url.host == POOLED_HOST
    assert url.database == "neondb"
    assert url.query["sslmode"] == "require"
    assert url.query["channel_binding"] == "require"
    settings = Settings(
        _env_file=None,
        DATABASE_URL=(
            f"{scheme}neondb_owner:p%40ss%3Aword@{POOLED_HOST}/neondb"
            "?sslmode=require&channel_binding=require"
        ),
    )
    assert settings.DATABASE_URL.startswith("postgresql+psycopg://")
    assert "p%40ss%3Aword@" in settings.DATABASE_URL
    engine = create_engine(url)
    try:
        assert engine.dialect.name == "postgresql"
        assert engine.dialect.driver == "psycopg"
        assert engine.url.query["channel_binding"] == "require"
    finally:
        engine.dispose()


def test_sqlalchemy_psycopg_url_is_preserved(monkeypatch):
    monkeypatch.setenv(
        "DATABASE_URL",
        f"postgresql+psycopg://neondb_owner:synthetic@{POOLED_HOST}/neondb?sslmode=require",
    )
    assert beta_url_from_environment().drivername == "postgresql+psycopg"


@pytest.mark.parametrize(
    ("url", "error_code"),
    [
        (f"postgresql://neondb_owner:synthetic@{POOLED_HOST}/other?sslmode=require", "DATABASE_TARGET_MISMATCH"),
        ("postgresql://neondb_owner:synthetic@ep-cool-breeze.us-east-2.aws.neon.tech/neondb?sslmode=require", "NEON_POOLER_HOST_REQUIRED"),
        (f"postgresql://neondb_owner:synthetic@{POOLED_HOST}/neondb", "TLS_REQUIRED"),
        (f"postgresql://neondb_owner:synthetic@{POOLED_HOST}/neondb?sslmode=require&channel_binding=invalid", "CHANNEL_BINDING_INVALID"),
    ],
)
def test_unsafe_or_wrong_target_urls_fail_with_stage_and_safe_code(monkeypatch, url, error_code):
    monkeypatch.setenv("DATABASE_URL", url)

    with pytest.raises(BetaDatabaseError) as error:
        beta_url_from_environment()

    assert error.value.code == error_code
    assert "synthetic" not in str(error.value)
    assert "ep-cool-breeze" not in str(error.value)


def test_missing_process_url_does_not_fall_back_to_dotenv(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)

    with pytest.raises(BetaDatabaseError) as error:
        beta_url_from_environment()

    assert error.value.code == "DATABASE_URL_MISSING"
    assert error.value.stage == "environment"
