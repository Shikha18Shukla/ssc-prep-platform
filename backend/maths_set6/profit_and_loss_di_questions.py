# -*- coding: utf-8 -*-
"""Profit and Loss – Data Interpretation (Prelims) — 120 self-contained questions."""

from __future__ import annotations

from fractions import Fraction

from .bank import fmt
from .common import F, build_specs, data, dec, near_num, near_pct, pct, q

SOURCE = "Profit and Loss Data Interpretation class notes (local PDF)"
PAGES = {
    1: "55742ecb-5ae3-4ad2-b6ab-0283e85516fa.pdf, pp. 4-7",
    2: "55742ecb-5ae3-4ad2-b6ab-0283e85516fa.pdf, pp. 8-10",
    3: "55742ecb-5ae3-4ad2-b6ab-0283e85516fa.pdf, pp. 12-13",
    4: "55742ecb-5ae3-4ad2-b6ab-0283e85516fa.pdf, pp. 4-13",
}


def pdl_cp_sp_table(r, v):
    cp, sp = ((400, 500), (600, 720), (800, 920), (1000, 1150), (1200, 1380))[v]
    profit = sp - cp
    block = data([("item cost price", f"₹{cp}"), ("item selling price", f"₹{sp}")])
    return q(
        "pdl_cp_sp_table", v,
        f"{block} Find the profit on the item.",
        f"₹{profit}", near_num(profit, 25),
        f"Profit = SP - CP = {sp} - {cp} = ₹{profit}.",
        {"cp": cp, "sp": sp},
    )


def pdl_profit_percent(r, v):
    cp, sp = ((500, 600), (750, 900), (1000, 1150), (1250, 1500), (1600, 1800))[v]
    profit = F((sp - cp) * 100, cp)
    block = data([("cost price", f"₹{cp}"), ("selling price", f"₹{sp}")])
    return q(
        "pdl_profit_percent", v,
        f"{block} Find the profit percent.",
        pct(profit), near_pct(profit, 2),
        f"Profit = ₹{sp - cp}; profit% = ({sp - cp}/{cp}) x 100 = {dec(profit)}%.",
        {"cp": cp, "sp": sp},
    )


def pdl_discount(r, v):
    mp, sp = ((500, 450), (800, 720), (1000, 900), (1200, 1080), (1500, 1350))[v]
    discount = F((mp - sp) * 100, mp)
    block = data([("marked price", f"₹{mp}"), ("selling price", f"₹{sp}")])
    return q(
        "pdl_discount", v,
        f"{block} Find the discount percent.",
        pct(discount), near_pct(discount, 2),
        f"Discount = ₹{mp - sp}; discount% = ({mp - sp}/{mp}) x 100 = {dec(discount)}%.",
        {"mp": mp, "sp": sp},
    )


def pdl_total_profit(r, v):
    items = (((100, 120), (200, 230), (300, 360)),
             ((150, 180), (250, 290), (350, 420)),
             ((200, 240), (400, 460), (500, 575)),
             ((250, 300), (350, 400), (450, 525)),
             ((300, 360), (500, 575), (700, 805)))[v]
    total = sum(sp - cp for cp, sp in items)
    block = data([(f"item {idx} CP", f"₹{cp}") for idx, (cp, _sp) in enumerate(items, 1)]
                 + [(f"item {idx} SP", f"₹{sp}") for idx, (_cp, sp) in enumerate(items, 1)])
    return q(
        "pdl_total_profit", v,
        f"{block} Find the total profit.",
        f"₹{total}", near_num(total, 25),
        f"Profits are {', '.join(str(sp - cp) for cp, sp in items)}; total = ₹{total}.",
        {"items": [[cp, sp] for cp, sp in items]},
    )


def pdl_avg_profit(r, v):
    profits = ((20, 30, 40), (25, 35, 45), (40, 50, 60), (50, 70, 90), (60, 80, 100))[v]
    avg = F(sum(profits), len(profits))
    block = data([("item 1 profit", f"₹{profits[0]}"), ("item 2 profit", f"₹{profits[1]}"),
                  ("item 3 profit", f"₹{profits[2]}")])
    return q(
        "pdl_avg_profit", v,
        f"{block} Find the average profit per item.",
        f"₹{fmt(avg)}", near_num(avg, 5),
        f"Average = ({' + '.join(str(p) for p in profits)})/3 = ₹{fmt(avg)}.",
        {"profits": list(profits)},
    )


def pdl_missing_sp(r, v):
    cp, profit = ((400, 15), (600, 20), (800, 25), (1000, 10), (1200, 30))[v]
    sp = F(cp * (100 + profit), 100)
    block = data([("cost price", f"₹{cp}"), ("profit percent", f"{profit}%")])
    return q(
        "pdl_missing_sp", v,
        f"{block} Find the selling price.",
        f"₹{fmt(sp)}", near_num(sp, 25),
        f"SP = {cp} x {(100 + profit)}/100 = ₹{fmt(sp)}.",
        {"cp": cp, "profit": profit},
    )


def pdl_missing_cp(r, v):
    sp, profit = ((460, 15), (720, 20), (1000, 25), (1100, 10), (1560, 30))[v]
    cp = F(sp * 100, 100 + profit)
    block = data([("selling price", f"₹{sp}"), ("profit percent", f"{profit}%")])
    return q(
        "pdl_missing_cp", v,
        f"{block} Find the cost price.",
        f"₹{fmt(cp)}", near_num(cp, 25),
        f"CP = {sp} x 100/{(100 + profit)} = ₹{fmt(cp)}.",
        {"sp": sp, "profit": profit},
    )


def pdl_loss_percent(r, v):
    cp, sp = ((500, 450), (800, 720), (1000, 900), (1200, 1080), (1500, 1350))[v]
    loss = F((cp - sp) * 100, cp)
    block = data([("cost price", f"₹{cp}"), ("selling price", f"₹{sp}")])
    return q(
        "pdl_loss_percent", v,
        f"{block} Find the loss percent.",
        pct(loss), near_pct(loss, 2),
        f"Loss = ₹{cp - sp}; loss% = ({cp - sp}/{cp}) x 100 = {dec(loss)}%.",
        {"cp": cp, "sp": sp},
    )


def pdl_mp_from_sp(r, v):
    sp, discount = ((450, 10), (720, 20), (900, 25), (1080, 10), (1350, 25))[v]
    mp = F(sp * 100, 100 - discount)
    block = data([("selling price", f"₹{sp}"), ("discount percent", f"{discount}%")])
    return q(
        "pdl_mp_from_sp", v,
        f"{block} Find the marked price.",
        f"₹{fmt(mp)}", near_num(mp, 25),
        f"MP = {sp} x 100/{(100 - discount)} = ₹{fmt(mp)}.",
        {"sp": sp, "discount": discount},
    )


def pdl_discount_amount(r, v):
    mp, discount = ((600, 10), (900, 20), (1200, 25), (1500, 30), (1800, 15))[v]
    amount = F(mp * discount, 100)
    block = data([("marked price", f"₹{mp}"), ("discount percent", f"{discount}%")])
    return q(
        "pdl_discount_amount", v,
        f"{block} Find the discount amount.",
        f"₹{fmt(amount)}", near_num(amount, 25),
        f"Discount = {mp} x {discount}/100 = ₹{fmt(amount)}.",
        {"mp": mp, "discount": discount},
    )


def pdl_profit_ratio(r, v):
    p1, p2 = ((100, 150), (150, 200), (200, 300), (250, 400), (300, 500))[v]
    from math import gcd
    g = gcd(p1, p2)
    answer = f"{p1 // g}:{p2 // g}"
    block = data([("shop A profit", f"₹{p1}"), ("shop B profit", f"₹{p2}")])
    return q(
        "pdl_profit_ratio", v,
        f"{block} Find the ratio of shop A's profit to shop B's profit.",
        answer, [f"{p2 // g}:{p1 // g}", f"{p1}:{p2 + 1}", f"{p1 + 1}:{p2}"],
        f"Ratio = {p1}:{p2} = {answer}.",
        {"p1": p1, "p2": p2},
    )


def pdl_share_of_total(r, v):
    p1, p2 = ((100, 300), (150, 350), (200, 600), (250, 750), (300, 900))[v]
    share = F(p1 * 100, p1 + p2)
    block = data([("shop A profit", f"₹{p1}"), ("shop B profit", f"₹{p2}")])
    return q(
        "pdl_share_of_total", v,
        f"{block} What percentage of total profit came from shop A?",
        pct(share), near_pct(share, 2),
        f"A's share = {p1}/({p1}+{p2}) x 100 = {dec(share)}%.",
        {"p1": p1, "p2": p2},
    )


def pdl_wholesale(r, v):
    cp, profit = ((1000, 10), (1500, 12), (2000, 15), (2500, 20), (3000, 25))[v]
    sp = F(cp * (100 + profit), 100)
    block = data([("wholesale cost", f"₹{cp}"), ("profit percent", f"{profit}%")])
    return q(
        "pdl_wholesale", v,
        f"{block} Find the selling price.",
        f"₹{fmt(sp)}", near_num(sp, 50),
        f"SP = {cp} x {(100 + profit)}/100 = ₹{fmt(sp)}.",
        {"cp": cp, "profit": profit},
    )


def pdl_equal_cp(r, v):
    cp, p1, p2 = ((500, 10, 20), (600, 15, 25), (800, 20, 30), (1000, 10, 30), (1200, 25, 15))[v]
    total = F(cp * (p1 + p2), 100)
    block = data([("cost of each item", f"₹{cp}"), ("profit on item 1", f"{p1}%"),
                  ("profit on item 2", f"{p2}%")])
    return q(
        "pdl_equal_cp", v,
        f"{block} Find the total profit on both items.",
        f"₹{fmt(total)}", near_num(total, 25),
        f"Profits = ₹{fmt(F(cp * p1, 100))} and ₹{fmt(F(cp * p2, 100))}; total = ₹{fmt(total)}.",
        {"cp": cp, "p1": p1, "p2": p2},
    )


def pdl_sequence(r, v):
    cp, p, loss = ((400, 10, 5), (600, 15, 10), (800, 20, 15), (1000, 25, 20), (1200, 10, 20))[v]
    final = F(cp * (100 + p) * (100 - loss), 10000)
    block = data([("initial cost", f"₹{cp}"), ("first change", f"+{p}%"),
                  ("second change", f"-{loss}%")])
    return q(
        "pdl_sequence", v,
        f"{block} Find the final value.",
        f"₹{fmt(final)}", near_num(final, 25),
        f"Final = {cp} x {(100 + p)}/100 x {(100 - loss)}/100 = ₹{fmt(final)}.",
        {"cp": cp, "p": p, "q": loss},
    )


def pdl_markup(r, v):
    cp, markup = ((500, 20), (700, 25), (900, 30), (1100, 40), (1500, 50))[v]
    mp = F(cp * (100 + markup), 100)
    block = data([("cost price", f"₹{cp}"), ("markup percent", f"{markup}%")])
    return q(
        "pdl_markup", v,
        f"{block} Find the marked price.",
        f"₹{fmt(mp)}", near_num(mp, 25),
        f"MP = {cp} x {(100 + markup)}/100 = ₹{fmt(mp)}.",
        {"cp": cp, "markup": markup},
    )


def pdl_tax(r, v):
    sp, tax = ((500, 5), (800, 8), (1000, 10), (1200, 12), (1500, 15))[v]
    total = F(sp * (100 + tax), 100)
    block = data([("selling price before tax", f"₹{sp}"), ("tax percent", f"{tax}%")])
    return q(
        "pdl_tax", v,
        f"{block} Find the amount paid including tax.",
        f"₹{fmt(total)}", near_num(total, 25),
        f"Total = {sp} x {(100 + tax)}/100 = ₹{fmt(total)}.",
        {"sp": sp, "tax": tax},
    )


def pdl_quantity(r, v):
    units, profit_each = ((20, 15), (30, 20), (40, 25), (50, 30), (60, 40))[v]
    total = units * profit_each
    block = data([("units sold", units), ("profit per unit", f"₹{profit_each}")])
    return q(
        "pdl_quantity", v,
        f"{block} Find the total profit.",
        f"₹{total}", near_num(total, 50),
        f"Total profit = {units} x {profit_each} = ₹{total}.",
        {"units": units, "profit_each": profit_each},
    )


def pdl_shop_compare(r, v):
    p1, p2 = ((500, 450), (600, 660), (750, 800), (900, 810), (1200, 1320))[v]
    diff = abs(p1 - p2)
    block = data([("shop A profit", f"₹{p1}"), ("shop B profit", f"₹{p2}")])
    return q(
        "pdl_shop_compare", v,
        f"{block} Find the difference between the two profits.",
        f"₹{diff}", near_num(diff, 25),
        f"Difference = |{p1} - {p2}| = ₹{diff}.",
        {"p1": p1, "p2": p2},
    )


def pdl_graph(r, v):
    cp, sp = ((200, 250), (300, 360), (400, 460), (500, 600), (600, 690))[v]
    profit = F((sp - cp) * 100, cp)
    block = data([("bar 1 cost price", f"₹{cp}"), ("bar 2 selling price", f"₹{sp}")])
    return q(
        "pdl_graph", v,
        f"{block} Find the profit percent.",
        pct(profit), near_pct(profit, 2),
        f"Profit = ₹{sp - cp}; profit% = {dec(profit)}%.",
        {"cp": cp, "sp": sp},
    )


def pdl_caselet(r, v):
    sales, profit_pct = ((12000, 10), (15000, 20), (18000, 15), (24000, 25), (30000, 20))[v]
    cost = F(sales * 100, 100 + profit_pct)
    block = data([("total sales", f"₹{sales}"), ("profit percent on cost", f"{profit_pct}%")])
    return q(
        "pdl_caselet", v,
        f"{block} Find the total cost price.",
        f"₹{fmt(cost)}", near_num(cost, 500),
        f"Cost = sales x 100/{(100 + profit_pct)} = ₹{fmt(cost)}.",
        {"sales": sales, "profit_pct": profit_pct},
    )


def pdl_discount_profit(r, v):
    mp, discount, cp = ((600, 10, 500), (800, 20, 600), (1000, 25, 700),
                        (1200, 30, 800), (1500, 20, 1100))[v]
    sp = F(mp * (100 - discount), 100)
    profit = F((sp - cp) * 100, cp)
    block = data([("marked price", f"₹{mp}"), ("discount", f"{discount}%"),
                  ("cost price", f"₹{cp}")])
    return q(
        "pdl_discount_profit", v,
        f"{block} Find the profit percent.",
        pct(profit), near_pct(profit, 2),
        f"SP = ₹{fmt(sp)}; profit% = {dec(profit)}%.",
        {"mp": mp, "discount": discount, "cp": cp},
    )


def pdl_percent_of_sales(r, v):
    cp, sp = ((400, 500), (600, 750), (800, 1000), (1000, 1200), (1500, 1800))[v]
    share = F((sp - cp) * 100, sp)
    block = data([("cost price", f"₹{cp}"), ("selling price", f"₹{sp}")])
    return q(
        "pdl_percent_of_sales", v,
        f"{block} What percentage of the selling price is profit?",
        pct(share), near_pct(share, 2),
        f"Profit = ₹{sp - cp}; share of SP = ({sp - cp}/{sp}) x 100 = {dec(share)}%.",
        {"cp": cp, "sp": sp},
    )


def pdl_statement(r, v):
    rates = ((10, 15, 12, 18), (20, 25, 15, 22), (12, 18, 25, 30),
             (5, 10, 8, 12), (25, 20, 30, 15))[v]
    threshold = 15
    count = sum(1 for rate in rates if rate > threshold)
    block = data([("item A profit%", rates[0]), ("item B profit%", rates[1]),
                  ("item C profit%", rates[2]), ("item D profit%", rates[3])])
    return q(
        "pdl_statement", v,
        f"{block} How many items have profit percent greater than {threshold}%?",
        fmt(count), near_num(count, 1),
        f"Comparing each value with {threshold}%, {count} item(s) qualify.",
        {"rates": list(rates)},
    )


FAMILIES = [
    pdl_cp_sp_table, pdl_profit_percent, pdl_discount, pdl_total_profit,
    pdl_avg_profit, pdl_missing_sp, pdl_missing_cp, pdl_loss_percent,
    pdl_mp_from_sp, pdl_discount_amount, pdl_profit_ratio, pdl_share_of_total,
    pdl_wholesale, pdl_equal_cp, pdl_sequence, pdl_markup, pdl_tax,
    pdl_quantity, pdl_shop_compare, pdl_graph, pdl_caselet, pdl_discount_profit,
    pdl_percent_of_sales, pdl_statement,
]


def build_profit_and_loss_di():
    specs = build_specs(FAMILIES)
    return [
        (part, "EASY" if index // 5 < 7 else "MEDIUM", fn, page)
        for index, (part, _difficulty, fn, page) in enumerate(specs)
    ]
