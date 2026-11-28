# -*- coding: utf-8 -*-
"""Partnership – Data Interpretation (Prelims) — 120 self-contained questions."""

from __future__ import annotations

from .bank import fmt
from .common import F, build_specs, data, money, near_money, near_pct, pct, q, ratio

SOURCE = "Partnership Data Interpretation class notes (local PDF)"
PAGES = {
    1: '9f8905f3-85dc-44f0-bda1-42d5c96a3304.pdf, pp. 4-6',
    2: '9f8905f3-85dc-44f0-bda1-42d5c96a3304.pdf, pp. 7-8',
    3: '9f8905f3-85dc-44f0-bda1-42d5c96a3304.pdf, pp. 9-10',
    4: '9f8905f3-85dc-44f0-bda1-42d5c96a3304.pdf, pp. 11-12',
}


def pd_total_capital(r, v):
    a, b = ((60000, 40000), (75000, 45000), (90000, 60000),
            (120000, 80000), (150000, 90000))[v]
    total = a + b
    block = data([("A capital", money(a)), ("B capital", money(b))])
    return q(
        "pd_total_capital", v,
        f"{block} Find the total capital invested by A and B.",
        money(total), near_money(total, 5000),
        f"Total capital = {a} + {b} = {total}.",
        {"a": a, "b": b},
    )


def pd_simple_ratio(r, v):
    a, b = ((60000, 40000), (75000, 45000), (90000, 60000),
            (120000, 90000), (150000, 100000))[v]
    answer = ratio(a, b)
    block = data([("A capital", money(a)), ("B capital", money(b))])
    return q(
        "pd_simple_ratio", v,
        f"{block} Find the simplest ratio of A's capital to B's capital.",
        answer, [ratio(b, a), f"{a}:{b + 1000}", f"{a + 1000}:{b}"],
        f"Capital ratio = {a}:{b} = {answer} after dividing by the common factor.",
        {"a": a, "b": b},
    )


def pd_one_share(r, v):
    a, b, P = ((60000, 40000, 150000), (75000, 25000, 160000),
               (90000, 60000, 180000), (120000, 80000, 200000),
               (150000, 100000, 250000))[v]
    share = F(P * a, a + b)
    block = data([("A capital", money(a)), ("B capital", money(b)),
                  ("total profit", money(P))])
    return q(
        "pd_one_share", v,
        f"{block} Both partners invested for the same period. Find A's profit share.",
        money(share), near_money(share, 5000),
        f"Profit ratio = {a}:{b}. A's share = {P}*{a}/({a}+{b}) = {fmt(share)}.",
        {"a": a, "b": b, "P": P},
    )


def pd_share_difference(r, v):
    a, b, P = ((60000, 40000, 150000), (75000, 25000, 160000),
               (90000, 60000, 180000), (120000, 80000, 200000),
               (150000, 100000, 250000))[v]
    diff = F(P * abs(a - b), a + b)
    block = data([("A capital", money(a)), ("B capital", money(b)),
                  ("total profit", money(P))])
    return q(
        "pd_share_difference", v,
        f"{block} Both partners invested for the same period. Find the difference "
        f"between their profit shares.",
        money(diff), near_money(diff, 5000),
        f"Profit share gap = {P}*({a}-{b})/({a}+{b}) = {fmt(diff)}.",
        {"a": a, "b": b, "P": P},
    )


def pd_share_percent(r, v):
    a, b, c = ((60000, 30000, 10000), (80000, 50000, 20000),
               (90000, 40000, 20000), (120000, 70000, 10000),
               (150000, 90000, 60000))[v]
    percent = F(a * 100, a + b + c)
    block = data([("A capital", money(a)), ("B capital", money(b)),
                  ("C capital", money(c))])
    return q(
        "pd_share_percent", v,
        f"{block} Find A's percentage share of the total capital.",
        pct(percent), near_pct(percent, 2),
        f"Total capital = {a + b + c}; A's percent = {a}*100/{a + b + c} "
        f"= {fmt(percent)}%.",
        {"a": a, "b": b, "c": c},
    )


def pd_joining_months(r, v):
    cap, months = ((60000, 9), (75000, 8), (90000, 10),
                   (120000, 7), (150000, 11))[v]
    weighted = cap * months
    block = data([("partner capital", money(cap)), ("months invested", months)])
    return q(
        "pd_joining_months", v,
        f"{block} Find this partner's capital-months (capital multiplied by months).",
        money(weighted), near_money(weighted, 5000),
        f"Capital-months = {cap}*{months} = {weighted}.",
        {"cap": cap, "months": months},
    )


def pd_profit_from_ratio(r, v):
    a, b, share_a = ((3, 2, 90000), (4, 1, 120000), (5, 3, 100000),
                     (2, 3, 80000), (7, 3, 140000))[v]
    total = F(share_a * (a + b), a)
    block = data([("A profit share ratio", a), ("B profit share ratio", b),
                  ("A share", money(share_a))])
    return q(
        "pd_profit_from_ratio", v,
        f"{block} Find the total profit.",
        money(total), near_money(total, 5000),
        f"A's part is {a} out of {a}+{b}; total profit = {share_a}*({a}+{b})/{a} "
        f"= {fmt(total)}.",
        {"a": a, "b": b, "share_a": share_a},
    )


def pd_capital_missing(r, v):
    a, b, cap_b = ((3, 2, 40000), (5, 4, 80000), (4, 3, 90000),
                   (2, 5, 150000), (7, 3, 60000))[v]
    cap_a = F(cap_b * a, b)
    block = data([("A:B capital ratio", f"{a}:{b}"), ("B capital", money(cap_b))])
    return q(
        "pd_capital_missing", v,
        f"{block} Find A's capital.",
        money(cap_a), near_money(cap_a, 5000),
        f"A's capital = {cap_b}*{a}/{b} = {fmt(cap_a)}.",
        {"a": a, "b": b, "cap_b": cap_b},
    )


def pd_avg_capital(r, v):
    a, b, c = ((60000, 90000, 120000), (75000, 105000, 120000),
               (90000, 150000, 180000), (120000, 180000, 240000),
               (150000, 210000, 270000))[v]
    avg = F(a + b + c, 3)
    block = data([("A capital", money(a)), ("B capital", money(b)),
                  ("C capital", money(c))])
    return q(
        "pd_avg_capital", v,
        f"{block} Find the average capital of the three partners.",
        money(avg), near_money(avg, 5000),
        f"Average = ({a}+{b}+{c})/3 = {fmt(avg)}.",
        {"a": a, "b": b, "c": c},
    )


def pd_yearwise_total(r, v):
    p1, p2, p3 = ((90000, 120000, 150000), (110000, 130000, 160000),
                  (100000, 140000, 180000), (120000, 160000, 200000),
                  (150000, 190000, 230000))[v]
    total = p1 + p2 + p3
    block = data([("year 1 profit", money(p1)), ("year 2 profit", money(p2)),
                  ("year 3 profit", money(p3))])
    return q(
        "pd_yearwise_total", v,
        f"{block} Find the total profit over the three years.",
        money(total), near_money(total, 10000),
        f"Total profit = {p1}+{p2}+{p3} = {total}.",
        {"p1": p1, "p2": p2, "p3": p3},
    )


def pd_yearwise_growth(r, v):
    p1, p2 = ((100000, 125000), (120000, 150000), (150000, 180000),
              (200000, 240000), (250000, 300000))[v]
    growth = F((p2 - p1) * 100, p1)
    block = data([("year 1 profit", money(p1)), ("year 2 profit", money(p2))])
    return q(
        "pd_yearwise_growth", v,
        f"{block} Find the percentage increase in profit from year 1 to year 2.",
        pct(growth), near_pct(growth, 2),
        f"Increase = {p2}-{p1} = {p2 - p1}; percent = {p2 - p1}*100/{p1} "
        f"= {fmt(growth)}%.",
        {"p1": p1, "p2": p2},
    )


def pd_yearwise_avg(r, v):
    p1, p2, p3 = ((90000, 120000, 150000), (105000, 135000, 180000),
                  (120000, 150000, 210000), (150000, 180000, 240000),
                  (180000, 210000, 270000))[v]
    avg = F(p1 + p2 + p3, 3)
    block = data([("year 1 profit", money(p1)), ("year 2 profit", money(p2)),
                  ("year 3 profit", money(p3))])
    return q(
        "pd_yearwise_avg", v,
        f"{block} Find the average yearly profit.",
        money(avg), near_money(avg, 5000),
        f"Average yearly profit = ({p1}+{p2}+{p3})/3 = {fmt(avg)}.",
        {"p1": p1, "p2": p2, "p3": p3},
    )


def pd_share_from_percent(r, v):
    P, percent = ((200000, 25), (300000, 30), (400000, 15),
                  (500000, 40), (600000, 35))[v]
    amount = F(P * percent, 100)
    block = data([("total profit", money(P)), ("A share percent", f"{percent}%")])
    return q(
        "pd_share_from_percent", v,
        f"{block} Find the amount corresponding to A's share percent.",
        money(amount), near_money(amount, 5000),
        f"Amount = {P}*{percent}/100 = {fmt(amount)}.",
        {"P": P, "percent": percent},
    )


def pd_ratio_three(r, v):
    a, b, c, scale = ((3, 2, 1, 20000), (5, 3, 2, 15000),
                      (4, 3, 1, 25000), (2, 1, 1, 40000),
                      (6, 4, 3, 10000))[v]
    answer = f"{a}:{b}:{c}"
    block = data([("A capital", money(a * scale)), ("B capital", money(b * scale)),
                  ("C capital", money(c * scale))])
    return q(
        "pd_ratio_three", v,
        f"{block} Find the ratio A:B:C of the capitals.",
        answer, [f"{c}:{b}:{a}", f"{a + 1}:{b}:{c}", f"{a}:{b + 1}:{c}"],
        f"Dividing each capital by {scale} gives {a}:{b}:{c}.",
        {"a": a, "b": b, "c": c, "scale": scale},
    )


def pd_time_weighted_ratio(r, v):
    ca, cb, ma, mb = ((60000, 40000, 12, 9), (75000, 45000, 12, 8),
                      (90000, 60000, 10, 8), (120000, 80000, 12, 6),
                      (150000, 100000, 9, 6))[v]
    wa, wb = ca * ma, cb * mb
    answer = ratio(wa, wb)
    block = data([("A capital", money(ca)), ("A months", ma),
                  ("B capital", money(cb)), ("B months", mb)])
    return q(
        "pd_time_weighted_ratio", v,
        f"{block} Find the ratio of A's capital-months to B's capital-months.",
        answer, [ratio(wb, wa), ratio(ca, cb), f"{wa // 1000}:{wb // 1000}"],
        f"Capital-months are {wa} and {wb}, so the ratio is {answer}.",
        {"ca": ca, "cb": cb, "ma": ma, "mb": mb},
    )


def pd_share_with_time(r, v):
    ca, cb, ma, mb, P = ((60000, 40000, 12, 9, 180000),
                         (75000, 45000, 12, 8, 126000),
                         (90000, 60000, 10, 8, 138000),
                         (120000, 80000, 12, 6, 192000),
                         (150000, 100000, 9, 6, 195000))[v]
    wa, wb = ca * ma, cb * mb
    share = F(P * wa, wa + wb)
    block = data([("A capital", money(ca)), ("A months", ma),
                  ("B capital", money(cb)), ("B months", mb),
                  ("total profit", money(P))])
    return q(
        "pd_share_with_time", v,
        f"{block} Find A's share of the profit.",
        money(share), near_money(share, 5000),
        f"Capital-months are {wa} and {wb}; A's share = {P}*{wa}/({wa}+{wb}) "
        f"= {fmt(share)}.",
        {"ca": ca, "cb": cb, "ma": ma, "mb": mb, "P": P},
    )


def pd_partner_comparison(r, v):
    s1a, s1b, s2a, s2b = ((90000, 60000, 120000, 80000),
                          (100000, 75000, 130000, 90000),
                          (120000, 80000, 150000, 100000),
                          (150000, 90000, 180000, 120000),
                          (180000, 120000, 220000, 140000))[v]
    increase = s2a - s1a
    block = data([("year 1 A share", money(s1a)), ("year 1 B share", money(s1b)),
                  ("year 2 A share", money(s2a)), ("year 2 B share", money(s2b))])
    return q(
        "pd_partner_comparison", v,
        f"{block} Find the increase in A's profit share from year 1 to year 2.",
        money(increase), near_money(increase, 5000),
        f"Increase in A's share = {s2a}-{s1a} = {increase}.",
        {"s1a": s1a, "s1b": s1b, "s2a": s2a, "s2b": s2b},
    )


def pd_total_investment_trend(r, v):
    y1a, y1b, y2a, y2b = ((60000, 40000, 80000, 50000),
                          (75000, 45000, 90000, 60000),
                          (90000, 60000, 110000, 80000),
                          (100000, 80000, 130000, 90000),
                          (120000, 90000, 150000, 110000))[v]
    change = (y2a + y2b) - (y1a + y1b)
    block = data([("year 1 A capital", money(y1a)), ("year 1 B capital", money(y1b)),
                  ("year 2 A capital", money(y2a)), ("year 2 B capital", money(y2b))])
    return q(
        "pd_total_investment_trend", v,
        f"{block} Find the increase in total capital from year 1 to year 2.",
        money(change), near_money(change, 5000),
        f"Year 1 total = {y1a + y1b}; year 2 total = {y2a + y2b}; increase = {change}.",
        {"y1a": y1a, "y1b": y1b, "y2a": y2a, "y2b": y2b},
    )


def pd_highest_share(r, v):
    a, b, c = ((90000, 60000, 30000), (120000, 80000, 50000),
               (150000, 90000, 70000), (180000, 120000, 60000),
               (210000, 140000, 90000))[v]
    highest = max(a, b, c)
    block = data([("A profit share", money(a)), ("B profit share", money(b)),
                  ("C profit share", money(c))])
    return q(
        "pd_highest_share", v,
        f"{block} Find the largest profit share.",
        money(highest), near_money(highest, 5000),
        f"Comparing {a}, {b} and {c}, the largest share is {highest}.",
        {"a": a, "b": b, "c": c},
    )


def pd_lowest_share(r, v):
    a, b, c = ((90000, 60000, 30000), (120000, 80000, 50000),
               (150000, 90000, 70000), (180000, 120000, 60000),
               (210000, 140000, 90000))[v]
    lowest = min(a, b, c)
    block = data([("A profit share", money(a)), ("B profit share", money(b)),
                  ("C profit share", money(c))])
    return q(
        "pd_lowest_share", v,
        f"{block} Find the smallest profit share.",
        money(lowest), near_money(lowest, 5000),
        f"Comparing {a}, {b} and {c}, the smallest share is {lowest}.",
        {"a": a, "b": b, "c": c},
    )


def pd_missing_profit(r, v):
    P, a, b = ((300000, 120000, 90000), (360000, 150000, 100000),
               (420000, 180000, 130000), (480000, 200000, 150000),
               (540000, 240000, 170000))[v]
    missing = P - a - b
    block = data([("total profit", money(P)), ("A share", money(a)),
                  ("B share", money(b))])
    return q(
        "pd_missing_profit", v,
        f"{block} Find C's share of the profit.",
        money(missing), near_money(missing, 5000),
        f"C's share = {P}-{a}-{b} = {missing}.",
        {"P": P, "a": a, "b": b},
    )


def pd_capital_percent(r, v):
    a, b = ((60000, 40000), (75000, 25000), (90000, 60000),
            (120000, 80000), (150000, 90000))[v]
    percent = F(a * 100, a + b)
    block = data([("A capital", money(a)), ("B capital", money(b))])
    return q(
        "pd_capital_percent", v,
        f"{block} Find A's capital as a percentage of total capital.",
        pct(percent), near_pct(percent, 2),
        f"Total capital = {a + b}; A's share = {a}*100/{a + b} = {fmt(percent)}%.",
        {"a": a, "b": b},
    )


def pd_avg_monthly_profit(r, v):
    P, months = ((240000, 12), (180000, 9), (300000, 10),
                 (360000, 12), (420000, 14))[v]
    avg = F(P, months)
    block = data([("total profit", money(P)), ("number of months", months)])
    return q(
        "pd_avg_monthly_profit", v,
        f"{block} Find the average profit per month.",
        money(avg), near_money(avg, 2000),
        f"Average monthly profit = {P}/{months} = {fmt(avg)}.",
        {"P": P, "months": months},
    )


def pd_two_year_ratio(r, v):
    p1, p2 = ((120000, 150000), (100000, 125000), (150000, 200000),
              (200000, 250000), (240000, 300000))[v]
    answer = ratio(p1, p2)
    block = data([("year 1 profit", money(p1)), ("year 2 profit", money(p2))])
    return q(
        "pd_two_year_ratio", v,
        f"{block} Find the ratio of year 1 profit to year 2 profit.",
        answer, [ratio(p2, p1), f"{p1 // 1000}:{p2 // 1000 + 1}", f"{p1 + 1000}:{p2}"],
        f"Profit ratio = {p1}:{p2} = {answer}.",
        {"p1": p1, "p2": p2},
    )


FAMILIES = (
    pd_total_capital,
    pd_simple_ratio,
    pd_one_share,
    pd_share_difference,
    pd_share_percent,
    pd_joining_months,
    pd_profit_from_ratio,
    pd_capital_missing,
    pd_avg_capital,
    pd_yearwise_total,
    pd_yearwise_growth,
    pd_yearwise_avg,
    pd_share_from_percent,
    pd_ratio_three,
    pd_time_weighted_ratio,
    pd_share_with_time,
    pd_partner_comparison,
    pd_total_investment_trend,
    pd_highest_share,
    pd_lowest_share,
    pd_missing_profit,
    pd_capital_percent,
    pd_avg_monthly_profit,
    pd_two_year_ratio,
)


def build_partnership_di():
    return build_specs(FAMILIES, mains=False)
