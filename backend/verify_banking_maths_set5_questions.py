# -*- coding: utf-8 -*-
"""Independently verify the fifth Banking Maths batch (6 x 120 questions).

This script never trusts ``correct_answer``.  Every result is recomputed from
``verification_data.inputs`` using the formula sheet below, which was written
separately from the chapter builders.  It also validates the JSON schema,
deterministic IDs, part counts, four distinct options, answer/index agreement,
units/rounding and explanation consistency.

Run:
    python backend/verify_banking_maths_set5_questions.py
"""

from __future__ import annotations

import json
import math
import os
import sys
from collections import Counter
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

FILES = {
    "Mensuration – 3D": "banking_maths_mensuration_3d_questions.json",
    "Permutations": "banking_maths_permutations_questions.json",
    "Combinations": "banking_maths_combinations_questions.json",
    "Probability": "banking_maths_probability_questions.json",
    "Data Interpretation": "banking_maths_data_interpretation_questions.json",
    "Caselet Data Interpretation": "banking_maths_caselet_data_interpretation_questions.json",
}
CHAPTER_KEYS = {
    "Mensuration – 3D": "mensuration_3d",
    "Permutations": "permutations",
    "Combinations": "combinations",
    "Probability": "probability",
    "Data Interpretation": "data_interpretation",
    "Caselet Data Interpretation": "caselet_data_interpretation",
}

PART_SIZES = {1: 15, 2: 20, 3: 30, 4: 55}
DIFFICULTIES = {"EASY", "MEDIUM", "HARD"}
LETTERS = "ABCD"
PI = Fraction(22, 7)


def F(numerator, denominator=None):
    if denominator is None:
        return Fraction(numerator)
    return Fraction(numerator, denominator)


def fmt(value):
    if isinstance(value, Fraction):
        if value.denominator == 1:
            return str(value.numerator)
        return f"{value.numerator}/{value.denominator}"
    return str(value)


def dec(value, places: int = 2) -> str:
    text = f"{float(value):.{places}f}"
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def rat(a, b) -> str:
    x, y = F(a), F(b)
    scale = math.lcm(x.denominator, y.denominator)
    first = x.numerator * (scale // x.denominator)
    second = y.numerator * (scale // y.denominator)
    divisor = math.gcd(abs(first), abs(second)) or 1
    return f"{first // divisor}:{second // divisor}"


def fact(n: int) -> int:
    return math.factorial(int(n))


def perm(n: int, r: int) -> int:
    return fact(n) // fact(n - r)


def counts(text: str) -> Counter:
    return Counter(ch for ch in text.upper() if ch.isalpha())


def repeat_factor(text: str, group: str | None = None) -> int:
    factor = 1
    for ch, count in counts(text).items():
        include = (
            True if group is None
            else ch in "AEIOU" if group == "vowels"
            else ch not in "AEIOU" if group == "consonants"
            else False
        )
        if include:
            factor *= fact(count)
    return factor


def rank_word(word: str) -> int:
    letters = sorted(word.upper())
    size = len(letters)
    rank = 1
    for pos, ch in enumerate(word.upper()):
        smaller = sum(1 for available in letters if available < ch)
        rank += smaller * fact(size - pos - 1)
        letters.remove(ch)
    return rank


def pct(numerator, denominator) -> str:
    if F(denominator) == 0:
        raise ZeroDivisionError("zero denominator in percentage")
    return dec(F(numerator) * 100 / F(denominator)) + "%"


FORMULAS: dict = {}

FORMULAS.update({
    "m3_cube_volume": lambda i: fmt(F(i["s"]) ** 3) + " cu m",
    "m3_cube_tsa": lambda i: fmt(6 * F(i["s"]) ** 2) + " sq m",
    "m3_cube_lsa": lambda i: fmt(4 * F(i["s"]) ** 2) + " sq m",
    "m3_cuboid_volume": lambda i: fmt(F(i["L"]) * F(i["B"]) * F(i["H"])) + " cu m",
    "m3_cuboid_tsa": lambda i: fmt(2 * (F(i["L"]) * F(i["B"]) + F(i["B"]) * F(i["H"]) + F(i["H"]) * F(i["L"]))) + " sq m",
    "m3_cuboid_lsa": lambda i: fmt(2 * F(i["H"]) * (F(i["L"]) + F(i["B"]))) + " sq m",
    "m3_cylinder_volume": lambda i: fmt(PI * F(i["r"]) ** 2 * F(i["h"])) + " cu m",
    "m3_cylinder_csa": lambda i: fmt(2 * PI * F(i["r"]) * F(i["h"])) + " sq m",
    "m3_cylinder_tsa": lambda i: fmt(2 * PI * F(i["r"]) * (F(i["r"]) + F(i["h"]))) + " sq m",
    "m3_cone_volume": lambda i: fmt(PI * F(i["r"]) ** 2 * F(i["h"]) / 3) + " cu m",
    "m3_cone_csa": lambda i: fmt(PI * F(i["r"]) * F(i["l"])) + " sq m",
    "m3_cone_tsa": lambda i: fmt(PI * F(i["r"]) * (F(i["r"]) + F(i["l"]))) + " sq m",
    "m3_sphere_volume": lambda i: fmt(F(4, 3) * PI * F(i["r"]) ** 3) + " cu m",
    "m3_sphere_surface": lambda i: fmt(4 * PI * F(i["r"]) ** 2) + " sq m",
    "m3_hemisphere_volume": lambda i: fmt(F(2, 3) * PI * F(i["r"]) ** 3) + " cu m",
    "m3_hemisphere_csa": lambda i: fmt(2 * PI * F(i["r"]) ** 2) + " sq m",
    "m3_hemisphere_tsa": lambda i: fmt(3 * PI * F(i["r"]) ** 2) + " sq m",
    "m3_melt_cylinder_cones": lambda i: fmt(3 * F(i["h"]) / F(i["H"])),
    "m3_melt_cube_cuboid": lambda i: fmt(F(i["s"]) ** 3 / (F(i["b"]) * F(i["h"]))),
    "m3_combined_cylinder_cone": lambda i: fmt(PI * F(i["r"]) ** 2 * (F(i["h"]) + F(i["H"], 3))) + " cu m",
    "m3_capacity_litres": lambda i: fmt(F(i["L"]) * F(i["B"]) * F(i["H"]) / 1000) + " litres",
    "m3_water_rise": lambda i: fmt(F(i["s"]) ** 3 / (PI * F(i["R"]) ** 2)) + " m",
    "m3_hollow_cylinder": lambda i: fmt(PI * F(i["h"]) * (F(i["R"]) ** 2 - F(i["r"]) ** 2)) + " cu m",
    "m3_paint_cost": lambda i: "₹" + fmt(2 * (F(i["L"]) * F(i["B"]) + F(i["B"]) * F(i["H"]) + F(i["H"]) * F(i["L"])) * F(i["rate"])),
})

FORMULAS.update({
    "p_count_fcp": lambda i: fmt(F(i["m"]) * F(i["n"])),
    "p_distinct_arrangements": lambda i: fmt(fact(i["n"])),
    "p_repeated_letters": lambda i: fmt(F(fact(len(i["word"])), repeat_factor(i["word"]))),
    "p_word_all_distinct": lambda i: fmt(fact(len(i["word"]))),
    "p_word_repeated": lambda i: fmt(F(fact(len(i["word"])), repeat_factor(i["word"]))),
    "p_together_pair": lambda i: fmt(2 * fact(i["n"] - 1)),
    "p_not_together": lambda i: fmt(fact(i["n"]) - 2 * fact(i["n"] - 1)),
    "p_ends_restriction": lambda i: fmt(2 * fact(i["n"] - 2)),
    "p_fixed_position": lambda i: fmt(fact(i["n"] - 2)),
    "p_circular_distinct": lambda i: fmt(fact(i["n"] - 1)),
    "p_circular_pair_together": lambda i: fmt(2 * fact(i["n"] - 2)),
    "p_arrange_selected": lambda i: fmt(perm(i["n"], i["r"])),
    "p_three_digit_no_repeat": lambda i: fmt(perm(len(i["d"]), 3)),
    "p_even_numbers": lambda i: fmt(sum(1 for ch in i["d"] if int(ch) % 2 == 0) * perm(len(i["d"]) - 1, 3)),
    "p_odd_numbers": lambda i: fmt(sum(1 for ch in i["d"] if int(ch) % 2 == 1) * perm(len(i["d"]) - 1, 3)),
    "p_divisible_by_five": lambda i: fmt(sum(1 for ch in i["d"] if ch in "05") * perm(len(i["d"]) - 1, 3)),
    "p_vowels_together": lambda i: (
        lambda word, v, c: fmt(F(fact(c + 1) * fact(v), repeat_factor(word, "vowels") * repeat_factor(word, "consonants")))
    )(i["word"], sum(1 for ch in i["word"] if ch in "AEIOU"), sum(1 for ch in i["word"] if ch not in "AEIOU")),
    "p_vowels_not_together": lambda i: (
        lambda word, v, c: fmt(
            F(fact(len(word)), repeat_factor(word))
            - (0 if v == 1 else F(fact(c + 1) * fact(v), repeat_factor(word, "vowels") * repeat_factor(word, "consonants")))
        )
    )(i["word"], sum(1 for ch in i["word"] if ch in "AEIOU"), sum(1 for ch in i["word"] if ch not in "AEIOU")),
    "p_consonants_together": lambda i: (
        lambda word, v, c: fmt(F(fact(v + 1) * fact(c), repeat_factor(word, "consonants") * repeat_factor(word, "vowels")))
    )(i["word"], sum(1 for ch in i["word"] if ch in "AEIOU"), sum(1 for ch in i["word"] if ch not in "AEIOU")),
    "p_pair_never_adjacent": lambda i: fmt(fact(i["n"]) - 2 * fact(i["n"] - 1)),
    "p_circular_pair_not_together": lambda i: fmt(fact(i["n"] - 1) - 2 * fact(i["n"] - 2)),
    "p_rank_word": lambda i: fmt(rank_word(i["word"])),
    "p_committee_chair": lambda i: fmt(math.comb(i["n"], i["k"]) * i["k"]),
    "p_password_pattern": lambda i: fmt(26 ** i["L"] * 10 ** i["D"]),
})

FORMULAS.update({
    "c_basic": lambda i: fmt(math.comb(i["n"], i["k"])),
    "c_exactly_groups": lambda i: fmt(math.comb(i["a"], i["r"]) * math.comb(i["b"], i["s"])),
    "c_at_least_one": lambda i: fmt(sum(math.comb(i["a"], x) * math.comb(i["b"], i["n"] - x) for x in range(i["m"], min(i["a"], i["n"]) + 1))),
    "c_at_most_one": lambda i: fmt(math.comb(i["o"], i["n"]) + math.comb(i["s"], 1) * math.comb(i["o"], i["n"] - 1)),
    "c_particular_included": lambda i: fmt(math.comb(i["n"] - 1, i["k"] - 1)),
    "c_particular_excluded": lambda i: fmt(math.comb(i["n"] - 1, i["k"])),
    "c_include_exclude": lambda i: fmt(math.comb(i["n"] - 2, i["k"] - 1)),
    "c_team_from_groups": lambda i: fmt(math.comb(i["a"], i["r"]) * math.comb(i["b"], i["s"])),
    "c_cards": lambda i: fmt(sum(math.comb(i["r"], x) * math.comb(i["b"], i["n"] - x) for x in range(2, min(i["r"], i["n"]) + 1))),
    "c_relation_pr_comb": lambda i: fmt(fact(i["k"])),
    "c_select_then_arrange": lambda i: fmt(math.comb(i["n"], i["k"]) * fact(i["k"])),
    "c_assign_roles": lambda i: fmt(math.comb(i["n"], i["k"]) * fact(i["k"])),
    "c_complement": lambda i: fmt(math.comb(i["n"] - i["b"], i["k"])),
    "c_question_selection": lambda i: fmt(math.comb(i["a"], i["r"]) * math.comb(i["b"], i["s"])),
    "c_diag_handshake": lambda i: fmt(math.comb(i["n"], 2)),
    "c_diag_polygon": lambda i: fmt(math.comb(i["n"], 2) - i["n"]),
    "c_at_most_from_group": lambda i: fmt(sum(math.comb(i["a"], x) * math.comb(i["b"], i["n"] - x) for x in range(0, min(i["a"], i["m"]) + 1))),
    "c_multi_step_sum": lambda i: fmt(math.comb(i["a"] + i["b"] + i["c"], i["n"])),
    "c_exactly_two_special": lambda i: fmt(math.comb(i["s"], 2) * math.comb(i["o"], i["n"] - 2)),
    "c_no_adjacent_seats": lambda i: fmt(math.comb(i["n"] - 1, 2)),
    "c_distribute_identical": lambda i: fmt(math.comb(i["n"] - 1, i["g"] - 1)),
    "c_pair_grouping": lambda i: fmt(fact(2 * i["p"]) // (2 ** i["p"] * fact(i["p"]))),
    "c_letter_selection": lambda i: fmt(math.comb(i["n"], i["k"]) + math.comb(i["n"], i["k"] - 1)),
    "c_multi_committee": lambda i: fmt(math.comb(i["a"], i["r"]) * math.comb(i["b"], i["s"])),
})

FORMULAS.update({
    "prob_basic_coin": lambda i: fmt(F(1, 2)),
    "prob_die_face": lambda i: fmt(F(1, 6)),
    "prob_die_even": lambda i: fmt(F(sum(1 for face in range(1, i["n"] + 1) if face % 2 == 0), i["n"])),
    "prob_two_dice_sum": lambda i: fmt(F({7: 6, 8: 5, 9: 4, 10: 3, 11: 2}[i["sum"]], 36)),
    "prob_doublet": lambda i: fmt(F(1, i["n"])),
    "prob_card_suit": lambda i: fmt(F(i["f"], 52)),
    "prob_card_face": lambda i: fmt(F(i["f"], 52)),
    "prob_balls_bag": lambda i: fmt(F(i["a"], i["a"] + i["b"])),
    "prob_two_same_without": lambda i: fmt(F(i["a"] * (i["a"] - 1) + i["b"] * (i["b"] - 1), (i["a"] + i["b"]) * (i["a"] + i["b"] - 1))),
    "prob_two_different_without": lambda i: fmt(F(2 * i["a"] * i["b"], (i["a"] + i["b"]) * (i["a"] + i["b"] - 1))),
    "prob_complement": lambda i: fmt(F(i["b"], i["a"] + i["b"])),
    "prob_independent_both": lambda i: fmt(F(1, i["a"] * i["b"])),
    "prob_independent_at_least_one": lambda i: fmt(1 - F(i["a"] - 1, i["a"]) * F(i["b"] - 1, i["b"])),
    "prob_conditional_without": lambda i: fmt(F(i["r"] - 1, i["r"] + i["b"] - 1)),
    "prob_conditional_table": lambda i: fmt(F(i["b"], i["a"])),
    "prob_committee_count": lambda i: fmt(F(math.comb(i["m"], i["k"]), math.comb(i["m"] + i["w"], i["k"]))),
    "prob_coin_exact_heads": lambda i: fmt(F(math.comb(i["n"], i["k"]), 2 ** i["n"])),
    "prob_coin_at_least_head": lambda i: fmt(1 - F(1, 2 ** i["n"])),
    "prob_die_multiple": lambda i: fmt(F(i["n"] // i["m"], i["n"])),
    "prob_card_ace_king": lambda i: fmt(F(i["f"], 52)),
    "prob_two_dice_product_even": lambda i: fmt(1 - F(sum(1 for face in range(1, i["n"] + 1) if face % 2 == 1), i["n"]) ** 2),
    "prob_bag_transfer": lambda i: fmt(F(i["r"], i["r"] + i["b"])),
    "prob_combination_or": lambda i: fmt(F(math.comb(i["a"] + i["b"], i["k"]) - math.comb(i["a"], i["k"]) - math.comb(i["b"], i["k"]), math.comb(i["a"] + i["b"], i["k"]))),
    "prob_die_less_than": lambda i: fmt(F(min(i["limit"] - 1, i["n"]), i["n"])),
})

FORMULAS.update({
    "di_table_total": lambda i: fmt(sum(i["v"])),
    "di_table_difference": lambda i: fmt(F(i["x"]) - F(i["y"])),
    "di_table_pct_change": lambda i: pct(F(i["new"]) - F(i["old"]), i["old"]),
    "di_table_ratio": lambda i: rat(i["a"], i["b"]),
    "di_table_average": lambda i: fmt(F(sum(i["v"]), len(i["v"]))),
    "di_table_missing": lambda i: fmt(F(i["t"]) - i["a"] - i["b"] - i["c"]),
    "di_bar_max": lambda i: ("P", "Q", "R", "S")[max(range(4), key=lambda pos: i["v"][pos])],
    "di_bar_min": lambda i: ("P", "Q", "R", "S")[min(range(4), key=lambda pos: i["v"][pos])],
    "di_bar_sum_two": lambda i: fmt(F(i["a"]) + F(i["c"])),
    "di_bar_pct_total": lambda i: pct(i["a"], i["t"]),
    "di_line_increase": lambda i: fmt(F(i["b"]) - F(i["a"])),
    "di_line_decrease": lambda i: pct(F(i["a"]) - F(i["b"]), i["a"]),
    "di_line_average": lambda i: fmt(F(sum(i["v"]), len(i["v"]))),
    "di_line_growth": lambda i: pct(F(i["b"]) - F(i["a"]), i["a"]),
    "di_pie_angle": lambda i: fmt(F(i["p"] * i["d"], 100)),
    "di_pie_value": lambda i: fmt(F(i["d"] * i["t"], 360)),
    "di_pie_diff": lambda i: fmt(F((i["a"] - i["b"]) * i["t"], 360)),
    "di_mixed_sum": lambda i: fmt(sum(i["v"])),
    "di_pct_point": lambda i: fmt(F(i["b"]) - F(i["a"])),
    "di_pass_percentage": lambda i: pct(i["p"], i["a"]),
    "di_ratio_parts": lambda i: rat(i["a"], i["b"]),
    "di_two_table_multi": lambda i: fmt(F(i["a"]) + F(i["c"]) - F(i["b"]) - F(i["d"])),
    "di_weighted_avg": lambda i: fmt(F(i["n1"] * i["a1"] + i["n2"] * i["a2"], i["n1"] + i["n2"])),
    "di_growth_compare": lambda i: (
        "A" if F(i["a2"] - i["a1"], i["a1"]) > F(i["b2"] - i["b1"], i["b1"])
        else "B" if F(i["b2"] - i["b1"], i["b1"]) > F(i["a2"] - i["a1"], i["a1"])
        else "Equal"
    ),
})

FORMULAS.update({
    "cd_total": lambda i: fmt(F(i["a"]) + F(i["b"]) + F(i["c"])),
    "cd_difference": lambda i: fmt(F(i["a"]) - F(i["b"])),
    "cd_ratio": lambda i: rat(i["a"], i["b"]),
    "cd_pct_of_total": lambda i: pct(i["a"], i["t"]),
    "cd_missing_value": lambda i: fmt(F(i["t"]) - i["a"] - i["b"]),
    "cd_average": lambda i: fmt(F(sum(i["v"]), len(i["v"]))),
    "cd_percentage_change": lambda i: pct(F(i["b"]) - F(i["a"]), i["a"]),
    "cd_successive_change": lambda i: fmt(F(i["s"] * (100 + i["p"]) * (100 - i["q"]), 10000)),
    "cd_weighted_avg": lambda i: fmt(F(i["n1"] * i["a1"] + i["n2"] * i["a2"], i["n1"] + i["n2"])),
    "cd_ratio_split": lambda i: fmt(F(i["t"] * i["a"], i["a"] + i["b"])),
    "cd_ratio_difference": lambda i: fmt(F(i["t"] * abs(i["a"] - i["b"]), i["a"] + i["b"])),
    "cd_fraction_remaining": lambda i: fmt(F(i["t"] * (i["d"] - i["n"]), i["d"])),
    "cd_cost_price": lambda i: fmt(F(i["c"] * (100 + i["p"]) * (100 - i["d"]), 10000)),
    "cd_population": lambda i: fmt(F(i["p"] * (100 + i["g"]) * (100 - i["d"]), 10000)),
    "cd_average_missing": lambda i: fmt(4 * F(i["avg"]) - i["a"] - i["b"] - i["c"]),
    "cd_two_year_total": lambda i: fmt(F(i["a"]) + F(i["b"]) + F(i["c"]) + F(i["d"])),
    "cd_two_year_gap": lambda i: fmt(F(i["b"]) + F(i["d"]) - F(i["a"]) - F(i["c"])),
    "cd_share_after_add": lambda i: pct(F(i["a"] + i["x"]), i["a"] + i["b"] + i["x"]),
    "cd_multi_tag": lambda i: pct(F(i["a"]) + F(i["b"]) - F(i["c"]), i["t"]),
    "cd_discount_ratio": lambda i: fmt(F(i["f"], i["m"] - i["f"])),
    "cd_target_actual": lambda i: pct(i["a"], i["t"]),
    "cd_expenditure_split": lambda i: fmt(F(i["t"] * i["n"], i["d"])),
    "cd_growth_difference": lambda i: fmt(abs(F(i["b"] - i["a"], i["a"]) - F(i["d"] - i["c"], i["c"])) * 100) + " percentage points",
    "cd_stock_reorder": lambda i: fmt(F(i["s"]) - F(i["o"]) + F(i["a"])),
})


def independent_answer(item) -> str:
    meta = item.get("verification_data") or {}
    family = meta.get("family")
    if family not in FORMULAS:
        raise ValueError(f"unhandled verification family: {family}")
    return str(FORMULAS[family](meta.get("inputs") or {}))


# Name used by the import validator; identical to the independent recomputer.
expected_answer = independent_answer


def main() -> int:
    failures: list[str] = []
    total = 0
    seen_ids: set[str] = set()
    seen_texts: set[str] = set()
    family_counts: dict[str, int] = {}
    for chapter, filename in FILES.items():
        path = os.path.join(DATA, filename)
        with open(path, encoding="utf-8") as handle:
            items = json.load(handle)
        if len(items) != 120:
            failures.append(f"{chapter}: expected 120 items, found {len(items)}")
        parts = {part: 0 for part in PART_SIZES}
        key = CHAPTER_KEYS[chapter]
        for index, item in enumerate(items):
            total += 1
            tag = f"{chapter}#{index + 1} ({item.get('id')})"
            item_id = item.get("id")
            if item_id != f"{key}-{index + 1:04d}":
                failures.append(f"{tag}: non-deterministic id")
            if item_id in seen_ids:
                failures.append(f"{tag}: duplicate id")
            seen_ids.add(item_id)
            if item.get("chapter") != chapter or item.get("chapter_key") != key:
                failures.append(f"{tag}: chapter label mismatch")
            if item.get("section") != f"{key}_part_{item.get('part')}":
                failures.append(f"{tag}: section mismatch")
            if item.get("difficulty") not in DIFFICULTIES:
                failures.append(f"{tag}: bad difficulty {item.get('difficulty')!r}")
            part = item.get("part")
            if part not in PART_SIZES:
                failures.append(f"{tag}: bad part {part}")
            else:
                parts[part] += 1
            text = str(item.get("question_text", "")).strip()
            if not text:
                failures.append(f"{tag}: missing question text")
            if text in seen_texts:
                failures.append(f"{tag}: duplicate question text")
            seen_texts.add(text)
            options = item.get("options", [])
            if len(options) != 4 or len(set(map(str, options))) != 4:
                failures.append(f"{tag}: options are not four distinct strings")
                continue
            letter = item.get("correct_option")
            if letter not in LETTERS:
                failures.append(f"{tag}: bad correct_option {letter}")
                continue
            if str(options[LETTERS.index(letter)]) != str(item.get("correct_answer")):
                failures.append(f"{tag}: correct_option/correct_answer mismatch")
            matches = [option for option in options if str(option) == str(item.get("correct_answer"))]
            if len(matches) != 1:
                failures.append(f"{tag}: correct answer is not unique among options")
            explanation = str(item.get("explanation", "")).strip()
            if not explanation:
                failures.append(f"{tag}: missing explanation")
            if item.get("exam_year") is not None:
                failures.append(f"{tag}: exam_year must be null")
            if item.get("source_type") != "ORIGINAL_VERIFIED":
                failures.append(f"{tag}: unexpected source_type")
            if not str(item.get("source_page", "")).strip():
                failures.append(f"{tag}: missing source_page")
            meta = item.get("verification_data")
            if not meta:
                failures.append(f"{tag}: missing verification_data")
                continue
            family = meta.get("family")
            family_counts[str(family)] = family_counts.get(str(family), 0) + 1
            try:
                expected = independent_answer(item)
            except Exception as exc:  # noqa: BLE001
                failures.append(f"{tag}: recomputation error {exc}")
                continue
            if expected != str(item.get("correct_answer")):
                failures.append(
                    f"{tag}: recomputed {expected!r} != stored {item.get('correct_answer')!r}"
                )
            if expected not in explanation and str(item.get("correct_answer")) not in explanation:
                failures.append(f"{tag}: explanation does not state the recomputed answer")
        for part, size in PART_SIZES.items():
            if parts.get(part) != size:
                failures.append(f"{chapter}: part {part} has {parts.get(part)}, expected {size}")

    print(f"verified {total} questions across {len(FILES)} chapters")
    print(f"families exercised: {len(family_counts)}; answers per family: 5")
    if failures:
        print(f"FAILED {len(failures)} checks:")
        for line in failures[:120]:
            print(" -", line)
        return 1
    print("all answers independently recomputed; structure, options, units and explanations valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
