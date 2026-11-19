"""Quality checks for copying verified SSC Sitting Arrangement questions."""

import json
import re
import unicodedata
from collections import Counter
from pathlib import Path


IMPORT_FILE = (
    Path(__file__).parents[1]
    / "data/imports/reasoning/seating-arrangement/ssc_sitting_arrangement_verified.json"
)
HELD_QUESTION_IDS = {
    "11396733-7bfa-4c8d-bf97-fe2bc9f3a486",
    "39b4c4bc-3253-46af-bbcc-b2a07b018db5",
    "80f9702d-de5e-4432-ae34-aae4d6aad6a9",
    "d9edf595-08f6-4587-b4ab-d328ff05f3de",
}
EXPECTED_COUNTS = {
    "linear-arrangements": 15,
    "circular-arrangements": 8,
    "square-rectangular-arrangements": 3,
}
SOURCE_CHAPTER_ID = "32faa174-9f26-4524-9639-f325ef6674b8"


def _normalized(value: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def test_import_batch_preserves_source_rows_and_destination_allocation():
    records = json.loads(IMPORT_FILE.read_text(encoding="utf-8"))["questions"]

    assert len(records) == 26
    assert Counter(row["chapter_slug"] for row in records) == EXPECTED_COUNTS
    assert len({_normalized(row["question_text"]) for row in records}) == len(records)

    original_ids = []
    for row in records:
        match = re.search(r"original question ID ([0-9a-f-]{36})", row["source"])
        assert match
        original_id = match.group(1)
        original_ids.append(original_id)
        assert original_id not in HELD_QUESTION_IDS
        assert f"SSC Sitting Arrangement chapter {SOURCE_CHAPTER_ID}" in row["source"]
        assert row["exam_slug"] == "banking-clerk"
        assert row["subject_slug"] == "reasoning"
        assert row["subcategory_slug"] is None
        assert set(row["options"]) in ({"A", "B", "C", "D"}, {"A", "B", "C", "D", "E"})
        assert row["correct_option"] in row["options"]
        assert row["explanation"].strip()
        assert row["difficulty"] in {"EASY", "MEDIUM", "HARD"}
        assert row["source"].strip()
        assert len(row["source"]) <= 255

    assert len(set(original_ids)) == 26
