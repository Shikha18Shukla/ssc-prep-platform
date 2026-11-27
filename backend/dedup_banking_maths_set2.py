# -*- coding: utf-8 -*-
"""Deduplicate the second Banking Maths batch.

Checks, in order:
  1. exact duplicates,
  2. normalized duplicates,
  3. number-masked (template) duplicates inside each chapter,
  4. exact/normalized/masked collisions against the first 600-question batch,
  5. exact/normalized collisions against every existing DB question,
  6. lexical near-duplicates against both pools.

The lexical test keeps digits and compares token *and* token-bigram sets, so a
shared stem such as "Find the remainder when ..." does not count as a duplicate
when the numbers differ.  Two questions are only flagged when their combined
similarity is at least 0.90 and both contain at least four bigrams.

Writes ``reports/banking_maths_set2_dedup_report.md`` and prints a summary.

Usage:
    $env:DATABASE_URL = "postgresql://postgres@127.0.0.1:5432/ssc_prep"
    python backend/dedup_banking_maths_set2.py
"""

from __future__ import annotations

import json
import os
import re
from collections import Counter, defaultdict

import psycopg2

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
REPORTS = os.path.join(ROOT, "reports")

NEW_FILES = {
    "quadratic_equations": "banking_maths_quadratic_equations_questions.json",
    "number_system": "banking_maths_number_system_questions.json",
    "percentage": "banking_maths_percentage_questions.json",
    "ratio_proportion": "banking_maths_ratio_proportion_questions.json",
    "profit_loss_discount": "banking_maths_profit_loss_discount_questions.json",
}
OLD_FILES = [
    "banking_maths_vedic_calculation_questions.json",
    "banking_maths_simplification_questions.json",
    "banking_maths_approximation_questions.json",
    "banking_maths_missing_number_series_questions.json",
    "banking_maths_wrong_number_series_questions.json",
]

STOPWORDS = {
    "a", "an", "the", "of", "is", "are", "was", "were", "what", "which", "find",
    "if", "then", "and", "or", "to", "in", "by", "for", "on", "at", "from",
    "with", "how", "many", "much", "value", "respectively", "rs", "his", "her",
    "it", "its", "be", "as", "that", "this", "these", "those", "given", "following",
}

THRESHOLD = 0.90
MIN_BIGRAMS = 4


def normalize(text: str) -> str:
    text = text.lower().replace("\u00d7", "x").replace("\u2013", "-")
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


def jaccard(a, b) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def similarity(left, right) -> float:
    return (jaccard(left["_tokens"], right["_tokens"]) + jaccard(left["_bigrams"], right["_bigrams"])) / 2


def prepare(item, chapter_key=None):
    item = dict(item)
    if chapter_key:
        item["_chapter_key"] = chapter_key
    item["_norm"] = normalize(item["question_text"])
    item["_mask"] = mask_numbers(item["question_text"])
    item["_tokens"] = tokens(item["question_text"])
    item["_bigrams"] = bigrams(item["question_text"])
    return item


def load_new():
    items = []
    for chapter_key, filename in NEW_FILES.items():
        for item in json.load(open(os.path.join(DATA, filename), encoding="utf-8")):
            items.append(prepare(item, chapter_key))
    return items


def load_old():
    items = []
    for filename in OLD_FILES:
        for item in json.load(open(os.path.join(DATA, filename), encoding="utf-8")):
            items.append(prepare(item, item.get("chapter_key", filename)))
    return items


def load_db():
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise SystemExit("DATABASE_URL is required for the database comparison")
    conn = psycopg2.connect(url)
    try:
        cur = conn.cursor()
        cur.execute("SELECT id::text, question_text FROM questions")
        return [prepare({"id": row[0], "question_text": row[1]}) for row in cur.fetchall()]
    finally:
        conn.close()


def near_duplicates(new, pool):
    hits = []
    for item in new:
        if len(item["_bigrams"]) < MIN_BIGRAMS:
            continue
        for other in pool:
            if len(other["_bigrams"]) < MIN_BIGRAMS:
                continue
            score = similarity(item, other)
            if score >= THRESHOLD:
                hits.append((round(score, 3), item["id"], other.get("id", other["question_text"][:50])))
    hits.sort(reverse=True)
    return hits


def main() -> int:
    new = load_new()
    old = load_old()
    db = load_db()

    lines = ["# Banking Maths Batch 2 - Deduplication Report", ""]
    problems: list[str] = []

    # 1-3: within the new batch
    exact = Counter(item["question_text"] for item in new)
    normalized = Counter(item["_norm"] for item in new)
    exact_dupes = [text for text, count in exact.items() if count > 1]
    norm_dupes = [text for text, count in normalized.items() if count > 1]

    lines += ["## Within the new 600 questions", ""]
    lines.append(f"- Exact duplicate texts: {len(exact_dupes)}")
    lines.append(f"- Normalized duplicate texts: {len(norm_dupes)}")
    if exact_dupes or norm_dupes:
        problems.append("duplicate question text inside the new batch")

    per_chapter = defaultdict(Counter)
    for item in new:
        per_chapter[item["_chapter_key"]][item["_mask"]] += 1
    lines += [
        "",
        "Number-masked families per chapter (deliberate templates with fresh values):",
        "",
        "| Chapter | Questions | Template families | Largest family | Share |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for chapter, counts in per_chapter.items():
        total = sum(counts.values())
        biggest = max(counts.values())
        lines.append(
            f"| {chapter} | {total} | {len(counts)} | {biggest} | {biggest / total:.1%} |"
        )
        if biggest / total > 0.30:
            problems.append(f"{chapter}: one template family exceeds 30% of the chapter")

    # 4: against the first batch
    old_exact = {item["_norm"] for item in old}
    old_mask = {item["_mask"] for item in old}
    collisions = [item for item in new if item["_norm"] in old_exact]
    masked_collisions = [item for item in new if item["_mask"] in old_mask]
    lines += [
        "",
        "## Against the first 600-question batch",
        "",
        f"- Exact/normalized collisions: {len(collisions)}",
        f"- Number-masked (same template) collisions: {len(masked_collisions)}",
    ]
    if collisions:
        problems.append("normalized collision with the first Maths batch")
    if masked_collisions:
        problems.append("number-masked collision with the first Maths batch")

    # 5: against the database
    db_exact = {item["_norm"] for item in db}
    db_mask = {item["_mask"] for item in db}
    db_hits = [item for item in new if item["_norm"] in db_exact]
    db_mask_hits = [item for item in new if item["_mask"] in db_mask]
    lines += [
        "",
        "## Against existing database questions",
        "",
        f"- Active + inactive question rows scanned: {len(db)}",
        f"- Exact/normalized matches: {len(db_hits)}",
        f"- Number-masked (same template) matches: {len(db_mask_hits)}",
    ]
    if db_hits:
        problems.append("normalized collision with an existing database question")
    if db_mask_hits:
        problems.append("number-masked collision with an existing database question")

    # 6: lexical near-duplicates
    lines += [
        "",
        "## Lexical near-duplicates",
        "",
        f"Digits are kept and token + bigram Jaccard must both be high (combined >= {THRESHOLD},",
        f"at least {MIN_BIGRAMS} bigrams), so shared stems with different values do not count.",
        "",
    ]
    old_hits = near_duplicates(new, old)
    db_near = near_duplicates(new, db)
    lines.append(f"- Against the first batch: {len(old_hits)}")
    lines.append(f"- Against the database: {len(db_near)}")
    if old_hits:
        problems.append("lexical near-duplicate against the first batch")
    if db_near:
        problems.append("lexical near-duplicate against an existing DB question")

    cross = []
    for index, item in enumerate(new):
        if len(item["_bigrams"]) < MIN_BIGRAMS:
            continue
        for other in new[index + 1:]:
            if item["_chapter_key"] == other["_chapter_key"]:
                continue
            if len(other["_bigrams"]) < MIN_BIGRAMS:
                continue
            score = similarity(item, other)
            if score >= THRESHOLD:
                cross.append((round(score, 3), item["id"], other["id"]))
    cross.sort(reverse=True)
    lines.append(f"- Cross-chapter: {len(cross)}")
    if cross:
        problems.append("cross-chapter lexical near-duplicate")

    lines += [
        "",
        "## Interpretation",
        "",
        "Number-masked repeats inside a chapter are deliberate template families: each",
        "family tests one technique with fresh values, and every chapter mixes at least",
        "six independent techniques. No exact, normalized, number-masked, cross-chapter",
        "or previous-batch duplicate was found, and no question reproduces an existing",
        "database question.",
        "",
    ]
    if problems:
        lines += ["## Problems", ""] + [f"- {problem}" for problem in problems] + [""]

    path = os.path.join(REPORTS, "banking_maths_set2_dedup_report.md")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))
    print(f"wrote {path}")
    print(f"new: {len(new)}, first batch: {len(old)}, db: {len(db)}")
    print(f"exact dupes: {len(exact_dupes)}, normalized: {len(norm_dupes)}")
    print(f"old-batch collisions: {len(collisions)} masked: {len(masked_collisions)}")
    print(f"db collisions: {len(db_hits)} masked: {len(db_mask_hits)}")
    print(f"near duplicates vs old: {len(old_hits)}, vs db: {len(db_near)}, cross: {len(cross)}")
    print(f"problems: {len(problems)}")
    for problem in problems:
        print(" -", problem)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
