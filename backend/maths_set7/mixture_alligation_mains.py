# -*- coding: utf-8 -*-
"""Mixture and Alligation (Mains) — 120 original HARD, multi-step questions."""

from __future__ import annotations

from fractions import Fraction as _Fraction

from .bank import fmt
from .common import (
    F,
    build_specs,
    money,
    near_num,
    near_pct,
    pct,
    q,
    ratio,
)

SOURCE = "Mixture and Alligation Mains class notes (local PDF)"
PAGES = {
    1: '36c4c768-3fbf-4ae7-8b96-debff3f16eec.pdf, pp. 4-6',
    2: '36c4c768-3fbf-4ae7-8b96-debff3f16eec.pdf, pp. 7-9',
    3: '36c4c768-3fbf-4ae7-8b96-debff3f16eec.pdf, pp. 10-12',
    4: '36c4c768-3fbf-4ae7-8b96-debff3f16eec.pdf, pp. 4-12',
}


def _ratio_distractors(answer: str) -> list[str]:
    first, second = answer.split(":")
    return [f"{second}:{first}", f"{int(first) + 1}:{second}", f"{first}:{int(second) + 1}"]


def _explain(note: str, answer: str) -> str:
    return f"{note} Working through the stages in order, the requested value is {answer}."


def _raw(answer: str):
    """Recover a numeric Fraction from a formatted answer string."""
    return _Fraction(str(answer).replace("₹", "").rstrip("%"))


def _distractors_for(answer: str) -> list[str]:
    if answer.startswith("₹"):
        return near_num(_raw(answer), 100)
    if answer.endswith("%"):
        return near_pct(_raw(answer), 5)
    if ":" in answer:
        return _ratio_distractors(answer)
    return near_num(_raw(answer), 2)


# ---------------------------------------------------------------------------
# 1. Repeated draw-offs with intermediate charging, boiling and back-calc.
# ---------------------------------------------------------------------------
def _solve_replacement_chain(x):
    V = x["V"]
    sol = F(V * x["c"], 100)
    for d, r in ((x["d1"], x["r1"]), (x["d2"], x["r2"]), (x["d3"], x["r3"])):
        if d:
            sol = sol * (V - d) / V + F(d * r, 100)
    sol += x["s"]
    vol = V - x["w"] + x["s"]
    if x["ask"] == "target":
        return fmt(F(x["t"] * vol - 100 * sol, 100 - x["t"]))
    return pct(F(sol * 100, vol))


def mam_replacement_chain(r, v):
    rows = (
        (180, 55, 45, 20, 60, 80, 0, 0, 0, 0, 0, "final"),
        (240, 40, 60, 0, 80, 75, 0, 0, 18, 30, 0, "final"),
        (200, 60, 50, 0, 50, 40, 0, 0, 0, 0, 70, "target"),
        (300, 35, 60, 10, 75, 60, 45, 0, 0, 20, 0, "final"),
        (150, 48, 30, 90, 50, 0, 0, 0, 12, 10, 0, "final"),
    )
    (V, c, d1, r1, d2, r2, d3, r3, s, w, t, ask) = rows[v]
    x = {"V": V, "c": c, "d1": d1, "r1": r1, "d2": d2, "r2": r2,
         "d3": d3, "r3": r3, "s": s, "w": w, "t": t, "ask": ask}
    ans = _solve_replacement_chain(x)
    texts = (
        f"An assay vat holds {V} L of {c}% acid. {d1} L is drawn off and charged with a {r1}% "
        f"solution, then {d2} L is drawn off and charged with an {r2}% solution. Find the final strength.",
        f"A reactor holds {V} L of {c}% brine. {d1} L is withdrawn and made up with water, "
        f"{d2} L is then withdrawn and made up with {r2}% brine, {w} L of water is boiled off "
        f"and {s} kg of salt is dissolved. Find the final solute percent.",
        f"From {V} L of a {c}% solution, {d1} L is replaced by water and then {d2} L is replaced "
        f"by a {r2}% solution. How many litres of pure solute must be added to reach {t}% strength?",
        f"A {V} L processing tank starts at {c}%. Three draw-offs follow: {d1} L replaced with "
        f"{r1}%, {d2} L with {r2}% and {d3} L with water; then {w} L evaporates. Find the final concentration.",
        f"A {V} L batch is {c}% solute. {d1} L is swapped for a {r1}% solution and {d2} L for "
        f"water; next {s} kg solute is added and {w} L evaporates. Find the final percent.",
    )
    notes = (
        "Two successive draw-off-and-charge operations change the solute before the strength is read.",
        "Two replacements are followed by evaporation and a salt addition.",
        "After two replacements the missing pure solute is solved from a final-strength equation.",
        "Three different replacement liquids act in sequence, followed by evaporation.",
        "A replacement pair is followed by salt addition and evaporation.",
    )
    return q("mam_replacement_chain", v, texts[v], ans,
             _distractors_for(ans),
             _explain(notes[v], ans), x)


# ---------------------------------------------------------------------------
# 2. Three stock solutions, withdrawal cycle and comparison / back-calc.
# ---------------------------------------------------------------------------
def _solve_three_solution_mix(x):
    vol0 = x["a"] + x["b"] + x["c"]
    solute = F(x["a"] * x["c1"] + x["b"] * x["c2"] + x["c"] * x["c3"], 100)
    vol = vol0 + x["y"] - x["e"]
    solute = solute * (vol0 - x["draw"]) / vol0 + F(x["draw"] * x["r"], 100)
    solute += F(x["y"] * x["c4"], 100) + x["add"]
    if x["ask"] == "pp":
        return fmt(abs(F(solute * 100, vol) - F(x["a"] * x["c1"] + x["b"] * x["c2"] + x["c"] * x["c3"], vol0)))
    if x["ask"] == "reverse":
        return fmt(F(x["t"] * vol - 100 * solute, 100 - x["t"]))
    return pct(F(solute * 100, vol))


def mam_three_solution_mix(r, v):
    rows = (
        (40, 50, 30, 20, 50, 80, 20, 0, 0, 0, 0, 0, "final"),
        (50, 40, 60, 15, 45, 70, 30, 60, 20, 90, 0, 0, "final"),
        (60, 50, 40, 25, 55, 75, 25, 0, 0, 0, 5, 0, "pp"),
        (45, 55, 50, 30, 60, 10, 25, 0, 0, 0, 0, 0, "reverse"),
        (70, 60, 50, 20, 50, 65, 30, 40, 20, 80, 0, 15, "final"),
    )
    (a, b, c, c1, c2, c3, draw, rr, y, c4, add, e, ask) = rows[v]
    x = {"a": a, "b": b, "c": c, "c1": c1, "c2": c2, "c3": c3,
         "draw": draw, "r": rr, "y": y, "c4": c4, "add": add, "e": e,
         "t": 40, "ask": ask}
    ans = _solve_three_solution_mix(x)
    texts = (
        f"Three stock solutions of {c1}%, {c2}% and {c3}% are drawn in volumes {a} L, {b} L and "
        f"{c} L into a blending tank. {draw} L of the blend is then swapped for water. Find the final strength.",
        f"A bank of {a} L at {c1}%, {b} L at {c2}% and {c} L at {c3}% is blended, {draw} L is "
        f"withdrawn and replaced with {rr}% liquid, and {y} L at {c4}% is poured in. Find the final percent.",
        f"Mixtures of {a}, {b} and {c} L at {c1}%, {c2}% and {c3}% are combined. After {draw} L "
        f"is replaced with water and {add} kg solute is added, by how many percentage points does "
        f"the strength differ from the direct three-way mix?",
        f"Three reservoirs contribute {a}, {b} and {c} L at {c1}%, {c2}% and {c3}%. {draw} L is "
        f"drawn off and replaced with water. How much pure solute is needed to bring the blend to {x['t']}%?",
        f"A vat receives {a}, {b} and {c} L at {c1}%, {c2}% and {c3}%. {draw} L is swapped for "
        f"{rr}% liquid, {y} L at {c4}% is added and {e} L boils away. Find the final concentration.",
    )
    notes = (
        "The weighted solute of three stocks is followed by a withdrawal-and-replace step.",
        "A three-way blend, a partial swap and a further addition all change the solute.",
        "The treated strength is compared with the untreated direct mix in percentage points.",
        "After a withdrawal cycle the required solute addition is found by reversing a percentage equation.",
        "Three stocks, a replacement, an addition and evaporation are combined.",
    )
    return q("mam_three_solution_mix", v, texts[v], ans,
             _distractors_for(ans),
             _explain(notes[v], ans), x)


# ---------------------------------------------------------------------------
# 3. Evaporation, crystallisation, dilution and reverse restoration.
# ---------------------------------------------------------------------------
def _solve_evap_restore(x):
    sol = F(x["V"] * x["c"], 100) - x["p1"] + x["s"]
    vol = x["V"] + x["w1"] - x["e1"] - x["p1"] + x["w2"] + x["s"]
    if x["ask"] == "evap_back":
        return fmt(vol - F(sol * 100, x["c"]))
    if x["ask"] == "solute_to":
        return fmt(F(x["t"] * vol - 100 * sol, 100 - x["t"]))
    return pct(F(sol * 100, vol))


def mam_evap_restore(r, v):
    rows = (
        (200, 30, 50, 20, 5, 0, 0, 0, "evap_back"),
        (240, 25, 0, 60, 8, 20, 0, 0, "final"),
        (300, 18, 40, 70, 6, 0, 14, 25, "solute_to"),
        (180, 40, 30, 50, 10, 25, 0, 0, "final"),
        (250, 22, 20, 40, 0, 30, 0, 0, "evap_back"),
    )
    (V, c, w1, e1, p1, w2, s, t, ask) = rows[v]
    x = {"V": V, "c": c, "w1": w1, "e1": e1, "p1": p1,
         "w2": w2, "s": s, "t": t, "ask": ask}
    ans = _solve_evap_restore(x)
    texts = (
        f"A syrup kettle holds {V} L at {c}% solute. {w1} L of water is added, {e1} L is evaporated "
        f"and {p1} kg of crystals is filtered out. How much water must then be evaporated to restore {c}%?",
        f"A brine pan has {V} L at {c}%. {e1} L boils off, {p1} kg of salt is removed and {w2} L of "
        f"water is returned. Find the final solute percentage.",
        f"A {V} L solution at {c}% gets {w1} L water, loses {e1} L by boiling and {p1} kg of crystals, "
        f"then receives {s} kg of solute. How much more solute is needed for {t}%?",
        f"A {V} L batch at {c}% is diluted with {w1} L water, concentrated by {e1} L, stripped of "
        f"{p1} kg crystals and topped up with {w2} L water. Find the final concentration.",
        f"A {V} L batch at {c}% gains {w1} L water, loses {e1} L to evaporation and gains {w2} L "
        f"water. How much water must be boiled off to return to {c}%?",
    )
    notes = (
        "Dilution, evaporation and crystal removal precede a reverse evaporation calculation.",
        "Boiling, crystallisation and water restoration are applied in sequence.",
        "Four physical changes are followed by a reverse solute-addition equation.",
        "A dilution-and-concentration cycle with crystal loss ends in a percentage calculation.",
        "The net volume is reversed to find the evaporation that restores the original strength.",
    )
    return q("mam_evap_restore", v, texts[v], ans,
             _distractors_for(ans),
             _explain(notes[v], ans), x)


# ---------------------------------------------------------------------------
# 4. Two-drum transfer, return, comparison and reverse dilution.
# ---------------------------------------------------------------------------
def _solve_vessel_transfer(x):
    VA, VB, t, u = x["VA"], x["VB"], x["t"], x["u"]
    a_sol = F(x["cA"] * (VA - t), 100)
    b_sol = F(x["cB"] * VB, 100) + F(x["cA"] * t, 100)
    b_vol = VB + t
    bc = F(b_sol * 100, b_vol)
    if u:
        moved = F(u * bc, 100)
        a_sol += moved
        b_sol -= moved
        b_vol -= u
        a_vol = VA - t + u
    else:
        a_vol = VA - t
    b_vol -= x["e"]
    a_sol += x["add"]
    a_vol += x["add"] + x["w"]
    ca = F(a_sol * 100, a_vol)
    cb = F(b_sol * 100, b_vol)
    if x["ask"] == "diff":
        return fmt(ca - cb)
    if x["ask"] == "target":
        return fmt(F(a_sol * 100, x["tgt"]) - a_vol)
    return pct(ca if x["ask"] == "A" else cb)


def mam_vessel_transfer(r, v):
    rows = (
        (120, 50, 100, 20, 40, 20, 0, 0, 0, 0, "diff"),
        (150, 40, 120, 10, 50, 30, 20, 0, 0, 0, "A"),
        (180, 45, 140, 15, 60, 40, 0, 0, 0, 30, "target"),
        (200, 35, 160, 12, 50, 25, 0, 15, 0, 0, "A"),
        (160, 55, 120, 25, 40, 30, 0, 0, 10, 0, "B"),
    )
    (VA, cA, VB, cB, t, u, w, e, add, tgt, ask) = rows[v]
    x = {"VA": VA, "cA": cA, "VB": VB, "cB": cB, "t": t, "u": u,
         "w": w, "e": e, "add": add, "tgt": tgt, "ask": ask}
    ans = _solve_vessel_transfer(x)
    texts = (
        f"Drum P holds {VA} L at {cA}% and drum Q holds {VB} L at {cB}%. {t} L goes P to Q, "
        f"then {u} L of the mixed Q liquid returns to P. Find the difference in final strength "
        f"between P and Q in percentage points.",
        f"Drum P has {VA} L at {cA}% and Q has {VB} L at {cB}%. {t} L is sent P to Q, {u} L comes "
        f"back after mixing, and {w} L of water is added to P. Find P's final strength.",
        f"Drum P has {VA} L at {cA}% and Q has {VB} L at {cB}%. After a {t} L transfer and a "
        f"{u} L return, how much water must be added to P to bring it to {tgt}%?",
        f"Drum P holds {VA} L at {cA}% and Q holds {VB} L at {cB}%. {t} L is moved P to Q, {u} L "
        f"is returned and {e} L evaporates from Q. Find P's strength.",
        f"Drum P has {VA} L at {cA}% and Q has {VB} L at {cB}%. {t} L passes P to Q, {u} L returns "
        f"to P and {add} kg solute is dissolved in P. Find Q's final concentration.",
    )
    notes = (
        "The transfer changes Q's strength, which then governs the return; the two strengths are compared.",
        "A transfer, a return and a dilution are chained before P's strength is read.",
        "After a transfer and return, the water needed for a target strength is solved backwards.",
        "A transfer-return cycle is followed by evaporation in Q before P is measured.",
        "A two-way transfer is followed by a solute addition before Q is measured.",
    )
    return q("mam_vessel_transfer", v, texts[v], ans,
             _distractors_for(ans),
             _explain(notes[v], ans), x)


# ---------------------------------------------------------------------------
# 5. Blended spice lots: wastage, discount, revenue and reverse pricing.
# ---------------------------------------------------------------------------
def _solve_price_profit_mix(x):
    cper = F(x["m"] * x["a"] + x["n"] * x["b"], x["m"] + x["n"])
    cost = F(x["T"] * cper * (100 - x["d"]), 100)
    qty = F(x["T"] * (100 - x["w"]), 100)
    eff = F(cper * 100, 100 - x["w"])
    rev = F(qty * x["sell"])
    sp = F(x["mp"] * (100 - x["disc"]), 100)
    if x["ask"] == "profit":
        return money(F(rev - cost))
    if x["ask"] == "pct":
        return pct(F((sp - eff) * 100, eff))
    if x["ask"] == "sell_needed":
        return money(F(eff * (100 + x["p"]), 100))
    if x["ask"] == "pct_diff":
        return fmt(F((x["sell"] - cper) * 100, cper) - F((x["sell"] - eff) * 100, eff))
    return fmt(F(x["target"] * 100, x["sell"] * (100 - x["w"]) - 100 * cper))


def mam_price_profit_mix(r, v):
    rows = (
        (60, 90, 2, 1, 150, 8, 0, 85, 0, 0, 0, "profit"),
        (40, 70, 3, 2, 100, 10, 0, 0, 66, 5, 0, "pct"),
        (50, 80, 1, 2, 120, 12, 0, 0, 0, 0, 25, "sell_needed"),
        (30, 50, 3, 2, 200, 15, 0, 60, 0, 0, 0, "pct_diff"),
        (45, 75, 1, 1, 0, 10, 0, 80, 0, 0, 900, "qty"),
    )
    (a, b, m, n, T, w, d, sell, mp, disc, p, ask) = rows[v]
    target = rows[v][10] if ask == "qty" else 0
    x = {"a": a, "b": b, "m": m, "n": n, "T": T, "w": w, "d": d,
         "sell": sell, "mp": mp, "disc": disc, "p": p,
         "target": target, "ask": ask}
    ans = _solve_price_profit_mix(x)
    texts = (
        f"Two spice lots costing ₹{a} and ₹{b} per kg are blended {m}:{n}. {T} kg is made, "
        f"{w}% is lost in handling and the balance is sold at ₹{sell} per kg. Find the total profit.",
        f"Spices worth ₹{a} and ₹{b} per kg are mixed {m}:{n}; {w}% of the blend is wasted. "
        f"Marked ₹{mp} per kg and sold at a {disc}% discount, find the effective profit percent.",
        f"Two grades at ₹{a} and ₹{b} per kg are combined {m}:{n} with {w}% wastage. At what price "
        f"per kg must the saleable lot be sold to earn {p}% profit?",
        f"A {m}:{n} blend of ₹{a} and ₹{b} spices suffers {w}% wastage and sells at ₹{sell} per "
        f"kg. By how many percentage points is the profit rate lower than in the no-wastage case?",
        f"An equal blend of ₹{a} and ₹{b} grades loses {w}% in processing and sells at ₹{sell} "
        f"per kg. How many kilograms must be purchased to earn ₹{target} profit?",
    )
    notes = (
        "The blend cost, wastage-adjusted quantity and revenue are all needed before profit.",
        "An effective cost after wastage is compared with a discounted marked price.",
        "The wastage-adjusted cost is reversed into a required selling price.",
        "Profit rates with and without wastage are compared in percentage points.",
        "The per-purchased-kg profit is reversed to obtain the required purchase quantity.",
    )
    return q("mam_price_profit_mix", v, texts[v], ans,
             _distractors_for(ans),
             _explain(notes[v], ans), x)


# ---------------------------------------------------------------------------
# 6. Scrap alloys: wastage, draw-off, metal addition, ratio and back-calc.
# ---------------------------------------------------------------------------
def _solve_alloy_wastage(x):
    cu = (F(x["m1"] * x["c1"] * (100 - x["w1"]), 10000)
          + F(x["m2"] * x["c2"] * (100 - x["w2"]), 10000))
    zn = (F(x["m1"] * (100 - x["c1"]) * (100 - x["w1"]), 10000)
          + F(x["m2"] * (100 - x["c2"]) * (100 - x["w2"]), 10000))
    mass = F(x["m1"] * (100 - x["w1"]), 100) + F(x["m2"] * (100 - x["w2"]), 100)
    if x["draw"]:
        factor = F(mass - x["draw"], mass)
        cu = F(cu * factor)
        zn = F(zn * factor)
        mass -= x["draw"]
    cu += x["pc"]
    zn += x["za"]
    mass += x["pc"] + x["za"]
    if x["ask"] == "mass":
        return fmt(cu)
    if x["ask"] == "ratio":
        return ratio(cu, zn)
    if x["ask"] == "reverse":
        return fmt(F(x["t"] * mass - 100 * cu, 100 - x["t"]))
    return pct(F(cu * 100, mass))


def mam_alloy_wastage(r, v):
    rows = (
        (120, 40, 5, 80, 65, 8, 20, 0, 0, 0, "pct"),
        (150, 30, 10, 100, 55, 6, 0, 8, 5, 0, "ratio"),
        (100, 25, 10, 150, 60, 20, 10, 0, 0, 50, "reverse"),
        (200, 35, 6, 120, 55, 6, 0, 10, 0, 0, "mass"),
        (160, 45, 5, 140, 20, 10, 30, 0, 6, 0, "pct"),
    )
    (m1, c1, w1, m2, c2, w2, draw, pc, za, t, ask) = rows[v]
    x = {"m1": m1, "c1": c1, "w1": w1, "m2": m2, "c2": c2, "w2": w2,
         "draw": draw, "pc": pc, "za": za, "t": t, "ask": ask}
    ans = _solve_alloy_wastage(x)
    texts = (
        f"Two scrap alloys of {m1} kg at {c1}% copper and {m2} kg at {c2}% copper melt with "
        f"{w1}% and {w2}% mass loss; {draw} kg of the melt is then removed. Find the copper percent.",
        f"A foundry melts {m1} kg of {c1}% copper alloy and {m2} kg of {c2}% copper alloy, losing "
        f"{w1}% and {w2}% mass, then adds {pc} kg copper and {za} kg zinc. Find the final Cu:Zn ratio.",
        f"Alloys of {m1} kg at {c1}% and {m2} kg at {c2}% copper lose {w1}% and {w2}% in melting; "
        f"{draw} kg is tapped off. How much copper must be added for {t}% copper?",
        f"Two ingots of {m1} kg at {c1}% and {m2} kg at {c2}% copper lose {w1}% and {w2}% of their "
        f"mass; {pc} kg copper is then added. Find the mass of copper in the final ingot.",
        f"Scrap of {m1} kg at {c1}% and {m2} kg at {c2}% copper is melted with {w1}% and {w2}% "
        f"loss, {draw} kg is removed and {za} kg zinc is added. Find the copper percentage.",
    )
    notes = (
        "Wastage of two alloys precedes a proportional draw-off and a percentage calculation.",
        "Both constituent metals are tracked through wastage and separate additions.",
        "After wastage and tapping, a reverse copper-addition equation is solved.",
        "Copper mass is found after wastage and a fresh metal addition.",
        "Wastage, draw-off and zinc addition combine before the copper percent is read.",
    )
    return q("mam_alloy_wastage", v, texts[v], ans,
             _distractors_for(ans),
             _explain(notes[v], ans), x)


# ---------------------------------------------------------------------------
# 7. Withdrawal, dilution and evaporation followed by reverse replenishment.
# ---------------------------------------------------------------------------
def _solve_dilution_recovery(x):
    sol = F(x["V"] * x["c"], 100) * F(x["V"] - x["draw"], x["V"])
    vol = x["V"] - x["draw"] + x["w1"] + x["w2"] - x["e"]
    if x["ask"] == "solute":
        return fmt(F(x["t"] * vol - 100 * sol, 100 - x["t"]))
    if x["ask"] == "liquid":
        return fmt(F(x["t"] * vol - 100 * sol, x["ac"] - x["t"]))
    if x["ask"] == "water":
        return fmt(F(sol * 100, x["t"]) - vol)
    if x["ask"] == "evap":
        return fmt(vol - F(sol * 100, x["t"]))
    sol += F(x["x"] * x["ac"], 100) + x["s"]
    vol += x["x"] + x["s"]
    return pct(F(sol * 100, vol))


def mam_dilution_recovery(r, v):
    rows = (
        (120, 40, 30, 20, 0, 0, 35, 40, 60, 0, "liquid"),
        (150, 35, 0, 30, 20, 10, 45, 40, 0, 0, "solute"),
        (100, 50, 20, 10, 0, 0, 25, 0, 0, 0, "water"),
        (180, 25, 30, 40, 0, 0, 40, 0, 0, 0, "evap"),
        (200, 30, 40, 30, 0, 20, 0, 80, 8, 25, "final"),
    )
    (V, c, draw, w1, w2, e, t, ac, xx, s, ask) = rows[v]
    x = {"V": V, "c": c, "draw": draw, "w1": w1, "w2": w2, "e": e,
         "t": t, "ac": ac, "x": xx, "s": s, "ask": ask}
    ans = _solve_dilution_recovery(x)
    texts = (
        f"A replenishment line holds {V} L at {c}%. {draw} L is run off, {w1} L water is added "
        f"and then {ac}% liquid is used to raise the strength to {t}%. How much of that liquid is needed?",
        f"A {V} L tank at {c}% gets {w1} L and {w2} L of water in turn, then {e} L of water is "
        f"boiled off. How much pure solute brings it to {t}%?",
        f"From {V} L at {c}%, {draw} L is removed and {w1} L water is poured in. How much more "
        f"water is required to bring the strength down to {t}%?",
        f"A vessel of {V} L at {c}% loses {draw} L, gains {w1} L water and must reach {t}%. "
        f"How many litres must be evaporated?",
        f"A {V} L lot at {c}% has {draw} L removed, {w1} L water added and {e} L evaporated; "
        f"then {xx} L of {ac}% liquid and {s} kg solute are added. Find the final strength.",
    )
    notes = (
        "Withdrawal and dilution are followed by an alligation-style reverse addition.",
        "Two dilutions and an evaporation precede a reverse solute calculation.",
        "The solute is fixed after withdrawal, so water addition is solved backwards.",
        "Evaporation needed for a target strength is found from the solute balance.",
        "A withdrawal-dilution-evaporation chain ends with two different additions.",
    )
    return q("mam_dilution_recovery", v, texts[v], ans, near_num(_raw(ans), 2),
             _explain(notes[v], ans), x)


# ---------------------------------------------------------------------------
# 8. Component transfer with return, additives and reverse ratio adjustment.
# ---------------------------------------------------------------------------
def _solve_component_transfer_ratio(x):
    VA, VB, t, u = x["VA"], x["VB"], x["t"], x["u"]
    m1 = F(VA * x["a"], x["a"] + x["b"])
    w1 = VA - m1
    m2 = F(VB * x["c"], x["c"] + x["d"])
    w2 = VB - m2
    m1 -= F(t * x["a"], x["a"] + x["b"])
    w1 -= F(t * x["b"], x["a"] + x["b"])
    m2 += F(t * x["a"], x["a"] + x["b"])
    w2 += F(t * x["b"], x["a"] + x["b"])
    v2 = VB + t
    if u:
        rm = F(u * m2, v2)
        rw = F(u * w2, v2)
        m1 += rm
        w1 += rw
        m2 -= rm
        w2 -= rw
    m1 += x["am"]
    w1 += x["aw"]
    if x["ask"] == "reverse_water":
        return fmt(F(x["qq"] * m1, x["p"]) - w1)
    if x["ask"] == "reverse_milk":
        return fmt(F(x["p"] * w1 - x["qq"] * m1, x["qq"]))
    return ratio(m1, w1) if x["ask"] == "first" else ratio(m2, w2)


def mam_component_transfer_ratio(r, v):
    rows = (
        (90, 2, 1, 60, 1, 1, 30, 20, 6, 0, 0, 0, "first"),
        (100, 3, 2, 80, 1, 3, 40, 25, 0, 10, 0, 0, "first"),
        (120, 4, 1, 90, 2, 3, 30, 20, 0, 0, 1, 1, "reverse_water"),
        (140, 5, 2, 100, 1, 1, 40, 25, 0, 0, 3, 1, "reverse_milk"),
        (160, 3, 1, 120, 2, 1, 50, 30, 8, 12, 0, 0, "first"),
    )
    (VA, a, b, VB, c, d, t, u, am, aw, p, qq, ask) = rows[v]
    x = {"VA": VA, "a": a, "b": b, "VB": VB, "c": c, "d": d,
         "t": t, "u": u, "am": am, "aw": aw, "p": p, "qq": qq, "ask": ask}
    ans = _solve_component_transfer_ratio(x)
    texts = (
        f"Can A has {VA} L of milk:water {a}:{b} and can B has {VB} L at {c}:{d}. {t} L moves A to "
        f"B, {u} L of B's mixture returns to A, then {am} L milk is poured into A. Find A's ratio.",
        f"Can A holds {VA} L at {a}:{b} and B holds {VB} L at {c}:{d}. After {t} L A-to-B and "
        f"{u} L B-to-A transfers, {aw} L water is added to A. Find the ratio in A.",
        f"Can A has {VA} L at {a}:{b}, can B {VB} L at {c}:{d}. {t} L goes A to B and {u} L "
        f"comes back. How much water must join A for a {p}:{qq} milk-water ratio?",
        f"Can A has {VA} L at {a}:{b}, can B {VB} L at {c}:{d}. After {t} L and {u} L transfers, "
        f"how much milk must be added to A for a {p}:{qq} ratio?",
        f"Can A has {VA} L at {a}:{b} and B has {VB} L at {c}:{d}. A {t} L transfer and {u} L "
        f"return are followed by {am} L milk and {aw} L water in A. Find A's ratio.",
    )
    notes = (
        "The return from B uses B's changed composition, then milk is added to A.",
        "A two-way transfer changes both cans; A's ratio is read after water is added.",
        "A transfer-return cycle is followed by a reverse water-adjustment equation.",
        "After a two-way transfer, milk addition is reversed from the target ratio.",
        "Two transfers and two separate additions are chained in vessel A.",
    )
    return q("mam_component_transfer_ratio", v, texts[v], ans, _distractors_for(ans),
             _explain(notes[v], ans), x)


# ---------------------------------------------------------------------------
# 9. Fractional removals with second removal, evaporation and back-calc.
# ---------------------------------------------------------------------------
def _solve_fractional_replace(x):
    milk = F(x["V"] * x["a"], x["a"] + x["b"])
    vol = F(x["V"])
    milk = F(milk * (x["fd"] - x["fn"]), x["fd"])
    vol = F(vol * (x["fd"] - x["fn"]), x["fd"])
    if x["x"]:
        milk = milk * F(vol - x["x"], vol) + F(x["x"] * x["rr"], 100)
    if x["fn2"]:
        milk = F(milk * (x["fd2"] - x["fn2"]), x["fd2"])
        vol = F(vol * (x["fd2"] - x["fn2"]), x["fd2"])
    if x["x2"]:
        milk = milk * F(vol - x["x2"], vol) + F(x["x2"] * x["r2"], 100)
    milk += x["add"]
    vol = vol - x["e"] + x["add"]
    if x["ask"] == "pct":
        return pct(F(milk * 100, vol))
    if x["ask"] == "reverse":
        return fmt(F(x["t"] * vol - 100 * milk, 100 - x["t"]))
    return ratio(milk, vol - milk)


def mam_fractional_replace(r, v):
    rows = (
        (120, 3, 1, 1, 4, 30, 50, 0, 1, 0, 0, 10, 0, 0, "pct"),
        (180, 2, 1, 1, 3, 30, 60, 1, 5, 20, 0, 0, 0, 0, "ratio"),
        (200, 3, 2, 1, 5, 25, 80, 0, 1, 0, 0, 0, 0, 65, "reverse"),
        (240, 5, 3, 1, 4, 40, 75, 0, 1, 0, 20, 15, 0, 0, "pct"),
        (150, 1, 1, 1, 3, 20, 80, 1, 4, 15, 0, 0, 0, 0, "ratio"),
    )
    (V, a, b, fn, fd, xx, rr, fn2, fd2, x2, e, add, r2, t, ask) = rows[v]
    x = {"V": V, "a": a, "b": b, "fn": fn, "fd": fd, "x": xx, "rr": rr,
         "fn2": fn2, "fd2": fd2, "x2": x2, "e": e, "add": add, "r2": r2,
         "t": t, "ask": ask}
    ans = _solve_fractional_replace(x)
    texts = (
        f"A blender jar holds {V} L at milk:water {a}:{b}. One quarter is removed, {xx} L of "
        f"{rr}% milk mixture is put back, and {add} L pure milk is added. Find the milk percent.",
        f"A blender jar of {V} L at {a}:{b} loses one third of its contents, receives {xx} L at "
        f"{rr}% milk, loses one fifth more, then has {x2} L swapped for water. Find the milk:water ratio.",
        f"From {V} L at {a}:{b}, one fifth is removed and {xx} L of {rr}% milk is returned. "
        f"How much pure milk must then be added to reach {t}% milk?",
        f"A {V} L jar at {a}:{b} loses one quarter, is topped with {xx} L at {rr}% milk, "
        f"boils down by {e} L and receives {add} L milk. Find the milk percentage.",
        f"A jar of {V} L at {a}:{b} has one third removed and {xx} L at {rr}% returned; a further "
        f"one quarter is removed and {x2} L is swapped for water. Find the milk:water ratio.",
    )
    notes = (
        "A fractional removal, a replacement and a milk addition determine the percentage.",
        "Two fractional removals with different replacement liquids are chained.",
        "After a fractional replacement, the milk needed for a target percent is reversed.",
        "A fractional swap, evaporation and milk addition are applied in turn.",
        "Two successive fractional removals with distinct fill liquids end in a ratio.",
    )
    return q("mam_fractional_replace", v, texts[v], ans,
             _distractors_for(ans),
             _explain(notes[v], ans), x)


# ---------------------------------------------------------------------------
# 10. Two replacements with evaporation, additions and point comparisons.
# ---------------------------------------------------------------------------
def _solve_percentage_point_change(x):
    sol = F(x["V"] * x["c"], 100)
    sol = sol * F(x["V"] - x["x"], x["V"]) + F(x["x"] * x["s"], 100)
    sol = sol * F(x["V"] - x["d2"], x["V"]) + F(x["d2"] * x["r2"], 100)
    vol = x["V"] - x["e"] + x["w"] + x["adds"]
    sol += x["adds"]
    if x["ask"] == "pp":
        return fmt(F(sol * 100, vol) - x["c"])
    if x["ask"] == "reverse":
        return fmt(F(x["t"] * vol - 100 * sol, 100 - x["t"]))
    return pct(F(sol * 100, vol))


def mam_percentage_point_change(r, v):
    rows = (
        (40, 120, 30, 10, 40, 70, 0, 0, 0, 0, "pp"),
        (35, 200, 40, 0, 50, 60, 30, 0, 12, 0, "pp"),
        (25, 180, 45, 0, 30, 40, 0, 0, 0, 30, "reverse"),
        (50, 150, 30, 80, 45, 0, 0, 25, 0, 0, "final"),
        (30, 240, 60, 0, 40, 50, 35, 0, 0, 0, "pp"),
    )
    (c, V, xx, s, d2, r2, e, w, adds, t, ask) = rows[v]
    x = {"c": c, "V": V, "x": xx, "s": s, "d2": d2, "r2": r2,
         "e": e, "w": w, "adds": adds, "t": t, "ask": ask}
    ans = _solve_percentage_point_change(x)
    texts = (
        f"A chemical drum starts at {c}% solute in {V} L. {xx} L is replaced with a {s}% liquid "
        f"and {d2} L with a {r2}% liquid. By how many percentage points does the strength change?",
        f"A {V} L drum at {c}% undergoes replacements of {xx} L with {s}% and {d2} L with {r2}% "
        f"liquid, then {e} L evaporates and {adds} kg solute is dissolved. Find the point change.",
        f"From {V} L at {c}%, {xx} L is replaced with water and {d2} L with {r2}% liquid. "
        f"How much pure solute is needed to finish at {t}%?",
        f"A drum of {V} L at {c}% has {xx} L swapped for {s}% liquid and {d2} L swapped for "
        f"water, after which {w} L water is added. Find the final concentration.",
        f"A {V} L solution at {c}% is treated twice ({xx} L with water, {d2} L with {r2}%) and "
        f"{e} L is evaporated. Find the percentage-point change.",
    )
    notes = (
        "Two replacement liquids act in sequence before the point difference is taken.",
        "Two replacements, evaporation and solute addition are combined.",
        "After two replacements the required solute addition is found in reverse.",
        "Two swaps and a water addition lead to a final percentage.",
        "Replacement pair and evaporation precede the point comparison.",
    )
    return q("mam_percentage_point_change", v, texts[v], ans, near_num(_raw(ans), 3),
             _explain(notes[v], ans), x)


# ---------------------------------------------------------------------------
# 11. Weighted-average lots with discount, wastage and reverse pricing.
# ---------------------------------------------------------------------------
def _solve_weighted_unknown(x):
    first = F(x["T"] * (x["b"] - x["t"]), x["b"] - x["a"])
    cost = F((first * x["a"] + (x["T"] - first) * x["b"]) * (100 - x["d"]), 100)
    qty = F(x["T"] * (100 - x["w"]), 100)
    if x["ask"] == "quantity":
        return fmt(first)
    if x["ask"] == "profit":
        return money(F(qty * x["s"]) - cost)
    if x["ask"] == "sell_needed":
        return money(F(cost * (100 + x["p"]), 100 * qty))
    if x["ask"] == "reverse_price":
        return money(F(cost + x["target"], qty))
    return money(cost)


def mam_weighted_unknown(r, v):
    rows = (
        (20, 50, 35, 120, 8, 45, 0, 0, 0, "profit"),
        (30, 60, 40, 150, 10, 60, 5, 0, 0, "profit"),
        (40, 70, 55, 200, 12, 0, 0, 20, 0, "sell_needed"),
        (25, 45, 35, 180, 5, 42, 0, 0, 900, "reverse_price"),
        (50, 90, 70, 240, 15, 95, 8, 0, 0, "cost"),
    )
    (a, b, t, T, w, s, d, p, target, ask) = rows[v]
    x = {"a": a, "b": b, "t": t, "T": T, "w": w, "s": s,
         "d": d, "p": p, "target": target, "ask": ask}
    ans = _solve_weighted_unknown(x)
    texts = (
        f"Grain lots worth ₹{a} and ₹{b} per kg are blended to make {T} kg worth ₹{t} per kg. "
        f"{w}% is lost and the balance sells at ₹{s} per kg. Find the profit.",
        f"Two lots at ₹{a} and ₹{b} per kg form {T} kg averaging ₹{t}. A {d}% purchase discount "
        f"applies and {w}% is wasted; the rest sells at ₹{s}. Find the profit.",
        f"Grades at ₹{a} and ₹{b} are mixed to make {T} kg worth ₹{t} per kg. With {w}% wastage, "
        f"find the selling price needed for {p}% profit.",
        f"A {T} kg blend of ₹{a} and ₹{b} lots averages ₹{t} per kg. After {w}% wastage, what "
        f"selling price yields ₹{target} profit?",
        f"Two grades at ₹{a} and ₹{b} per kg make {T} kg worth ₹{t} per kg. An {d}% discount is "
        f"availed and {w}% is lost. Find the total purchase cost.",
    )
    notes = (
        "Alligation fixes the quantities, then wastage and revenue determine profit.",
        "Alligation, a purchase discount and wastage precede the profit calculation.",
        "The blend quantity, effective cost and wastage are reversed into a selling price.",
        "A profit target is reversed into a selling price after alligation and wastage.",
        "Alligation, discount and wastage combine in the cost calculation.",
    )
    return q("mam_weighted_unknown", v, texts[v], ans,
             _distractors_for(ans),
             _explain(notes[v], ans), x)


# ---------------------------------------------------------------------------
# 12. Two-stage alligation with shortage, replacement and reverse limits.
# ---------------------------------------------------------------------------
def _solve_two_stage_restriction(x):
    if x["ask"] == "third":
        return fmt(F(x["Q"] * (x["p"] - x["t"]), x["t"] - x["ac"]))
    if x["ask"] == "first":
        return fmt(F(x["Q"] * (x["c2"] - x["p"]), x["c2"] - x["c1"]))
    if x["ask"] == "replace":
        return fmt(F(x["Q"] * (x["p"] - x["t"]), x["p"]))
    if x["ask"] == "replace_up":
        return fmt(F(x["Q"] * (x["t2"] - x["p"]), x["ac"] - x["p"]))
    return fmt(F(x["Q"] * x["p"] - x["qty"] * x["c2"]
                 - (x["Q"] - x["qty"]) * x["c1"], 100))


def mam_two_stage_restriction(r, v):
    rows = (
        (10, 50, 30, 15, 0, 0, 100, 0, "replace"),
        (20, 60, 40, 30, 10, 0, 120, 0, "third"),
        (15, 45, 30, 0, 0, 0, 90, 30, "extra"),
        (25, 65, 50, 35, 20, 0, 80, 0, "replace"),
        (10, 40, 25, 35, 60, 0, 100, 40, "extra"),
    )
    (c1, c2, p, t, ac, t2, Q, qty, ask) = rows[v]
    x = {"c1": c1, "c2": c2, "p": p, "t": t, "ac": ac, "t2": t2,
         "Q": Q, "qty": qty, "ask": ask}
    ans = _solve_two_stage_restriction(x)
    texts = (
        f"A {p}% premix of {c1}% and {c2}% feeds is prepared as {Q} L. Some premix is then drawn "
        f"off and replaced with water to reach {t}%. Find the replaced volume.",
        f"A {p}% premix is made from {c1}% and {c2}% liquids. {Q} L of it is diluted with a "
        f"{ac}% liquid to reach {t}%. Find how much of that liquid is required.",
        f"A plant needs {Q} L of {p}% premix from {c1}% and {c2}% feeds, but only {qty} L of the "
        f"strong feed is in stock. How much pure solute makes up the shortfall?",
        f"A {p}% premix is prepared from {c1}% and {c2}% liquids. From {Q} L, how much must be "
        f"drawn off and replaced with water to land at {t}%?",
        f"Only {qty} L of the {c2}% feed is available for {Q} L of {p}% premix from {c1}% feed. "
        f"Find the pure solute needed to meet the strength.",
    )
    notes = (
        "The premix strength is set first, then the water replacement is reversed.",
        "Two alligation stages find the premix and the diluting-liquid quantity.",
        "A stock limit forces a pure-solute top-up after the first alligation.",
        "The premix composition and a withdrawal equation are chained.",
        "The shortfall of strong feed is converted into a pure-solute addition.",
    )
    return q("mam_two_stage_restriction", v, texts[v], ans, near_num(_raw(ans), 2),
             _explain(notes[v], ans), x)


# ---------------------------------------------------------------------------
# 13. Alloy ratios of ratios with wastage, tapping and reverse additions.
# ---------------------------------------------------------------------------
def _solve_alloy_ratio_of_ratios(x):
    a, b, c, d = x["a"], x["b"], x["c"], x["d"]
    cu = (F(x["mA"] * a * (100 - x["w1"]), 100 * (a + b))
          + F(x["mB"] * c * (100 - x["w2"]), 100 * (c + d)))
    zn = (F(x["mA"] * b * (100 - x["w1"]), 100 * (a + b))
          + F(x["mB"] * d * (100 - x["w2"]), 100 * (c + d)))
    mass = F(x["mA"] * (100 - x["w1"]), 100) + F(x["mB"] * (100 - x["w2"]), 100)
    if x["draw"]:
        factor = F(mass - x["draw"], mass)
        cu = F(cu * factor)
        zn = F(zn * factor)
        mass -= x["draw"]
    cu += x["cuadd"]
    zn += x["znadd"]
    mass += x["cuadd"] + x["znadd"]
    if x["ask"] == "ratio":
        return ratio(cu, zn)
    if x["ask"] == "pct":
        return pct(F(cu * 100, mass))
    if x["ask"] == "reverse_cu":
        return fmt(F(x["ta"] * mass - (x["ta"] + x["tb"]) * cu, x["tb"]))
    return fmt(F(x["tb"] * mass - (x["ta"] + x["tb"]) * zn, x["ta"]))


def mam_alloy_ratio_of_ratios(r, v):
    rows = (
        (3, 2, 5, 3, 120, 100, 5, 8, 20, 10, 0, 0, 0, 0, "pct"),
        (2, 1, 3, 5, 140, 140, 5, 20, 20, 0, 5, 0, 0, 0, "ratio"),
        (1, 1, 4, 1, 100, 120, 0, 5, 0, 0, 0, 4, 1, 0, "reverse_cu"),
        (3, 1, 2, 3, 120, 90, 4, 6, 0, 0, 0, 1, 1, 0, "reverse_zn"),
        (5, 2, 1, 1, 160, 80, 8, 5, 30, 6, 4, 0, 0, 0, "pct"),
    )
    (a, b, c, d, mA, mB, w1, w2, draw, cuadd, znadd, ta, tb, spare, ask) = rows[v]
    x = {"a": a, "b": b, "c": c, "d": d, "mA": mA, "mB": mB,
         "w1": w1, "w2": w2, "draw": draw, "cuadd": cuadd, "znadd": znadd,
         "ta": ta, "tb": tb, "ask": ask}
    ans = _solve_alloy_ratio_of_ratios(x)
    w1_loss = "no loss" if w1 == 0 else f"{w1}% loss"
    texts = (
        f"Alloy X is {a}:{b} copper-zinc and weighs {mA} kg; alloy Y is {c}:{d} and weighs "
        f"{mB} kg. They lose {w1}% and {w2}% on melting, {draw} kg is tapped off and {cuadd} kg "
        f"copper is added. Find the copper percent.",
        f"A foundry mixes {mA} kg of {a}:{b} alloy with {mB} kg of {c}:{d} alloy, losing {w1}% "
        f"and {w2}%; after {draw} kg is tapped, {znadd} kg zinc is charged. Find the Cu:Zn ratio.",
        f"Two alloys of {a}:{b} ({mA} kg) and {c}:{d} ({mB} kg) melt with {w1_loss} in the first "
        f"and {w2}% in the second. How much copper must be added for a {ta}:{tb} copper-zinc ratio?",
        f"An alloy of {a}:{b} weighing {mA} kg is combined with {mB} kg at {c}:{d}, losing {w1}% "
        f"and {w2}%. How much zinc is needed for a {ta}:{tb} ratio?",
        f"Scrap of {a}:{b} ({mA} kg) and {c}:{d} ({mB} kg) melts with {w1}% and {w2}% loss; "
        f"{draw} kg is removed and {cuadd} kg copper plus {znadd} kg zinc is added. Find copper percent.",
    )
    notes = (
        "Constituent metals are tracked through two wastages, a tap-off and an addition.",
        "A ratio-of-ratios is followed by wastage, tapping and zinc charging.",
        "The alloy ratio is reversed into the copper addition for a target Cu:Zn ratio.",
        "The zinc addition is solved backwards from a target ratio after wastage.",
        "Wastage, tapping and two metal additions precede the final percentage.",
    )
    return q("mam_alloy_ratio_of_ratios", v, texts[v], ans,
             _distractors_for(ans),
             _explain(notes[v], ans), x)


# ---------------------------------------------------------------------------
# 14. Three successive draw-offs with charging, boiling and back-calc.
# ---------------------------------------------------------------------------
def _solve_successive_ops(x):
    V = x["V"]
    sol = F(V * x["c"], 100)
    for o, rr in ((x["o1"], x["r1"]), (x["o2"], x["r2"]), (x["o3"], x["r3"])):
        if o:
            sol = sol * F(V - o, V) + F(o * rr, 100)
    sol += x["add"]
    vol = V - x["e"] + x["w"] + x["add"]
    if x["ask"] == "pct":
        return pct(F(sol * 100, vol))
    if x["ask"] == "reverse":
        return fmt(F(x["tp"] * vol - (x["tp"] + x["tq"]) * sol, x["tq"]))
    return ratio(sol, vol - sol)


def mam_successive_ops(r, v):
    rows = (
        (100, 50, 20, 0, 30, 100, 20, 40, 0, 0, 0, 0, 0, "ratio"),
        (120, 40, 30, 0, 20, 50, 40, 0, 10, 0, 0, 0, 0, "pct"),
        (150, 60, 30, 100, 40, 0, 30, 50, 0, 0, 0, 3, 2, "reverse"),
        (180, 25, 40, 0, 30, 100, 50, 0, 0, 20, 0, 0, 0, "ratio"),
        (200, 35, 50, 20, 40, 60, 30, 0, 0, 0, 15, 0, 0, "pct"),
    )
    (V, c, o1, r1, o2, r2, o3, r3, add, e, w, tp, tq, ask) = rows[v]
    x = {"V": V, "c": c, "o1": o1, "r1": r1, "o2": o2, "r2": r2,
         "o3": o3, "r3": r3, "add": add, "e": e, "w": w,
         "tp": tp, "tq": tq, "ask": ask}
    ans = _solve_successive_ops(x)
    texts = (
        f"A series of draw-offs acts on {V} L of {c}% milk: {o1} L replaced with water, {o2} L "
        f"with pure milk and {o3} L with a {r3}% mixture. Find the final milk:water ratio.",
        f"A jar of {V} L at {c}% has {o1} L, {o2} L and {o3} L successively replaced with "
        f"{r1}%, {r2}% and water, then {add} L milk is added. Find the milk percentage.",
        f"Three charges ({o1} L at {r1}%, {o2} L at {r2}%, {o3} L at {r3}%) are made in {V} L of "
        f"{c}% milk. How much milk gives a {tp}:{tq} ratio at the end?",
        f"In {V} L of {c}% milk, {o1} L is replaced with water, {o2} L with pure milk and {o3} L "
        f"with water, after which {e} L boils off. Find the milk:water ratio.",
        f"A {V} L jar at {c}% receives three replacements of {o1}, {o2} and {o3} L at {r1}%, "
        f"{r2}% and water, followed by {w} L water. Find the milk percent.",
    )
    notes = (
        "Three replacements with unlike fill liquids precede the ratio.",
        "Three replacements and a milk addition determine the percentage.",
        "After three replacements, the milk addition is reversed from the target ratio.",
        "Three replacements plus evaporation determine the final ratio.",
        "Three charges and a water addition are chained before the percentage.",
    )
    return q("mam_successive_ops", v, texts[v], ans,
             _distractors_for(ans),
             _explain(notes[v], ans), x)


# ---------------------------------------------------------------------------
# 15. Tea blends with wastage, mark-up, discount and reverse margin.
# ---------------------------------------------------------------------------
def _solve_tea_wastage_profit(x):
    cper = F(x["m"] * x["a"] + x["n"] * x["b"], x["m"] + x["n"])
    eff = F(cper * 100, 100 - x["w"])
    sp = F(x["mp"] * (100 - x["disc"]), 100)
    if x["ask"] == "pct":
        return pct(F((sp - eff) * 100, eff))
    if x["ask"] == "sell_needed":
        return money(F(eff * (100 + x["p"]), 100))
    if x["ask"] == "profit_total":
        return money(F(F(x["T"] * (100 - x["w"]), 100) * (sp - eff)))
    if x["ask"] == "mp_needed":
        return money(F(F(eff * (100 + x["p"]), 100) * 100, 100 - x["disc"]))
    return fmt(F(100 - F(cper * (100 + x["p"]), sp)))


def mam_tea_wastage_profit(r, v):
    rows = (
        (60, 90, 2, 1, 10, 99, 10, 0, 120, "pct"),
        (40, 70, 3, 2, 12, 0, 0, 25, 100, "sell_needed"),
        (50, 80, 1, 2, 8, 110, 5, 0, 150, "profit_total"),
        (30, 50, 3, 2, 15, 0, 20, 30, 100, "mp_needed"),
        (75, 100, 2, 3, 0, 105, 5, 5, 0, "wastage"),
    )
    (a, b, m, n, w, mp, disc, p, T, ask) = rows[v]
    x = {"a": a, "b": b, "m": m, "n": n, "w": w, "mp": mp,
         "disc": disc, "p": p, "T": T, "ask": ask}
    ans = _solve_tea_wastage_profit(x)
    texts = (
        f"Tea at ₹{a} and ₹{b} per kg is mixed {m}:{n}; {w}% of the blend is lost. Marked ₹{mp} "
        f"and sold at a {disc}% discount, find the effective profit percent.",
        f"A tea blend of {m}:{n} grades costing ₹{a} and ₹{b} suffers {w}% wastage. At what "
        f"price per kg should the saleable tea be sold for {p}% profit?",
        f"Tea grades at ₹{a} and ₹{b} per kg are blended {m}:{n} and {w}% is wasted. From {T} kg "
        f"purchased, marked ₹{mp} with a {disc}% discount, find the total profit.",
        f"A {m}:{n} tea blend of ₹{a} and ₹{b} grades wastes {w}%. For {p}% profit after a {disc}% "
        f"discount, what marked price per kg is needed?",
        f"Tea costing ₹{a} and ₹{b} per kg is blended {m}:{n}; marked ₹{mp} and sold at {disc}% "
        f"discount, what loss percent to stock makes the profit {p}%?",
    )
    notes = (
        "An effective wastage cost is compared with a discounted marked price.",
        "The wastage-loaded cost is reversed into a selling price for the target profit.",
        "Blend cost, wastage and discount combine in a total-profit calculation.",
        "A target profit is reversed through discount and wastage into a marked price.",
        "The wastage percentage itself is recovered from the target profit and selling price.",
    )
    return q("mam_tea_wastage_profit", v, texts[v], ans,
             _distractors_for(ans),
             _explain(notes[v], ans), x)


# ---------------------------------------------------------------------------
# 16. Three-vessel transfer cycle with evaporation, comparison and reverse.
# ---------------------------------------------------------------------------
def _solve_three_vessel_cycle(x):
    VA, VB, VC = x["VA"], x["VB"], x["VC"]
    a_sol = F(x["cA"] * (VA - x["x"]), 100)
    a_vol = VA - x["x"]
    b_sol = F(x["cB"] * VB, 100) + F(x["cA"] * x["x"], 100)
    b_vol = VB + x["x"]
    bc = F(b_sol * 100, b_vol)
    if x["y"]:
        moved = F(x["y"] * bc, 100)
        b_sol -= moved
        b_vol -= x["y"]
        c_sol = F(x["cC"] * VC, 100) + moved
    else:
        c_sol = F(x["cC"] * VC, 100)
    c_vol = VC + x["y"]
    cc = F(c_sol * 100, c_vol)
    if x["z"]:
        moved = F(x["z"] * cc, 100)
        c_sol -= moved
        c_vol -= x["z"]
        a_sol += moved
        a_vol += x["z"]
    ca, cb, ccf = F(a_sol * 100, a_vol), F(b_sol * 100, b_vol), F(c_sol * 100, c_vol)
    if x["ask"] == "diff":
        return fmt(abs(ca - cb))
    if x["ask"] == "reverse":
        return fmt(F(c_sol * 100, ca) - c_vol)
    if x["ask"] == "C":
        c_sol += x["add"]
        c_vol += x["add"] - x["e"]
        return pct(F(c_sol * 100, c_vol))
    if x["ask"] == "A":
        a_vol -= x["e"]
        return pct(F(a_sol * 100, a_vol))
    return pct(cb)


def mam_three_vessel_cycle(r, v):
    rows = (
        (100, 20, 80, 50, 120, 30, 20, 30, 10, 0, 15, "C"),
        (120, 40, 100, 10, 90, 60, 30, 20, 25, 0, 10, "A"),
        (150, 25, 120, 45, 100, 15, 40, 30, 20, 0, 0, "diff"),
        (180, 30, 140, 15, 110, 40, 40, 40, 50, 0, 0, "reverse"),
        (200, 15, 160, 35, 120, 25, 40, 0, 30, 12, 0, "C"),
    )
    (VA, cA, VB, cB, VC, cC, x, y, z, add, e, ask) = rows[v]
    vx = {"VA": VA, "cA": cA, "VB": VB, "cB": cB, "VC": VC, "cC": cC,
          "x": x, "y": y, "z": z, "add": add, "e": e, "ask": ask}
    ans = _solve_three_vessel_cycle(vx)
    texts = (
        f"Tanks A, B and C hold {VA} L at {cA}%, {VB} L at {cB}% and {VC} L at {cC}%. "
        f"Transfers of {x}, {y} and {z} L run A-B, B-C, C-A; then {e} L evaporates from C. "
        f"Find C's final strength.",
        f"A wash line has tanks A, B, C with {VA}, {VB} and {VC} L at {cA}%, {cB}% and {cC}%. "
        f"After transfers of {x}, {y} and {z} L around A-B-C-A and {e} L evaporation from A, "
        f"find A's strength.",
        f"Three tanks A, B, C contain {VA}, {VB}, {VC} L at {cA}%, {cB}%, {cC}%. Transfers of "
        f"{x}, {y}, {z} L go A to B, B to C and C to A. Find the difference between A and B "
        f"in percentage points.",
        f"Tanks A, B and C start with {VA}, {VB}, {VC} L at {cA}%, {cB}% and {cC}%. After a "
        f"{x}, {y}, {z} L cycle, how much water must join C to match A's strength?",
        f"A three-tank rig holds {VA} L at {cA}%, {VB} L at {cB}% and {VC} L at {cC}%. Only a "
        f"{x} L A-to-B and a {z} L C-to-A transfer occur, then {add} kg solute enters C. Find C's strength.",
    )
    notes = (
        "Each transfer uses the previously changed concentration, followed by evaporation.",
        "A three-transfer cycle and evaporation are chained.",
        "The cycle changes A and B differently and their strength gap is asked.",
        "After the full cycle, water addition to C is reversed from A's strength.",
        "A partial cycle plus solute addition determines C's final concentration.",
    )
    return q("mam_three_vessel_cycle", v, texts[v], ans,
             _distractors_for(ans),
             _explain(notes[v], ans), vx)


# ---------------------------------------------------------------------------
# 17. Salt pans: repeated boiling, crystal removal and reverse operations.
# ---------------------------------------------------------------------------
def _solve_crystallisation(x):
    salt = F(x["V"] * x["c"], 100) - x["p1"] - x["p2"] + x["sadd"]
    vol = x["V"] + x["w"] - x["e1"] - x["e2"] - x["p1"] - x["p2"] + x["sadd"]
    if x["ask"] == "pct":
        return pct(F(salt * 100, vol))
    if x["ask"] == "ratio":
        return ratio(salt, vol - salt)
    if x["ask"] == "reverse_salt":
        return fmt(F(x["t"] * vol - 100 * salt, 100 - x["t"]))
    if x["ask"] == "reverse_water":
        return fmt(vol - F(salt * 100, x["t"]))
    return fmt(F(F(x["V"] * x["c"], 100) * 100 - x["t"] * (x["V"] - x["e1"]),
                 100 - x["t"]))


def mam_crystallisation(r, v):
    rows = (
        (300, 20, 0, 50, 10, 40, 8, 5, 0, 0, "pct"),
        (250, 25, 20, 40, 15, 0, 0, 0, 0, 35, "reverse_salt"),
        (400, 18, 0, 60, 20, 0, 0, 0, 0, 25, "reverse_water"),
        (350, 22, 0, 50, 0, 0, 0, 0, 0, 20, "reverse_crystals"),
        (280, 24, 30, 30, 10, 20, 5, 0, 0, 0, "ratio"),
    )
    (V, c, w, e1, p1, e2, p2, sadd, spare, t, ask) = rows[v]
    x = {"V": V, "c": c, "w": w, "e1": e1, "p1": p1, "e2": e2,
         "p2": p2, "sadd": sadd, "t": t, "ask": ask}
    ans = _solve_crystallisation(x)
    texts = (
        f"A salt pan starts with {V} L at {c}%. Two boilings remove {e1} L and {e2} L, and "
        f"crystal harvests of {p1} kg and {p2} kg follow; {sadd} kg salt is then returned. Find the percent.",
        f"A pan of {V} L at {c}% gains {w} L water, loses {e1} L by boiling and yields {p1} kg of "
        f"crystals. How much salt must be dissolved to reach {t}%?",
        f"From {V} L at {c}%, {e1} L is boiled off and {p1} kg of crystals is removed. How much "
        f"more water must be boiled away to reach {t}%?",
        f"A {V} L pan at {c}% is boiled down by {e1} L. How many kilograms of crystals must be "
        f"removed for the remaining brine to be {t}%?",
        f"A pan of {V} L at {c}% gets {w} L water, loses {e1} L and {e2} L to boiling, and gives "
        f"{p1} kg and {p2} kg of crystals. Find the salt:water ratio.",
    )
    notes = (
        "Two evaporations and two crystal removals precede a salt return.",
        "Dilution, boiling and crystallisation precede a reverse salt-addition equation.",
        "The water still to be boiled off is found from the fixed salt mass.",
        "Crystal removal changes salt and volume together, so the amount is solved backwards.",
        "Two boiling-and-harvest cycles determine the final salt:water ratio.",
    )
    return q("mam_crystallisation", v, texts[v], ans,
             _distractors_for(ans),
             _explain(notes[v], ans), x)


# ---------------------------------------------------------------------------
# 19. Discounted purchases, wastage, selling price and reverse discount.
# ---------------------------------------------------------------------------
def _solve_discount_purchase_mix(x):
    cost = (F(x["a"] * x["x"] * (100 - x["d1"]), 100)
            + F(x["b"] * x["y"] * (100 - x["d2"]), 100))
    qty = x["x"] + x["y"]
    sell_qty = F(qty * (100 - x["w"]), 100)
    rev = F(sell_qty * x["z"])
    if x["ask"] == "pct":
        return pct(F((rev - cost) * 100, cost))
    if x["ask"] == "profit":
        return money(rev - cost)
    if x["ask"] == "cost":
        return money(cost)
    if x["ask"] == "sell_needed":
        return money(F((cost + x["target"]) * 100, sell_qty))
    other = F(x["b"] * x["y"] * (100 - x["d2"]), 100)
    allowed = F((rev - x["target"]) * 100 - other * 100, 100)
    return fmt(F(100 - F(allowed * 100, x["a"] * x["x"])))


def mam_discount_purchase_mix(r, v):
    rows = (
        (60, 90, 20, 30, 10, 0, 85, 5, 0, "pct"),
        (70, 100, 25, 25, 5, 0, 100, 8, 0, "profit"),
        (50, 80, 30, 20, 10, 10, 0, 6, 600, "sell_needed"),
        (55, 85, 24, 16, 8, 0, 78, 10, 0, "cost"),
        (60, 90, 20, 30, 0, 10, 90, 5, 800, "reverse_discount"),
    )
    (a, b, xx, y, d1, d2, z, w, target, ask) = rows[v]
    x = {"a": a, "b": b, "x": xx, "y": y, "d1": d1, "d2": d2,
         "z": z, "w": w, "target": target, "ask": ask}
    ans = _solve_discount_purchase_mix(x)
    d1_buy = "at full price" if d1 == 0 else f"with {d1}% concession"
    d2_buy = "at full price" if d2 == 0 else f"with {d2}% concession"
    d1_short = "no discount" if d1 == 0 else f"{d1}% discount"
    d2_short = "no discount" if d2 == 0 else f"{d2}% discount"
    texts = (
        f"An audit records {xx} kg of spice bought at ₹{a}/kg with {d1}% discount and {y} kg at "
        f"₹{b}/kg at full price. {w}% of the mixed lot is lost and the rest sells at ₹{z}/kg. Find profit percent.",
        f"A purchase of {xx} kg at ₹{a}/kg ({d1}% discount) and {y} kg at ₹{b}/kg is blended; "
        f"{w}% is spoiled and the balance sells at ₹{z}/kg. Find the profit.",
        f"Lots of {xx} kg at ₹{a}/kg and {y} kg at ₹{b}/kg attract {d1}% and {d2}% discounts. "
        f"After {w}% wastage, what selling price yields ₹{target} profit?",
        f"A buyer takes {xx} kg at ₹{a}/kg {d1_buy} and {y} kg at ₹{b}/kg {d2_buy}, "
        f"loses {w}% and sells at ₹{z}/kg. Find the purchase cost.",
        f"Two purchases of {xx} kg at ₹{a}/kg and {y} kg at ₹{b}/kg carry {d1_short} and "
        f"{d2_short}; after {w}% loss the lot sells at ₹{z}/kg for ₹{target} profit. Find the first discount.",
    )
    notes = (
        "Two discounted costs, wastage and revenue determine the profit rate.",
        "Discounted purchases and spoilage precede total profit.",
        "The selling price is reversed from a target profit after discounts and wastage.",
        "Concessions and wastage combine in the purchase cost.",
        "The first discount rate is recovered from a profit target after wastage and sales.",
    )
    return q("mam_discount_purchase_mix", v, texts[v], ans,
             _distractors_for(ans),
             _explain(notes[v], ans), x)


# ---------------------------------------------------------------------------
# 20. Stock limits, top-up solutes and withdrawal adjustments.
# ---------------------------------------------------------------------------
def _solve_availability_constraint(x):
    weak = F(x["T"] * (x["t"] - x["c1"]), x["c2"] - x["c1"])
    extra = F(x["T"] * x["t"] - x["qty"] * x["c2"]
              - (x["T"] - x["qty"]) * x["c1"], x["ac"] - x["c1"])
    revqty = F(x["T"] * (x["t"] - x["c1"]) - x["pc"] * 100,
               x["c2"] - x["c1"])
    replace = F(x["T"] * (x["t"] - x["t2"]), x["t"])
    replace_up = F(x["T"] * (x["t2"] - x["t"]), x["ac"] - x["t"])
    return fmt({"extra": extra, "weak": weak, "revqty": revqty,
                "replace": replace, "replace_up": replace_up}[x["ask"]])


def mam_availability_constraint(r, v):
    rows = (
        (10, 50, 30, 100, 0, 100, 20, 0, 0, "replace"),
        (10, 50, 30, 100, 30, 100, 0, 0, 0, "extra"),
        (15, 45, 30, 120, 0, 100, 0, 6, 0, "revqty"),
        (20, 60, 40, 150, 50, 80, 0, 0, 0, "extra"),
        (10, 50, 30, 100, 0, 60, 35, 0, 0, "replace_up"),
    )
    (c1, c2, t, T, qty, ac, t2, pc, spare, ask) = rows[v]
    x = {"c1": c1, "c2": c2, "t": t, "T": T, "qty": qty,
         "ac": ac, "t2": t2, "pc": pc, "ask": ask}
    ans = _solve_availability_constraint(x)
    texts = (
        f"A stock room has {c1}% and {c2}% feeds for {T} L of {t}% blend. After making it, some "
        f"blend is drawn off and replaced with water to reach {t2}%. Find the drawn volume.",
        f"Only {qty} L of the {c2}% feed is in stock for {T} L of {t}% blend made with {c1}% "
        f"feed. How much pure solute must top up the strength?",
        f"For {T} L of {t}% blend from {c1}% and {c2}% feeds, {pc} kg of pure solute is used. "
        f"How many litres of the strong feed were available?",
        f"A limited stock of {qty} L of {c2}% liquid is available for {T} L of {t}% blend from "
        f"{c1}% liquid, with {ac}% liquid as top-up. Find the top-up volume.",
        f"From {T} L of a {t}% stock blend, some is drawn off and replaced with {ac}% liquid to "
        f"reach {t2}%. Find the replaced volume.",
    )
    notes = (
        "Alligation sets the premix, then a withdrawal equation lowers the strength.",
        "A stock limit creates a solute deficit that must be reversed into a top-up.",
        "The quantity of strong feed is recovered from a known solute top-up.",
        "A scarce strong feed is supplemented with a concentrated liquid.",
        "A replacement with stronger liquid raises the strength after alligation.",
    )
    return q("mam_availability_constraint", v, texts[v], ans, near_num(_raw(ans), 2),
             _explain(notes[v], ans), x)


# ---------------------------------------------------------------------------
# 21. Fraction-based alligation with withdrawal and component reversals.
# ---------------------------------------------------------------------------
def _solve_ratio_of_ratios_selection(x):
    fa = F(x["a"], x["a"] + x["b"])
    fb = F(x["c"], x["c"] + x["d"])
    ft = F(x["p"], x["p"] + x["qq"])
    first = F(x["T"] * (fb - ft), fb - fa)
    second = x["T"] - first
    if x["draw"]:
        first = F(first * F(x["T"] - x["draw"], x["T"]))
        second = F(second * F(x["T"] - x["draw"], x["T"]))
        first += F(x["draw"] * x["rr"], x["rr"] + x["ss"])
        second += F(x["draw"] * x["ss"], x["rr"] + x["ss"])
    first += x["add"]
    if x["ask"] == "ratio":
        return ratio(first, second)
    if x["ask"] == "component":
        return fmt(first)
    if x["ask"] == "reverse_add":
        return fmt(F(x["tp"] * (first + second) - (x["tp"] + x["tq"]) * first, x["tq"]))
    return fmt(first if x["ask"] == "first" else second)


def mam_ratio_of_ratios_selection(r, v):
    rows = (
        (2, 1, 1, 1, 3, 2, 100, 20, 1, 1, 0, 0, 0, "ratio"),
        (3, 2, 1, 1, 5, 4, 120, 0, 1, 1, 10, 0, 0, "first"),
        (1, 1, 3, 2, 5, 4, 150, 30, 2, 1, 0, 0, 0, "component"),
        (4, 1, 1, 2, 3, 2, 180, 0, 1, 1, 0, 0, 0, "second"),
        (1, 3, 5, 2, 1, 1, 200, 0, 1, 1, 0, 3, 2, "reverse_add"),
    )
    (a, b, c, d, p, qq, T, draw, rr, ss, add, tp, tq, ask) = rows[v]
    x = {"a": a, "b": b, "c": c, "d": d, "p": p, "qq": qq, "T": T,
         "draw": draw, "rr": rr, "ss": ss, "add": add,
         "tp": tp, "tq": tq, "ask": ask}
    ans = _solve_ratio_of_ratios_selection(x)
    texts = (
        f"Jars P and Q contain milk fractions {a}/{a + b} and {c}/{c + d}. They are mixed to a "
        f"{p}:{qq} ratio, then {draw} L of the mix is replaced by a {rr}:{ss} mixture. Find the final ratio.",
        f"Jars P and Q hold milk:water {a}:{b} and {c}:{d}. A {T} L blend at {p}:{qq} is made and "
        f"{add} L of pure first-component is added. Find the final first-component volume in litres.",
        f"Two jars with {a}:{b} and {c}:{d} milk-water ratios make {T} L at {p}:{qq}. {draw} L is "
        f"then swapped for a {rr}:{ss} mixture. Find the first-component litres.",
        f"Jars of {a}:{b} and {c}:{d} are combined into {T} L at {p}:{qq}. Find the litres taken "
        f"from the second jar.",
        f"Two liquids at milk fractions {a}/{a + b} and {c}/{c + d} form {T} L at {p}:{qq}. "
        f"How much pure first-component gives a {tp}:{tq} ratio?",
    )
    notes = (
        "Fractional alligation is followed by a withdrawal and a fresh mixture charge.",
        "The alligation quantity is adjusted by a pure-component addition.",
        "Fraction alligation, a partial withdrawal and a replacement mixture are chained.",
        "Alligation on fractions returns the second jar's quantity.",
        "Alligation is followed by a reverse pure-component addition to a new ratio.",
    )
    return q("mam_ratio_of_ratios_selection", v, texts[v], ans,
             _distractors_for(ans),
             _explain(notes[v], ans), x)


# ---------------------------------------------------------------------------
# 22. Pre-treated vessels, combined mix, withdrawal and point comparisons.
# ---------------------------------------------------------------------------
def _solve_evap_pp_change(x):
    direct = F(x["V1"] * x["c1"] + x["V2"] * x["c2"], x["V1"] + x["V2"])
    a_sol = F(x["V1"] * x["c1"], 100)
    a_vol = x["V1"] - x["e1"] + x["w1"]
    b_sol = F(x["V2"] * x["c2"], 100) + x["s2"]
    b_vol = x["V2"] - x["e2"]
    sol = a_sol + b_sol
    vol = a_vol + b_vol
    if x["draw"]:
        sol = sol * F(vol - x["draw"], vol) + F(x["draw"] * x["r"], 100)
    if x["ask"] == "pp":
        return fmt(abs(F(sol * 100, vol) - direct))
    if x["ask"] == "reverse":
        return fmt(F(x["t"] * vol - 100 * sol, 100 - x["t"]))
    return pct(F(sol * 100, vol))


def mam_evap_pp_change(r, v):
    rows = (
        (100, 20, 100, 40, 20, 0, 0, 0, 20, 0, 0, "pp"),
        (120, 25, 80, 45, 0, 15, 25, 0, 0, 60, 0, "pp"),
        (150, 30, 100, 10, 0, 0, 20, 12, 0, 0, 36, "reverse"),
        (200, 15, 120, 35, 30, 20, 0, 0, 0, 0, 0, "final"),
        (180, 20, 140, 40, 0, 0, 15, 0, 25, 50, 0, "final"),
    )
    (V1, c1, V2, c2, e1, e2, w1, s2, draw, rr, t, ask) = rows[v]
    x = {"V1": V1, "c1": c1, "V2": V2, "c2": c2, "e1": e1, "e2": e2,
         "w1": w1, "s2": s2, "draw": draw, "r": rr, "t": t, "ask": ask}
    ans = _solve_evap_pp_change(x)
    texts = (
        f"Vessels A ({V1} L at {c1}%) and B ({V2} L at {c2}%) are pre-treated: {e1} L boils off "
        f"A, then both are mixed and {draw} L is replaced with water. Find the drop versus direct mixing, in points.",
        f"A ({V1} L, {c1}%) and B ({V2} L, {c2}%) are altered before blending: A gains {w1} L "
        f"water and B loses {e2} L. After mixing, find the drop from a direct blend, in points.",
        f"Vessels A ({V1} L at {c1}%) and B ({V2} L at {c2}%) are combined after A is diluted "
        f"by {w1} L and B gets {s2} kg solute. How much solute brings the blend to {t}%?",
        f"Two vessels with {V1} L at {c1}% and {V2} L at {c2}% each lose {e1} L and {e2} L by "
        f"boiling before mixing. Find the final percentage of the combined liquid.",
        f"A ({V1} L, {c1}%) receives {w1} L water and B ({V2} L, {c2}%) is unchanged; {draw} L "
        f"of the blend is then swapped for a {rr}% liquid. Find the final percent.",
    )
    notes = (
        "Pre-evaporation, mixing and a withdrawal cycle precede the point comparison.",
        "One vessel is diluted and the other concentrated before the point gap is taken.",
        "Pre-treatments are followed by a reverse solute equation on the combined liquid.",
        "Both vessels are concentrated before their combined strength is read.",
        "A pre-dilution and a replacement mixture determine the final percent.",
    )
    return q("mam_evap_pp_change", v, texts[v], ans,
             _distractors_for(ans),
             _explain(notes[v], ans), x)


# ---------------------------------------------------------------------------
# 23. Conditional valve rules applied over three branching stages.
# ---------------------------------------------------------------------------
def _solve_conditional_operations(x):
    milk = F(x["V"] * x["a"], x["a"] + x["b"])
    vol = F(x["V"])
    th = F(x["th"], x["thd"])
    for step in (x["x"], x["y"], x["z"]):
        if F(milk, vol) > th:
            milk = F(milk * (vol - step), vol)
        else:
            milk += step
            vol += step
    if x["ask"] == "reverse":
        return fmt(F(x["tp"] * vol - (x["tp"] + x["tq"]) * milk, x["tq"]))
    return pct(F(milk * 100, vol))


def mam_conditional_operations(r, v):
    rows = (
        (120, 3, 1, 30, 40, 20, 1, 2, 0, 0, "pct"),
        (120, 1, 3, 30, 30, 30, 1, 2, 0, 0, "pct"),
        (150, 2, 1, 40, 30, 0, 1, 2, 3, 2, "reverse"),
        (200, 3, 2, 50, 40, 30, 3, 5, 0, 0, "pct"),
        (100, 1, 1, 20, 40, 30, 1, 2, 0, 0, "pct"),
    )
    (V, a, b, xx, y, z, th, thd, tp, tq, ask) = rows[v]
    x = {"V": V, "a": a, "b": b, "x": xx, "y": y, "z": z,
         "th": th, "thd": thd, "tp": tp, "tq": tq, "ask": ask}
    ans = _solve_conditional_operations(x)
    step_count = "two" if z == 0 else "three"
    step_sizes = f"{xx} and {y} L" if z == 0 else f"{xx}, {y} and {z} L"
    texts = (
        f"An automated valve works on {V} L at milk:water {a}:{b}: if milk is above one half it "
        f"replaces {xx}, {y} and {z} L in turn with water, otherwise it adds that much milk. Find final percent.",
        f"A rule acts on {V} L at {a}:{b}: when milk exceeds half, replace the stated litres with "
        f"water, else add milk. It runs with {xx} L, {y} L and {z} L. Find the final milk percent.",
        f"Starting with {V} L at {a}:{b}, apply {step_count} conditional steps of {step_sizes}: "
        f"replace with water above half, add milk otherwise. How much milk gives a {tp}:{tq} ratio?",
        f"A {V} L vessel at {a}:{b} is tested against a {th}/{thd} milk threshold: replace "
        f"{xx}, {y} and {z} L with water when above it, else add milk. Find the final percent.",
        f"On {V} L of {a}:{b} liquid the controller runs three rounds ({xx}, {y}, {z} L) with "
        f"water replacement if milk is above the threshold, otherwise milk addition. Find the milk percentage.",
    )
    notes = (
        "Each of three branching steps depends on the milk fraction left by the previous one.",
        "Starting below half, the branches flip as milk is added over successive rounds.",
        "A conditional chain is followed by a reverse ratio adjustment.",
        "The threshold itself is changed, so the branch sequence must be re-tested each round.",
        "Three conditional rounds with distinct volumes determine the final percentage.",
    )
    return q("mam_conditional_operations", v, texts[v], ans,
             _distractors_for(ans),
             _explain(notes[v], ans), x)


# ---------------------------------------------------------------------------
# 24. Multi-stage stream: two fractions, solute, evaporation and reversals.
# ---------------------------------------------------------------------------
def _solve_multi_stage_ratio(x):
    sol = F(x["V"] * x["a"], x["a"] + x["b"])
    wat = x["V"] - sol
    sol = F(sol * (x["f1d"] - x["f1n"]), x["f1d"])
    wat = F(wat * (x["f1d"] - x["f1n"]), x["f1d"])
    sol += x["s"]
    wat = wat - x["e"] + x["w"]
    if x["f2n"]:
        sol = F(sol * (x["f2d"] - x["f2n"]), x["f2d"])
        wat = F(wat * (x["f2d"] - x["f2n"]), x["f2d"])
    sol += x["add2"]
    if x["ask"] == "pct":
        return pct(F(sol * 100, sol + wat))
    if x["ask"] == "reverse_solute":
        return fmt(F(x["tp"] * wat - x["tq"] * sol, x["tq"]))
    if x["ask"] == "reverse_water":
        return fmt(F((x["tp"] + x["tq"]) * sol - x["tp"] * (sol + wat), x["tp"]))
    return ratio(sol, wat)


def mam_multi_stage_ratio(r, v):
    rows = (
        (120, 3, 1, 1, 4, 10, 0, 0, 1, 0, 0, 0, 0, "ratio"),
        (150, 2, 1, 1, 3, 0, 20, 0, 1, 10, 5, 0, 0, "pct"),
        (240, 5, 3, 1, 4, 20, 30, 1, 5, 15, 0, 3, 1, "reverse_solute"),
        (200, 1, 1, 1, 5, 30, 20, 0, 1, 0, 0, 1, 1, "reverse_water"),
        (180, 4, 1, 1, 3, 15, 15, 1, 6, 12, 0, 0, 0, "ratio"),
    )
    (V, a, b, f1n, f1d, s, e, f2n, f2d, w, add2, tp, tq, ask) = rows[v]
    x = {"V": V, "a": a, "b": b, "f1n": f1n, "f1d": f1d, "s": s,
         "e": e, "f2n": f2n, "f2d": f2d, "w": w, "add2": add2,
         "tp": tp, "tq": tq, "ask": ask}
    ans = _solve_multi_stage_ratio(x)
    texts = (
        f"A process stream of {V} L at solute:water {a}:{b} loses {f1n}/{f1d} of itself, gains "
        f"{s} kg solute and is held. Find the final solute:water ratio.",
        f"A {V} L stream at {a}:{b} loses {f1n}/{f1d}, then {e} L of water evaporates, {w} L "
        f"water returns and {add2} kg solute is added. Find the solute percentage.",
        f"A stream of {V} L at {a}:{b} loses {f1n}/{f1d}, gets {s} kg solute, loses {e} L water "
        f"and {f2n}/{f2d} more, then gains {w} L water. How much solute gives a {tp}:{tq} ratio?",
        f"From {V} L at {a}:{b}, {f1n}/{f1d} is removed, {s} kg solute is added and {e} L water "
        f"boils off. How much water gives a {tp}:{tq} solute-water ratio?",
        f"A {V} L stream at {a}:{b} undergoes two fractional removals of {f1n}/{f1d} and "
        f"{f2n}/{f2d}, with {s} kg solute, {e} L evaporation and {w} L water in between. Find the ratio.",
    )
    notes = (
        "Fractional removal and solute addition change both components before the ratio.",
        "A fractional loss, evaporation, water return and solute addition are chained.",
        "A four-stage stream is followed by a reverse solute equation for a target ratio.",
        "After fraction, solute and evaporation, water addition is solved backwards.",
        "Two fractional removals with intermediate additions determine the ratio.",
    )
    return q("mam_multi_stage_ratio", v, texts[v], ans,
             _distractors_for(ans),
             _explain(notes[v], ans), x)


# ---------------------------------------------------------------------------
# 18. Two replacement mixtures, evaporation, topping and reverse milk.
# ---------------------------------------------------------------------------
def _solve_withdraw_readd(x):
    milk = F(x["V"] * x["a"], x["a"] + x["b"])
    milk = milk * F(x["V"] - x["x"], x["V"]) + F(x["x"] * x["sr"], x["sr"] + x["sd"])
    milk = milk * F(x["V"] - x["y"], x["V"]) + F(x["y"] * x["cr"], x["cr"] + x["cd"])
    milk += x["add"]
    vol = x["V"] - x["e"] + x["w"] + x["add"]
    if x["ask"] == "pct":
        return pct(F(milk * 100, vol))
    if x["ask"] == "reverse_milk":
        return fmt(F(x["tp"] * vol - (x["tp"] + x["tq"]) * milk, x["tq"]))
    return ratio(milk, vol - milk)


def mam_withdraw_readd(r, v):
    rows = (
        (3, 1, 120, 30, 0, 1, 30, 1, 1, 0, 0, 0, 0, 0, "ratio"),
        (2, 1, 150, 40, 1, 1, 30, 0, 1, 12, 20, 0, 0, 0, "pct"),
        (3, 2, 200, 50, 0, 1, 40, 3, 1, 0, 0, 0, 3, 2, "reverse_milk"),
        (5, 3, 240, 60, 0, 1, 30, 1, 0, 0, 25, 15, 0, 0, "pct"),
        (4, 1, 160, 40, 1, 0, 30, 0, 1, 0, 0, 10, 0, 0, "ratio"),
    )
    (a, b, V, xx, sr, sd, y, cr, cd, add, e, w, tp, tq, ask) = rows[v]
    x = {"a": a, "b": b, "V": V, "x": xx, "sr": sr, "sd": sd,
         "y": y, "cr": cr, "cd": cd, "add": add, "e": e, "w": w,
         "tp": tp, "tq": tq, "ask": ask}
    ans = _solve_withdraw_readd(x)
    texts = (
        f"A canteen vessel has {V} L of milk:water {a}:{b}. {xx} L is swapped for water and {y} L "
        f"for a 1:1 mixture. Find the final milk:water ratio.",
        f"A canteen vessel of {V} L at {a}:{b} has {xx} L replaced by an equal milk-water mix and "
        f"{y} L by water, then {e} L evaporates and {add} L milk is added. Find the milk percent.",
        f"From {V} L at {a}:{b}, {xx} L is replaced with water and {y} L with a {cr}:{cd} mix. "
        f"How much milk is needed for a {tp}:{tq} ratio?",
        f"A vessel of {V} L at {a}:{b} loses {xx} L to water, then {y} L is replaced with pure "
        f"milk, {e} L boils off and {w} L water is added. Find the milk percentage.",
        f"A canteen vessel holds {V} L at {a}:{b}. {xx} L is replaced with pure milk, {y} L with "
        f"water and {w} L water is added. Find the final milk:water ratio.",
    )
    notes = (
        "Two unlike replacement liquids are applied in sequence before the ratio.",
        "Two replacements, evaporation and a milk addition determine the percentage.",
        "After two replacements the milk addition is reversed from a target ratio.",
        "A replacement pair, evaporation and a water addition are chained.",
        "Two replacements and a water addition determine the final ratio.",
    )
    return q("mam_withdraw_readd", v, texts[v], ans,
             _distractors_for(ans),
             _explain(notes[v], ans), x)


FAMILIES = [
    mam_replacement_chain, mam_three_solution_mix, mam_evap_restore,
    mam_vessel_transfer, mam_price_profit_mix, mam_alloy_wastage,
    mam_dilution_recovery, mam_component_transfer_ratio, mam_fractional_replace,
    mam_percentage_point_change, mam_weighted_unknown, mam_two_stage_restriction,
    mam_alloy_ratio_of_ratios, mam_successive_ops, mam_tea_wastage_profit,
    mam_three_vessel_cycle, mam_crystallisation, mam_withdraw_readd,
    mam_discount_purchase_mix, mam_availability_constraint,
    mam_ratio_of_ratios_selection, mam_evap_pp_change,
    mam_conditional_operations, mam_multi_stage_ratio,
]


def build_mixture_alligation_mains():
    return build_specs(FAMILIES, mains=True)
