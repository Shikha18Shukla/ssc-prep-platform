"""Independent answer-key, provenance, and duplicate checks for Mixture."""
import json
import re
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BATCH = Path(__file__).resolve().parents[1] / "data" / "mixture_verified_batch.json"

# Recomputed from each original stem, separately from its generated choices.
CALCULATED = [
    "11:9", "5 L", "3.6 kg", "10 L", "Rs 26/kg", "35%", "12 kg", "25%", "4 L", "4 L",
    "Rs 390/kg", "4 L", "10 kg", "3:5", "15 kg", "1:1", "3 L", "30%", "Rs 92/kg", "12 L",
    "Rs 144/kg", "22.5%", "4 L", "32.5%", "7:8",
    "3:2", "1:1", "4:1", "21:19", "23.6667%", "24 kg", "15 L", "5 kg", "44%", "44%",
    "5:4", "10 kg", "20 L", "2.5 kg", "45%", "24 kg", "35%", "9:7", "43.3333%",
    "1.25 kg", "3.75 L", "31.5%", "5 L",
    "45.9375%", "36%", "32.8%", "10 kg", "60 kg", "40%", "7:3", "26.6667 L",
    "36.875%", "45%", "31.2%", "2.6667 L", "14.4 L", "45%", "2:1", "39%", "11.4286 L",
    "40 L", "15 kg", "6.6667 L", "240 L", "8 kg", "67.6%", "41.6%", "7.5 kg", "37.5 L",
]

PDF_ANSWERS = [
    "N.O.T.", "45 litres", "10 litres", "800 g", "33 1/3", "2:1", "59:53", "50.7%",
    "9:11", "11:14", "14:31", "24 2/7%", "4:7", "21:8", "7:4", "7:5",
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


def test_batch_schema_provenance_and_independently_checked_answers():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    assert len(rows) == 90
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    assert sum(row["source"].startswith("Verified from supplied Mixture PDF") for row in rows) == 16
    assert sum(row["source"] == "Original SSC-style practice question" for row in rows) == 74
    assert len(PDF_ANSWERS) == 16 and len(CALCULATED) == 74

    for index, row in enumerate(rows):
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == (
            "maths", "arithmetic-maths", "mixture"
        )
        assert row["is_pyq"] is False
        assert row.get("pyq_year") is None and row.get("pyq_exam_name") is None
        assert row["question_text"].strip() and row["explanation"].strip()
        assert set(row["options"]) == set("ABCD")
        assert len({normalized(value) for value in row["options"].values()}) == 4
        assert row["correct_option"] in row["options"]
        correct = row["options"][row["correct_option"]]
        assert sum(value == correct for value in row["options"].values()) == 1
        expected = PDF_ANSWERS[index] if index < 16 else CALCULATED[index - 16]
        if ":" in expected or expected == "N.O.T." or "/" in expected:
            assert correct == expected, row["question_text"]
        else:
            assert numeric_value(correct) == numeric_value(expected), row["question_text"]


def test_no_exact_normalized_number_masked_or_high_lexical_duplicates():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    stems = [row["question_text"] for row in rows]
    assert len({normalized(stem) for stem in stems}) == 90
    for index, stem in enumerate(stems):
        for prior in stems[:index]:
            assert masked(stem) != masked(prior), f"number-masked duplicate: {stem!r} / {prior!r}"
            score = SequenceMatcher(None, normalized(stem), normalized(prior)).ratio()
            assert score < .92, f"high lexical similarity ({score:.3f}): {stem!r} / {prior!r}"
