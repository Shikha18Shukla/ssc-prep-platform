# -*- coding: utf-8 -*-
"""Generate the second Banking Maths batch (5 chapters x 120 verified questions).

Answers are computed in Python, never copied from a printed key, and every item
carries a ``verification_data`` block that
``verify_banking_maths_set2_questions.py`` recomputes independently.

Run:
    python backend/generate_banking_maths_set2_questions.py
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from maths_set2 import PART_SIZES, TARGET_PER_CHAPTER  # noqa: E402
from maths_set2.number_system import build_number_system  # noqa: E402
from maths_set2.percentage import build_percentage  # noqa: E402
from maths_set2.profit_loss import build_profit_loss  # noqa: E402
from maths_set2.quadratic import build_quadratic  # noqa: E402
from maths_set2.ratio import build_ratio  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

BANK_FILES = {
    "quadratic_equations": "banking_maths_quadratic_equations_questions.json",
    "number_system": "banking_maths_number_system_questions.json",
    "percentage": "banking_maths_percentage_questions.json",
    "ratio_proportion": "banking_maths_ratio_proportion_questions.json",
    "profit_loss_discount": "banking_maths_profit_loss_discount_questions.json",
}


def write_bank(bank, filename: str) -> None:
    assert bank.count() == TARGET_PER_CHAPTER, (bank.chapter, bank.count())
    for part, size in PART_SIZES.items():
        assert bank.count(part) == size, (bank.chapter, part, bank.count(part))
    path = os.path.join(DATA, filename)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(bank.items, handle, ensure_ascii=False, indent=2)
    print(f"wrote {path} ({bank.count()} questions)")


def main() -> int:
    banks = [
        build_quadratic(),
        build_number_system(),
        build_percentage(),
        build_ratio(),
        build_profit_loss(),
    ]
    for bank in banks:
        write_bank(bank, BANK_FILES[bank.chapter_key])
    total = sum(bank.count() for bank in banks)
    print(f"TOTAL {total} questions across {len(banks)} chapters")
    return 0


if __name__ == "__main__":
    sys.exit(main())
