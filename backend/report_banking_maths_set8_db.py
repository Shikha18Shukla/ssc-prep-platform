# -*- coding: utf-8 -*-
"""Snapshot only local ssc_prep counts before/after the Set 8 import.

Read-only. Writes a JSON snapshot under reports/.

Usage:
    # DATABASE_URL is supplied through the process environment for an isolated local database
    python backend/report_banking_maths_set8_db.py before
    python backend/report_banking_maths_set8_db.py after
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
        "time_and_work_mains": "c715d5e0-f4a6-4b72-bb6a-75aa89d43910",
        "time_and_work_data_interpretation": "861757ce-f66f-4073-9263-ef5ba2cd5cce",
        "time_speed_and_distance_mains": "a05b925a-5cbb-47e1-9728-af69eb1d3f81",
        "simple_and_compound_interest_mains": "0dd9b558-68d0-435e-b28a-55a19cc97cfd",
        "simple_and_compound_interest_data_interpretation": "81661ae6-f422-4b96-bd50-c920fa945415",
        "pipe_and_cistern_mains": "6830cf0a-e3e7-4ed5-a752-b31de4327e0e",
    },
    "banking-po": {
        "time_and_work_mains": "f841e9d9-47c8-426f-ac88-43d2b12d3fc4",
        "time_and_work_data_interpretation": "c52a6759-9616-41ad-9fd8-872d94a17978",
        "time_speed_and_distance_mains": "46f1b0ff-2206-42be-9f01-ace3670d4d11",
        "simple_and_compound_interest_mains": "63d51e71-5f82-42b9-854c-0f40618568ff",
        "simple_and_compound_interest_data_interpretation": "e70de42e-c81d-4f35-a05d-ec42d615a223",
        "pipe_and_cistern_mains": "4e4a8f25-8c93-47b1-a3df-eec32e5427bc",
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
        raise SystemExit("usage: report_banking_maths_set8_db.py before|after")
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
        snapshot["set8_section_questions"] = cur.fetchone()[0]
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

    path = os.path.join(REPORTS, f"banking_maths_set8_db_{label}.json")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(snapshot, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    print(f"wrote {path}")
    print(
        f"questions={snapshot['table_counts'].get('questions')} "
        f"options={snapshot['table_counts'].get('question_options')} "
        f"set8={snapshot['set8_section_questions']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
