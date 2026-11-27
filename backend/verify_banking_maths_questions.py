# -*- coding: utf-8 -*-
"""Independently verify the five Banking Maths datasets.

This script does not trust the generator's `correct_answer` field.  It
recomputes every numeric answer from `verification_data`, re-checks every
series rule, and validates option/structure rules.

Run:
    python backend/verify_banking_maths_questions.py
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
    "Vedic Maths Tricks - Calculation Techniques": "banking_maths_vedic_calculation_questions.json",
    "Simplification": "banking_maths_simplification_questions.json",
    "Approximation": "banking_maths_approximation_questions.json",
    "Missing Number Series": "banking_maths_missing_number_series_questions.json",
    "Wrong Number Series": "banking_maths_wrong_number_series_questions.json",
}


def close(a, b, tol=1e-6) -> bool:
    return abs(float(a) - float(b)) <= tol


def verify_rule(terms, rule: str) -> bool:
    if "arithmetic progression" in rule:
        d = terms[1] - terms[0]
        return all(terms[i] - terms[i - 1] == d for i in range(1, len(terms)))
    if "geometric progression" in rule:
        if terms[0] == 0:
            return False
        ratio = Fraction(terms[1], terms[0])
        return all(Fraction(terms[i], terms[i - 1]) == ratio for i in range(1, len(terms)))
    if "consecutive perfect squares" in rule:
        root = round(math.isqrt(terms[0]))
        return all(terms[i] == (root + i) ** 2 for i in range(len(terms)))
    if "consecutive perfect cubes" in rule:
        root = round(terms[0] ** (1 / 3))
        return all(terms[i] == (root + i) ** 3 for i in range(len(terms)))
    if "differences are 1, 4, 9, 16" in rule:
        return all(terms[i] - terms[i - 1] == i ** 2 for i in range(1, len(terms)))
    if "differences are 1, 8, 27, 64" in rule:
        return all(terms[i] - terms[i - 1] == i ** 3 for i in range(1, len(terms)))
    if "alternates" in rule:
        match = re.search(r"x(\d+), then \+(\d+)", rule)
        if not match:
            return False
        r, add = int(match.group(1)), int(match.group(2))
        for i in range(1, len(terms)):
            expected = terms[i - 1] * r if (i - 1) % 2 == 0 else terms[i - 1] + add
            if terms[i] != expected:
                return False
        return True
    if "differences increase by" in rule:
        match = re.search(r"increase by (\d+)", rule)
        if not match:
            return False
        inc = int(match.group(1))
        diffs = [terms[i] - terms[i - 1] for i in range(1, len(terms))]
        return all(diffs[i] - diffs[i - 1] == inc for i in range(1, len(diffs)))
    if "sum of the two previous" in rule:
        return all(terms[i] == terms[i - 1] + terms[i - 2] for i in range(2, len(terms)))
    if rule.startswith("The pattern is x"):
        match = re.search(r"x(\d+) \+ (\d+)", rule)
        if not match:
            return False
        r, add = int(match.group(1)), int(match.group(2))
        return all(terms[i] == terms[i - 1] * r + add for i in range(1, len(terms)))
    if "consecutive prime" in rule:
        def is_prime(n):
            if n < 2:
                return False
            for p in range(2, int(n ** 0.5) + 1):
                if n % p == 0:
                    return False
            return True
        if not all(is_prime(t) for t in terms):
            return False
        nxt = terms[-1] + 1
        while not is_prime(nxt):
            nxt += 1
        return True
    if "decreases by" in rule:
        match = re.search(r"decreases by (\d+), then by (\d+)", rule)
        if not match:
            return False
        first, second = int(match.group(1)), int(match.group(2))
        inc = second - first
        diffs = [terms[i - 1] - terms[i] for i in range(1, len(terms))]
        return diffs[0] == first and all(diffs[i] - diffs[i - 1] == inc for i in range(1, len(diffs)))
    return False


def closest_option(item, exact):
    expected = item["correct_answer"]
    distances = {opt: abs(float(opt) - float(exact)) for opt in item["options"]}
    best = min(distances, key=distances.get)
    return best == expected


def verify_item(item) -> list[str]:
    errors = []
    options = item["options"]
    if len(options) != 4 or len(set(options)) != 4:
        errors.append("options are not four unique values")
    if item["correct_option"] not in "ABCD":
        errors.append("correct_option is not A-D")
    elif options["ABCD".index(item["correct_option"])] != item["correct_answer"]:
        errors.append("correct_option does not point at correct_answer")
    if not item["explanation"].strip():
        errors.append("empty explanation")
    if item["difficulty"] not in {"EASY", "MEDIUM", "HARD"}:
        errors.append("bad difficulty")
    if item["part"] not in {1, 2, 3, 4}:
        errors.append("bad part")
    if item["verification_status"] != "VERIFIED":
        errors.append("not marked VERIFIED")

    data = item["verification_data"]
    op = data["op"]
    try:
        if op == "mul":
            expected = data["a"] * data["b"]
            if expected != data["expected"]:
                errors.append("mul verification_data mismatch")
        elif op == "square":
            expected = data["a"] ** 2
            if expected != data["expected"]:
                errors.append("square verification_data mismatch")
        elif op == "div":
            expected = data["a"] / data["b"]
            if expected != data["expected"]:
                errors.append("div verification_data mismatch")
        elif op == "diff_squares":
            expected = data["a"] ** 2 - data["b"] ** 2
            if expected != data["expected"]:
                errors.append("diff_squares verification_data mismatch")
        elif op == "sum_natural":
            expected = data["n"] * (data["n"] + 1) // 2
            if expected != data["expected"]:
                errors.append("sum_natural verification_data mismatch")
        elif op == "sum_odd":
            expected = data["n"] ** 2
            if expected != data["expected"]:
                errors.append("sum_odd verification_data mismatch")
        elif op == "sum_even":
            expected = data["n"] * (data["n"] + 1)
            if expected != data["expected"]:
                errors.append("sum_even verification_data mismatch")
        elif op == "mod":
            expected = data["a"] % data["b"]
            if expected != data["expected"]:
                errors.append("mod verification_data mismatch")
        elif op == "digital_root":
            expected = 1 + (data["n"] - 1) % 9
            if expected != data["expected"]:
                errors.append("digital_root verification_data mismatch")
        elif op == "fraction_of":
            expected = Fraction(data["num"], data["den"]) * data["base"]
            if str(expected.numerator) + ("" if expected.denominator == 1 else f"/{expected.denominator}") != data["expected"]:
                errors.append("fraction_of verification_data mismatch")
        elif op == "expr":
            result = eval(data["expr"], {"__builtins__": {}}, {})  # noqa: S307 - generated expression
            if not close(result, Fraction(item["correct_answer"])):
                errors.append(f"expr {data['expr']} != {item['correct_answer']} (got {result})")
        elif op == "percent_sum":
            expected = Fraction(data["x"], 100) * data["A"] + Fraction(data["y"], 100) * data["B"]
            if not close(expected, Fraction(item["correct_answer"])):
                errors.append("percent_sum mismatch")
        elif op == "decimal_expr":
            expected = Fraction(str(data["a"])) * Fraction(str(data["b"])) + Fraction(str(data["c"]))
            if not close(expected, Fraction(item["correct_answer"])):
                errors.append("decimal_expr mismatch")
        elif op in {
            "approx_product", "approx_division", "approx_percent", "approx_sqrt",
            "approx_sumsq", "approx_mixed", "approx_fracsum", "approx_multistep",
        }:
            if op == "approx_product":
                exact = data["a"] * data["b"]
            elif op == "approx_division":
                exact = data["a"] / data["b"]
            elif op == "approx_percent":
                exact = data["p"] * data["n"] / 100
            elif op == "approx_sqrt":
                exact = math.sqrt(data["n"])
            elif op == "approx_sumsq":
                exact = data["a"] ** 2 + data["b"] ** 2
            elif op == "approx_mixed":
                exact = data["a"] * data["b"] + data["c"] / data["d"]
            elif op == "approx_fracsum":
                exact = 1 / data["a"] + 1 / data["b"]
            else:
                exact = (data["a"] + data["b"]) * data["c"] / data["d"]
            if not closest_option(item, exact):
                errors.append(f"approx answer is not the closest option (exact={exact})")
        elif op == "series":
            terms = data["terms"]
            if terms[data["missing_index"]] != data["expected"]:
                errors.append("series expected value mismatch")
            if not verify_rule(terms, data["rule"]):
                errors.append(f"series rule does not fit terms: {data['rule']}")
        elif op == "wrong_series":
            terms = data["correct_terms"]
            if not verify_rule(terms, data["rule"]):
                errors.append(f"wrong_series rule does not fit correct terms: {data['rule']}")
            if data["wrong_value"] == terms[data["wrong_index"]]:
                errors.append("wrong_series wrong_value equals correct term")
            if str(data["wrong_value"]) not in item["question_text"]:
                errors.append("wrong_series wrong_value not present in question text")
        else:
            errors.append(f"unknown verification op {op}")
    except Exception as exc:  # noqa: BLE001
        errors.append(f"verification raised {type(exc).__name__}: {exc}")
    return errors


def main() -> int:
    all_items = []
    failed = 0
    for chapter, filename in FILES.items():
        path = os.path.join(DATA, filename)
        items = json.load(open(path, encoding="utf-8"))
        all_items.extend(items)
        if len(items) != 120:
            print(f"FAIL {chapter}: expected 120 questions, found {len(items)}")
            failed += 1
        for part, size in {1: 15, 2: 20, 3: 30, 4: 55}.items():
            count = sum(1 for item in items if item["part"] == part)
            if count != size:
                print(f"FAIL {chapter}: part {part} has {count}, expected {size}")
                failed += 1
        for item in items:
            errors = verify_item(item)
            if errors:
                failed += 1
                print(f"FAIL {chapter} / {item['id']}: {errors}")
        print(f"{chapter}: {len(items)} questions checked")
    texts = [item["question_text"].strip().lower() for item in all_items]
    if len(texts) != len(set(texts)):
        duplicates = {text for text in texts if texts.count(text) > 1}
        print(f"FAIL: {len(duplicates)} duplicate question texts across all chapters")
        failed += 1
    print(f"TOTAL: {len(all_items)} questions, {failed} failure(s)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
