# -*- coding: utf-8 -*-
"""Generate the fifth Banking Maths batch (6 chapters x 120 verified questions).

Answers are computed in Python, never copied from a printed key.  Every item
carries a ``verification_data`` block that
``verify_banking_maths_set5_questions.py`` recomputes independently.

Run:
    python backend/generate_banking_maths_set5_questions.py
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from maths_set5 import PART_SIZES, TARGET_PER_CHAPTER  # noqa: E402
from maths_set5.mensuration_3d import build_mensuration_3d  # noqa: E402
from maths_set5.permutations import build_permutations  # noqa: E402
from maths_set5.combinations import build_combinations  # noqa: E402
from maths_set5.probability import build_probability  # noqa: E402
from maths_set5.data_interpretation import build_data_interpretation  # noqa: E402
from maths_set5.caselet_data_interpretation import build_caselet_data_interpretation  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

BANK_FILES = {
    "mensuration_3d": "banking_maths_mensuration_3d_questions.json",
    "permutations": "banking_maths_permutations_questions.json",
    "combinations": "banking_maths_combinations_questions.json",
    "probability": "banking_maths_probability_questions.json",
    "data_interpretation": "banking_maths_data_interpretation_questions.json",
    "caselet_data_interpretation": "banking_maths_caselet_data_interpretation_questions.json",
}


def build_bank(chapter, chapter_key, spec, seed):
    from maths_set5 import Bank, fill

    bank = Bank(chapter, chapter_key, seed)
    for spec_index, (part, difficulty, fn, page_set) in enumerate(spec):
        fill(
            bank,
            part,
            difficulty,
            1,
            fn,
            source_name=spec_source_name(chapter_key),
            source_page=spec_source_page(chapter_key, page_set_for(chapter_key, spec_index, page_set)),
            source_type="ORIGINAL_VERIFIED",
        )
    return bank


def spec_source_name(chapter_key):
    return {
        "mensuration_3d": "Mensuration 3D class notes (local PDFs)",
        "permutations": "Permutations class notes (local PDFs)",
        "combinations": "Combinations class notes (local PDFs)",
        "probability": "Probability class notes (local PDFs)",
        "data_interpretation": "Data Interpretation class notes (local PDFs)",
        "caselet_data_interpretation": "Caselet Data Interpretation class notes (local PDFs)",
    }[chapter_key]


def page_set_for(chapter_key, spec_index, fallback):
    from maths_set5 import caselet_data_interpretation, combinations, data_interpretation
    from maths_set5 import mensuration_3d, permutations, probability

    modules = {
        "mensuration_3d": mensuration_3d,
        "permutations": permutations,
        "combinations": combinations,
        "probability": probability,
        "data_interpretation": data_interpretation,
        "caselet_data_interpretation": caselet_data_interpretation,
    }
    keys = sorted(modules[chapter_key].PAGES)
    return keys[spec_index % len(keys)] if keys else fallback


def spec_source_page(chapter_key, page_set):
    from maths_set5 import caselet_data_interpretation, combinations, data_interpretation
    from maths_set5 import mensuration_3d, permutations, probability

    modules = {
        "mensuration_3d": mensuration_3d,
        "permutations": permutations,
        "combinations": combinations,
        "probability": probability,
        "data_interpretation": data_interpretation,
        "caselet_data_interpretation": caselet_data_interpretation,
    }
    return modules[chapter_key].PAGES[page_set]


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
        ("Mensuration – 3D", "mensuration_3d", build_mensuration_3d(), 8301),
        ("Permutations", "permutations", build_permutations(), 8302),
        ("Combinations", "combinations", build_combinations(), 8303),
        ("Probability", "probability", build_probability(), 8304),
        ("Data Interpretation", "data_interpretation", build_data_interpretation(), 8305),
        ("Caselet Data Interpretation", "caselet_data_interpretation", build_caselet_data_interpretation(), 8306),
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
