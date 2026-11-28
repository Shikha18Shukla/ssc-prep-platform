# -*- coding: utf-8 -*-
"""Independently verify Banking Maths Set 9 (7 x 120 questions).

This script never trusts ``correct_answer``. Every result is recomputed from
``verification_data.inputs`` using the independent formula sheet in
``maths_set9/formulas.py``. It also validates the exact JSON schema,
deterministic IDs, part counts, four distinct options, answer/index agreement,
difficulty separation, explanations, provenance and inline DI data.

Run:
    python backend/verify_banking_maths_set9_questions.py
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

from maths_set9.family_names import FAMILY_NAMES  # noqa: E402
from maths_set9.formulas import FORMULAS  # noqa: E402

DATA = os.path.join(ROOT, "data")
FILES = {
    "Pipe and Cistern – Data Interpretation": "banking_maths_pipe_and_cistern_di_questions.json",
    "Trains (Mains)": "banking_maths_trains_mains_questions.json",
    "Trains – Data Interpretation": "banking_maths_trains_data_interpretation_questions.json",
    "Boats and Streams (Mains)": "banking_maths_boats_and_streams_mains_questions.json",
    "Boats and Streams – Data Interpretation": "banking_maths_boats_and_streams_data_interpretation_questions.json",
    "Probability (Mains)": "banking_maths_probability_mains_questions.json",
    "Probability – Data Interpretation": "banking_maths_probability_data_interpretation_questions.json",
}
CHAPTER_KEYS = {
    "Pipe and Cistern – Data Interpretation": "pipe_and_cistern_data_interpretation",
    "Trains (Mains)": "trains_mains",
    "Trains – Data Interpretation": "trains_data_interpretation",
    "Boats and Streams (Mains)": "boats_and_streams_mains",
    "Boats and Streams – Data Interpretation": "boats_and_streams_data_interpretation",
    "Probability (Mains)": "probability_mains",
    "Probability – Data Interpretation": "probability_data_interpretation",
}
MAINS_CHAPTERS = {"Trains (Mains)", "Boats and Streams (Mains)", "Probability (Mains)"}
DI_CHAPTERS = set(FILES) - MAINS_CHAPTERS
EXPECTED_SCHEMA = [
    "id", "chapter", "chapter_key", "part", "section", "question_text",
    "options", "correct_option", "correct_answer", "explanation",
    "difficulty", "source_name", "source_url", "source_page", "source_type",
    "exam_year", "verification_status", "verification_method",
    "verification_data", "provenance_note",
]
PART_SIZES = {1: 15, 2: 20, 3: 30, 4: 55}
EXTERNAL_REFERENCE = re.compile(
    r"original|class notes|pdf|pp\.|aligned|topic scope", re.IGNORECASE
)


def expected_answer(item: dict) -> str:
    data = item["verification_data"]
    return FORMULAS[data["family"]](data["inputs"])


def main() -> int:
    failures: list[str] = []
    total = 0
    seen_ids: set[str] = set()
    all_family_counts: Counter = Counter()
    for chapter, filename in FILES.items():
        path = os.path.join(DATA, filename)
        with open(path, encoding="utf-8") as fp:
            items = json.load(fp)
        if len(items) != 120:
            failures.append(f"{filename}: expected 120 items, found {len(items)}")
        counts = Counter()
        families = Counter()
        for item in items:
            total += 1
            ident = item.get("id")
            if ident in seen_ids:
                failures.append(f"duplicate dataset id {ident}")
            seen_ids.add(ident)
            if list(item.keys()) != EXPECTED_SCHEMA:
                failures.append(f"{ident}: schema mismatch")
            if item.get("chapter") != chapter or item.get("chapter_key") != CHAPTER_KEYS[chapter]:
                failures.append(f"{ident}: chapter/key mismatch")
            part = item.get("part")
            if part not in PART_SIZES:
                failures.append(f"{ident}: bad part {part}")
            counts[part] += 1
            if item.get("section") != f"{CHAPTER_KEYS[chapter]}_part_{part}":
                failures.append(f"{ident}: bad section")
            options = item.get("options")
            if not isinstance(options, list) or len(options) != 4:
                failures.append(f"{ident}: options must be a four-item list")
            elif len(set(options)) != 4:
                failures.append(f"{ident}: options are not distinct")
            correct_option = item.get("correct_option")
            if correct_option not in ("A", "B", "C", "D"):
                failures.append(f"{ident}: bad correct_option")
            elif isinstance(options, list) and item.get("correct_answer") != options["ABCD".index(correct_option)]:
                failures.append(f"{ident}: answer/index mismatch")
            if not isinstance(item.get("explanation"), str) or len(item["explanation"].strip()) < 20:
                failures.append(f"{ident}: explanation too short")
            if item.get("source_type") != "ORIGINAL_VERIFIED":
                failures.append(f"{ident}: bad source_type")
            if item.get("verification_status") != "VERIFIED":
                failures.append(f"{ident}: bad verification_status")
            if item.get("exam_year") is not None:
                failures.append(f"{ident}: exam_year must be null")
            if not EXTERNAL_REFERENCE.search(item.get("provenance_note") or ""):
                failures.append(f"{ident}: provenance lacks source reference")
            expected_family = FAMILY_NAMES[CHAPTER_KEYS[chapter]]
            vd = item.get("verification_data") or {}
            family = vd.get("family")
            families[family] += 1
            all_family_counts[family] += 1
            if family not in expected_family:
                failures.append(f"{ident}: unexpected family {family}")
            if not isinstance(vd.get("inputs"), dict):
                failures.append(f"{ident}: missing verification inputs")
            else:
                try:
                    computed = expected_answer(item)
                except Exception as exc:
                    failures.append(f"{ident}: recomputation error {exc}")
                else:
                    if computed != item.get("correct_answer"):
                        failures.append(
                            f"{ident}: answer {item.get('correct_answer')} != recomputed {computed}"
                        )
            if chapter in MAINS_CHAPTERS:
                if item.get("difficulty") != "HARD":
                    failures.append(f"{ident}: mains item must be HARD")
            else:
                if item.get("difficulty") not in ("EASY", "MEDIUM"):
                    failures.append(f"{ident}: DI item must be EASY or MEDIUM")
                if not item.get("question_text", "").startswith("Data:"):
                    failures.append(f"{ident}: DI item lacks inline data")
        for part, expected in PART_SIZES.items():
            if counts[part] != expected:
                failures.append(f"{filename}: part {part} has {counts[part]}, expected {expected}")
        for family in expected_family:
            if families[family] != 5:
                failures.append(
                    f"{filename}: family {family} has {families[family]} variants, expected 5"
                )
    for family, count in all_family_counts.items():
        if count != 5:
            failures.append(f"family {family} appears {count} times across dataset")
    print(f"verified {total} questions across {len(FILES)} chapters")
    if failures:
        for failure in failures[:100]:
            print("FAIL:", failure)
        print(f"{len(failures)} failure(s)")
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
