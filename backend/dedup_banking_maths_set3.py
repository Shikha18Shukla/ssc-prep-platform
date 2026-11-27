# -*- coding: utf-8 -*-
"""Deduplicate the third Banking Maths batch.

Screening order:
  1. exact and normalized duplicates inside the new 720 questions,
  2. number-masked template families inside each chapter,
  3. exact/normalized/number-masked collisions against Banking Maths Sets 1+2,
  4. exact/normalized/number-masked collisions against every existing DB question,
  5. lexical near-duplicates (token + bigram Jaccard, digits retained),
  6. semantic near-duplicates (domain signature + number-masked sequence ratio).

Semantic and lexical hits are listed for manual review.  Only exact,
normalized, number-masked and high lexical hits are treated as hard failures.

Usage (process-only override; never edit .env):
    # DATABASE_URL is supplied through the process environment for an isolated local database
    python backend/dedup_banking_maths_set3.py
"""

from __future__ import annotations

import json
import math
import os
import re
from collections import Counter, defaultdict
from difflib import SequenceMatcher

import psycopg2

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
REPORTS = os.path.join(ROOT, "reports")

NEW_FILES = {
    "simple_interest": "banking_maths_simple_interest_questions.json",
    "compound_interest": "banking_maths_compound_interest_questions.json",
    "mixture_alligation": "banking_maths_mixture_alligation_questions.json",
    "problems_on_age": "banking_maths_problems_on_age_questions.json",
    "partnership": "banking_maths_partnership_questions.json",
    "time_and_work": "banking_maths_time_and_work_questions.json",
}
OLD_FILES = [
    "banking_maths_vedic_calculation_questions.json",
    "banking_maths_simplification_questions.json",
    "banking_maths_approximation_questions.json",
    "banking_maths_missing_number_series_questions.json",
    "banking_maths_wrong_number_series_questions.json",
    "banking_maths_quadratic_equations_questions.json",
    "banking_maths_number_system_questions.json",
    "banking_maths_percentage_questions.json",
    "banking_maths_ratio_proportion_questions.json",
    "banking_maths_profit_loss_discount_questions.json",
]

STOPWORDS = {
    "a", "an", "the", "of", "is", "are", "was", "were", "what", "which", "find",
    "if", "then", "and", "or", "to", "in", "by", "for", "on", "at", "from",
    "with", "how", "many", "much", "value", "respectively", "rs", "his", "her",
    "it", "its", "be", "as", "that", "this", "these", "those", "given", "following",
    "will", "would", "can", "needs", "need", "take", "takes", "work", "year",
    "years", "day", "days", "months", "month", "hours", "hour", "question",
}

LEXICAL_THRESHOLD = 0.90
SEMANTIC_THRESHOLD = 0.78
MIN_BIGRAMS = 4
MIN_OVERLAP = 3

DOMAIN_PATTERNS = [
    ("simple_interest", re.compile(r"simple interest|si\s*=|rate of simple interest")),
    ("compound_interest", re.compile(r"compound interest|ci\s*=|amount.*compound|compounded")),
    ("mixture_alligation", re.compile(r"alligation|mean price|mixture|milk|water|solution|proportion.*mix")),
    ("problems_on_age", re.compile(r"\bage[sd]?\b|years old|older|younger|father|mother|son|daughter")),
    ("partnership", re.compile(r"partner|invests?|capital|profit share|profit.*ratio|business")),
    ("time_and_work", re.compile(r"works? together|one.day work|efficien|pipe|tank|outlet|leak|labourer|worker-days")),
]


def normalize(text: str) -> str:
    text = str(text).lower().replace("\u00d7", "x").replace("\u2013", "-")
    text = re.sub(r"[^a-z0-9/%.:+\- ]", " ", text)
    return " ".join(text.split())


def mask_numbers(text: str) -> str:
    return re.sub(r"\d+(?:\.\d+)?", "#", normalize(text))


def words(text: str) -> list[str]:
    return [w for w in re.findall(r"[a-z0-9]+", normalize(text)) if w not in STOPWORDS]


def tokens(text: str) -> frozenset[str]:
    return frozenset(words(text))


def bigrams(text: str) -> frozenset[tuple[str, str]]:
    seq = words(text)
    return frozenset(zip(seq, seq[1:]))


def domain_signature(text: str) -> tuple[str, ...]:
    lowered = str(text).lower()
    tags = tuple(name for name, pattern in DOMAIN_PATTERNS if pattern.search(lowered))
    return tags or ("general",)


def jaccard(a, b) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def similarity(left, right) -> float:
    return (jaccard(left["_tokens"], right["_tokens"]) + jaccard(left["_bigrams"], right["_bigrams"])) / 2


def prepare(item, label: str) -> dict:
    item = dict(item)
    text = item["question_text"]
    item["_label"] = label
    item["_norm"] = normalize(text)
    item["_mask"] = mask_numbers(text)
    item["_tokens"] = tokens(text)
    item["_bigrams"] = bigrams(text)
    item["_domains"] = domain_signature(text)
    return item


def load_new() -> list[dict]:
    items = []
    for chapter_key, filename in NEW_FILES.items():
        with open(os.path.join(DATA, filename), encoding="utf-8") as handle:
            for item in json.load(handle):
                items.append(prepare(item, item.get("id", chapter_key)))
    return items


def load_old() -> list[dict]:
    items = []
    for filename in OLD_FILES:
        path = os.path.join(DATA, filename)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as handle:
            for item in json.load(handle):
                items.append(prepare(item, item.get("id", filename)))
    return items


def load_db() -> list[dict]:
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise SystemExit("DATABASE_URL is required for the database comparison")
    conn = psycopg2.connect(url)
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id::text, question_text FROM questions")
            return [prepare({"id": row[0], "question_text": row[1]}, row[0]) for row in cur.fetchall()]
    finally:
        conn.close()


def build_index(pool: list[dict]) -> dict[str, set[int]]:
    index: dict[str, set[int]] = defaultdict(set)
    for position, item in enumerate(pool):
        for token in item["_tokens"]:
            index[token].add(position)
    return index


def candidate_pairs(new: list[dict], pool: list[dict], index: dict[str, set[int]]):
    """Yield (new item, pool item, lexical score, semantic score) for plausible pairs."""
    for item in new:
        if len(item["_bigrams"]) < MIN_BIGRAMS:
            continue
        counts: Counter[int] = Counter()
        for token in item["_tokens"]:
            counts.update(index.get(token, ()))
        for position, overlap in counts.items():
            if overlap < MIN_OVERLAP:
                continue
            other = pool[position]
            if len(other["_bigrams"]) < MIN_BIGRAMS:
                continue
            lexical = similarity(item, other)
            if lexical < 0.55:
                continue
            semantic = 0.0
            if set(item["_domains"]) & set(other["_domains"]):
                semantic = SequenceMatcher(
                    None, item["_mask"], other["_mask"], autojunk=False
                ).ratio()
            yield item, other, lexical, semantic


def hit_label(item: dict) -> str:
    return str(item.get("_label") or item.get("id") or item["question_text"][:60])


def main() -> int:
    new = load_new()
    old = load_old()
    db = load_db()
    old_index = build_index(old)
    db_index = build_index(db)

    lines = ["# Banking Maths Set 3 - Deduplication Report", ""]
    problems: list[str] = []

    # 1. Exact and normalized duplicates inside the new batch.
    exact = Counter(item["question_text"] for item in new)
    normalized = Counter(item["_norm"] for item in new)
    exact_dupes = [text for text, count in exact.items() if count > 1]
    norm_dupes = [text for text, count in normalized.items() if count > 1]
    lines += ["## Within the new 720 questions", ""]
    lines.append(f"- Exact duplicate texts: {len(exact_dupes)}")
    lines.append(f"- Normalized duplicate texts: {len(norm_dupes)}")
    if exact_dupes or norm_dupes:
        problems.append("duplicate question text inside the new batch")

    # 2. Number-masked template families per chapter.
    per_chapter = defaultdict(Counter)
    for item in new:
        chapter = item.get("chapter_key", "unknown")
        per_chapter[chapter][item["_mask"]] += 1
    lines += [
        "",
        "Number-masked families per chapter (fresh values are expected):",
        "",
        "| Chapter | Questions | Distinct templates | Largest family | Share |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for chapter, counts in sorted(per_chapter.items()):
        total = sum(counts.values())
        biggest = max(counts.values())
        lines.append(
            f"| {chapter} | {total} | {len(counts)} | {biggest} | {biggest / total:.1%} |"
        )
        repeated = [mask for mask, count in counts.items() if count > 1]
        if repeated:
            lines.append(f"- Repeated number-masked templates in {chapter}: {len(repeated)}")
            problems.append(f"{chapter}: repeated number-masked template")
    lines.append("")

    # 3/4. Exact, normalized and masked collisions with the prior batches and DB.
    def collision_section(title: str, pool: list[dict]) -> None:
        norms = {item["_norm"] for item in pool}
        masks = {item["_mask"] for item in pool}
        norm_hits = [item for item in new if item["_norm"] in norms]
        mask_hits = [item for item in new if item["_mask"] in masks]
        lines.extend([
            f"## {title}",
            "",
            f"- Questions screened: {len(new)}",
            f"- Pool screened: {len(pool)}",
            f"- Exact/normalized matches: {len(norm_hits)}",
            f"- Number-masked (template) matches: {len(mask_hits)}",
            "",
        ])
        for item in norm_hits[:20]:
            lines.append(f"- Normalized match: {hit_label(item)}")
        for item in mask_hits[:20]:
            lines.append(f"- Number-masked match: {hit_label(item)}")
        if norm_hits:
            problems.append(f"normalized collision against {title.lower()}")
        if mask_hits:
            problems.append(f"number-masked collision against {title.lower()}")

    collision_section("Against Banking Maths Sets 1 and 2", old)
    collision_section("Against existing database questions", db)

    # 5/6. Lexical and semantic near-duplicates for manual review.
    lexical_old: list[tuple[float, str, str]] = []
    lexical_db: list[tuple[float, str, str]] = []
    semantic_old: list[tuple[float, str, str]] = []
    semantic_db: list[tuple[float, str, str]] = []
    for item, other, lexical, semantic in candidate_pairs(new, old, old_index):
        if lexical >= LEXICAL_THRESHOLD:
            lexical_old.append((lexical, hit_label(item), hit_label(other)))
        if semantic >= SEMANTIC_THRESHOLD:
            semantic_old.append((semantic, hit_label(item), hit_label(other)))
    for item, other, lexical, semantic in candidate_pairs(new, db, db_index):
        if lexical >= LEXICAL_THRESHOLD:
            lexical_db.append((lexical, hit_label(item), hit_label(other)))
        if semantic >= SEMANTIC_THRESHOLD:
            semantic_db.append((semantic, hit_label(item), hit_label(other)))

    lexical_old.sort(reverse=True)
    lexical_db.sort(reverse=True)
    semantic_old.sort(reverse=True)
    semantic_db.sort(reverse=True)

    cross: list[tuple[float, str, str]] = []
    for position, item in enumerate(new):
        if len(item["_bigrams"]) < MIN_BIGRAMS:
            continue
        for other in new[position + 1:]:
            if item.get("chapter_key") == other.get("chapter_key"):
                continue
            if len(other["_bigrams"]) < MIN_BIGRAMS:
                continue
            score = similarity(item, other)
            if score >= LEXICAL_THRESHOLD:
                cross.append((score, hit_label(item), hit_label(other)))
    cross.sort(reverse=True)

    lines += [
        "## Lexical near-duplicates (manual review)",
        "",
        f"Digits are retained. Token and bigram Jaccard are averaged; the combined score",
        f"must reach {LEXICAL_THRESHOLD:.2f} with at least {MIN_BIGRAMS} bigrams.",
        "",
        f"- Against Sets 1+2: {len(lexical_old)}",
        f"- Against the database: {len(lexical_db)}",
        f"- Cross-chapter within Set 3: {len(cross)}",
        "",
        "## Semantic near-duplicates (manual review)",
        "",
        f"A shared domain signature plus a number-masked string similarity of at least",
        f"{SEMANTIC_THRESHOLD:.2f} is listed for human inspection; these are not automatic failures.",
        "",
        f"- Against Sets 1+2: {len(semantic_old)}",
        f"- Against the database: {len(semantic_db)}",
        "",
    ]
    for title, hits in (
        ("Sets 1+2 lexical", lexical_old),
        ("Database lexical", lexical_db),
        ("Cross-chapter lexical", cross),
        ("Sets 1+2 semantic", semantic_old),
        ("Database semantic", semantic_db),
    ):
        if hits:
            lines += [f"### {title}", ""]
            for score, left, right in hits[:30]:
                lines.append(f"- {score:.3f}: {left} / {right}")
            lines.append("")

    if lexical_old:
        problems.append("lexical near-duplicate against Sets 1+2")
    if lexical_db:
        problems.append("lexical near-duplicate against the database")
    if cross:
        problems.append("cross-chapter lexical near-duplicate")

    lines += [
        "## Result",
        "",
        f"- New questions: {len(new)}",
        f"- Prior-batch questions: {len(old)}",
        f"- Database questions: {len(db)}",
        f"- Hard problems: {len(problems)}",
        f"- Semantic flags requiring review: {len(semantic_old) + len(semantic_db)}",
        "",
    ]
    if problems:
        lines += ["### Problems", ""] + [f"- {problem}" for problem in problems] + [""]

    os.makedirs(REPORTS, exist_ok=True)
    path = os.path.join(REPORTS, "banking_maths_set3_dedup_report.md")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))
    print(f"wrote {path}")
    print(f"new {len(new)}, old {len(old)}, db {len(db)}")
    print(f"exact dupes {len(exact_dupes)}, normalized dupes {len(norm_dupes)}")
    print(f"lexical old {len(lexical_old)}, db {len(lexical_db)}, cross {len(cross)}")
    print(f"semantic old {len(semantic_old)}, db {len(semantic_db)}")
    print(f"problems {len(problems)}")
    for problem in problems:
        print(" -", problem)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
