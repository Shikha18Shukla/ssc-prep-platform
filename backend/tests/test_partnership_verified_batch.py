"""Independent answer-key, provenance, and duplicate checks for Partnership."""
import json
import re
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BATCH = Path(__file__).resolve().parents[1] / "data" / "partnership_verified_batch.json"

# Recomputed from each authored stem, independently of its generated choices.
CALCULATED = [
    15000, 9000, 6, 25000, 20000, "1:1", 16000, 3000, 9000, 12000, 36000, 17500,
    7000, 3200, 8000, 12000, 24000, 7200, 10000, 3000, 7000, 15000, 4000,
    "1:1", 28000, "1:2", 12, "1:1:2", 576000, "7:9", 19000, 9, "32:15", "3:4",
    12000, "6:5", 10000, "10:9", 20000, 6000, "77:60:7", 10000, 30000, 12000,
    9000, "9:8", "39:38", "10:9:9", 50000, 16000, "11:15:9", "21:41", 10,
    "24:25:24", 32666.67, 32000, "36:53", 21450, "12:11", "8:5:8", 4, 68000,
    "5:4", "9:55", "15:16", 9, 19000, "24:29",
]

PDF_ANSWERS = [
    "Rs 6,868", "Rs 9,200", "1:1", "08:15:30", "1:6:4", "Rs 4,000", "1:1", "1:1",
    "4 months", "3 months", "5 months", "Rs 2,400", "19:19:18", "Rs 1,200", "Rs 1,200",
    "Rs 42,000", "Rs 1,600", "Rs 2,40,625", "Rs 2,000", "64:49:20", "81:48:22", "Rs 1,26,000",
]


def normalized(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def masked(text):
    value = normalized(text)
    value = re.sub(r"\d[\d,]*(?:\.\d+)?%?", " <n> ", value)
    return " ".join(re.sub(r"[^a-z<> ]", " ", value).split())


def numeric_value(option):
    match = re.search(r"-?[\d,]+(?:\.\d+)?", option)
    assert match, option
    return float(match.group().replace(",", ""))


def test_schema_counts_provenance_and_independently_calculated_keys():
    questions = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    assert len(questions) == 90
    assert Counter(q["difficulty"] for q in questions) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    assert sum(q["source"].startswith("Verified from supplied Partnership PDF") for q in questions) == 22
    assert sum(q["source"] == "Original SSC-style practice question" for q in questions) == 68
    assert len(CALCULATED) == 68 and len(PDF_ANSWERS) == 22

    for index, row in enumerate(questions):
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == (
            "maths", "arithmetic-maths", "partnership"
        )
        assert row["is_pyq"] is False
        assert row.get("pyq_year") is None and row.get("pyq_exam_name") is None
        assert row["question_text"].strip() and row["explanation"].strip()
        assert set(row["options"]) == set("ABCD")
        assert len({normalized(value) for value in row["options"].values()}) == 4
        assert row["correct_option"] in row["options"]
        correct = row["options"][row["correct_option"]]
        assert sum(value == correct for value in row["options"].values()) == 1
        if index < 22:
            assert correct == PDF_ANSWERS[index], row["question_text"]
        else:
            expected = CALCULATED[index - 22]
            if isinstance(expected, str):
                assert correct == expected, row["question_text"]
            else:
                assert numeric_value(correct) == expected, row["question_text"]


def test_no_exact_number_masked_or_high_lexical_duplicates():
    questions = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    stems = [row["question_text"] for row in questions]
    assert len({normalized(stem) for stem in stems}) == 90
    for index, stem in enumerate(stems):
        for prior in stems[:index]:
            assert masked(stem) != masked(prior), f"number-masked duplicate: {stem!r} / {prior!r}"
            score = SequenceMatcher(None, normalized(stem), normalized(prior)).ratio()
            assert score < .92, f"high lexical similarity ({score:.3f}): {stem!r} / {prior!r}"
