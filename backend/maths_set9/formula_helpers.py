# -*- coding: utf-8 -*-
"""Formatting helpers for the independent Set 9 formula sheets.

These helpers are intentionally separate from the chapter builders so the
verifier can recompute every answer without importing builder logic.
"""

from __future__ import annotations

import math
import re
from fractions import Fraction


def F(a, b=1):
    return Fraction(a) if b == 1 else Fraction(a, b)


def fmt(value):
    if isinstance(value, Fraction):
        if value.denominator == 1:
            return str(value.numerator)
        return f"{value.numerator}/{value.denominator}"
    if isinstance(value, float):
        if abs(value - round(value)) < 1e-9:
            return str(int(round(value)))
        return f"{value:.4f}".rstrip("0").rstrip(".")
    return str(value)


def dec(value, places=2):
    text = f"{float(value):.{places}f}"
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def pct(value):
    return dec(value) + "%"


def money(value):
    return "₹" + fmt(value)


def ratio(a, b):
    x, y = F(a), F(b)
    scale = math.lcm(x.denominator, y.denominator)
    first = x.numerator * (scale // x.denominator)
    second = y.numerator * (scale // y.denominator)
    divisor = math.gcd(abs(first), abs(second)) or 1
    return f"{first // divisor}:{second // divisor}"


_EVAL_GLOBALS = {
    "__builtins__": {},
    "F": F,
    "C": math.comb,
    "min": min,
    "max": max,
    "abs": abs,
    "ratio": ratio,
    "fact": math.factorial,
    "P": math.perm,
}


def value(value):
    if isinstance(value, str) and "/" in value:
        num, den = value.split("/", 1)
        return F(int(num), int(den))
    if isinstance(value, int):
        return value
    result = F(value)
    return int(result) if result.denominator == 1 else result


def ratio(a, b):
    x, y = value(a), value(b)
    scale = math.lcm(x.denominator, y.denominator)
    first = x.numerator * (scale // x.denominator)
    second = y.numerator * (scale // y.denominator)
    divisor = math.gcd(abs(first), abs(second)) or 1
    return f"{first // divisor}:{second // divisor}"


def calc(d: dict) -> str:
    """Independent recomputation of a Set 9 answer from exact inputs."""
    env = {k: value(v) for k, v in d.items() if k not in {"expr", "unit", "family", "variant"}}
    result = eval(d["expr"], _EVAL_GLOBALS, env)  # noqa: S307 - local authored expressions only
    return fmt(result) + str(d.get("unit") or "")
