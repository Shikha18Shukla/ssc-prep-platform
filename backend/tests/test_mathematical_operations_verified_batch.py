"""Focused structural, provenance, duplicate, and answer checks for the bank."""

import json
import sys
import unicodedata
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
BATCH = BASE / "data" / "mathematical_operations_verified_batch.json"
LEDGER = BASE / "data" / "mathematical_operations_answer_ledger.json"
sys.path.insert(0, str(BASE))
from scripts.import_mathematical_operations_verified_batch import load_artifacts, verify_existing


def norm(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def artifacts():
    return json.loads(BATCH.read_text(encoding="utf-8"))["questions"], json.loads(LEDGER.read_text(encoding="utf-8"))


def test_batch_schema_options_metadata_and_difficulty():
    rows, ledger = artifacts()
    assert len(rows) == len(ledger) == 30
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 10, "MEDIUM": 12, "HARD": 8}
    assert Counter("pdf1" if "01 _.pdf" in row["source"] else "pdf2" for row in rows) == {"pdf1": 12, "pdf2": 18}
    for i, (row, audit) in enumerate(zip(rows, ledger), 1):
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == ("reasoning", None, "mathematical-operations")
        assert row["is_pyq"] is False and row["pyq_year"] is None and row["pyq_exam_name"] is None
        assert row["question_text"].strip() and row["explanation"].strip()
        assert row["difficulty"] in {"EASY", "MEDIUM", "HARD"}
        assert row["source"].endswith("; exam/year not stated")
        assert row["source"].startswith("Mathematical Operations 0")
        options = row["options"]
        assert set(options) == set("ABCD")
        assert all(isinstance(value, str) and value.strip() for value in options.values())
        assert len({norm(value) for value in options.values()}) == 4
        assert row["correct_option"] in options
        assert audit["row"] == i and audit["question"] == row["question_text"]
        assert audit["expected_answer"] == options[row["correct_option"]]
        assert audit["correct_option"] == row["correct_option"]
        assert audit["difficulty"] == row["difficulty"] and audit["source"] == row["source"]
        assert audit["source_type"] == "pdf-derived"
        assert audit["independent_reasoning"].strip() and audit["option_review"].strip()
        assert audit["concept_signature"].strip() and audit["duplicate_review"].strip()


def test_stems_signatures_and_available_batch_stems_are_unique():
    rows, ledger = artifacts()
    stems = [norm(row["question_text"]) for row in rows]
    signatures = [entry["concept_signature"] for entry in ledger]
    assert len(set(stems)) == len(set(signatures)) == 30
    for path in (BASE / "data").glob("*.json"):
        if path in {BATCH, LEDGER}:
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        prior = payload.get("questions", []) if isinstance(payload, dict) else []
        for item in prior if isinstance(prior, list) else []:
            if isinstance(item, dict) and isinstance(item.get("question_text"), str):
                assert norm(item["question_text"]) not in set(stems), f"Duplicate stem in {path.name}: {item['question_text']}"


def test_independent_answer_checkpoints_and_exact_duplicate_exclusions():
    rows, _ = artifacts()
    keyed = {row["question_text"]: row["options"][row["correct_option"]] for row in rows}
    assert keyed["If A stands for ÷, B for ×, C for +, and D for −, what is 46 A 2 C 21 D 8 B 3?"] == "20"
    assert keyed["If P represents +, R represents ×, S represents −, and T represents ÷, what is 5 R 9 P 7 S 9 T 3 P 6?"] == "55"
    assert keyed["Choose the correct sequence of mathematical symbols to balance 15 * 24 * 3 * 6 * 17."] == "+, ÷, −, ="
    assert keyed["If A denotes +, B denotes ×, C denotes −, and D denotes ÷, evaluate 34 A 15 B 3 C 11 B 2 A (51 D 17)."] == "60"
    assert keyed["In a code, a=0, b=1, c=2, d=3, e=4, f=5, g=6, h=7, i=8, and j=9. Evaluate (dc×f)−(bf−d)×d, then write the result using the same digit-to-letter code."] == "bce"
    assert keyed["Evaluate 108÷36×1/4 + 2/5×1/4 using standard order of operations."] == "17/20"
    assert keyed["Evaluate 100÷10−[−2+{−9+(3−6×2)}] using standard order of operations."] == "30"
    assert not any("Mathematical Operations 01 _.pdf, page 6;" in row["source"] for row in rows)
    assert not any("Mathematical Operations 01 _.pdf, page 8;" in row["source"] for row in rows)
    assert not any("Mathematical Operations 01 _.pdf, page 11;" in row["source"] for row in rows)
    assert not any("Mathematical Operations 01 _.pdf, page 20;" in row["source"] for row in rows)


def test_importer_load_validation_and_exact_chapter_pin():
    rows = load_artifacts()
    assert len(rows) == 30
    assert verify_existing(rows, []) == {}
