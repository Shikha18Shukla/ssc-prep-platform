# -*- coding: utf-8 -*-
"""Snapshot only local ssc_prep counts before/after the Set 9 import.

Read-only. Writes a JSON snapshot under reports/.

Usage:
    # DATABASE_URL is supplied through the process environment for an isolated local database
    python backend/report_banking_maths_set9_db.py before
    python backend/report_banking_maths_set9_db.py after
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
        "pipe_and_cistern_data_interpretation": "e721bca9-b0a7-4a58-8ff7-19ace7c5181d",
        "trains_mains": "d4536a1e-9bca-4b7f-a164-765261055639",
        "trains_data_interpretation": "a860fd97-1f72-4a04-a2f8-6879e5a8827c",
        "boats_and_streams_mains": "4e4348d8-24f7-4bfa-869b-8d2c7ccaf39f",
        "boats_and_streams_data_interpretation": "04572173-26ab-4ea7-8a43-5b88d6843304",
        "probability_mains": "13f877fc-bd67-416a-9d6d-368e1f7e3245",
        "probability_data_interpretation": "40ab1ced-e54b-4b01-9252-e691da893c66",
    },
    "banking-po": {
        "pipe_and_cistern_data_interpretation": "e972e9b1-cc3d-4027-a6f8-72ef551fb89c",
        "trains_mains": "42b0ffd2-63bd-4c5f-acfc-5cffee211e85",
        "trains_data_interpretation": "83a1f672-9718-40a0-bd4c-3cf8ef7b65fa",
        "boats_and_streams_mains": "6dc40aaf-9ec0-4466-995a-f841825c9bf5",
        "boats_and_streams_data_interpretation": "aa2f8a4c-1ce2-4fe5-b3eb-6c75a46c9327",
        "probability_mains": "b9c4dc55-7f29-4b2f-abf3-13739a1d9ed3",
        "probability_data_interpretation": "7d33a530-4d6e-4c33-b5e0-b2fd318d3373",
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
        raise SystemExit("usage: report_banking_maths_set9_db.py before|after")
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
        snapshot["set9_section_questions"] = cur.fetchone()[0]
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

    path = os.path.join(REPORTS, f"banking_maths_set9_db_{label}.json")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(snapshot, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    print(f"wrote {path}")
    print(
        f"questions={snapshot['table_counts'].get('questions')} "
        f"options={snapshot['table_counts'].get('question_options')} "
        f"set9={snapshot['set9_section_questions']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
