# -*- coding: utf-8 -*-
"""Partnership - 120 verified questions for the third Maths batch."""

from __future__ import annotations

import math
from fractions import Fraction

from .bank import fmt_dec, near_ints, near_values

SOURCE = "Partnership class notes and topic-wise sets (local PDFs)"
PAGES = {
    1: "Partnership, pp. 1-202",
    2: "Partnership 02_Class Notes, pp. 1-16",
    3: "Partnership 03_Class Notes, pp. 1-13",
    4: "Partnership 04_Class Notes, pp. 1-13",
}

NAMES = [
    ("Rakesh", "Suresh"), ("Anil", "Sunil"), ("Vijay", "Ajay"),
    ("Prakash", "Manoj"), ("Sanjay", "Rajesh"), ("Kiran", "Arjun"),
    ("Deepak", "Mahesh"), ("Naveen", "Ravi"), ("Hemant", "Ganesh"),
    ("Amit", "Sumit"),
]


def pair(v):
    return NAMES[v % len(NAMES)]


def ratio_str(a, b):
    x, y = Fraction(a), Fraction(b)
    scale = math.lcm(x.denominator, y.denominator)
    first = x.numerator * (scale // x.denominator)
    second = y.numerator * (scale // y.denominator)
    g = math.gcd(abs(first), abs(second)) or 1
    return f"{first // g}:{second // g}"


def dec(value):
    return fmt_dec(float(value), 2)


def q(family, variant, text, answer, distractors, explanation, inputs):
    return {
        "text": text,
        "correct": str(answer),
        "distractors": [str(d) for d in distractors],
        "explanation": explanation,
        "verification_data": {"family": family, "variant": variant, "inputs": inputs},
    }


def ps_same_time_share(r, v):
    a, b = pair(v)
    presets = [(4000, 6000, 5000), (8000, 12000, 9000), (15000, 10000, 10000),
               (5000, 7500, 7500), (9000, 6000, 12000)]
    p1, p2, total = presets[v % len(presets)]
    share = Fraction(total * p1, p1 + p2)
    assert share.denominator == 1
    return q(
        "ps_same_time_share", v,
        f"{a} and {b} invest Rs.{p1} and Rs.{p2} in a business for the same period. "
        f"If the profit is Rs.{total}, what is {a}'s share?",
        share.numerator, near_ints(share.numerator, r, 8),
        f"Profit is shared in the capital ratio {p1}:{p2}; {a}'s share = {total} x {p1}/({p1}+{p2}) = {share.numerator}.",
        {"P1": p1, "P2": p2, "Total": total, "Share": share.numerator},
    )


def ps_time_weighted_share(r, v):
    a, b = pair(v + 1)
    presets = [(4000, 12, 6000, 8, 6000), (6000, 12, 4000, 9, 9000),
               (5000, 10, 7500, 8, 11000), (8000, 12, 12000, 6, 14000),
               (3000, 8, 2000, 12, 10000)]
    p1, t1, p2, t2, total = presets[v % len(presets)]
    w1, w2 = p1 * t1, p2 * t2
    share = Fraction(total * w1, w1 + w2)
    assert share.denominator == 1
    return q(
        "ps_time_weighted_share", v,
        f"{a} puts Rs.{p1} for {t1} months and {b} puts Rs.{p2} for {t2} months. "
        f"The profit is Rs.{total}. Find {a}'s share.",
        share.numerator, near_ints(share.numerator, r, 8),
        f"Effective capitals are {w1} and {w2}; {a}'s share = {total} x {w1}/({w1}+{w2}) = {share.numerator}.",
        {"P1": p1, "T1": t1, "P2": p2, "T2": t2, "Total": total, "Share": share.numerator},
    )


def ps_profit_ratio(r, v):
    a, b = pair(v + 2)
    presets = [(5000, 12, 8000, 9), (6000, 8, 4000, 12), (9000, 10, 6000, 15),
               (7500, 6, 5000, 9), (12000, 4, 8000, 9)]
    p1, t1, p2, t2 = presets[v % len(presets)]
    answer = ratio_str(p1 * t1, p2 * t2)
    return q(
        "ps_profit_ratio", v,
        f"{a} invests Rs.{p1} for {t1} months and {b} invests Rs.{p2} for {t2} months. "
        "What is the ratio of their profits?",
        answer, [ratio_str(p2 * t2, p1 * t1), ratio_str(p1, p2), "1:1"],
        f"Profit ratio = {p1}x{t1} : {p2}x{t2} = {answer}.",
        {"P1": p1, "T1": t1, "P2": p2, "T2": t2, "Ratio": answer},
    )


def ps_capital_from_ratio(r, v):
    a, b = pair(v + 3)
    presets = [(2, 3, 9000), (3, 5, 10000), (4, 7, 14000), (5, 8, 16000), (7, 9, 18000)]
    ra, rb, cb = presets[v % len(presets)]
    ca = Fraction(cb * ra, rb)
    assert ca.denominator == 1
    return q(
        "ps_capital_from_ratio", v,
        f"{a} and {b} share profits in the ratio {ra}:{rb}, having invested for the "
        f"same time. If {b} invested Rs.{cb}, how much did {a} invest?",
        ca.numerator, near_ints(ca.numerator, r, 8),
        f"With equal time, capital ratio = profit ratio, so {a}'s capital = {cb} x {ra}/{rb} = {ca.numerator}.",
        {"RA": ra, "RB": rb, "CB": cb, "CA": ca.numerator},
    )


def ps_time_from_ratio(r, v):
    a, b = pair(v + 4)
    presets = [(12, 3, 2), (9, 3, 1), (10, 5, 4), (8, 4, 3), (6, 2, 1)]
    t1, ra, rb = presets[v % len(presets)]
    t2 = Fraction(t1 * rb, ra)
    assert t2.denominator == 1
    return q(
        "ps_time_from_ratio", v,
        f"{a} and {b} invest equal capitals. Their profits are in the ratio {ra}:{rb}. "
        f"If {a} invested for {t1} months, for how many months did {b} invest?",
        t2.numerator, near_ints(t2.numerator, r, 3),
        f"With equal capital, profit ratio equals time ratio, so {b}'s time = {t1} x {rb}/{ra} = {t2.numerator} months.",
        {"T1": t1, "RA": ra, "RB": rb, "T2": t2.numerator},
    )


def ps_three_share(r, v):
    presets = [(4000, 6000, 10000, 20000), (5000, 5000, 10000, 12000),
               (8000, 12000, 20000, 20000), (3000, 6000, 9000, 12000),
               (7000, 3000, 10000, 10000)]
    p1, p2, p3, total = presets[v % len(presets)]
    share = Fraction(total * p3, p1 + p2 + p3)
    assert share.denominator == 1
    first, second = pair(v)
    third = pair(v + 1)[1]
    return q(
        "ps_three_share", v,
        f"{first}, {second} and {third} invest Rs.{p1}, Rs.{p2} and Rs.{p3} for one "
        f"year. Out of a profit of Rs.{total}, what does {third} receive?",
        share.numerator, near_ints(share.numerator, r, 8),
        f"Capital ratio = {p1}:{p2}:{p3}; third share = {total} x {p3}/({p1}+{p2}+{p3}) = {share.numerator}.",
        {"P1": p1, "P2": p2, "P3": p3, "Total": total, "Share": share.numerator},
    )


def ps_salary_then_share(r, v):
    a, b = pair(v)
    presets = [(4000, 6000, 10000, 1000), (8000, 12000, 15000, 1500),
               (5000, 5000, 12000, 1200), (6000, 9000, 18000, 3000),
               (10000, 15000, 20000, 2000)]
    p1, p2, total, salary = presets[v % len(presets)]
    rest = total - salary
    share = salary + Fraction(rest * p1, p1 + p2)
    assert share.denominator == 1
    return q(
        "ps_salary_then_share", v,
        f"{a} and {b} invest Rs.{p1} and Rs.{p2}. {a} gets a salary of Rs.{salary} "
        f"from a total profit of Rs.{total}; the rest is split by capital. What does {a} get in all?",
        share.numerator, near_ints(share.numerator, r, 8),
        f"Remaining profit = {rest}; capital share = {rest} x {p1}/({p1}+{p2}); total = {share.numerator}.",
        {"P1": p1, "P2": p2, "Total": total, "Salary": salary, "Share": share.numerator},
    )


def ps_join_later(r, v):
    a, b = pair(v + 1)
    presets = [(6000, 4000, 4, 13000), (8000, 6000, 3, 14000),
               (5000, 10000, 6, 15000), (12000, 8000, 4, 26000),
               (9000, 6000, 2, 14000)]
    p1, p2, late, total = presets[v % len(presets)]
    w1, w2 = p1 * 12, p2 * (12 - late)
    share = Fraction(total * w1, w1 + w2)
    assert share.denominator == 1
    return q(
        "ps_join_later", v,
        f"{a} starts a business with Rs.{p1}. After {late} months {b} joins with "
        f"Rs.{p2}. At the year's end the profit is Rs.{total}. Find {a}'s share.",
        share.numerator, near_ints(share.numerator, r, 8),
        f"Effective capitals: {a} = {w1}, {b} = {w2}; {a}'s share = {share.numerator}.",
        {"P1": p1, "P2": p2, "Late": late, "Total": total, "Share": share.numerator},
    )


def ps_withdraw(r, v):
    a, b = pair(v + 2)
    presets = [(6000, 4000, 6, 14000), (8000, 4000, 6, 12000),
               (10000, 5000, 8, 14000), (5000, 8000, 4, 14500),
               (12000, 6000, 9, 15000)]
    p1, p2, months, total = presets[v % len(presets)]
    w1, w2 = p1 * months, p2 * 12
    share = Fraction(total * w1, w1 + w2)
    assert share.denominator == 1
    return q(
        "ps_withdraw", v,
        f"{a} invests Rs.{p1} and {b} invests Rs.{p2}. {a} withdraws after "
        f"{months} months while {b} continues for the full year. If the profit is "
        f"Rs.{total}, what is {a}'s share?",
        share.numerator, near_ints(share.numerator, r, 8),
        f"Effective capitals are {w1} and {w2}; {a}'s share = {share.numerator}.",
        {"P1": p1, "P2": p2, "Months": months, "Total": total, "Share": share.numerator},
    )


def ps_changing_capital(r, v):
    a, b = pair(v + 3)
    presets = [(4000, 6000, 6, 6), (5000, 8000, 4, 8), (6000, 4000, 6, 6),
               (3000, 5000, 3, 9), (8000, 6000, 8, 4)]
    p, qcap, t1, t2 = presets[v % len(presets)]
    wa = p * t1 + 2 * p * t2
    wb = qcap * (t1 + t2)
    answer = ratio_str(wa, wb)
    return q(
        "ps_changing_capital", v,
        f"{a} invests Rs.{p} for {t1} months and then doubles it for {t2} months. "
        f"{b} keeps Rs.{qcap} invested throughout. Find the profit-sharing ratio.",
        answer, [ratio_str(wb, wa), ratio_str(p, qcap), "1:1"],
        f"{a}'s effective capital = {p}x{t1} + {2*p}x{t2} = {wa}; {b}'s = {wb}; ratio = {answer}.",
        {"P": p, "Q": qcap, "T1": t1, "T2": t2, "WA": wa, "WB": wb},
    )


def ps_loss_share(r, v):
    a, b = pair(v + 4)
    presets = [(4000, 6000, 5000), (8000, 12000, 10000), (5000, 5000, 8000),
               (3000, 7000, 9000), (9000, 6000, 12000)]
    p1, p2, loss = presets[v % len(presets)]
    share = Fraction(loss * p2, p1 + p2)
    assert share.denominator == 1
    return q(
        "ps_loss_share", v,
        f"{a} and {b} invest Rs.{p1} and Rs.{p2}. The business incurs a loss of "
        f"Rs.{loss}. How much loss does {b} bear?",
        share.numerator, near_ints(share.numerator, r, 6),
        f"Loss is shared in the capital ratio {p1}:{p2}; {b}'s loss = {loss} x {p2}/({p1}+{p2}) = {share.numerator}.",
        {"P1": p1, "P2": p2, "Loss": loss, "Share": share.numerator},
    )


def ps_equal_share_capital(r, v):
    a, b = pair(v)
    presets = [(9000, 12, 9), (12000, 8, 12), (6000, 10, 8), (10000, 6, 8), (8000, 9, 6)]
    qcap, t2, t1 = presets[v % len(presets)]
    pcap = Fraction(qcap * t2, t1)
    assert pcap.denominator == 1
    return q(
        "ps_equal_share_capital", v,
        f"{b} invests Rs.{qcap} for {t2} months. What sum should {a} invest for "
        f"{t1} months so that both earn equal profits?",
        pcap.numerator, near_ints(pcap.numerator, r, 8),
        f"Equal profit needs P1 x {t1} = {qcap} x {t2}, so P1 = {pcap.numerator}.",
        {"Q": qcap, "T2": t2, "T1": t1, "P": pcap.numerator},
    )


def ps_donation_then_share(r, v):
    a, b = pair(v + 1)
    presets = [(4000, 6000, 10000, 10), (5000, 5000, 12000, 5),
               (8000, 12000, 15000, 20), (3000, 7000, 20000, 10),
               (6000, 9000, 18000, 10)]
    p1, p2, total, donate = presets[v % len(presets)]
    rest = Fraction(total * (100 - donate), 100)
    share = rest * Fraction(p1, p1 + p2)
    answer = dec(share)
    return q(
        "ps_donation_then_share", v,
        f"{a} and {b} invest Rs.{p1} and Rs.{p2}. Of a profit of Rs.{total}, "
        f"{donate}% is donated to charity and the rest is split by capital. "
        f"What is {a}'s share?",
        answer, near_values(answer, r, 20),
        f"Amount left = {total} x (100-{donate})/100 = {dec(rest)}; {a}'s share = {answer}.",
        {"P1": p1, "P2": p2, "Total": total, "Donate": donate, "Share": answer},
    )


def ps_commission_then_share(r, v):
    a, b = pair(v + 2)
    presets = [(4000, 6000, 10000, 1000), (8000, 12000, 15000, 1500),
               (6000, 6000, 12000, 1200), (9000, 3000, 16000, 1600),
               (5000, 10000, 20000, 2000)]
    p1, p2, total, commission = presets[v % len(presets)]
    rest = total - commission
    share = commission + Fraction(rest * p1, p1 + p2)
    assert share.denominator == 1
    return q(
        "ps_commission_then_share", v,
        f"{a} and {b} invest Rs.{p1} and Rs.{p2}. {a} manages the business and "
        f"receives Rs.{commission} as commission from the Rs.{total} profit; the "
        f"balance is split by capital. What does {a} receive?",
        share.numerator, near_ints(share.numerator, r, 8),
        f"Balance = {rest}; capital share = {rest} x {p1}/({p1}+{p2}); total = {share.numerator}.",
        {"P1": p1, "P2": p2, "Total": total, "Commission": commission, "Share": share.numerator},
    )


def ps_annual_profit(r, v):
    a, b = pair(v + 3)
    presets = [(2, 3, 1000), (3, 1, 800), (5, 3, 1200), (4, 5, 900), (7, 3, 1500)]
    ra, rb, monthly = presets[v % len(presets)]
    annual = monthly * 12
    share = Fraction(annual * rb, ra + rb)
    assert share.denominator == 1
    return q(
        "ps_annual_profit", v,
        f"{a} and {b} share profits in the ratio {ra}:{rb}. The firm earns "
        f"Rs.{monthly} profit per month. What is {b}'s share for the year?",
        share.numerator, near_ints(share.numerator, r, 8),
        f"Annual profit = {monthly} x 12 = {annual}; {b}'s share = {annual} x {rb}/({ra}+{rb}) = {share.numerator}.",
        {"RA": ra, "RB": rb, "Monthly": monthly, "Share": share.numerator},
    )


def ps_capital_ratio(r, v):
    a, b = pair(v + 4)
    presets = [(4000, 6000), (9000, 3000), (7500, 5000), (12000, 8000), (5000, 7000)]
    profit1, profit2 = presets[v % len(presets)]
    answer = ratio_str(profit1, profit2)
    return q(
        "ps_capital_ratio", v,
        f"{a} and {b} invested for equal periods and received profits of "
        f"Rs.{profit1} and Rs.{profit2}. What was the ratio of their capitals?",
        answer, [ratio_str(profit2, profit1), "1:1", f"{profit1 + 100}:{profit2}"],
        f"Equal time means capital ratio equals profit ratio = {answer}.",
        {"Profit1": profit1, "Profit2": profit2, "Ratio": answer},
    )


def ps_two_stage(r, v):
    a, b = pair(v)
    presets = [(4000, 6, 6000, 6, 6000), (5000, 4, 8000, 8, 8000),
               (6000, 8, 4000, 4, 5000), (3000, 3, 9000, 9, 6000),
               (8000, 10, 4000, 2, 7000)]
    p1, t1, p2, t2, qcap = presets[v % len(presets)]
    wa = p1 * t1 + p2 * t2
    wb = qcap * 12
    answer = ratio_str(wa, wb)
    return q(
        "ps_two_stage", v,
        f"{a} invests Rs.{p1} for {t1} months and Rs.{p2} for the next {t2} months. "
        f"{b} invests Rs.{qcap} for the entire year. Find the profit ratio.",
        answer, [ratio_str(wb, wa), ratio_str(p1 + p2, qcap), "1:1"],
        f"{a}'s effective capital = {wa}; {b}'s = {wb}; ratio = {answer}.",
        {"P1": p1, "T1": t1, "P2": p2, "T2": t2, "Q": qcap, "WA": wa, "WB": wb},
    )


def ps_share_difference(r, v):
    a, b = pair(v + 1)
    presets = [(2, 3, 5000), (3, 5, 8000), (4, 7, 11000), (5, 6, 11000), (1, 3, 10000)]
    ra, rb, total = presets[v % len(presets)]
    diff = Fraction(total * (rb - ra), ra + rb)
    assert diff.denominator == 1
    return q(
        "ps_share_difference", v,
        f"{a} and {b} share profits in the ratio {ra}:{rb}. If the total profit "
        f"is Rs.{total}, how much more does {b} get than {a}?",
        diff.numerator, near_ints(diff.numerator, r, 8),
        f"Difference = {total} x ({rb}-{ra})/({ra}+{rb}) = {diff.numerator}.",
        {"RA": ra, "RB": rb, "Total": total, "Diff": diff.numerator},
    )


def ps_time_months(r, v):
    a, b = pair(v + 2)
    presets = [(5000, 12, 7500, 8), (6000, 9, 4000, 12), (8000, 6, 6000, 10),
               (9000, 8, 3000, 18), (12000, 5, 8000, 12)]
    p1, m1, p2, m2 = presets[v % len(presets)]
    answer = ratio_str(p1 * m1, p2 * m2)
    return q(
        "ps_time_months", v,
        f"{a} invests Rs.{p1} for {m1} months and {b} invests Rs.{p2} for {m2} "
        "months. In what ratio do they share the profit?",
        answer, [ratio_str(p2 * m2, p1 * m1), ratio_str(p1, p2), "1:1"],
        f"Profit ratio = capital x time = {p1}x{m1} : {p2}x{m2} = {answer}.",
        {"P1": p1, "M1": m1, "P2": p2, "M2": m2, "Ratio": answer},
    )


def ps_three_time_share(r, v):
    presets = [(4000, 12, 6000, 6, 8000, 3, 9000), (5000, 12, 5000, 8, 10000, 6, 10000),
               (6000, 10, 4000, 10, 10000, 5, 12000), (3000, 12, 6000, 9, 9000, 6, 18000),
               (8000, 6, 4000, 12, 6000, 9, 14000)]
    p1, m1, p2, m2, p3, m3, total = presets[v % len(presets)]
    w1, w2, w3 = p1 * m1, p2 * m2, p3 * m3
    share = Fraction(total * w3, w1 + w2 + w3)
    assert share.denominator == 1
    first, second = pair(v + 2)
    third = pair(v + 3)[1]
    return q(
        "ps_three_time_share", v,
        f"{first}, {second} and {third} invest Rs.{p1} for {m1} months, Rs.{p2} "
        f"for {m2} months and Rs.{p3} for {m3} months. From a profit of Rs.{total}, "
        f"find {third}'s share.",
        share.numerator, near_ints(share.numerator, r, 8),
        f"Effective capitals are {w1}, {w2} and {w3}; third share = {share.numerator}.",
        {"P1": p1, "M1": m1, "P2": p2, "M2": m2, "P3": p3, "M3": m3,
         "Total": total, "Share": share.numerator},
    )


def ps_profit_percent(r, v):
    presets = [(20000, 3000), (25000, 5000), (40000, 6000), (15000, 1800), (30000, 7500)]
    capital, profit = presets[v % len(presets)]
    percent = Fraction(profit * 100, capital)
    answer = dec(percent)
    owner = pair(v + 4)[0]
    business = ["retail shop", "trading firm", "manufacturing unit",
                "transport business", "wholesale store"][v % 5]
    return q(
        "ps_profit_percent", v,
        f"{owner}'s {business} has a total capital of Rs.{capital} and earns Rs.{profit} "
        "profit. What is the profit as a percentage of capital?",
        answer + "%", [x + "%" for x in near_values(answer, r, 2)],
        f"Profit percent = {profit} x 100 / {capital} = {answer}%.",
        {"Capital": capital, "Profit": profit, "Percent": answer},
    )


def ps_total_capital(r, v):
    presets = [(3000, 6), (4800, 8), (2500, 5), (7200, 9), (5400, 6)]
    profit, rate = presets[v % len(presets)]
    capital = Fraction(profit * 100, rate)
    assert capital.denominator == 1
    owner = pair(v + 5)[0]
    venture = ["jewellery venture", "fertiliser venture", "textile venture",
               "export venture", "food-processing venture"][v % 5]
    return q(
        "ps_total_capital", v,
        f"{owner}'s {venture} earns Rs.{profit}, which is {rate}% of its total "
        "capital. What is the total capital?",
        capital.numerator, near_ints(capital.numerator, r, 10),
        f"Capital = {profit} x 100 / {rate} = {capital.numerator}.",
        {"Profit": profit, "Rate": rate, "Capital": capital.numerator},
    )


def ps_rejoin(r, v):
    a, b = pair(v + 3)
    presets = [(6000, 4000, 3, 12000), (8000, 6000, 4, 18000),
               (5000, 5000, 6, 12000), (10000, 8000, 3, 16800),
               (9000, 3000, 2, 12000)]
    p, qcap, months, total = presets[v % len(presets)]
    wa = p * 12
    wb = qcap * months + qcap * months
    share = Fraction(total * wa, wa + wb)
    assert share.denominator == 1
    return q(
        "ps_rejoin", v,
        f"{a} invests Rs.{p} for the whole year. {b} invests Rs.{qcap} for the first "
        f"{months} months, withdraws it, then rejoins with Rs.{qcap} for the last "
        f"{months} months. If profit is Rs.{total}, what is {a}'s share?",
        share.numerator, near_ints(share.numerator, r, 8),
        f"Effective capitals: {a} = {wa}, {b} = {wb}; {a}'s share = {share.numerator}.",
        {"P": p, "Q": qcap, "Months": months, "Total": total, "Share": share.numerator},
    )


def ps_compare(r, v):
    a, b = pair(v + 4)
    presets = [(4000, 12, 6000, 6), (6000, 8, 5000, 9), (9000, 4, 4000, 12),
               (7500, 6, 6000, 8), (12000, 3, 5000, 9)]
    p1, t1, p2, t2 = presets[v % len(presets)]
    w1, w2 = p1 * t1, p2 * t2
    answer = a if w1 > w2 else b if w2 > w1 else "Both are equal"
    options = [a, b, "Both are equal", "Cannot be determined"]
    return {
        "text": (
            f"{a} invests Rs.{p1} for {t1} months and {b} invests Rs.{p2} for "
            f"{t2} months. Who earns the larger profit?"
        ),
        "correct": answer,
        "distractors": [o for o in options if o != answer],
        "explanation": f"Effective capitals are {w1} and {w2}; hence {answer}.",
        "verification_data": {
            "family": "ps_compare", "variant": v,
            "inputs": {"P1": p1, "T1": t1, "P2": p2, "T2": t2, "W1": w1, "W2": w2, "Answer": answer},
        },
    }


FAMILIES = [
    ps_same_time_share, ps_time_weighted_share, ps_profit_ratio,
    ps_capital_from_ratio, ps_time_from_ratio, ps_three_share,
    ps_salary_then_share, ps_join_later, ps_withdraw, ps_changing_capital,
    ps_loss_share, ps_equal_share_capital, ps_donation_then_share,
    ps_commission_then_share, ps_annual_profit, ps_capital_ratio,
    ps_two_stage, ps_share_difference, ps_time_months, ps_three_time_share,
    ps_profit_percent, ps_total_capital, ps_rejoin, ps_compare,
]


def build_partnership():
    spec = []
    for index, fn in enumerate(FAMILIES):
        part = 1 if index < 3 else 2 if index < 7 else 3 if index < 13 else 4
        difficulty = "EASY" if index < 7 else "MEDIUM" if index < 19 else "HARD"
        for variant in range(5):
            spec.append((part, difficulty, lambda r, f=fn, v=variant: f(r, v), (index % 4) + 1))
    return spec
