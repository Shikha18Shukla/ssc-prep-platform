# -*- coding: utf-8 -*-
"""Mixture and Alligation – Data Interpretation (Prelims) — 120 questions."""

from __future__ import annotations

from .bank import fmt
from .common import (
    F,
    build_specs,
    data,
    money,
    near_num,
    near_pct,
    pct,
    q,
    ratio,
)

SOURCE = "Mixture and Alligation Data Interpretation class notes (local PDF)"
PAGES = {
    1: '66052d90-202e-454e-96d2-3f7291856dba.pdf, pp. 4-8',
    2: '66052d90-202e-454e-96d2-3f7291856dba.pdf, pp. 9-10',
    3: '66052d90-202e-454e-96d2-3f7291856dba.pdf, pp. 11-12',
    4: '66052d90-202e-454e-96d2-3f7291856dba.pdf, pp. 4-12',
}


def _ratio_distractors(answer: str) -> list[str]:
    first, second = answer.split(":")
    return [f"{second}:{first}", f"{int(first) + 1}:{second}", f"{first}:{int(second) + 1}"]


def mad_vessel_totals(r, v):
    x, y, p, qty, ask = (
        (40, 20, 50, 30, "total"),
        (40, 20, 50, 30, "milk"),
        (40, 20, 50, 30, "water"),
        (60, 25, 45, 35, "diff"),
        (80, 40, 60, 20, "total"),
    )[v]
    milk = x + p
    water = y + qty
    values = {"total": milk + water, "milk": milk, "water": water,
              "diff": abs(milk - water)}
    ans = values[ask]
    block = data([
        ("vessel A milk", f"{x} L"), ("vessel A water", f"{y} L"),
        ("vessel B milk", f"{p} L"), ("vessel B water", f"{qty} L"),
    ])
    prompts = {
        "total": "Find the combined volume of both vessels.",
        "milk": "Find the total quantity of milk.",
        "water": "Find the total quantity of water.",
        "diff": "Find the difference between total milk and total water.",
    }
    return q(
        "mad_vessel_totals", v, f"{block} {prompts[ask]}", fmt(ans),
        near_num(ans, 5), f"Milk = {x} + {p} = {milk} L; water = {y} + {qty} = "
        f"{water} L; requested value = {fmt(ans)} L.",
        {"x": x, "y": y, "p": p, "qty": qty, "ask": ask},
    )


def mad_component_difference(r, v):
    x, y, p, qty, ask = (
        (50, 30, 70, 20, "milk_water"),
        (50, 30, 70, 20, "between_milk"),
        (50, 30, 70, 20, "between_water"),
        (80, 40, 60, 50, "total_milk"),
        (80, 40, 60, 50, "total_water"),
    )[v]
    values = {
        "milk_water": abs((x + p) - (y + qty)),
        "between_milk": abs(x - p),
        "between_water": abs(y - qty),
        "total_milk": x + p,
        "total_water": y + qty,
    }
    ans = values[ask]
    block = data([
        ("A milk", f"{x} L"), ("A water", f"{y} L"),
        ("B milk", f"{p} L"), ("B water", f"{qty} L"),
    ])
    prompts = {
        "milk_water": "Find the difference between total milk and total water.",
        "between_milk": "Find the difference between milk quantities in the two vessels.",
        "between_water": "Find the difference between water quantities in the two vessels.",
        "total_milk": "Find the sum of milk in both vessels.",
        "total_water": "Find the sum of water in both vessels.",
    }
    return q(
        "mad_component_difference", v, f"{block} {prompts[ask]}", fmt(ans),
        near_num(ans, 5), f"Requested difference or sum computed from {x}, {y}, "
        f"{p} and {qty} gives {fmt(ans)} L.",
        {"x": x, "y": y, "p": p, "qty": qty, "ask": ask},
    )


def mad_percentage_split(r, v):
    T, m, w, ask = (
        (200, 60, 40, "milk"),
        (200, 60, 40, "water"),
        (200, 60, 40, "diff"),
        (300, 45, 55, "milk"),
        (250, 70, 30, "water"),
    )[v]
    milk = F(T * m, 100)
    water = F(T * w, 100)
    ans = milk if ask == "milk" else (water if ask == "water" else abs(milk - water))
    block = data([
        ("mixture volume", f"{T} L"), ("milk percent", f"{m}%"),
        ("water percent", f"{w}%"),
    ])
    prompts = {
        "milk": "Find the milk quantity.",
        "water": "Find the water quantity.",
        "diff": "Find the difference between milk and water quantities.",
    }
    return q(
        "mad_percentage_split", v, f"{block} {prompts[ask]}", fmt(ans),
        near_num(ans, 5), f"Milk = {T}x{m}/100 = {fmt(milk)} L; water = "
        f"{T}x{w}/100 = {fmt(water)} L; requested value = {fmt(ans)} L.",
        {"T": T, "m": m, "w": w, "ask": ask},
    )


def mad_milk_percent(r, v):
    x, y, ask = ((60, 40, "milk"), (60, 40, "water"), (90, 30, "milk"),
                 (75, 25, "water"), (120, 80, "milk"))[v]
    ans = F(100 * (x if ask == "milk" else y), x + y)
    block = data([("milk", f"{x} L"), ("water", f"{y} L")])
    prompt = "Find the milk percentage." if ask == "milk" else "Find the water percentage."
    return q(
        "mad_milk_percent", v, f"{block} {prompt}", pct(ans), near_pct(ans, 5),
        f"Total = {x} + {y} = {x + y} L; requested share = "
        f"{(x if ask == 'milk' else y)}/{x + y} x 100 = {pct(ans)}.",
        {"x": x, "y": y, "ask": ask},
    )


def mad_shop_cost_diff(r, v):
    a, b, x, y, ask = (
        (20, 25, 10, 8, "diff"),
        (20, 25, 10, 8, "A"),
        (20, 25, 10, 8, "B"),
        (30, 24, 12, 15, "total"),
        (18, 22, 20, 15, "ratio"),
    )[v]
    cost_a = F(a * x)
    cost_b = F(b * y)
    if ask == "diff":
        ans = abs(cost_a - cost_b)
    elif ask == "A":
        ans = cost_a
    elif ask == "B":
        ans = cost_b
    elif ask == "total":
        ans = cost_a + cost_b
    else:
        ans = ratio(cost_a, cost_b)
    block = data([
        ("shop A price", f"₹{a}/L"), ("shop A quantity", f"{x} L"),
        ("shop B price", f"₹{b}/L"), ("shop B quantity", f"{y} L"),
    ])
    prompts = {
        "diff": "Find the difference between the two purchase costs.",
        "A": "Find the purchase cost at shop A.",
        "B": "Find the purchase cost at shop B.",
        "total": "Find the total purchase cost.",
        "ratio": "Find the ratio of shop A cost to shop B cost.",
    }
    answer = money(ans) if ask != "ratio" else ans
    distract = near_num(ans, 50) if ask != "ratio" else _ratio_distractors(ans)
    return q(
        "mad_shop_cost_diff", v, f"{block} {prompts[ask]}", answer, distract,
        f"Shop A cost = {fmt(cost_a)}, shop B cost = {fmt(cost_b)}; requested "
        f"value = {answer}.",
        {"a": a, "b": b, "x": x, "y": y, "ask": ask},
    )


def mad_simple_alligation(r, v):
    c1, c2, t, T, ask = (
        (10, 30, 20, 100, "ratio"),
        (10, 30, 20, 100, "weak"),
        (10, 30, 20, 100, "strong"),
        (20, 50, 35, 120, "weak"),
        (15, 40, 25, 150, "strong"),
    )[v]
    weak = F(T * (c2 - t), c2 - c1)
    strong = F(T * (t - c1), c2 - c1)
    ans = ratio(c2 - t, t - c1) if ask == "ratio" else (weak if ask == "weak" else strong)
    block = data([
        ("solution A strength", f"{c1}%"), ("solution B strength", f"{c2}%"),
        ("target strength", f"{t}%"), ("mixture needed", f"{T} L"),
    ])
    prompts = {
        "ratio": "Find the mixing ratio of solution A to solution B.",
        "weak": "Find the litres of solution A needed.",
        "strong": "Find the litres of solution B needed.",
    }
    answer = ans if ask == "ratio" else fmt(ans)
    distract = _ratio_distractors(ans) if ask == "ratio" else near_num(ans, 5)
    return q(
        "mad_simple_alligation", v, f"{block} {prompts[ask]}", answer, distract,
        f"Alligation ratio = ({c2} - {t}):({t} - {c1}) = {ratio(c2 - t, t - c1)}; "
        f"for {T} L, A = {fmt(weak)} L and B = {fmt(strong)} L.",
        {"c1": c1, "c2": c2, "t": t, "T": T, "ask": ask},
    )


def mad_missing_water(r, v):
    x, T, y, z, ask = (
        (30, 80, 40, 20, "water"),
        (30, 80, 40, 20, "total_A"),
        (45, 120, 35, 25, "water"),
        (50, 125, 40, 10, "water"),
        (60, 150, 50, 30, "total_B"),
    )[v]
    water_a = T - x
    total_b = y + z
    ans = water_a if ask == "water" else (T if ask == "total_A" else total_b)
    block = data([
        ("vessel A milk", f"{x} L"), ("vessel A total", f"{T} L"),
        ("vessel B milk", f"{y} L"), ("vessel B water", f"{z} L"),
    ])
    prompts = {
        "water": "Find the missing water quantity in vessel A.",
        "total_A": "Find the total volume in vessel A.",
        "total_B": "Find the total volume in vessel B.",
    }
    return q(
        "mad_missing_water", v, f"{block} {prompts[ask]}", fmt(ans),
        near_num(ans, 5), f"Water in A = {T} - {x} = {water_a} L; total in B = "
        f"{y} + {z} = {total_b} L; requested value = {fmt(ans)} L.",
        {"x": x, "T": T, "y": y, "z": z, "ask": ask},
    )


def mad_weighted_average(r, v):
    V1, c1, V2, c2, ask = (
        (40, 20, 60, 40, "combined"),
        (40, 20, 60, 40, "solute"),
        (50, 30, 50, 50, "combined"),
        (80, 25, 40, 55, "solute"),
        (100, 15, 60, 35, "combined"),
    )[v]
    solute = F(V1 * c1 + V2 * c2, 100)
    combined = F((V1 * c1 + V2 * c2), V1 + V2)
    ans = combined if ask == "combined" else solute
    block = data([
        ("mixture A volume", f"{V1} L"), ("mixture A strength", f"{c1}%"),
        ("mixture B volume", f"{V2} L"), ("mixture B strength", f"{c2}%"),
    ])
    prompt = ("Find the combined concentration."
              if ask == "combined" else "Find the total solute quantity.")
    answer = pct(ans) if ask == "combined" else fmt(ans)
    distract = near_pct(ans, 5) if ask == "combined" else near_num(ans, 5)
    return q(
        "mad_weighted_average", v, f"{block} {prompt}", answer, distract,
        f"Solute = {fmt(solute)} L in {V1 + V2} L; concentration = "
        f"{fmt(combined)}%.",
        {"V1": V1, "c1": c1, "V2": V2, "c2": c2, "ask": ask},
    )


def mad_combined_ratio(r, v):
    a, b, V, c, d, W, ask = (
        (2, 1, 60, 1, 1, 40, "ratio"),
        (2, 1, 60, 1, 1, 40, "milk"),
        (2, 1, 60, 1, 1, 40, "water"),
        (3, 2, 100, 1, 3, 80, "ratio"),
        (1, 1, 120, 3, 1, 90, "milk"),
    )[v]
    m1 = F(V * a, a + b)
    w1 = V - m1
    m2 = F(W * c, c + d)
    w2 = W - m2
    if ask == "ratio":
        ans = ratio(m1 + m2, w1 + w2)
    elif ask == "milk":
        ans = m1 + m2
    else:
        ans = w1 + w2
    block = data([
        ("vessel A milk:water", f"{a}:{b}"), ("vessel A volume", f"{V} L"),
        ("vessel B milk:water", f"{c}:{d}"), ("vessel B volume", f"{W} L"),
    ])
    prompts = {
        "ratio": "Find the combined milk:water ratio.",
        "milk": "Find the total milk after mixing.",
        "water": "Find the total water after mixing.",
    }
    answer = ans if ask == "ratio" else fmt(ans)
    distract = _ratio_distractors(ans) if ask == "ratio" else near_num(ans, 5)
    return q(
        "mad_combined_ratio", v, f"{block} {prompts[ask]}", answer, distract,
        f"Milk = {fmt(m1)} + {fmt(m2)} = {fmt(m1 + m2)} L; water = "
        f"{fmt(w1)} + {fmt(w2)} = {fmt(w1 + w2)} L.",
        {"a": a, "b": b, "V": V, "c": c, "d": d, "W": W, "ask": ask},
    )


def mad_simple_evaporation(r, v):
    V, c, e, ask = (
        (100, 20, 20, "new_pct"),
        (100, 20, 20, "solute"),
        (150, 30, 30, "water"),
        (200, 25, 40, "new_pct"),
        (180, 15, 45, "water"),
    )[v]
    solute = F(V * c, 100)
    water = V - solute - e
    vol = V - e
    ans = F(solute * 100, vol) if ask == "new_pct" else (solute if ask == "solute" else water)
    block = data([
        ("solution volume", f"{V} L"), ("solute strength", f"{c}%"),
        ("water evaporated", f"{e} L"),
    ])
    prompts = {
        "new_pct": "Find the new solute percentage.",
        "solute": "Find the solute quantity.",
        "water": "Find the water quantity left.",
    }
    answer = pct(ans) if ask == "new_pct" else fmt(ans)
    distract = near_pct(ans, 5) if ask == "new_pct" else near_num(ans, 5)
    return q(
        "mad_simple_evaporation", v, f"{block} {prompts[ask]}", answer, distract,
        f"Solute = {V}x{c}/100 = {fmt(solute)} L; volume after evaporation = "
        f"{V} - {e} = {vol} L; strength = {pct(F(solute * 100, vol))}.",
        {"V": V, "c": c, "e": e, "ask": ask},
    )


def mad_simple_replacement(r, v):
    V, c, x, ask = (
        (100, 40, 20, "milk"),
        (100, 40, 20, "water"),
        (100, 40, 20, "pct"),
        (150, 30, 30, "milk"),
        (200, 25, 40, "water"),
    )[v]
    milk = F(c * (V - x), 100)
    water = V - milk
    ans = milk if ask == "milk" else (water if ask == "water" else F(milk * 100, V))
    block = data([
        ("jar volume", f"{V} L"), ("initial milk strength", f"{c}%"),
        ("liquid replaced with water", f"{x} L"),
    ])
    prompts = {
        "milk": "Find the milk left after replacement.",
        "water": "Find the water after replacement.",
        "pct": "Find the milk percentage after replacement.",
    }
    answer = pct(ans) if ask == "pct" else fmt(ans)
    distract = near_pct(ans, 5) if ask == "pct" else near_num(ans, 5)
    return q(
        "mad_simple_replacement", v, f"{block} {prompts[ask]}", answer, distract,
        f"Milk left = {c}x({V} - {x})/100 = {fmt(milk)} L; water = "
        f"{fmt(water)} L; milk strength = {pct(F(milk * 100, V))}.",
        {"V": V, "c": c, "x": x, "ask": ask},
    )


def mad_addition_ratio(r, v):
    x, y, m, w, ask = (
        (60, 40, 20, 10, "ratio"),
        (60, 40, 20, 10, "milk"),
        (60, 40, 20, 10, "pct"),
        (80, 40, 20, 30, "ratio"),
        (90, 60, 30, 20, "milk"),
    )[v]
    milk = x + m
    water = y + w
    ans = ratio(milk, water) if ask == "ratio" else (
        milk if ask == "milk" else F(milk * 100, milk + water)
    )
    block = data([
        ("initial milk", f"{x} L"), ("initial water", f"{y} L"),
        ("milk added", f"{m} L"), ("water added", f"{w} L"),
    ])
    prompts = {
        "ratio": "Find the new milk:water ratio.",
        "milk": "Find the milk quantity after addition.",
        "pct": "Find the milk percentage after addition.",
    }
    answer = ans if ask == "ratio" else (pct(ans) if ask == "pct" else fmt(ans))
    distract = (_ratio_distractors(ans) if ask == "ratio" else
                (near_pct(ans, 5) if ask == "pct" else near_num(ans, 5)))
    return q(
        "mad_addition_ratio", v, f"{block} {prompts[ask]}", answer, distract,
        f"After addition, milk = {x} + {m} = {milk} L and water = {y} + {w} = "
        f"{water} L, so the ratio is {ratio(milk, water)}.",
        {"x": x, "y": y, "m": m, "w": w, "ask": ask},
    )


def mad_average_cost(r, v):
    a, x, b, y, ask = (
        (40, 10, 60, 20, "avg"),
        (40, 10, 60, 20, "costA"),
        (40, 10, 60, 20, "costB"),
        (50, 12, 70, 18, "total"),
        (30, 20, 45, 15, "avg"),
    )[v]
    ca = F(a * x)
    cb = F(b * y)
    ans = (ca + cb) / (x + y) if ask == "avg" else (
        ca if ask == "costA" else (cb if ask == "costB" else ca + cb)
    )
    block = data([
        ("variety A price", f"₹{a}/kg"), ("variety A quantity", f"{x} kg"),
        ("variety B price", f"₹{b}/kg"), ("variety B quantity", f"{y} kg"),
    ])
    prompts = {
        "avg": "Find the average cost per kilogram.",
        "costA": "Find the cost of variety A.",
        "costB": "Find the cost of variety B.",
        "total": "Find the total cost of both varieties.",
    }
    return q(
        "mad_average_cost", v, f"{block} {prompts[ask]}", money(ans),
        near_num(ans, 10), f"Cost of A = ₹{fmt(ca)}; cost of B = ₹"
        f"{fmt(cb)}; total = ₹{fmt(ca + cb)} for {x + y} kg.",
        {"a": a, "x": x, "b": b, "y": y, "ask": ask},
    )


def mad_simple_profit(r, v):
    c, s, qty, ask = (
        (50, 65, 20, "profit"),
        (50, 65, 20, "revenue"),
        (50, 65, 20, "cost"),
        (60, 54, 30, "pct"),
        (80, 100, 25, "profit"),
    )[v]
    cost = F(c * qty)
    rev = F(s * qty)
    ans = (rev - cost) if ask == "profit" else (
        rev if ask == "revenue" else (cost if ask == "cost" else F((rev - cost) * 100, cost))
    )
    block = data([
        ("cost per kg", f"₹{c}"), ("selling price per kg", f"₹{s}"),
        ("quantity sold", f"{qty} kg"),
    ])
    prompts = {
        "profit": "Find the total profit.",
        "revenue": "Find the total selling price.",
        "cost": "Find the total cost.",
        "pct": "Find the profit or loss percentage.",
    }
    answer = pct(ans) if ask == "pct" else money(ans)
    distract = near_pct(ans, 5) if ask == "pct" else near_num(ans, 50)
    return q(
        "mad_simple_profit", v, f"{block} {prompts[ask]}", answer, distract,
        f"Cost = ₹{fmt(cost)}; revenue = ₹{fmt(rev)}; profit = "
        f"₹{fmt(rev - cost)}.",
        {"c": c, "s": s, "qty": qty, "ask": ask},
    )


def mad_pie_other(r, v):
    T, m, w, ask = (
        (300, 50, 30, "other"),
        (300, 50, 30, "milk"),
        (300, 50, 30, "diff"),
        (400, 40, 45, "other"),
        (240, 60, 25, "water"),
    )[v]
    milk = F(T * m, 100)
    water = F(T * w, 100)
    other = F(T * (100 - m - w), 100)
    ans = (other if ask == "other" else
           (milk if ask == "milk" else
            (water if ask == "water" else abs(milk - water))))
    block = data([
        ("pie total", f"{T} L"), ("milk sector", f"{m}%"),
        ("water sector", f"{w}%"),
    ])
    prompts = {
        "other": "Find the quantity of the remaining component.",
        "milk": "Find the milk quantity.",
        "water": "Find the water quantity.",
        "diff": "Find the difference between milk and water quantities.",
    }
    return q(
        "mad_pie_other", v, f"{block} {prompts[ask]}", fmt(ans), near_num(ans, 5),
        f"Milk = {fmt(milk)} L, water = {fmt(water)} L, remainder = "
        f"{T}x({100 - m - w})/100 = {fmt(other)} L.",
        {"T": T, "m": m, "w": w, "ask": ask},
    )


def mad_avg_percent(r, v):
    p1, p2, p3, p4, ask = (
        (20, 30, 40, 50, "avg"),
        (20, 30, 40, 50, "max"),
        (20, 30, 40, 50, "range"),
        (15, 25, 35, 45, "avg"),
        (10, 20, 30, 60, "range"),
    )[v]
    avg = F(p1 + p2 + p3 + p4, 4)
    ans = avg if ask == "avg" else (max(p1, p2, p3, p4) if ask == "max"
                                    else max(p1, p2, p3, p4) - min(p1, p2, p3, p4))
    block = data([
        ("container 1 strength", f"{p1}%"), ("container 2 strength", f"{p2}%"),
        ("container 3 strength", f"{p3}%"), ("container 4 strength", f"{p4}%"),
    ])
    prompts = {
        "avg": "Find the average strength of the four containers.",
        "max": "Find the highest strength among the containers.",
        "range": "Find the range of the strengths.",
    }
    answer = pct(ans) if ask != "range" else fmt(ans)
    distract = near_pct(ans, 5) if ask != "range" else near_num(ans, 5)
    return q(
        "mad_avg_percent", v, f"{block} {prompts[ask]}", answer, distract,
        f"Strengths are {p1}%, {p2}%, {p3}% and {p4}%; average = "
        f"({p1} + {p2} + {p3} + {p4})/4 = {pct(avg)}.",
        {"p1": p1, "p2": p2, "p3": p3, "p4": p4, "ask": ask},
    )


def mad_water_needed(r, v):
    m, w, t, ask = (
        (60, 40, 50, "water"),
        (60, 40, 50, "total"),
        (80, 40, 60, "water"),
        (90, 30, 60, "total"),
        (120, 80, 60, "water"),
    )[v]
    add = F(100 * m, t) - (m + w)
    ans = add if ask == "water" else m + w + add
    block = data([
        ("milk present", f"{m} L"), ("water present", f"{w} L"),
        ("target milk percentage", f"{t}%"),
    ])
    prompt = "Find the water to be added." if ask == "water" else "Find the final mixture volume."
    return q(
        "mad_water_needed", v, f"{block} {prompt}", fmt(ans), near_num(ans, 5),
        f"Let x L water be added: {m}/({m} + {w} + x) = {t}/100, so x = "
        f"100x{m}/{t} - {m + w} = {fmt(add)} L.",
        {"m": m, "w": w, "t": t, "ask": ask},
    )


def mad_solute_needed(r, v):
    V, c, t, ask = (
        (100, 20, 30, "solute"),
        (100, 20, 30, "final"),
        (150, 25, 40, "solute"),
        (200, 10, 20, "final"),
        (180, 15, 25, "solute"),
    )[v]
    add = F(V * (t - c), 100 - t)
    ans = add if ask == "solute" else F(V * c, 100) + add
    block = data([
        ("solution volume", f"{V} L"), ("current strength", f"{c}%"),
        ("target strength", f"{t}%"),
    ])
    prompt = ("Find the pure solute to be added." if ask == "solute"
              else "Find the final solute quantity.")
    return q(
        "mad_solute_needed", v, f"{block} {prompt}", fmt(ans), near_num(ans, 2),
        f"Initial solute = {fmt(F(V * c, 100))} kg; if x kg solute is added, "
        f"({fmt(F(V * c, 100))} + x)/({V} + x) = {t}/100, so x = {fmt(add)} kg.",
        {"V": V, "c": c, "t": t, "ask": ask},
    )


def mad_price_ratio(r, v):
    a, x, b, y, ask = (
        (60, 3, 80, 4, "ratio"),
        (60, 3, 80, 4, "A"),
        (60, 3, 80, 4, "B"),
        (90, 6, 120, 8, "ratio"),
        (40, 5, 75, 6, "B"),
    )[v]
    price_a = F(a, x)
    price_b = F(b, y)
    ans = ratio(price_a, price_b) if ask == "ratio" else (
        price_a if ask == "A" else price_b
    )
    block = data([
        ("shop A price", f"₹{a} for {x} L"),
        ("shop B price", f"₹{b} for {y} L"),
    ])
    prompts = {
        "ratio": "Find the ratio of per-litre prices of shop A and shop B.",
        "A": "Find the per-litre price at shop A.",
        "B": "Find the per-litre price at shop B.",
    }
    answer = ans if ask == "ratio" else money(ans)
    distract = _ratio_distractors(ans) if ask == "ratio" else near_num(ans, 5)
    return q(
        "mad_price_ratio", v, f"{block} {prompts[ask]}", answer, distract,
        f"Per-litre prices are ₹{fmt(price_a)} and ₹{fmt(price_b)}; their "
        f"ratio is {ratio(price_a, price_b)}.",
        {"a": a, "x": x, "b": b, "y": y, "ask": ask},
    )


def mad_caselet_half(r, v):
    x, y, p, qty, ask = (
        (60, 40, 80, 20, "ratio"),
        (60, 40, 80, 20, "milk"),
        (60, 40, 80, 20, "water"),
        (100, 60, 40, 40, "ratio"),
        (120, 40, 60, 30, "milk"),
    )[v]
    milk = F(x, 2) + p
    water = F(y, 2) + qty
    ans = ratio(milk, water) if ask == "ratio" else (milk if ask == "milk" else water)
    block = data([
        ("vessel A milk", f"{x} L"), ("vessel A water", f"{y} L"),
        ("vessel B milk", f"{p} L"), ("vessel B water", f"{qty} L"),
        ("portion of A mixed", "one-half"),
    ])
    prompts = {
        "ratio": "Find the milk:water ratio after mixing.",
        "milk": "Find the milk mixed.",
        "water": "Find the water mixed.",
    }
    answer = ans if ask == "ratio" else fmt(ans)
    distract = _ratio_distractors(ans) if ask == "ratio" else near_num(ans, 5)
    return q(
        "mad_caselet_half", v, f"{block} {prompts[ask]}", answer, distract,
        f"Half of A gives {fmt(F(x, 2))} L milk and {fmt(F(y, 2))} L water; "
        f"adding all of B gives milk = {fmt(milk)} L and water = {fmt(water)} L.",
        {"x": x, "y": y, "p": p, "qty": qty, "ask": ask},
    )


def mad_discount_total(r, v):
    m, d, qty, ask = (
        (100, 10, 20, "total"),
        (100, 10, 20, "discount"),
        (100, 10, 20, "each"),
        (150, 20, 12, "total"),
        (200, 25, 10, "discount"),
    )[v]
    each = F(m * (100 - d), 100)
    ans = each * qty if ask == "total" else (
        F(m * d * qty, 100) if ask == "discount" else each
    )
    block = data([
        ("marked price", f"₹{m}"), ("discount", f"{d}%"),
        ("quantity", f"{qty} units"),
    ])
    prompts = {
        "total": "Find the total selling price.",
        "discount": "Find the total discount.",
        "each": "Find the selling price per unit.",
    }
    return q(
        "mad_discount_total", v, f"{block} {prompts[ask]}", money(ans),
        near_num(ans, 50), f"Selling price per unit = {m}x({100 - d})/100 = "
        f"₹{fmt(each)}; for {qty} units the total is ₹{fmt(each * qty)}.",
        {"m": m, "d": d, "qty": qty, "ask": ask},
    )


def mad_alloy_copper_mass(r, v):
    x, a, y, b, ask = (
        (100, 40, 80, 60, "copper"),
        (100, 40, 80, 60, "zinc"),
        (100, 40, 80, 60, "ratio"),
        (120, 25, 90, 50, "copper"),
        (150, 30, 100, 45, "ratio"),
    )[v]
    cu = F(x * a + y * b, 100)
    zn = F(x * (100 - a) + y * (100 - b), 100)
    ans = ratio(cu, zn) if ask == "ratio" else (cu if ask == "copper" else zn)
    block = data([
        ("alloy A mass", f"{x} kg"), ("alloy A copper", f"{a}%"),
        ("alloy B mass", f"{y} kg"), ("alloy B copper", f"{b}%"),
    ])
    prompts = {
        "copper": "Find the total copper mass.",
        "zinc": "Find the total zinc mass.",
        "ratio": "Find the copper:zinc ratio in the mixed alloy.",
    }
    answer = ans if ask == "ratio" else fmt(ans)
    distract = _ratio_distractors(ans) if ask == "ratio" else near_num(ans, 5)
    return q(
        "mad_alloy_copper_mass", v, f"{block} {prompts[ask]}", answer, distract,
        f"Copper = {fmt(cu)} kg and zinc = {fmt(zn)} kg, giving ratio "
        f"{ratio(cu, zn)}.",
        {"x": x, "a": a, "y": y, "b": b, "ask": ask},
    )


def mad_double_replacement(r, v):
    V, c, x, ask = (
        (100, 40, 20, "pct"),
        (100, 40, 20, "milk"),
        (100, 40, 20, "water"),
        (120, 50, 30, "pct"),
        (150, 30, 25, "milk"),
    )[v]
    milk = F(c * (V - x) * (V - x), V * V)
    ans = milk if ask == "milk" else (V - milk if ask == "water" else milk)
    block = data([
        ("jar volume", f"{V} L"), ("initial milk strength", f"{c}%"),
        ("liquid replaced each time", f"{x} L"),
        ("number of replacements", "2"),
    ])
    prompts = {
        "pct": "Find the final milk percentage.",
        "milk": "Find the milk left after both replacements.",
        "water": "Find the water after both replacements.",
    }
    answer = pct(ans) if ask == "pct" else fmt(ans)
    distract = near_pct(ans, 5) if ask == "pct" else near_num(ans, 5)
    return q(
        "mad_double_replacement", v, f"{block} {prompts[ask]}", answer, distract,
        f"Each replacement multiplies milk by ({V} - {x})/{V}; final milk = "
        f"{c}x({V} - {x})^2/{V}^2 = {fmt(milk)} L, i.e. {pct(milk)}.",
        {"V": V, "c": c, "x": x, "ask": ask},
    )


def mad_missing_price(r, v):
    T, C, x, a, ask = (
        (100, 4800, 40, 40, "priceB"),
        (100, 4800, 40, 40, "qtyB"),
        (100, 4800, 40, 40, "costA"),
        (150, 9000, 60, 50, "priceB"),
        (200, 14000, 80, 60, "qtyB"),
    )[v]
    qty_b = T - x
    cost_a = F(x * a)
    price_b = F(C - x * a, qty_b)
    ans = price_b if ask == "priceB" else (qty_b if ask == "qtyB" else cost_a)
    block = data([
        ("total mixture", f"{T} kg"), ("total cost", f"₹{C}"),
        ("variety A quantity", f"{x} kg"), ("variety A price", f"₹{a}/kg"),
    ])
    prompts = {
        "priceB": "Find the price per kilogram of variety B.",
        "qtyB": "Find the quantity of variety B.",
        "costA": "Find the cost of variety A.",
    }
    answer = money(ans) if ask != "qtyB" else fmt(ans)
    distract = near_num(ans, 5) if ask != "qtyB" else near_num(ans, 10)
    return q(
        "mad_missing_price", v, f"{block} {prompts[ask]}", answer, distract,
        f"Variety B quantity = {T} - {x} = {qty_b} kg; its cost = ₹"
        f"{C - x * a}, so price = ₹{fmt(price_b)} per kg.",
        {"T": T, "C": C, "x": x, "a": a, "ask": ask},
    )


FAMILIES = [
    mad_vessel_totals, mad_component_difference, mad_percentage_split,
    mad_milk_percent, mad_shop_cost_diff, mad_simple_alligation,
    mad_missing_water, mad_weighted_average, mad_combined_ratio,
    mad_simple_evaporation, mad_simple_replacement, mad_addition_ratio,
    mad_average_cost, mad_simple_profit, mad_pie_other, mad_avg_percent,
    mad_water_needed, mad_solute_needed, mad_price_ratio, mad_caselet_half,
    mad_discount_total, mad_alloy_copper_mass, mad_double_replacement,
    mad_missing_price,
]


def build_mixture_alligation_di():
    return build_specs(FAMILIES, mains=False)
