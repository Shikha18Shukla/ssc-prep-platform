"""Read-only inspection and guarded Alembic upgrade for the Neon beta DB.

The URL must be supplied through the process environment. This deliberately
does not fall back to the local .env file, and only accepts the named Neon beta
database/role on a pooled Neon TLS endpoint.
"""

import argparse
import os
from pathlib import Path
import re
import sys

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL, make_url
from sqlalchemy.exc import ArgumentError, SQLAlchemyError
from sqlalchemy.pool import NullPool


EXPECTED_DATABASE = "neondb"
EXPECTED_ROLE = "neondb_owner"
EXPECTED_HEAD = "0009_generic_beta_invites"
CONFIRMATION = "APPLY 0001-0009 TO ssc-prep-beta/neondb"
REQUIRED_TABLES = {
    "users", "exams", "subjects", "subcategories", "chapters", "questions",
    "question_options", "test_attempts", "test_questions", "user_answers",
    "user_chapter_rotations", "user_question_history", "beta_capacity",
    "beta_invitations", "rate_limit_windows",
}
REQUIRED_CONSTRAINTS = {
    "beta_capacity_pkey",
    "ck_beta_capacity_singleton",
    "ck_beta_capacity_max_200",
    "beta_invitations_pkey",
    "uq_beta_invitation_token_hash",
    "rate_limit_windows_pkey",
    "uq_subject_exam_slug",
    "uq_subcategory_subject_slug",
    "uq_subcategory_id_subject",
    "uq_chapter_subcategory_slug",
    "fk_chapter_subcategory_subject",
    "uq_question_option_key",
    "uq_test_attempt_question",
    "uq_test_attempt_question_order",
    "uq_test_attempt_test_question_answer",
    "uq_user_chapter_rotation_mode",
    "uq_user_chapter_mode_question_history",
}
REQUIRED_INDEXES = {
    "ix_users_email",
    "ix_exams_slug",
    "uq_chapter_subject_slug_without_subcategory",
}
COUNT_TABLES = ("users", "beta_invitations", "exams", "subjects", "chapters", "questions")


class BetaDatabaseError(Exception):
    """A stage-labeled, credential-safe failure message."""

    def __init__(self, stage: str, code: str, safe_message: str):
        super().__init__(safe_message)
        self.stage = stage
        self.code = code


def _safe_postgres_diagnostic(error: BaseException) -> str | None:
    """Format only allowlisted PostgreSQL diagnostic fields, never raw errors."""
    fields: dict[str, str] = {}
    pending = [error]
    visited: set[int] = set()
    while pending and len(visited) < 12:
        current = pending.pop(0)
        if id(current) in visited:
            continue
        visited.add(id(current))
        candidates = [current]
        original = getattr(current, "orig", None)
        if isinstance(original, BaseException):
            candidates.append(original)
            pending.append(original)
        pending.extend(
            chained for chained in (current.__cause__, current.__context__)
            if isinstance(chained, BaseException)
        )

        for candidate in candidates:
            sqlstate = getattr(candidate, "sqlstate", None) or getattr(candidate, "pgcode", None)
            if isinstance(sqlstate, str) and re.fullmatch(r"[0-9A-Z]{5}", sqlstate):
                fields.setdefault("SQLSTATE", sqlstate)
            diagnostic = getattr(candidate, "diag", None)
            if diagnostic is None:
                continue
            for key, attribute in (
                ("primary_message", "message_primary"),
                ("table_name", "table_name"),
                ("column_name", "column_name"),
                ("constraint_name", "constraint_name"),
            ):
                value = getattr(diagnostic, attribute, None)
                if isinstance(value, str) and value:
                    # PostgreSQL's primary message is distinct from DETAIL,
                    # which can include row data. Flatten controls and cap it.
                    safe_value = " ".join(value.split())[:500]
                    fields.setdefault(key, safe_value)

    if not fields:
        return None
    order = ("SQLSTATE", "primary_message", "table_name", "column_name", "constraint_name")
    return "; ".join(f"{key}={fields[key]}" for key in order if key in fields)


def beta_url_from_environment() -> URL:
    raw_url = os.environ.get("DATABASE_URL")
    if not raw_url:
        raise BetaDatabaseError(
            "environment", "DATABASE_URL_MISSING",
            "DATABASE_URL is not set in this process; the local .env file is not used as a fallback.",
        )

    try:
        url = make_url(raw_url)
    except (ArgumentError, ValueError, TypeError) as exc:
        raise BetaDatabaseError(
            "URL parse", "DATABASE_URL_INVALID",
            "DATABASE_URL could not be parsed; use a PostgreSQL URL and percent-encode reserved password characters.",
        ) from exc

    # Neon Console commonly provides postgresql:// (and some clients show
    # postgres://). SQLAlchemy otherwise chooses psycopg2 for those schemes;
    # explicitly select the project's installed psycopg 3 driver instead.
    if url.drivername in {"postgresql", "postgres"}:
        url = url.set(drivername="postgresql+psycopg")
    elif url.drivername != "postgresql+psycopg":
        raise BetaDatabaseError(
            "URL driver", "DATABASE_DRIVER_UNSUPPORTED",
            "Use postgresql://, postgres://, or postgresql+psycopg://; this project uses psycopg 3.",
        )

    hostname = (url.host or "").lower()
    sslmode = url.query.get("sslmode")
    if not url.username or not url.password:
        raise BetaDatabaseError(
            "URL credentials", "DATABASE_CREDENTIALS_MISSING",
            "The URL must contain the configured database role and password.",
        )
    if url.username != EXPECTED_ROLE or url.database != EXPECTED_DATABASE:
        raise BetaDatabaseError(
            "beta target validation", "DATABASE_TARGET_MISMATCH",
            "Expected database neondb and role neondb_owner; supplied values were not displayed.",
        )
    if not hostname.endswith(".neon.tech") or "-pooler" not in hostname:
        raise BetaDatabaseError(
            "pooled host validation", "NEON_POOLER_HOST_REQUIRED",
            "Expected a pooled Neon hostname ending in .neon.tech with -pooler in its endpoint name; hostname was not displayed.",
        )
    if sslmode not in {"require", "verify-ca", "verify-full"}:
        raise BetaDatabaseError(
            "TLS validation", "TLS_REQUIRED",
            "TLS is required; set sslmode=require (channel_binding=require is also accepted).",
        )
    channel_binding = url.query.get("channel_binding")
    if channel_binding is not None and channel_binding not in {"require", "prefer", "disable"}:
        raise BetaDatabaseError(
            "channel binding validation", "CHANNEL_BINDING_INVALID",
            "channel_binding must be require, prefer, or disable.",
        )
    return url


def verify_read_only_connection(url: URL) -> None:
    try:
        engine = create_engine(
            url,
            poolclass=NullPool,
            pool_pre_ping=True,
            connect_args={"connect_timeout": 10},
        )
    except (ValueError, TypeError, ImportError) as exc:
        raise BetaDatabaseError(
            "SQLAlchemy driver setup", "SQLALCHEMY_DRIVER_SETUP_FAILED",
            "SQLAlchemy could not configure the psycopg 3 driver; verify the installed backend dependencies.",
        ) from exc
    try:
        try:
            with engine.connect() as connection:
                with connection.begin():
                    connection.execute(text("SET TRANSACTION READ ONLY"))
                    database, role, read_only = connection.execute(text(
                        "SELECT current_database(), current_user, "
                        "current_setting('transaction_read_only')"
                    )).one()
                    if (database, role, read_only) != (EXPECTED_DATABASE, EXPECTED_ROLE, "on"):
                        raise BetaDatabaseError(
                            "connected identity check", "CONNECTED_TARGET_MISMATCH",
                            "The server returned a database, role, or read-only state different from the required beta target.",
                        )
        except BetaDatabaseError:
            raise
        except SQLAlchemyError as exc:
            raise BetaDatabaseError(
                "database connection/query", "DATABASE_CONNECTION_FAILED",
                "The read-only PostgreSQL connection or identity query failed; check Neon availability, URL credentials, SSL, and network access.",
            ) from exc
        except ValueError as exc:
            raise BetaDatabaseError(
                "database connection setup", "DATABASE_CONNECTION_SETUP_FAILED",
                "The PostgreSQL driver rejected a connection option; confirm the URL query options are supported by psycopg 3.",
            ) from exc
    finally:
        engine.dispose()

    print(
        "Read-only connection verified: "
        f"database={EXPECTED_DATABASE}, role={EXPECTED_ROLE}, "
        f"pooled=yes, TLS={url.query.get('sslmode')}. No schema changes made."
    )


def inspect_beta_database(url: URL) -> None:
    """Print migration/schema/capacity/data counts using one read-only transaction."""
    try:
        engine = create_engine(
            url,
            poolclass=NullPool,
            pool_pre_ping=True,
            connect_args={"connect_timeout": 10},
        )
    except (ValueError, TypeError, ImportError) as exc:
        raise BetaDatabaseError(
            "SQLAlchemy driver setup", "SQLALCHEMY_DRIVER_SETUP_FAILED",
            "SQLAlchemy could not configure the psycopg 3 driver; verify the backend dependencies.",
        ) from exc

    try:
        with engine.connect() as connection:
            with connection.begin():
                connection.execute(text("SET TRANSACTION READ ONLY"))
                database, role, read_only = connection.execute(text(
                    "SELECT current_database(), current_user, "
                    "current_setting('transaction_read_only')"
                )).one()
                if (database, role, read_only) != (EXPECTED_DATABASE, EXPECTED_ROLE, "on"):
                    raise BetaDatabaseError(
                        "connected identity check", "CONNECTED_TARGET_MISMATCH",
                        "Connected database identity/read-only state does not match the expected beta target.",
                    )

                revisions = connection.execute(
                    text("SELECT version_num FROM alembic_version")
                ).scalars().all()
                tables = set(connection.execute(text(
                    "SELECT table_name FROM information_schema.tables "
                    "WHERE table_schema = current_schema() AND table_type = 'BASE TABLE'"
                )).scalars().all())
                constraints = set(connection.execute(text(
                    "SELECT conname FROM pg_constraint "
                    "WHERE connamespace = current_schema()::regnamespace"
                )).scalars().all())
                indexes = set(connection.execute(text(
                    "SELECT indexname FROM pg_indexes WHERE schemaname = current_schema()"
                )).scalars().all())
                user_columns = set(connection.execute(text(
                    "SELECT column_name FROM information_schema.columns "
                    "WHERE table_schema = current_schema() AND table_name = 'users'"
                )).scalars().all())
                capacity_rows = connection.execute(text(
                    "SELECT id, max_accounts FROM beta_capacity ORDER BY id"
                )).all()

                counts = {}
                for table in COUNT_TABLES:
                    if table in tables:
                        counts[table] = connection.execute(
                            text(f'SELECT count(*) FROM "{table}"')
                        ).scalar_one()
                    else:
                        counts[table] = None
                if "beta_invitations" in tables:
                    counts["pending_unexpired_invitations"] = connection.execute(text(
                        "SELECT count(*) FROM beta_invitations "
                        "WHERE redeemed_at IS NULL AND expires_at > now()"
                    )).scalar_one()
                else:
                    counts["pending_unexpired_invitations"] = None
    except BetaDatabaseError:
        raise
    except SQLAlchemyError as exc:
        raise BetaDatabaseError(
            "read-only schema inspection", "READ_ONLY_INSPECTION_FAILED",
            "A read-only inspection query failed; the database was not modified.",
        ) from exc
    finally:
        engine.dispose()

    missing_tables = sorted(REQUIRED_TABLES - tables)
    missing_constraints = sorted(REQUIRED_CONSTRAINTS - constraints)
    missing_indexes = sorted(REQUIRED_INDEXES - indexes)
    print(f"Database identity: {database}/{role}; transaction_read_only={read_only}")
    print(f"Alembic revision: {', '.join(revisions) if revisions else 'MISSING'} (expected {EXPECTED_HEAD})")
    print(f"Required tables: {len(REQUIRED_TABLES) - len(missing_tables)}/{len(REQUIRED_TABLES)} present")
    if missing_tables:
        print("Missing tables: " + ", ".join(missing_tables))
    print(f"Required constraints: {len(REQUIRED_CONSTRAINTS) - len(missing_constraints)}/{len(REQUIRED_CONSTRAINTS)} present")
    if missing_constraints:
        print("Missing constraints: " + ", ".join(missing_constraints))
    print(f"Required unique indexes: {len(REQUIRED_INDEXES) - len(missing_indexes)}/{len(REQUIRED_INDEXES)} present")
    if missing_indexes:
        print("Missing indexes: " + ", ".join(missing_indexes))
    print(f"users.is_admin column: {'present' if 'is_admin' in user_columns else 'MISSING'}")
    capacity = [value for row_id, value in capacity_rows if row_id == 1]
    print(f"Account capacity row (id=1): {capacity[0] if capacity else 'MISSING'} (expected 200)")
    print("Row counts (no identifiers or personal data):")
    for table in COUNT_TABLES:
        print(f"  {table}: {counts[table] if counts[table] is not None else 'MISSING TABLE'}")
    print(f"  pending_unexpired_invitations: {counts['pending_unexpired_invitations'] if counts['pending_unexpired_invitations'] is not None else 'MISSING TABLE'}")
    print("Inspection completed in a read-only transaction; no data was changed.")


def upgrade_beta_database(url: URL) -> None:
    verify_read_only_connection(url)

    from alembic import command
    from alembic.config import Config
    from alembic.script import ScriptDirectory

    backend_dir = Path(__file__).resolve().parents[2]
    config = Config(str(backend_dir / "alembic.ini"))
    head = ScriptDirectory.from_config(config).get_current_head()
    if head != EXPECTED_HEAD:
        raise RuntimeError(f"Unexpected Alembic head: {head!r}")

    print(
        f"Target: {EXPECTED_DATABASE}@{url.host}; "
        f"Alembic will upgrade to {EXPECTED_HEAD}."
    )
    if input(f'Type exactly "{CONFIRMATION}" to continue: ').strip() != CONFIRMATION:
        print("Cancelled; no migrations run.")
        return

    # app.config reads DATABASE_URL from the process environment, which takes
    # precedence over its .env file. This script never sets or edits .env.
    command.upgrade(config, "head")
    print(f"Alembic upgrade complete at {EXPECTED_HEAD}.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("verify", "inspect", "upgrade"))
    args = parser.parse_args()

    try:
        url = beta_url_from_environment()
        if args.action == "verify":
            verify_read_only_connection(url)
        elif args.action == "inspect":
            inspect_beta_database(url)
        else:
            upgrade_beta_database(url)
    except BetaDatabaseError as exc:
        print(
            f"Beta database operation failed at {exc.stage} [{exc.code}]: {exc}",
            file=sys.stderr,
        )
        return 1
    except Exception as exc:
        # Do not print raw driver/config exception text: it may echo connection data.
        stage = (
            "Alembic upgrade" if args.action == "upgrade"
            else "read-only inspection" if args.action == "inspect"
            else "read-only verification"
        )
        message = (
            f"Beta database operation failed at {stage} [{type(exc).__name__}]; "
            "sensitive connection details were suppressed."
        )
        diagnostic = _safe_postgres_diagnostic(exc)
        if diagnostic:
            message += f" Safe PostgreSQL diagnostic: {diagnostic}."
        print(message, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
