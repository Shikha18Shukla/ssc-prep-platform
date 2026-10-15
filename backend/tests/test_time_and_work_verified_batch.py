import json
import re
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BATCH = Path(__file__).resolve().parents[1] / "data" / "time_and_work_verified_batch.json"
LEVELS = ("EASY", "MEDIUM", "HARD")
EXPECTED = [
    "6 days", "6 3/7 days", "84 days", "10 days", "16 days", "8 days", "5 5/11 days", "4 days", "6 days", "12 days",
    "16", "16 days", "75 minutes", "7 1/2 days", "2 hours", "7 1/2 days", "5 days", "10.2 days", "11 days", "12 days",
    "14 days", "45 days", "60 days", "60 days", "24 days", "27th day", "13 3/4 days", "6:30 p.m.", "13 1/4 days", "8 days",
    "8 days", "7 1/2 days", "54 men", "10 hours", "36 days", "32 days", "320 men", "600 people", "6 days", "6 2/3 days",
    "12 days", "36 days", "47 1/2 days", "75 men", "200 laborers", "4 days", "10 days", "5 2/3 days", "15 days",
    "1 5/19 days", "33 days", "90 days", "₹12,000", "₹300", "₹50", "₹400", "₹225", "4 days", "10 days",
    "48 days", "11 1/13 months", "12 1/2 days", "17 1/2 days", "₹60", "₹90", "None of these", "24 days", "6 days", "10.5 hours",
    "15 days", "4:3", "20 days", "24 days", "2/5", "360 parts", "20 days", "40 days", "9 1/2 days", "8.4 days", "10.5 days",
    "13.5 days", "60/13 days", "16 days", "64/9 days", "24 days", "3 days", "12 days", "2.4 days", "11 1/4 days", "4 days",
]


def norm(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def masked(value):
    value = norm(value)
    value = re.sub(r"\d[\d,]*(?:\.\d+)?%?", " <number> ", value)
    return " ".join(re.sub(r"[^a-z<> ]", " ", value).split())


def test_schema_provenance_distribution_and_independently_checked_answers():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    assert len(rows) == len(EXPECTED) == 90
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    assert sum(row["source"].startswith("Verified from supplied PDF:") for row in rows) == 69
    assert sum(row["source"] == "Original SSC-style practice question" for row in rows) == 21
    for index, row in enumerate(rows):
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == ("maths", "arithmetic-maths", "time-and-work")
        assert row["is_pyq"] is False and row.get("pyq_year") is None and row.get("pyq_exam_name") is None
        assert row["question_text"].strip() and row["explanation"].strip()
        assert set(row["options"]) == set("ABCD")
        assert len({norm(value) for value in row["options"].values()}) == 4
        expected = EXPECTED[index]
        assert row["options"][row["correct_option"]] == expected, row["question_text"]
        assert sum(value == expected for value in row["options"].values()) == 1


def test_exact_normalized_number_masked_and_lexical_duplicate_review():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    stems = [row["question_text"] for row in rows]
    assert len(set(stems)) == 90
    assert len(set(map(norm, stems))) == 90
    for index, stem in enumerate(stems):
        for prior in stems[:index]:
            assert masked(stem) != masked(prior), f"number-masked duplicate: {stem!r} / {prior!r}"
            assert SequenceMatcher(None, norm(stem), norm(prior)).ratio() < 0.92, f"lexical duplicate: {stem!r} / {prior!r}"

