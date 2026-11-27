# -*- coding: utf-8 -*-
"""Independently verify the sixth Banking Maths batch (6 x 120 questions).

This script never trusts ``correct_answer``.  Every result is recomputed from
``verification_data.inputs`` using the formula sheet below, which was written
separately from the chapter builders.  It also validates the JSON schema,
deterministic IDs, part counts, four distinct options, answer/index agreement,
units/rounding, difficulty classification and explanation consistency.

Run:
    python backend/verify_banking_maths_set6_questions.py
"""

from __future__ import annotations

import json
import math
import os
from collections import Counter
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

FILES = {
    "Percentage Arithmetic (Mains)": "banking_maths_percentage_arithmetic_mains_questions.json",
    "Percentage – Data Interpretation (Mains)": "banking_maths_percentage_di_mains_questions.json",
    "Ratio Arithmetic (Mains)": "banking_maths_ratio_arithmetic_mains_questions.json",
    "Ratio – Data Interpretation (Mains)": "banking_maths_ratio_di_mains_questions.json",
    "Profit and Loss (Mains)": "banking_maths_profit_and_loss_mains_questions.json",
    "Profit and Loss – Data Interpretation": "banking_maths_profit_and_loss_di_questions.json",
}
CHAPTER_KEYS = {
    "Percentage Arithmetic (Mains)": "percentage_arithmetic_mains",
    "Percentage – Data Interpretation (Mains)": "percentage_data_interpretation_mains",
    "Ratio Arithmetic (Mains)": "ratio_arithmetic_mains",
    "Ratio – Data Interpretation (Mains)": "ratio_data_interpretation_mains",
    "Profit and Loss (Mains)": "profit_and_loss_mains",
    "Profit and Loss – Data Interpretation": "profit_and_loss_data_interpretation",
}
PART_SIZES = {1: 15, 2: 20, 3: 30, 4: 55}
LETTERS = "ABCD"
MAINS_CHAPTERS = {
    "Percentage Arithmetic (Mains)",
    "Percentage – Data Interpretation (Mains)",
    "Ratio Arithmetic (Mains)",
    "Ratio – Data Interpretation (Mains)",
    "Profit and Loss (Mains)",
}


def F(numerator, denominator=None):
    if denominator is None:
        return Fraction(numerator)
    return Fraction(numerator, denominator)


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


def dec(value, places: int = 2) -> str:
    text = f"{float(value):.{places}f}"
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def pct(value) -> str:
    return dec(value) + "%"


def money(value) -> str:
    return "₹" + fmt(value)


def ratio(a, b) -> str:
    x, y = F(a), F(b)
    scale = math.lcm(x.denominator, y.denominator)
    first = x.numerator * (scale // x.denominator)
    second = y.numerator * (scale // y.denominator)
    divisor = math.gcd(abs(first), abs(second)) or 1
    return f"{first // divisor}:{second // divisor}"


FORMULAS: dict = {}

# Percentage Arithmetic (Mains)
FORMULAS.update({
    "pa_successive_three": lambda i: money(F(i["base"] * (100 + i["a"]) * (100 + i["b"]) * (100 + i["c"]), 1000000)),
    "pa_reverse_original": lambda i: money(F(i["final"] * 10000, (100 + i["a"]) * (100 + i["b"]))),
    "pa_population_net": lambda i: fmt(F(i["pop"] * (100 + i["growth"]), 100) + i["migrants"]),
    "pa_price_return": lambda i: pct(F(i["rise"] * 100, 100 + i["rise"])),
    "pa_allocation_remaining": lambda i: money(F(i["income"] * (100 - i["a"]) * (100 - i["b"]) * (100 - i["c"]), 1000000)),
    "pa_weighted_average": lambda i: pct(F(i["q1"] * i["c1"] + i["q2"] * i["c2"], i["q1"] + i["q2"])),
    "pa_election_margin": lambda i: fmt(F(F(i["total"] * (100 - i["invalid"]), 100) * (2 * i["winner"] - 100), 100)),
    "pa_exam_pass": lambda i: fmt(F(i["enrolled"] * (100 - i["absent"]) * i["pass_pct"], 10000)),
    "pa_depreciation": lambda i: money(F(i["value"] * (100 - i["d1"]) * (100 - i["d2"]), 10000)),
    "pa_tax_slab": lambda i: money(F((i["income"] - i["free"]) * i["rate"] * (100 + i["cess"]), 10000)),
    "pa_percentage_point": lambda i: fmt(F(i["new_total"] * i["new_share"], 100) - F(i["old_total"] * i["old_share"], 100)),
    "pa_ratio_from_percent": lambda i: ratio(F(i["x"] * i["y"], 10000), 1),
    "pa_expenditure_change": lambda i: pct(F((100 + i["price"]) * (100 - i["consumption"]), 100) - 100),
    "pa_overlap_pass": lambda i: fmt(F(i["total"] * (i["math_pct"] + i["eng_pct"] - i["both_pct"]), 100)),
    "pa_gender_literacy": lambda i: fmt(F(i["pop"] * (i["male_pct"] * i["male_lit"] + (100 - i["male_pct"]) * i["female_lit"]), 10000)),
    "pa_investment_split": lambda i: money(F(i["total"] * i["x"] * i["r1"], (i["x"] + i["y"]) * 100) + F(i["total"] * i["y"] * i["r2"], (i["x"] + i["y"]) * 100)),
    "pa_discount_tax": lambda i: money(F(i["mp"] * (100 - i["discount"]) * (100 + i["tax"]), 10000)),
    "pa_evaporation": lambda i: pct(F(i["total"] * i["solute_pct"], i["total"] - i["evaporated"])),
    "pa_alloy_mix": lambda i: pct(F(i["q1"] * i["c1"] + i["q2"] * i["c2"], i["q1"] + i["q2"])),
    "pa_time_allocation": lambda i: fmt(F(i["hours"] * (100 - i["sleep"]) * (100 - i["study"]) * (100 - i["work"]), 1000000)),
    "pa_claim_settlement": lambda i: fmt(F(i["claims"] * (100 - i["settled"]) * (100 - i["reopened"]), 10000)),
    "pa_consecutive_discount": lambda i: pct(F(i["d1"] + i["d2"]) - F(i["d1"] * i["d2"], 100)),
    "pa_area_change": lambda i: pct(F((100 + i["a"]) * (100 + i["b"]), 100) - 100),
    "pa_two_year_growth": lambda i: fmt(F(i["pop"] * (100 + i["a"]) * (100 + i["b"]), 10000)),
})

# Ratio Arithmetic (Mains)
FORMULAS.update({
    "ra_sum_adjust": lambda i: fmt(abs(F(i["total"] * (i["a"] - i["b"]), i["a"] + i["b"]))),
    "ra_continuing": lambda i: fmt(i["a"] * F(i["added"] * (i["c"] - i["d"]), i["a"] * i["d"] - i["b"] * i["c"])),
    "ra_income_savings": lambda i: money(F(i["total_income"] * i["ib"], i["ia"] + i["ib"]) - F(i["total_exp"] * i["eb"], i["ea"] + i["eb"])),
    "ra_ages": lambda i: fmt(i["a"] * F(i["years"] * (i["c"] - i["d"]), i["a"] * i["d"] - i["b"] * i["c"])),
    "ra_coins": lambda i: fmt(F(i["value"] * i["a"], i["a"] * i["d1"] + i["b"] * i["d2"])),
    "ra_mixture_replacement": lambda i: fmt(F(i["a"] * (i["total"] - i["removed"]), i["a"] + i["b"])),
    "ra_partnership": lambda i: money(F(i["profit"] * i["a"] * i["t1"], i["a"] * i["t1"] + i["b"] * i["t2"])),
    "ra_alloy_target": lambda i: ratio(i["c2"] - i["target"], i["target"] - i["c1"]),
    "ra_students_admission": lambda i: ratio(F(i["a"] * i["total"], i["a"] + i["b"]) + i["boys"], F(i["b"] * i["total"], i["a"] + i["b"]) + i["girls"]),
    "ra_transfer": lambda i: ratio(F(i["a"] * i["total"], i["a"] + i["b"]) - i["moved"], F(i["b"] * i["total"], i["a"] + i["b"]) + i["moved"]),
    "ra_two_vessels": lambda i: ratio(F(i["a"] * i["volume"], i["a"] + i["b"]) + F(i["c"] * i["volume"], i["c"] + i["d"]), F(i["b"] * i["volume"], i["a"] + i["b"]) + F(i["d"] * i["volume"], i["c"] + i["d"])),
    "ra_speed_time": lambda i: ratio(i["b"], i["a"]),
    "ra_efficiency": lambda i: fmt(F(i["days"] * (i["a"] + i["b"]), i["a"])),
    "ra_denomination_value": lambda i: fmt(F(i["value"] * i["a"], i["a"] * i["d1"] + i["b"] * i["d2"])),
    "ra_profit_share_salary": lambda i: money(i["salary"] + F((i["profit"] - i["salary"]) * i["a"], i["a"] + i["b"])),
    "ra_lcm_hcf": lambda i: fmt(i["hcf"] * i["a"] * i["b"]),
    "ra_unit_price": lambda i: money(F(i["total"] * i["p"], i["x"] * i["p"] + i["y"] * i["qty"])),
    "ra_remove_quantity": lambda i: fmt(F(i["a"] * (i["total"] - i["removed"]), i["a"] + i["b"])),
    "ra_three_part": lambda i: fmt(F(i["b"] * i["total"], i["a"] + i["b"] + i["c"])),
    "ra_after_percentage": lambda i: ratio(i["a"] * (100 + i["pa"]), i["b"] * (100 + i["pb"])),
    "ra_distance": lambda i: ratio(i["a"] * i["t1"], i["b"] * i["t2"]),
    "ra_wages": lambda i: ratio(i["a"] * i["c"] * i["t1"], i["b"] * i["d"] * i["t2"]),
    "ra_dilution": lambda i: ratio(F(i["a"] * i["total"], i["a"] + i["b"]), F(i["b"] * i["total"], i["a"] + i["b"]) + i["added"]),
    "ra_inverse": lambda i: ratio(i["b"], i["a"]),
})

# Profit and Loss (Mains)
FORMULAS.update({
    "pl_successive_discount_profit": lambda i: pct(F((F(i["mp"] * (100 - i["d1"]) * (100 - i["d2"]), 10000) - i["cost"]) * 100, i["cost"])),
    "pl_mp_cp_ratio": lambda i: pct(F(((100 - i["discount"]) * i["a"] - 100 * i["b"]) * 100, 100 * i["b"])),
    "pl_same_sp": lambda i: (
        lambda c1, c2: pct(F((2 * i["sp"] - c1 - c2) * 100, c1 + c2))
    )(F(i["sp"] * 100, 100 + i["profit"]), F(i["sp"] * 100, 100 - i["loss"])),
    "pl_adulteration": lambda i: pct(F(((i["pure"] + i["added"]) * i["sell"] - i["pure"] * i["cost"]) * 100, i["pure"] * i["cost"])),
    "pl_false_weight": lambda i: pct(F((i["claimed"] - i["actual"]) * 100, i["actual"])),
    "pl_free_item": lambda i: pct(F((i["buy"] * (100 + i["markup"]) - 100 * (i["buy"] + i["free"])) * 100, 100 * (i["buy"] + i["free"]))),
    "pl_overheads": lambda i: money(F(i["base"] * (100 + i["overhead"]) * (100 + i["profit"]), 10000)),
    "pl_two_transactions": lambda i: (
        lambda final: pct(F((final - i["cost"]) * 100, i["cost"]))
    )(F(i["cost"] * (100 + i["p"]) * (100 - i["q"]), 10000)),
    "pl_profit_on_sp": lambda i: pct(F(i["p"] * 100, 100 - i["p"])),
    "pl_equal_sp_loss": lambda i: pct(-F(i["p"] * i["p"], 100)),
    "pl_tax_invoice": lambda i: money(F(i["mp"] * (100 - i["discount"]), 100) - i["cost"]),
    "pl_chain": lambda i: (
        lambda final: pct(F((final - i["cost"]) * 100, i["cost"]))
    )(F(i["cost"] * (100 + i["p"]) * (100 + i["q"]) * (100 - i["discount"]), 1000000)),
    "pl_wastage": lambda i: (
        lambda good: pct(F((good * i["sell"] - i["qty"] * i["cost"]) * 100, i["qty"] * i["cost"]))
    )(F(i["qty"] * (100 - i["waste"]), 100)),
    "pl_markup_target": lambda i: money(F(i["cost"] * (100 + i["target"]), 100 - i["discount"])),
    "pl_partial": lambda i: pct(F(i["x"] * i["p"] - (100 - i["x"]) * i["q"], 100)),
    "pl_discount_series": lambda i: money(F(i["mp"] * (100 - i["d1"]) * (100 - i["d2"]) * (100 - i["d3"]), 1000000)),
    "pl_changed_cost": lambda i: (
        lambda old, new: pct(F((i["sp"] - new) * 100, new))
    )(F(i["sp"] * 100, 100 + i["old_profit"]), F(F(i["sp"] * 100, 100 + i["old_profit"]) * (100 + i["rise"]), 100)),
    "pl_equal_profit": lambda i: ratio(100 + i["p2"], 100 + i["p1"]),
    "pl_buy_sell_diff": lambda i: (
        lambda cost: pct(F(((i["x"] + i["y"]) * i["sell"] - cost) * 100, cost))
    )(i["x"] * i["a"] + i["y"] * i["b"]),
    "pl_defective": lambda i: (
        lambda good: pct(F((good * i["sell"] - i["n"] * i["cost"]) * 100, i["n"] * i["cost"]))
    )(F(i["n"] * (100 - i["defective_pct"]), 100)),
    "pl_credit_terms": lambda i: (
        lambda effective: pct(F((i["credit"] - effective) * 100, effective))
    )(F(i["cash"] * (1200 + i["rate"] * i["months"]), 1200)),
    "pl_quantity_discount": lambda i: (
        lambda cost: pct(F((i["qty"] * i["sell"] - cost) * 100, cost))
    )(F(i["qty"] * i["price"] * (100 - i["discount"]), 100)),
    "pl_mixed_margin": lambda i: (
        lambda mp, revenue: pct(F((revenue - i["cost"]) * 100, i["cost"]))
    )(F(i["cost"] * (100 + i["markup"]), 100),
      F(F(i["cost"] * (100 + i["markup"]), 100) * i["full_pct"], 100)
      + F(F(i["cost"] * (100 + i["markup"]), 100) * (100 - i["full_pct"]) * (100 - i["discount"]), 10000)),
    "pl_reinvest": lambda i: (
        lambda final: pct(F((final - i["cost"]) * 100, i["cost"]))
    )(F(i["cost"] * (100 + i["p"]) * (100 - i["q"]), 10000)),
})

# Percentage DI (Mains)
FORMULAS.update({
    "pdi_school_ratio": lambda i: (
        lambda g1, g2: pct(F((g2 - g1) * 100, g1))
    )(F(i["b"] * i["total1"], i["a"] + i["b"]), F(i["d"] * i["total2"], i["c"] + i["d"])),
    "pdi_pie_two_year": lambda i: fmt(F(i["total2"] * i["share2"], 100) - F(i["total1"] * i["share1"], 100)),
    "pdi_table_percentage_change": lambda i: pct(F((i["new"] - i["old"]) * 100, i["old"])),
    "pdi_weighted_average": lambda i: fmt(F(i["n1"] * i["avg1"] + i["n2"] * i["avg2"], i["n1"] + i["n2"])),
    "pdi_pass_percent": lambda i: fmt(F(i["centers"][1][1] * i["centers"][1][2], 100)),
    "pdi_missing_share": lambda i: pct(100 - i["a"] - i["b"] - i["c"]),
    "pdi_successive_percent": lambda i: fmt(F(i["base"] * (100 + i["a"]) * (100 - i["b"]), 10000)),
    "pdi_ratio_to_percent": lambda i: pct(F(max(i["a"], i["b"]) * 100, i["a"] + i["b"])),
    "pdi_growth_comparison": lambda i: pct(abs(F((i["a_new"] - i["a_old"]) * 100, i["a_old"]) - F((i["b_new"] - i["b_old"]) * 100, i["b_old"]))),
    "pdi_expenditure_share": lambda i: fmt(F(i["total"] * i["share"] * i["sub"], 10000)),
    "pdi_two_condition": lambda i: fmt(F(i["rows"][2][1] * i["rows"][2][2], 100)),
    "pdi_percentage_point_change": lambda i: fmt(F(i["new_total"] * i["new_share"], 100) - F(i["old_total"] * i["old_share"], 100)),
    "pdi_discount_distribution": lambda i: fmt(F(i["items"][1][1] * i["items"][1][2], 100)),
    "pdi_production_defects": lambda i: fmt(F(i["units"] * (100 - i["defect"]), 100)),
    "pdi_investment_return": lambda i: fmt(F(i["a"] * i["ra"] + i["b"] * i["rb"], 100)),
    "pdi_library_books": lambda i: fmt(F(i["total"] * (i["fiction"] - i["reference"]), 100)),
    "pdi_bank_loans": lambda i: fmt(F(i["total"] * i["priority"] * i["sub"], 10000)),
    "pdi_exam_weighted": lambda i: pct(F(i["m1"] * i["w1"] + i["m2"] * i["w2"] + i["m3"] * i["w3"], 100)),
    "pdi_attendance": lambda i: pct(F(sum(F(n * p, 100) for _name, n, p in i["classes"]) * 100, sum(n for _name, n, _p in i["classes"]))),
    "pdi_budget_saving": lambda i: fmt(F(F(i["income"] * (100 - i["rent"]) * (100 - i["food"]) * (100 - i["travel"]), 1000000) * (100 - i["extra"]), 100)),
    "pdi_population_split": lambda i: fmt(F(F(i["pop"] * (100 - i["male_pct"]), 100) * i["female_lit"], 100)),
    "pdi_sales_mix": lambda i: fmt(F((i["a"] + i["b"]) * (100 - i["return_pct"]), 100)),
    "pdi_multi_year_growth": lambda i: pct(F((i["y3"] - i["y1"]) * 100, i["y1"])),
    "pdi_statement_check": lambda i: fmt(sum(1 for rate in i["rates"] if F(rate) > F(sum(i["rates"]), 4))),
})

# Ratio DI (Mains)
FORMULAS.update({
    "rdi_seller_products": lambda i: ratio(i["px"], i["qy"]),
    "rdi_division_gender": lambda i: ratio(F(i["total"] * (100 - i["male_pct"]), 100), F(i["total"] * i["male_pct"], 100)),
    "rdi_pie_fans": lambda i: ratio(F(i["total"] * i["a_pct"], 100), F(i["total"] * i["b_pct"], 100)),
    "rdi_two_year_ratio": lambda i: ratio(i["y1"], i["y2"]),
    "rdi_ratio_missing": lambda i: ratio(i["first"], F(i["first"] * i["b"], i["a"])),
    "rdi_investment_returns": lambda i: ratio(i["a"] * i["ra"], i["b"] * i["rb"]),
    "rdi_month_ratio": lambda i: ratio(i["m1"] + i["m2"], i["m3"]),
    "rdi_department_ratio": lambda i: ratio(F(i["a"], i["a"] + i["b"]) + F(i["c"], i["c"] + i["d"]), F(i["b"], i["a"] + i["b"]) + F(i["d"], i["c"] + i["d"])),
    "rdi_cost_quantity": lambda i: ratio(i["qa"] * i["pa"], i["qb"] * i["pb"]),
    "rdi_pass_ratio": lambda i: ratio(F(i["a"] * i["pa"], 100), F(i["b"] * i["pb"], 100)),
    "rdi_employees": lambda i: ratio(F(i["male"] * i["a_pct"], 100), F(i["female"] * i["b_pct"], 100)),
    "rdi_mixture_tables": lambda i: ratio(F(i["a"] * i["volume1"], i["a"] + i["b"]) + F(i["c"] * i["volume2"], i["c"] + i["d"]), F(i["b"] * i["volume1"], i["a"] + i["b"]) + F(i["d"] * i["volume2"], i["c"] + i["d"])),
    "rdi_average_ratio": lambda i: ratio(i["n1"] * i["avg1"], i["n2"] * i["avg2"]),
    "rdi_percent_change_ratio": lambda i: ratio(F(i["a"] * (100 + i["pa"]), 100), F(i["b"] * (100 + i["pb"]), 100)),
    "rdi_difference_ratio": lambda i: ratio(i["a1"] - i["a2"], i["b1"] - i["b2"]),
    "rdi_cumulative_ratio": lambda i: ratio(i["first"] + i["second"], i["second"] + i["third"]),
    "rdi_surplus_ratio": lambda i: ratio(i["ia"] - i["ea"], i["ib"] - i["eb"]),
    "rdi_weighted": lambda i: ratio(i["a"] * i["wa"], i["b"] * i["wb"]),
    "rdi_transfer": lambda i: ratio(F(i["a"] * i["total"], i["a"] + i["b"]) - i["moved"], F(i["b"] * i["total"], i["a"] + i["b"]) + i["moved"]),
    "rdi_speed_distance": lambda i: ratio(F(i["d1"], i["t1"]), F(i["d2"], i["t2"])),
    "rdi_cost_per_unit": lambda i: ratio(F(i["total_a"], i["qty_a"]), F(i["total_b"], i["qty_b"])),
    "rdi_pie_angle": lambda i: ratio(i["angle_a"], i["angle_b"]),
    "rdi_statement": lambda i: fmt(sum(1 for _name, a, b in i["rows"] if a > b)),
    "rdi_ratio_of_ratios": lambda i: ratio(F(i["a"] * i["c"]), F(i["b"] * i["d"])),
})

# Profit and Loss DI (Prelims)
FORMULAS.update({
    "pdl_cp_sp_table": lambda i: money(i["sp"] - i["cp"]),
    "pdl_profit_percent": lambda i: pct(F((i["sp"] - i["cp"]) * 100, i["cp"])),
    "pdl_discount": lambda i: pct(F((i["mp"] - i["sp"]) * 100, i["mp"])),
    "pdl_total_profit": lambda i: money(sum(sp - cp for cp, sp in i["items"])),
    "pdl_avg_profit": lambda i: money(F(sum(i["profits"]), len(i["profits"]))),
    "pdl_missing_sp": lambda i: money(F(i["cp"] * (100 + i["profit"]), 100)),
    "pdl_missing_cp": lambda i: money(F(i["sp"] * 100, 100 + i["profit"])),
    "pdl_loss_percent": lambda i: pct(F((i["cp"] - i["sp"]) * 100, i["cp"])),
    "pdl_mp_from_sp": lambda i: money(F(i["sp"] * 100, 100 - i["discount"])),
    "pdl_discount_amount": lambda i: money(F(i["mp"] * i["discount"], 100)),
    "pdl_profit_ratio": lambda i: (
        lambda g: f"{i['p1'] // g}:{i['p2'] // g}"
    )(math.gcd(i["p1"], i["p2"])),
    "pdl_share_of_total": lambda i: pct(F(i["p1"] * 100, i["p1"] + i["p2"])),
    "pdl_wholesale": lambda i: money(F(i["cp"] * (100 + i["profit"]), 100)),
    "pdl_equal_cp": lambda i: money(F(i["cp"] * (i["p1"] + i["p2"]), 100)),
    "pdl_sequence": lambda i: money(F(i["cp"] * (100 + i["p"]) * (100 - i["q"]), 10000)),
    "pdl_markup": lambda i: money(F(i["cp"] * (100 + i["markup"]), 100)),
    "pdl_tax": lambda i: money(F(i["sp"] * (100 + i["tax"]), 100)),
    "pdl_quantity": lambda i: money(i["units"] * i["profit_each"]),
    "pdl_shop_compare": lambda i: money(abs(i["p1"] - i["p2"])),
    "pdl_graph": lambda i: pct(F((i["sp"] - i["cp"]) * 100, i["cp"])),
    "pdl_caselet": lambda i: money(F(i["sales"] * 100, 100 + i["profit_pct"])),
    "pdl_discount_profit": lambda i: (
        lambda sp: pct(F((sp - i["cp"]) * 100, i["cp"]))
    )(F(i["mp"] * (100 - i["discount"]), 100)),
    "pdl_percent_of_sales": lambda i: pct(F((i["sp"] - i["cp"]) * 100, i["sp"])),
    "pdl_statement": lambda i: fmt(sum(1 for rate in i["rates"] if rate > 15)),
})


def expected_answer(item: dict) -> str:
    verification = item["verification_data"]
    family = verification["family"]
    if family not in FORMULAS:
        raise KeyError(f"no independent formula for family {family!r}")
    return FORMULAS[family](verification["inputs"])


def main() -> int:
    failures: list[str] = []
    total = 0
    seen_ids: set[str] = set()
    difficulty_counts: Counter = Counter()
    for chapter, filename in FILES.items():
        with open(os.path.join(DATA, filename), encoding="utf-8") as handle:
            items = json.load(handle)
        if len(items) != 120:
            failures.append(f"{filename}: {len(items)} items, expected 120")
        counts = Counter(item.get("part") for item in items)
        if dict(counts) != PART_SIZES:
            failures.append(f"{filename}: part counts {dict(counts)}")
        families: Counter = Counter()
        for item in items:
            item_id = item.get("id", "<missing>")
            total += 1
            families[item["verification_data"]["family"]] += 1
            difficulty_counts[(chapter, item.get("difficulty"))] += 1
            expected_id = f"{CHAPTER_KEYS[chapter]}-{items.index(item) + 1:04d}"
            if item_id != expected_id:
                failures.append(f"{item_id}: non-deterministic id, expected {expected_id}")
            if item_id in seen_ids:
                failures.append(f"{item_id}: duplicate id")
            seen_ids.add(item_id)
            if item.get("chapter") != chapter:
                failures.append(f"{item_id}: wrong chapter")
            if item.get("chapter_key") != CHAPTER_KEYS[chapter]:
                failures.append(f"{item_id}: wrong chapter_key")
            if item.get("section") != f"{CHAPTER_KEYS[chapter]}_part_{item.get('part')}":
                failures.append(f"{item_id}: wrong section")
            options = item.get("options")
            if not isinstance(options, list) or len(options) != 4 or len(set(options)) != 4:
                failures.append(f"{item_id}: options are not four distinct values")
                continue
            letter = item.get("correct_option")
            if letter not in LETTERS:
                failures.append(f"{item_id}: invalid correct_option {letter!r}")
                continue
            if options[LETTERS.index(letter)] != item.get("correct_answer"):
                failures.append(f"{item_id}: answer/option letter mismatch")
            if not str(item.get("explanation", "")).strip():
                failures.append(f"{item_id}: missing explanation")
            if item.get("source_type") != "ORIGINAL_VERIFIED":
                failures.append(f"{item_id}: source_type is not ORIGINAL_VERIFIED")
            if item.get("verification_status") != "VERIFIED":
                failures.append(f"{item_id}: verification_status is not VERIFIED")
            if item.get("exam_year") is not None:
                failures.append(f"{item_id}: exam_year is not null")
            if "set6" not in str(item.get("verification_method", "")).lower():
                failures.append(f"{item_id}: verification_method does not name Set 6")
            if chapter in MAINS_CHAPTERS and item.get("difficulty") != "HARD":
                failures.append(f"{item_id}: Mains chapter item is not HARD")
            if chapter == "Profit and Loss – Data Interpretation" and item.get("difficulty") not in {"EASY", "MEDIUM"}:
                failures.append(f"{item_id}: Prelims chapter item is not EASY/MEDIUM")
            try:
                computed = expected_answer(item)
            except Exception as exc:
                failures.append(f"{item_id}: recomputation failed: {exc}")
                continue
            if computed != item.get("correct_answer"):
                failures.append(
                    f"{item_id}: recomputed {computed!r} != stored {item.get('correct_answer')!r}"
                )
        if len(families) != 24 or any(count != 5 for count in families.values()):
            failures.append(f"{filename}: expected 24 families x 5 variants, got {len(families)} families")

    print(f"verified {total} questions across {len(FILES)} chapters")
    print(f"families per chapter: 24; variants per family: 5")
    for chapter in FILES:
        main_count = difficulty_counts[(chapter, "HARD")]
        easy_count = difficulty_counts[(chapter, "EASY")]
        medium_count = difficulty_counts[(chapter, "MEDIUM")]
        if chapter in MAINS_CHAPTERS:
            print(f"{chapter}: HARD={main_count}, EASY=0, MEDIUM=0")
        else:
            print(f"{chapter}: EASY={easy_count}, MEDIUM={medium_count}, HARD=0")
    if failures:
        print(f"FAILED {len(failures)} checks:")
        for failure in failures[:100]:
            print(" -", failure)
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
