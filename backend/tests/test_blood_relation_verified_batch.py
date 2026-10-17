"""Focused structural, provenance, deduplication, and answer checks for Blood Relation."""

import json
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
BATCH = BASE / "data" / "blood_relation_verified_batch.json"
LEDGER = BASE / "data" / "blood_relation_answer_ledger.json"
ORIGINAL = "Original SSC-style practice question"


def norm(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def records():
    return json.loads(BATCH.read_text(encoding="utf-8"))["questions"], json.loads(LEDGER.read_text(encoding="utf-8"))


def test_batch_schema_metadata_ledger_and_difficulty_distribution():
    rows, ledger = records()
    assert len(rows) == len(ledger) == 30
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 10, "MEDIUM": 12, "HARD": 8}
    assert Counter("original" if row["source"] == ORIGINAL else "pdf" for row in rows) == {"pdf": 14, "original": 16}
    for index, (row, audit) in enumerate(zip(rows, ledger), 1):
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == ("reasoning", None, "blood-relation")
        assert row["is_pyq"] is False and row["pyq_year"] is None and row["pyq_exam_name"] is None
        assert row["question_text"].strip() and row["explanation"].strip()
        assert row["difficulty"] in {"EASY", "MEDIUM", "HARD"}
        assert 0 < len(row["source"]) <= 255
        if row["source"] != ORIGINAL:
            assert row["source"].startswith("Blood relation 0")
            assert "lecture slide " in row["source"] and "exam/year not stated" in row["source"]
        options = row["options"]
        assert set(options) == set("ABCD")
        assert all(isinstance(value, str) and value.strip() for value in options.values())
        assert len({norm(value) for value in options.values()}) == 4
        assert row["correct_option"] in options
        assert audit["row"] == index and audit["question"] == row["question_text"]
        assert audit["expected_answer"] == options[row["correct_option"]]
        assert audit["correct_option"] == row["correct_option"]
        assert audit["difficulty"] == row["difficulty"] and audit["source"] == row["source"]
        assert audit["independent_reasoning"].strip() and audit["option_review"].strip()
        assert audit["concept_signature"].strip()


def test_stems_and_concept_signatures_are_unique_against_batches():
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
                assert norm(row["question_text"]) not in set(stems), f"Exact duplicate in {path.name}: {row['question_text']}"


def test_independently_solved_source_and_original_answer_checkpoints():
    rows, _ = records()
    keyed = {row["question_text"]: row["options"][row["correct_option"]] for row in rows}
    assert keyed[next(stem for stem in keyed if stem.startswith("A joint family has"))] == "9"
    assert keyed["F is the brother of G. G is the husband of H. H is the daughter of I, and I is the wife of J. How is F related to J?"] == "Daughter's husband's brother"
    assert keyed["Karishma introduces Reshma and says, ‘She is my father-in-law's daughter's daughter.’ How is Reshma related to Karishma?"] == "Niece"
    assert keyed["Rita is the sister of Mohan. Mohan is the father of Kiran. How is Rita related to Kiran?"] == "Paternal aunt"
    assert keyed["Pointing to a boy, Meena says, ‘He is the son of my father's only son.’ Meena has one brother, and her father has no other sons. How is the boy related to Meena?"] == "Nephew"
    assert keyed["The symbols mean: A+B: A is the father of B; A−B: A is the mother of B; A×B: A is the sister of B. How is P related to S in P×R−B+S?"] == "Father's maternal aunt"
