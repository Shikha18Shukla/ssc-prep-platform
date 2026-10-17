"""Batch shape, provenance, answer-ledger alignment, and duplicate checks."""
import json
import unicodedata
from collections import Counter
from difflib import SequenceMatcher

from scripts.import_maximum_and_minimum_value_verified_batch import BATCH, LEDGER, load_batch


def norm(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def test_batch_and_ledger_have_required_distribution_and_metadata():
    rows = load_batch()
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    assert len(rows) == len(ledger) == 90
    assert Counter(r["difficulty"] for r in rows) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    assert sum(r["source"] != "Original SSC-style practice question" for r in rows) == 16
    assert sum(r["is_pyq"] for r in rows) == 0
    for i, row in enumerate(rows, 1):
        assert row["chapter_slug"] == "maximum-and-minimum-value"
        assert row["options"][row["correct_option"]] == ledger[i-1]["expected_answer"]
        assert len({norm(v) for v in row["options"].values()}) == 4


def test_stems_have_no_exact_or_near_verbatim_duplicates():
    stems = [norm(r["question_text"]) for r in json.loads(BATCH.read_text(encoding="utf-8"))["questions"]]
    assert len(set(stems)) == 90
    for i, stem in enumerate(stems):
        assert all(SequenceMatcher(None, stem, old).ratio() < .97 for old in stems[:i])


def test_source_rows_use_reviewed_pdf_pages_and_originals_are_labelled():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    sourced = [r for r in rows if r["source"] != "Original SSC-style practice question"]
    assert len(sourced) == 16
    assert all("Maximum and  Minimum Value.pdf, PDF page " in r["source"] for r in sourced)
    assert all(r["source"] == "Original SSC-style practice question" for r in rows if r not in sourced)
