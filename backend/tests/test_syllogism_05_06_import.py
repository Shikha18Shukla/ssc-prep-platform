"""Quality checks for the verified Syllogism lecture 05/06 import batch."""

import json
from collections import Counter
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
IMPORT = BASE / "data" / "imports" / "reasoning" / "syllogism" / "syllogism_05_06_verified_import.json"
REVIEW = BASE / "data" / "imports" / "reasoning" / "syllogism" / "syllogism_05_06_review_report.md"


def test_verified_batch_is_complete_and_source_traceable():
    rows = json.loads(IMPORT.read_text(encoding="utf-8"))["questions"]
    assert len(rows) == 15
    assert Counter(row["source"].split(", p. ")[0] for row in rows) == {
        "Syllogism 05_Class Notes.pdf": 9,
        "Syllogism 06_Class Notes.pdf": 6,
    }
    for row in rows:
        assert (row["exam_slug"], row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == (
            "banking-clerk", "reasoning", "", "syllogism"
        )
        assert row["source"].rsplit("p. ", 1)[1].isdigit()
        assert set(row["options"]) == set("ABCDE")
        assert row["correct_option"] in row["options"]
        assert row["explanation"].strip()
        assert row["difficulty"] in {"EASY", "MEDIUM", "HARD"}


def test_unclear_question_is_held_out_with_reason():
    report = REVIEW.read_text(encoding="utf-8")
    assert "p. 15" in report
    assert "Held out" in report
    rows = json.loads(IMPORT.read_text(encoding="utf-8"))["questions"]
    assert not any(row["source"].endswith("p. 15") for row in rows)
