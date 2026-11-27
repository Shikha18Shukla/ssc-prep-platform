# -*- coding: utf-8 -*-
"""Mixture and Alligation - 120 verified questions for the third Maths batch."""

from __future__ import annotations

import math
from fractions import Fraction

from .bank import fmt_dec, near_ints, near_values

SOURCE = "Mixture and Alligation class notes and mains topic-wise sets (local PDFs)"
PAGES = {
    1: "Mains Topic wise Mixture and Alligation Set 1, pp. 1-8",
    2: "Mains Topic wise Mixture and Alligation Set 2, pp. 1-12",
    3: "Mains Topic wise Mixture and Alligation Set 3, pp. 1-8",
    4: "Mains Topic wise Mixture and Alligation Set 4, pp. 1-7",
}

ITEMS = [
    ("rice varieties", "a grocer"), ("oils", "a trader"),
    ("tea leaves", "a shopkeeper"), ("milk and water", "a dairy"),
    ("sugar solutions", "a vendor"), ("pulses", "a merchant"),
    ("coffee powders", "a cafe owner"), ("fruit juices", "a stall owner"),
    ("wheat lots", "a buyer"), ("chemical solutions", "a lab assistant"),
]


def who(v):
    return ITEMS[v % len(ITEMS)]


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


def mix_alligation_ratio(r, v):
    subject, person = who(v)
    cheap = r.choice([20, 30, 40, 50])
    mean = cheap + r.choice([5, 8, 10, 12])
    dear = mean + r.choice([6, 10, 12, 15])
    answer = ratio_str(dear - mean, mean - cheap)
    text = (
        f"{person} mixes two {subject} costing Rs.{cheap} and Rs.{dear} per kg "
        f"to get a mixture worth Rs.{mean} per kg. In what ratio are they mixed?"
    )
    return q(
        "mix_alligation_ratio", v, text, answer,
        [ratio_str(mean - cheap, dear - mean), f"{dear - mean + 1}:{mean - cheap}", "1:1"],
        f"Alligation gives cheap:dear = ({dear}-{mean}):({mean}-{cheap}) = {answer}.",
        {"C": cheap, "D": dear, "M": mean},
    )


def mix_quantity_cheaper(r, v):
    subject, person = who(v + 1)
    cheap, dear, total = r.choice([(20, 50, 90), (30, 60, 120), (40, 70, 150), (25, 45, 140)])
    mean = r.choice([30, 40, 50])
    if not cheap < mean < dear:
        mean = (cheap + dear) // 2
    cq = Fraction(total * (dear - mean), dear - cheap)
    if cq.denominator != 1:
        return None
    text = (
        f"{person} wants {total} kg of a mixture of {subject} worth Rs.{mean}/kg "
        f"using Rs.{cheap}/kg and Rs.{dear}/kg material. How many kg of the cheaper "
        "variety are needed?"
    )
    return q(
        "mix_quantity_cheaper", v, text, cq.numerator, near_ints(cq.numerator, r, 8),
        f"Ratio cheap:dear = ({dear}-{mean}):({mean}-{cheap}); cheaper quantity = {total} x ({dear}-{mean})/({dear}-{cheap}) = {cq.numerator} kg.",
        {"C": cheap, "D": dear, "M": mean, "Total": total},
    )


def mix_quantity_dearer(r, v):
    subject, person = who(v + 2)
    cheap, dear, total = r.choice([(20, 50, 90), (30, 60, 120), (40, 70, 150), (25, 45, 140)])
    mean = (cheap + dear) // 2
    dq = Fraction(total * (mean - cheap), dear - cheap)
    if dq.denominator != 1:
        return None
    text = (
        f"A {total} kg mixture of {subject} worth Rs.{mean}/kg is made from "
        f"Rs.{cheap}/kg and Rs.{dear}/kg stocks. How much of the costlier variety "
        f"does {person} use?"
    )
    return q(
        "mix_quantity_dearer", v, text, dq.numerator, near_ints(dq.numerator, r, 8),
        f"Dearer quantity = {total} x ({mean}-{cheap})/({dear}-{cheap}) = {dq.numerator} kg.",
        {"C": cheap, "D": dear, "M": mean, "Total": total},
    )


def mix_mean_price(r, v):
    subject, person = who(v + 3)
    q1 = r.choice([10, 20, 30, 40])
    q2 = r.choice([10, 20, 30, 40])
    p1 = r.choice([20, 30, 40, 50])
    p2 = r.choice([60, 70, 80, 90])
    mean = Fraction(q1 * p1 + q2 * p2, q1 + q2)
    answer = dec(mean)
    text = (
        f"{person} blends {q1} kg of {subject} at Rs.{p1}/kg with {q2} kg at "
        "Rs.{p2}/kg. What is the average cost per kg?"
    )
    return q(
        "mix_mean_price", v, text, answer, near_values(answer, r, 5),
        f"Mean price = ({q1}x{p1} + {q2}x{p2})/({q1}+{q2}) = {answer}.",
        {"Q1": q1, "Q2": q2, "P1": p1, "P2": p2},
    )


def mix_milk_water_ratio(r, v):
    milk = r.choice([20, 30, 40, 50])
    water = r.choice([10, 15, 20, 25])
    total = r.choice([60, 80, 100, 120])
    mq = Fraction(total * milk, milk + water)
    qty = dec(mq)
    subject, person = who(v)
    text = (
        f"In {person}'s {total}-litre {subject} vessel, milk and water are in the "
        f"ratio {milk}:{water}. How many litres of milk does it contain?"
    )
    return q(
        "mix_milk_water_ratio", v, text, qty, near_values(qty, r, 4),
        f"Milk quantity = {total} x {milk}/({milk}+{water}) = {qty} litres.",
        {"M": milk, "W": water, "Total": total, "Qty": qty},
    )


def mix_replace_fraction(r, v):
    total = r.choice([40, 60, 80, 100])
    milk_frac = Fraction(r.choice([1, 2, 3]), 4)
    remove = Fraction(total, r.choice([4, 5, 10]))
    milk_left = (total - remove) * milk_frac
    answer = dec(milk_left)
    subject, person = who(v + 1)
    text = (
        f"For {person}, a {total}-litre {subject} mixture has {milk_frac} milk. "
        f"{dec(remove)} litres are drawn off and replaced with water. How many "
        "litres of milk remain?"
    )
    return q(
        "mix_replace_fraction", v, text, answer, near_values(answer, r, 5),
        f"Fraction removed is uniform, so milk left = ({total} - {dec(remove)}) x {milk_frac} = {answer} litres.",
        {"Total": total, "F": str(milk_frac), "R": str(remove)},
    )


def mix_replace_twice(r, v):
    presets = [(80, Fraction(3, 4), 20), (100, Fraction(4, 5), 25), (120, Fraction(2, 3), 30)]
    total, frac, remove = presets[v % len(presets)]
    keep = Fraction(total - remove, total)
    milk = Fraction(total) * frac * keep * keep
    answer = dec(milk)
    subject, person = who(v)
    text = (
        f"For {person}, a {total}-litre vessel of {subject} contains milk worth {frac} of its volume. "
        f"{remove} litres are replaced by water, and the process is repeated once. "
        "How much milk is left?"
    )
    return q(
        "mix_replace_twice", v, text, answer, near_values(answer, r, 6),
        f"Retention factor each time = ({total}-{remove})/{total}; milk after two replacements = {total} x {frac} x ({keep})^2 = {answer} litres.",
        {"Total": total, "F": str(frac), "R": remove},
    )


def mix_add_water(r, v):
    presets = [(40, 3, 1, 2, 1), (60, 4, 1, 3, 1), (80, 5, 2, 3, 2)]
    total, m, w, nm, nw = presets[v % len(presets)]
    milk = Fraction(total * m, m + w)
    water = total - milk
    add = Fraction(milk * nw, nm) - water
    answer = dec(add)
    subject, person = who(v + 1)
    text = (
        f"A {total}-litre {subject} mixture prepared by {person} has milk:water = {m}:{w}. How many litres of "
        f"water must be added to make the ratio {nm}:{nw}?"
    )
    return q(
        "mix_add_water", v, text, answer, near_values(answer, r, 5),
        f"Milk fixed at {milk} litres; final water needed = {milk} x {nw}/{nm}; water to add = {answer} litres.",
        {"Total": total, "M": m, "W": w, "NM": nm, "NW": nw},
    )


def mix_add_milk(r, v):
    presets = [(40, 1, 3, 1, 1), (60, 1, 4, 1, 2), (80, 2, 3, 1, 1)]
    total, m, w, nm, nw = presets[v % len(presets)]
    milk = Fraction(total * m, m + w)
    water = total - milk
    add = Fraction(water * nm, nw) - milk
    answer = dec(add)
    subject, person = who(v + 2)
    text = (
        f"In {person}'s {total} litres of a milk-water {subject} mixture the ratio is {m}:{w}. "
        f"How much milk should be added to make it {nm}:{nw}?"
    )
    return q(
        "mix_add_milk", v, text, answer, near_values(answer, r, 5),
        f"Water fixed at {water} litres; final milk needed = {water} x {nm}/{nw}; milk to add = {answer} litres.",
        {"Total": total, "M": m, "W": w, "NM": nm, "NW": nw},
    )


def mix_two_vessels(r, v):
    presets = [(20, 3, 1, 20, 1, 1), (30, 2, 1, 30, 3, 1), (40, 4, 1, 40, 1, 2)]
    q1, m1, w1, q2, m2, w2 = presets[v % len(presets)]
    milk = Fraction(q1 * m1, m1 + w1) + Fraction(q2 * m2, m2 + w2)
    water = q1 + q2 - milk
    answer = ratio_str(milk, water)
    subject, person = who(v + 3)
    text = (
        f"For {person}, {q1} litres from a vessel with milk:water = {m1}:{w1} is mixed with "
        f"{q2} litres from another vessel with ratio {m2}:{w2}. Find the final "
        "milk-to-water ratio."
    )
    return q(
        "mix_two_vessels", v, text, answer,
        [ratio_str(water, milk), f"{m1+m2}:{w1+w2}", "1:1"],
        f"Milk = {milk} litres and water = {water} litres, giving {answer}.",
        {"Q1": q1, "M1": m1, "W1": w1, "Q2": q2, "M2": m2, "W2": w2},
    )


def mix_concentration_percent(r, v):
    presets = [(50, 20, 30), (80, 25, 40), (100, 15, 60), (60, 30, 30), (120, 10, 80)]
    total, pct, water = presets[v % len(presets)]
    solute = Fraction(total * pct, 100)
    strength = Fraction(solute * 100, total + water)
    answer = dec(strength)
    subject, person = who(v + 2)
    text = (
        f"For {person}, a {total}-litre {subject} solution is {pct}% solute. "
        f"After adding {water} litres of water, what is the new concentration?"
    )
    return q(
        "mix_concentration_percent", v, text, answer + "%", [x + "%" for x in near_values(answer, r, 3)],
        f"Solute = {solute} litres; new volume = {total + water}; concentration = {answer}%.",
        {"Total": total, "Pct": pct, "Water": water},
    )


def mix_profit_sale(r, v):
    subject, person = who(v + 4)
    q1, p1, q2, p2, sp = r.choice([
        (20, 30, 20, 50, 44), (30, 40, 30, 60, 54), (10, 20, 30, 40, 37),
    ])
    cost = Fraction(q1 * p1 + q2 * p2, q1 + q2)
    profit = Fraction((sp - cost) * 100, cost)
    answer = dec(profit)
    text = (
        f"{person} mixes {q1} kg of {subject} costing Rs.{p1}/kg with {q2} kg "
        f"costing Rs.{p2}/kg and sells the mixture at Rs.{sp}/kg. Find the profit percent."
    )
    return q(
        "mix_profit_sale", v, text, answer + "%", [x + "%" for x in near_values(answer, r, 3)],
        f"Average cost = {dec(cost)}; profit percent = (SP - cost)/cost x 100 = {answer}%.",
        {"Q1": q1, "P1": p1, "Q2": q2, "P2": p2, "SP": sp},
    )


def mix_three_ingredients(r, v):
    subject, person = who(v + 5)
    q1, q2, q3 = r.choice([(10, 20, 30), (20, 20, 40), (15, 25, 35)])
    p1, p2, p3 = r.choice([(20, 40, 60), (30, 50, 70), (40, 60, 90)])
    mean = Fraction(q1 * p1 + q2 * p2 + q3 * p3, q1 + q2 + q3)
    answer = dec(mean)
    text = (
        f"{person} mixes {q1}, {q2} and {q3} kg of three {subject} priced at "
        f"Rs.{p1}, Rs.{p2} and Rs.{p3} per kg. What is the cost per kg of the blend?"
    )
    return q(
        "mix_three_ingredients", v, text, answer, near_values(answer, r, 5),
        f"Weighted average = ({q1}x{p1}+{q2}x{p2}+{q3}x{p3})/{q1+q2+q3} = {answer}.",
        {"Q1": q1, "Q2": q2, "Q3": q3, "P1": p1, "P2": p2, "P3": p3},
    )


def mix_water_to_milk(r, v):
    presets = [(30, 4, 1, 2), (50, 5, 1, 3), (70, 6, 1, 3), (40, 3, 1, 2), (90, 7, 1, 3)]
    total, m, w, target = presets[v % len(presets)]
    milk = Fraction(total * m, m + w)
    final_total = Fraction(milk * (target + 1), target)
    add = final_total - total
    answer = dec(add)
    subject, person = who(v + 3)
    text = (
        f"In {person}'s {total}-litre {subject} mixture, milk and water are in the "
        f"ratio {m}:{w}. How much water must be added so that milk becomes "
        f"{target}/{target+1} of the mixture?"
    )
    return q(
        "mix_water_to_milk", v, text, answer, near_values(answer, r, 5),
        f"Milk = {milk} litres; final total = {milk}/({target}/{target+1}) = {final_total}; water added = {answer} litres.",
        {"Total": total, "M": m, "W": w, "Target": target},
    )


def mix_milk_to_add(r, v):
    presets = [(40, 1, 4, 1), (60, 1, 5, 2), (80, 2, 5, 1), (50, 1, 3, 2), (100, 1, 4, 1)]
    total, m, w, target_m = presets[v % len(presets)]
    water = Fraction(total * w, m + w)
    final_milk = Fraction(water * target_m, 1)
    current_milk = total - water
    add = final_milk - current_milk
    answer = dec(add)
    subject, person = who(v + 4)
    text = (
        f"A {total}-litre {subject} mixture prepared by {person} has milk:water = "
        f"{m}:{w}. How much milk must be added to make milk:water = {target_m}:1?"
    )
    return q(
        "mix_milk_to_add", v, text, answer, near_values(answer, r, 5),
        f"Water = {water} litres; final milk needed = {final_milk}; current milk = {current_milk}; milk added = {answer} litres.",
        {"Total": total, "M": m, "W": w, "Target": target_m},
    )


def mix_price_per_kg(r, v):
    subject, person = who(v + 6)
    q1 = r.choice([15, 20, 25, 30])
    q2 = r.choice([15, 20, 25, 30])
    p1 = r.choice([30, 40, 50])
    p2 = r.choice([60, 70, 80])
    mean = Fraction(q1 * p1 + q2 * p2, q1 + q2)
    answer = dec(mean)
    text = (
        f"{person} buys {q1} kg of {subject} at Rs.{p1}/kg and {q2} kg at "
        f"Rs.{p2}/kg. What is the effective price per kg of the purchase?"
    )
    return q(
        "mix_price_per_kg", v, text, answer, near_values(answer, r, 5),
        f"Effective price = ({q1}x{p1}+{q2}x{p2})/({q1}+{q2}) = {answer}.",
        {"Q1": q1, "Q2": q2, "P1": p1, "P2": p2},
    )


def mix_ratio_from_percent(r, v):
    pct = r.choice([20, 25, 40, 60, 75])
    solute = Fraction(pct, 100)
    water = 1 - solute
    answer = ratio_str(solute, water)
    subject, person = who(v + 5)
    text = (
        f"In {person}'s {subject} solution, {pct}% is solute and the rest is water. "
        "What is the solute-to-water ratio?"
    )
    return q(
        "mix_ratio_from_percent", v, text, answer,
        [ratio_str(water, solute), f"{pct}:100", "1:1"],
        f"Solute:water = {pct}:{100-pct} = {answer}.",
        {"Pct": pct},
    )


def mix_repeated_dilution(r, v):
    presets = [(100, Fraction(1, 5), 3), (80, Fraction(1, 4), 2), (120, Fraction(1, 6), 3)]
    total, frac, times = presets[v % len(presets)]
    left = Fraction(total) * (1 - frac) ** times
    answer = dec(left)
    subject, person = who(v + 4)
    text = (
        f"For {person}, a fraction {frac} of a {total}-litre {subject} solution is replaced by water each time. "
        f"After {times} such replacements, how many litres of the original solute remain?"
    )
    return q(
        "mix_repeated_dilution", v, text, answer, near_values(answer, r, 6),
        f"Remaining solute = {total}(1 - {frac})^{times} = {answer} litres.",
        {"Total": total, "F": str(frac), "N": times},
    )


def mix_equal_mix_ratio(r, v):
    presets = [(20, 3, 1, 20, 1, 1), (30, 5, 2, 30, 2, 1), (40, 7, 3, 40, 3, 2)]
    q1, m1, w1, q2, m2, w2 = presets[v % len(presets)]
    ratio = Fraction(q1, q2)
    milk = Fraction(q1 * m1, m1 + w1) + Fraction(q2 * m2, m2 + w2)
    water = q1 + q2 - milk
    answer = ratio_str(milk, water)
    subject, person = who(v + 5)
    text = (
        f"For {person}, {subject} mixtures with milk:water ratios {m1}:{w1} and {m2}:{w2} are combined in "
        f"the quantity ratio {ratio_str(q1, q2)}. Find the final milk-to-water ratio."
    )
    return q(
        "mix_equal_mix_ratio", v, text, answer,
        [ratio_str(water, milk), f"{m1+m2}:{w1+w2}", "1:1"],
        f"Taking {q1} and {q2} litres, milk = {milk} and water = {water}; ratio = {answer}.",
        {"Q1": q1, "M1": m1, "W1": w1, "Q2": q2, "M2": m2, "W2": w2},
    )


def mix_selling_mixture(r, v):
    subject, person = who(v + 7)
    q1, p1, q2, p2, profit = r.choice([
        (20, 40, 30, 60, 20), (30, 50, 20, 70, 25), (10, 30, 40, 50, 15),
    ])
    cost = Fraction(q1 * p1 + q2 * p2, q1 + q2)
    sp = cost * Fraction(100 + profit, 100)
    answer = dec(sp)
    text = (
        f"{person} mixes {q1} litres of {subject} costing Rs.{p1}/litre with "
        f"{q2} litres costing Rs.{p2}/litre and sells at a {profit}% profit. "
        "What is the selling price per litre?"
    )
    return q(
        "mix_selling_mixture", v, text, answer, near_values(answer, r, 5),
        f"Cost per litre = {dec(cost)}; selling price = cost x (100+{profit})/100 = {answer}.",
        {"Q1": q1, "P1": p1, "Q2": q2, "P2": p2, "Profit": profit},
    )


def mix_alligation_quantity(r, v):
    subject, person = who(v + 8)
    cheap, dear, mean, cheap_qty = r.choice([
        (20, 50, 30, 60), (30, 60, 40, 75), (40, 70, 50, 80), (25, 45, 35, 50),
    ])
    dear_qty = Fraction(cheap_qty * (mean - cheap), dear - mean)
    answer = dec(dear_qty)
    text = (
        f"{person} mixes {cheap_qty} kg of {subject} costing Rs.{cheap}/kg with "
        f"some costing Rs.{dear}/kg to make the mixture worth Rs.{mean}/kg. "
        "How many kg of the dearer variety are used?"
    )
    return q(
        "mix_alligation_quantity", v, text, answer, near_values(answer, r, 6),
        f"Cheap:dear = ({dear}-{mean}):({mean}-{cheap}); dearer quantity = {cheap_qty} x ({mean}-{cheap})/({dear}-{mean}) = {answer} kg.",
        {"C": cheap, "D": dear, "M": mean, "CQ": cheap_qty},
    )


def mix_average_strength(r, v):
    presets = [(20, 30, 40, 20), (50, 25, 30, 10), (80, 15, 100, 25), (60, 40, 40, 20), (100, 10, 50, 30)]
    q1, p1, q2, p2 = presets[v % len(presets)]
    strength = Fraction(q1 * p1 + q2 * p2, q1 + q2)
    answer = dec(strength)
    subject, person = who(v + 6)
    text = (
        f"For {person}, {q1} litres of a {p1}% {subject} solution are mixed with "
        f"{q2} litres of a {p2}% solution. What is the strength percent of the "
        "mixture?"
    )
    return q(
        "mix_average_strength", v, text, answer + "%", [x + "%" for x in near_values(answer, r, 3)],
        f"Weighted strength = ({q1}x{p1}+{q2}x{p2})/({q1}+{q2}) = {answer}%.",
        {"Q1": q1, "P1": p1, "Q2": q2, "P2": p2},
    )


def mix_removed_milk(r, v):
    presets = [(60, 3, 1, 20), (80, 5, 3, 32), (100, 7, 3, 30), (90, 4, 1, 30), (120, 5, 1, 40)]
    total, m, w, remove = presets[v % len(presets)]
    milk = Fraction(total * m, m + w)
    removed = milk * Fraction(remove, total)
    answer = dec(removed)
    subject, person = who(v + 7)
    text = (
        f"From {person}'s {total}-litre {subject} mixture with milk:water = {m}:{w}, "
        f"{remove} litres are removed. How many litres of milk are taken out?"
    )
    return q(
        "mix_removed_milk", v, text, answer, near_values(answer, r, 5),
        f"Milk fraction = {m}/{m+w}; milk removed = {remove} x {m}/{m+w} = {answer} litres.",
        {"Total": total, "M": m, "W": w, "Remove": remove},
    )


def mix_compare(r, v):
    presets = [(40, 1, 1, 40, 2, 1), (60, 1, 2, 60, 2, 3), (80, 3, 1, 80, 5, 2)]
    t1, m1, w1, t2, m2, w2 = presets[v % len(presets)]
    f1 = Fraction(m1, m1 + w1)
    f2 = Fraction(m2, m2 + w2)
    answer = "First mixture" if f1 > f2 else "Second mixture" if f2 > f1 else "Both are equal"
    options = ["First mixture", "Second mixture", "Both are equal", "Cannot be determined"]
    subject, person = who(v + 6)
    return {
        "text": (
            f"For {person}, compare two {subject} milk-water mixtures: one has ratio "
            f"{m1}:{w1} and the other {m2}:{w2}. Which has the higher milk concentration?"
        ),
        "correct": answer,
        "distractors": [o for o in options if o != answer],
        "explanation": f"Milk fractions are {f1} and {f2}; hence {answer}.",
        "verification_data": {
            "family": "mix_compare", "variant": v,
            "inputs": {"M1": m1, "W1": w1, "M2": m2, "W2": w2, "F1": str(f1), "F2": str(f2)},
        },
    }


FAMILIES = [
    mix_alligation_ratio, mix_quantity_cheaper, mix_quantity_dearer, mix_mean_price,
    mix_milk_water_ratio, mix_replace_fraction, mix_replace_twice, mix_add_water,
    mix_add_milk, mix_two_vessels, mix_concentration_percent, mix_profit_sale,
    mix_three_ingredients, mix_water_to_milk, mix_milk_to_add, mix_price_per_kg,
    mix_ratio_from_percent, mix_repeated_dilution, mix_equal_mix_ratio,
    mix_selling_mixture, mix_alligation_quantity, mix_average_strength,
    mix_removed_milk, mix_compare,
]


def build_mixture_alligation():
    spec = []
    for index, fn in enumerate(FAMILIES):
        part = 1 if index < 3 else 2 if index < 7 else 3 if index < 13 else 4
        difficulty = "EASY" if index < 7 else "MEDIUM" if index < 19 else "HARD"
        for variant in range(5):
            spec.append((part, difficulty, lambda r, f=fn, v=variant: f(r, v), (index % 4) + 1))
    return spec
