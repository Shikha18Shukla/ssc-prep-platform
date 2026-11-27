# -*- coding: utf-8 -*-
"""Shared template helpers for the six Set 4 chapter builders."""

from __future__ import annotations

from .bank import fmt

NAMES = (
    "Aarav", "Meera", "Rohan", "Neha", "Kabir", "Priya", "Arjun", "Sneha",
    "Vikram", "Ananya", "Dev", "Isha", "Nikhil", "Riya", "Aditya", "Kavya",
    "Sahil", "Tara", "Manav", "Diya",
)


def pair(variant: int, offset: int = 0) -> tuple[str, str]:
    start = (2 * variant + offset) % len(NAMES)
    return NAMES[start], NAMES[(start + 1) % len(NAMES)]


def third(variant: int, offset: int = 2) -> str:
    return NAMES[(2 * variant + offset) % len(NAMES)]


def ratio_str(a: int, b: int) -> str:
    return f"{a}:{b}"


def q(family, variant, text, answer, distractors, explanation, inputs):
    """Build a candidate spec consumed by Bank.fill()."""
    return {
        "text": " ".join(str(text).split()),
        "correct": fmt(answer),
        "distractors": [fmt(value) for value in distractors],
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
