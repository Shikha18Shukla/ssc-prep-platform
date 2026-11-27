"""Shared rules for the Banking Clerk/PO three-section chapter rollout."""

from __future__ import annotations

import re
import unicodedata
from difflib import SequenceMatcher
from itertools import combinations

EXAM_SLUGS = ("banking-clerk", "banking-po")
SUBJECT_SLUGS = ("english", "general-banking-awareness", "computer")
SECTION_COUNTS = (10, 15, 15)
SECONDS_PER_QUESTION = 42
NEAR_DUPLICATE_THRESHOLD = 0.90


def key(value: str) -> str:
    """Convert a catalog slug to the stable section-name key format."""
    return value.replace("-", "_")


def section_name(exam_slug: str, subject_slug: str, chapter_slug: str, part: int) -> str:
    """Return the globally unique section string used by the backend."""
    return f"{key(exam_slug)}_{key(subject_slug)}_{key(chapter_slug)}_part_{part}"


def expected_sections(exam_slug: str, subject_slug: str, chapter_slug: str) -> list[str]:
    return [section_name(exam_slug, subject_slug, chapter_slug, part) for part in range(1, 4)]


def normalize_question_text(value: str) -> str:
    """Match the importer's normalized-content comparison."""
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def mask_numbers(normalized_text: str) -> str:
    return re.sub(r"\d+(?:\.\d+)?", "#", normalized_text)


def near_duplicate_pairs(texts: list[str], threshold: float = NEAR_DUPLICATE_THRESHOLD) -> int:
    """Count sorted-set pairs at or above the lexical similarity threshold."""
    ordered = sorted(set(texts))
    return sum(
        1
        for left, right in combinations(ordered, 2)
        if SequenceMatcher(None, left, right).ratio() >= threshold
    )


def plan_allocation(active_rows: list[dict]) -> tuple[list[str], dict[str, int]]:
    """Choose 40 unique active questions deterministically.

    Rows are ordered by creation time then id, and duplicate normalized
    question texts are skipped. The same input therefore always produces the
    same 10/15/15 allocation.
    """
    ordered = sorted(
        active_rows,
        key=lambda row: (
            str(row.get("created_at") or ""),
            str(row["question_id"]),
        ),
    )
    chosen: list[str] = []
    seen_texts: set[str] = set()
    duplicate_active_rows = 0
    for row in ordered:
        normalized = normalize_question_text(row["question_text"])
        if normalized in seen_texts:
            duplicate_active_rows += 1
            continue
        seen_texts.add(normalized)
        chosen.append(str(row["question_id"]))
        if len(chosen) == sum(SECTION_COUNTS):
            break
    allocation: dict[str, int] = {}
    cursor = 0
    for part, count in enumerate(SECTION_COUNTS, start=1):
        allocation[f"part_{part}"] = count
        cursor += count
    return chosen, {"duplicate_active_rows_skipped": duplicate_active_rows}


def split_allocation(question_ids: list[str]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {"part_1": [], "part_2": [], "part_3": []}
    cursor = 0
    for part, count in enumerate(SECTION_COUNTS, start=1):
        result[f"part_{part}"] = question_ids[cursor:cursor + count]
        cursor += count
    return result
