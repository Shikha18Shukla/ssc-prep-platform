# -*- coding: utf-8 -*-
"""Independently verify the second Banking Maths batch (5 x 120 questions).

This script never trusts ``correct_answer``.  It recomputes every result from
``verification_data``, rebuilds every series/equation/ratio string, checks that
exactly one option is correct, and validates the dataset structure.

Run:
    python backend/verify_banking_maths_set2_questions.py
"""

from __future__ import annotations

import json
import math
import os
import re
import sys
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

FILES = {
    "Quadratic Equations": "banking_maths_quadratic_equations_questions.json",
    "Number System": "banking_maths_number_system_questions.json",
    "Percentage": "banking_maths_percentage_questions.json",
    "Ratio and Proportion": "banking_maths_ratio_proportion_questions.json",
    "Profit, Loss and Discount": "banking_maths_profit_loss_discount_questions.json",
}

PART_SIZES = {1: 15, 2: 20, 3: 30, 4: 55}
NUMERIC = re.compile(r"^-?\d+(?:\.\d+)?$")


def fmt_dec(value: float, places: int = 2) -> str:
    text = f"{value:.{places}f}"
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def quad_str(b: int, c: int) -> str:
    terms = ["x^2"]
    if b:
        sign = "+" if b > 0 else "-"
        terms.append(f"{sign} x" if abs(b) == 1 else f"{sign} {abs(b)}x")
    if c:
        sign = "+" if c > 0 else "-"
        terms.append(f"{sign} {abs(c)}")
    return " ".join(terms) + " = 0"


def ratio_str(a: int, b: int) -> str:
    g = math.gcd(a, b)
    return f"{a // g}:{b // g}"


def triple_str(a: int, b: int, c: int) -> str:
    g = math.gcd(math.gcd(a, b), c)
    return f"{a // g}:{b // g}:{c // g}"


def factorise(n: int) -> dict[int, int]:
    factors: dict[int, int] = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def divisor_count(n: int) -> int:
    total = 1
    for exponent in factorise(n).values():
        total *= exponent + 1
    return total


def divisor_sum(n: int) -> int:
    total = 1
    for prime, exponent in factorise(n).items():
        total *= (prime ** (exponent + 1) - 1) // (prime - 1)
    return total


def trailing_zeros(n: int) -> int:
    total, power = 0, 5
    while power <= n:
        total += n // power
        power *= 5
    return total


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def relation_of(p1, q1, p2, q2) -> str:
    sx, sy = {p1, q1}, {p2, q2}
    if sx == sy:
        return "x = y"
    if max(sx) < min(sy):
        return "x < y"
    if min(sx) > max(sy):
        return "x > y"
    return "Relationship cannot be determined"


def expected_answer(item) -> str:
    data = item["verification_data"]
    op = data["op"]

    # --- Quadratic ---------------------------------------------------------
    if op == "q_compare":
        return relation_of(data["p1"], data["q1"], data["p2"], data["q2"])
    if op == "q_roots":
        p, q, which = data["p"], data["q"], data["which"]
        if which == "larger":
            return str(max(p, q))
        if which == "smaller":
            return str(min(p, q))
        if which == "difference":
            return str(abs(p - q))
    if op == "q_sumprod":
        return str(data["p"] + data["q"] if data["which"] == "sum" else data["p"] * data["q"])
    if op == "q_form":
        return quad_str(-(data["p"] + data["q"]), data["p"] * data["q"])
    if op == "q_nature":
        d = data["b"] ** 2 - 4 * data["c"]
        return (
            "Two distinct real roots"
            if d > 0
            else "Two equal real roots"
            if d == 0
            else "No real roots"
        )
    if op == "q_k":
        p, c = data["p"], data["c"]
        assert (p * p + c) % p == 0
        return str((p * p + c) // p)
    if op == "q_recip":
        k = data["k"]
        return str(k * k - 2 if data["kind"] == "square" else k ** 3 - 3 * k)
    if op == "q_rootfrac":
        value = Fraction(data["p"] + data["q"], data["p"] * data["q"])
        return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    if op == "q_addsq":
        half = data["b"] // 2
        assert data["b"] == 2 * half
        return str(half * half)

    # --- Number System -----------------------------------------------------
    if op == "ns_mod":
        return str(data["a"] % data["b"])
    if op == "ns_unit":
        return str(pow(data["a"], data["b"], 10))
    if op == "ns_gcd":
        return str(math.gcd(*data["nums"]))
    if op == "ns_lcm":
        return str(math.lcm(*data["nums"]))
    if op == "ns_divcount":
        return str(divisor_count(data["n"]))
    if op == "ns_divsum":
        return str(divisor_sum(data["n"]))
    if op == "ns_zeros":
        return str(trailing_zeros(data["n"]))
    if op == "ns_powmod":
        return str(pow(data["a"], data["b"], data["m"]))
    if op == "ns_pick_divisible":
        divisible = [o for o in data["options"] if int(o) % data["divisor"] == 0]
        assert len(divisible) == 1, data
        return divisible[0]
    if op == "ns_missing_digit":
        digits, pos, divisor = data["digits"], data["pos"], data["divisor"]
        solutions = []
        for x in range(10):
            trial = digits[:]
            trial[pos] = x
            if int("".join(str(d) for d in trial)) % divisor == 0:
                solutions.append(x)
        assert len(solutions) == 1, data
        return str(solutions[0])
    if op == "ns_frac_max":
        values = [Fraction(text) for text in data["fractions"]]
        best = max(values)
        label = data["fractions"][values.index(best)]
        return label
    if op == "ns_prime_pick":
        primes = [o for o in data["options"] if is_prime(int(o))]
        assert len(primes) == 1, data
        return primes[0]
    if op == "ns_hcf_lcm":
        return str(data["a"] * data["b"] // data["h"])
    if op == "ns_even_divcount":
        n = data["n"]
        power = 0
        while n % 2 == 0:
            power += 1
            n //= 2
        return str(power * divisor_count(n))
    if op == "ns_exp":
        return str(data["base"] ** (data["e1"] + data["e2"] - data["e3"]))

    # --- Percentage --------------------------------------------------------
    if op == "pct_of":
        value = Fraction(data["p"] * data["n"], 100)
        assert value.denominator == 1
        return str(value.numerator)
    if op == "pct_what":
        return fmt_dec(float(Fraction(data["a"], data["b"]) * 100), 2)
    if op == "pct_fraction":
        return fmt_dec(float(Fraction(data["num"], data["den"]) * 100), 2) + "%"
    if op == "pct_change":
        value = Fraction(data["new"] - data["old"], data["old"]) * 100
        assert value.denominator == 1
        return str(value.numerator)
    if op == "pct_reverse":
        value = Fraction(data["result"] * 100, 100 + data["p"])
        assert value.denominator == 1
        return str(value.numerator)
    if op == "pct_successive":
        net = (
            Fraction(data["p"]) + Fraction(data["q"]) + Fraction(data["p"] * data["q"], 100)
            if data["mode"] == "up_up"
            else Fraction(data["p"]) - Fraction(data["q"]) - Fraction(data["p"] * data["q"], 100)
        )
        if net > 0:
            return fmt_dec(float(net), 2) + "% increase"
        if net < 0:
            return fmt_dec(float(-net), 2) + "% decrease"
        return "No change"
    if op == "pct_more_less":
        return fmt_dec(float(Fraction(100 * data["p"], 100 + data["p"])), 2) + "%"
    if op == "pct_exam":
        value = Fraction(100 * (data["fail"] + data["extra"]), data["p2"] - data["p1"])
        assert value.denominator == 1
        return str(value.numerator)
    if op == "pct_consumption":
        denominator = 100 + data["p"] if data["rise"] else 100 - data["p"]
        return fmt_dec(float(Fraction(100 * data["p"], denominator)), 2) + "%"
    if op == "pct_population":
        value = data["population"] * (100 + data["p"]) // 100 * (100 + data["q"]) // 100
        return str(value)
    if op == "pct_income":
        value = Fraction(data["saving"] * 100, 100 - data["p"])
        assert value.denominator == 1
        return str(value.numerator)

    # --- Ratio and Proportion ---------------------------------------------
    if op == "r_divide":
        total, ratio, index = data["total"], data["ratio"], data["index"]
        value = Fraction(total * ratio[index], sum(ratio))
        assert value.denominator == 1
        return str(value.numerator)
    if op == "r_prop":
        value = Fraction(data["b"] * data["c"], data["a"])
        assert value.denominator == 1
        return str(value.numerator)
    if op == "r_boys":
        value = Fraction(data["total"] * data["a"], data["a"] + data["b"])
        assert value.denominator == 1
        return str(value.numerator)
    if op == "r_share":
        value = Fraction(data["total"] * max(data["a"], data["b"]), data["a"] + data["b"])
        assert value.denominator == 1
        return str(value.numerator)
    if op == "r_combine":
        common = math.lcm(data["b1"], data["b2"])
        return triple_str(
            data["a1"] * (common // data["b1"]),
            common,
            data["c1"] * (common // data["b2"]),
        )
    if op == "r_mean":
        root = math.isqrt(data["a"] * data["b"])
        assert root * root == data["a"] * data["b"]
        return str(root)
    if op == "r_third":
        value = Fraction(data["b"] * data["b"], data["a"])
        assert value.denominator == 1
        return str(value.numerator)
    if op == "r_inverse":
        return ratio_str(data["p"] * data["m"], data["q"] * data["n"])
    if op == "r_ages":
        numerator = data["t"] * (data["c"] - data["d"])
        denominator = data["a"] * data["d"] - data["b"] * data["c"]
        assert denominator != 0 and numerator % denominator == 0, data
        k = numerator // denominator
        return str((data["a"] if data["which"] == "A" else data["b"]) * k)
    if op == "r_income":
        numerator = data["saving"] * (data["d"] - data["c"])
        denominator = data["a"] * data["d"] - data["b"] * data["c"]
        assert denominator != 0 and numerator % denominator == 0, data
        k = numerator // denominator
        return str(data["a"] * k)
    if op == "r_coins":
        unit = data["a"] * 1 + data["b"] * 2 + data["c"] * 5
        assert data["total"] % unit == 0, data
        k = data["total"] // unit
        return str(data["b"] * k)
    if op == "r_mixture":
        a, b, c, d = data["a"], data["b"], data["c"], data["d"]
        return ratio_str(a * (c + d) + c * (a + b), b * (c + d) + d * (a + b))
    if op == "r_partnership":
        unit = data["c1"] * data["t1"] + data["c2"] * data["t2"]
        value = Fraction(data["total"] * data["c1"] * data["t1"], unit)
        assert value.denominator == 1
        return str(value.numerator)

    # --- Profit, Loss and Discount ----------------------------------------
    if op == "pl_profit_pct":
        value = Fraction((data["sp"] - data["cp"]) * 100, data["cp"])
        assert value.denominator == 1
        return str(value.numerator)
    if op == "pl_sp":
        return str(data["cp"] + data["cp"] * data["p"] // 100)
    if op == "pl_cp":
        value = Fraction(data["sp"] * 100, 100 + data["p"])
        assert value.denominator == 1
        return str(value.numerator)
    if op == "pl_discount":
        return str(data["mp"] - data["mp"] * data["d"] // 100)
    if op == "pl_successive":
        net = Fraction(data["d1"]) + Fraction(data["d2"]) - Fraction(data["d1"] * data["d2"], 100)
        return fmt_dec(float(net), 2) + "%"
    if op == "pl_mp_profit":
        profit = Fraction((100 + data["markup"]) * (100 - data["discount"]), 100) - 100
        return fmt_dec(float(profit), 2)
    if op == "pl_mp_value":
        return str(data["cp"] * (100 + data["markup"]) // 100)
    if op == "pl_false_weight":
        gain = Fraction((data["true_w"] - data["false_w"]) * 100, data["false_w"])
        return fmt_dec(float(gain), 2) + "%"
    if op == "pl_two":
        return fmt_dec(float(Fraction(data["p"] * data["p"], 100)), 2) + "%"
    if op == "pl_profit_on_sp":
        return fmt_dec(float(Fraction(100 * data["p"], 100 - data["p"])), 2) + "%"
    if op == "pl_mp_ratio":
        sp_part = Fraction(data["cp_part"] * (100 + data["profit"]), 100)
        discount = (Fraction(data["mp_part"]) - sp_part) / data["mp_part"] * 100
        return fmt_dec(float(discount), 2) + "%"
    if op == "pl_break_even":
        cp = Fraction(data["sp"] * 100, 100 - data["loss"])
        assert cp.denominator == 1
        value = cp * (100 + data["gain"]) / 100
        assert value.denominator == 1
        return str(value.numerator)

    raise AssertionError(f"unknown op {op}")


def check_item(item) -> list[str]:
    errors: list[str] = []
    options = item.get("options", [])
    if len(options) != 4 or len(set(options)) != 4:
        errors.append("options are not four unique values")
    if item.get("correct_option") not in "ABCD":
        errors.append("correct_option is not A-D")
    elif options["ABCD".index(item["correct_option"])] != item.get("correct_answer"):
        errors.append("correct_option does not point at correct_answer")
    if not item.get("explanation", "").strip():
        errors.append("empty explanation")
    if item.get("difficulty") not in {"EASY", "MEDIUM", "HARD"}:
        errors.append("bad difficulty")
    if item.get("part") not in {1, 2, 3, 4}:
        errors.append("bad part")
    if item.get("verification_status") != "VERIFIED":
        errors.append("not marked VERIFIED")
    if item.get("is_pyq") or item.get("pyq_year") is not None:
        errors.append("question is flagged as PYQ")
    if item.get("source_type") not in {"ORIGINAL_VERIFIED", "PDF_DERIVED_VERIFIED"}:
        errors.append("bad source_type")

    try:
        expected = expected_answer(item)
    except AssertionError as exc:
        errors.append(f"verification assertion failed: {exc}")
        return errors

    if expected != item.get("correct_answer"):
        errors.append(
            f"answer mismatch: computed {expected!r}, stored {item.get('correct_answer')!r}"
        )
    matches = [option for option in options if option == expected]
    if len(matches) != 1:
        errors.append(f"expected exactly one option {expected!r}, found {len(matches)}")

    # When every option is a plain number, no other option may be numerically equal.
    if all(NUMERIC.match(str(option)) for option in options) and NUMERIC.match(expected):
        target = float(expected)
        equal = [o for o in options if abs(float(o) - target) < 1e-9]
        if len(equal) != 1:
            errors.append(f"more than one numerically equal option: {equal}")
    return errors


def main() -> int:
    failures: list[str] = []
    all_texts: dict[str, str] = {}
    all_ids: set[str] = set()
    total = 0
    for chapter, filename in FILES.items():
        path = os.path.join(DATA, filename)
        if not os.path.exists(path):
            failures.append(f"missing dataset {filename}")
            continue
        items = json.load(open(path, encoding="utf-8"))
        if len(items) != 120:
            failures.append(f"{filename}: {len(items)} questions, expected 120")
        for part, size in PART_SIZES.items():
            count = sum(1 for item in items if item["part"] == part)
            if count != size:
                failures.append(f"{filename}: part {part} has {count}, expected {size}")
        chapter_errors = 0
        for item in items:
            total += 1
            for error in check_item(item):
                chapter_errors += 1
                failures.append(f"{filename}/{item.get('id')}: {error}")
            text = " ".join(item["question_text"].split()).lower()
            if text in all_texts:
                failures.append(
                    f"duplicate text: {item.get('id')} and {all_texts[text]}"
                )
            all_texts[text] = item.get("id")
            if item.get("id") in all_ids:
                failures.append(f"duplicate id {item.get('id')}")
            all_ids.add(item.get("id"))
        print(f"{chapter}: {len(items)} questions checked, {chapter_errors} error(s)")

    print(f"TOTAL: {total} questions, {len(failures)} failure(s)")
    for failure in failures[:60]:
        print(" -", failure)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
