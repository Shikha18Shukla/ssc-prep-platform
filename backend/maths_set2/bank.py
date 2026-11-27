# -*- coding: utf-8 -*-
"""Shared question-bank helpers for the second Banking Maths batch.

The helpers mirror ``backend/generate_banking_maths_questions.py`` so the two
batches share one JSON schema and one option-shuffling convention.
"""

from __future__ import annotations

import random
import re
from fractions import Fraction

TARGET_PER_CHAPTER = 120
PART_SIZES = {1: 15, 2: 20, 3: 30, 4: 55}


def fmt(value) -> str:
    """Format an int/Fraction/float for display and for an option string."""
    if isinstance(value, Fraction):
        if value.denominator == 1:
            return str(value.numerator)
        return f"{value.numerator}/{value.denominator}"
    if isinstance(value, float):
        if abs(value - round(value)) < 1e-9:
            return str(int(round(value)))
        return f"{value:.4f}".rstrip("0").rstrip(".")
    return str(value)


def fmt_dec(value: float, places: int = 2) -> str:
    text = f"{value:.{places}f}"
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def fmt_pct(value) -> str:
    """Percentage display with at most two decimals."""
    return fmt_dec(float(value), 2) + "%"


def unique_options(correct: str, distractors: list[str], rng: random.Random):
    """Return four distinct options and the correct letter."""
    correct = str(correct)
    options: list[str] = []
    for candidate in [correct] + [str(d) for d in distractors]:
        if candidate not in options:
            options.append(candidate)
    if len(options) < 4:
        ratio = re.fullmatch(r"(\d+):(\d+)(?::(\d+))?", correct)
        percent = re.fullmatch(r"(-?\d+(?:\.\d+)?)(\s*%.*)", correct)
        if ratio:
            parts = [int(part) for part in ratio.groups() if part is not None]
            step = 1
            while len(options) < 4:
                trial = parts[:]
                trial[0] += step
                text = ":".join(str(part) for part in trial)
                if text not in options:
                    options.append(text)
                step += 1
        elif percent:
            number = float(percent.group(1))
            suffix = percent.group(2)
            step = 1
            while len(options) < 4:
                for candidate in (number + step, number - step):
                    text = fmt_dec(candidate, 2) + suffix
                    if text not in options:
                        options.append(text)
                        break
                step += 1
        else:
            try:
                base = Fraction(correct) if "/" in correct else Fraction(str(correct))
            except (ValueError, ZeroDivisionError) as exc:
                raise ValueError(
                    f"template supplied fewer than four distinct options for {correct!r}"
                ) from exc
            step = Fraction(1)
            while len(options) < 4:
                for candidate in (base + step, base - step):
                    text = fmt(candidate)
                    if text not in options:
                        options.append(text)
                        break
                step += 1
    options = options[:4]
    rng.shuffle(options)
    return options, "ABCD"[options.index(correct)]


class Bank:
    def __init__(self, chapter: str, chapter_key: str, seed: int):
        self.chapter = chapter
        self.chapter_key = chapter_key
        self.rng = random.Random(seed)
        self.items: list[dict] = []
        self.texts: set[str] = set()

    def count(self, part: int | None = None) -> int:
        if part is None:
            return len(self.items)
        return sum(1 for item in self.items if item["part"] == part)

    def add(
        self,
        *,
        part: int,
        difficulty: str,
        text: str,
        correct: str,
        distractors: list[str],
        explanation: str,
        source_name: str,
        source_page: str,
        source_type: str,
        verification_data: dict,
        provenance_note: str | None = None,
    ) -> bool:
        text = " ".join(text.split())
        if text in self.texts:
            return False
        options, letter = unique_options(correct, distractors, self.rng)
        if len(options) != 4 or len(set(options)) != 4:
            raise ValueError(f"bad options for: {text}")
        if not explanation.strip():
            raise ValueError(f"missing explanation for: {text}")
        self.texts.add(text)
        self.items.append(
            {
                "id": f"{self.chapter_key}-{len(self.items) + 1:04d}",
                "chapter": self.chapter,
                "chapter_key": self.chapter_key,
                "part": part,
                "section": f"{self.chapter_key}_part_{part}",
                "question_text": text,
                "options": options,
                "correct_option": letter,
                "correct_answer": options["ABCD".index(letter)],
                "explanation": explanation.strip(),
                "difficulty": difficulty,
                "source_name": source_name,
                "source_url": "",
                "source_page": source_page,
                "source_type": source_type,
                "exam_year": None,
                "verification_status": "VERIFIED",
                "verification_method": (
                    "Independent recomputation in verify_banking_maths_set2_questions.py"
                ),
                "verification_data": verification_data,
                "provenance_note": provenance_note
                or (
                    "Original question written for this bank. Topic scope is aligned "
                    "with the cited source pages; it is not an extracted PDF MCQ and is "
                    "not a previous-year question."
                ),
            }
        )
        return True


def fill(bank: Bank, part: int, difficulty: str, count: int, fn, source_name: str,
         source_page: str, source_type: str = "ORIGINAL_VERIFIED",
         max_tries: int = 6000):
    """Repeatedly call ``fn`` until ``count`` unique questions were added."""
    added = 0
    tries = 0
    while added < count and tries < max_tries:
        tries += 1
        candidate = fn(bank.rng)
        if candidate is None:
            continue
        if bank.add(
            part=part,
            difficulty=difficulty,
            text=candidate["text"],
            correct=candidate["correct"],
            distractors=candidate["distractors"],
            explanation=candidate["explanation"],
            source_name=source_name,
            source_page=source_page,
            source_type=source_type,
            verification_data=candidate["verification_data"],
            provenance_note=candidate.get("provenance_note"),
        ):
            added += 1
    if added < count:
        raise RuntimeError(
            f"{bank.chapter_key} part {part}: wanted {count}, added {added} "
            f"after {tries} tries"
        )
