# -*- coding: utf-8 -*-
"""Percentage – Data Interpretation (Mains) — 120 self-contained questions."""

from __future__ import annotations

from fractions import Fraction

from .bank import fmt
from .common import F, build_specs, data, dec, near_num, near_pct, pct, q, ratio

SOURCE = "Percentage Data Interpretation Mains class notes (local PDF)"
PAGES = {
    1: "6a3006de-e616-4a57-94e5-8db1d4c07b67.pdf, pp. 4-6",
    2: "6a3006de-e616-4a57-94e5-8db1d4c07b67.pdf, pp. 7-9",
    3: "6a3006de-e616-4a57-94e5-8db1d4c07b67.pdf, pp. 10-11",
    4: "6a3006de-e616-4a57-94e5-8db1d4c07b67.pdf, pp. 4-11",
}


def pdi_school_ratio(r, v):
    total1, a, b, total2, c, d = (
        (600, 3, 2, 900, 5, 4), (800, 5, 3, 1200, 7, 5),
        (900, 4, 5, 1350, 5, 4), (1200, 7, 5, 1800, 8, 7),
        (1500, 5, 4, 2100, 6, 5),
    )[v]
    girls1 = F(b * total1, a + b)
    girls2 = F(d * total2, c + d)
    change = F((girls2 - girls1) * 100, girls1)
    block = data([("school P 2021 total", total1), ("boys:girls", f"{a}:{b}"),
                  ("school P 2023 total", total2), ("boys:girls", f"{c}:{d}")])
    return q(
        "pdi_school_ratio", v,
        f"{block} Find the percentage change in the number of girls from 2021 to 2023.",
        pct(change), near_pct(change, 5),
        f"Girls 2021 = {fmt(girls1)}; girls 2023 = {fmt(girls2)}; change = "
        f"{dec(change)}%.",
        {"total1": total1, "a": a, "b": b, "total2": total2, "c": c, "d": d},
    )


def pdi_pie_two_year(r, v):
    total1, share1, total2, share2 = (
        (12000, 25, 18000, 30), (15000, 20, 24000, 25), (18000, 35, 27000, 40),
        (24000, 15, 36000, 20), (30000, 30, 42000, 35),
    )[v]
    value1 = F(total1 * share1, 100)
    value2 = F(total2 * share2, 100)
    diff = value2 - value1
    block = data([("year 1 total", total1), ("category share", f"{share1}%"),
                  ("year 2 total", total2), ("category share", f"{share2}%")])
    return q(
        "pdi_pie_two_year", v,
        f"{block} Find the increase in the category's actual value.",
        fmt(diff), near_num(diff, 500),
        f"Year 1 value = {fmt(value1)}; year 2 value = {fmt(value2)}; increase = "
        f"{fmt(diff)}.",
        {"total1": total1, "share1": share1, "total2": total2, "share2": share2},
    )


def pdi_table_percentage_change(r, v):
    old, new = ((40, 50), (50, 65), (60, 72), (80, 92), (120, 150))[v]
    change = F((new - old) * 100, old)
    block = data([("product A old price", old), ("product A new price", new),
                  ("product B old price", 100), ("product B new price", 110)])
    return q(
        "pdi_table_percentage_change", v,
        f"{block} Find the percentage increase in product A's price.",
        pct(change), near_pct(change, 2),
        f"Increase = {new} - {old} = {new - old}; percent = "
        f"({new - old}/{old}) x 100 = {dec(change)}%.",
        {"old": old, "new": new},
    )


def pdi_weighted_average(r, v):
    n1, avg1, n2, avg2 = ((20, 60, 30, 80), (30, 55, 50, 75), (40, 65, 60, 85),
                          (50, 70, 75, 90), (60, 58, 90, 78))[v]
    avg = F(n1 * avg1 + n2 * avg2, n1 + n2)
    block = data([("group 1 students", n1), ("group 1 average", avg1),
                  ("group 2 students", n2), ("group 2 average", avg2)])
    return q(
        "pdi_weighted_average", v,
        f"{block} Find the combined average score.",
        fmt(avg), near_num(avg, 2),
        f"Combined average = ({n1}x{avg1} + {n2}x{avg2})/{n1 + n2} = {fmt(avg)}.",
        {"n1": n1, "avg1": avg1, "n2": n2, "avg2": avg2},
    )


def pdi_pass_percent(r, v):
    centers = (
        (("P", 200, 70), ("Q", 300, 80), ("R", 400, 75)),
        (("P", 250, 68), ("Q", 350, 72), ("R", 450, 80)),
        (("P", 300, 75), ("Q", 400, 65), ("R", 500, 70)),
        (("P", 360, 80), ("Q", 480, 75), ("R", 600, 85)),
        (("P", 420, 65), ("Q", 540, 70), ("R", 660, 75)),
    )[v]
    target = centers[1][0]
    passed = F(centers[1][1] * centers[1][2], 100)
    block = data(
        [(f"{name} appeared", appeared) for name, appeared, _pctv in centers]
        + [(f"{name} pass%", pctv) for name, _appeared, pctv in centers]
    )
    return q(
        "pdi_pass_percent", v,
        f"{block} How many students passed in centre {target}?",
        fmt(passed), near_num(passed, 20),
        f"Passed in {target} = {centers[1][1]} x {centers[1][2]}% = {fmt(passed)}.",
        {"centers": [[name, appeared, pctv] for name, appeared, pctv in centers]},
    )


def pdi_missing_share(r, v):
    a, b, c = ((25, 30, 20), (18, 32, 24), (22, 28, 25), (15, 35, 20), (30, 25, 18))[v]
    missing = 100 - a - b - c
    block = data([("category A", f"{a}%"), ("category B", f"{b}%"),
                  ("category C", f"{c}%"), ("category D", "?")])
    return q(
        "pdi_missing_share", v,
        f"{block} Find category D's percentage share.",
        pct(missing), near_pct(missing, 3),
        f"D = 100 - ({a} + {b} + {c}) = {missing}%.",
        {"a": a, "b": b, "c": c},
    )


def pdi_successive_percent(r, v):
    base, a, b = ((10000, 20, 10), (15000, 25, 20), (20000, 15, 25),
                  (25000, 30, 10), (30000, 10, 30))[v]
    final = F(base * (100 + a) * (100 - b), 10000)
    block = data([("base production", base), ("year 1 change", f"+{a}%"),
                  ("year 2 change", f"-{b}%")])
    return q(
        "pdi_successive_percent", v,
        f"{block} Find the production after both changes.",
        fmt(final), near_num(final, 500),
        f"Final = {base} x {(100 + a)}/100 x {(100 - b)}/100 = {fmt(final)}.",
        {"base": base, "a": a, "b": b},
    )


def pdi_ratio_to_percent(r, v):
    a, b, total = ((3, 2, 500), (4, 5, 900), (5, 7, 1200), (7, 9, 1600), (8, 11, 1900))[v]
    larger = max(a, b)
    share = F(larger * 100, a + b)
    block = data([("category A:B", f"{a}:{b}"), ("total units", total)])
    return q(
        "pdi_ratio_to_percent", v,
        f"{block} What percentage of the total is the larger category?",
        pct(share), near_pct(share, 2),
        f"Larger share = {larger}/({a + b}) x 100 = {dec(share)}%.",
        {"a": a, "b": b, "total": total},
    )


def pdi_growth_comparison(r, v):
    a_old, a_new, b_old, b_new = (
        (100, 120, 200, 230), (150, 180, 250, 290), (200, 250, 300, 360),
        (250, 300, 400, 460), (300, 360, 500, 575),
    )[v]
    ga = F((a_new - a_old) * 100, a_old)
    gb = F((b_new - b_old) * 100, b_old)
    diff = abs(ga - gb)
    block = data([("city A old", a_old), ("city A new", a_new),
                  ("city B old", b_old), ("city B new", b_new)])
    return q(
        "pdi_growth_comparison", v,
        f"{block} By how many percentage points do the growth rates differ?",
        pct(diff), near_pct(diff, 2),
        f"Growth A = {dec(ga)}%, growth B = {dec(gb)}%; difference = {dec(diff)} points.",
        {"a_old": a_old, "a_new": a_new, "b_old": b_old, "b_new": b_new},
    )


def pdi_expenditure_share(r, v):
    total, share, sub = ((800000, 30, 40), (1000000, 25, 60), (1200000, 20, 75),
                         (1500000, 35, 30), (1800000, 40, 25))[v]
    amount = F(total * share * sub, 10000)
    block = data([("total expenditure", total), ("salary head share", f"{share}%"),
                  ("salary head spent on urban staff", f"{sub}%")])
    return q(
        "pdi_expenditure_share", v,
        f"{block} Find the amount spent on urban staff within the salary head.",
        fmt(amount), near_num(amount, 5000),
        f"Salary head = {total} x {share}% = {F(total * share, 100)}; urban staff "
        f"= that x {sub}% = {fmt(amount)}.",
        {"total": total, "share": share, "sub": sub},
    )


def pdi_two_condition(r, v):
    data_rows = (
        (("P", 100, 25), ("Q", 200, 30), ("R", 300, 20), ("S", 400, 15)),
        (("P", 120, 20), ("Q", 240, 25), ("R", 360, 30), ("S", 480, 10)),
        (("P", 150, 30), ("Q", 250, 15), ("R", 350, 25), ("S", 450, 20)),
        (("P", 200, 25), ("Q", 300, 20), ("R", 400, 35), ("S", 500, 10)),
        (("P", 250, 10), ("Q", 350, 30), ("R", 450, 20), ("S", 550, 25)),
    )[v]
    target = data_rows[2]
    value = F(target[1] * target[2], 100)
    block = data([(f"{name} total", total) for name, total, _ in data_rows]
                 + [(f"{name} share", f"{share}%") for name, _, share in data_rows])
    return q(
        "pdi_two_condition", v,
        f"{block} Find the actual value for {target[0]}.",
        fmt(value), near_num(value, 50),
        f"Value for {target[0]} = {target[1]} x {target[2]}% = {fmt(value)}.",
        {"rows": [[n, t, s] for n, t, s in data_rows]},
    )


def pdi_percentage_point_change(r, v):
    old_total, old_share, new_total, new_share = (
        (20000, 30, 30000, 25), (24000, 40, 36000, 35), (30000, 25, 45000, 30),
        (36000, 45, 48000, 40), (40000, 20, 60000, 25),
    )[v]
    old_value = F(old_total * old_share, 100)
    new_value = F(new_total * new_share, 100)
    change = new_value - old_value
    block = data([("year 1 total", old_total), ("year 1 share", f"{old_share}%"),
                  ("year 2 total", new_total), ("year 2 share", f"{new_share}%")])
    return q(
        "pdi_percentage_point_change", v,
        f"{block} Find the absolute change in the category's value.",
        fmt(change), near_num(change, 500),
        f"Old value = {fmt(old_value)}; new value = {fmt(new_value)}; change = "
        f"{fmt(change)}.",
        {"old_total": old_total, "old_share": old_share,
         "new_total": new_total, "new_share": new_share},
    )


def pdi_discount_distribution(r, v):
    items = (
        (("A", 20000, 10), ("B", 30000, 15), ("C", 40000, 20)),
        (("A", 25000, 12), ("B", 35000, 18), ("C", 45000, 24)),
        (("A", 30000, 15), ("B", 40000, 20), ("C", 50000, 25)),
        (("A", 36000, 20), ("B", 48000, 25), ("C", 60000, 30)),
        (("A", 42000, 10), ("B", 54000, 15), ("C", 66000, 20)),
    )[v]
    target = items[1]
    discount = F(target[1] * target[2], 100)
    block = data([(f"item {n} MP", mp) for n, mp, _ in items]
                 + [(f"item {n} discount", f"{d}%") for n, _, d in items])
    return q(
        "pdi_discount_distribution", v,
        f"{block} Find the discount amount on item {target[0]}.",
        fmt(discount), near_num(discount, 500),
        f"Discount = {target[1]} x {target[2]}% = {fmt(discount)}.",
        {"items": [[n, mp, d] for n, mp, d in items]},
    )


def pdi_production_defects(r, v):
    units, defect = ((1000, 5), (1500, 8), (2000, 12), (2500, 10), (3000, 15))[v]
    good = F(units * (100 - defect), 100)
    block = data([("units produced", units), ("defect rate", f"{defect}%")])
    return q(
        "pdi_production_defects", v,
        f"{block} How many units are good?",
        fmt(good), near_num(good, 50),
        f"Good units = {units} x {(100 - defect)}% = {fmt(good)}.",
        {"units": units, "defect": defect},
    )


def pdi_investment_return(r, v):
    a, ra, b, rb = ((50000, 8, 70000, 12), (60000, 7, 90000, 11),
                    (80000, 9, 120000, 13), (100000, 6, 150000, 10),
                    (120000, 10, 180000, 14))[v]
    interest = F(a * ra + b * rb, 100)
    block = data([("investment A", a), ("return A", f"{ra}%"),
                  ("investment B", b), ("return B", f"{rb}%")])
    return q(
        "pdi_investment_return", v,
        f"{block} Find the total annual interest.",
        fmt(interest), near_num(interest, 1000),
        f"Interest = {a}x{ra}% + {b}x{rb}% = {fmt(interest)}.",
        {"a": a, "ra": ra, "b": b, "rb": rb},
    )


def pdi_library_books(r, v):
    total, fiction, reference = ((20000, 45, 15), (30000, 40, 20), (40000, 50, 10),
                                 (50000, 35, 25), (60000, 42, 18))[v]
    diff = F(total * (fiction - reference), 100)
    block = data([("total books", total), ("fiction", f"{fiction}%"),
                  ("reference", f"{reference}%")])
    return q(
        "pdi_library_books", v,
        f"{block} Find how many more fiction books there are than reference books.",
        fmt(diff), near_num(diff, 500),
        f"Difference = {total} x ({fiction}-{reference})% = {fmt(diff)}.",
        {"total": total, "fiction": fiction, "reference": reference},
    )


def pdi_bank_loans(r, v):
    total, priority, sub = ((5000000, 40, 25), (6000000, 35, 30), (8000000, 45, 20),
                            (10000000, 30, 40), (12000000, 50, 15))[v]
    amount = F(total * priority * sub, 10000)
    block = data([("total loans", total), ("priority share", f"{priority}%"),
                  ("priority share to small borrowers", f"{sub}%")])
    return q(
        "pdi_bank_loans", v,
        f"{block} Find the amount lent to small borrowers within priority lending.",
        fmt(amount), near_num(amount, 10000),
        f"Priority loans = {F(total * priority, 100)}; small borrowers = "
        f"{fmt(amount)}.",
        {"total": total, "priority": priority, "sub": sub},
    )


def pdi_exam_weighted(r, v):
    m1, w1, m2, w2, m3, w3 = (
        (80, 30, 70, 30, 90, 40), (75, 40, 85, 25, 65, 35),
        (90, 20, 80, 30, 70, 50), (60, 25, 75, 35, 85, 40),
        (88, 30, 72, 40, 96, 30),
    )[v]
    weighted = F(m1 * w1 + m2 * w2 + m3 * w3, 100)
    block = data([("paper 1 marks", m1), ("weight", f"{w1}%"),
                  ("paper 2 marks", m2), ("weight", f"{w2}%"),
                  ("paper 3 marks", m3), ("weight", f"{w3}%")])
    return q(
        "pdi_exam_weighted", v,
        f"{block} Find the weighted percentage score.",
        pct(weighted), near_pct(weighted, 2),
        f"Weighted score = ({m1}x{w1} + {m2}x{w2} + {m3}x{w3})/100 = "
        f"{dec(weighted)}%.",
        {"m1": m1, "w1": w1, "m2": m2, "w2": w2, "m3": m3, "w3": w3},
    )


def pdi_attendance(r, v):
    classes = (
        (("A", 100, 90), ("B", 120, 85), ("C", 80, 95)),
        (("A", 150, 80), ("B", 200, 90), ("C", 100, 75)),
        (("A", 200, 92), ("B", 250, 88), ("C", 150, 80)),
        (("A", 180, 85), ("B", 220, 95), ("C", 120, 90)),
        (("A", 240, 78), ("B", 260, 82), ("C", 200, 88)),
    )[v]
    present = sum(F(n * p, 100) for _name, n, p in classes)
    strength = sum(n for _name, n, _p in classes)
    overall = F(present * 100, strength)
    block = data([(f"class {name} strength", n) for name, n, _ in classes]
                 + [(f"class {name} attendance", f"{p}%") for name, _, p in classes])
    return q(
        "pdi_attendance", v,
        f"{block} Find the overall attendance percentage.",
        pct(overall), near_pct(overall, 2),
        f"Total present = {fmt(present)} out of {strength}; overall = "
        f"{dec(overall)}%.",
        {"classes": [[name, n, p] for name, n, p in classes]},
    )


def pdi_budget_saving(r, v):
    income, rent, food, travel, extra = (
        (50000, 30, 25, 15, 20), (60000, 25, 30, 10, 25),
        (75000, 20, 35, 15, 30), (90000, 35, 20, 20, 40),
        (120000, 30, 25, 25, 50),
    )[v]
    remaining = F(income * (100 - rent) * (100 - food) * (100 - travel), 1000000)
    saving = F(remaining * (100 - extra), 100)
    block = data([("income", income), ("rent", f"{rent}%"), ("food of remainder", f"{food}%"),
                  ("travel of remainder", f"{travel}%"), ("saving of final remainder", f"{extra}%")])
    return q(
        "pdi_budget_saving", v,
        f"{block} Find the amount saved.",
        fmt(saving), near_num(saving, 500),
        f"After three spends, remainder = ₹{fmt(remaining)}; saving = "
        f"{extra}% less than that = ₹{fmt(saving)}.",
        {"income": income, "rent": rent, "food": food, "travel": travel, "extra": extra},
    )


def pdi_population_split(r, v):
    pop, male_pct, male_lit, female_lit = (
        (50000, 55, 80, 60), (60000, 60, 75, 65), (80000, 52, 85, 70),
        (100000, 58, 78, 62), (120000, 62, 82, 68),
    )[v]
    females = F(pop * (100 - male_pct), 100)
    literate_females = F(females * female_lit, 100)
    block = data([("population", pop), ("male share", f"{male_pct}%"),
                  ("male literacy", f"{male_lit}%"), ("female literacy", f"{female_lit}%")])
    return q(
        "pdi_population_split", v,
        f"{block} Find the number of literate females.",
        fmt(literate_females), near_num(literate_females, 500),
        f"Females = {fmt(females)}; literate females = {fmt(literate_females)}.",
        {"pop": pop, "male_pct": male_pct, "male_lit": male_lit, "female_lit": female_lit},
    )


def pdi_sales_mix(r, v):
    a, b, return_pct = ((1200, 1800, 5), (1500, 2500, 8), (2000, 3000, 10),
                        (2400, 3600, 12), (3000, 4500, 15))[v]
    total = a + b
    net = F(total * (100 - return_pct), 100)
    block = data([("product A sold", a), ("product B sold", b),
                  ("overall return rate", f"{return_pct}%")])
    return q(
        "pdi_sales_mix", v,
        f"{block} Find the net number of units retained after returns.",
        fmt(net), near_num(net, 100),
        f"Gross units = {total}; net = {total} x {(100 - return_pct)}% = {fmt(net)}.",
        {"a": a, "b": b, "return_pct": return_pct},
    )


def pdi_multi_year_growth(r, v):
    y1, y2, y3 = ((1000, 1200, 1500), (1200, 1500, 1800), (1500, 1800, 2250),
                  (2000, 2500, 3000), (2500, 3000, 3750))[v]
    growth = F((y3 - y1) * 100, y1)
    block = data([("year 1", y1), ("year 2", y2), ("year 3", y3)])
    return q(
        "pdi_multi_year_growth", v,
        f"{block} Find the overall percentage growth from year 1 to year 3.",
        pct(growth), near_pct(growth, 5),
        f"Growth = ({y3}-{y1})/{y1} x 100 = {dec(growth)}%.",
        {"y1": y1, "y2": y2, "y3": y3},
    )


def pdi_statement_check(r, v):
    pass_rates = ((60, 75, 80, 65), (70, 85, 90, 75), (55, 65, 72, 60),
                  (80, 88, 92, 84), (62, 78, 82, 70))[v]
    overall = F(sum(pass_rates), 4)
    above = sum(1 for rate in pass_rates if rate > overall)
    block = data([("centre P pass%", pass_rates[0]), ("centre Q pass%", pass_rates[1]),
                  ("centre R pass%", pass_rates[2]), ("centre S pass%", pass_rates[3])])
    return q(
        "pdi_statement_check", v,
        f"{block} How many centres have a pass percentage above the average of "
        f"the four centres?",
        fmt(above), near_num(above, 1),
        f"Average = {fmt(overall)}%; centres above it = {above}.",
        {"rates": list(pass_rates)},
    )


FAMILIES = [
    pdi_school_ratio, pdi_pie_two_year, pdi_table_percentage_change, pdi_weighted_average,
    pdi_pass_percent, pdi_missing_share, pdi_successive_percent, pdi_ratio_to_percent,
    pdi_growth_comparison, pdi_expenditure_share, pdi_two_condition,
    pdi_percentage_point_change, pdi_discount_distribution, pdi_production_defects,
    pdi_investment_return, pdi_library_books, pdi_bank_loans, pdi_exam_weighted,
    pdi_attendance, pdi_budget_saving, pdi_population_split, pdi_sales_mix,
    pdi_multi_year_growth, pdi_statement_check,
]


def build_percentage_di_mains():
    specs = build_specs(FAMILIES)
    return [(part, "HARD", fn, page) for part, _difficulty, fn, page in specs]
