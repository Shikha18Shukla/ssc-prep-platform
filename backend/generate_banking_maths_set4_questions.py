# -*- coding: utf-8 -*-
"""Generate the fourth Banking Maths batch (6 chapters x 120 verified questions).

Answers are computed in Python, never copied from a printed key.  Every item
carries a ``verification_data`` block that
``verify_banking_maths_set4_questions.py`` recomputes independently.

Run:
    python backend/generate_banking_maths_set4_questions.py
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from maths_set4 import PART_SIZES, TARGET_PER_CHAPTER  # noqa: E402
from maths_set4.average import build_average  # noqa: E402
from maths_set4.speed_time_distance import build_speed_time_distance  # noqa: E402
from maths_set4.boats_and_streams import build_boats_and_streams  # noqa: E402
from maths_set4.problems_on_trains import build_problems_on_trains  # noqa: E402
from maths_set4.pipe_and_cistern import build_pipe_and_cistern  # noqa: E402
from maths_set4.mensuration_2d import build_mensuration_2d  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

BANK_FILES = {
    "pipe_and_cistern": "banking_maths_pipe_and_cistern_questions.json",
    "average": "banking_maths_average_questions.json",
    "speed_time_distance": "banking_maths_speed_time_distance_questions.json",
    "problems_on_trains": "banking_maths_problems_on_trains_questions.json",
    "boats_and_streams": "banking_maths_boats_and_streams_questions.json",
    "mensuration_2d": "banking_maths_mensuration_2d_questions.json",
}


def build_bank(chapter, chapter_key, spec, seed):
    from maths_set4 import Bank, fill

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
        "pipe_and_cistern": "Pipe and Cistern topic-wise mains sets (local PDFs)",
        "average": "Average topic-wise mains sets (local PDFs)",
        "speed_time_distance": "Speed, Time and Distance topic-wise mains sets (local PDFs)",
        "problems_on_trains": "Problems on Trains topic-wise mains sets (local PDFs)",
        "boats_and_streams": "Boats and Streams topic-wise mains sets (local PDFs)",
        "mensuration_2d": "Mensuration 2D class notes (local PDFs)",
    }[chapter_key]


def page_set_for(chapter_key, spec_index, fallback):
    """Cycle a chapter's inspected PDFs, including the fifth TSD reference."""
    from maths_set4 import average, speed_time_distance, boats_and_streams
    from maths_set4 import problems_on_trains, pipe_and_cistern, mensuration_2d

    modules = {
        "pipe_and_cistern": pipe_and_cistern,
        "average": average,
        "speed_time_distance": speed_time_distance,
        "problems_on_trains": problems_on_trains,
        "boats_and_streams": boats_and_streams,
        "mensuration_2d": mensuration_2d,
    }
    keys = sorted(modules[chapter_key].PAGES)
    if chapter_key == "speed_time_distance" and 5 in keys:
        keys = [1, 2, 3, 4, 5]
    return keys[spec_index % len(keys)] if keys else fallback


def spec_source_page(chapter_key, page_set):
    from maths_set4 import average, speed_time_distance, boats_and_streams
    from maths_set4 import problems_on_trains, pipe_and_cistern, mensuration_2d

    modules = {
        "pipe_and_cistern": pipe_and_cistern,
        "average": average,
        "speed_time_distance": speed_time_distance,
        "problems_on_trains": problems_on_trains,
        "boats_and_streams": boats_and_streams,
        "mensuration_2d": mensuration_2d,
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
        ("Pipe and Cistern", "pipe_and_cistern", build_pipe_and_cistern(), 7301),
        ("Average", "average", build_average(), 7302),
        ("Speed, Time and Distance", "speed_time_distance", build_speed_time_distance(), 7303),
        ("Problems on Trains", "problems_on_trains", build_problems_on_trains(), 7304),
        ("Boats and Streams", "boats_and_streams", build_boats_and_streams(), 7305),
        ("Mensuration – 2D", "mensuration_2d", build_mensuration_2d(), 7306),
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
