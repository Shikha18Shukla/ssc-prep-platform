"""Schema, provenance, answer-ledger and duplicate checks for the DI batch."""
import json
import re
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BATCH = Path(__file__).resolve().parents[1] / "data" / "data_interpretation_verified_batch.json"
LEDGER = Path(__file__).resolve().parents[1] / "data" / "data_interpretation_answer_ledger.json"
PDF_EXPECTED = {
    5: "16:11", 6: "500%", 7: "260", 9: "40:33", 10: "Neither I nor II",
    11: "54%", 12: "Only II", 13: "0", 14: "85:76", 15: "1:00 p.m.",
    16: "Y3", 17: "Only I", 18: "40%", 19: "125", 20: "A",
}


def normalized(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def number_masked(value):
    value = normalized(value)
    value = re.sub(r"\b\d+(?:,\d{3})*(?:\.\d+)?%?\b", " <n> ", value)
    return " ".join(re.sub(r"[^a-z<> ]", " ", value).split())


def test_batch_schema_distribution_provenance_and_independent_source_answers():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    assert len(rows) == len(ledger) == 90
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    pdf_rows = [row for row in rows if row["source"].startswith("Verified from supplied Data Interpretation PDF")]
    assert len(pdf_rows) == 15
    assert sum(row["source"] == "Original SSC-style practice question" for row in rows) == 75
    assert [int(re.search(r"page (\d+);", row["source"]).group(1)) for row in pdf_rows] == list(PDF_EXPECTED)
    for row, audit in zip(rows, ledger):
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == (
            "maths", "arithmetic-maths", "data-interpretation")
        assert row["is_pyq"] is False and row.get("pyq_year") is None and row.get("pyq_exam_name") is None
        assert row["question_text"].strip() and row["explanation"].strip()
        assert set(row["options"]) == set("ABCD")
        assert len({normalized(v) for v in row["options"].values()}) == 4
        assert row["correct_option"] in row["options"]
        assert row["options"][row["correct_option"]] == audit["expected_answer"]
    for row in pdf_rows:
        page = int(re.search(r"page (\d+);", row["source"]).group(1))
        assert row["options"][row["correct_option"]] == PDF_EXPECTED[page]


def test_batch_stems_have_no_exact_normalized_number_masked_or_lexical_duplicates():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    stems = [row["question_text"] for row in rows]
    assert len({normalized(stem) for stem in stems}) == len(stems)
    for index, stem in enumerate(stems):
        for prior in stems[:index]:
            assert number_masked(stem) != number_masked(prior), f"number-masked duplicate: {stem!r} / {prior!r}"
            score = SequenceMatcher(None, normalized(stem), normalized(prior)).ratio()
            assert score < .92, f"lexical near duplicate {score:.3f}: {stem!r} / {prior!r}"
