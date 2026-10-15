"""Independent answer-key, provenance, and duplicate checks for Alligation."""
import json
import re
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BATCH = Path(__file__).resolve().parents[1] / "data" / "alligation_verified_batch.json"

# Independently recomputed from the supplied PDF and original question stems.
PDF_ANSWERS = [
    "3:1", "7:3", "3:4", "2:3", "108 kg", "1:5", "2:3", "1:5", "26", "700", "40%",
]
CALCULATED = [
    "Rs 21.60/kg", "Rs 27.60/kg", "Rs 50/kg", "Rs 61.60/L", "Rs 95/kg", "Rs 80/kg", "3 kg",
    "3:2", "3:2", "3:2", "3:2", "Rs 102/kg", "1:1", "1:1", "2:1", "32.5%", "Rs 30/kg",
    "Rs 60/kg", "Rs 39/kg", "2 kg", "33.3333%", "3.3333 kg", "10 L", "4.5 L", "20.8%",
    "Rs 44.40/kg", "1:2", "21.6 kg", "18 L", "3:2", "16 kg", "2:1", "38%", "12.5 kg",
    "37%", "8 kg", "12 L", "Rs 58.50/kg", "47.5%", "48:17", "12 kg", "40 L",
    "Rs 158.40/kg", "15 L", "18 kg", "30 L", "18%", "36 kg", "58.3333%", "Rs 108.50/kg",
    "Rs 54.50/kg", "35%", "26.6667 kg", "66.6667 L", "1:1", "12 kg", "20 kg", "21.4286 L",
    "Rs 82.11/kg", "5 kg", "150 kg", "Rs 110/kg", "12 L", "37.5 kg", "18 L", "13.8889 L",
    "11.72%", "14.4 kg", "12 L", "25 kg", "54 L", "15 L", "32.8571 kg", "29.1667%",
    "Rs 56/kg", "29.375%", "Rs 80/kg", "50 L", "14 g",
]


def normalized(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def masked(text):
    value = normalized(text)
    value = re.sub(r"\d[\d,]*(?:\.\d+)?%?", " <n> ", value)
    return " ".join(re.sub(r"[^a-z<> ]", " ", value).split())


def numeric_value(value):
    match = re.search(r"-?[\d,]+(?:\.\d+)?", value)
    assert match, value
    return float(match.group().replace(",", ""))


def ratio_key(value):
    parts = [int(part) for part in value.split(":")]
    from math import gcd
    from functools import reduce
    divisor = reduce(gcd, parts)
    return tuple(part // divisor for part in parts)


def test_batch_schema_provenance_and_independently_checked_answers():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    assert len(rows) == 90
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    assert sum(row["source"].startswith("Verified from supplied Alligation PDF") for row in rows) == 11
    assert sum(row["source"] == "Original SSC-style practice question" for row in rows) == 79
    assert len(PDF_ANSWERS) == 11 and len(CALCULATED) == 79

    for index, row in enumerate(rows):
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == (
            "maths", "arithmetic-maths", "alligation"
        )
        assert row["is_pyq"] is False
        assert row.get("pyq_year") is None and row.get("pyq_exam_name") is None
        assert row["question_text"].strip() and row["explanation"].strip()
        assert set(row["options"]) == set("ABCD")
        assert len({normalized(value) for value in row["options"].values()}) == 4
        assert row["correct_option"] in row["options"]
        correct = row["options"][row["correct_option"]]
        expected = PDF_ANSWERS[index] if index < 11 else CALCULATED[index - 11]
        if ":" in expected:
            assert correct == expected, row["question_text"]
        else:
            assert abs(numeric_value(correct) - numeric_value(expected)) < 0.0001, row["question_text"]
        ratios = [value for value in row["options"].values() if re.fullmatch(r"\d+:\d+", value)]
        assert len({ratio_key(value) for value in ratios}) == len(ratios)


def test_no_exact_normalized_number_masked_or_high_lexical_duplicates():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    stems = [row["question_text"] for row in rows]
    assert len({normalized(stem) for stem in stems}) == 90
    for index, stem in enumerate(stems):
        for prior in stems[:index]:
            assert masked(stem) != masked(prior), f"number-masked duplicate: {stem!r} / {prior!r}"
            score = SequenceMatcher(None, normalized(stem), normalized(prior)).ratio()
            assert score < .92, f"high lexical similarity ({score:.3f}): {stem!r} / {prior!r}"
