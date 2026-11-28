# -*- coding: utf-8 -*-
"""Generate Banking Maths Set 7 (6 chapters x 120 verified questions).

Answers are computed in Python, never copied from a printed key. Every item
carries a ``verification_data`` block that
``verify_banking_maths_set7_questions.py`` recomputes independently from the
separate formula sheets in ``maths_set7/formulas_*.py``.

Run:
    python backend/generate_banking_maths_set7_questions.py
"""

from __future__ import annotations

import importlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from maths_set7 import PART_SIZES, TARGET_PER_CHAPTER  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

MODULES = {
    "mixture_alligation_mains": "mixture_alligation_mains",
    "mixture_alligation_data_interpretation": "mixture_alligation_di",
    "ages_mains": "ages_mains",
    "ages_data_interpretation": "ages_di",
    "partnership_mains": "partnership_mains",
    "partnership_data_interpretation": "partnership_di",
}

BANK_FILES = {
    "mixture_alligation_mains": "banking_maths_mixture_alligation_mains_questions.json",
    "mixture_alligation_data_interpretation": "banking_maths_mixture_alligation_di_questions.json",
    "ages_mains": "banking_maths_ages_mains_questions.json",
    "ages_data_interpretation": "banking_maths_ages_di_questions.json",
    "partnership_mains": "banking_maths_partnership_mains_questions.json",
    "partnership_data_interpretation": "banking_maths_partnership_di_questions.json",
}

SOURCE_NAMES = {
    "mixture_alligation_mains": "Mixture and Alligation Mains class notes (local PDF)",
    "mixture_alligation_data_interpretation": "Mixture and Alligation Data Interpretation class notes (local PDF)",
    "ages_mains": "Ages Mains class notes (local PDF)",
    "ages_data_interpretation": "Ages Data Interpretation class notes (local PDF)",
    "partnership_mains": "Partnership Mains class notes (local PDF)",
    "partnership_data_interpretation": "Partnership Data Interpretation class notes (local PDF)",
}

SPECS = [
    ("Mixture and Alligation (Mains)", "mixture_alligation_mains",
     "build_mixture_alligation_mains", 8501),
    ("Mixture and Alligation – Data Interpretation", "mixture_alligation_data_interpretation",
     "build_mixture_alligation_di", 8502),
    ("Ages (Mains)", "ages_mains", "build_ages_mains", 8503),
    ("Ages – Data Interpretation", "ages_data_interpretation", "build_ages_di", 8504),
    ("Partnership (Mains)", "partnership_mains", "build_partnership_mains", 8505),
    ("Partnership – Data Interpretation", "partnership_data_interpretation",
     "build_partnership_di", 8506),
]


def build_bank(chapter, chapter_key, spec, seed):
    from maths_set7 import Bank, fill

    module = importlib.import_module("maths_set7." + MODULES[chapter_key])
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
        module = importlib.import_module("maths_set7." + MODULES[key])
        spec = getattr(module, builder_name)()
        bank = build_bank(chapter, key, spec, seed)
        write_bank(bank, BANK_FILES[key])
        total += bank.count()
    print(f"TOTAL {total} questions across {len(selected)} chapters")
    return 0


if __name__ == "__main__":
    sys.exit(main())
