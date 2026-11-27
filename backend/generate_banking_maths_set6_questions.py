# -*- coding: utf-8 -*-
"""Generate the sixth Banking Maths batch (6 chapters x 120 verified questions).

Answers are computed in Python, never copied from a printed key.  Every item
carries a ``verification_data`` block that
``verify_banking_maths_set6_questions.py`` recomputes independently.

Run:
    python backend/generate_banking_maths_set6_questions.py
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from maths_set6 import PART_SIZES, TARGET_PER_CHAPTER  # noqa: E402
from maths_set6.percentage_arithmetic_mains import build_percentage_arithmetic_mains  # noqa: E402
from maths_set6.percentage_di_mains import build_percentage_di_mains  # noqa: E402
from maths_set6.ratio_arithmetic_mains import build_ratio_arithmetic_mains  # noqa: E402
from maths_set6.ratio_di_mains import build_ratio_di_mains  # noqa: E402
from maths_set6.profit_and_loss_mains import build_profit_and_loss_mains  # noqa: E402
from maths_set6.profit_and_loss_di_questions import build_profit_and_loss_di  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

BANK_FILES = {
    "percentage_arithmetic_mains": "banking_maths_percentage_arithmetic_mains_questions.json",
    "percentage_data_interpretation_mains": "banking_maths_percentage_di_mains_questions.json",
    "ratio_arithmetic_mains": "banking_maths_ratio_arithmetic_mains_questions.json",
    "ratio_data_interpretation_mains": "banking_maths_ratio_di_mains_questions.json",
    "profit_and_loss_mains": "banking_maths_profit_and_loss_mains_questions.json",
    "profit_and_loss_data_interpretation": "banking_maths_profit_and_loss_di_questions.json",
}

SOURCE_NAMES = {
    "percentage_arithmetic_mains": "Percentage Arithmetic Mains class notes (local PDF)",
    "percentage_data_interpretation_mains": "Percentage Data Interpretation Mains class notes (local PDF)",
    "ratio_arithmetic_mains": "Ratio Arithmetic Mains class notes (local PDF)",
    "ratio_data_interpretation_mains": "Ratio Data Interpretation Mains class notes (local PDF)",
    "profit_and_loss_mains": "Profit and Loss Mains class notes (local PDF)",
    "profit_and_loss_data_interpretation": "Profit and Loss Data Interpretation class notes (local PDF)",
}

MODULES = {
    "percentage_arithmetic_mains": "percentage_arithmetic_mains",
    "percentage_data_interpretation_mains": "percentage_di_mains",
    "ratio_arithmetic_mains": "ratio_arithmetic_mains",
    "ratio_data_interpretation_mains": "ratio_di_mains",
    "profit_and_loss_mains": "profit_and_loss_mains",
    "profit_and_loss_data_interpretation": "profit_and_loss_di_questions",
}


def build_bank(chapter, chapter_key, spec, seed):
    from maths_set6 import Bank, fill
    from importlib import import_module

    module = import_module("maths_set6." + MODULES[chapter_key])
    bank = Bank(chapter, chapter_key, seed)
    keys = sorted(module.PAGES)
    for spec_index, (part, difficulty, fn, _page_set) in enumerate(spec):
        fill(
            bank,
            part,
            difficulty,
            1,
            fn,
            source_name=SOURCE_NAMES[chapter_key],
            source_page=module.PAGES[keys[spec_index % len(keys)]],
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
    specs = [
        ("Percentage Arithmetic (Mains)", "percentage_arithmetic_mains",
         build_percentage_arithmetic_mains(), 8401),
        ("Percentage – Data Interpretation (Mains)", "percentage_data_interpretation_mains",
         build_percentage_di_mains(), 8402),
        ("Ratio Arithmetic (Mains)", "ratio_arithmetic_mains",
         build_ratio_arithmetic_mains(), 8403),
        ("Ratio – Data Interpretation (Mains)", "ratio_data_interpretation_mains",
         build_ratio_di_mains(), 8404),
        ("Profit and Loss (Mains)", "profit_and_loss_mains",
         build_profit_and_loss_mains(), 8405),
        ("Profit and Loss – Data Interpretation", "profit_and_loss_data_interpretation",
         build_profit_and_loss_di(), 8406),
    ]
    total = 0
    for chapter, key, spec, seed in specs:
        bank = build_bank(chapter, key, spec, seed)
        write_bank(bank, BANK_FILES[key])
        total += bank.count()
    print(f"TOTAL {total} questions across {len(specs)} chapters")
    return 0


if __name__ == "__main__":
    sys.exit(main())
