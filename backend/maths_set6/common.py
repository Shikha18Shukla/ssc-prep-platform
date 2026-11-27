# -*- coding: utf-8 -*-
"""Shared template helpers for the six Set 6 chapter builders."""

from __future__ import annotations

import math
import re
from fractions import Fraction

from .bank import fmt

NAMES = (
    "Aarav", "Meera", "Rohan", "Neha", "Kabir", "Priya", "Arjun", "Sneha",
    "Vikram", "Ananya", "Dev", "Isha", "Nikhil", "Riya", "Aditya", "Kavya",
    "Sahil", "Tara", "Manav", "Diya", "Kunal", "Pooja", "Rehan", "Sania",
)


def pair(variant: int, offset: int = 0) -> tuple[str, str]:
    start = (2 * variant + offset) % len(NAMES)
    return NAMES[start], NAMES[(start + 1) % len(NAMES)]


def third(variant: int, offset: int = 2) -> str:
    return NAMES[(2 * variant + offset) % len(NAMES)]


def ratio_str(a: int, b: int) -> str:
    return f"{a}:{b}"


def ratio(a, b) -> str:
    x, y = F(a), F(b)
    scale = math.lcm(x.denominator, y.denominator)
    first = x.numerator * (scale // x.denominator)
    second = y.numerator * (scale // y.denominator)
    divisor = math.gcd(abs(first), abs(second)) or 1
    return f"{first // divisor}:{second // divisor}"


def F(a, b=1):
    return Fraction(a, b)


def dec(value, places: int = 2) -> str:
    text = f"{float(value):.{places}f}"
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def pct(value) -> str:
    return dec(value) + "%"


def money(value) -> str:
    return "₹" + fmt(value)


def near_num(value, step=1) -> list[str]:
    value = F(value)
    return [fmt(value + step), fmt(value - step), fmt(value * 2)]


def near_pct(value, step=5) -> list[str]:
    value = F(value)
    return [pct(value + step), pct(value - step), pct(value / 2)]


def near_money(value, step=50) -> list[str]:
    value = F(value)
    return [money(value + step), money(value - step), money(value * 2)]


def table(rows) -> str:
    return "; ".join(f"{name}={value}" for name, value in rows)


def data(rows) -> str:
    """Inline DI data block that makes every question self-contained."""
    return "Data: " + table(rows) + "."


def _four_options(correct: str, distractors: list[str]) -> tuple[str, list[str]]:
    """Return the correct answer and exactly three distinct, type-matched distractors."""
    options: list[str] = []
    for value in [correct] + [fmt(item) for item in distractors]:
        text = fmt(value)
        if text not in options:
            options.append(text)
    step = 1
    while len(options) < 4:
        added = False
        ratio = re.fullmatch(r"(-?\d+):(\d+)", correct)
        percent = re.fullmatch(r"(-?\d+(?:\.\d+)?)(.*%)", correct)
        numeric = re.fullmatch(r"(₹\s*)?(-?\d+(?:/\d+|\.\d+)?)(.*)", correct)
        if ratio:
            first, second = int(ratio.group(1)), int(ratio.group(2))
            for delta in (step, -step):
                text = f"{first + delta}:{second}"
                if text not in options:
                    options.append(text)
                    added = True
                    break
        elif percent:
            base = float(percent.group(1))
            suffix = percent.group(2)
            for delta in (step, -step):
                text = fmt(round(base + delta, 4)) + suffix
                if text not in options:
                    options.append(text)
                    added = True
                    break
        elif numeric:
            symbol = numeric.group(1) or ""
            suffix = numeric.group(3) or ""
            try:
                base = Fraction(numeric.group(2))
            except (ValueError, ZeroDivisionError):
                base = None
            if base is not None:
                for delta in (step, -step):
                    text = symbol + fmt(base + delta) + suffix
                    if text not in options:
                        options.append(text)
                        added = True
                        break
        if not added:
            for text in (
                "None of these", "Cannot be determined", "All of these",
                "Both A and B", "Data inadequate",
            ):
                if text not in options:
                    options.append(text)
                    break
        step += 1
    return options[0], options[1:4]


def q(family, variant, text, answer, distractors, explanation, inputs):
    """Build a candidate spec consumed by Bank.fill()."""
    correct, unique_distractors = _four_options(fmt(answer), list(distractors))
    return {
        "text": " ".join(str(text).split()),
        "correct": correct,
        "distractors": unique_distractors,
        "explanation": " ".join(str(explanation).split()),
        "verification_data": {
            "family": family,
            "variant": variant,
            "inputs": inputs,
        },
    }


def build_specs(FAMILIES):
    """Return the standard 3/4/6/11 family distribution of 120 specs."""
    specs = []
    for index, fn in enumerate(FAMILIES):
        if index < 3:
            part, difficulty = 1, "EASY"
        elif index < 7:
            part, difficulty = 2, "EASY"
        elif index < 13:
            part, difficulty = 3, "MEDIUM"
        else:
            part, difficulty = 4, "MEDIUM" if index < 19 else "HARD"
        for variant in range(5):
            specs.append((part, difficulty, lambda r, f=fn, v=variant: f(r, v), (index % 4) + 1))
    return specs
