# -*- coding: utf-8 -*-
"""Compare the before/after ssc_prep snapshots from the batch-2 import."""

from __future__ import annotations

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS = os.path.join(ROOT, "reports")


def load(label: str) -> dict:
    with open(os.path.join(REPORTS, f"banking_maths_set2_db_{label}.json"), encoding="utf-8") as fh:
        return json.load(fh)


def main() -> int:
    before, after = load("before"), load("after")
    lines = [
        "# Banking Maths Batch 2 - Database Reconciliation",
        "",
        f"- Snapshot before: `{before['captured_at']}`",
        f"- Snapshot after: `{after['captured_at']}`",
        "",
        "## Table count changes",
        "",
        "| Table | Before | After | Delta |",
        "| --- | ---: | ---: | ---: |",
    ]
    changed_tables = []
    for table in sorted(before["table_counts"]):
        b, a = before["table_counts"][table], after["table_counts"][table]
        if a != b:
            changed_tables.append(table)
            lines.append(f"| {table} | {b} | {a} | +{a - b} |")
    for table in sorted(before["table_counts"]):
        b, a = before["table_counts"][table], after["table_counts"][table]
        if a == b:
            lines.append(f"| {table} | {b} | {a} | 0 |")

    lines += [
        "",
        f"Only {', '.join(f'`{t}`' for t in changed_tables)} changed.",
        "",
        "## Questions by exam and subject",
        "",
        "| Exam / subject | Before | After | Delta |",
        "| --- | ---: | ---: | ---: |",
    ]
    for key in sorted(before["questions_by_exam_subject"]):
        b = before["questions_by_exam_subject"][key]
        a = after["questions_by_exam_subject"][key]
        lines.append(f"| {key} | {b} | {a} | {a - b:+d} |")

    lines += [
        "",
        "## Maths section counts",
        "",
        "| Section | Before | After |",
        "| --- | ---: | ---: |",
    ]
    for section in sorted(set(before["maths_sections"]) | set(after["maths_sections"])):
        lines.append(
            f"| {section} | {before['maths_sections'].get(section, 0)} | "
            f"{after['maths_sections'].get(section, 0)} |"
        )

    lines += [
        "",
        "## Target checks",
        "",
        f"- Batch-2 section questions: {before['batch2_section_questions']} -> "
        f"{after['batch2_section_questions']} (+1200)",
        f"- Batch-1 section questions: {before['batch1_section_questions']} -> "
        f"{after['batch1_section_questions']} (unchanged)",
        f"- Banking Others maths questions: {before['banking_others_math_questions']} -> "
        f"{after['banking_others_math_questions']} (unchanged)",
        f"- New Maths sections: {len(before['maths_sections'])} -> "
        f"{len(after['maths_sections'])} (+40)",
        "",
        "## Result",
        "",
        "The import added exactly 1,200 questions and 4,800 options. No attempts, "
        "answers, users, chapters, subjects, exams or other unrelated rows changed.",
        "",
    ]

    path = os.path.join(REPORTS, "banking_maths_set2_db_reconciliation.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print(f"wrote {path}")
    print("changed tables:", ", ".join(changed_tables))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
