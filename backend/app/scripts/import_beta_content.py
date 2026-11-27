"""Guarded, idempotent importer for the approved 81-chapter beta content set."""

from __future__ import annotations

import os
import traceback
from enum import Enum
from typing import Any

import psycopg
from psycopg.rows import dict_row
from sqlalchemy import create_engine, func, select, text
from sqlalchemy.engine import URL
from sqlalchemy.pool import NullPool

from app.models import Chapter, Exam, Question, QuestionOption, Subcategory, Subject
from app.scripts.neon_beta_db import (
    BetaDatabaseError,
    EXPECTED_HEAD,
    beta_url_from_environment,
    inspect_beta_database,
)
from app.scripts.plan_beta_content_import import (
    CONTENT_TABLES,
    SOURCE,
    _expected_chapters,
    _query_source,
    _sanitize_error,
)

EXPECTED = {
    "exams": 1,
    "subjects": 3,
    "subcategories": 3,
    "chapters": 81,
    "questions": 4610,
    "question_options": 18440,
}
MODEL_BY_TABLE = {
    "exams": Exam,
    "subjects": Subject,
    "subcategories": Subcategory,
    "chapters": Chapter,
    "questions": Question,
    "question_options": QuestionOption,
}
PROTECTED_TABLES = (
    "users", "test_attempts", "test_questions", "user_answers",
    "user_chapter_rotations", "user_question_history", "rate_limit_windows",
    "auth_sessions", "oauth_identities", "oauth_states", "oauth_exchange_codes",
    "password_reset_tokens",
)


def _stage(message: str) -> None:
    print(f"[{message}]")


def _source_connect() -> psycopg.Connection:
    password = os.environ.get("PGPASSWORD")
    if not password:
        raise RuntimeError("The masked local PostgreSQL password prompt returned no password.")
    return psycopg.connect(**SOURCE, password=password, connect_timeout=8)


def _load_source_rows(report: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    _stage("Source extraction (read-only)")
    expected_keys = _expected_chapters()
    if (report["allowlist"]["expected"] != 81 or report["allowlist"]["found"] != 81
            or report["allowlist"]["missing"] or report["allowlist"]["unexpected"]
            or report["allowlist"]["duplicate_keys"]):
        raise RuntimeError("Source catalog does not resolve to exactly the approved 81 unique chapters.")
    metric = report["question_metrics"]
    if (metric[0], metric[1], metric[2], metric[7], metric[8]) != (4610, 4393, 217, 4610, 0):
        raise RuntimeError("Source question totals, active/inactive split, or explanation completeness differ from the approved batch.")
    if report["option_count"] != 18440:
        raise RuntimeError("Source option count differs from the approved 18,440.")
    if report["invalid_question_option_sets"] or report["foreign_key_violations"] or report["missing_or_unvalidated_foreign_keys"]:
        raise RuntimeError("Source question options or foreign-key validation failed; refusing import.")

    chapter_ids = [row[6] for row in report["allowlist"]["rows"]]
    exam_ids = {row[0] for row in report["allowlist"]["rows"]}
    subject_ids = {row[2] for row in report["allowlist"]["rows"]}
    subcategory_ids = {row[4] for row in report["allowlist"]["rows"] if row[4]}
    column_names = {
        table: [column.name for column in model.__table__.columns]
        for table, model in MODEL_BY_TABLE.items()
    }
    data: dict[str, list[dict[str, Any]]] = {}

    with _source_connect() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ, READ ONLY")
            cur.execute(
                "SELECT current_database() AS current_database, "
                "current_user AS current_user, "
                "inet_server_addr()::text AS inet_server_addr, "
                "inet_server_port() AS inet_server_port, "
                "current_setting('transaction_read_only') AS transaction_read_only"
            )
            identity = cur.fetchone()
            server_address = identity["inet_server_addr"]
            if server_address:
                import ipaddress
                server_address = str(ipaddress.ip_interface(server_address).ip)
            actual_identity = (
                identity["current_database"], identity["current_user"], server_address,
                identity["inet_server_port"], identity["transaction_read_only"],
            )
            if actual_identity != ("ssc_prep", "postgres", "127.0.0.1", 5432, "on"):
                raise RuntimeError(f"Source identity changed before extraction: {actual_identity!r}.")

            def fetch(table: str, where: str, params: tuple[Any, ...]) -> list[dict[str, Any]]:
                columns = column_names[table]
                projection = ",".join(f'"{column}"' for column in columns)
                cur.execute(f'SELECT {projection} FROM "{table}" WHERE {where}', params)
                return [dict(row) for row in cur.fetchall()]

            data["exams"] = fetch("exams", "id = ANY(%s::uuid[])", (list(exam_ids),))
            data["subjects"] = fetch("subjects", "id = ANY(%s::uuid[])", (list(subject_ids),))
            data["subcategories"] = fetch("subcategories", "id = ANY(%s::uuid[])", (list(subcategory_ids),))
            data["chapters"] = fetch("chapters", "id = ANY(%s::uuid[])", (chapter_ids,))
            data["questions"] = fetch("questions", "chapter_id = ANY(%s::uuid[])", (chapter_ids,))
            question_ids = [str(row["id"]) for row in data["questions"]]
            data["question_options"] = fetch(
                "question_options", "question_id = ANY(%s::uuid[])", (question_ids,)
            )

    for table, count in EXPECTED.items():
        if len(data[table]) != count:
            raise RuntimeError(f"Source extraction count mismatch for {table}: expected {count}, found {len(data[table])}.")
    if len(exam_ids) != 1 or len(subject_ids) != 3 or len(subcategory_ids) != 3:
        raise RuntimeError("Source foreign-key catalog mapping did not resolve to 1 exam, 3 subjects, and 3 subcategories.")

    expected_questions = {str(row["id"]) for row in data["questions"]}
    if any(str(option["question_id"]) not in expected_questions for option in data["question_options"]):
        raise RuntimeError("An extracted option does not belong to an approved question.")
    if any(not row["explanation"] or not str(row["explanation"]).strip() for row in data["questions"]):
        raise RuntimeError("An approved source question is missing its explanation.")

    # Do not deduplicate question stems. Only enforce actual database unique keys.
    unique_keys = {
        "exams": [(row["slug"],) for row in data["exams"]],
        "subjects": [(row["exam_id"], row["slug"]) for row in data["subjects"]],
        "subcategories": [(row["subject_id"], row["slug"]) for row in data["subcategories"]],
        "chapters": [(row["subject_id"], row["subcategory_id"], row["slug"]) for row in data["chapters"]],
        "question_options": [(row["question_id"], row["option_key"]) for row in data["question_options"]],
    }
    for table, keys in unique_keys.items():
        if len(keys) != len(set(keys)):
            raise RuntimeError(f"Source records collide on a database uniqueness key in {table}.")
    if not expected_keys or any(
        (next(r for r in report["allowlist"]["rows"] if str(r[6]) == str(chapter["id"]))[3],
         next(r for r in report["allowlist"]["rows"] if str(r[6]) == str(chapter["id"]))[5], chapter["slug"])
        not in expected_keys for chapter in data["chapters"]
    ):
        raise RuntimeError("Extracted chapters include a row outside the approved allowlist.")
    print("Source extraction counts validated; all flagged question-stem groups remain untouched.")
    return data


def _normalize_value(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    return value


def _normalize_row(row: dict[str, Any]) -> dict[str, Any]:
    return {key: _normalize_value(value) for key, value in row.items()}


def _records_for_compare(conn, table: str) -> list[dict[str, Any]]:
    model = MODEL_BY_TABLE[table]
    return [_normalize_row(dict(row)) for row in conn.execute(select(model.__table__)).mappings().all()]


def _count_tables(conn, tables: tuple[str, ...]) -> dict[str, int]:
    return {
        table: int(conn.execute(text(f'SELECT count(*) FROM "{table}"')).scalar_one())
        for table in tables
    }


def _protected_counts(conn) -> dict[str, tuple[int, int | None]]:
    results = {}
    for table in PROTECTED_TABLES:
        if table == "users":
            total, admins = conn.execute(text(
                "SELECT count(*),count(*) FILTER (WHERE is_admin) FROM users"
            )).one()
            results[table] = (int(total), int(admins))
        else:
            results[table] = (int(conn.execute(text(f'SELECT count(*) FROM "{table}"')).scalar_one()), None)
    return results


def _validate_contents(conn, data: dict[str, list[dict[str, Any]]], before_protected) -> dict[str, int]:
    counts = _count_tables(conn, CONTENT_TABLES)
    if counts != EXPECTED:
        raise RuntimeError(f"In-transaction content count validation failed: {counts!r}.")
    after_protected = _protected_counts(conn)
    if after_protected != before_protected:
        raise RuntimeError("Protected student/admin data counts changed during content import.")

    for table in CONTENT_TABLES:
        actual = _records_for_compare(conn, table)
        expected_rows = [_normalize_row(row) for row in data[table]]
        actual_by_id = {str(row["id"]): row for row in actual}
        expected_by_id = {str(row["id"]): row for row in expected_rows}
        if actual_by_id != expected_by_id:
            raise RuntimeError(f"Full row verification failed for {table}; transaction will roll back.")

    invalid_options = conn.execute(text(
        "SELECT count(*) FROM (SELECT q.id FROM questions q "
        "LEFT JOIN question_options o ON o.question_id=q.id GROUP BY q.id "
        "HAVING count(o.id)<>4 OR count(DISTINCT o.option_key)<>4 "
        "OR count(*) FILTER (WHERE o.is_correct)<>1) bad"
    )).scalar_one()
    if int(invalid_options):
        raise RuntimeError(f"Destination has {invalid_options} questions without four distinct options and one correct answer.")
    if conn.execute(text(
        "SELECT count(*) FROM questions WHERE explanation IS NULL OR btrim(explanation)=''"
    )).scalar_one():
        raise RuntimeError("Destination contains questions with missing explanations.")
    if conn.execute(text(
        "SELECT count(*) FROM chapters c LEFT JOIN subjects s ON s.id=c.subject_id "
        "LEFT JOIN subcategories sc ON sc.id=c.subcategory_id AND sc.subject_id=c.subject_id "
        "WHERE s.id IS NULL OR (c.subcategory_id IS NOT NULL AND sc.id IS NULL)"
    )).scalar_one():
        raise RuntimeError("Destination chapter foreign-key validation failed.")
    if conn.execute(text(
        "SELECT count(*) FROM questions q LEFT JOIN chapters c ON c.id=q.chapter_id WHERE c.id IS NULL"
    )).scalar_one():
        raise RuntimeError("Destination question foreign-key validation failed.")
    if conn.execute(text(
        "SELECT count(*) FROM question_options o LEFT JOIN questions q ON q.id=o.question_id WHERE q.id IS NULL"
    )).scalar_one():
        raise RuntimeError("Destination option foreign-key validation failed.")
    row = conn.execute(text(
        "SELECT count(*), count(*) FILTER (WHERE is_active), "
        "count(*) FILTER (WHERE NOT is_active), "
        "count(*) FILTER (WHERE is_active AND NOT is_pyq), "
        "count(*) FILTER (WHERE is_active AND is_pyq), "
        "count(*) FILTER (WHERE explanation IS NOT NULL AND btrim(explanation)<>''), "
        "count(*) FILTER (WHERE explanation IS NULL OR btrim(explanation)=''), "
        "count(*) FILTER (WHERE is_pyq), count(*) FILTER (WHERE pyq_year IS NOT NULL), "
        "count(*) FILTER (WHERE pyq_exam_name IS NOT NULL AND btrim(pyq_exam_name)<>''), "
        "count(*) FILTER (WHERE source IS NOT NULL AND btrim(source)<>''), "
        "count(*) FILTER (WHERE image_url IS NOT NULL AND btrim(image_url)<>''), "
        "count(*) FILTER (WHERE difficulty='EASY'), "
        "count(*) FILTER (WHERE difficulty='MEDIUM'), "
        "count(*) FILTER (WHERE difficulty='HARD') FROM questions"
    )).one()
    option_total, correct_options = conn.execute(text(
        "SELECT count(*),count(*) FILTER (WHERE is_correct) FROM question_options"
    )).one()
    metric_names = (
        "questions", "active", "inactive", "active_ordinary", "active_pyq",
        "with_explanation", "without_explanation", "pyq", "with_pyq_year",
        "with_pyq_exam", "with_source", "with_image", "easy", "medium", "hard",
    )
    verified = dict(zip(metric_names, map(int, row)))
    verified["options"] = int(option_total)
    verified["correct_options"] = int(correct_options)
    return verified


def _apply(url: URL, data: dict[str, list[dict[str, Any]]]) -> dict[str, int]:
    _stage("Neon preflight (read-only helper)")
    inspect_beta_database(url)
    engine = create_engine(url, poolclass=NullPool, pool_pre_ping=True, connect_args={"connect_timeout": 10})
    committed_counts = {}
    try:
        with engine.connect() as conn:
            with conn.begin():
                conn.execute(text("SET TRANSACTION READ WRITE"))
                identity = conn.execute(text(
                    "SELECT current_database(),current_user,current_setting('transaction_read_only')"
                )).one()
                if identity != ("neondb", "neondb_owner", "off"):
                    raise RuntimeError(f"Writable target identity check failed: {identity!r}.")
                revision = conn.execute(text("SELECT version_num FROM alembic_version")).scalar_one()
                if revision != EXPECTED_HEAD:
                    raise RuntimeError(f"Target Alembic revision is {revision!r}, expected {EXPECTED_HEAD!r}.")
                before_protected = _protected_counts(conn)
                if before_protected["users"][0] < 1 or before_protected["users"][1] < 1:
                    raise RuntimeError("Existing beta administrator was not found; aborting without writes.")
                before_counts = _count_tables(conn, CONTENT_TABLES)
                already_imported = False

                _stage("Destination ID and uniqueness preflight")
                if all(before_counts[table] == 0 for table in CONTENT_TABLES):
                    # Empty destination means no primary-key, stable-key, or option-key collision.
                    inserted = data
                else:
                    exact = True
                    for table in CONTENT_TABLES:
                        existing = _records_for_compare(conn, table)
                        expected_rows = [_normalize_row(row) for row in data[table]]
                        if {str(row["id"]): row for row in existing} != {
                            str(row["id"]): row for row in expected_rows
                        }:
                            exact = False
                            break
                    if not exact:
                        raise RuntimeError(
                            "Target contains partial, unrelated, or conflicting content; refusing replacement or merge."
                        )
                    _stage("Idempotent replay verified; no inserts required")
                    _validate_contents(conn, data, before_protected)
                    already_imported = True
                    committed_counts = before_counts

                if not already_imported:
                    # Recheck target identity in the same transaction immediately before the first insert.
                    _stage("Final destination identity check")
                    identity = conn.execute(text(
                        "SELECT current_database(),current_user,current_setting('transaction_read_only')"
                    )).one()
                    if identity != ("neondb", "neondb_owner", "off"):
                        raise RuntimeError(f"Final writable target identity check failed: {identity!r}.")

                    for table in CONTENT_TABLES:
                        _stage(f"Insert {table}")
                        model_table = MODEL_BY_TABLE[table].__table__
                        rows = inserted[table]
                        for offset in range(0, len(rows), 500):
                            conn.execute(model_table.insert(), rows[offset:offset + 500])

                    _stage("Pre-commit content, option, metadata, and foreign-key validation")
                    _validate_contents(conn, data, before_protected)
                    committed_counts = _count_tables(conn, CONTENT_TABLES)
            # SQLAlchemy commits only after all validations in the context pass.

        _stage("Post-commit read-only verification")
        with engine.connect() as conn:
            with conn.begin():
                conn.execute(text("SET TRANSACTION READ ONLY"))
                identity = conn.execute(text(
                    "SELECT current_database(),current_user,current_setting('transaction_read_only')"
                )).one()
                if identity != ("neondb", "neondb_owner", "on"):
                    raise RuntimeError("Post-commit read-only target identity verification failed.")
                verification = _validate_contents(conn, data, before_protected)
                committed_counts = _count_tables(conn, CONTENT_TABLES)
        return {"counts": committed_counts, "verification": verification}
    finally:
        engine.dispose()


def main() -> int:
    current_stage = "Initialization"

    def set_stage(stage: str) -> None:
        nonlocal current_stage
        current_stage = stage
        _stage(stage)

    try:
        set_stage("Source preflight read-only verification")
        report = _query_source(set_stage)
        data = _load_source_rows(report)
        set_stage("Neon target URL validation")
        url = beta_url_from_environment()
        result = _apply(url, data)
        print("IMPORT_COMPLETE")
        for table in CONTENT_TABLES:
            print(f"{table}: {result['counts'][table]}")
        for label, count in result["verification"].items():
            print(f"verified_{label}: {count}")
        print("Preserved existing administrator; protected user-related tables unchanged.")
        return 0
    except BetaDatabaseError as exc:
        print(f"Import stopped at {current_stage} / {exc.stage} [{exc.code}]: {_sanitize_error(str(exc))}")
        return 2
    except Exception as exc:
        print(f"Import failed at {current_stage} ({type(exc).__name__}): {_sanitize_error(str(exc))}; transaction rolled back if not committed.")
        if os.environ.get("BETA_IMPORT_DEBUG") == "1":
            print("Sanitized traceback:")
            print(_sanitize_error("".join(traceback.format_exception(type(exc), exc, exc.__traceback__)), 10000))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
