# -*- coding: utf-8 -*-
"""Profit and Loss (Mains) — 120 independently recomputed questions."""

from __future__ import annotations

from fractions import Fraction

from .bank import fmt
from .common import F, build_specs, money, near_num, near_pct, pct, q, ratio

SOURCE = "Profit and Loss Mains class notes (local PDF)"
PAGES = {
    1: "e6b0be93-e145-4d7c-852e-cab76407378c.pdf, pp. 4-7",
    2: "e6b0be93-e145-4d7c-852e-cab76407378c.pdf, pp. 8-11",
    3: "e6b0be93-e145-4d7c-852e-cab76407378c.pdf, pp. 12-14",
    4: "e6b0be93-e145-4d7c-852e-cab76407378c.pdf, pp. 15-16",
}


def near_money(value, step=500):
    value = F(value)
    return [money(value + step), money(value - step), money(value * 2)]


def pl_successive_discount_profit(r, v):
    mp, cost, d1, d2 = ((40000, 28000, 10, 5), (50000, 36000, 15, 10),
                        (60000, 42000, 20, 5), (72000, 50000, 25, 10),
                        (90000, 63000, 20, 15))[v]
    sp = F(mp * (100 - d1) * (100 - d2), 10000)
    profit = F((sp - cost) * 100, cost)
    return q(
        "pl_successive_discount_profit", v,
        f"An article has marked price ₹{mp} and cost ₹{cost}. Successive discounts "
        f"of {d1}% and {d2}% are given. Find the profit percent.",
        pct(profit), near_pct(profit, 2),
        f"Selling price = ₹{fmt(sp)}; profit = ₹{fmt(sp - cost)}; profit% = "
        f"{dec_safe(profit)}%.",
        {"mp": mp, "cost": cost, "d1": d1, "d2": d2},
    )


def dec_safe(value):
    text = f"{float(value):.2f}"
    return text.rstrip("0").rstrip(".")


def pl_mp_cp_ratio(r, v):
    a, b, discount = ((5, 4, 10), (7, 5, 20), (9, 7, 15), (11, 8, 25), (13, 10, 20))[v]
    profit = F(((100 - discount) * a - 100 * b) * 100, 100 * b)
    return q(
        "pl_mp_cp_ratio", v,
        f"Marked price : cost price = {a}:{b}. A discount of {discount}% is given. "
        f"Find the profit percent.",
        pct(profit), near_pct(profit, 2),
        f"Let CP = {b}x and MP = {a}x. SP = {a}x x {(100 - discount)}/100. "
        f"Profit% = {dec_safe(profit)}%.",
        {"a": a, "b": b, "discount": discount},
    )


def pl_same_sp(r, v):
    sp, profit, loss = ((24000, 20, 20), (36000, 25, 10), (48000, 30, 20),
                        (60000, 20, 25), (72000, 40, 20))[v]
    cp1 = F(sp * 100, 100 + profit)
    cp2 = F(sp * 100, 100 - loss)
    net = F((2 * sp - cp1 - cp2) * 100, cp1 + cp2)
    return q(
        "pl_same_sp", v,
        f"Two articles are sold at the same price ₹{sp}. One earns {profit}% and "
        f"the other loses {loss}%. Find the net profit or loss percent.",
        pct(net), near_pct(net, 2),
        f"CPs are ₹{fmt(cp1)} and ₹{fmt(cp2)}; total CP = ₹{fmt(cp1 + cp2)}, total "
        f"SP = ₹{2 * sp}; net = {dec_safe(net)}%.",
        {"sp": sp, "profit": profit, "loss": loss},
    )


def pl_adulteration(r, v):
    pure, added, cost, sell = ((80, 20, 50, 55), (100, 25, 60, 66),
                               (120, 30, 75, 80), (150, 50, 80, 85),
                               (200, 40, 90, 95))[v]
    total_cost = pure * cost
    revenue = (pure + added) * sell
    profit = F((revenue - total_cost) * 100, total_cost)
    return q(
        "pl_adulteration", v,
        f"A trader mixes {added} kg of free filler with {pure} kg of goods costing "
        f"₹{cost}/kg and sells the whole lot at ₹{sell}/kg. Find the profit percent.",
        pct(profit), near_pct(profit, 2),
        f"Cost = ₹{total_cost}; revenue = ₹{revenue}; profit% = {dec_safe(profit)}%.",
        {"pure": pure, "added": added, "cost": cost, "sell": sell},
    )


def pl_false_weight(r, v):
    claimed, actual, rate = ((1000, 900, 80), (1000, 850, 100), (2000, 1750, 60),
                             (5000, 4500, 120), (10000, 8750, 150))[v]
    profit = F((claimed - actual) * 100, actual)
    return q(
        "pl_false_weight", v,
        f"A dealer sells {actual} g while charging for {claimed} g at the cost "
        f"rate of ₹{rate}/kg. Find the profit percent.",
        pct(profit), near_pct(profit, 2),
        f"He receives payment for {claimed} g but parts with {actual} g. "
        f"Profit% = ({claimed}-{actual})/{actual} x 100 = {dec_safe(profit)}%.",
        {"claimed": claimed, "actual": actual, "rate": rate},
    )


def pl_free_item(r, v):
    buy, free, markup = ((4, 1, 20), (5, 1, 25), (6, 2, 30), (8, 2, 40), (9, 3, 50))[v]
    profit = F((buy * (100 + markup) - 100 * (buy + free)) * 100, 100 * (buy + free))
    return q(
        "pl_free_item", v,
        f"A scheme offers {free} free item(s) for every {buy} bought. The markup "
        f"on cost is {markup}%. Find the effective profit percent.",
        pct(profit), near_pct(profit, 2),
        f"Customer pays for {buy} units at {(100 + markup)}% of cost and receives "
        f"{buy + free}; profit% = {dec_safe(profit)}%.",
        {"buy": buy, "free": free, "markup": markup},
    )


def pl_overheads(r, v):
    base, overhead, profit = ((50000, 8, 15), (60000, 10, 20), (75000, 12, 18),
                              (90000, 15, 25), (120000, 20, 30))[v]
    sp = F(base * (100 + overhead) * (100 + profit), 10000)
    return q(
        "pl_overheads", v,
        f"An item costs ₹{base} before overheads of {overhead}%. The seller wants "
        f"{profit}% profit on the total cost. Find the selling price.",
        money(sp), near_money(sp, 2000),
        f"Effective cost = ₹{fmt(F(base * (100 + overhead), 100))}; SP = "
        f"₹{fmt(sp)}.",
        {"base": base, "overhead": overhead, "profit": profit},
    )


def pl_two_transactions(r, v):
    cost, p, loss = ((20000, 20, 10), (30000, 25, 15), (40000, 30, 20),
                     (50000, 10, 25), (60000, 15, 30))[v]
    final = F(cost * (100 + p) * (100 - loss), 10000)
    net = F((final - cost) * 100, cost)
    return q(
        "pl_two_transactions", v,
        f"A trader sells an article at {p}% profit, buys it back at that price and "
        f"sells it again at {loss}% loss. Find the net profit or loss percent on the "
        f"original cost.",
        pct(net), near_pct(net, 2),
        f"Final SP = original cost x {(100 + p)}/100 x {(100 - loss)}/100 = "
        f"₹{fmt(final)}; net = {dec_safe(net)}%.",
        {"cost": cost, "p": p, "q": loss},
    )


def pl_profit_on_sp(r, v):
    sp, p = ((40000, 20), (50000, 25), (60000, 30), (72000, 40), (90000, 50))[v]
    cost = F(sp * (100 - p), 100)
    equivalent = F(p * 100, 100 - p)
    return q(
        "pl_profit_on_sp", v,
        f"Profit is {p}% of the selling price ₹{sp}. Find the profit percent on cost.",
        pct(equivalent), near_pct(equivalent, 2),
        f"Cost = ₹{fmt(cost)}; profit = ₹{fmt(sp - cost)}; profit% on cost = "
        f"{dec_safe(equivalent)}%.",
        {"sp": sp, "p": p},
    )


def pl_equal_sp_loss(r, v):
    p = ((10, 10), (20, 20), (25, 25), (30, 30), (40, 40))[v][0]
    loss = F(p * p, 100)
    return q(
        "pl_equal_sp_loss", v,
        f"Two articles are sold at the same price, one at {p}% profit and the "
        f"other at {p}% loss. Find the net result percent.",
        pct(-loss), near_pct(-loss, 2),
        f"With equal selling prices, net loss% = p²/100 = {p}²/100 = "
        f"{dec_safe(loss)}%, written as -{dec_safe(loss)}%.",
        {"p": p},
    )


def pl_tax_invoice(r, v):
    cost, mp, discount, tax = ((30000, 40000, 10, 8), (40000, 52000, 15, 5),
                               (50000, 65000, 20, 12), (60000, 78000, 25, 6),
                               (80000, 100000, 20, 10))[v]
    sp = F(mp * (100 - discount), 100)
    profit = sp - cost
    tax_amount = F(sp * tax, 100)
    return q(
        "pl_tax_invoice", v,
        f"An invoice has cost ₹{cost}, marked price ₹{mp}, discount {discount}% and "
        f"tax {tax}% on the discounted price. Find the profit before tax.",
        money(profit), near_money(profit, 1000),
        f"Discounted price = ₹{fmt(sp)}; tax = ₹{fmt(tax_amount)} (not part of "
        f"profit); profit = ₹{fmt(profit)}.",
        {"cost": cost, "mp": mp, "discount": discount, "tax": tax},
    )


def pl_chain(r, v):
    cost, p, retail, discount = ((20000, 20, 25, 10), (30000, 15, 20, 5),
                                 (40000, 25, 20, 15), (50000, 10, 30, 10),
                                 (60000, 20, 25, 20))[v]
    final = F(cost * (100 + p) * (100 + retail) * (100 - discount), 1000000)
    profit = F((final - cost) * 100, cost)
    return q(
        "pl_chain", v,
        f"A maker sells to a retailer at {p}% profit and the retailer marks up "
        f"{retail}% before giving {discount}% discount. Starting from cost ₹{cost}, "
        f"find the overall profit percent.",
        pct(profit), near_pct(profit, 2),
        f"Final price = ₹{fmt(final)}; profit% = {dec_safe(profit)}%.",
        {"cost": cost, "p": p, "q": retail, "discount": discount},
    )


def pl_wastage(r, v):
    qty, cost, waste, sell = ((100, 40, 10, 52), (200, 50, 15, 65),
                              (300, 60, 20, 78), (400, 75, 25, 100),
                              (500, 80, 30, 110))[v]
    good = F(qty * (100 - waste), 100)
    total_cost = qty * cost
    revenue = good * sell
    profit = F((revenue - total_cost) * 100, total_cost)
    return q(
        "pl_wastage", v,
        f"A merchant buys {qty} kg at ₹{cost}/kg. {waste}% is wasted and the rest "
        f"sold at ₹{sell}/kg. Find the profit percent.",
        pct(profit), near_pct(profit, 2),
        f"Good quantity = {fmt(good)} kg; revenue = ₹{fmt(revenue)}; cost = ₹{total_cost}; "
        f"profit% = {dec_safe(profit)}%.",
        {"qty": qty, "cost": cost, "waste": waste, "sell": sell},
    )


def pl_markup_target(r, v):
    cost, target, discount = ((28000, 25, 20), (36000, 30, 25), (45000, 20, 10),
                              (56000, 35, 30), (70000, 40, 20))[v]
    mp = F(cost * (100 + target), 100 - discount)
    return q(
        "pl_markup_target", v,
        f"An article costs ₹{cost}. The seller wants {target}% profit after a "
        f"{discount}% discount. Find the required marked price.",
        money(mp), near_money(mp, 2000),
        f"Required SP = ₹{fmt(F(cost * (100 + target), 100))}; MP = SP x "
        f"100/{(100 - discount)} = ₹{fmt(mp)}.",
        {"cost": cost, "target": target, "discount": discount},
    )


def pl_partial(r, v):
    x, p, loss = ((40, 20, 10), (50, 25, 15), (60, 30, 20), (75, 40, 25), (80, 15, 30))[v]
    avg = F(x * p - (100 - x) * loss, 100)
    return q(
        "pl_partial", v,
        f"{x}% of a stock is sold at {p}% profit and the rest at {loss}% loss. Find "
        f"the overall profit or loss percent.",
        pct(avg), near_pct(avg, 2),
        f"Weighted result = ({x}x{p} - {(100 - x)}x{loss})/100 = {dec_safe(avg)}%.",
        {"x": x, "p": p, "q": loss},
    )


def pl_discount_series(r, v):
    mp, d1, d2, d3 = ((80000, 10, 15, 5), (90000, 20, 10, 5), (100000, 15, 20, 10),
                      (120000, 25, 10, 15), (150000, 20, 25, 20))[v]
    sp = F(mp * (100 - d1) * (100 - d2) * (100 - d3), 1000000)
    return q(
        "pl_discount_series", v,
        f"Find the selling price of an article marked ₹{mp} after successive "
        f"discounts of {d1}%, {d2}% and {d3}%.",
        money(sp), near_money(sp, 2000),
        f"SP = {mp} x {(100 - d1)}/100 x {(100 - d2)}/100 x {(100 - d3)}/100 = "
        f"₹{fmt(sp)}.",
        {"mp": mp, "d1": d1, "d2": d2, "d3": d3},
    )


def pl_changed_cost(r, v):
    sp, old_profit, rise = ((48000, 20, 10), (60000, 25, 20), (72000, 20, 25),
                            (90000, 50, 20), (105000, 40, 30))[v]
    old_cost = F(sp * 100, 100 + old_profit)
    new_cost = F(old_cost * (100 + rise), 100)
    new_profit = F((sp - new_cost) * 100, new_cost)
    return q(
        "pl_changed_cost", v,
        f"An article sold at ₹{sp} earned {old_profit}% on cost. If cost rises "
        f"{rise}% and the selling price stays the same, find the new profit percent.",
        pct(new_profit), near_pct(new_profit, 2),
        f"Old cost = ₹{fmt(old_cost)}; new cost = ₹{fmt(new_cost)}; new profit% = "
        f"{dec_safe(new_profit)}%.",
        {"sp": sp, "old_profit": old_profit, "rise": rise},
    )


def pl_equal_profit(r, v):
    p1, p2 = ((20, 30), (25, 40), (10, 25), (30, 50), (15, 35))[v]
    answer = ratio(100 + p2, 100 + p1)
    return q(
        "pl_equal_profit", v,
        f"Two articles are sold at the same price, earning {p1}% and {p2}% "
        f"respectively. Find the ratio of their cost prices.",
        answer, [ratio(100 + p1, 100 + p2), f"{p1}:{p2}", f"{100}:{p1}"],
        f"Equal SP implies CP₁:CP₂ = (100+{p2}):(100+{p1}) = {answer}.",
        {"p1": p1, "p2": p2},
    )


def pl_buy_sell_diff(r, v):
    x, a, y, b, sell = ((20, 40, 30, 60, 55), (30, 50, 40, 70, 65),
                        (40, 60, 60, 85, 80), (50, 75, 70, 100, 95),
                        (60, 80, 90, 110, 105))[v]
    total_cost = x * a + y * b
    revenue = (x + y) * sell
    profit = F((revenue - total_cost) * 100, total_cost)
    return q(
        "pl_buy_sell_diff", v,
        f"A shopkeeper buys {x} units at ₹{a} and {y} units at ₹{b}, then sells "
        f"all at ₹{sell} each. Find the profit or loss percent.",
        pct(profit), near_pct(profit, 2),
        f"Total cost = ₹{total_cost}; revenue = ₹{revenue}; result = "
        f"{dec_safe(profit)}%.",
        {"x": x, "a": a, "y": y, "b": b, "sell": sell},
    )


def pl_defective(r, v):
    n, cost, defective_pct, sell = ((100, 50, 10, 60), (200, 60, 15, 75),
                                    (300, 80, 20, 100), (400, 90, 25, 120),
                                    (500, 100, 30, 140))[v]
    good = F(n * (100 - defective_pct), 100)
    total_cost = n * cost
    revenue = good * sell
    profit = F((revenue - total_cost) * 100, total_cost)
    return q(
        "pl_defective", v,
        f"A buyer purchases {n} items at ₹{cost} each. {defective_pct}% are "
        f"defective and unsellable; the rest sell at ₹{sell} each. Find the result percent.",
        pct(profit), near_pct(profit, 2),
        f"Sellable = {fmt(good)}; revenue = ₹{fmt(revenue)}; cost = ₹{total_cost}; "
        f"result = {dec_safe(profit)}%.",
        {"n": n, "cost": cost, "defective_pct": defective_pct, "sell": sell},
    )


def pl_credit_terms(r, v):
    cash, credit, months, rate = ((40000, 44000, 12, 10), (50000, 56000, 12, 12),
                                  (60000, 66000, 6, 12), (80000, 88000, 18, 10),
                                  (100000, 112000, 12, 15))[v]
    effective_cost = F(cash * (1200 + rate * months), 1200)
    profit = F((credit - effective_cost) * 100, effective_cost)
    return q(
        "pl_credit_terms", v,
        f"Cash price is ₹{cash}; credit price after {months} months is ₹{credit}. "
        f"Money is worth {rate}% per annum simple interest. Find the seller's "
        f"effective profit percent.",
        pct(profit), near_pct(profit, 2),
        f"Effective cost after interest = ₹{fmt(effective_cost)}; profit% = "
        f"{dec_safe(profit)}%.",
        {"cash": cash, "credit": credit, "months": months, "rate": rate},
    )


def pl_quantity_discount(r, v):
    qty, price, discount, sell = ((100, 60, 10, 65), (200, 75, 15, 82),
                                  (300, 90, 20, 95), (400, 100, 25, 110),
                                  (500, 120, 10, 125))[v]
    cost = F(qty * price * (100 - discount), 100)
    revenue = qty * sell
    profit = F((revenue - cost) * 100, cost)
    return q(
        "pl_quantity_discount", v,
        f"A buyer purchases {qty} units at ₹{price} each and gets a {discount}% "
        f"quantity discount. He sells them at ₹{sell} each. Find the profit percent.",
        pct(profit), near_pct(profit, 2),
        f"Effective cost = ₹{fmt(cost)}; revenue = ₹{revenue}; profit% = "
        f"{dec_safe(profit)}%.",
        {"qty": qty, "price": price, "discount": discount, "sell": sell},
    )


def pl_mixed_margin(r, v):
    cost, markup, discount, full_pct = ((40000, 25, 20, 40), (50000, 30, 15, 60),
                                        (60000, 20, 25, 30), (80000, 40, 30, 50),
                                        (100000, 25, 10, 75))[v]
    mp = F(cost * (100 + markup), 100)
    revenue = F(mp * full_pct, 100) + F(mp * (100 - full_pct) * (100 - discount), 10000)
    profit = F((revenue - cost) * 100, cost)
    return q(
        "pl_mixed_margin", v,
        f"Goods costing ₹{cost} are marked up {markup}%. {full_pct}% is sold at "
        f"marked price and the rest at a {discount}% discount. Find the overall "
        f"profit percent.",
        pct(profit), near_pct(profit, 2),
        f"Marked price = ₹{fmt(mp)}; average revenue = ₹{fmt(revenue)}; profit% = "
        f"{dec_safe(profit)}%.",
        {"cost": cost, "markup": markup, "discount": discount, "full_pct": full_pct},
    )


def pl_reinvest(r, v):
    cost, p, loss = ((30000, 20, 10), (40000, 25, 20), (50000, 30, 25),
                     (60000, 15, 30), (80000, 40, 20))[v]
    final = F(cost * (100 + p) * (100 - loss), 10000)
    net = F((final - cost) * 100, cost)
    return q(
        "pl_reinvest", v,
        f"Capital of ₹{cost} earns {p}% profit; the entire proceeds are then "
        f"reinvested and lose {loss}%. Find the net profit or loss percent.",
        pct(net), near_pct(net, 2),
        f"Final capital = ₹{fmt(final)}; net = {dec_safe(net)}%.",
        {"cost": cost, "p": p, "q": loss},
    )


FAMILIES = [
    pl_successive_discount_profit, pl_mp_cp_ratio, pl_same_sp, pl_adulteration,
    pl_false_weight, pl_free_item, pl_overheads, pl_two_transactions,
    pl_profit_on_sp, pl_equal_sp_loss, pl_tax_invoice, pl_chain, pl_wastage,
    pl_markup_target, pl_partial, pl_discount_series, pl_changed_cost,
    pl_equal_profit, pl_buy_sell_diff, pl_defective, pl_credit_terms,
    pl_quantity_discount, pl_mixed_margin, pl_reinvest,
]


def build_profit_and_loss_mains():
    specs = build_specs(FAMILIES)
    return [(part, "HARD", fn, page) for part, _difficulty, fn, page in specs]
