"""Independent PDF answer, schema, provenance, and duplicate checks."""
import json
import re
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BATCH = Path(__file__).resolve().parents[1] / "data" / "pipe_and_cistern_verified_batch.json"
PDF_ANSWERS = ["12 min", "15 min", "4 h", "15 min", "48 h", "20 h", "220 gal", "60 gal", "120 gal", "7:12 p.m.", "2:40 p.m.", "4 2/3 h", "115 min", "51 5/6 min", "4:00 p.m."]


def normalized(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def masked(value):
    value = normalized(value)
    value = re.sub(r"\d[\d,]*(?:\.\d+)?%?", " <n> ", value)
    return " ".join(re.sub(r"[^a-z<> ]", " ", value).split())


def test_batch_schema_provenance_answers_and_distribution():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    assert len(rows) == 90
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    assert len(PDF_ANSWERS) == 15
    assert sum(row["source"].startswith("Verified from supplied Pipe and Cistern PDF") for row in rows) == 15
    assert sum(row["source"] == "Original SSC-style practice question" for row in rows) == 75
    for index, row in enumerate(rows):
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == (
            "maths", "arithmetic-maths", "pipe-and-cistern")
        assert row["is_pyq"] is False and row.get("pyq_year") is None and row.get("pyq_exam_name") is None
        assert row["question_text"].strip() and row["explanation"].strip()
        assert set(row["options"]) == set("ABCD")
        assert len({normalized(value) for value in row["options"].values()}) == 4
        assert row["correct_option"] in row["options"]
        if index < 15:
            assert row["options"][row["correct_option"]].casefold() == PDF_ANSWERS[index].casefold(), row["question_text"]


def test_batch_has_no_exact_normalized_number_masked_or_high_lexical_duplicates():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    stems = [row["question_text"] for row in rows]
    assert len({normalized(stem) for stem in stems}) == 90
    for index, stem in enumerate(stems):
        for prior in stems[:index]:
            assert masked(stem) != masked(prior), f"number-masked duplicate: {stem!r} / {prior!r}"
            score = SequenceMatcher(None, normalized(stem), normalized(prior)).ratio()
            assert score < .92, f"high lexical similarity ({score:.3f}): {stem!r} / {prior!r}"
