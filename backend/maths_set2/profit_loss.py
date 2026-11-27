# -*- coding: utf-8 -*-
"""Profit, Loss and Discount - 120 verified questions for the second Maths batch."""

from __future__ import annotations

from fractions import Fraction

from .bank import Bank, fill, fmt_dec

SOURCE = (
    "PW Banking Wallah - Profit, Loss and Discount Class Notes; Guidely "
    "Profit&Loss Sets 1-6 (local PDFs)"
)
PAGES = {
    1: "Profit, Loss and Discount 05, pp. 3-17",
    2: "Profit, Loss and Discount 06, pp. 3-17",
    3: "Profit & Loss Set-1, pp. 2-5",
    4: "Profit & Loss Set-2, pp. 2-5",
    5: "Profit & Loss Set-3, pp. 2-6",
    6: "Profit & Loss Set-4, pp. 2-6",
    7: "Profit & Loss Set-6, pp. 2-7",
}


def near_values(correct: float, rng, spread: float = 8) -> list[str]:
    target = fmt_dec(correct, 2)
    values: list[str] = []
    while len(values) < 3:
        delta = rng.choice([-1, 1]) * rng.choice([2, 3, 5, 6, 8, 10])
        text = fmt_dec(correct + delta, 2)
        if text != target and text not in values:
            values.append(text)
    return values


def pl_profit_pct(rng):
    cp = 20 * rng.randint(10, 90)
    p = 5 * rng.randint(2, 12)
    sp = cp + cp * p // 100
    return {
        "text": f"An article bought for Rs {cp} is sold for Rs {sp}. Find the profit percentage.",
        "correct": str(p),
        "distractors": near_values(p, rng, 8),
        "explanation": (
            f"Profit = {sp} - {cp} = {sp - cp}. Profit% = ({sp - cp}/{cp}) x 100 "
            f"= {p}%."
        ),
        "verification_data": {"op": "pl_profit_pct", "cp": cp, "sp": sp},
    }


def pl_sp(rng):
    cp = 20 * rng.randint(10, 90)
    p = 5 * rng.randint(2, 14)
    answer = cp + cp * p // 100
    return {
        "text": f"Find the selling price of an article whose cost price is Rs {cp} and profit is {p}%.",
        "correct": str(answer),
        "distractors": near_values(answer, rng, 40),
        "explanation": (
            f"SP = CP x (1 + profit%/100) = {cp} x (1 + {p}/100) = {answer}."
        ),
        "verification_data": {"op": "pl_sp", "cp": cp, "p": p},
    }


def pl_cp(rng):
    cp = 20 * rng.randint(10, 90)
    p = 5 * rng.randint(2, 12)
    sp = cp + cp * p // 100
    return {
        "text": (
            f"An article is sold for Rs {sp} at a profit of {p}%. Find its cost price."
        ),
        "correct": str(cp),
        "distractors": near_values(cp, rng, 50),
        "explanation": (
            f"CP = SP x 100/(100 + profit%) = {sp} x 100/{100 + p} = {cp}."
        ),
        "verification_data": {"op": "pl_cp", "sp": sp, "p": p},
    }


def pl_discount(rng):
    mp = 20 * rng.randint(20, 90)
    d = 5 * rng.randint(2, 12)
    answer = mp - mp * d // 100
    return {
        "text": (
            f"The marked price of an item is Rs {mp} and a discount of {d}% is given. "
            f"Find the selling price."
        ),
        "correct": str(answer),
        "distractors": near_values(answer, rng, 40),
        "explanation": (
            f"SP = MP x (1 - discount%/100) = {mp} x (1 - {d}/100) = {answer}."
        ),
        "verification_data": {"op": "pl_discount", "mp": mp, "d": d},
    }


def pl_successive(rng):
    d1 = 5 * rng.randint(2, 8)
    d2 = 5 * rng.randint(2, 8)
    net = Fraction(d1) + Fraction(d2) - Fraction(d1 * d2, 100)
    return {
        "text": (
            f"Two successive discounts of {d1}% and {d2}% are given on an item. "
            f"Find the single equivalent discount."
        ),
        "correct": fmt_dec(float(net), 2) + "%",
        "distractors": [
            f"{d1 + d2}%",
            fmt_dec(float(net) + 5, 2) + "%",
            fmt_dec(float(net) - 4, 2) + "%",
        ],
        "explanation": (
            f"Equivalent discount = {d1} + {d2} - ({d1} x {d2})/100 = "
            f"{fmt_dec(float(net), 2)}%."
        ),
        "verification_data": {"op": "pl_successive", "d1": d1, "d2": d2},
    }


def pl_mp_profit(rng):
    cp = 100 * rng.randint(2, 20)
    markup = rng.choice([20, 25, 30, 40, 50, 60])
    discount = rng.choice([5, 10, 15, 20, 25])
    profit = Fraction((100 + markup) * (100 - discount), 100) - 100
    if profit <= 0:
        return None
    answer = fmt_dec(float(profit), 2)
    return {
        "text": (
            f"A trader marks his goods {markup}% above cost price and then allows a "
            f"discount of {discount}%. Find his profit percentage."
        ),
        "correct": answer,
        "distractors": [
            f"{markup - discount}",
            fmt_dec(float(profit) + 4, 2),
            fmt_dec(float(profit) - 3, 2),
        ],
        "explanation": (
            f"Let CP = 100. Then MP = {100 + markup} and SP = "
            f"{100 + markup} x {100 - discount}/100 = "
            f"{fmt_dec(float(Fraction((100 + markup) * (100 - discount), 100)), 2)}. "
            f"Profit% = {answer}%."
        ),
        "verification_data": {
            "op": "pl_mp_profit",
            "markup": markup,
            "discount": discount,
        },
    }


def pl_mp_value(rng):
    cp = 100 * rng.randint(2, 20)
    markup = rng.choice([20, 25, 30, 40, 50, 60])
    answer = cp * (100 + markup) // 100
    return {
        "text": (
            f"An article with cost price Rs {cp} is marked {markup}% above cost "
            f"price. Find its marked price."
        ),
        "correct": str(answer),
        "distractors": near_values(answer, rng, 40),
        "explanation": (
            f"MP = CP x (1 + {markup}/100) = {cp} x {100 + markup}/100 = {answer}."
        ),
        "verification_data": {"op": "pl_mp_value", "cp": cp, "markup": markup},
    }


def pl_false_weight(rng):
    true_w = 1000
    false_w = rng.randrange(700, 1000, 10)
    gain = Fraction(true_w - false_w, false_w) * 100
    return {
        "text": (
            f"A dishonest dealer sells goods using a weight of {false_w} g instead of "
            f"1 kg. Find his gain percentage."
        ),
        "correct": fmt_dec(float(gain), 2) + "%",
        "distractors": [
            fmt_dec(float(Fraction(true_w - false_w, true_w) * 100), 2) + "%",
            fmt_dec(float(gain) + 2, 2) + "%",
            fmt_dec(float(gain) - 2, 2) + "%",
        ],
        "explanation": (
            f"He charges for {true_w} g but gives {false_w} g, so the gain is "
            f"{true_w - false_w} g on an outlay of {false_w} g. Gain% = "
            f"({true_w - false_w}/{false_w}) x 100 = {fmt_dec(float(gain), 2)}%."
        ),
        "verification_data": {"op": "pl_false_weight", "true_w": true_w, "false_w": false_w},
    }


def pl_two(rng):
    p = rng.choice([10, 15, 20, 25, 30, 40])
    sp = 100 * rng.randint(3, 20)
    loss = Fraction(p * p, 100)
    return {
        "text": (
            f"Two articles are each sold for Rs {sp}, one at a profit of {p}% and the "
            f"other at a loss of {p}%. Find the overall loss percentage."
        ),
        "correct": fmt_dec(float(loss), 2) + "%",
        "distractors": [
            f"{p}%",
            f"0%",
            fmt_dec(float(loss) + 2, 2) + "%",
        ],
        "explanation": (
            f"When two articles are sold at the same price with equal profit and loss "
            f"percentages, the net result is always a loss of (p/10)^2% = "
            f"{fmt_dec(float(loss), 2)}%."
        ),
        "verification_data": {"op": "pl_two", "p": p},
    }


def pl_profit_on_sp(rng):
    p = rng.choice([5, 10, 12, 15, 20, 25, 30, 40])
    answer = Fraction(100 * p, 100 - p)
    return {
        "text": (
            f"A shopkeeper's profit is {p}% of the selling price. Find his profit "
            f"percentage on the cost price."
        ),
        "correct": fmt_dec(float(answer), 2) + "%",
        "distractors": [
            f"{p}%",
            fmt_dec(float(answer) + 4, 2) + "%",
            fmt_dec(float(answer) - 4, 2) + "%",
        ],
        "explanation": (
            f"If profit is {p}% of SP, then CP = SP - profit = {100 - p}% of SP. "
            f"Profit% on CP = {p}/{100 - p} x 100 = {fmt_dec(float(answer), 2)}%."
        ),
        "verification_data": {"op": "pl_profit_on_sp", "p": p},
    }


def pl_mp_ratio(rng):
    cp_part = rng.randint(2, 6)
    mp_part = cp_part + rng.randint(1, 5)
    profit = rng.choice([10, 20, 25, 30, 40])
    sp_part = Fraction(cp_part * (100 + profit), 100)
    if sp_part >= mp_part:
        return None
    discount = (Fraction(mp_part) - sp_part) / mp_part * 100
    return {
        "text": (
            f"The ratio of the marked price of an article to its cost price is "
            f"{mp_part}:{cp_part}. If a profit of {profit}% is made, find the discount "
            f"percentage."
        ),
        "correct": fmt_dec(float(discount), 2) + "%",
        "distractors": [
            fmt_dec(float(profit), 2) + "%",
            fmt_dec(float(discount) + 4, 2) + "%",
            fmt_dec(float(discount) - 4, 2) + "%",
        ],
        "explanation": (
            f"Let CP = {cp_part}k and MP = {mp_part}k. A {profit}% profit gives "
            f"SP = {cp_part}k x {100 + profit}/100 = "
            f"{fmt_dec(float(sp_part), 2)}k. Discount = ({mp_part} - "
            f"{fmt_dec(float(sp_part), 2)})/{mp_part} x 100 = "
            f"{fmt_dec(float(discount), 2)}%."
        ),
        "verification_data": {
            "op": "pl_mp_ratio",
            "cp_part": cp_part,
            "mp_part": mp_part,
            "profit": profit,
        },
    }


def pl_break_even(rng):
    cp = 100 * rng.randint(3, 20)
    loss = rng.choice([10, 15, 20, 25])
    sp = cp - cp * loss // 100
    gain = rng.choice([10, 20, 25, 30])
    answer = sp * (100 + gain) // (100 - loss)
    return {
        "text": (
            f"By selling an article for Rs {sp}, a shopkeeper incurs a loss of "
            f"{loss}%. At what price should he sell it to gain {gain}%?"
        ),
        "correct": str(answer),
        "distractors": near_values(answer, rng, 40),
        "explanation": (
            f"CP = {sp} x 100/{100 - loss} = {cp}. For a {gain}% gain, "
            f"SP = {cp} x {100 + gain}/100 = {answer}."
        ),
        "verification_data": {
            "op": "pl_break_even",
            "sp": sp,
            "loss": loss,
            "gain": gain,
        },
    }


def build_profit_loss() -> Bank:
    bank = Bank("Profit, Loss and Discount", "profit_loss_discount", seed=605)
    spec = [
        (1, "EASY", 4, pl_profit_pct, 3),
        (1, "EASY", 4, pl_sp, 4),
        (1, "EASY", 4, pl_discount, 5),
        (1, "EASY", 3, pl_cp, 6),
        (2, "EASY", 4, pl_profit_pct, 1),
        (2, "MEDIUM", 4, pl_sp, 2),
        (2, "MEDIUM", 4, pl_cp, 3),
        (2, "MEDIUM", 4, pl_discount, 4),
        (2, "MEDIUM", 4, pl_successive, 5),
        (3, "MEDIUM", 6, pl_mp_profit, 6),
        (3, "MEDIUM", 6, pl_successive, 7),
        (3, "HARD", 6, pl_false_weight, 1),
        (3, "HARD", 6, pl_two, 2),
        (3, "HARD", 6, pl_profit_on_sp, 3),
        (4, "HARD", 10, pl_mp_profit, 4),
        (4, "HARD", 10, pl_mp_ratio, 5),
        (4, "HARD", 10, pl_false_weight, 6),
        (4, "HARD", 10, pl_two, 7),
        (4, "HARD", 10, pl_break_even, 1),
        (4, "HARD", 5, pl_discount, 2),
    ]
    for part, difficulty, count, fn, page in spec:
        fill(bank, part, difficulty, count, fn, SOURCE, PAGES[page])
    return bank
