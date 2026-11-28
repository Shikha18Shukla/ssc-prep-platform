# -*- coding: utf-8 -*-
"""Independently verify Banking Maths Set 7 (6 x 120 questions).

This script never trusts ``correct_answer``. Every result is recomputed from
``verification_data.inputs`` using separate formula sheets in
``maths_set7/formulas_*.py``. It also validates the exact JSON schema,
deterministic IDs, part counts, four distinct options, answer/index agreement,
difficulty separation, explanations, provenance and inline DI data.

Run:
    python backend/verify_banking_maths_set7_questions.py
"""

from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND = os.path.join(ROOT, "backend")
if BACKEND not in sys.path:
    sys.path.insert(0, BACKEND)

from maths_set7.formulas import FORMULAS  # noqa: E402

DATA = os.path.join(ROOT, "data")
FILES = {
    "Mixture and Alligation (Mains)": "banking_maths_mixture_alligation_mains_questions.json",
    "Mixture and Alligation – Data Interpretation": "banking_maths_mixture_alligation_di_questions.json",
    "Ages (Mains)": "banking_maths_ages_mains_questions.json",
    "Ages – Data Interpretation": "banking_maths_ages_di_questions.json",
    "Partnership (Mains)": "banking_maths_partnership_mains_questions.json",
    "Partnership – Data Interpretation": "banking_maths_partnership_di_questions.json",
}
CHAPTER_KEYS = {
    "Mixture and Alligation (Mains)": "mixture_alligation_mains",
    "Mixture and Alligation – Data Interpretation": "mixture_alligation_data_interpretation",
    "Ages (Mains)": "ages_mains",
    "Ages – Data Interpretation": "ages_data_interpretation",
    "Partnership (Mains)": "partnership_mains",
    "Partnership – Data Interpretation": "partnership_data_interpretation",
}
PART_SIZES = {1: 15, 2: 20, 3: 30, 4: 55}
LETTERS = "ABCD"
MAINS_CHAPTERS = {
    "Mixture and Alligation (Mains)",
    "Ages (Mains)",
    "Partnership (Mains)",
}
DI_CHAPTERS = set(FILES) - MAINS_CHAPTERS
EXPECTED_KEYS = {
    "id", "chapter", "chapter_key", "part", "section", "question_text",
    "options", "correct_option", "correct_answer", "explanation",
    "difficulty", "source_name", "source_url", "source_page",
    "source_type", "exam_year", "verification_status", "verification_method",
    "verification_data", "provenance_note",
}
EXTERNAL_REFERENCE = re.compile(
    r"\b(the|above|following)\b.*\b(table|graph|chart|passage|information|data)\b",
    re.I,
)
NUMBER_RE = re.compile(r"\d+(?:\.\d+)?")


def expected_answer(item: dict) -> str:
    verification = item["verification_data"]
    family = verification["family"]
    if family not in FORMULAS:
        raise KeyError(f"no independent formula for family {family!r}")
    return FORMULAS[family](verification["inputs"])


def main() -> int:
    failures: list[str] = []
    total = 0
    seen_ids: set[str] = set()
    difficulty_counts: Counter = Counter()
    requested = sys.argv[1] if len(sys.argv) > 1 else None
    if requested:
        reverse = {key: name for name, key in CHAPTER_KEYS.items()}
        if requested not in reverse:
            print(f"unknown chapter key {requested!r}")
            return 2
        chapter_name = reverse[requested]
        selected = {chapter_name: FILES[chapter_name]}
    else:
        selected = dict(FILES)
    for chapter, filename in selected.items():
        with open(os.path.join(DATA, filename), encoding="utf-8") as handle:
            items = json.load(handle)
        if len(items) != 120:
            failures.append(f"{filename}: {len(items)} items, expected 120")
        counts = Counter(item.get("part") for item in items)
        if dict(counts) != PART_SIZES:
            failures.append(f"{filename}: part counts {dict(counts)}")
        families: Counter = Counter()
        for index, item in enumerate(items, start=1):
            item_id = item.get("id", "<missing>")
            total += 1
            families[item["verification_data"]["family"]] += 1
            difficulty_counts[(chapter, item.get("difficulty"))] += 1
            expected_id = f"{CHAPTER_KEYS[chapter]}-{index:04d}"
            if item_id != expected_id:
                failures.append(f"{item_id}: non-deterministic id, expected {expected_id}")
            if item_id in seen_ids:
                failures.append(f"{item_id}: duplicate id")
            seen_ids.add(item_id)
            if set(item) != EXPECTED_KEYS:
                missing = sorted(EXPECTED_KEYS - set(item))
                extra = sorted(set(item) - EXPECTED_KEYS)
                failures.append(f"{item_id}: schema mismatch missing={missing} extra={extra}")
            if item.get("chapter") != chapter:
                failures.append(f"{item_id}: wrong chapter")
            if item.get("chapter_key") != CHAPTER_KEYS[chapter]:
                failures.append(f"{item_id}: wrong chapter_key")
            if item.get("section") != f"{CHAPTER_KEYS[chapter]}_part_{item.get('part')}":
                failures.append(f"{item_id}: wrong section")
            options = item.get("options")
            if not isinstance(options, list) or len(options) != 4 or len(set(options)) != 4:
                failures.append(f"{item_id}: options are not four distinct values")
                continue
            letter = item.get("correct_option")
            if letter not in LETTERS:
                failures.append(f"{item_id}: invalid correct_option {letter!r}")
                continue
            if options[LETTERS.index(letter)] != item.get("correct_answer"):
                failures.append(f"{item_id}: answer/option letter mismatch")
            if not str(item.get("explanation", "")).strip():
                failures.append(f"{item_id}: missing explanation")
            if item.get("source_type") != "ORIGINAL_VERIFIED":
                failures.append(f"{item_id}: source_type is not ORIGINAL_VERIFIED")
            if item.get("verification_status") != "VERIFIED":
                failures.append(f"{item_id}: verification_status is not VERIFIED")
            if item.get("exam_year") is not None:
                failures.append(f"{item_id}: exam_year is not null")
            if "set7" not in str(item.get("verification_method", "")).lower():
                failures.append(f"{item_id}: verification_method does not name Set 7")
            if chapter in MAINS_CHAPTERS and item.get("difficulty") != "HARD":
                failures.append(f"{item_id}: Mains chapter item is not HARD")
            if chapter in DI_CHAPTERS and item.get("difficulty") not in {"EASY", "MEDIUM"}:
                failures.append(f"{item_id}: Prelims DI item is not EASY/MEDIUM")
            text = str(item.get("question_text", ""))
            if chapter in DI_CHAPTERS:
                if "Data:" not in text:
                    failures.append(f"{item_id}: DI data not embedded in question text")
                if EXTERNAL_REFERENCE.search(text):
                    failures.append(f"{item_id}: DI question references external data")
                if len(NUMBER_RE.findall(text)) < 2:
                    failures.append(f"{item_id}: DI question has too few inline values")
            try:
                computed = expected_answer(item)
            except Exception as exc:
                failures.append(f"{item_id}: recomputation failed: {exc}")
                continue
            if computed != item.get("correct_answer"):
                failures.append(
                    f"{item_id}: recomputed {computed!r} != stored {item.get('correct_answer')!r}"
                )
        if len(families) != 24 or any(count != 5 for count in families.values()):
            failures.append(f"{filename}: expected 24 families x 5 variants, got {len(families)} families")

    print(f"verified {total} questions across {len(selected)} chapters")
    print("families per chapter: 24; variants per family: 5")
    for chapter in selected:
        hard = difficulty_counts[(chapter, "HARD")]
        easy = difficulty_counts[(chapter, "EASY")]
        medium = difficulty_counts[(chapter, "MEDIUM")]
        if chapter in MAINS_CHAPTERS:
            print(f"{chapter}: HARD={hard}, EASY=0, MEDIUM=0")
        else:
            print(f"{chapter}: EASY={easy}, MEDIUM={medium}, HARD=0")
    if failures:
        print(f"FAILED {len(failures)} checks:")
        for failure in failures[:100]:
            print(" -", failure)
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
