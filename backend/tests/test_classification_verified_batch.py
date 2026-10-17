"""Artifact checks for the reviewed Classification Normal bank."""

import json
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
BATCH = BASE / "data" / "classification_verified_batch.json"
LEDGER = BASE / "data" / "classification_answer_ledger.json"
ORIGINAL = "Original SSC-style practice question"


def norm(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def records():
    return json.loads(BATCH.read_text(encoding="utf-8"))["questions"], json.loads(LEDGER.read_text(encoding="utf-8"))


def test_batch_schema_metadata_answer_ledger_and_distribution():
    rows, ledger = records()
    assert len(rows) == len(ledger) == 30
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 10, "MEDIUM": 12, "HARD": 8}
    assert Counter("original" if row["source"] == ORIGINAL else "pdf" for row in rows) == {"pdf": 17, "original": 13}
    for index, (row, audit) in enumerate(zip(rows, ledger), 1):
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == ("reasoning", None, "classification")
        assert row["is_pyq"] is False and row["pyq_year"] is None and row["pyq_exam_name"] is None
        assert row["question_text"].strip() and row["explanation"].strip()
        assert row["difficulty"] in {"EASY", "MEDIUM", "HARD"}
        assert 0 < len(row["source"]) <= 255
        if row["source"] != ORIGINAL:
            assert row["source"].startswith("Classification 0")
            assert "lecture slide " in row["source"] and "exam/year not stated" in row["source"]
        options = row["options"]
        assert set(options) == set("ABCD")
        assert all(isinstance(value, str) and value.strip() for value in options.values())
        assert len({norm(value) for value in options.values()}) == 4
        key = row["correct_option"]
        assert key in options
        assert audit["row"] == index and audit["question"] == row["question_text"]
        assert audit["expected_answer"] == options[key] and audit["correct_option"] == key
        assert audit["difficulty"] == row["difficulty"] and audit["source"] == row["source"]
        assert audit["independent_reasoning"].strip() and audit["option_review"].strip()
        assert audit["concept_signature"].strip()


def test_stems_and_problem_signatures_are_unique_across_artifacts():
    rows, ledger = records()
    stems = [norm(row["question_text"]) for row in rows]
    signatures = [entry["concept_signature"] for entry in ledger]
    assert len(set(stems)) == len(set(signatures)) == 30
    for index, stem in enumerate(stems):
        assert all(SequenceMatcher(None, stem, other).ratio() < 0.97 for other in stems[:index])
    for path in (BASE / "data").glob("*.json"):
        if path == BATCH:
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        previous = payload.get("questions", []) if isinstance(payload, dict) else []
        for row in previous if isinstance(previous, list) else []:
            if isinstance(row, dict) and isinstance(row.get("question_text"), str):
                candidate = norm(row["question_text"])
                assert candidate not in set(stems), f"Exact duplicate in {path.name}: {row['question_text']}"
                if row.get("chapter_slug") == "classification":
                    assert all(SequenceMatcher(None, candidate, stem).ratio() < 0.97 for stem in stems)


def test_independently_recomputed_numeric_checkpoints():
    rows, _ = records()
    keyed = {row["question_text"]: row["options"][row["correct_option"]] for row in rows}
    assert keyed["Which number pair is inconsistent with the rule n → n³+n?"] == "1 : 4"
    assert keyed["Which number pair is different from the other three?"] == "18 : 42"
    assert keyed["Which triple does not follow the same rule as the others?"] == "3, 27, 19"
    assert keyed["Which group of three numbers is different?"] == "100, 90, 85"
    assert keyed["Which number triple does not follow the same rule?"] == "7, 70, 1600"
    assert keyed["Which triplet is inconsistent with the others?"] == "5 : 10 : 125"
    assert keyed["Which group does not follow the same rule?"] == "8, 17, 25"
    assert keyed["Which number triple is different by the relation between consecutive entries?"] == "6, 19, 59"
