# -*- coding: utf-8 -*-
"""Idempotently import the second Banking Maths batch into Clerk and PO.

Five datasets, 120 verified questions each, split into four parts per chapter:

    banking_<exam>_maths_<chapter_key>_part_<1..4>

Only Banking Clerk and Banking PO are touched.  Banking Others is never read or
written.  Section names are unique per exam because the test service filters by
``Question.section`` alone.

Every row gets a deterministic UUID derived from the exam slug and the dataset
question id, so re-running updates the same rows instead of duplicating them.
The import is one transaction and rolls back if any post-import check fails.

Usage:
    $env:DATABASE_URL = "postgresql://postgres@127.0.0.1:5432/ssc_prep"
    python backend/import_banking_maths_set2_questions.py --dry-run
    python backend/import_banking_maths_set2_questions.py
"""

from __future__ import annotations

import json
import os
import sys
import uuid
from collections import Counter

import psycopg2
from psycopg2.extensions import parse_dsn

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

EXAMS = {
    "banking-clerk": "Banking Clerk",
    "banking-po": "Banking PO",
}

CHAPTERS = {
    "quadratic_equations": ("quadratic-equations", "Quadratic Equations"),
    "number_system": ("number-system", "Number System"),
    "percentage": ("percentage", "Percentage"),
    "ratio_proportion": ("ratio-and-proportion", "Ratio and Proportion"),
    "profit_loss_discount": ("profit-loss-and-discount", "Profit, Loss and Discount"),
}

FILES = {
    "quadratic_equations": "banking_maths_quadratic_equations_questions.json",
    "number_system": "banking_maths_number_system_questions.json",
    "percentage": "banking_maths_percentage_questions.json",
    "ratio_proportion": "banking_maths_ratio_proportion_questions.json",
    "profit_loss_discount": "banking_maths_profit_loss_discount_questions.json",
}

PART_SIZES = {1: 15, 2: 20, 3: 30, 4: 55}
EXPECTED_TOTAL = 120 * len(CHAPTERS) * len(EXAMS)
SOURCE_LABEL = (
    "Original verified question; topic reference: PW Banking Wallah class notes "
    "and Guidely topic-wise sets (not a PYQ)"
)


def fail(message: str) -> None:
    raise SystemExit("ERROR: " + message)


def load_datasets() -> dict[str, list[dict]]:
    datasets: dict[str, list[dict]] = {}
    for key, filename in FILES.items():
        path = os.path.join(DATA, filename)
        if not os.path.exists(path):
            fail(f"missing dataset {path}")
        items = json.load(open(path, encoding="utf-8"))
        if len(items) != 120:
            fail(f"{filename}: expected 120 questions, found {len(items)}")
        texts = [item["question_text"].strip().lower() for item in items]
        if len(set(texts)) != len(texts):
            fail(f"{filename}: duplicate question text inside the dataset")
        for part, size in PART_SIZES.items():
            count = sum(1 for item in items if item["part"] == part)
            if count != size:
                fail(f"{filename}: part {part} has {count} questions, expected {size}")
        for item in items:
            if item.get("chapter_key") != key:
                fail(f"{filename}: question {item.get('id')} has wrong chapter_key")
            if item.get("verification_status") != "VERIFIED":
                fail(f"{filename}: question {item.get('id')} is not VERIFIED")
            options = item.get("options", [])
            if len(options) != 4 or len(set(options)) != 4:
                fail(f"{filename}: question {item.get('id')} does not have 4 unique options")
            letter = item.get("correct_option")
            if letter not in ("A", "B", "C", "D"):
                fail(f"{filename}: question {item.get('id')} has invalid correct_option")
            if options["ABCD".index(letter)] != item.get("correct_answer"):
                fail(f"{filename}: question {item.get('id')} answer/option mismatch")
            if not item.get("explanation", "").strip():
                fail(f"{filename}: question {item.get('id')} has no explanation")
            if item.get("exam_year") is not None:
                fail(f"{filename}: question {item.get('id')} carries an exam year")
        datasets[key] = items
    return datasets


def stable_id(exam_slug: str, item_id: str) -> str:
    return str(
        uuid.uuid5(
            uuid.NAMESPACE_URL,
            f"https://ssc-prep.local/banking-maths/{exam_slug}/{item_id}",
        )
    )


def section_prefix(exam_slug: str, chapter_key: str) -> str:
    return f"{exam_slug.replace('-', '_')}_maths_{chapter_key}"


def section_name(exam_slug: str, chapter_key: str, part: int) -> str:
    return f"{section_prefix(exam_slug, chapter_key)}_part_{part}"


def connect():
    url = os.environ.get("DATABASE_URL")
    if not url:
        fail("DATABASE_URL must be set to the local ssc_prep database")
    dsn = parse_dsn(url)
    host = (dsn.get("host") or "").lower()
    dbname = dsn.get("dbname")
    if host not in {"127.0.0.1", "localhost", "::1"}:
        fail(f"refusing to write to non-local host {host!r}")
    if dbname != "ssc_prep":
        fail(f"refusing to write to database {dbname!r}; expected ssc_prep")
    conn = psycopg2.connect(url)
    conn.autocommit = False
    return conn


def resolve_chapters(cur) -> dict[tuple[str, str], str]:
    resolved: dict[tuple[str, str], str] = {}
    for exam_slug in EXAMS:
        for chapter_key, (chapter_slug, expected_name) in CHAPTERS.items():
            cur.execute(
                """
                SELECT c.id, c.name
                FROM chapters c
                JOIN subjects s ON s.id = c.subject_id
                JOIN exams e ON e.id = s.exam_id
                WHERE e.slug = %s
                  AND s.slug = 'math-quant'
                  AND c.slug = %s
                  AND c.is_active = true
                """,
                (exam_slug, chapter_slug),
            )
            rows = cur.fetchall()
            if len(rows) != 1:
                fail(
                    f"expected exactly one active chapter for {exam_slug}/{chapter_slug}, "
                    f"found {len(rows)}"
                )
            chapter_id, chapter_name = rows[0]
            if chapter_name.strip().lower() != expected_name.lower():
                fail(
                    f"chapter name mismatch for {exam_slug}/{chapter_slug}: "
                    f"{chapter_name!r} != {expected_name!r}"
                )
            resolved[(exam_slug, chapter_key)] = str(chapter_id)
    return resolved


def preflight(cur, datasets, chapters) -> None:
    planned_ids = {
        stable_id(exam_slug, item["id"])
        for exam_slug in EXAMS
        for items in datasets.values()
        for item in items
    }
    if len(planned_ids) != EXPECTED_TOTAL:
        fail(f"planned {len(planned_ids)} unique IDs, expected {EXPECTED_TOTAL}")

    # Never mix our bank with pre-existing questions in the target chapters.
    for (exam_slug, chapter_key), chapter_id in chapters.items():
        cur.execute(
            "SELECT COUNT(*) FROM questions WHERE chapter_id = %s",
            (chapter_id,),
        )
        existing = cur.fetchone()[0]
        if existing:
            cur.execute(
                "SELECT COUNT(*) FROM questions WHERE chapter_id = %s AND id = ANY(%s::uuid[])",
                (chapter_id, list(planned_ids)),
            )
            ours = cur.fetchone()[0]
            if existing != ours:
                fail(
                    f"{exam_slug}/{chapter_key} already contains {existing - ours} "
                    "question(s) that this importer does not own; refusing to write"
                )
        cur.execute(
            """
            SELECT COUNT(*)
            FROM questions
            WHERE chapter_id = %s
              AND (section IS NULL OR section NOT LIKE %s)
            """,
            (chapter_id, f"{section_prefix(exam_slug, chapter_key)}_part_%"),
        )
        unexpected_sections = cur.fetchone()[0]
        if unexpected_sections:
            fail(
                f"{exam_slug}/{chapter_key}: {unexpected_sections} question(s) have a "
                "section outside this chapter's Maths parts; refusing to write"
            )


def import_rows(cur, datasets, chapters) -> Counter:
    stats = Counter()
    for exam_slug in EXAMS:
        for chapter_key, items in datasets.items():
            chapter_id = chapters[(exam_slug, chapter_key)]
            for item in items:
                qid = stable_id(exam_slug, item["id"])
                section = section_name(exam_slug, chapter_key, item["part"])
                cur.execute("SELECT chapter_id FROM questions WHERE id = %s", (qid,))
                row = cur.fetchone()
                if row is None:
                    cur.execute(
                        """
                        INSERT INTO questions
                            (id, chapter_id, question_text, explanation, difficulty,
                             is_pyq, pyq_year, pyq_exam_name, source, is_active, section)
                        VALUES (%s, %s, %s, %s, %s, false, NULL, NULL, %s, true, %s)
                        """,
                        (
                            qid,
                            chapter_id,
                            item["question_text"],
                            item["explanation"],
                            item["difficulty"],
                            SOURCE_LABEL,
                            section,
                        ),
                    )
                    stats["inserted"] += 1
                else:
                    if str(row[0]) != chapter_id:
                        fail(f"question {qid} exists in a different chapter; refusing to move it")
                    cur.execute(
                        """
                        UPDATE questions
                        SET question_text = %s,
                            explanation = %s,
                            difficulty = %s,
                            is_pyq = false,
                            pyq_year = NULL,
                            pyq_exam_name = NULL,
                            source = %s,
                            is_active = true,
                            section = %s,
                            updated_at = now()
                        WHERE id = %s
                        """,
                        (
                            item["question_text"],
                            item["explanation"],
                            item["difficulty"],
                            SOURCE_LABEL,
                            section,
                            qid,
                        ),
                    )
                    stats["updated"] += 1

                for index, key in enumerate("ABCD"):
                    cur.execute(
                        """
                        INSERT INTO question_options
                            (id, question_id, option_key, option_text, display_order, is_correct)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (question_id, option_key)
                        DO UPDATE SET option_text = EXCLUDED.option_text,
                                      display_order = EXCLUDED.display_order,
                                      is_correct = EXCLUDED.is_correct
                        """,
                        (
                            str(uuid.uuid4()),
                            qid,
                            key,
                            item["options"][index],
                            index + 1,
                            key == item["correct_option"],
                        ),
                    )
                cur.execute(
                    """
                    DELETE FROM question_options
                    WHERE question_id = %s AND option_key NOT IN ('A', 'B', 'C', 'D')
                    """,
                    (qid,),
                )
    return stats


def post_check(cur, datasets, chapters) -> list[str]:
    problems: list[str] = []
    for exam_slug in EXAMS:
        for chapter_key, items in datasets.items():
            chapter_id = chapters[(exam_slug, chapter_key)]
            for part, expected in PART_SIZES.items():
                section = section_name(exam_slug, chapter_key, part)
                cur.execute(
                    """
                    SELECT COUNT(*)
                    FROM questions
                    WHERE chapter_id = %s AND section = %s AND is_active = true
                    """,
                    (chapter_id, section),
                )
                actual = cur.fetchone()[0]
                if actual != expected:
                    problems.append(f"{section}: {actual} questions, expected {expected}")
                cur.execute(
                    """
                    SELECT COUNT(*) FROM (
                        SELECT question_text
                        FROM questions
                        WHERE chapter_id = %s AND section = %s AND is_active = true
                        GROUP BY question_text
                        HAVING COUNT(*) > 1
                    ) dupes
                    """,
                    (chapter_id, section),
                )
                if cur.fetchone()[0]:
                    problems.append(f"{section}: duplicate question text")

    target_ids = list(chapters.values())
    cur.execute(
        """
        SELECT COUNT(*)
        FROM questions q
        WHERE q.chapter_id = ANY(%s::uuid[])
          AND q.is_active = true
          AND q.section LIKE %s
        """,
        (target_ids, "banking_%_maths_%_part_%"),
    )
    total = cur.fetchone()[0]
    if total != EXPECTED_TOTAL:
        problems.append(f"total imported questions {total}, expected {EXPECTED_TOTAL}")

    cur.execute(
        """
        SELECT COUNT(*)
        FROM questions q
        WHERE q.chapter_id = ANY(%s::uuid[])
          AND q.is_active = true
          AND q.section LIKE %s
          AND (SELECT COUNT(*) FROM question_options o WHERE o.question_id = q.id) <> 4
        """,
        (target_ids, "banking_%_maths_%_part_%"),
    )
    if cur.fetchone()[0]:
        problems.append("some imported questions do not have exactly four options")

    cur.execute(
        """
        SELECT COUNT(*)
        FROM questions q
        WHERE q.chapter_id = ANY(%s::uuid[])
          AND q.is_active = true
          AND q.section LIKE %s
          AND (
              SELECT COUNT(*) FROM question_options o
              WHERE o.question_id = q.id AND o.is_correct = true
          ) <> 1
        """,
        (target_ids, "banking_%_maths_%_part_%"),
    )
    if cur.fetchone()[0]:
        problems.append("some imported questions do not have exactly one correct option")

    cur.execute(
        """
        SELECT COUNT(*)
        FROM questions q
        WHERE q.chapter_id = ANY(%s::uuid[])
          AND q.is_active = true
          AND q.section LIKE %s
          AND (q.explanation IS NULL OR btrim(q.explanation) = '')
        """,
        (target_ids, "banking_%_maths_%_part_%"),
    )
    if cur.fetchone()[0]:
        problems.append("some imported questions have no explanation")

    cur.execute(
        """
        SELECT COUNT(*)
        FROM questions q
        JOIN chapters c ON c.id = q.chapter_id
        JOIN subjects s ON s.id = c.subject_id
        JOIN exams e ON e.id = s.exam_id
        WHERE e.slug = 'banking-others'
          AND s.slug = 'math-quant'
          AND q.section LIKE %s
        """,
        ("banking_others_maths_%",),
    )
    if cur.fetchone()[0]:
        problems.append("Banking Others contains Maths questions from this batch")
    return problems


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    datasets = load_datasets()
    conn = connect()
    try:
        cur = conn.cursor()
        chapters = resolve_chapters(cur)
        preflight(cur, datasets, chapters)
        print(
            f"preflight OK: {len(chapters)} target chapters, "
            f"{EXPECTED_TOTAL} planned questions"
        )
        if dry_run:
            print("dry run: no database changes written")
            conn.rollback()
            return 0
        stats = import_rows(cur, datasets, chapters)
        problems = post_check(cur, datasets, chapters)
        if problems:
            conn.rollback()
            for problem in problems:
                print("POST-CHECK FAIL:", problem)
            fail("post-import checks failed; transaction rolled back")
        conn.commit()
        print(
            f"imported: {stats['inserted']} inserted, {stats['updated']} updated, "
            f"{EXPECTED_TOTAL} total rows"
        )
        for exam_slug in EXAMS:
            for chapter_key in CHAPTERS:
                section_counts = {
                    part: sum(1 for item in datasets[chapter_key] if item["part"] == part)
                    for part in PART_SIZES
                }
                print(f"  {exam_slug}/{chapter_key}: {section_counts}")
        return 0
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
