# -*- coding: utf-8 -*-
"""Quadratic Equations - 120 verified questions for the second Maths batch."""

from __future__ import annotations

from fractions import Fraction

from .bank import Bank, fill

SOURCE = "Guidely Topic-Wise Bundle 2022 - Quadratic Equation Sets 1-6 (local PDF)"
PAGES = {
    1: "Quadratic Equation Set-1, pp. 2-20",
    2: "Quadratic Equation Set-2, pp. 2-20",
    3: "Quadratic Equation Set-3, pp. 2-20",
    4: "Quadratic Equation Set-4, pp. 2-20",
    5: "Quadratic Equation Set-5, pp. 2-20",
    6: "Quadratic Equation Set-6, pp. 2-20",
}
RELATIONS = ["x < y", "x > y", "x = y", "Relationship cannot be determined"]


def quad_str(b: int, c: int, var: str = "x") -> str:
    terms = [f"{var}^2"]
    if b:
        sign = "+" if b > 0 else "-"
        terms.append(f"{sign} {var}" if abs(b) == 1 else f"{sign} {abs(b)}{var}")
    if c:
        sign = "+" if c > 0 else "-"
        terms.append(f"{sign} {abs(c)}")
    return " ".join(terms) + " = 0"


def near_ints(correct: int, rng, spread: int = 4) -> list[str]:
    values: list[str] = []
    while len(values) < 3:
        delta = rng.choice([-1, 1]) * rng.randint(1, spread)
        text = str(correct + delta)
        if text != str(correct) and text not in values:
            values.append(text)
    return values


def relation_of(p1: int, q1: int, p2: int, q2: int) -> str:
    sx, sy = {p1, q1}, {p2, q2}
    if sx == sy:
        return "x = y"
    if max(sx) < min(sy):
        return "x < y"
    if min(sx) > max(sy):
        return "x > y"
    return "Relationship cannot be determined"


def q_compare(rng, hard: bool = False):
    p1 = rng.randint(2, 19)
    q1 = rng.randint(2, 19)
    while q1 == p1:
        q1 = rng.randint(2, 19)
    mode = rng.choice(["lt", "gt", "eq", "und"]) if hard else rng.choice(["lt", "gt"])
    if mode == "eq":
        p2, q2 = p1, q1
    elif mode == "lt":
        base = max(p1, q1) + rng.randint(1, 9)
        p2 = base + rng.randint(0, 4)
        q2 = p2 + rng.randint(1, 7)
    elif mode == "gt":
        base = min(p1, q1) - rng.randint(1, 9)
        p2 = base - rng.randint(0, 4)
        q2 = p2 - rng.randint(1, 7)
    else:
        p2, q2 = p1, q1 + rng.randint(1, 6)

    eq1 = quad_str(-(p1 + q1), p1 * q1)
    eq2 = quad_str(-(p2 + q2), p2 * q2, "y")
    answer = relation_of(p1, q1, p2, q2)
    roots_x = sorted([p1, q1])
    roots_y = sorted([p2, q2])
    if answer == "Relationship cannot be determined":
        reason = (
            f"the two root sets overlap, so neither variable is always larger, "
            f"smaller or equal"
        )
    elif answer == "x = y":
        reason = "both equations have exactly the same pair of roots"
    else:
        reason = (
            f"every root on the x side is {'less' if answer == 'x < y' else 'greater'} "
            f"than every root on the y side"
        )
    return {
        "text": (
            f"Solve the two equations and determine the relation between x and y: "
            f"I) {eq1}; II) {eq2}."
        ),
        "correct": answer,
        "distractors": [r for r in RELATIONS if r != answer],
        "explanation": (
            f"I gives x = {roots_x[0]} or {roots_x[1]}, and II gives y = "
            f"{roots_y[0]} or {roots_y[1]}. Here {reason}, so the answer is "
            f"'{answer}'."
        ),
        "verification_data": {
            "op": "q_compare",
            "p1": p1,
            "q1": q1,
            "p2": p2,
            "q2": q2,
        },
    }


def q_roots(rng, which: str = "larger"):
    p = rng.randint(1, 16)
    q = rng.randint(1, 16)
    while q == p:
        q = rng.randint(1, 16)
    b, c = -(p + q), p * q
    if which == "larger":
        answer = max(p, q)
        text = f"Solve {quad_str(b, c)}. What is the larger root?"
        why = f"The roots are {min(p, q)} and {max(p, q)}, so the larger root is {answer}."
    elif which == "smaller":
        answer = min(p, q)
        text = f"Solve {quad_str(b, c)}. What is the smaller root?"
        why = f"The roots are {min(p, q)} and {max(p, q)}, so the smaller root is {answer}."
    elif which == "difference":
        answer = abs(p - q)
        text = f"Solve {quad_str(b, c)}. What is the positive difference between its roots?"
        why = (
            f"The roots are {min(p, q)} and {max(p, q)}; their difference is "
            f"{max(p, q)} - {min(p, q)} = {answer}."
        )
    else:
        raise ValueError(which)
    return {
        "text": text,
        "correct": str(answer),
        "distractors": near_ints(answer, rng),
        "explanation": why,
        "verification_data": {"op": "q_roots", "p": p, "q": q, "which": which},
    }


def q_sumprod(rng, which: str = "sum"):
    p = rng.randint(2, 18)
    q = rng.randint(2, 18)
    while q == p:
        q = rng.randint(2, 18)
    b, c = -(p + q), p * q
    answer = p + q if which == "sum" else p * q
    text = (
        f"For the equation {quad_str(b, c)}, find the sum of its roots."
        if which == "sum"
        else f"For the equation {quad_str(b, c)}, find the product of its roots."
    )
    why = (
        f"Write the equation as x^2 - (sum)x + (product) = 0. The roots are "
        f"{min(p, q)} and {max(p, q)}, so the {'sum' if which == 'sum' else 'product'} "
        f"is {answer}."
    )
    return {
        "text": text,
        "correct": str(answer),
        "distractors": near_ints(answer, rng, 5),
        "explanation": why,
        "verification_data": {"op": "q_sumprod", "p": p, "q": q, "which": which},
    }


def q_form(rng):
    p = rng.randint(1, 12)
    q = rng.randint(1, 12)
    while q == p:
        q = rng.randint(1, 12)
    b, c = -(p + q), p * q
    correct = quad_str(b, c)
    distractors = [
        quad_str(b, -c),
        quad_str(-b, c),
        quad_str(-b, -c),
    ]
    return {
        "text": f"Which of the following equations has {p} and {q} as its roots?",
        "correct": correct,
        "distractors": distractors,
        "explanation": (
            f"Sum of roots = {p} + {q} = {p + q} and product = {p} x {q} = {p * q}. "
            f"The equation is x^2 - (sum)x + (product) = 0, that is {correct}."
        ),
        "verification_data": {"op": "q_form", "p": p, "q": q},
    }


def q_nature(rng):
    kind = rng.choice(["distinct", "equal", "none"])
    if kind == "equal":
        r = rng.randint(1, 12)
        b, c = -2 * r, r * r
    elif kind == "distinct":
        p = rng.randint(1, 10)
        q = p + rng.randint(1, 8)
        b, c = -(p + q), p * q
    else:
        b = rng.choice([1, 2, 3, 4, 5])
        c = (b * b) // 4 + rng.randint(1, 9)
    d = b * b - 4 * c
    if d > 0:
        answer = "Two distinct real roots"
    elif d == 0:
        answer = "Two equal real roots"
    else:
        answer = "No real roots"
    options = [
        "Two distinct real roots",
        "Two equal real roots",
        "No real roots",
        "Exactly one real root",
    ]
    return {
        "text": f"Determine the nature of the roots of {quad_str(b, c)}.",
        "correct": answer,
        "distractors": [o for o in options if o != answer],
        "explanation": (
            f"Discriminant D = b^2 - 4ac = ({b})^2 - 4(1)({c}) = {d}. "
            + (
                "Since D > 0, the roots are real and distinct."
                if d > 0
                else "Since D = 0, the roots are real and equal."
                if d == 0
                else "Since D < 0, the equation has no real roots."
            )
        ),
        "verification_data": {"op": "q_nature", "b": b, "c": c},
    }


def q_k(rng):
    p = rng.randint(2, 12)
    m = rng.randint(1, 12)
    c = p * m
    k = p + m
    return {
        "text": f"If x = {p} is a root of x^2 - kx + {c} = 0, find the value of k.",
        "correct": str(k),
        "distractors": near_ints(k, rng),
        "explanation": (
            f"Substitute x = {p}: {p}^2 - k({p}) + {c} = 0, so {p * p} + {c} = "
            f"{p}k and k = {p * p + c}/{p} = {k}."
        ),
        "verification_data": {"op": "q_k", "p": p, "c": c},
    }


def q_recip(rng, kind: str = "square"):
    k = rng.randint(3, 14)
    if kind == "square":
        answer = k * k - 2
        text = f"If x + 1/x = {k}, find the value of x^2 + 1/x^2."
        why = f"(x + 1/x)^2 = x^2 + 1/x^2 + 2, so x^2 + 1/x^2 = {k}^2 - 2 = {answer}."
    else:
        answer = k ** 3 - 3 * k
        text = f"If x + 1/x = {k}, find the value of x^3 + 1/x^3."
        why = (
            f"x^3 + 1/x^3 = (x + 1/x)^3 - 3(x + 1/x) = {k}^3 - 3 x {k} = {answer}."
        )
    return {
        "text": text,
        "correct": str(answer),
        "distractors": near_ints(answer, rng, 6),
        "explanation": why,
        "verification_data": {"op": "q_recip", "k": k, "kind": kind},
    }


def q_rootfrac(rng):
    p = rng.randint(1, 10)
    q = rng.randint(1, 10)
    while q == p:
        q = rng.randint(1, 10)
    b, c = -(p + q), p * q
    value = Fraction(p + q, p * q)
    answer = str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    d1 = Fraction(p + q, p * q + 1)
    d2 = Fraction(p * q, p + q)
    d3 = Fraction(p + q + 1, p * q)
    distractors = []
    for item in (d1, d2, d3):
        text = str(item.numerator) if item.denominator == 1 else f"{item.numerator}/{item.denominator}"
        if text != answer and text not in distractors:
            distractors.append(text)
    return {
        "text": f"If a and b are the roots of {quad_str(b, c)}, find 1/a + 1/b.",
        "correct": answer,
        "distractors": distractors,
        "explanation": (
            f"The roots are {min(p, q)} and {max(p, q)}. So 1/a + 1/b = "
            f"(a + b)/(ab) = {p + q}/{p * q} = {answer}."
        ),
        "verification_data": {"op": "q_rootfrac", "p": p, "q": q},
    }


def q_addsq(rng):
    half = rng.randint(2, 12)
    b = 2 * half
    answer = half * half
    return {
        "text": f"What must be added to x^2 + {b}x to make it a perfect square?",
        "correct": str(answer),
        "distractors": near_ints(answer, rng, 6),
        "explanation": (
            f"Half of the coefficient of x is {b}/2 = {half}. Adding its square, "
            f"{half}^2 = {answer}, gives (x + {half})^2."
        ),
        "verification_data": {"op": "q_addsq", "b": b},
    }


def build_quadratic() -> Bank:
    bank = Bank("Quadratic Equations", "quadratic_equations", seed=601)
    spec = [
        (1, "EASY", 5, q_compare, 1),
        (1, "EASY", 4, lambda r: q_roots(r, "larger"), 1),
        (1, "EASY", 3, lambda r: q_sumprod(r, "sum"), 2),
        (1, "EASY", 3, q_form, 3),
        (2, "EASY", 4, q_compare, 1),
        (2, "MEDIUM", 4, lambda r: q_roots(r, "larger"), 2),
        (2, "MEDIUM", 4, lambda r: q_sumprod(r, "product"), 2),
        (2, "MEDIUM", 4, q_nature, 4),
        (2, "EASY", 4, q_form, 3),
        (3, "MEDIUM", 6, q_compare, 2),
        (3, "MEDIUM", 6, lambda r: q_roots(r, "difference"), 3),
        (3, "MEDIUM", 6, q_rootfrac, 4),
        (3, "HARD", 6, q_k, 5),
        (3, "MEDIUM", 6, q_addsq, 6),
        (4, "HARD", 12, lambda r: q_compare(r, hard=True), 3),
        (4, "HARD", 10, lambda r: q_recip(r, "square"), 5),
        (4, "HARD", 11, q_rootfrac, 6),
        (4, "HARD", 10, q_k, 6),
        (4, "HARD", 6, q_nature, 5),
        (4, "HARD", 6, q_form, 6),
    ]
    for part, difficulty, count, fn, set_no in spec:
        fill(bank, part, difficulty, count, fn, SOURCE, PAGES[set_no])
    return bank
