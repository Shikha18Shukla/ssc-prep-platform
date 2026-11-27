# -*- coding: utf-8 -*-
"""Generate the third Banking Maths batch (6 chapters x 120 verified questions).

Answers are computed in Python, never copied from a printed key.  Every item
carries a ``verification_data`` block that
``verify_banking_maths_set3_questions.py`` recomputes independently.

Run:
    python backend/generate_banking_maths_set3_questions.py
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from maths_set3 import PART_SIZES, TARGET_PER_CHAPTER  # noqa: E402
from maths_set3.compound_interest import build_compound_interest  # noqa: E402
from maths_set3.mixture_alligation import build_mixture_alligation  # noqa: E402
from maths_set3.partnership import build_partnership  # noqa: E402
from maths_set3.problems_on_age import build_problems_on_age  # noqa: E402
from maths_set3.simple_interest import build_simple_interest  # noqa: E402
from maths_set3.time_and_work import build_time_and_work  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

BANK_FILES = {
    "simple_interest": "banking_maths_simple_interest_questions.json",
    "compound_interest": "banking_maths_compound_interest_questions.json",
    "mixture_alligation": "banking_maths_mixture_alligation_questions.json",
    "problems_on_age": "banking_maths_problems_on_age_questions.json",
    "partnership": "banking_maths_partnership_questions.json",
    "time_and_work": "banking_maths_time_and_work_questions.json",
}


def build_bank(chapter, chapter_key, spec, seed):
    from maths_set3 import Bank, fill

    bank = Bank(chapter, chapter_key, seed)
    for part, difficulty, fn, page_set in spec:
        fill(
            bank,
            part,
            difficulty,
            1,
            fn,
            source_name=spec_source_name(chapter_key),
            source_page=spec_source_page(chapter_key, page_set),
            source_type="ORIGINAL_VERIFIED",
        )
    return bank


def spec_source_name(chapter_key):
    return {
        "simple_interest": "Simple Interest class notes and mains topic-wise sets (local PDFs)",
        "compound_interest": "Compound Interest class notes and mains topic-wise sets (local PDFs)",
        "mixture_alligation": "Mixture and Alligation class notes and mains topic-wise sets (local PDFs)",
        "problems_on_age": "Problems on Age class notes and topic-wise sets (local PDFs)",
        "partnership": "Partnership class notes and topic-wise sets (local PDFs)",
        "time_and_work": "Time and Work class notes and topic-wise sets (local PDFs)",
    }[chapter_key]


def spec_source_page(chapter_key, page_set):
    from maths_set3 import compound_interest, mixture_alligation, partnership
    from maths_set3 import problems_on_age, simple_interest, time_and_work

    modules = {
        "simple_interest": simple_interest,
        "compound_interest": compound_interest,
        "mixture_alligation": mixture_alligation,
        "problems_on_age": problems_on_age,
        "partnership": partnership,
        "time_and_work": time_and_work,
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
        ("Simple Interest", "simple_interest", build_simple_interest(), 7301),
        ("Compound Interest", "compound_interest", build_compound_interest(), 7302),
        ("Mixture and Alligation", "mixture_alligation", build_mixture_alligation(), 7303),
        ("Problems on Age", "problems_on_age", build_problems_on_age(), 7304),
        ("Partnership", "partnership", build_partnership(), 7305),
        ("Time and Work", "time_and_work", build_time_and_work(), 7306),
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
