"""Independent answer ledger and structural checks for Boat and Stream."""
import json
import re
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BATCH = Path(__file__).resolve().parents[1] / "data" / "boat_and_stream_verified_batch.json"
PDF_PAGES = [7, 12, 25, 23, 24, 17]
# Independently recalculated in batch order, not read from the option key.
EXPECTED = [
    "6 km/h", "1.5 km/h", "4 km/h", "9 km/h", "3 1/3 km/h", "21 km",
    "2 km/h", "11 km/h", "3 hours", "5 hours", "18 km/h", "5 km/h", "36 km", "4 hours", "3:2",
    "10 km/h", "8 hours", "30 km", "2 km/h", "15 km/h", "3 hours", "17 km/h", "42 km", "5 km/h",
    "12 km/h", "52 km", "6 hours", "2:3", "125/18 m/s", "8 hours", "17 km/h", "52 km", "9.6 km/h",
    "15 km/h", "12 km/h", "8 hours", "2 km/h", "5 hours", "60 km", "13.5 km/h", "3:2", "2 km/h",
    "15 km/h", "10 km/h", "2 km/h", "16 km/h", "24 km", "92 km", "12 km/h", "10 km/h", "5 km/h",
    "12 km/h", "13.5 km/h", "15 km/h", "3 hours", "10 2/3 km/h", "2 hours", "6 hours", "10 hours", "70 km", "2 km/h",
    "12 km/h", "14 km/h", "18 km/h", "60 km", "15 km/h", "0.73 hour", "10 km/h", "5 km downstream", "15 km/h",
    "2 km/h", "15 km/h", "5 km/h", "25 km/h", "12 km/h", "20 km/h", "42 km", "3.6 hours", "20 km/h", "15 km/h",
    "3 hours", "4 km/h", "5 km/h", "20 km/h", "25 km/h", "18 km/h", "5 km/h", "6 km/h", "15 km/h", "20 km/h",
]


def normalized(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def masked(text):
    value = normalized(text)
    value = re.sub(r"\d[\d,]*(?:\.\d+)?%?", " <n> ", value)
    return " ".join(re.sub(r"[^a-z<> ]", " ", value).split())


def test_schema_sources_distribution_and_independent_answer_ledger():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    assert len(rows) == len(EXPECTED) == 90
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    pdf_rows = [row for row in rows if row["source"].startswith("Verified from supplied Boat and Stream PDF")]
    assert len(pdf_rows) == 6
    assert [int(re.search(r"page (\d+);", row["source"]).group(1)) for row in pdf_rows] == PDF_PAGES
    assert sum(row["source"] == "Original SSC-style practice question" for row in rows) == 84
    for index, row in enumerate(rows):
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == (
            "maths", "arithmetic-maths", "boat-and-stream"
        )
        assert row["is_pyq"] is False
        assert row.get("pyq_year") is None and row.get("pyq_exam_name") is None
        assert row["question_text"].strip() and row["explanation"].strip()
        assert set(row["options"]) == set("ABCD")
        assert len({normalized(value) for value in row["options"].values()}) == 4
        assert row["correct_option"] in row["options"]
        assert row["options"][row["correct_option"]] == EXPECTED[index], row["question_text"]
        assert sum(value == EXPECTED[index] for value in row["options"].values()) == 1


def test_exact_number_masked_and_lexical_duplicate_review():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    stems = [row["question_text"] for row in rows]
    assert len({normalized(stem) for stem in stems}) == 90
    for index, stem in enumerate(stems):
        for prior in stems[:index]:
            assert masked(stem) != masked(prior), f"number-masked duplicate: {stem!r} / {prior!r}"
            score = SequenceMatcher(None, normalized(stem), normalized(prior)).ratio()
            assert score < .92, f"lexical near duplicate {score:.3f}: {stem!r} / {prior!r}"
