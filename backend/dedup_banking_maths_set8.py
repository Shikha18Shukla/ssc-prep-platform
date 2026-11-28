# -*- coding: utf-8 -*-
"""Deduplicate the eighth Banking Maths batch.

Screening order:
  1. exact and normalized duplicates inside the new 720 questions,
  2. number-masked template families inside each chapter and across chapters,
  3. exact/normalized/number-masked collisions against Banking Maths Sets 1-7,
  4. exact/normalized/number-masked collisions against existing DB questions other
     than this batch's own 1,440 deterministic rows,
  5. lexical near-duplicates (token + bigram Jaccard, digits retained),
  6. semantic near-duplicates (domain signature + number-masked sequence ratio).

Semantic and lexical hits are listed for manual review. Only exact,
normalized, number-masked and high lexical hits are automatic failures.

Usage (process-only override; never edit .env):
    # DATABASE_URL is supplied through the process environment for an isolated local database
    python backend/dedup_banking_maths_set8.py
"""

from __future__ import annotations

import glob
import json
import os
import re
import uuid
from collections import Counter, defaultdict
from difflib import SequenceMatcher

import psycopg2
from psycopg2.extensions import parse_dsn

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
REPORTS = os.path.join(ROOT, "reports")

NEW_FILES = {
    "time_and_work_mains": "banking_maths_time_and_work_mains_questions.json",
    "time_and_work_data_interpretation": "banking_maths_time_and_work_di_questions.json",
    "time_speed_and_distance_mains": "banking_maths_time_speed_and_distance_mains_questions.json",
    "simple_and_compound_interest_mains": "banking_maths_simple_and_compound_interest_mains_questions.json",
    "simple_and_compound_interest_data_interpretation": "banking_maths_simple_and_compound_interest_di_questions.json",
    "pipe_and_cistern_mains": "banking_maths_pipe_and_cistern_mains_questions.json",
}
EXAMS = ("banking-clerk", "banking-po")

STOPWORDS = {
    "a", "an", "the", "of", "is", "are", "was", "were", "what", "which", "find",
    "if", "then", "and", "or", "to", "in", "by", "for", "on", "at", "from",
    "with", "how", "many", "much", "value", "respectively", "rs", "his", "her",
    "it", "its", "be", "as", "that", "this", "these", "those", "given", "following",
    "will", "would", "can", "needs", "need", "take", "takes", "work", "year",
    "years", "day", "days", "month", "months", "hour", "hours", "question",
    "who", "whom", "asks", "ask", "finds", "need", "together", "all", "one", "two",
}

LEXICAL_THRESHOLD = 0.90
SEMANTIC_THRESHOLD = 0.78
MIN_BIGRAMS = 4
MIN_OVERLAP = 3

DOMAIN_PATTERNS = [
    ("mixture", re.compile(r"mixture|alligation|solution|concentration|alloy|water|milk|dilut|replac|withdraw|evaporat|component|strength")),
    ("ages", re.compile(r"\bage|aged|years old|older|younger|father|mother|child|family|average age|birth|admission|joining")),
    ("partnership", re.compile(r"partnership|capital|invest|profit share|profit-sharing|working partner|commission|salary|joined|withdrew|minimum guarantee|guaranteed")),
    ("time_work", re.compile(r"time and work|worker|men |man |women |woman |efficien|man.day|wage|job|task|pipe|cistern|tank|inlet|outlet|leak")),
    ("speed_distance", re.compile(r"speed|distance|train|platform|boat|stream|current|journey|kmph|km/h|m/s|circular|track|chase|meet")),
    ("interest", re.compile(r"interest|principal|compound|installment|deposit|amount|rate of interest|growth|population")),
    ("data_interpretation", re.compile(r"data:|table|caselet|pie chart|bar graph|bar chart|line graph|percentage distribution|centre|school|seller|item")),
    ("general_percent", re.compile(r"percentage|percent|%|increase|decrease|discount|growth|share|weighted|average|population|literacy|allocation")),
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
    paths = sorted(glob.glob(os.path.join(DATA, "banking_maths_*_questions.json")))
    for path in paths:
        filename = os.path.basename(path)
        if filename in NEW_FILES.values():
            continue
        with open(path, encoding="utf-8") as handle:
            for item in json.load(handle):
                items.append(prepare(item, item.get("id", filename)))
    return items


def stable_id(exam_slug: str, item_id: str) -> str:
    return str(
        uuid.uuid5(
            uuid.NAMESPACE_URL,
            f"https://ssc-prep.local/banking-maths/{exam_slug}/{item_id}",
        )
    )


def planned_ids() -> list[str]:
    ids = set()
    for filename in NEW_FILES.values():
        with open(os.path.join(DATA, filename), encoding="utf-8") as handle:
            for item in json.load(handle):
                for exam_slug in EXAMS:
                    ids.add(stable_id(exam_slug, item["id"]))
    return sorted(ids)


def load_db() -> list[dict]:
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise SystemExit("DATABASE_URL is required for the database comparison")
    dsn = parse_dsn(url)
    if (dsn.get("host") or "").lower() not in {"127.0.0.1", "localhost", "::1"}:
        raise SystemExit("refusing non-local host")
    if dsn.get("dbname") != "ssc_prep":
        raise SystemExit("refusing non-ssc_prep database")
    conn = psycopg2.connect(url)
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id::text, question_text FROM questions WHERE NOT (id = ANY(%s::uuid[]))",
                (planned_ids(),),
            )
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

    lines = ["# Banking Maths Set 8 - Deduplication Report", ""]
    problems: list[str] = []

    if len(new) != 720:
        problems.append(f"expected 720 new questions, found {len(new)}")
    if len(old) != 4800:
        problems.append(f"expected 4800 questions in Sets 1-7, found {len(old)}")

    exact = Counter(item["question_text"] for item in new)
    normalized = Counter(item["_norm"] for item in new)
    exact_dupes = [text for text, count in exact.items() if count > 1]
    norm_dupes = [text for text, count in normalized.items() if count > 1]
    lines += ["## Within the new 720 questions", ""]
    lines.append(f"- Exact duplicate texts: {len(exact_dupes)}")
    lines.append(f"- Normalized duplicate texts: {len(norm_dupes)}")
    if exact_dupes or norm_dupes:
        problems.append("duplicate question text inside the new batch")

    per_chapter = defaultdict(Counter)
    family_counts = Counter()
    mask_owners = defaultdict(set)
    for item in new:
        chapter = item.get("chapter_key", "unknown")
        family = str(item.get("verification_data", {}).get("family", "unknown"))
        per_chapter[chapter][item["_mask"]] += 1
        family_counts[(chapter, family)] += 1
        mask_owners[item["_mask"]].add((chapter, family))
    all_masks = Counter(item["_mask"] for item in new)
    lines += [
        "",
        "Number-masked families per chapter (each family has five fresh numeric",
        "variants, so a repeated template inside one family is expected):",
        "",
        "| Chapter | Questions | Families | Variants / family | Distinct templates | Largest template family |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for chapter, counts in sorted(per_chapter.items()):
        total = sum(counts.values())
        families = {family for (key, family) in family_counts if key == chapter}
        variants = sorted({family_counts[(chapter, family)] for family in families})
        lines.append(
            f"| {chapter} | {total} | {len(families)} | "
            f"{', '.join(str(value) for value in variants)} | {len(counts)} | {max(counts.values())} |"
        )
        if families != {family for (key, family) in family_counts if key == chapter}:
            problems.append(f"{chapter}: family accounting mismatch")
        if variants != [5]:
            problems.append(f"{chapter}: families do not all have five variants")
    shared_masks = {
        mask: owners for mask, owners in mask_owners.items() if len(owners) > 1
    }
    cross_chapter_masks = {
        mask: owners for mask, owners in shared_masks.items()
        if len({chapter for chapter, _ in owners}) > 1
    }
    repeated_all = [mask for mask, count in all_masks.items() if count > 1]
    lines += [
        f"- Repeated number-masked templates inside a single family: {len(repeated_all)} "
        "(expected for the five variants of each family)",
        f"- Templates shared by more than one family: {len(shared_masks)}",
        f"- Cross-chapter repeated number-masked templates: {len(cross_chapter_masks)}",
    ]
    if shared_masks:
        problems.append("number-masked template shared by more than one family")
    if cross_chapter_masks:
        problems.append("cross-chapter repeated number-masked template")

    def collision_section(title: str, pool: list[dict]) -> None:
        exacts = {item["question_text"] for item in pool}
        norms = {item["_norm"] for item in pool}
        masks = {item["_mask"] for item in pool}
        exact_hits = [item for item in new if item["question_text"] in exacts]
        norm_hits = [item for item in new if item["_norm"] in norms]
        mask_hits = [item for item in new if item["_mask"] in masks]
        lines.extend([
            f"## {title}",
            "",
            f"- Questions screened: {len(new)}",
            f"- Pool screened: {len(pool)}",
            f"- Exact matches: {len(exact_hits)}",
            f"- Normalized matches: {len(norm_hits)}",
            f"- Number-masked (template) matches: {len(mask_hits)}",
            "",
        ])
        for item in exact_hits[:20]:
            lines.append(f"- Exact match: {hit_label(item)}")
        for item in norm_hits[:20]:
            lines.append(f"- Normalized match: {hit_label(item)}")
        for item in mask_hits[:20]:
            lines.append(f"- Number-masked match: {hit_label(item)}")
        if exact_hits:
            problems.append(f"exact collision against {title.lower()}")
        if norm_hits:
            problems.append(f"normalized collision against {title.lower()}")
        if mask_hits:
            problems.append(f"number-masked collision against {title.lower()}")

    collision_section("Against Banking Maths Sets 1-7", old)
    collision_section("Against existing database questions", db)

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
        "Digits are retained. Token and bigram Jaccard are averaged; the combined",
        f"score must reach {LEXICAL_THRESHOLD:.2f} with at least {MIN_BIGRAMS} bigrams.",
        "",
        f"- Against Sets 1-7: {len(lexical_old)}",
        f"- Against the database: {len(lexical_db)}",
        f"- Cross-chapter within Set 8: {len(cross)}",
        "",
        "## Semantic near-duplicates (manual review)",
        "",
        "A shared domain signature plus a number-masked string similarity of at least",
        f"{SEMANTIC_THRESHOLD:.2f} is listed for human inspection; these are not automatic failures.",
        "",
        f"- Against Sets 1-7: {len(semantic_old)}",
        f"- Against the database: {len(semantic_db)}",
        "",
    ]
    for title, hits in (
        ("Sets 1-7 lexical", lexical_old),
        ("Database lexical", lexical_db),
        ("Cross-chapter lexical", cross),
        ("Sets 1-7 semantic", semantic_old),
        ("Database semantic", semantic_db),
    ):
        if hits:
            lines += [f"### {title}", ""]
            for score, left, right in hits[:40]:
                lines.append(f"- {score:.3f}: {left} / {right}")
            lines.append("")

    if lexical_old:
        problems.append("lexical near-duplicate against Sets 1-7")
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
        f"- Semantic flags requiring manual review: {len(semantic_old) + len(semantic_db)}",
        "",
    ]
    if problems:
        lines += ["### Problems", ""] + [f"- {problem}" for problem in problems] + [""]

    os.makedirs(REPORTS, exist_ok=True)
    path = os.path.join(REPORTS, "banking_maths_set8_dedup_report.md")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))
    print(f"wrote {path}")
    print(f"new {len(new)}, old {len(old)}, db {len(db)}")
    print(f"exact dupes {len(exact_dupes)}, normalized dupes {len(norm_dupes)}, masked repeated {len(repeated_all)}")
    print(f"lexical old {len(lexical_old)}, db {len(lexical_db)}, cross {len(cross)}")
    print(f"semantic old {len(semantic_old)}, db {len(semantic_db)}")
    print(f"problems {len(problems)}")
    for problem in problems:
        print(" -", problem)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
