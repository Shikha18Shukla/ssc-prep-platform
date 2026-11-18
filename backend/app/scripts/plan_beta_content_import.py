"""Read-only source-to-Neon content import planner for the 81 beta chapters.

This module has no apply mode. The source connection is fixed to the explicitly
approved local ssc_prep endpoint, and both connections are forced read-only.
"""

from __future__ import annotations

import os
import ipaddress
import re
import traceback
from collections import Counter
from typing import Any

import psycopg
from dotenv import dotenv_values
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool

from app.database.ssc_catalog import SSC_CATALOG, slugify
from app.scripts.neon_beta_db import (
    BetaDatabaseError,
    beta_url_from_environment,
    inspect_beta_database,
)

SOURCE = {"host": "127.0.0.1", "port": 5432, "dbname": "ssc_prep", "user": "postgres"}
EXPECTED_GROUPS = {
    ("maths", "arithmetic-maths"): 18,
    ("maths", "advanced-maths"): 13,
    ("reasoning", None): 22,
    ("gk-gs", "science"): 28,
}
CONTENT_TABLES = ("exams", "subjects", "subcategories", "chapters", "questions", "question_options")


def _expected_chapters() -> set[tuple[str, str | None, str]]:
    expected: set[tuple[str, str | None, str]] = set()
    for subject, groups in SSC_CATALOG.items():
        for category, names in groups:
            category_slug = slugify(category) if category else None
            if (subject, category_slug) not in EXPECTED_GROUPS:
                continue
            for name in names:
                expected.add((subject, category_slug, slugify(name)))
    return expected


def _source_connect() -> psycopg.Connection:
    password = os.environ.get("PGPASSWORD")
    if not password:
        raise RuntimeError("The masked local PostgreSQL password prompt returned no password.")
    return psycopg.connect(**SOURCE, password=password, connect_timeout=8)


def _query_source(set_stage) -> dict[str, Any]:
    report: dict[str, Any] = {}
    expected = _expected_chapters()
    if len(expected) != 81 or Counter((s, c) for s, c, _ in expected) != Counter(EXPECTED_GROUPS):
        raise RuntimeError("The repository catalog does not match the fixed 81-chapter allowlist.")

    set_stage("Source connection")
    with _source_connect() as conn:
        with conn.cursor() as cur:
            set_stage("Source identity verification")
            cur.execute("SET TRANSACTION READ ONLY")
            cur.execute(
                "SELECT current_database(), current_user, inet_server_addr()::text, "
                "inet_server_port(), current_setting('transaction_read_only')"
            )
            returned_identity = cur.fetchone()
            raw_server_address = (
                str(returned_identity[2]) if returned_identity[2] is not None else None
            )
            normalized_server_address = (
                str(ipaddress.ip_interface(raw_server_address).ip)
                if raw_server_address is not None else None
            )
            identity = (
                str(returned_identity[0]) if returned_identity[0] is not None else None,
                str(returned_identity[1]) if returned_identity[1] is not None else None,
                normalized_server_address,
                int(returned_identity[3]) if returned_identity[3] is not None else None,
                str(returned_identity[4]) if returned_identity[4] is not None else None,
            )
            print(
                "Source identity returned: "
                f"current_database={identity[0]!r}, current_user={identity[1]!r}, "
                f"inet_server_addr={raw_server_address!r} (normalized={identity[2]!r}), "
                f"inet_server_port={identity[3]!r}, "
                f"transaction_read_only={identity[4]!r}"
            )
            expected_identity = ("ssc_prep", "postgres", "127.0.0.1", 5432, "on")
            if identity != expected_identity:
                raise RuntimeError(
                    "Source live identity mismatch: "
                    f"returned={identity!r}; expected={expected_identity!r}."
                )
            report["source_identity"] = identity

            set_stage("Source schema inspection")
            cur.execute(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = current_schema() AND table_type = 'BASE TABLE'"
            )
            tables = {row[0] for row in cur.fetchall()}
            required = set(CONTENT_TABLES)
            missing_tables = sorted(required - tables)
            if missing_tables:
                raise RuntimeError("Source schema is missing required content tables: " + ", ".join(missing_tables))

            set_stage("Source catalog inspection")
            cur.execute(
                "SELECT e.id::text, e.slug, s.id::text, s.slug, "
                "sc.id::text, sc.slug, c.id::text, c.name, c.slug, c.is_active, "
                "c.display_order, c.description "
                "FROM exams e JOIN subjects s ON s.exam_id=e.id "
                "JOIN chapters c ON c.subject_id=s.id "
                "LEFT JOIN subcategories sc ON sc.id=c.subcategory_id AND sc.subject_id=s.id "
                "WHERE e.slug='ssc' AND s.slug IN ('maths','reasoning','gk-gs')"
            )
            catalog_rows = cur.fetchall()
            approved = [r for r in catalog_rows if (r[3], r[5], r[8]) in expected]
            found = {(r[3], r[5], r[8]) for r in approved}
            key_counts = Counter((r[3], r[5], r[8]) for r in approved)
            missing_chapters = sorted(expected - found)
            unexpected_in_scope = sorted(
                (r[3], r[5], r[8]) for r in catalog_rows
                if (r[3] in {"maths", "reasoning"} or (r[3] == "gk-gs" and r[5] == "science"))
                and (r[3], r[5], r[8]) not in expected
            )
            report["allowlist"] = {
                "expected": len(expected), "found": len(found),
                "missing": missing_chapters, "unexpected": unexpected_in_scope,
                "duplicate_keys": sorted(key for key, count in key_counts.items() if count > 1),
                "rows": approved,
            }
            chapter_ids = [r[6] for r in approved]
            if chapter_ids:
                cur.execute(
                    "SELECT c.id::text, s.slug, sc.slug, c.name, c.slug, c.is_active, "
                    "count(DISTINCT q.id), count(DISTINCT q.id) FILTER (WHERE q.is_active), "
                    "count(DISTINCT q.id) FILTER (WHERE q.is_active AND NOT q.is_pyq), "
                    "count(DISTINCT q.id) FILTER (WHERE q.is_active AND q.is_pyq), "
                    "count(DISTINCT q.id) FILTER (WHERE q.explanation IS NOT NULL AND btrim(q.explanation)<>''), "
                    "count(DISTINCT q.id) FILTER (WHERE q.explanation IS NULL OR btrim(q.explanation)=''), "
                    "count(DISTINCT q.id) FILTER (WHERE q.is_pyq AND q.pyq_year IS NOT NULL), "
                    "count(DISTINCT q.id) FILTER (WHERE q.source IS NOT NULL AND btrim(q.source)<>''), "
                    "count(DISTINCT q.id) FILTER (WHERE q.image_url IS NOT NULL AND btrim(q.image_url)<>''), "
                    "count(DISTINCT qo.id), "
                    "count(DISTINCT q.id) FILTER (WHERE q.difficulty='EASY'), "
                    "count(DISTINCT q.id) FILTER (WHERE q.difficulty='MEDIUM'), "
                    "count(DISTINCT q.id) FILTER (WHERE q.difficulty='HARD') "
                    "FROM chapters c JOIN subjects s ON s.id=c.subject_id "
                    "LEFT JOIN subcategories sc ON sc.id=c.subcategory_id "
                    "LEFT JOIN questions q ON q.chapter_id=c.id "
                    "LEFT JOIN question_options qo ON qo.question_id=q.id "
                    "WHERE c.id = ANY(%s::uuid[]) "
                    "GROUP BY c.id,s.slug,sc.slug,c.name,c.slug,c.is_active ORDER BY s.slug,sc.slug,c.display_order,c.name",
                    (chapter_ids,),
                )
                chapter_stats = cur.fetchall()
            else:
                chapter_stats = []
            report["chapter_stats"] = chapter_stats

            set_stage("Source content counting")
            # Table row totals use fixed identifiers to avoid any dynamic SQL.
            report["source_table_counts"] = {}
            for table in CONTENT_TABLES:
                cur.execute(f'SELECT count(*) FROM "{table}"')
                report["source_table_counts"][table] = cur.fetchone()[0]

            cur.execute(
                "SELECT count(*), count(*) FILTER (WHERE is_active), "
                "count(*) FILTER (WHERE NOT is_active), "
                "count(*) FILTER (WHERE is_active AND NOT is_pyq), "
                "count(*) FILTER (WHERE is_active AND is_pyq), "
                "count(*) FILTER (WHERE NOT is_active AND NOT is_pyq), "
                "count(*) FILTER (WHERE NOT is_active AND is_pyq), "
                "count(*) FILTER (WHERE explanation IS NOT NULL AND btrim(explanation)<>''), "
                "count(*) FILTER (WHERE explanation IS NULL OR btrim(explanation)=''), "
                "count(*) FILTER (WHERE pyq_year IS NOT NULL), "
                "count(*) FILTER (WHERE pyq_exam_name IS NOT NULL AND btrim(pyq_exam_name)<>''), "
                "count(*) FILTER (WHERE source IS NOT NULL AND btrim(source)<>''), "
                "count(*) FILTER (WHERE image_url IS NOT NULL AND btrim(image_url)<>''), "
                "count(*) FILTER (WHERE difficulty='EASY'), "
                "count(*) FILTER (WHERE difficulty='MEDIUM'), "
                "count(*) FILTER (WHERE difficulty='HARD') "
                "FROM questions WHERE chapter_id=ANY(%s::uuid[])",
                (chapter_ids,),
            )
            report["question_metrics"] = cur.fetchone()

            cur.execute(
                "SELECT count(*) FROM question_options qo JOIN questions q ON q.id=qo.question_id "
                "WHERE q.chapter_id=ANY(%s::uuid[])", (chapter_ids,)
            )
            report["option_count"] = cur.fetchone()[0]
            cur.execute(
                "SELECT count(*) FROM (SELECT q.id FROM questions q "
                "LEFT JOIN question_options qo ON qo.question_id=q.id "
                "WHERE q.chapter_id=ANY(%s::uuid[]) GROUP BY q.id "
                "HAVING count(qo.id)<>4 OR count(DISTINCT qo.option_key)<>4 "
                "OR count(*) FILTER (WHERE qo.is_correct)<>1) bad", (chapter_ids,)
            )
            report["invalid_question_option_sets"] = cur.fetchone()[0]
            report["excluded_options"] = max(
                report["source_table_counts"]["question_options"] - report["option_count"], 0
            )
            cur.execute(
                "SELECT count(*) FROM (SELECT lower(regexp_replace(btrim(question_text), '\\s+', ' ', 'g')) stem "
                "FROM questions WHERE chapter_id=ANY(%s::uuid[]) GROUP BY 1 HAVING count(*)>1) d",
                (chapter_ids,),
            )
            report["duplicate_exact_stems"] = cur.fetchone()[0]
            cur.execute(
                "SELECT count(*) FROM chapters c LEFT JOIN subjects s ON s.id=c.subject_id "
                "LEFT JOIN subcategories sc ON sc.id=c.subcategory_id AND sc.subject_id=c.subject_id "
                "WHERE c.id=ANY(%s::uuid[]) AND (s.id IS NULL OR (c.subcategory_id IS NOT NULL AND sc.id IS NULL))",
                (chapter_ids,),
            )
            bad_chapters = cur.fetchone()[0]
            cur.execute(
                "SELECT count(*) FROM questions q LEFT JOIN chapters c ON c.id=q.chapter_id "
                "WHERE q.chapter_id=ANY(%s::uuid[]) AND c.id IS NULL", (chapter_ids,)
            )
            bad_questions = cur.fetchone()[0]
            cur.execute(
                "SELECT conname, convalidated FROM pg_constraint "
                "WHERE contype='f' AND conrelid::regclass::text = ANY(%s)",
                (["chapters", "questions", "question_options"],),
            )
            present_fks = {name: validated for name, validated in cur.fetchall()}
            expected_fks = {
                "chapters_subject_id_fkey", "fk_chapter_subcategory_subject",
                "questions_chapter_id_fkey", "question_options_question_id_fkey",
            }
            report["missing_or_unvalidated_foreign_keys"] = sorted(
                name for name in expected_fks if present_fks.get(name) is not True
            )
            report["foreign_key_violations"] = bad_chapters + bad_questions

            cur.execute(
                "SELECT count(*) FROM questions q WHERE NOT (q.chapter_id=ANY(%s::uuid[]))",
                (chapter_ids,),
            )
            report["excluded_questions"] = cur.fetchone()[0]
            cur.execute(
                "SELECT count(*) FROM chapters c WHERE NOT (c.id=ANY(%s::uuid[]))",
                (chapter_ids,),
            )
            report["excluded_chapters"] = cur.fetchone()[0]
    return report


def _inspect_target(set_stage) -> dict[str, Any]:
    set_stage("Neon read-only inspection")
    # The existing Neon helper enforces neondb/neondb_owner, pooled Neon, TLS,
    # live identity and read-only inspection. Load the configured URL in memory;
    # never write or print it.
    raw = dotenv_values(".env").get("DATABASE_URL")
    if not raw:
        raise BetaDatabaseError("target environment", "DATABASE_URL_MISSING", "backend/.env has no beta DATABASE_URL.")
    os.environ["DATABASE_URL"] = raw
    url = beta_url_from_environment()
    inspect_beta_database(url)
    engine = create_engine(url, poolclass=NullPool, pool_pre_ping=True, connect_args={"connect_timeout": 10})
    try:
        with engine.connect() as conn:
            with conn.begin():
                conn.execute(text("SET TRANSACTION READ ONLY"))
                identity = conn.execute(text(
                    "SELECT current_database(),current_user,inet_server_addr()::text,"
                    "current_setting('transaction_read_only')"
                )).one()
                if identity[0] != "neondb" or identity[1] != "neondb_owner" or identity[3] != "on":
                    raise BetaDatabaseError("connected identity", "TARGET_MISMATCH", "Live Neon target identity/read-only check failed.")
                counts = {}
                for table in CONTENT_TABLES:
                    counts[table] = conn.execute(text(f'SELECT count(*) FROM "{table}"')).scalar_one()
                chapters = conn.execute(text(
                    "SELECT c.id::text,s.slug,sc.slug,c.slug FROM chapters c "
                    "JOIN subjects s ON s.id=c.subject_id "
                    "LEFT JOIN subcategories sc ON sc.id=c.subcategory_id "
                    "JOIN exams e ON e.id=s.exam_id WHERE e.slug='ssc' "
                    "AND ((s.slug IN ('maths','reasoning')) OR (s.slug='gk-gs' AND sc.slug='science'))"
                )).all()
                return {"identity": identity, "counts": counts, "chapters": chapters}
    finally:
        engine.dispose()


def _print_report(source: dict[str, Any], target: dict[str, Any]) -> None:
    print("\n# Beta content import dry-run (read-only; no writes performed)")
    print("Source identity: database=ssc_prep, role=postgres, host=127.0.0.1, port=5432, transaction_read_only=on")
    print("Destination identity: database=neondb, role=neondb_owner, pooled Neon/TLS validated by existing helper")
    print("\n## Allowlist validation")
    print(f"Expected chapters: {source['allowlist']['expected']}; matched: {source['allowlist']['found']}")
    for (subject, category), expected_count in EXPECTED_GROUPS.items():
        found_count = sum(1 for r in source["allowlist"]["rows"] if r[3] == subject and r[5] == category)
        print(f"- {subject}/{category or 'direct'}: expected {expected_count}, found {found_count}")
    print(f"Missing chapter keys: {source['allowlist']['missing'] or 'none'}")
    print(f"Duplicate source chapter keys: {source['allowlist']['duplicate_keys'] or 'none'}")
    print(f"Unexpected chapter keys inside approved sections: {source['allowlist']['unexpected'] or 'none'}")
    print("\n## Approved chapter detail")
    print("Subject | Subcategory | Chapter | Active | Questions | Active Normal | Active PYQ | Options | Explanations | Missing Explanations | Easy | Medium | Hard")
    for row in source["chapter_stats"]:
        print(f"{row[1]} | {row[2] or 'direct'} | {row[3]} | {row[5]} | {row[6]} | {row[8]} | {row[9]} | {row[12]} | {row[10]} | {row[11]} | {row[13]} | {row[14]} | {row[15]}")
    print("\n## Source table totals (whole database; content tables only)")
    for table, count in source["source_table_counts"].items():
        print(f"- {table}: {count}")
    metrics = source["question_metrics"]
    labels = ("questions", "active", "inactive", "active ordinary", "active PYQ", "inactive ordinary", "inactive PYQ", "with explanation", "without explanation", "with PYQ year", "with PYQ exam", "with source", "with image", "Easy", "Medium", "Hard")
    print("\n## Approved-chapter source content")
    for label, count in zip(labels, metrics):
        print(f"- {label}: {count}")
    print(f"- Question options: {source['option_count']}")
    print(f"- Questions lacking exactly four distinct options and one correct option: {source['invalid_question_option_sets']}")
    print(f"- Exact duplicate question-stem groups: {source['duplicate_exact_stems']}")
    print(f"- Foreign-key relationship violations: {source['foreign_key_violations']}")
    print(f"- Missing or unvalidated source foreign-key constraints: {source['missing_or_unvalidated_foreign_keys'] or 'none'}")
    print(f"- Source chapters excluded from import: {source['excluded_chapters']}")
    print(f"- Source questions excluded from import: {source['excluded_questions']}")
    print(f"- Source options excluded from import: {source['excluded_options']}")
    print("\n## Destination counts (live read-only query)")
    for table, count in target["counts"].items():
        print(f"- {table}: {count}")
    expected = _expected_chapters()
    target_keys = {(r[1], r[2], r[3]) for r in target["chapters"]}
    target_allowlisted = target_keys & expected
    print(f"- Existing destination chapters in allowlist: {len(target_allowlisted)}")
    # Source UUIDs are retained unless the target already contains content.
    source_counts = {
        "exams": len({r[0] for r in source["allowlist"]["rows"]}),
        "subjects": len({r[2] for r in source["allowlist"]["rows"]}),
        "subcategories": len({r[4] for r in source["allowlist"]["rows"] if r[4]}),
        "chapters": len(source["allowlist"]["rows"]),
        "questions": metrics[0],
        "question_options": source["option_count"],
    }
    print("\n## Planned reconciliation (only approved content tables)")
    empty_target = all(target["counts"][table] == 0 for table in CONTENT_TABLES)
    for table in CONTENT_TABLES:
        dst = target["counts"][table]
        src = source_counts[table]
        if empty_target:
            print(f"- {table}: source {src}; destination {dst}; missing {src}; exact duplicates 0; ID conflicts 0")
        else:
            print(f"- {table}: source {src}; destination total {dst}; exact key/ID/content reconciliation required before counts can be classified")
    if empty_target:
        print("- Total exact duplicates: 0; total ID conflicts: 0; skipped source content: only rows outside the 81-chapter allowlist.")
    else:
        print("- Duplicate and ID-conflict totals are not inferred from row counts; exact record comparison remains required.")
    print("- Foreign-key plan: insert SSC exam → approved subjects → required subcategories → 81 chapters → questions → options; preserve source UUIDs when unused.")
    print("- Excluded tables: users, beta invitations/capacity, attempts, test questions, answers, histories, rate limits, results and all unrelated data.")
    print(f"- Source UUIDs can be preserved: {'yes' if empty_target else 'pending target ID comparison'}.")
    print(f"- Dry-run is approval-ready: {'yes' if empty_target else 'no; exact target-content reconciliation remains required'}.")
    print("\nDry-run complete. No import/apply option is available in this command.")


def _sanitize_error(value: str, limit: int = 700) -> str:
    """Redact connection credentials and keep one-line diagnostic details."""
    safe = re.sub(r"(?i)postgres(?:ql)?(?:\+\w+)?://[^\s\"'<>]+", "[DATABASE_URL REDACTED]", value)
    safe = re.sub(
        r"(?i)\b(password|passwd|pwd|token|secret|authorization|pgpassword|user|username|role)\b\s*[:=]\s*[^\s,;]+",
        r"\1=[REDACTED]",
        safe,
    )
    safe = re.sub(r"(?i)\bDATABASE_URL\s*[:=]\s*[^\s,;]+", "DATABASE_URL=[REDACTED]", safe)
    safe = re.sub(r"(?i)\b(user|username)\s+[\"'][^\"']+[\"']", r"\1 [REDACTED]", safe)
    safe = re.sub(r"(?i)\buser\s+[A-Za-z0-9_.-]+", "user [REDACTED]", safe)
    safe = re.sub(r"[\r\n\t]+", " ", safe)
    return safe[:limit]


def main() -> int:
    current_stage = "Dry-run initialization"

    def set_stage(stage: str) -> None:
        nonlocal current_stage
        current_stage = stage

    try:
        source = _query_source(set_stage)
        target = _inspect_target(set_stage)
        set_stage("Dry-run comparison")
        _print_report(source, target)
        if (
            source["allowlist"]["expected"] != source["allowlist"]["found"]
            or source["allowlist"]["missing"]
            or source["allowlist"]["unexpected"]
            or source["allowlist"]["duplicate_keys"]
        ):
            return 2
        return 0
    except BetaDatabaseError as exc:
        print(f"Dry-run failed at {current_stage} / {exc.stage} [{exc.code}]: {_sanitize_error(str(exc))}")
        return 2
    except Exception as exc:
        print(
            f"Dry-run failed at {current_stage} ({type(exc).__name__}): "
            f"{_sanitize_error(str(exc))}; no database writes were performed."
        )
        if os.environ.get("BETA_DRY_RUN_DEBUG") == "1":
            # Keep the local traceback useful while applying the same redaction
            # to exception text and any connection string fragments.
            formatted = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
            print("Sanitized traceback (BETA_DRY_RUN_DEBUG=1):")
            print(_sanitize_error(formatted, limit=10000))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
