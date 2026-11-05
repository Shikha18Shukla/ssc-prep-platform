"""Database-backed fixed-window limits shared across API workers."""

from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import threading
import time

from fastapi import HTTPException, status
from sqlalchemy import case, delete
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.orm import Session

from app.config import settings
from app.models import RateLimitWindow

_cleanup_lock = threading.Lock()
_last_cleanup = 0.0


def enforce_rate_limit(db: Session, identity: str, limit: int, window_seconds: int) -> None:
    """Atomically count one request for a pseudonymous identity and reject excess."""
    global _last_cleanup
    now = datetime.now(timezone.utc)
    window = timedelta(seconds=window_seconds)
    expires_before = now - window
    raw_key = identity.encode("utf-8")
    key_hash = hmac.new(settings.SECRET_KEY.encode("utf-8"), raw_key, hashlib.sha256).hexdigest()
    table = RateLimitWindow.__table__
    values = {"key_hash": key_hash, "window_started_at": now, "request_count": 1, "updated_at": now}
    dialect = db.bind.dialect.name
    if dialect == "postgresql":
        statement = pg_insert(table).values(**values)
        insert = statement.on_conflict_do_update(
            index_elements=[table.c.key_hash],
            set_={
                "window_started_at": case(
                    (table.c.window_started_at <= expires_before, now),
                    else_=table.c.window_started_at,
                ),
                "request_count": case(
                    (table.c.window_started_at <= expires_before, 1),
                    else_=table.c.request_count + 1,
                ),
                "updated_at": now,
            },
        )
    elif dialect == "sqlite":
        statement = sqlite_insert(table).values(**values)
        insert = statement.on_conflict_do_update(
            index_elements=[table.c.key_hash],
            set_={
                "window_started_at": case(
                    (table.c.window_started_at <= expires_before, now),
                    else_=table.c.window_started_at,
                ),
                "request_count": case(
                    (table.c.window_started_at <= expires_before, 1),
                    else_=table.c.request_count + 1,
                ),
                "updated_at": now,
            },
        )
    else:
        raise RuntimeError("Rate limiting requires PostgreSQL or SQLite upsert support")

    count, started_at = db.execute(
        insert.returning(table.c.request_count, table.c.window_started_at)
    ).one()
    db.commit()

    current = time.monotonic()
    if current - _last_cleanup >= settings.RATE_LIMIT_CLEANUP_SECONDS:
        with _cleanup_lock:
            current = time.monotonic()
            if current - _last_cleanup >= settings.RATE_LIMIT_CLEANUP_SECONDS:
                with db.begin():
                    db.execute(delete(RateLimitWindow).where(
                        RateLimitWindow.window_started_at < now - timedelta(days=1)
                    ))
                _last_cleanup = current

    if count > limit:
        if started_at.tzinfo is None:
            started_at = started_at.replace(tzinfo=timezone.utc)
        elapsed = max(0, int((now - started_at).total_seconds()))
        retry_after = max(1, window_seconds - elapsed)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Try again later.",
            headers={"Retry-After": str(retry_after)},
        )
