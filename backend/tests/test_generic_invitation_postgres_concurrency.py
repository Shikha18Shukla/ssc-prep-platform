"""Opt-in PostgreSQL locking tests using a dedicated local *_test database.

Set BETA_INVITATION_TEST_DATABASE_URL only to a disposable local PostgreSQL
database whose name ends in ``_test``. Each test creates and drops its own
random schema; Neon and non-local databases are rejected before connecting.
"""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import hashlib
import os
import threading
import uuid

import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine, func, select, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.database.base import Base
from app.models import BetaCapacity, BetaInvitation, User
from app.schemas.auth import RegisterRequest
from app.services.auth_service import register_user


DATABASE_URL = os.environ.get("BETA_INVITATION_TEST_DATABASE_URL")
pytestmark = pytest.mark.skipif(not DATABASE_URL, reason="requires a dedicated local PostgreSQL *_test database")


@pytest.fixture
def postgres_schema_engine():
    url = make_url(DATABASE_URL)
    if url.host not in {"localhost", "127.0.0.1", "::1"} or not (url.database or "").endswith("_test"):
        pytest.fail("Refusing concurrency test: URL must target a local PostgreSQL database ending in _test")
    if url.drivername in {"postgresql", "postgres"}:
        url = url.set(drivername="postgresql+psycopg")
    base_engine = create_engine(url, pool_pre_ping=True)
    schema = f"invite_test_{uuid.uuid4().hex}"
    with base_engine.begin() as connection:
        connection.execute(text(f'CREATE SCHEMA "{schema}"'))
    engine = create_engine(url, connect_args={"options": f"-csearch_path={schema}"}, pool_size=4)
    Base.metadata.create_all(engine)
    try:
        yield engine
    finally:
        engine.dispose()
        with base_engine.begin() as connection:
            connection.execute(text(f'DROP SCHEMA "{schema}" CASCADE'))
        base_engine.dispose()


def _register_concurrently(SessionLocal, payloads):
    barrier = threading.Barrier(len(payloads))

    def attempt(payload):
        with SessionLocal() as session:
            barrier.wait(timeout=10)
            try:
                user = register_user(session, payload)
                return ("created", user.id)
            except HTTPException as exc:
                return ("rejected", exc.status_code)

    with ThreadPoolExecutor(max_workers=len(payloads)) as pool:
        return list(pool.map(attempt, payloads))


def test_postgres_concurrent_redemption_consumes_one_generic_code_once(postgres_schema_engine, monkeypatch):
    monkeypatch.setattr(settings, "BETA_INVITATIONS_REQUIRED", True)
    SessionLocal = sessionmaker(bind=postgres_schema_engine, expire_on_commit=False)
    code = "one-time-" + uuid.uuid4().hex + "-" + uuid.uuid4().hex
    with SessionLocal.begin() as session:
        session.add(BetaCapacity(id=1, max_accounts=200))
        session.add(BetaInvitation(
            email=None,
            token_hash=hashlib.sha256(code.encode()).hexdigest(),
            expires_at=datetime.now(timezone.utc) + timedelta(days=1),
        ))

    results = _register_concurrently(SessionLocal, [
        RegisterRequest(full_name="Student One", email="one@example.com", password="StudentPass123", invitation_code=code),
        RegisterRequest(full_name="Student Two", email="two@example.com", password="StudentPass123", invitation_code=code),
    ])
    assert [result[0] for result in results].count("created") == 1
    assert [result for result in results if result[0] == "rejected"] == [("rejected", 403)]
    with SessionLocal() as session:
        invitation = session.scalar(select(BetaInvitation))
        assert invitation.redeemed_at is not None
        assert session.scalar(select(func.count(User.id))) == 1


def test_postgres_concurrent_distinct_codes_cannot_exceed_capacity(postgres_schema_engine, monkeypatch):
    monkeypatch.setattr(settings, "BETA_INVITATIONS_REQUIRED", True)
    SessionLocal = sessionmaker(bind=postgres_schema_engine, expire_on_commit=False)
    codes = ["capacity-" + uuid.uuid4().hex for _ in range(2)]
    with SessionLocal.begin() as session:
        session.add(BetaCapacity(id=1, max_accounts=1))
        for code in codes:
            session.add(BetaInvitation(
                email=None,
                token_hash=hashlib.sha256(code.encode()).hexdigest(),
                expires_at=datetime.now(timezone.utc) + timedelta(days=1),
            ))

    results = _register_concurrently(SessionLocal, [
        RegisterRequest(full_name="Student One", email="capacity-one@example.com", password="StudentPass123", invitation_code=codes[0]),
        RegisterRequest(full_name="Student Two", email="capacity-two@example.com", password="StudentPass123", invitation_code=codes[1]),
    ])
    assert [result[0] for result in results].count("created") == 1
    assert sorted(result[1] for result in results if result[0] == "rejected") == [409]
    with SessionLocal() as session:
        assert session.scalar(select(func.count(User.id))) == 1
        redeemed = session.scalar(select(func.count(BetaInvitation.id)).where(BetaInvitation.redeemed_at.is_not(None)))
        assert redeemed == 1
