# -*- coding: utf-8 -*-
"""Snapshot only local ssc_prep counts before/after the Set 6 import.

Read-only. Writes a JSON snapshot under reports/.

Usage:
    # DATABASE_URL is supplied through the process environment for an isolated local database
    python backend/report_banking_maths_set6_db.py before
    python backend/report_banking_maths_set6_db.py after
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone

import psycopg2
from psycopg2.extensions import parse_dsn

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS = os.path.join(ROOT, "reports")

TARGET_CHAPTERS = {
    "banking-clerk": {
        "percentage_arithmetic_mains": "509af984-32cc-4ffe-8215-d1ccba497a50",
        "percentage_data_interpretation_mains": "e8616f20-e48c-4b94-b1db-1c97c1cdced3",
        "ratio_arithmetic_mains": "97c93357-1d6d-4a27-853b-3ecbe80bed31",
        "ratio_data_interpretation_mains": "d8e1ca61-2153-4348-a3ed-78a2d88556fb",
        "profit_and_loss_mains": "421f1261-a3fc-42d9-b34d-068d6075cf94",
        "profit_and_loss_data_interpretation": "1296eadd-c31f-4b80-8e8c-d93a7db0c5d0",
    },
    "banking-po": {
        "percentage_arithmetic_mains": "ad9392e5-9dc6-4a95-bdfd-3dc2535bb5fa",
        "percentage_data_interpretation_mains": "185ff46a-0597-42ba-99d9-d181c7370d34",
        "ratio_arithmetic_mains": "910deabf-04bd-4b3f-9b84-7a0b1e5eddd0",
        "ratio_data_interpretation_mains": "bd6937fc-bbec-47e5-8ead-f93cfe0f2d12",
        "profit_and_loss_mains": "cb7af300-e9c3-4e03-9713-a8f802ce6232",
        "profit_and_loss_data_interpretation": "c8f1b450-52d1-4683-b1c0-2400d70839ec",
    },
}
ALL_TARGET_IDS = sorted({value for chapters in TARGET_CHAPTERS.values() for value in chapters.values()})


def connect():
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise SystemExit("DATABASE_URL is required")
    dsn = parse_dsn(url)
    if (dsn.get("host") or "").lower() not in {"127.0.0.1", "localhost", "::1"}:
        raise SystemExit("refusing non-local host")
    if dsn.get("dbname") != "ssc_prep":
        raise SystemExit("refusing non-ssc_prep database")
    return psycopg2.connect(url)


def count(cur, table: str) -> int:
    cur.execute(f'SELECT COUNT(*) FROM "{table}"')
    return cur.fetchone()[0]


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in {"before", "after"}:
        raise SystemExit("usage: report_banking_maths_set6_db.py before|after")
    label = sys.argv[1]
    conn = connect()
    snapshot: dict = {"label": label, "captured_at": datetime.now(timezone.utc).isoformat()}
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
            ORDER BY table_name
            """
        )
        tables = [row[0] for row in cur.fetchall()]
        snapshot["table_counts"] = {table: count(cur, table) for table in tables}

        cur.execute(
            """
            SELECT e.slug, s.slug, COUNT(*)
            FROM questions q
            JOIN chapters c ON c.id = q.chapter_id
            JOIN subjects s ON s.id = c.subject_id
            JOIN exams e ON e.id = s.exam_id
            GROUP BY 1, 2 ORDER BY 1, 2
            """
        )
        snapshot["questions_by_exam_subject"] = {
            f"{exam}/{subject}": total for exam, subject, total in cur.fetchall()
        }

        cur.execute(
            """
            SELECT q.section, COUNT(*)
            FROM questions q
            WHERE q.section LIKE 'banking_%_maths_%_part_%'
            GROUP BY q.section ORDER BY q.section
            """
        )
        snapshot["maths_sections"] = dict(cur.fetchall())

        target_counts = {}
        for exam, chapters in TARGET_CHAPTERS.items():
            for key, chapter_id in chapters.items():
                cur.execute(
                    "SELECT COUNT(*) FROM questions WHERE chapter_id = %s",
                    (chapter_id,),
                )
                target_counts[f"{exam}/{key}"] = cur.fetchone()[0]
        snapshot["target_chapter_questions"] = target_counts

        cur.execute(
            """
            SELECT COUNT(*)
            FROM questions q
            WHERE q.chapter_id = ANY(%s::uuid[])
              AND q.section LIKE %s
            """,
            (ALL_TARGET_IDS, "banking_%_maths_%_part_%"),
        )
        snapshot["set6_section_questions"] = cur.fetchone()[0]
        cur.execute(
            """
            SELECT COUNT(*)
            FROM questions q
            WHERE q.section LIKE %s
              AND q.chapter_id <> ALL(%s::uuid[])
            """,
            ("banking_%_maths_%_part_%", ALL_TARGET_IDS),
        )
        snapshot["prior_section_questions"] = cur.fetchone()[0]
        cur.execute(
            """
            SELECT COUNT(*)
            FROM questions q
            JOIN chapters c ON c.id = q.chapter_id
            JOIN subjects s ON s.id = c.subject_id
            JOIN exams e ON e.id = s.exam_id
            WHERE e.slug = 'banking-others' AND s.slug = 'math-quant'
            """
        )
        snapshot["banking_others_math_questions"] = cur.fetchone()[0]
    finally:
        conn.close()

    path = os.path.join(REPORTS, f"banking_maths_set6_db_{label}.json")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(snapshot, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    print(f"wrote {path}")
    print(
        f"questions={snapshot['table_counts'].get('questions')} "
        f"options={snapshot['table_counts'].get('question_options')} "
        f"set6={snapshot['set6_section_questions']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
