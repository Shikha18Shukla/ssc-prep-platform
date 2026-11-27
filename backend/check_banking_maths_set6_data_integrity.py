# -*- coding: utf-8 -*-
"""Compare live data with the pre-import baseline, excluding Set 6 rows.

The scratch database must first be restored from the pre-import backup.  This
script hashes every table in both databases after excluding the deterministic
Set 6 question IDs (and their options), so all unrelated records are compared
by content, not just by row count.

Usage:
    # Supply SSC_PREP_LIVE_DATABASE_URL and SSC_PREP_SCRATCH_DATABASE_URL
    # through the process environment; no connection strings are stored here.
    python backend/check_banking_maths_set6_data_integrity.py
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

import psycopg2
from psycopg2.extensions import parse_dsn

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from import_banking_maths_set6_questions import EXAMS, FILES, stable_id

LIVE_URL = os.environ["SSC_PREP_LIVE_DATABASE_URL"]
SCRATCH_URL = os.environ["SSC_PREP_SCRATCH_DATABASE_URL"]
DATA = os.path.join(ROOT, "data")


def local_only(url: str) -> None:
    dsn = parse_dsn(url)
    if (dsn.get("host") or "").lower() not in {"127.0.0.1", "localhost", "::1"}:
        raise SystemExit("refusing a non-local database")


def planned_ids() -> list[str]:
    ids = set()
    for filename in FILES.values():
        with open(os.path.join(DATA, filename), encoding="utf-8") as handle:
            for item in json.load(handle):
                for exam_slug in EXAMS:
                    ids.add(stable_id(exam_slug, item["id"]))
    return sorted(ids)


def primary_key_columns(cur, table: str) -> list[str]:
    cur.execute(
        """
        SELECT kcu.column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
          ON tc.constraint_catalog = kcu.constraint_catalog
         AND tc.constraint_schema = kcu.constraint_schema
         AND tc.constraint_name = kcu.constraint_name
        WHERE tc.table_schema = 'public'
          AND tc.table_name = %s
          AND tc.constraint_type = 'PRIMARY KEY'
        ORDER BY kcu.ordinal_position
        """,
        (table,),
    )
    columns = [row[0] for row in cur.fetchall()]
    if columns:
        return columns
    cur.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = %s
        ORDER BY ordinal_position
        """,
        (table,),
    )
    return [row[0] for row in cur.fetchall()]


def encode(value) -> bytes:
    if value is None:
        return b"<NULL>"
    if isinstance(value, (datetime, date)):
        return value.isoformat().encode("utf-8")
    if isinstance(value, (UUID, Decimal)):
        return str(value).encode("utf-8")
    if isinstance(value, (dict, list)):
        return json.dumps(value, sort_keys=True, default=str).encode("utf-8")
    return str(value).encode("utf-8")


def table_hash(conn, table: str, ids: list[str]) -> tuple[str, int]:
    with conn.cursor() as cur:
        columns = primary_key_columns(cur, table)
        order = ", ".join(f'"{column}"' for column in columns)
        where = ""
        params: tuple = ()
        if table == "questions":
            where = " WHERE id <> ALL(%s::uuid[])"
            params = (ids,)
        elif table == "question_options":
            where = " WHERE question_id <> ALL(%s::uuid[])"
            params = (ids,)
        cur.execute(f'SELECT * FROM "{table}"{where} ORDER BY {order}', params)
        digest = hashlib.sha256()
        rows = 0
        for row in cur.fetchall():
            rows += 1
            row_hash = hashlib.sha256()
            for value in row:
                part = encode(value)
                row_hash.update(len(part).to_bytes(8, "big"))
                row_hash.update(part)
            digest.update(row_hash.digest())
        return digest.hexdigest(), rows


def main() -> int:
    configured = os.environ.get("DATABASE_URL")
    if not configured:
        raise SystemExit("DATABASE_URL is required")
    local_only(configured)
    local_only(LIVE_URL)
    local_only(SCRATCH_URL)

    ids = planned_ids()
    if len(ids) != 1440:
        raise SystemExit(f"expected 1440 planned Set 6 IDs, found {len(ids)}")

    live = psycopg2.connect(LIVE_URL)
    scratch = psycopg2.connect(SCRATCH_URL)
    mismatches: list[str] = []
    lines = [
        "# Banking Maths Set 6 - Unrelated Data Integrity Report",
        "",
        "The live database was compared with a restored pre-import baseline.",
        "The 1,440 deterministic Set 6 question rows and their 5,760 options were",
        "excluded; every remaining row was compared by content hash.",
        "",
        "| Table | Rows compared | Live hash | Baseline hash | Result |",
        "| --- | ---: | --- | --- | --- |",
    ]
    try:
        with live.cursor() as cur:
            cur.execute(
                """
                SELECT table_name FROM information_schema.tables
                WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
                ORDER BY table_name
                """
            )
            tables = [row[0] for row in cur.fetchall()]
        for table in tables:
            live_hash, live_rows = table_hash(live, table, ids)
            baseline_hash, baseline_rows = table_hash(scratch, table, ids)
            same = live_hash == baseline_hash and live_rows == baseline_rows
            lines.append(
                f"| {table} | {live_rows} | `{live_hash[:16]}...` | "
                f"`{baseline_hash[:16]}...` | {'SAME' if same else 'DIFFERENT'} |"
            )
            if not same:
                mismatches.append(
                    f"{table}: live {live_rows} rows / {live_hash}, "
                    f"baseline {baseline_rows} rows / {baseline_hash}"
                )
        with live.cursor() as cur:
            cur.execute(
                """
                SELECT COUNT(*)
                FROM questions q
                WHERE q.id = ANY(%s::uuid[])
                  AND q.is_active = true
                  AND q.section LIKE %s
                """,
                (ids, "banking_%_maths_%_part_%"),
            )
            set6_questions = cur.fetchone()[0]
            cur.execute(
                """
                SELECT COUNT(*) FROM question_options
                WHERE question_id = ANY(%s::uuid[])
                """,
                (ids,),
            )
            set6_options = cur.fetchone()[0]
        lines += [
            "",
            f"- Set 6 rows on the live database: {set6_questions} questions, "
            f"{set6_options} options",
            f"- Tables compared: {len(tables)}",
            "",
        ]
        if set6_questions != 1440 or set6_options != 5760:
            mismatches.append(
                f"live Set 6 rows are {set6_questions} questions / {set6_options} options"
            )
        if mismatches:
            lines += [f"## Differences ({len(mismatches)})", ""] + [
                f"- {item}" for item in mismatches
            ] + [""]
        else:
            lines += [
                "## Result",
                "",
                "ALL UNRELATED DATA UNCHANGED",
                "",
                "Banking Others, attempts, answers, users, progress, history and every",
                "other unrelated table are byte-equivalent to the pre-import baseline.",
            ]
    finally:
        live.close()
        scratch.close()

    path = os.path.join(ROOT, "reports", "banking_maths_set6_data_integrity_report.md")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))
    print(f"wrote {path}")
    if mismatches:
        for item in mismatches:
            print(" -", item)
        return 1
    print("ALL UNRELATED DATA UNCHANGED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
