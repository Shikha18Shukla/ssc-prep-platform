"""Database engine and session configuration.

Architecture decision — Synchronous SQLAlchemy
───────────────────────────────────────────────
This project uses **synchronous** SQLAlchemy 2.x with the psycopg (v3)
driver for the following reasons:

1. **Simplicity** — sync code is easier to debug and reason about.
2. **FastAPI compatibility** — FastAPI runs sync dependencies in a
   thread-pool, so sync DB access does not block the event loop.
3. **Reliability** — fewer edge-cases than async session management.
4. **Migration path** — psycopg v3 supports both sync and async.
   Switching to async later requires swapping ``create_engine`` →
   ``create_async_engine`` and ``sessionmaker`` → ``async_sessionmaker``
   with minimal other changes.
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that provides a database session per request.

    Usage in a router::

        @router.get("/example")
        def example(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
