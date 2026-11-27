# -*- coding: utf-8 -*-
"""Independently verify the third Banking Maths batch (6 x 120 questions).

This script never trusts ``correct_answer``.  It recomputes every result from
``verification_data`` using fresh arithmetic, rebuilds every answer string,
checks that exactly one option is correct, and validates the dataset structure.

Run:
    python backend/verify_banking_maths_set3_questions.py
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
    "Simple Interest": "banking_maths_simple_interest_questions.json",
    "Compound Interest": "banking_maths_compound_interest_questions.json",
    "Mixture and Alligation": "banking_maths_mixture_alligation_questions.json",
    "Problems on Age": "banking_maths_problems_on_age_questions.json",
    "Partnership": "banking_maths_partnership_questions.json",
    "Time and Work": "banking_maths_time_and_work_questions.json",
}

PART_SIZES = {1: 15, 2: 20, 3: 30, 4: 55}
DIFFICULTIES = {"EASY", "MEDIUM", "HARD"}
LETTERS = "ABCD"


def fmt(value) -> str:
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def dec(value) -> str:
    text = f"{float(value):.2f}"
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def ratio_str(a, b) -> str:
    x, y = Fraction(a), Fraction(b)
    scale = math.lcm(x.denominator, y.denominator)
    first = x.numerator * (scale // x.denominator)
    second = y.numerator * (scale // y.denominator)
    g = math.gcd(abs(first), abs(second)) or 1
    return f"{first // g}:{second // g}"


def ci_amount(p, rate, periods):
    return Fraction(p) * (1 + Fraction(rate) / 100) ** periods


def ci_dec(p, rate, periods):
    return dec(ci_amount(p, rate, periods))


def simulate_alternate(rates, count):
    done = Fraction(0)
    day = 0
    while done < 1:
        done += Fraction(1, rates[day % count])
        day += 1
    return str(day)


def expected_answer(item) -> str:
    meta = item["verification_data"]
    family = meta["family"]
    d = meta["inputs"]

    # ---------------------------- Simple Interest --------------------------
    if family == "si_interest":
        return fmt(Fraction(d["P"] * d["R"] * d["T"], 100))
    if family == "si_amount":
        return fmt(d["P"] + Fraction(d["P"] * d["R"] * d["T"], 100))
    if family == "si_principal":
        return fmt(Fraction(d["I"] * 100, d["R"] * d["T"]))
    if family == "si_rate":
        return fmt(Fraction(d["I"] * 100, d["P"] * d["T"]))
    if family == "si_time":
        return fmt(Fraction(d["I"] * 100, d["P"] * d["R"]))
    if family == "si_amount_principal":
        return fmt(Fraction(d["A"] * 100, 100 + d["R"] * d["T"]))
    if family == "si_amount_rate":
        return fmt(Fraction((d["A"] - d["P"]) * 100, d["P"] * d["T"]))
    if family == "si_amount_time":
        return fmt(Fraction((d["A"] - d["P"]) * 100, d["P"] * d["R"]))
    if family == "si_months":
        return fmt(Fraction(d["P"] * d["R"] * d["M"], 1200))
    if family == "si_days365":
        return fmt(Fraction(d["P"] * d["R"] * d["D"], 36500))
    if family == "si_days360":
        return fmt(Fraction(d["P"] * d["R"] * d["D"], 36000))
    if family == "si_double":
        return fmt(Fraction(100, d["R"]))
    if family == "si_triple":
        return fmt(Fraction(200, d["R"]))
    if family == "si_rate_double":
        return fmt(Fraction(100, d["T"]))
    if family == "si_split_equal":
        return fmt(Fraction(d["Total"] * d["R2"], d["R1"] + d["R2"]))
    if family == "si_split_total_interest":
        total, r1, r2, t, interest = (
            d["Total"], d["R1"], d["R2"], d["T"], d["I"]
        )
        return fmt(Fraction(interest * 100 - total * r2 * t, (r1 - r2) * t))
    if family == "si_rate_diff":
        return fmt(Fraction(d["P"] * d["T"] * (d["R1"] - d["R2"]), 100))
    if family == "si_time_ratio":
        return f"{d['T1']}:{d['T2']}"
    if family == "si_rate_ratio":
        return f"{d['R1']}:{d['R2']}"
    if family == "si_principal_ratio":
        return f"{d['P1']}:{d['P2']}"
    if family == "si_successive_rate":
        return fmt(Fraction(d["P"] * (d["T1"] * d["R1"] + d["T2"] * d["R2"]), 100))
    if family == "si_partial_withdrawal":
        p, w, r = d["P"], d["W"], d["R"]
        return fmt(Fraction(p * r * d["T1"] + (p - w) * r * d["T2"], 100))
    if family == "si_extra_deposit":
        p, e, r = d["P"], d["E"], d["R"]
        return fmt(
            p + Fraction(p * r * d["T1"], 100)
            + (p + e) + Fraction((p + e) * r * d["T2"], 100)
        )
    if family == "si_compare":
        p, t = d["P"], d["T"]
        a = Fraction(p * d["R1"] * t, 100)
        b = Fraction(p * d["R2"] * t, 100)
        return "First option" if a > b else "Second option" if b > a else "Both pay equally"

    # --------------------------- Compound Interest -------------------------
    if family == "ci_amount_annual":
        return ci_dec(d["P"], d["R"], d["T"])
    if family == "ci_interest_annual":
        return dec(ci_amount(d["P"], d["R"], d["T"]) - d["P"])
    if family == "ci_half_amount":
        return ci_dec(d["P"], Fraction(d["R"], 2), 2 * d["T"])
    if family == "ci_half_interest":
        return dec(ci_amount(d["P"], Fraction(d["R"], 2), 2) - d["P"])
    if family == "ci_quarter_amount":
        return ci_dec(d["P"], Fraction(d["R"], 4), 4)
    if family == "ci_quarter_interest":
        return dec(ci_amount(d["P"], Fraction(d["R"], 4), 4) - d["P"])
    if family == "ci_principal":
        assert ci_amount(d["P"], d["R"], d["T"]) == d["A"]
        return str(d["P"])
    if family == "ci_find_rate":
        assert ci_amount(d["P"], d["R"], d["T"]) == d["A"]
        return str(d["R"])
    if family == "ci_find_time":
        assert ci_amount(d["P"], d["R"], d["T"]) == d["A"]
        return str(d["T"])
    if family == "ci_si_ci_diff2":
        rr = Fraction(d["R"], 100)
        return dec(Fraction(d["P"]) * rr * rr)
    if family == "ci_si_ci_diff3":
        rr = Fraction(d["R"], 100)
        return dec(Fraction(d["P"]) * rr * rr * (3 + rr))
    if family == "ci_growth":
        return ci_dec(d["P"], d["R"], 2)
    if family == "ci_depreciation":
        return ci_dec(d["P"], -d["R"], 2)
    if family == "ci_variable_rates":
        p = d["P"]
        return dec(p * (1 + Fraction(d["R1"], 100)) * (1 + Fraction(d["R2"], 100)))
    if family == "ci_amount_ratio":
        a1 = ci_dec(d["P"], d["R1"], d["T"])
        a2 = ci_dec(d["P"], d["R2"], d["T"])
        return f"{a1}:{a2}"
    if family == "ci_half_annual_diff":
        p, rate = d["P"], d["R"]
        return dec(ci_amount(p, Fraction(rate, 2), 2) - ci_amount(p, rate, 1))
    if family == "ci_quarter_annual_diff":
        p, rate = d["P"], d["R"]
        return dec(ci_amount(p, Fraction(rate, 4), 4) - ci_amount(p, rate, 1))
    if family == "ci_fractional_rate":
        rate = Fraction(d["R"])
        return dec(Fraction(d["P"]) * (1 + rate / 100) ** 2)
    if family == "ci_interest_year_ratio":
        first = Fraction(d["P"]) * Fraction(d["R"], 100)
        second = first * (1 + Fraction(d["R"], 100))
        return f"{dec(second)}:{dec(first)}"
    if family == "ci_principal_from_ci":
        assert ci_amount(d["P"], d["R"], d["T"]) == d["P"] + d["CI"]
        return str(d["P"])
    if family == "ci_three_year_amount":
        return ci_dec(d["P"], d["R"], 3)
    if family == "ci_half_rate":
        assert ci_dec(d["P"], Fraction(d["R"], 2), 2 * d["T"]) == d["A"]
        return str(d["R"])
    if family == "ci_compare":
        a1 = ci_amount(d["P1"], d["R1"], d["T1"])
        a2 = ci_amount(d["P2"], d["R2"], d["T2"])
        return "Scheme A" if a1 > a2 else "Scheme B" if a2 > a1 else "Both are equal"
    if family == "ci_two_scheme_diff":
        c1 = ci_amount(d["P1"], d["R1"], d["T"]).numerator - d["P1"]
        c2 = ci_amount(d["P2"], d["R2"], d["T"]).numerator - d["P2"]
        return str(abs(c2 - c1))

    # ------------------------- Mixture and Alligation ----------------------
    if family == "mix_alligation_ratio":
        return ratio_str(d["D"] - d["M"], d["M"] - d["C"])
    if family == "mix_quantity_cheaper":
        return fmt(Fraction(d["Total"] * (d["D"] - d["M"]), d["D"] - d["C"]))
    if family == "mix_quantity_dearer":
        return fmt(Fraction(d["Total"] * (d["M"] - d["C"]), d["D"] - d["C"]))
    if family == "mix_mean_price":
        mean = Fraction(d["Q1"] * d["P1"] + d["Q2"] * d["P2"], d["Q1"] + d["Q2"])
        return dec(mean)
    if family == "mix_milk_water_ratio":
        return dec(Fraction(d["Total"] * d["M"], d["M"] + d["W"]))
    if family == "mix_replace_fraction":
        return dec((d["Total"] - Fraction(d["R"])) * Fraction(d["F"]))
    if family == "mix_replace_twice":
        keep = Fraction(d["Total"] - d["R"], d["Total"])
        return dec(Fraction(d["Total"]) * Fraction(d["F"]) * keep * keep)
    if family in ("mix_add_water", "mix_add_milk"):
        milk = Fraction(d["Total"] * d["M"], d["M"] + d["W"])
        water = d["Total"] - milk
        if family == "mix_add_water":
            return dec(Fraction(milk * d["NW"], d["NM"]) - water)
        return dec(Fraction(water * d["NM"], d["NW"]) - milk)
    if family in ("mix_two_vessels", "mix_equal_mix_ratio"):
        milk = Fraction(d["Q1"] * d["M1"], d["M1"] + d["W1"]) + Fraction(
            d["Q2"] * d["M2"], d["M2"] + d["W2"]
        )
        return ratio_str(milk, d["Q1"] + d["Q2"] - milk)
    if family == "mix_concentration_percent":
        solute = Fraction(d["Total"] * d["Pct"], 100)
        return dec(Fraction(solute * 100, d["Total"] + d["Water"])) + "%"
    if family == "mix_profit_sale":
        cost = Fraction(d["Q1"] * d["P1"] + d["Q2"] * d["P2"], d["Q1"] + d["Q2"])
        return dec(Fraction((d["SP"] - cost) * 100, cost)) + "%"
    if family in ("mix_three_ingredients", "mix_price_per_kg"):
        mean = Fraction(
            d["Q1"] * d["P1"] + d["Q2"] * d["P2"] + d["Q3"] * d["P3"],
            d["Q1"] + d["Q2"] + d["Q3"],
        ) if "Q3" in d else Fraction(
            d["Q1"] * d["P1"] + d["Q2"] * d["P2"], d["Q1"] + d["Q2"]
        )
        return dec(mean)
    if family == "mix_water_to_milk":
        milk = Fraction(d["Total"] * d["M"], d["M"] + d["W"])
        target = d["Target"]
        return dec(Fraction(milk * (target + 1), target) - d["Total"])
    if family == "mix_milk_to_add":
        water = Fraction(d["Total"] * d["W"], d["M"] + d["W"])
        return dec(water * d["Target"] - (d["Total"] - water))
    if family == "mix_ratio_from_percent":
        return ratio_str(d["Pct"], 100 - d["Pct"])
    if family == "mix_repeated_dilution":
        return dec(Fraction(d["Total"]) * (1 - Fraction(d["F"])) ** d["N"])
    if family == "mix_selling_mixture":
        cost = Fraction(d["Q1"] * d["P1"] + d["Q2"] * d["P2"], d["Q1"] + d["Q2"])
        return dec(Fraction(cost * (100 + d["Profit"]), 100))
    if family == "mix_alligation_quantity":
        return dec(Fraction(d["CQ"] * (d["M"] - d["C"]), d["D"] - d["M"]))
    if family == "mix_average_strength":
        mean = Fraction(d["Q1"] * d["P1"] + d["Q2"] * d["P2"], d["Q1"] + d["Q2"])
        return dec(mean) + "%"
    if family == "mix_removed_milk":
        return dec(Fraction(d["Remove"] * d["M"], d["M"] + d["W"]))
    if family == "mix_compare":
        f1 = Fraction(d["M1"], d["M1"] + d["W1"])
        f2 = Fraction(d["M2"], d["M2"] + d["W2"])
        return "First mixture" if f1 > f2 else "Second mixture" if f2 > f1 else "Both are equal"

    # ----------------------------- Problems on Age -------------------------
    if family == "age_friend_ratio":
        k = Fraction(d["Total"], d["A"] + d["B"])
        asked = d["A"] if d["Asked"] == "A" else d["B"]
        return fmt(asked * k)
    if family in ("age_ratio_present", "age_father_son_sum"):
        return fmt(Fraction(d["A"] * d["Total"], d["A"] + d["B"]))
    if family == "age_after_years_ratio":
        return ratio_str(d["X"] + d["N"], d["Y"] + d["N"])
    if family == "age_before_years_ratio":
        return ratio_str(d["X"] - d["N"], d["Y"] - d["N"])
    if family == "age_difference":
        return fmt(Fraction(d["B"] * d["Diff"], d["B"] - d["A"]))
    if family in ("age_mother_daughter", "age_father_at_birth", "age_teacher_student"):
        if family == "age_mother_daughter":
            return str(d["M"] - d["D"])
        if family == "age_father_at_birth":
            return str(d["F"] - d["S"])
        return str(d["T"] - d["S"])
    if family == "age_brother_sister_future":
        return str(d["Target"] - d["X"])
    if family == "age_family_average":
        return str(3 * d["Avg"] - d["A"] - d["B"])
    if family == "age_grandparent":
        return f"{d['G'] + d['N']}:{d['P'] + d['N']}"
    if family == "age_husband_wife":
        return fmt(Fraction(d["B"] * d["Diff"], d["A"] - d["B"]))
    if family == "age_three_people":
        return fmt(Fraction(d["C"] * d["Total"], d["A"] + d["B"] + d["C"]))
    if family == "age_double_after":
        assert d["X"] + d["N"] == d["Target"] * (d["Y"] + d["N"])
        return str(d["N"])
    if family == "age_half_before":
        assert d["X"] - d["N"] == d["Target"] * (d["Y"] - d["N"])
        return str(d["N"])
    if family == "age_sum_after":
        return str(d["X"] + d["Y"] + 2 * d["N"])
    if family == "age_diff_after":
        return str(d["X"] - d["Y"])
    if family == "age_ratio_change":
        return ratio_str(d["NX"], d["NY"])
    if family == "age_average_family_future":
        return fmt(Fraction(d["A"] + d["B"] + d["C"] + 3 * d["N"], 3))
    if family == "age_son_from_father_future":
        return str(d["S"] + d["N"])
    if family in ("age_cousin",):
        return str(d["Y"] - d["X"])
    if family == "age_product":
        return str(d["X"] * d["Y"])
    if family in ("age_compare", "ps_compare", "tw_compare"):
        text = item["question_text"]
        if family == "age_compare":
            first, second = "First person", "Second person"
        else:
            fixed = {"Both are equal", "Cannot be determined"}
            people = [o for o in item["options"] if o not in fixed]
            if len(people) != 2:
                raise ValueError(f"cannot identify two people from options: {item['options']}")
            people.sort(key=text.find)
            first, second = people
        if family == "age_compare":
            x, y = d["X"], d["Y"]
            return first if x > y else second if y > x else "Both are equal"
        if family == "ps_compare":
            w1, w2 = d["P1"] * d["T1"], d["P2"] * d["T2"]
            return first if w1 > w2 else second if w2 > w1 else "Both are equal"
        return first if d["X"] < d["Y"] else second if d["Y"] < d["X"] else "Both are equal"

    # ------------------------------- Partnership ---------------------------
    if family == "ps_same_time_share":
        return fmt(Fraction(d["Total"] * d["P1"], d["P1"] + d["P2"]))
    if family == "ps_time_weighted_share":
        w1, w2 = d["P1"] * d["T1"], d["P2"] * d["T2"]
        return fmt(Fraction(d["Total"] * w1, w1 + w2))
    if family == "ps_profit_ratio":
        return ratio_str(d["P1"] * d["T1"], d["P2"] * d["T2"])
    if family == "ps_capital_from_ratio":
        return fmt(Fraction(d["CB"] * d["RA"], d["RB"]))
    if family == "ps_time_from_ratio":
        return fmt(Fraction(d["T1"] * d["RB"], d["RA"]))
    if family == "ps_three_share":
        return fmt(Fraction(d["Total"] * d["P3"], d["P1"] + d["P2"] + d["P3"]))
    if family == "ps_salary_then_share":
        rest = d["Total"] - d["Salary"]
        return fmt(d["Salary"] + Fraction(rest * d["P1"], d["P1"] + d["P2"]))
    if family == "ps_join_later":
        w1, w2 = d["P1"] * 12, d["P2"] * (12 - d["Late"])
        return fmt(Fraction(d["Total"] * w1, w1 + w2))
    if family == "ps_withdraw":
        w1, w2 = d["P1"] * d["Months"], d["P2"] * 12
        return fmt(Fraction(d["Total"] * w1, w1 + w2))
    if family == "ps_changing_capital":
        wa = d["P"] * d["T1"] + 2 * d["P"] * d["T2"]
        wb = d["Q"] * (d["T1"] + d["T2"])
        return ratio_str(wa, wb)
    if family == "ps_loss_share":
        return fmt(Fraction(d["Loss"] * d["P2"], d["P1"] + d["P2"]))
    if family == "ps_equal_share_capital":
        return fmt(Fraction(d["Q"] * d["T2"], d["T1"]))
    if family == "ps_donation_then_share":
        rest = Fraction(d["Total"] * (100 - d["Donate"]), 100)
        return dec(Fraction(rest * d["P1"], d["P1"] + d["P2"]))
    if family == "ps_commission_then_share":
        rest = d["Total"] - d["Commission"]
        return fmt(d["Commission"] + Fraction(rest * d["P1"], d["P1"] + d["P2"]))
    if family == "ps_annual_profit":
        annual = d["Monthly"] * 12
        return fmt(Fraction(annual * d["RB"], d["RA"] + d["RB"]))
    if family == "ps_capital_ratio":
        return ratio_str(d["Profit1"], d["Profit2"])
    if family == "ps_two_stage":
        wa = d["P1"] * d["T1"] + d["P2"] * d["T2"]
        wb = d["Q"] * 12
        return ratio_str(wa, wb)
    if family == "ps_share_difference":
        return fmt(Fraction(d["Total"] * (d["RB"] - d["RA"]), d["RA"] + d["RB"]))
    if family == "ps_time_months":
        return ratio_str(d["P1"] * d["M1"], d["P2"] * d["M2"])
    if family == "ps_three_time_share":
        w1, w2, w3 = d["P1"] * d["M1"], d["P2"] * d["M2"], d["P3"] * d["M3"]
        return fmt(Fraction(d["Total"] * w3, w1 + w2 + w3))
    if family == "ps_profit_percent":
        return dec(Fraction(d["Profit"] * 100, d["Capital"])) + "%"
    if family == "ps_total_capital":
        return fmt(Fraction(d["Profit"] * 100, d["Rate"]))
    if family == "ps_rejoin":
        wa, wb = d["P"] * 12, d["Q"] * d["Months"] + d["Q"] * d["Months"]
        return fmt(Fraction(d["Total"] * wa, wa + wb))

    # ------------------------------ Time and Work --------------------------
    if family == "tw_basic_days":
        return fmt(Fraction(d["X"] * d["Y"], d["X"] + d["Y"]))
    if family == "tw_one_day_work":
        return fmt(Fraction(1, d["X"]))
    if family == "tw_combine_three":
        rate = Fraction(1, d["X"]) + Fraction(1, d["Y"]) + Fraction(1, d["Z"])
        return dec(1 / rate)
    if family == "tw_efficiency_ratio":
        return dec(Fraction(d["BDays"] * d["Eb"], d["Ea"]))
    if family == "tw_leave_after":
        return dec(d["N"] + (1 - Fraction(d["N"], d["X"])) * d["Y"])
    if family == "tw_alternate_days":
        return simulate_alternate([d["X"], d["Y"]], 2)
    if family in ("tw_man_days", "tw_inverse_men"):
        return fmt(Fraction(d["Men"] * d["Days"], d["NewMen"]))
    if family == "tw_men_women":
        rate = Fraction(d["Men"], d["M"] * d["Days"]) + Fraction(d["Women"], d["W"] * d["Days"])
        return dec(1 / rate)
    if family == "tw_partial_work":
        return dec((1 - Fraction(d["Frac"])) * d["YDays"])
    if family == "tw_work_wages":
        return fmt(Fraction(d["Wage"] * d["Y"], d["X"] + d["Y"]))
    if family == "tw_pipes":
        return dec(1 / (Fraction(1, d["X"]) + Fraction(1, d["Y"])))
    if family == "tw_leak":
        return dec(1 / (Fraction(1, d["X"]) - Fraction(1, d["Y"])))
    if family == "tw_outlet":
        rate = Fraction(1, d["X"]) + Fraction(1, d["Y"]) - Fraction(1, d["Z"])
        return dec(1 / rate)
    if family == "tw_efficiency_percent":
        return dec(Fraction(d["BDays"] * 100, 100 + d["Percent"]))
    if family == "tw_half_work":
        return str(2 * d["X"])
    if family == "tw_time_fraction":
        return fmt(Fraction(d["N"], d["X"]))
    if family == "tw_group_work":
        return fmt(Fraction((d["Days"] - d["Worked"]) * d["Men"], d["Men"] - d["Left"]))
    if family == "tw_remaining_work":
        return fmt(Fraction(d["Together"] * d["Alone"], d["Alone"] - d["Together"]))
    if family == "tw_combined_three":
        work = d["N"] * (Fraction(1, d["X"]) + Fraction(1, d["Y"]) + Fraction(1, d["Z"]))
        return fmt(work)
    if family == "tw_alternate_group":
        return simulate_alternate([d["X"], d["Y"], d["Z"]], 3)
    if family == "tw_wage_share":
        wa, wb = Fraction(d["N1"], d["X"]), Fraction(d["N2"], d["Y"])
        return dec(Fraction(d["Wage"] * wa, wa + wb))
    if family == "tw_capacity_ratio":
        return fmt(Fraction(d["Together"] * (d["RA"] + d["RB"]), d["RB"]))

    raise ValueError(f"unhandled verification family: {family}")


def main() -> int:
    failures: list[str] = []
    total = 0
    seen_ids: set[str] = set()
    for chapter, filename in FILES.items():
        path = os.path.join(DATA, filename)
        with open(path, encoding="utf-8") as handle:
            items = json.load(handle)
        if len(items) != 120:
            failures.append(f"{chapter}: expected 120 items, found {len(items)}")
        parts = {p: 0 for p in PART_SIZES}
        for index, item in enumerate(items):
            total += 1
            tag = f"{chapter}#{index + 1} ({item.get('id')})"
            parts[item.get("part")] = parts.get(item.get("part"), 0) + 1
            if item["id"] in seen_ids:
                failures.append(f"{tag}: duplicate id")
            seen_ids.add(item["id"])
            if item.get("difficulty") not in DIFFICULTIES:
                failures.append(f"{tag}: bad difficulty {item.get('difficulty')}")
            options = item.get("options", [])
            if len(options) != 4 or len(set(options)) != 4:
                failures.append(f"{tag}: options are not four distinct strings")
                continue
            letter = item.get("correct_option")
            if letter not in LETTERS:
                failures.append(f"{tag}: bad correct_option {letter}")
                continue
            if options[LETTERS.index(letter)] != item.get("correct_answer"):
                failures.append(f"{tag}: correct_option/correct_answer mismatch")
            matches = [o for o in options if o == item.get("correct_answer")]
            if len(matches) != 1:
                failures.append(f"{tag}: correct answer is not unique among options")
            if not str(item.get("explanation", "")).strip():
                failures.append(f"{tag}: missing explanation")
            if not item.get("verification_data"):
                failures.append(f"{tag}: missing verification_data")
                continue
            try:
                expected = expected_answer(item)
            except Exception as exc:  # noqa: BLE001
                failures.append(f"{tag}: recomputation error {exc}")
                continue
            if expected != item.get("correct_answer"):
                failures.append(
                    f"{tag}: recomputed {expected!r} != stored {item.get('correct_answer')!r}"
                )
        for part, size in PART_SIZES.items():
            if parts.get(part) != size:
                failures.append(f"{chapter}: part {part} has {parts.get(part)}, expected {size}")

    print(f"verified {total} questions across {len(FILES)} chapters")
    if failures:
        print(f"FAILED {len(failures)} checks:")
        for line in failures[:60]:
            print(" -", line)
        return 1
    print("all answers independently recomputed; structure and options valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
