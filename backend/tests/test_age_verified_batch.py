"""Independent checks for the reviewed Age chapter batch."""
import json
import re
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BATCH = Path(__file__).resolve().parents[1] / "data" / "age_verified_batch.json"

# Independently recalculated results for the 66 authored questions, in batch order.
CALCULATED = [
    19, 14, 12, 20, 21, 18, 21, 28, 18, 10, 20, 16, 48, 28, 6, 44, 36, 45, 43, 36,
    6, 8, 9, 16, 6, 9, 14, 39, 10, 20, 21, 26, 37, 10, 16, 20, 15, 17, 16,
    26, 56, 130, 61, 8, 34, 58, 19, 16, 25, 12, 39, 21, 35, 48, 35, 48, 67, 48,
    45, 30, 44, 35, 20, 29, 20, 50,
]

# The source PDF's marked answer, checked independently against the printed stem.
PDF_ANSWERS = [
    "24 years", "5:6", "9:11", "2:3", "29 years", "24 years", "6 years", "16 years",
    "60 years", "9 years", "5 years", "Sudha 30, Radha 16", "28 and 13 years",
    "50 years", "30 years 8 months", "24 years", "4 years", "1 year", "2 years",
    "13 years", "45 years", "12 years", "17 years", "39 years",
]


def normalized(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def masked(text):
    value = normalized(text)
    value = re.sub(r"\d[\d,]*(?:\.\d+)?%?", " <n> ", value)
    return " ".join(re.sub(r"[^a-z<> ]", " ", value).split())


def test_batch_schema_counts_provenance_and_answers():
    questions = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    assert len(questions) == 90
    assert Counter(q["difficulty"] for q in questions) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    assert sum(q["source"].startswith("Verified from supplied Age PDF") for q in questions) == 24
    assert sum(q["source"] == "Original SSC-style practice question" for q in questions) == 66
    assert len(CALCULATED) == 66
    assert len(PDF_ANSWERS) == 24

    for index, row in enumerate(questions):
        assert row["subject_slug"] == "maths"
        assert row["subcategory_slug"] == "arithmetic-maths"
        assert row["chapter_slug"] == "age"
        assert row["is_pyq"] is False
        assert row.get("pyq_year") is None and row.get("pyq_exam_name") is None
        assert row["difficulty"] in {"EASY", "MEDIUM", "HARD"}
        assert row["question_text"].strip() and row["explanation"].strip()
        assert set(row["options"]) == set("ABCD")
        assert len({normalized(v) for v in row["options"].values()}) == 4
        assert row["correct_option"] in row["options"]
        if index < 24:
            assert row["options"][row["correct_option"]] == PDF_ANSWERS[index]
        else:
            expected = CALCULATED[index - 24]
            correct = row["options"][row["correct_option"]]
            assert correct == f"{expected} years", row["question_text"]
            assert sum(value == correct for value in row["options"].values()) == 1


def test_no_exact_number_masked_or_high_lexical_duplicates():
    questions = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    stems = [row["question_text"] for row in questions]
    assert len({normalized(stem) for stem in stems}) == 90
    for index, stem in enumerate(stems):
        for prior in stems[:index]:
            assert masked(stem) != masked(prior), f"number-masked duplicate: {stem!r} / {prior!r}"
            similarity = SequenceMatcher(None, normalized(stem), normalized(prior)).ratio()
            assert similarity < .92, f"high lexical similarity ({similarity:.3f}): {stem!r} / {prior!r}"
