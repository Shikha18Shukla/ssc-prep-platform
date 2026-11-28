# -*- coding: utf-8 -*-
"""Generate Banking Maths Set 9 (7 chapters x 120 verified questions).

Answers are computed in Python, never copied from a printed key. Every item
carries a ``verification_data`` block that
``verify_banking_maths_set9_questions.py`` recomputes independently from the
separate formula sheet in ``maths_set9/formulas.py``.

Run:
    python backend/generate_banking_maths_set9_questions.py
"""

from __future__ import annotations

import importlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from maths_set9 import PART_SIZES, TARGET_PER_CHAPTER, Bank, fill  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

MODULES = {
    "pipe_and_cistern_data_interpretation": "pipe_and_cistern_di",
    "trains_mains": "trains_mains",
    "trains_data_interpretation": "trains_di",
    "boats_and_streams_mains": "boats_and_streams_mains",
    "boats_and_streams_data_interpretation": "boats_and_streams_di",
    "probability_mains": "probability_mains",
    "probability_data_interpretation": "probability_di",
}
CHAPTERS = {
    "pipe_and_cistern_data_interpretation": "Pipe and Cistern – Data Interpretation",
    "trains_mains": "Trains (Mains)",
    "trains_data_interpretation": "Trains – Data Interpretation",
    "boats_and_streams_mains": "Boats and Streams (Mains)",
    "boats_and_streams_data_interpretation": "Boats and Streams – Data Interpretation",
    "probability_mains": "Probability (Mains)",
    "probability_data_interpretation": "Probability – Data Interpretation",
}
SOURCE_NAMES = {
    "pipe_and_cistern_data_interpretation": "Pipe and Cistern Data Interpretation 01  Class Notes.pdf",
    "trains_mains": "98b402b7-32a0-4ce4-bed3-b059242c8e14.pdf",
    "trains_data_interpretation": "207b546a-6d75-4080-8b00-114f9d7c977d.pdf",
    "boats_and_streams_mains": "ce7bd62e-b49c-41dc-9441-23cfd6cc40f8.pdf",
    "boats_and_streams_data_interpretation": "245ea656-5a7f-4175-9bd5-b920dada2d07.pdf",
    "probability_mains": "106c989f-3149-4b18-8084-66e351389c37.pdf",
    "probability_data_interpretation": "f9d83e47-9397-4b2e-99aa-92595ea4647c.pdf",
}
SOURCE_PAGES = {
    "pipe_and_cistern_data_interpretation": "Pipe and Cistern Data Interpretation 01  Class Notes.pdf, pp. 4-16",
    "trains_mains": "98b402b7-32a0-4ce4-bed3-b059242c8e14.pdf, pp. 4-8",
    "trains_data_interpretation": "207b546a-6d75-4080-8b00-114f9d7c977d.pdf, pp. 4-11",
    "boats_and_streams_mains": "ce7bd62e-b49c-41dc-9441-23cfd6cc40f8.pdf, pp. 4-9",
    "boats_and_streams_data_interpretation": "245ea656-5a7f-4175-9bd5-b920dada2d07.pdf, pp. 4-10",
    "probability_mains": "106c989f-3149-4b18-8084-66e351389c37.pdf, pp. 4-11",
    "probability_data_interpretation": "f9d83e47-9397-4b2e-99aa-92595ea4647c.pdf, pp. 4-16",
}
SEEDS = {
    "pipe_and_cistern_data_interpretation": 9601,
    "trains_mains": 9602,
    "trains_data_interpretation": 9603,
    "boats_and_streams_mains": 9604,
    "boats_and_streams_data_interpretation": 9605,
    "probability_mains": 9606,
    "probability_data_interpretation": 9607,
}
BUILDERS = {
    "pipe_and_cistern_data_interpretation": "build_pipe_and_cistern_di",
    "trains_mains": "build_trains_mains",
    "trains_data_interpretation": "build_trains_di",
    "boats_and_streams_mains": "build_boats_and_streams_mains",
    "boats_and_streams_data_interpretation": "build_boats_and_streams_di",
    "probability_mains": "build_probability_mains",
    "probability_data_interpretation": "build_probability_di",
}
BANK_FILES = {
    key: f"banking_maths_{key}_questions.json"
    if key in (
        "trains_mains", "trains_data_interpretation",
        "boats_and_streams_mains", "boats_and_streams_data_interpretation",
        "probability_mains", "probability_data_interpretation",
    )
    else "banking_maths_pipe_and_cistern_di_questions.json"
    for key in MODULES
}


def main() -> int:
    requested = sys.argv[1:]
    targets = requested or list(MODULES)
    for chapter_key in targets:
        if chapter_key not in MODULES:
            raise SystemExit(f"unknown chapter: {chapter_key}")
        module = importlib.import_module(f"maths_set9.{MODULES[chapter_key]}")
        builder_name = BUILDERS[chapter_key]
        specs = getattr(module, builder_name)()
        from maths_set9 import Bank

        bank = Bank(CHAPTERS[chapter_key], chapter_key, SEEDS[chapter_key])
        for part, difficulty, fn, _source_index in specs:
            fill(
                bank,
                part=part,
                difficulty=difficulty,
                count=1,
                fn=fn,
                source_name=SOURCE_NAMES[chapter_key],
                source_page=SOURCE_PAGES[chapter_key],
            )
        if len(bank.items) != TARGET_PER_CHAPTER:
            raise SystemExit(
                f"{chapter_key}: generated {len(bank.items)}, expected {TARGET_PER_CHAPTER}"
            )
        counts = {part: 0 for part in PART_SIZES}
        for item in bank.items:
            counts[item["part"]] += 1
        if counts != PART_SIZES:
            raise SystemExit(f"{chapter_key}: part counts {counts} != {PART_SIZES}")
        path = os.path.join(DATA, BANK_FILES[chapter_key])
        with open(path, "w", encoding="utf-8") as fp:
            json.dump(bank.items, fp, ensure_ascii=False, indent=2)
        print(f"generated {len(bank.items)} questions in {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
