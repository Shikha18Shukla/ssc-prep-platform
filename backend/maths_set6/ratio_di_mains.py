# -*- coding: utf-8 -*-
"""Ratio – Data Interpretation (Mains) — 120 self-contained questions."""

from __future__ import annotations

from fractions import Fraction

from .bank import fmt
from .common import F, build_specs, data, near_num, pct, q, ratio

SOURCE = "Ratio Data Interpretation Mains class notes (local PDF)"
PAGES = {
    1: "b9943fe1-2ef5-4b1d-a84e-09ad8387176e.pdf, pp. 4-11",
    2: "b9943fe1-2ef5-4b1d-a84e-09ad8387176e.pdf, pp. 12-20",
    3: "b9943fe1-2ef5-4b1d-a84e-09ad8387176e.pdf, pp. 21-25",
    4: "b9943fe1-2ef5-4b1d-a84e-09ad8387176e.pdf, pp. 4-25",
}


def ratio_options(answer: str):
    first, second = answer.split(":")
    return [f"{second}:{first}", f"{int(first) + 1}:{second}", f"{first}:{int(second) + 1}"]


def rdi_seller_products(r, v):
    total, px, qy = ((5000, 2500, 1500), (8000, 3200, 2400), (10000, 4500, 3500),
                     (12000, 5400, 4200), (15000, 6000, 5250))[v]
    answer = ratio(px, qy)
    block = data([("seller P total products sold", total), ("product X share of P", f"{F(px * 100, total)}%"),
                  ("seller Q total products sold", total), ("product Y share of Q", f"{F(qy * 100, total)}%")])
    return q(
        "rdi_seller_products", v,
        f"{block} Find the ratio of product X sold by P to product Y sold by Q.",
        answer, ratio_options(answer),
        f"X by P = {px}; Y by Q = {qy}; ratio = {answer}.",
        {"total": total, "px": px, "qy": qy},
    )


def rdi_division_gender(r, v):
    total, male_pct = ((400, 55), (600, 60), (800, 45), (1000, 65), (1200, 50))[v]
    female = F(total * (100 - male_pct), 100)
    answer = ratio(female, F(total * male_pct, 100))
    block = data([("division A total", total), ("male share", f"{male_pct}%"),
                  ("division B total", total), ("male share", f"{male_pct}%")])
    return q(
        "rdi_division_gender", v,
        f"{block} Find the ratio of females in division A to males in division B.",
        answer, ratio_options(answer),
        f"Females in A = {fmt(female)}; males in B = {fmt(F(total * male_pct, 100))}; "
        f"ratio = {answer}.",
        {"total": total, "male_pct": male_pct},
    )


def rdi_pie_fans(r, v):
    total, a_pct, b_pct = ((7200, 25, 15), (9600, 30, 20), (10800, 35, 10),
                           (12000, 40, 25), (14400, 20, 30))[v]
    a = F(total * a_pct, 100)
    b = F(total * b_pct, 100)
    answer = ratio(a, b)
    block = data([("total fans sold", total), ("seller A share", f"{a_pct}%"),
                  ("seller B share", f"{b_pct}%")])
    return q(
        "rdi_pie_fans", v,
        f"{block} Find the ratio of fans sold by seller A to those sold by seller B.",
        answer, ratio_options(answer),
        f"A sold {fmt(a)}; B sold {fmt(b)}; ratio = {answer}.",
        {"total": total, "a_pct": a_pct, "b_pct": b_pct},
    )


def rdi_two_year_ratio(r, v):
    y1, y2 = ((120, 180), (150, 225), (200, 280), (240, 360), (300, 420))[v]
    answer = ratio(y1, y2)
    block = data([("year 1 count", y1), ("year 2 count", y2)])
    return q(
        "rdi_two_year_ratio", v,
        f"{block} Find the ratio of year 1 count to year 2 count in lowest terms.",
        answer, ratio_options(answer),
        f"Ratio = {y1}:{y2} = {answer}.",
        {"y1": y1, "y2": y2},
    )


def rdi_ratio_missing(r, v):
    a, b, first = ((3, 5, 120), (4, 7, 160), (5, 8, 200), (7, 9, 280), (8, 11, 320))[v]
    second = F(first * b, a)
    answer = ratio(first, second)
    block = data([("quantity A:B", f"{a}:{b}"), ("quantity A", first), ("quantity B", "?")])
    return q(
        "rdi_ratio_missing", v,
        f"{block} Find the ratio of A to B after determining B.",
        answer, ratio_options(answer),
        f"B = {first}x{b}/{a} = {fmt(second)}; ratio = {answer}.",
        {"a": a, "b": b, "first": first},
    )


def rdi_investment_returns(r, v):
    a, b, ra, rb = ((2, 3, 8, 12), (3, 5, 6, 10), (4, 5, 9, 15), (5, 7, 7, 11), (3, 7, 8, 13))[v]
    profit_a = a * ra
    profit_b = b * rb
    answer = ratio(profit_a, profit_b)
    block = data([("investment A:B", f"{a}:{b}"), ("return A", f"{ra}%"), ("return B", f"{rb}%")])
    return q(
        "rdi_investment_returns", v,
        f"{block} Find the ratio of interest earned from A to that from B.",
        answer, ratio_options(answer),
        f"Interest ratio = {a}x{ra}:{b}x{rb} = {profit_a}:{profit_b} = {answer}.",
        {"a": a, "b": b, "ra": ra, "rb": rb},
    )


def rdi_month_ratio(r, v):
    m1, m2, m3 = ((120, 180, 240), (150, 225, 300), (200, 250, 350),
                  (240, 360, 420), (300, 450, 600))[v]
    answer = ratio(m1 + m2, m3)
    block = data([("January sales", m1), ("February sales", m2), ("March sales", m3)])
    return q(
        "rdi_month_ratio", v,
        f"{block} Find the ratio of combined January-February sales to March sales.",
        answer, ratio_options(answer),
        f"Combined = {m1 + m2}; March = {m3}; ratio = {answer}.",
        {"m1": m1, "m2": m2, "m3": m3},
    )


def rdi_department_ratio(r, v):
    a, b, c, d = ((3, 2, 4, 3), (5, 4, 2, 3), (7, 5, 3, 4), (4, 5, 6, 5), (8, 7, 5, 6))[v]
    males = F(a, a + b) + F(c, c + d)
    females = F(b, a + b) + F(d, c + d)
    answer = ratio(males, females)
    block = data([("dept 1 male:female", f"{a}:{b}"), ("dept 2 male:female", f"{c}:{d}"),
                  ("each department size", 100)])
    return q(
        "rdi_department_ratio", v,
        f"{block} Find the combined male:female ratio for both departments.",
        answer, ratio_options(answer),
        f"Male fractions sum to {fmt(males)}, female fractions to {fmt(females)}; "
        f"ratio = {answer}.",
        {"a": a, "b": b, "c": c, "d": d},
    )


def rdi_cost_quantity(r, v):
    qa, qb, pa, pb = ((10, 20, 2, 3), (15, 25, 3, 4), (20, 30, 4, 5),
                      (25, 40, 3, 7), (30, 50, 5, 8))[v]
    answer = ratio(qa * pa, qb * pb)
    block = data([("quantity A", qa), ("quantity B", qb),
                  ("unit price A:B", f"{pa}:{pb}")])
    return q(
        "rdi_cost_quantity", v,
        f"{block} Find the ratio of total cost of A to total cost of B.",
        answer, ratio_options(answer),
        f"Costs = {qa}x{pa} and {qb}x{pb}; ratio = {answer}.",
        {"qa": qa, "qb": qb, "pa": pa, "pb": pb},
    )


def rdi_pass_ratio(r, v):
    a, b, pa, pb = ((3, 5, 60, 80), (4, 7, 75, 65), (5, 8, 90, 70),
                    (7, 9, 80, 85), (8, 11, 65, 75))[v]
    passed_a = F(a * pa, 100)
    passed_b = F(b * pb, 100)
    answer = ratio(passed_a, passed_b)
    block = data([("appeared A:B", f"{a}:{b}"), ("pass% A", f"{pa}%"), ("pass% B", f"{pb}%")])
    return q(
        "rdi_pass_ratio", v,
        f"{block} Find the ratio of students passing in A to those passing in B.",
        answer, ratio_options(answer),
        f"Passed A = {fmt(passed_a)} units, B = {fmt(passed_b)} units; ratio = {answer}.",
        {"a": a, "b": b, "pa": pa, "pb": pb},
    )


def rdi_employees(r, v):
    male, female, a_pct, b_pct = ((600, 400, 30, 40), (900, 600, 25, 50),
                                  (1200, 800, 20, 60), (1500, 1000, 40, 30),
                                  (1800, 1200, 35, 45))[v]
    male_a = F(male * a_pct, 100)
    female_b = F(female * b_pct, 100)
    answer = ratio(male_a, female_b)
    block = data([("total male staff", male), ("total female staff", female),
                  ("male in dept A", f"{a_pct}%"), ("female in dept B", f"{b_pct}%")])
    return q(
        "rdi_employees", v,
        f"{block} Find the ratio of male employees in department A to female "
        f"employees in department B.",
        answer, ratio_options(answer),
        f"Male in A = {fmt(male_a)}; female in B = {fmt(female_b)}; ratio = {answer}.",
        {"male": male, "female": female, "a_pct": a_pct, "b_pct": b_pct},
    )


def rdi_mixture_tables(r, v):
    a, b, volume1, c, d, volume2 = (
        (2, 3, 40, 3, 1, 60), (3, 2, 60, 1, 4, 80), (4, 5, 90, 2, 7, 110),
        (5, 3, 120, 3, 5, 150), (7, 5, 180, 4, 8, 200),
    )[v]
    first = F(a * volume1, a + b) + F(c * volume2, c + d)
    second = F(b * volume1, a + b) + F(d * volume2, c + d)
    answer = ratio(first, second)
    block = data([("vessel 1 ratio", f"{a}:{b}"), ("vessel 1 volume", volume1),
                  ("vessel 2 ratio", f"{c}:{d}"), ("vessel 2 volume", volume2)])
    return q(
        "rdi_mixture_tables", v,
        f"{block} Find the first:second ratio in the combined mixture.",
        answer, ratio_options(answer),
        f"First = {fmt(first)} L; second = {fmt(second)} L; ratio = {answer}.",
        {"a": a, "b": b, "volume1": volume1, "c": c, "d": d, "volume2": volume2},
    )


def rdi_average_ratio(r, v):
    n1, avg1, n2, avg2 = ((20, 40, 30, 60), (30, 50, 50, 70), (40, 60, 60, 80),
                          (50, 55, 75, 75), (60, 65, 90, 85))[v]
    total1 = n1 * avg1
    total2 = n2 * avg2
    answer = ratio(total1, total2)
    block = data([("group 1 count", n1), ("group 1 average", avg1),
                  ("group 2 count", n2), ("group 2 average", avg2)])
    return q(
        "rdi_average_ratio", v,
        f"{block} Find the ratio of group 1 total to group 2 total.",
        answer, ratio_options(answer),
        f"Totals are {total1} and {total2}; ratio = {answer}.",
        {"n1": n1, "avg1": avg1, "n2": n2, "avg2": avg2},
    )


def rdi_percent_change_ratio(r, v):
    a, b, pa, pb = ((100, 200, 20, 10), (150, 250, 30, 20), (200, 300, 25, 15),
                    (250, 400, 40, 25), (300, 500, 10, 30))[v]
    new_a = F(a * (100 + pa), 100)
    new_b = F(b * (100 + pb), 100)
    answer = ratio(new_a, new_b)
    block = data([("item A base", a), ("item A change", f"+{pa}%"),
                  ("item B base", b), ("item B change", f"+{pb}%")])
    return q(
        "rdi_percent_change_ratio", v,
        f"{block} Find the ratio of the new values A:B.",
        answer, ratio_options(answer),
        f"New A = {fmt(new_a)}; new B = {fmt(new_b)}; ratio = {answer}.",
        {"a": a, "b": b, "pa": pa, "pb": pb},
    )


def rdi_difference_ratio(r, v):
    a1, a2, b1, b2 = ((120, 80, 200, 140), (150, 90, 250, 170), (180, 120, 300, 220),
                      (240, 160, 400, 300), (300, 210, 500, 380))[v]
    answer = ratio(a1 - a2, b1 - b2)
    block = data([("A high", a1), ("A low", a2), ("B high", b1), ("B low", b2)])
    return q(
        "rdi_difference_ratio", v,
        f"{block} Find the ratio of A's range to B's range.",
        answer, ratio_options(answer),
        f"A range = {a1 - a2}; B range = {b1 - b2}; ratio = {answer}.",
        {"a1": a1, "a2": a2, "b1": b1, "b2": b2},
    )


def rdi_cumulative_ratio(r, v):
    first, second, third = ((100, 150, 200), (120, 180, 240), (150, 225, 300),
                            (200, 300, 400), (250, 375, 500))[v]
    answer = ratio(first + second, second + third)
    block = data([("day 1 sales", first), ("day 2 sales", second), ("day 3 sales", third)])
    return q(
        "rdi_cumulative_ratio", v,
        f"{block} Find the ratio of first-two-day sales to last-two-day sales.",
        answer, ratio_options(answer),
        f"First two = {first + second}; last two = {second + third}; ratio = {answer}.",
        {"first": first, "second": second, "third": third},
    )


def rdi_surplus_ratio(r, v):
    ia, ib, ea, eb = ((50000, 70000, 40000, 52000), (60000, 90000, 45000, 65000),
                      (80000, 100000, 60000, 72000), (100000, 140000, 75000, 100000),
                      (120000, 180000, 90000, 130000))[v]
    sa = ia - ea
    sb = ib - eb
    answer = ratio(sa, sb)
    block = data([("income A", ia), ("expenditure A", ea),
                  ("income B", ib), ("expenditure B", eb)])
    return q(
        "rdi_surplus_ratio", v,
        f"{block} Find the ratio of savings of A to savings of B.",
        answer, ratio_options(answer),
        f"Savings = {sa} and {sb}; ratio = {answer}.",
        {"ia": ia, "ib": ib, "ea": ea, "eb": eb},
    )


def rdi_weighted(r, v):
    a, b, wa, wb = ((2, 3, 10, 20), (3, 5, 15, 25), (4, 7, 20, 30),
                    (5, 8, 25, 40), (7, 9, 30, 50))[v]
    answer = ratio(a * wa, b * wb)
    block = data([("value A", a), ("weight A", wa), ("value B", b), ("weight B", wb)])
    return q(
        "rdi_weighted", v,
        f"{block} Find the weighted contribution ratio A:B.",
        answer, ratio_options(answer),
        f"Weighted contributions = {a}x{wa} and {b}x{wb}; ratio = {answer}.",
        {"a": a, "b": b, "wa": wa, "wb": wb},
    )


def rdi_transfer(r, v):
    a, b, total, moved = ((5, 3, 160, 20), (4, 5, 180, 30), (7, 5, 240, 40),
                          (3, 8, 220, 25), (9, 7, 320, 50))[v]
    first = F(a * total, a + b) - moved
    second = F(b * total, a + b) + moved
    answer = ratio(first, second)
    block = data([("initial ratio A:B", f"{a}:{b}"), ("total", total), ("transferred A to B", moved)])
    return q(
        "rdi_transfer", v,
        f"{block} Find the new A:B ratio.",
        answer, ratio_options(answer),
        f"A = {fmt(first)}, B = {fmt(second)}; ratio = {answer}.",
        {"a": a, "b": b, "total": total, "moved": moved},
    )


def rdi_speed_distance(r, v):
    d1, t1, d2, t2 = ((120, 2, 180, 3), (150, 3, 200, 4), (200, 4, 300, 5),
                      (240, 6, 360, 8), (300, 5, 450, 9))[v]
    answer = ratio(F(d1, t1), F(d2, t2))
    block = data([("vehicle A distance", d1), ("vehicle A time", t1),
                  ("vehicle B distance", d2), ("vehicle B time", t2)])
    return q(
        "rdi_speed_distance", v,
        f"{block} Find the ratio of speeds A:B.",
        answer, ratio_options(answer),
        f"Speeds = {d1}/{t1} and {d2}/{t2}; ratio = {answer}.",
        {"d1": d1, "t1": t1, "d2": d2, "t2": t2},
    )


def rdi_cost_per_unit(r, v):
    total_a, qty_a, total_b, qty_b = ((6000, 20, 9000, 30), (8000, 25, 12000, 40),
                                      (10000, 40, 15000, 50), (12000, 30, 20000, 50),
                                      (15000, 50, 24000, 80))[v]
    answer = ratio(F(total_a, qty_a), F(total_b, qty_b))
    block = data([("total cost A", total_a), ("units A", qty_a),
                  ("total cost B", total_b), ("units B", qty_b)])
    return q(
        "rdi_cost_per_unit", v,
        f"{block} Find the ratio of unit costs A:B.",
        answer, ratio_options(answer),
        f"Unit costs = {fmt(F(total_a, qty_a))} and {fmt(F(total_b, qty_b))}; ratio = {answer}.",
        {"total_a": total_a, "qty_a": qty_a, "total_b": total_b, "qty_b": qty_b},
    )


def rdi_pie_angle(r, v):
    angle_a, angle_b = ((90, 60), (120, 80), (72, 108), (144, 36), (100, 80))[v]
    answer = ratio(angle_a, angle_b)
    block = data([("sector A angle", f"{angle_a}°"), ("sector B angle", f"{angle_b}°")])
    return q(
        "rdi_pie_angle", v,
        f"{block} Find the ratio of values represented by A and B.",
        answer, ratio_options(answer),
        f"Values are proportional to angles: {angle_a}:{angle_b} = {answer}.",
        {"angle_a": angle_a, "angle_b": angle_b},
    )


def rdi_statement(r, v):
    rows = (
        (("P", 3, 2), ("Q", 4, 5), ("R", 5, 4), ("S", 2, 3)),
        (("P", 5, 4), ("Q", 3, 6), ("R", 7, 5), ("S", 4, 4)),
        (("P", 2, 5), ("Q", 6, 4), ("R", 8, 7), ("S", 3, 2)),
        (("P", 7, 6), ("Q", 5, 8), ("R", 9, 7), ("S", 4, 5)),
        (("P", 4, 3), ("Q", 8, 9), ("R", 6, 5), ("S", 10, 11)),
    )[v]
    above = sum(1 for _name, a, b in rows if a > b)
    block = data([(f"dept {name} male:female", f"{a}:{b}") for name, a, b in rows])
    return q(
        "rdi_statement", v,
        f"{block} How many departments have more males than females?",
        fmt(above), near_num(above, 1),
        f"Comparing each ratio, {above} departments have male count greater than female.",
        {"rows": [[n, a, b] for n, a, b in rows]},
    )


def rdi_ratio_of_ratios(r, v):
    a, b, c, d = ((2, 3, 4, 5), (3, 5, 5, 7), (4, 7, 6, 9), (5, 8, 7, 11), (7, 9, 8, 13))[v]
    answer = ratio(F(a * c), F(b * d))
    block = data([("ratio 1", f"{a}:{b}"), ("ratio 2", f"{c}:{d}")])
    return q(
        "rdi_ratio_of_ratios", v,
        f"{block} Find the compound ratio.",
        answer, ratio_options(answer),
        f"Compound ratio = {a}x{c}:{b}x{d} = {answer}.",
        {"a": a, "b": b, "c": c, "d": d},
    )


FAMILIES = [
    rdi_seller_products, rdi_division_gender, rdi_pie_fans, rdi_two_year_ratio,
    rdi_ratio_missing, rdi_investment_returns, rdi_month_ratio, rdi_department_ratio,
    rdi_cost_quantity, rdi_pass_ratio, rdi_employees, rdi_mixture_tables,
    rdi_average_ratio, rdi_percent_change_ratio, rdi_difference_ratio,
    rdi_cumulative_ratio, rdi_surplus_ratio, rdi_weighted, rdi_transfer,
    rdi_speed_distance, rdi_cost_per_unit, rdi_pie_angle, rdi_statement,
    rdi_ratio_of_ratios,
]


def build_ratio_di_mains():
    specs = build_specs(FAMILIES)
    return [(part, "HARD", fn, page) for part, _difficulty, fn, page in specs]
