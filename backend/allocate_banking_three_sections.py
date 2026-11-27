"""Allocate existing Banking Clerk/PO chapter questions into three sections.

The script is transactional and idempotent. It only updates ``questions.section``;
it never inserts, deletes, or rewrites question content. Pass ``--commit`` to
write. Without it, the script performs all safety checks in dry-run mode.
"""

from __future__ import annotations

import argparse
import os
from collections import Counter, defaultdict
from pathlib import Path

from psycopg import connect
from psycopg.rows import dict_row

from banking_three_sections_common import (
    EXAM_SLUGS,
    SECTION_COUNTS,
    SUBJECT_SLUGS,
    expected_sections,
    normalize_question_text,
    plan_allocation,
    split_allocation,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = PROJECT_ROOT / "reports"

QUERY = """
SELECT
    e.slug AS exam_slug,
    s.slug AS subject_slug,
    c.id::text AS chapter_id,
    c.slug AS chapter_slug,
    c.name AS chapter_name,
    q.id::text AS question_id,
    q.question_text AS question_text,
    q.is_active AS is_active,
    q.section AS section,
    q.created_at AS created_at
FROM exams e
JOIN subjects s ON s.exam_id = e.id
JOIN chapters c ON c.subject_id = s.id
LEFT JOIN questions q ON q.chapter_id = c.id
WHERE e.slug = ANY(%s) AND s.slug = ANY(%s)
ORDER BY e.slug, s.display_order, c.display_order, c.slug, q.created_at, q.id
"""


def build_plans(conn) -> tuple[list[dict], list[dict], list[str]]:
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(QUERY, (list(EXAM_SLUGS), list(SUBJECT_SLUGS)))
        rows = cur.fetchall()

    chapters: dict[tuple[str, str, str], dict] = {}
    for row in rows:
        chapter_key = (row["exam_slug"], row["subject_slug"], row["chapter_id"])
        chapters.setdefault(chapter_key, {
            "exam_slug": row["exam_slug"],
            "subject_slug": row["subject_slug"],
            "chapter_id": row["chapter_id"],
            "chapter_slug": row["chapter_slug"],
            "chapter_name": row["chapter_name"],
            "rows": [],
        })
        if row["question_id"] is not None:
            chapters[chapter_key]["rows"].append(row)

    plans: list[dict] = []
    shortages: list[dict] = []
    for chapter in chapters.values():
        active_rows = [row for row in chapter["rows"] if row["is_active"]]
        chosen, _ = plan_allocation(active_rows)
        if len(chosen) < sum(SECTION_COUNTS):
            unique_texts = {normalize_question_text(row["question_text"]) for row in active_rows}
            shortages.append({
                **{k: chapter[k] for k in ("exam_slug", "subject_slug", "chapter_slug", "chapter_name")},
                "usable": len(unique_texts),
                "shortage": sum(SECTION_COUNTS) - len(unique_texts),
            })
            continue
        sections = expected_sections(chapter["exam_slug"], chapter["subject_slug"], chapter["chapter_slug"])
        split = split_allocation(chosen)
        plan_sections = [
            {
                "name": sections[index],
                "part": index + 1,
                "count": SECTION_COUNTS[index],
                "ids": split[f"part_{index + 1}"],
            }
            for index in range(3)
        ]
        planned_set = set(chosen)
        surplus = [
            row["question_id"] for row in active_rows
            if row["question_id"] not in planned_set
        ]
        plans.append({
            **{k: chapter[k] for k in ("exam_slug", "subject_slug", "chapter_id", "chapter_slug", "chapter_name")},
            "sections": plan_sections,
            "surplus_ids": surplus,
        })

    return plans, shortages, [name for plan in plans for section in plan["sections"] for name in [section["name"]]]


def safety_checks(conn, plans: list[dict], section_names: list[str]) -> None:
    expected_by_section: dict[str, dict] = {}
    expected_by_question: dict[str, str] = {}
    for plan in plans:
        for section in plan["sections"]:
            expected_by_section[section["name"]] = {
                "chapter_id": plan["chapter_id"],
                "ids": set(section["ids"]),
                "count": section["count"],
                "exam_slug": plan["exam_slug"],
                "subject_slug": plan["subject_slug"],
                "chapter_slug": plan["chapter_slug"],
            }
            for question_id in section["ids"]:
                expected_by_question[question_id] = section["name"]

    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            "SELECT id::text AS id, section, chapter_id::text AS chapter_id, is_active "
            "FROM questions WHERE section = ANY(%s)",
            (section_names,),
        )
        existing_by_section: dict[str, list[dict]] = defaultdict(list)
        for row in cur.fetchall():
            existing_by_section[row["section"]].append(row)

    for name, rows in existing_by_section.items():
        expected = expected_by_section[name]
        allowed_ids = expected["ids"]
        for row in rows:
            if row["chapter_id"] != expected["chapter_id"] or row["id"] not in allowed_ids or not row["is_active"]:
                raise RuntimeError(f"section collision or unexpected existing row: {name}")

    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            "SELECT id::text AS id, section, chapter_id::text AS chapter_id, is_active "
            "FROM questions WHERE id = ANY(%s)",
            (list(expected_by_question),),
        )
        current_questions = {row["id"]: row for row in cur.fetchall()}
    for question_id, target_section in expected_by_question.items():
        row = current_questions.get(question_id)
        if row is None:
            raise RuntimeError(f"planned question no longer exists: {question_id}")
        if not row["is_active"] or row["chapter_id"] != expected_by_section[target_section]["chapter_id"]:
            raise RuntimeError(f"planned question is no longer eligible: {question_id}")
        if row["section"] not in (None, "", target_section):
            raise RuntimeError(f"planned question belongs to another section: {question_id}")

    surplus_ids = [question_id for plan in plans for question_id in plan["surplus_ids"]]
    if surplus_ids:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                "SELECT id::text AS id, section FROM questions WHERE id = ANY(%s)",
                (surplus_ids,),
            )
            surplus_rows = cur.fetchall()
        assigned_surplus = [row["id"] for row in surplus_rows if row["section"] not in (None, "")]
        if assigned_surplus:
            raise RuntimeError(f"surplus questions already have sections: {len(assigned_surplus)}")


def apply_and_verify(conn, plans: list[dict], section_names: list[str]) -> int:
    changed = 0
    with conn.cursor(row_factory=dict_row) as cur:
        for plan in plans:
            for section in plan["sections"]:
                for question_id in section["ids"]:
                    cur.execute(
                        "UPDATE questions SET section = %s "
                        "WHERE id = %s::uuid AND (section IS DISTINCT FROM %s)",
                        (section["name"], question_id, section["name"]),
                    )
                    changed += cur.rowcount

        for section_name in section_names:
            cur.execute(
                "SELECT count(*) AS total, count(*) FILTER (WHERE is_active) AS active "
                "FROM questions WHERE section = %s",
                (section_name,),
            )
            row = cur.fetchone()
            if row is None or row["total"] != row["active"]:
                raise RuntimeError(f"inactive row found in section: {section_name}")

            cur.execute(
                "SELECT id::text AS id FROM questions WHERE section = %s AND is_active",
                (section_name,),
            )
            actual = {item["id"] for item in cur.fetchall()}
            expected = expected_by_section_from_plans(plans)[section_name]["ids"]
            if actual != expected:
                raise RuntimeError(f"section content mismatch after update: {section_name}")

        cur.execute(
            "SELECT section, count(DISTINCT chapter_id) AS chapters "
            "FROM questions WHERE section = ANY(%s) GROUP BY section",
            (section_names,),
        )
        multi_chapter = [row["section"] for row in cur.fetchall() if row["chapters"] != 1]
        if multi_chapter:
            raise RuntimeError(f"section reused across chapters: {multi_chapter}")

        surplus_ids = [question_id for plan in plans for question_id in plan["surplus_ids"]]
        if surplus_ids:
            cur.execute(
                "SELECT count(*) AS assigned FROM questions "
                "WHERE id = ANY(%s) AND section IS NOT NULL AND section <> ''",
                (surplus_ids,),
            )
            if cur.fetchone()["assigned"]:
                raise RuntimeError("surplus questions were unexpectedly assigned")

    return changed


def expected_by_section_from_plans(plans: list[dict]) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for plan in plans:
        for section in plan["sections"]:
            result[section["name"]] = {
                "chapter_id": plan["chapter_id"],
                "ids": set(section["ids"]),
                "count": section["count"],
            }
    return result


def write_report(plans: list[dict], shortages: list[dict], changed: int, committed: bool) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    name = "banking_three_section_allocation_report.md" if committed else "banking_three_section_allocation_dry_run.md"
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for plan in plans:
        grouped[(plan["exam_slug"], plan["subject_slug"])].append(plan)

    report = [
        "# Banking Three-Section Allocation Report" if committed else "# Banking Three-Section Allocation Dry Run",
        "",
        "Mode: **live allocation**." if committed else "Mode: **dry run, no writes**.",
        "",
        "Only `questions.section` is updated. Questions are never inserted, deleted, or rewritten. Section names follow `<exam>_<subject>_<chapter>_part_<1|2|3>` and are globally unique across the question bank.",
        "",
        f"Rows changed: **{changed}**. Questions allocated: **{sum(len(section['ids']) for plan in plans for section in plan['sections'])}**. Surplus questions left unassigned: **{sum(len(plan['surplus_ids']) for plan in plans)}**. Shortage chapters skipped: **{len(shortages)}**.",
        "",
        "## Grouped totals",
        "",
        "| Exam | Subject | Chapters | Allocated | Surplus preserved |",
        "| --- | --- | ---: | ---: | ---: |",
    ]
    for (exam, subject), rows in sorted(grouped.items()):
        report.append(
            f"| {exam} | {subject} | {len(rows)} | "
            f"{sum(len(section['ids']) for plan in rows for section in plan['sections'])} | "
            f"{sum(len(plan['surplus_ids']) for plan in rows)} |"
        )

    report.extend([
        "",
        "## Per-chapter allocation",
        "",
        "| Exam | Subject | Chapter | Section 1 | Section 2 | Section 3 | Surplus preserved |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: |",
    ])
    for plan in sorted(plans, key=lambda item: (item["exam_slug"], item["subject_slug"], item["chapter_slug"])):
        counts = [section["count"] for section in plan["sections"]]
        report.append(
            f"| {plan['exam_slug']} | {plan['subject_slug']} | {plan['chapter_slug']} | "
            f"{counts[0]} | {counts[1]} | {counts[2]} | {len(plan['surplus_ids'])} |"
        )

    report.extend(["", "## Shortage chapters", ""])
    if shortages:
        report.extend([
            "| Exam | Subject | Chapter | Usable | Shortfall |",
            "| --- | --- | --- | ---: | ---: |",
        ])
        for row in shortages:
            report.append(
                f"| {row['exam_slug']} | {row['subject_slug']} | {row['chapter_slug']} | "
                f"{row['usable']} | {row['shortage']} |"
            )
    else:
        report.append("None.")

    report.extend(["", "## Verification", ""])
    if committed:
        report.extend([
            "Post-update checks confirmed each section contains exactly its assigned active questions, no inactive rows are assigned, no section is used by more than one chapter, and every surplus question remains unassigned.",
        ])
    else:
        report.extend([
            "Dry-run checks confirmed the deterministic plan, eligibility, global section uniqueness, and absence of collisions before any write.",
        ])
    report.append("")
    (REPORT_DIR / name).write_text("\n".join(report), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--commit", action="store_true", help="write the allocation to the local database")
    args = parser.parse_args()

    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise SystemExit("DATABASE_URL must be set to the local development database")
    if args.commit and ".env" in database_url:
        raise SystemExit("refusing to write using a file-based configuration")

    with connect(database_url) as conn:
        if not args.commit:
            conn.read_only = True
        plans, shortages, section_names = build_plans(conn)
        safety_checks(conn, plans, section_names)
        changed = apply_and_verify(conn, plans, section_names) if args.commit else 0

    write_report(plans, shortages, changed, args.commit)
    print(
        f"{'allocation' if args.commit else 'dry run'} OK: {len(plans)} chapters, "
        f"{sum(len(section['ids']) for plan in plans for section in plan['sections'])} questions, "
        f"{changed} rows changed, {len(shortages)} shortages"
    )


if __name__ == "__main__":
    main()
