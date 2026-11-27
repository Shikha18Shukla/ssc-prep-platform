# -*- coding: utf-8 -*-
"""Snapshot only local ssc_prep counts before/after the Set 4 import.

Read-only. Writes a JSON snapshot under reports/.

Usage:
    $env:DATABASE_URL = "postgresql://postgres@127.0.0.1:5432/ssc_prep"
    python backend/report_banking_maths_set4_db.py before
    python backend/report_banking_maths_set4_db.py after
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
        "pipe_and_cistern": "4779a979-5652-4291-aa63-982c3557aaeb",
        "average": "f3b9593c-a548-4520-b0e5-fd4c530c2325",
        "speed_time_distance": "25824a64-6812-490d-a40f-f0098ca4e925",
        "problems_on_trains": "1438a334-cd3f-4df6-a315-5f2c29557bd2",
        "boats_and_streams": "cd13044e-d246-489d-b49f-a7da45d19845",
        "mensuration_2d": "e50bf3c4-af27-4508-a29c-e5e0e673ca23",
    },
    "banking-po": {
        "pipe_and_cistern": "6909ee61-2f7f-45a4-a076-9d2a869dedbd",
        "average": "3d43fe0f-3988-4da8-9822-da58f3701663",
        "speed_time_distance": "c12270bf-f375-4b8f-afaf-b8f478bc1b0b",
        "problems_on_trains": "03456030-fe38-4dd8-8b63-594b9af42af0",
        "boats_and_streams": "c85e3553-8dea-43b3-83d7-8a4fee388963",
        "mensuration_2d": "d6d59d57-6e87-4c98-a705-c09cb253e0c0",
    },
}

ALL_TARGET_IDS = list({value for chapters in TARGET_CHAPTERS.values() for value in chapters.values()})


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
        raise SystemExit("usage: report_banking_maths_set4_db.py before|after")
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
        snapshot["set4_section_questions"] = cur.fetchone()[0]
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

    path = os.path.join(REPORTS, f"banking_maths_set4_db_{label}.json")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(snapshot, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    print(f"wrote {path}")
    print(
        f"questions={snapshot['table_counts'].get('questions')} "
        f"options={snapshot['table_counts'].get('question_options')} "
        f"set4={snapshot['set4_section_questions']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
