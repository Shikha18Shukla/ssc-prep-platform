# -*- coding: utf-8 -*-
"""Generate Banking Maths Set 8 (6 chapters x 120 verified questions).

Answers are computed in Python, never copied from a printed key. Every item
carries a ``verification_data`` block that
``verify_banking_maths_set8_questions.py`` recomputes independently from the
separate formula sheets in ``maths_set8/formulas_*.py``.

Run:
    python backend/generate_banking_maths_set8_questions.py
"""

from __future__ import annotations

import importlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from maths_set8 import PART_SIZES, TARGET_PER_CHAPTER  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

MODULES = {
    "time_and_work_mains": "time_and_work_mains",
    "time_and_work_data_interpretation": "time_and_work_di",
    "time_speed_and_distance_mains": "time_speed_distance_mains",
    "simple_and_compound_interest_mains": "simple_and_compound_interest_mains",
    "simple_and_compound_interest_data_interpretation": "simple_and_compound_interest_di",
    "pipe_and_cistern_mains": "pipe_and_cistern_mains",
}

BANK_FILES = {
    "time_and_work_mains": "banking_maths_time_and_work_mains_questions.json",
    "time_and_work_data_interpretation": "banking_maths_time_and_work_di_questions.json",
    "time_speed_and_distance_mains": "banking_maths_time_speed_and_distance_mains_questions.json",
    "simple_and_compound_interest_mains": "banking_maths_simple_and_compound_interest_mains_questions.json",
    "simple_and_compound_interest_data_interpretation": "banking_maths_simple_and_compound_interest_di_questions.json",
    "pipe_and_cistern_mains": "banking_maths_pipe_and_cistern_mains_questions.json",
}

SOURCE_NAMES = {
    "time_and_work_mains": "Time and Work Mains class notes (local PDF)",
    "time_and_work_data_interpretation": "Time and Work Data Interpretation class notes (local PDF)",
    "time_speed_and_distance_mains": "Time, Speed and Distance Mains class notes (local PDF)",
    "simple_and_compound_interest_mains": "Simple and Compound Interest Mains class notes (local PDF)",
    "simple_and_compound_interest_data_interpretation": "Simple and Compound Interest Data Interpretation class notes (local PDF)",
    "pipe_and_cistern_mains": "Pipe and Cistern Mains class notes (local PDF)",
}

SPECS = [
    ("Time and Work (Mains)", "time_and_work_mains", "build_time_and_work_mains", 8601),
    ("Time and Work – Data Interpretation", "time_and_work_data_interpretation", "build_time_and_work_di", 8602),
    ("Time, Speed and Distance (Mains)", "time_speed_and_distance_mains", "build_time_speed_distance_mains", 8603),
    ("Simple and Compound Interest (Mains)", "simple_and_compound_interest_mains", "build_simple_and_compound_interest_mains", 8604),
    ("Simple and Compound Interest – Data Interpretation", "simple_and_compound_interest_data_interpretation", "build_simple_and_compound_interest_di", 8605),
    ("Pipe and Cistern (Mains)", "pipe_and_cistern_mains", "build_pipe_and_cistern_mains", 8606),
]


def build_bank(chapter, chapter_key, spec, seed):
    from maths_set8 import Bank, fill

    module = importlib.import_module("maths_set8." + MODULES[chapter_key])
    bank = Bank(chapter, chapter_key, seed)
    for part, difficulty, fn, page_ref in spec:
        if isinstance(page_ref, int):
            source_page = module.PAGES[page_ref]
        else:
            source_page = str(page_ref)
        fill(
            bank,
            part,
            difficulty,
            1,
            fn,
            source_name=SOURCE_NAMES[chapter_key],
            source_page=source_page,
            source_type="ORIGINAL_VERIFIED",
        )
    return bank


def write_bank(bank, filename: str) -> None:
    assert bank.count() == TARGET_PER_CHAPTER, (bank.chapter, bank.count())
    for part, size in PART_SIZES.items():
        assert bank.count(part) == size, (bank.chapter, part, bank.count(part))
    path = os.path.join(DATA, filename)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(bank.items, handle, ensure_ascii=False, indent=2)
    print(f"wrote {path} ({bank.count()} questions)")


def main() -> int:
    requested = sys.argv[1] if len(sys.argv) > 1 else None
    selected = [spec for spec in SPECS if not requested or spec[1] == requested]
    if requested and not selected:
        print(f"unknown chapter key {requested!r}")
        return 2
    total = 0
    for chapter, key, builder_name, seed in selected:
        module = importlib.import_module("maths_set8." + MODULES[key])
        spec = getattr(module, builder_name)()
        bank = build_bank(chapter, key, spec, seed)
        write_bank(bank, BANK_FILES[key])
        total += bank.count()
    print(f"TOTAL {total} questions across {len(selected)} chapters")
    return 0


if __name__ == "__main__":
    sys.exit(main())
