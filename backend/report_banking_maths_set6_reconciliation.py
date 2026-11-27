# -*- coding: utf-8 -*-
"""Compare the before/after local snapshots from the Set 6 import."""

from __future__ import annotations

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS = os.path.join(ROOT, "reports")

CHAPTER_KEYS = (
    "percentage_arithmetic_mains",
    "percentage_data_interpretation_mains",
    "ratio_arithmetic_mains",
    "ratio_data_interpretation_mains",
    "profit_and_loss_mains",
    "profit_and_loss_data_interpretation",
)
EXPECTED_SECTIONS = {
    f"banking_{exam}_maths_{chapter}_part_{part}": size
    for exam in ("clerk", "po")
    for chapter in CHAPTER_KEYS
    for part, size in ((1, 15), (2, 20), (3, 30), (4, 55))
}


def load(label: str) -> dict:
    with open(os.path.join(REPORTS, f"banking_maths_set6_db_{label}.json"), encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    before, after = load("before"), load("after")
    problems: list[str] = []
    lines = [
        "# Banking Maths Set 6 - Database Reconciliation",
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
        b = before["table_counts"][table]
        a = after["table_counts"][table]
        if a != b:
            changed_tables.append(table)
            lines.append(f"| {table} | {b} | {a} | {a - b:+d} |")
    for table in sorted(before["table_counts"]):
        b = before["table_counts"][table]
        a = after["table_counts"][table]
        if a == b:
            lines.append(f"| {table} | {b} | {a} | 0 |")

    expected_delta = {"questions": 1440, "question_options": 5760}
    actual_delta = {
        table: after["table_counts"].get(table, 0) - before["table_counts"].get(table, 0)
        for table in before["table_counts"]
    }
    if set(changed_tables) != set(expected_delta):
        problems.append(f"unexpected changed tables: {changed_tables}")
    for table, delta in expected_delta.items():
        if actual_delta.get(table) != delta:
            problems.append(f"{table} delta {actual_delta.get(table)}, expected +{delta}")

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
        a = after["questions_by_exam_subject"].get(key, 0)
        lines.append(f"| {key} | {b} | {a} | {a - b:+d} |")
        expected = 720 if key in {"banking-clerk/math-quant", "banking-po/math-quant"} else 0
        if a - b != expected:
            problems.append(f"{key}: delta {a - b}, expected {expected:+d}")

    lines += [
        "",
        "## Target chapters",
        "",
        "| Exam / chapter | Before | After | Delta |",
        "| --- | ---: | ---: | ---: |",
    ]
    for key in sorted(before["target_chapter_questions"]):
        b = before["target_chapter_questions"][key]
        a = after["target_chapter_questions"][key]
        lines.append(f"| {key} | {b} | {a} | {a - b:+d} |")
        if a - b != 120:
            problems.append(f"{key}: delta {a - b}, expected +120")

    lines += [
        "",
        "## Maths section counts",
        "",
        "| Section | Before | After | Expected after |",
        "| --- | ---: | ---: | ---: |",
    ]
    all_sections = sorted(set(before["maths_sections"]) | set(after["maths_sections"]))
    for section in all_sections:
        b = before["maths_sections"].get(section, 0)
        a = after["maths_sections"].get(section, 0)
        if section in EXPECTED_SECTIONS:
            expected = EXPECTED_SECTIONS[section]
            if b != 0 or a != expected:
                problems.append(f"{section}: before {b}, after {a}, expected 0 -> {expected}")
        else:
            expected = b
            if a != b:
                problems.append(f"{section}: changed from {b} to {a}; prior section must be unchanged")
        lines.append(f"| {section} | {b} | {a} | {expected} |")

    b3 = before["set6_section_questions"]
    a3 = after["set6_section_questions"]
    bp = before["prior_section_questions"]
    ap = after["prior_section_questions"]
    bo_b = before["banking_others_math_questions"]
    bo_a = after["banking_others_math_questions"]
    lines += [
        "",
        "## Target checks",
        "",
        f"- Set 6 section questions: {b3} -> {a3} (+1440)",
        f"- Prior batch section questions: {bp} -> {ap} (unchanged)",
        f"- Banking Others maths questions: {bo_b} -> {bo_a} (unchanged)",
        f"- Maths sections: {len(before['maths_sections'])} -> {len(after['maths_sections'])} (+48)",
        "",
        "## Result",
        "",
    ]
    if a3 - b3 != 1440:
        problems.append(f"Set 6 section delta {a3 - b3}, expected +1440")
    if ap != bp:
        problems.append(f"prior section questions changed from {bp} to {ap}")
    if bo_a != bo_b:
        problems.append(f"Banking Others maths changed from {bo_b} to {bo_a}")
    if len(after["maths_sections"]) - len(before["maths_sections"]) != 48:
        problems.append("expected exactly 48 new Maths sections")

    if problems:
        lines += [f"**Problems: {len(problems)}**", ""] + [f"- {problem}" for problem in problems] + [""]
    else:
        lines += [
            "The import added exactly 1,440 questions and 5,760 options across 48 new sections.",
            "No attempts, answers, users, chapters, subjects, exams or other unrelated rows changed.",
            "",
        ]

    path = os.path.join(REPORTS, "banking_maths_set6_db_reconciliation.md")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))
    print(f"wrote {path}")
    print("changed tables:", ", ".join(changed_tables))
    if problems:
        for problem in problems[:30]:
            print(" -", problem)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
