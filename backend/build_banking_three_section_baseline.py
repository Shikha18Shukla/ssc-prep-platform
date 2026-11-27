"""Build the read-only pre-allocation baseline for Banking three sections."""

from __future__ import annotations

import csv
import os
from collections import Counter, defaultdict
from pathlib import Path

from psycopg import connect

from banking_three_sections_common import (
    EXAM_SLUGS,
    SECTION_COUNTS,
    SECTION_COUNTS as ALLOCATED_TOTAL,
    SUBJECT_SLUGS,
    mask_numbers,
    near_duplicate_pairs,
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


def fetch_rows(database_url: str) -> list[dict]:
    with connect(database_url) as conn:
        conn.read_only = True
        with conn.cursor(row_factory=__import__("psycopg").rows.dict_row) as cur:
            cur.execute(QUERY, (list(EXAM_SLUGS), list(SUBJECT_SLUGS)))
            return cur.fetchall()


def analyse() -> tuple[list[dict], list[dict]]:
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise SystemExit("DATABASE_URL must be set to the local development database")
    rows = fetch_rows(database_url)

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

    required = sum(SECTION_COUNTS)
    results: list[dict] = []
    for chapter in chapters.values():
        all_rows = chapter["rows"]
        active_rows = [row for row in all_rows if row["is_active"]]
        all_texts = [normalize_question_text(row["question_text"]) for row in all_rows]
        active_texts = [normalize_question_text(row["question_text"]) for row in active_rows]
        all_counts = Counter(all_texts)
        active_counts = Counter(active_texts)
        masked_active = [mask_numbers(text) for text in active_texts]
        masked_counts = Counter(masked_active)
        planned_ids, plan_notes = plan_allocation(active_rows)
        allocation = split_allocation(planned_ids)
        active_unique = len(set(active_texts))
        total_rows = len(all_rows)
        distinct_ids = len({row["question_id"] for row in all_rows})
        section_counts = Counter((row["section"] or "<NULL>") for row in active_rows)
        surplus = max(active_unique - required, 0)
        shortage = max(required - active_unique, 0)
        results.append({
            **{k: chapter[k] for k in ("exam_slug", "subject_slug", "chapter_id", "chapter_slug", "chapter_name")},
            "total_questions": total_rows,
            "active_questions": len(active_rows),
            "distinct_question_ids": distinct_ids,
            "duplicate_id_rows": total_rows - distinct_ids,
            "normalized_unique_all": len(set(all_texts)),
            "normalized_unique_active": active_unique,
            "duplicate_content_groups_all": sum(1 for count in all_counts.values() if count > 1),
            "duplicate_content_groups_active": sum(1 for count in active_counts.values() if count > 1),
            "masked_template_groups_active": sum(1 for count in masked_counts.values() if count > 1),
            "near_duplicate_pairs_active": near_duplicate_pairs(active_texts),
            "active_duplicate_rows_skipped": plan_notes["duplicate_active_rows_skipped"],
            "active_sections": "; ".join(f"{name}={count}" for name, count in sorted(section_counts.items())),
            "usable_questions": active_unique,
            "allocated_questions": len(planned_ids),
            "surplus_questions": surplus,
            "shortage_questions": shortage,
            "section_1_count": len(allocation["part_1"]),
            "section_2_count": len(allocation["part_2"]),
            "section_3_count": len(allocation["part_3"]),
            "section_1_ids": ",".join(allocation["part_1"]),
            "section_2_ids": ",".join(allocation["part_2"]),
            "section_3_ids": ",".join(allocation["part_3"]),
        })
    results.sort(key=lambda row: (row["exam_slug"], row["subject_slug"], row["chapter_slug"]))
    return results, rows


def write_reports(results: list[dict]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = REPORT_DIR / "banking_three_section_baseline.csv"
    fields = list(results[0].keys())
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in results:
        grouped[(row["exam_slug"], row["subject_slug"])].append(row)

    report = [
        "# Banking Three-Section Baseline Report",
        "",
        "## Scope and method",
        "",
        "Read-only baseline captured before any allocation write. Scope: Banking Clerk and Banking PO chapters under English, General/Banking Awareness, and Computer. No other exam, subject or catalogue record is included.",
        "",
        "Usable questions are active rows with distinct normalized question text. A deterministic allocation plan selects the first 40 usable rows by creation time then question id, split 10 / 15 / 15. Duplicate normalized texts are skipped. Surplus usable rows are left unassigned and preserved.",
        "",
        "Content diagnostics use three measures: exact/normalized duplicate groups, number-masked template groups, and lexical pairs with similarity at least 0.90. Similarity flags are diagnostic, not automatic removals.",
        "",
        "## Grouped totals",
        "",
        "| Exam | Subject | Chapters | Total rows | Active rows | Active unique | Allocated | Surplus | Shortage chapters |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for (exam, subject), rows in sorted(grouped.items()):
        report.append(
            f"| {exam} | {subject} | {len(rows)} | {sum(r['total_questions'] for r in rows)} | "
            f"{sum(r['active_questions'] for r in rows)} | {sum(r['usable_questions'] for r in rows)} | "
            f"{sum(r['allocated_questions'] for r in rows)} | {sum(r['surplus_questions'] for r in rows)} | "
            f"{sum(1 for r in rows if r['shortage_questions'])} |"
        )
    total_shortage = sum(1 for row in results if row["shortage_questions"])
    report.extend([
        "",
        f"Overall: **{len(results)} chapters inspected**, "
        f"**{sum(r['allocated_questions'] for r in results)} questions planned for allocation**, "
        f"**{sum(r['surplus_questions'] for r in results)} surplus usable questions**, "
        f"**{total_shortage} shortage chapters**.",
        "",
        "## Per-chapter baseline",
        "",
        "| Exam | Subject | Chapter | Total | Active | Dup IDs | Active unique | Dup groups (all/active) | Masked groups | Near pairs | Usable | Plan | Surplus | Shortage | Sections before |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ])
    for row in results:
        report.append(
            f"| {row['exam_slug']} | {row['subject_slug']} | {row['chapter_slug']} | "
            f"{row['total_questions']} | {row['active_questions']} | {row['duplicate_id_rows']} | "
            f"{row['normalized_unique_active']} | {row['duplicate_content_groups_all']}/{row['duplicate_content_groups_active']} | "
            f"{row['masked_template_groups_active']} | {row['near_duplicate_pairs_active']} | "
            f"{row['usable_questions']} | {row['section_1_count']}/{row['section_2_count']}/{row['section_3_count']} | "
            f"{row['surplus_questions']} | {row['shortage_questions']} | {row['active_sections']} |"
        )

    surplus_rows = [row for row in results if row["surplus_questions"]]
    report.extend([
        "",
        "## Surplus chapters",
        "",
    ])
    if surplus_rows:
        report.extend([
            "| Exam | Subject | Chapter | Usable | Allocated | Surplus preserved |",
            "| --- | --- | --- | ---: | ---: | ---: |",
        ])
        for row in surplus_rows:
            report.append(
                f"| {row['exam_slug']} | {row['subject_slug']} | {row['chapter_slug']} | "
                f"{row['usable_questions']} | {row['allocated_questions']} | {row['surplus_questions']} |"
            )
    else:
        report.append("None.")

    shortage_rows = [row for row in results if row["shortage_questions"]]
    report.extend(["", "## Shortage chapters", ""])
    if shortage_rows:
        report.extend([
            "| Exam | Subject | Chapter | Usable | Shortfall |",
            "| --- | --- | --- | ---: | ---: |",
        ])
        for row in shortage_rows:
            report.append(
                f"| {row['exam_slug']} | {row['subject_slug']} | {row['chapter_slug']} | "
                f"{row['usable_questions']} | {row['shortage_questions']} |"
            )
    else:
        report.append("None. Every inspected chapter has at least 40 usable unique questions.")

    report.extend([
        "",
        "## Machine-readable plan",
        "",
        "`reports/banking_three_section_baseline.csv` records the deterministic section-1/2/3 question ids for every chapter.",
        "",
    ])
    (REPORT_DIR / "banking_three_section_baseline_report.md").write_text("\n".join(report), encoding="utf-8")


def main() -> None:
    results, _ = analyse()
    write_reports(results)
    print(
        f"baseline OK: {len(results)} chapters, "
        f"{sum(r['allocated_questions'] for r in results)} planned questions, "
        f"{sum(r['surplus_questions'] for r in results)} surplus, "
        f"{sum(1 for r in results if r['shortage_questions'])} shortages"
    )


if __name__ == "__main__":
    main()
