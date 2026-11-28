# -*- coding: utf-8 -*-
"""Snapshot only local ssc_prep counts before/after the Set 7 import.

Read-only. Writes a JSON snapshot under reports/.

Usage:
    # DATABASE_URL is supplied through the process environment for an isolated local database
    python backend/report_banking_maths_set7_db.py before
    python backend/report_banking_maths_set7_db.py after
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
        "mixture_alligation_mains": "ccc8b698-c154-4a6f-8aa4-35ca63dfcbe4",
        "mixture_alligation_data_interpretation": "212b5143-4215-477d-9778-de534c9d8b17",
        "ages_mains": "ead4acd9-7d06-4385-8a60-75e5f6e5339a",
        "ages_data_interpretation": "533f261f-a5db-4366-8786-640290e5c818",
        "partnership_mains": "c0dce56d-5ad9-4463-ac28-c8e00ae5d731",
        "partnership_data_interpretation": "e7a6921d-6694-4773-999d-c793b24fabcd",
    },
    "banking-po": {
        "mixture_alligation_mains": "ad6ac057-4a38-4aa9-a482-09329bb71e19",
        "mixture_alligation_data_interpretation": "49d406a5-256d-48ad-ac2c-7d75fc524b2d",
        "ages_mains": "e7088e0d-9f79-4999-b2a8-e33d72521cd5",
        "ages_data_interpretation": "3c259162-71b0-4792-af6f-26a5aec74fb1",
        "partnership_mains": "3196e56a-62d8-468e-805a-e1ef8eb533ba",
        "partnership_data_interpretation": "41601a34-a8fb-4d83-a490-3138e0739be3",
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
        raise SystemExit("usage: report_banking_maths_set7_db.py before|after")
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
        snapshot["set7_section_questions"] = cur.fetchone()[0]
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

    path = os.path.join(REPORTS, f"banking_maths_set7_db_{label}.json")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(snapshot, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    print(f"wrote {path}")
    print(
        f"questions={snapshot['table_counts'].get('questions')} "
        f"options={snapshot['table_counts'].get('question_options')} "
        f"set7={snapshot['set7_section_questions']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
