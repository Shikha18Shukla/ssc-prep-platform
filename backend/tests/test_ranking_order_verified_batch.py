"""Artifact, independent-answer, and duplicate checks for Ranking and Order."""

import json
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path
from types import SimpleNamespace

from app.services.test_service import _selection_counts

BASE = Path(__file__).resolve().parents[1]
BATCH = BASE / "data" / "ranking_order_verified_batch.json"
LEDGER = BASE / "data" / "ranking_order_answer_ledger.json"
ORIGINAL = "Original SSC-style practice question"


def norm(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def records():
    return json.loads(BATCH.read_text(encoding="utf-8"))["questions"], json.loads(LEDGER.read_text(encoding="utf-8"))


def test_batch_ledger_options_provenance_and_difficulty_align():
    rows, ledger = records()
    assert len(rows) == len(ledger) == 30
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 10, "MEDIUM": 10, "HARD": 10}
    assert Counter("original" if row["source"] == ORIGINAL else "pdf" for row in rows) == {"pdf": 8, "original": 22}
    for i, (row, audit) in enumerate(zip(rows, ledger), 1):
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == ("reasoning", None, "ranking-and-order")
        assert row["is_pyq"] is False and row["pyq_year"] is None and row["pyq_exam_name"] is None
        assert row["question_text"].strip() and row["explanation"].strip()
        options = row["options"]
        assert set(options) == set("ABCD") and len({norm(x) for x in options.values()}) == 4
        assert row["correct_option"] in options
        assert audit["question_id"] == f"ranking-order-{i:03}" and audit["row"] == i
        assert audit["question"] == row["question_text"] and audit["options"] == options
        assert audit["expected_answer"] == options[row["correct_option"]]
        assert audit["difficulty"] == row["difficulty"] and audit["source"] == row["source"]
        assert audit["verification_status"].startswith("PASS")
        if row["source"] == ORIGINAL:
            assert audit["source_type"] == "original" and audit["source_pdf"] is None and audit["source_page"] is None
        else:
            assert audit["source_type"] == "pdf-derived" and audit["source_pdf"] in row["source"]
            assert isinstance(audit["source_page"], int)
    rejected = ledger[5]["rejected_source_questions"]
    assert len(rejected) == 1 and rejected[0]["source_page"] == 11
    assert "ambiguous" in rejected[0]["rejection_reason"]


def test_stems_signatures_and_canonical_chapter_batches_have_no_duplicates():
    rows, ledger = records()
    stems = [norm(row["question_text"]) for row in rows]
    assert len(set(stems)) == len(rows)
    signatures = [audit["concept_signature"] for audit in ledger]
    assert all(signatures) and len(set(signatures)) == len(rows)
    for i, stem in enumerate(stems):
        assert all(SequenceMatcher(None, stem, prior).ratio() < 0.97 for prior in stems[:i])
    paths = list((BASE / "data").glob("*.json")) + [BASE.parent / "maximum_and_minimum_value_verified_batch.json"]
    for path in paths:
        if path == BATCH:
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        old_rows = payload.get("questions", []) if isinstance(payload, dict) else []
        for old in old_rows if isinstance(old_rows, list) else []:
            if not isinstance(old, dict) or old.get("subject_slug") != "reasoning":
                continue
            candidate = norm(old.get("question_text", ""))
            assert candidate not in set(stems), f"Exact duplicate in {path.name}: {candidate}"
            assert all(SequenceMatcher(None, candidate, stem).ratio() < 0.97 for stem in stems), f"Near duplicate in {path.name}: {candidate}"


def test_independent_ranking_formula_and_interchange_checkpoints():
    rows, _ = records()
    answers = {row["question_text"]: row["options"][row["correct_option"]] for row in rows}
    assert answers["In a group of 40 students, S is 15th from the top. What is S's rank from the bottom?"] == "26th"
    assert answers["Amit is 7th from the top and 26th from the bottom in his class. How many students are there?"] == "32"
    assert answers["A person is 27th in a queue from one end and 38th from the other. How many people are in the queue?"] == "64"
    assert answers["There are 35 people in a group. Govind is 6th from the top, and Krishna is 7 places below him. What is Krishna's rank from the bottom?"] == "23rd"
    assert answers["Ram and Sham are 13th and 14th from the top, respectively, in a class of 23. What are their ranks from the bottom, respectively?"] == "11th and 10th"
    assert answers["Samsung is 37th from the right and Nokia is 31st from the left. After they interchange positions, Samsung is 46th from the right. How many students are in the row?"] == "76"
    assert answers["Sahil is 12th from the left and Gaurav is 18th from the right. After they interchange, Sahil is 25th from the left. How many people are in the row?"] == "42"
    assert answers["Sameer is 20th from the left and Arun is 12th from the right. After they interchange, Arun is 10th from the right. How many people are in the row?"] == "29"


def test_each_difficulty_supports_reasoning_test_minimum():
    rows, _ = records()
    counts = Counter(row["difficulty"] for row in rows)
    assert all(_selection_counts(counts[level], SimpleNamespace(slug="reasoning")) == [10] for level in ("EASY", "MEDIUM", "HARD"))
