"""Source, answer, duplicate, importer-safety and chapter-flow checks for CH-15."""

import json
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path
from types import SimpleNamespace

from scripts import build_word_building_artifacts as builder
from scripts import import_word_building_verified_batch as importer

BASE = Path(__file__).resolve().parents[1]
BATCH = BASE / "data" / "word_building_verified_batch.json"
LEDGER = BASE / "data" / "word_building_answer_ledger.json"
ORIGINAL = "Original SSC-style practice question"


def norm(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def records():
    return json.loads(BATCH.read_text(encoding="utf-8"))["questions"], json.loads(LEDGER.read_text(encoding="utf-8"))


def test_batch_schema_difficulty_sources_and_ledger_alignment():
    rows, ledger = records()
    assert len(rows) == len(ledger) == 30
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 10, "MEDIUM": 10, "HARD": 10}
    assert Counter("original" if row["source"] == ORIGINAL else "pdf" for row in rows) == {"pdf": 20, "original": 10}
    assert Counter(entry["topic"] for entry in ledger) == {
        "dictionary_arrangement": 4,
        "word_formation": 5,
        "letter_jumbling": 7,
        "prefix_suffix": 4,
        "alphabetical_positions": 5,
        "letter_pairs": 5,
    }
    for index, (row, audit) in enumerate(zip(rows, ledger), 1):
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == ("reasoning", None, "word-building")
        assert audit["chapter_id"] == importer.EXPECTED_CHAPTER_ID
        assert row["is_pyq"] is False and row["pyq_year"] is None and row["pyq_exam_name"] is None
        assert row["difficulty"] in {"EASY", "MEDIUM", "HARD"}
        assert row["question_text"].strip() and row["explanation"].strip() and len(row["source"]) <= 255
        options = row["options"]
        assert set(options) == set("ABCD") and len({norm(v) for v in options.values()}) == 4
        assert all(isinstance(v, str) and v.strip() for v in options.values())
        assert row["correct_option"] in options
        assert audit["expected_answer"] == options[row["correct_option"]]
        assert audit["question_id"] == f"word-building-{index:03}"
        assert audit["question"] == row["question_text"]
        assert audit["source"] == row["source"] and audit["difficulty"] == row["difficulty"]
        assert audit["independent_verification"].strip() and audit["validation_status"].startswith("PASS")
        if row["source"] == ORIGINAL:
            assert audit["source_type"] == "original" and audit["source_pdf"] is None and audit["source_page"] is None
        else:
            assert audit["source_type"] == "pdf-derived" and audit["source_pdf"] in row["source"]
            assert isinstance(audit["source_page"], int) and audit["source_page"] > 0


def test_independent_letter_algorithm_checks_and_answer_key():
    rows, ledger = records()
    by_signature = {audit["concept_signature"]: row for row, audit in zip(rows, ledger)}
    for x in builder.ITEMS:
        builder.validate(x)
    assert by_signature["source_grape_dictionary_order"]["options"]["C"] == "1, 3, 5, 4, 2"
    assert by_signature["source_author_number_sequence"]["options"]["A"] == "6, 4, 2, 1, 5, 3"
    assert by_signature["source_develop_unchanged_count"]["options"]["A"] == "2"
    assert by_signature["source_fancier_letter_pairs"]["options"]["D"] == "More than three"
    assert builder.pair_list("PERHAPS") == [["P", "R"]]
    assert builder.pair_list("FANCIER") == [["F", "C"], ["A", "C"], ["A", "E"], ["N", "R"], ["C", "E"]]
    assert builder.pair_list("BEACON") == [["E", "C"], ["O", "N"]]


def test_stems_concepts_and_canonical_reasoning_batches_have_no_duplicates():
    rows, ledger = records()
    stems = [norm(row["question_text"]) for row in rows]
    signatures = [entry["concept_signature"] for entry in ledger]
    assert len(set(stems)) == len(rows)
    assert len(set(signatures)) == len(rows)
    assert importer.check_canonical_duplicates(rows) >= 500
    paths = list((BASE / "data").glob("*.json")) + [BASE / "maximum_and_minimum_value_verified_batch.json"]
    for path in paths:
        if path == BATCH or not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        prior_rows = data.get("questions", []) if isinstance(data, dict) else []
        for prior in prior_rows if isinstance(prior_rows, list) else []:
            if not isinstance(prior, dict) or prior.get("subject_slug") != "reasoning":
                continue
            candidate = norm(prior.get("question_text", ""))
            assert candidate not in set(stems)
            assert all(SequenceMatcher(None, candidate, stem).ratio() < 0.94 for stem in stems)


class _FakeSession:
    def __init__(self, existing):
        self.existing = existing

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def scalars(self, _query):
        return SimpleNamespace(all=lambda: self.existing)


def _mock_questions(rows):
    questions = []
    for row in rows:
        questions.append(SimpleNamespace(
            question_text=row["question_text"], explanation=row["explanation"],
            difficulty=SimpleNamespace(value=row["difficulty"]), is_pyq=False,
            pyq_year=None, pyq_exam_name=None, source=row["source"], is_active=True,
            options=[SimpleNamespace(option_key=key, option_text=value, is_correct=key == row["correct_option"])
                     for key, value in row["options"].items()],
        ))
    return questions


def test_importer_dry_run_and_idempotent_replay_do_not_write(monkeypatch, capsys):
    rows, _ = records()
    chapter = SimpleNamespace(id=importer.EXPECTED_CHAPTER_ID, name="Word Building")
    db = _FakeSession([])
    monkeypatch.setattr(importer, "SessionLocal", lambda: db)
    monkeypatch.setattr(importer, "chapter_context", lambda _db: (None, None, chapter))
    monkeypatch.setattr(importer, "check_reasoning_duplicates", lambda *_: 520)
    called = []

    def preview(*args):
        called.append(args[-1])
        return SimpleNamespace(aborted=False, errors=[], rejected=0, duplicates=0,
                               would_import=30, model_dump=lambda: {"would_import": 30, "duplicates": 0})

    monkeypatch.setattr(importer, "import_questions", preview)
    importer.main([])
    assert called == [True]
    assert "NO_DATABASE_CHANGES" in capsys.readouterr().out

    existing = _mock_questions(rows)
    monkeypatch.setattr(importer, "SessionLocal", lambda: _FakeSession(existing))
    called.clear()

    def replay_preview(*args):
        called.append(args[-1])
        return SimpleNamespace(aborted=False, errors=[], rejected=0, duplicates=30,
                               would_import=0, model_dump=lambda: {"would_import": 0, "duplicates": 30})

    monkeypatch.setattr(importer, "import_questions", replay_preview)
    importer.main(["--apply"])
    output = capsys.readouterr().out
    assert called == [True]
    assert "IDEMPOTENT_REPLAY" in output
