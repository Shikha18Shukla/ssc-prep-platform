"""Quality checks for the verified Blood Relations lecture 01–04 import batch."""

import json
import re
import unicodedata
from pathlib import Path


IMPORT_FILE = (
    Path(__file__).parents[1]
    / "data/imports/reasoning/blood-relations/blood_relations_01_04_verified.json"
)


def _normalized(value: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def test_blood_relations_batch_is_source_traceable_and_well_formed():
    records = json.loads(IMPORT_FILE.read_text(encoding="utf-8"))["questions"]

    assert len(records) == 22
    assert len({_normalized(row["question_text"]) for row in records}) == len(records)

    for row in records:
        assert row["exam_slug"] == "banking-clerk"
        assert row["subject_slug"] == "reasoning"
        assert row["chapter_slug"] == "blood-relations"
        assert row["subcategory_slug"] is None
        assert set(row["options"]) in ({"A", "B", "C", "D"}, {"A", "B", "C", "D", "E"})
        assert row["correct_option"] in row["options"]
        assert row["explanation"].strip()
        assert row["difficulty"] in {"EASY", "MEDIUM", "HARD"}
        assert row["is_pyq"] is False
        assert re.search(r"physical page \d+", row["source"])
        assert "Class Notes" in row["source"]
        assert len(row["source"]) <= 255
        assert "हिंदी मूल पाठ:" in row["question_text"]
