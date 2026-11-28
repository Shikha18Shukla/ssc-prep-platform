# -*- coding: utf-8 -*-
"""Independent formula sheet for Mixture and Alligation Set 7.

The verifier passes each family's exact ``inputs`` dict to the matching
lambda below. Nothing is imported from either chapter builder.
"""

from __future__ import annotations

from .formula_helpers import F, fmt, dec, pct, money, ratio


def _f2_mam_replacement_chain(x):
    V = x["V"]
    sol = F(x["c"] * V, 100)
    for d, rr in ((x["d1"], x["r1"]), (x["d2"], x["r2"]), (x["d3"], x["r3"])):
        if d:
            sol = sol * (V - d) / V + F(d * rr, 100)
    sol += x["s"]
    vol = V - x["w"] + x["s"]
    if x["ask"] == "target":
        return fmt(F(x["t"] * vol - 100 * sol, 100 - x["t"]))
    return pct(sol * 100 / vol)


def _f2_mam_three_solution_mix(x):
    vol0 = x["a"] + x["b"] + x["c"]
    solute = F(x["a"] * x["c1"] + x["b"] * x["c2"] + x["c"] * x["c3"], 100)
    vol = vol0 + x["y"] - x["e"]
    solute = solute * (vol0 - x["draw"]) / vol0 + F(x["draw"] * x["r"], 100)
    solute += F(x["y"] * x["c4"], 100) + x["add"]
    if x["ask"] == "pp":
        return fmt(abs(solute * 100 / vol - F(x["a"] * x["c1"] + x["b"] * x["c2"] + x["c"] * x["c3"], vol0)))
    if x["ask"] == "reverse":
        return fmt(F(x["t"] * vol - 100 * solute, 100 - x["t"]))
    return pct(solute * 100 / vol)


def _f2_mam_evap_restore(x):
    sol = F(x["V"] * x["c"], 100) - x["p1"] + x["s"]
    vol = x["V"] + x["w1"] - x["e1"] - x["p1"] + x["w2"] + x["s"]
    if x["ask"] == "evap_back":
        return fmt(vol - F(sol * 100, x["c"]))
    if x["ask"] == "solute_to":
        return fmt(F(x["t"] * vol - 100 * sol, 100 - x["t"]))
    return pct(sol * 100 / vol)


def _f2_mam_vessel_transfer(x):
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


def _f2_mam_price_profit_mix(x):
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


def _f2_mam_alloy_wastage(x):
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
    return pct(cu * 100 / mass)


def _f2_mam_dilution_recovery(x):
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
    return pct(sol * 100 / vol)


def _f2_mam_component_transfer_ratio(x):
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


def _f2_mam_fractional_replace(x):
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
        return pct(milk * 100 / vol)
    if x["ask"] == "reverse":
        return fmt(F(x["t"] * vol - 100 * milk, 100 - x["t"]))
    return ratio(milk, vol - milk)


def _f2_mam_percentage_point_change(x):
    sol = F(x["V"] * x["c"], 100)
    sol = sol * F(x["V"] - x["x"], x["V"]) + F(x["x"] * x["s"], 100)
    sol = sol * F(x["V"] - x["d2"], x["V"]) + F(x["d2"] * x["r2"], 100)
    vol = x["V"] - x["e"] + x["w"] + x["adds"]
    sol += x["adds"]
    if x["ask"] == "pp":
        return fmt(sol * 100 / vol - x["c"])
    if x["ask"] == "reverse":
        return fmt(F(x["t"] * vol - 100 * sol, 100 - x["t"]))
    return pct(sol * 100 / vol)


def _f2_mam_weighted_unknown(x):
    first = F(x["T"] * (x["b"] - x["t"]), x["b"] - x["a"])
    cost = F((first * x["a"] + (x["T"] - first) * x["b"]) * (100 - x["d"]), 100)
    qty = F(x["T"] * (100 - x["w"]), 100)
    if x["ask"] == "quantity":
        return fmt(first)
    if x["ask"] == "profit":
        return money(qty * x["s"] - cost)
    if x["ask"] == "sell_needed":
        return money(F(cost * (100 + x["p"]), 100 * qty))
    if x["ask"] == "reverse_price":
        return money(F(cost + x["target"], qty))
    return money(cost)


def _f2_mam_two_stage_restriction(x):
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


def _f2_mam_alloy_ratio_of_ratios(x):
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
        return pct(cu * 100 / mass)
    if x["ask"] == "reverse_cu":
        return fmt(F(x["ta"] * mass - (x["ta"] + x["tb"]) * cu, x["tb"]))
    return fmt(F(x["tb"] * mass - (x["ta"] + x["tb"]) * zn, x["ta"]))


def _f2_mam_successive_ops(x):
    V = x["V"]
    sol = F(V * x["c"], 100)
    for o, rr in ((x["o1"], x["r1"]), (x["o2"], x["r2"]), (x["o3"], x["r3"])):
        if o:
            sol = sol * F(V - o, V) + F(o * rr, 100)
    sol += x["add"]
    vol = V - x["e"] + x["w"] + x["add"]
    if x["ask"] == "pct":
        return pct(sol * 100 / vol)
    if x["ask"] == "reverse":
        return fmt(F(x["tp"] * vol - (x["tp"] + x["tq"]) * sol, x["tq"]))
    return ratio(sol, vol - sol)


def _f2_mam_tea_wastage_profit(x):
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


def _f2_mam_three_vessel_cycle(x):
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
        return pct(c_sol * 100 / c_vol)
    if x["ask"] == "A":
        a_vol -= x["e"]
        return pct(a_sol * 100 / a_vol)
    return pct(cb)


def _f2_mam_crystallisation(x):
    salt = F(x["V"] * x["c"], 100) - x["p1"] - x["p2"] + x["sadd"]
    vol = x["V"] + x["w"] - x["e1"] - x["e2"] - x["p1"] - x["p2"] + x["sadd"]
    if x["ask"] == "pct":
        return pct(salt * 100 / vol)
    if x["ask"] == "ratio":
        return ratio(salt, vol - salt)
    if x["ask"] == "reverse_salt":
        return fmt(F(x["t"] * vol - 100 * salt, 100 - x["t"]))
    if x["ask"] == "reverse_water":
        return fmt(vol - F(salt * 100, x["t"]))
    return fmt(F(F(x["V"] * x["c"], 100) * 100 - x["t"] * (x["V"] - x["e1"]),
                 100 - x["t"]))


def _f2_mam_discount_purchase_mix(x):
    cost = (F(x["a"] * x["x"] * (100 - x["d1"]), 100)
            + F(x["b"] * x["y"] * (100 - x["d2"]), 100))
    qty = x["x"] + x["y"]
    sell_qty = F(qty * (100 - x["w"]), 100)
    rev = F(sell_qty * x["z"])
    if x["ask"] == "pct":
        return pct(F((rev - cost) * 100, cost))
    if x["ask"] == "profit":
        return money(F(rev - cost))
    if x["ask"] == "cost":
        return money(cost)
    if x["ask"] == "sell_needed":
        return money(F((cost + x["target"]) * 100, sell_qty))
    other = F(x["b"] * x["y"] * (100 - x["d2"]), 100)
    allowed = F((rev - x["target"]) * 100 - other * 100, 100)
    return fmt(F(100 - F(allowed * 100, x["a"] * x["x"])))


def _f2_mam_availability_constraint(x):
    if x["ask"] == "weak":
        return fmt(F(x["T"] * (x["t"] - x["c1"]), x["c2"] - x["c1"]))
    if x["ask"] == "revqty":
        return fmt(F(x["T"] * (x["t"] - x["c1"]) - x["pc"] * 100,
                     x["c2"] - x["c1"]))
    if x["ask"] == "replace":
        return fmt(F(x["T"] * (x["t"] - x["t2"]), x["t"]))
    if x["ask"] == "replace_up":
        return fmt(F(x["T"] * (x["t2"] - x["t"]), x["ac"] - x["t"]))
    return fmt(F(x["T"] * x["t"] - x["qty"] * x["c2"]
                 - (x["T"] - x["qty"]) * x["c1"], x["ac"] - x["c1"]))


def _f2_mam_ratio_of_ratios_selection(x):
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
    if x["ask"] == "reverse_add":
        return fmt(F(x["tp"] * (first + second) - (x["tp"] + x["tq"]) * first, x["tq"]))
    if x["ask"] == "component":
        return fmt(first)
    return fmt(first if x["ask"] == "first" else second)


def _f2_mam_evap_pp_change(x):
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
        return fmt(abs(sol * 100 / vol - direct))
    if x["ask"] == "reverse":
        return fmt(F(x["t"] * vol - 100 * sol, 100 - x["t"]))
    return pct(sol * 100 / vol)


def _f2_mam_conditional_operations(x):
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
    return pct(milk * 100 / vol)


def _f2_mam_multi_stage_ratio(x):
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
        return pct(sol * 100 / (sol + wat))
    if x["ask"] == "reverse_solute":
        return fmt(F(x["tp"] * wat - x["tq"] * sol, x["tq"]))
    if x["ask"] == "reverse_water":
        return fmt(F((x["tp"] + x["tq"]) * sol - x["tp"] * (sol + wat), x["tp"]))
    return ratio(sol, wat)


def _f2_mam_withdraw_readd(x):
    milk = F(x["V"] * x["a"], x["a"] + x["b"])
    milk = milk * F(x["V"] - x["x"], x["V"]) + F(x["x"] * x["sr"], x["sr"] + x["sd"])
    milk = milk * F(x["V"] - x["y"], x["V"]) + F(x["y"] * x["cr"], x["cr"] + x["cd"])
    milk += x["add"]
    vol = x["V"] - x["e"] + x["w"] + x["add"]
    if x["ask"] == "pct":
        return pct(milk * 100 / vol)
    if x["ask"] == "reverse_milk":
        return fmt(F(x["tp"] * vol - (x["tp"] + x["tq"]) * milk, x["tq"]))
    return ratio(milk, vol - milk)


def _f_mad_vessel_totals(x):
    milk = x["x"] + x["p"]
    water = x["y"] + x["qty"]
    values = {"total": milk + water, "milk": milk, "water": water,
              "diff": abs(milk - water)}
    return fmt(values[x["ask"]])


def _f_mad_component_difference(x):
    values = {
        "milk_water": abs((x["x"] + x["p"]) - (x["y"] + x["qty"])),
        "between_milk": abs(x["x"] - x["p"]),
        "between_water": abs(x["y"] - x["qty"]),
        "total_milk": x["x"] + x["p"],
        "total_water": x["y"] + x["qty"],
    }
    return fmt(values[x["ask"]])


def _f_mad_percentage_split(x):
    milk = F(x["T"] * x["m"], 100)
    water = F(x["T"] * x["w"], 100)
    if x["ask"] == "milk":
        return fmt(milk)
    if x["ask"] == "water":
        return fmt(water)
    return fmt(abs(milk - water))


def _f_mad_milk_percent(x):
    numerator = x["x"] if x["ask"] == "milk" else x["y"]
    return pct(F(100 * numerator, x["x"] + x["y"]))


def _f_mad_shop_cost_diff(x):
    cost_a = F(x["a"] * x["x"])
    cost_b = F(x["b"] * x["y"])
    if x["ask"] == "diff":
        return money(abs(cost_a - cost_b))
    if x["ask"] == "A":
        return money(cost_a)
    if x["ask"] == "B":
        return money(cost_b)
    if x["ask"] == "total":
        return money(cost_a + cost_b)
    return ratio(cost_a, cost_b)


def _f_mad_simple_alligation(x):
    weak = F(x["T"] * (x["c2"] - x["t"]), x["c2"] - x["c1"])
    strong = F(x["T"] * (x["t"] - x["c1"]), x["c2"] - x["c1"])
    if x["ask"] == "ratio":
        return ratio(x["c2"] - x["t"], x["t"] - x["c1"])
    return fmt(weak if x["ask"] == "weak" else strong)


def _f_mad_missing_water(x):
    water_a = x["T"] - x["x"]
    total_b = x["y"] + x["z"]
    if x["ask"] == "water":
        return fmt(water_a)
    if x["ask"] == "total_A":
        return fmt(x["T"])
    return fmt(total_b)


def _f_mad_weighted_average(x):
    solute = F(x["V1"] * x["c1"] + x["V2"] * x["c2"], 100)
    combined = F(x["V1"] * x["c1"] + x["V2"] * x["c2"], x["V1"] + x["V2"])
    if x["ask"] == "combined":
        return pct(combined)
    return fmt(solute)


def _f_mad_combined_ratio(x):
    m1 = F(x["V"] * x["a"], x["a"] + x["b"])
    w1 = x["V"] - m1
    m2 = F(x["W"] * x["c"], x["c"] + x["d"])
    w2 = x["W"] - m2
    if x["ask"] == "ratio":
        return ratio(m1 + m2, w1 + w2)
    return fmt(m1 + m2 if x["ask"] == "milk" else w1 + w2)


def _f_mad_simple_evaporation(x):
    solute = F(x["V"] * x["c"], 100)
    water = x["V"] - solute - x["e"]
    if x["ask"] == "new_pct":
        return pct(solute * 100 / (x["V"] - x["e"]))
    return fmt(solute if x["ask"] == "solute" else water)


def _f_mad_simple_replacement(x):
    milk = F(x["c"] * (x["V"] - x["x"]), 100)
    water = x["V"] - milk
    if x["ask"] == "milk":
        return fmt(milk)
    if x["ask"] == "water":
        return fmt(water)
    return pct(milk * 100 / x["V"])


def _f_mad_addition_ratio(x):
    milk = x["x"] + x["m"]
    water = x["y"] + x["w"]
    if x["ask"] == "ratio":
        return ratio(milk, water)
    if x["ask"] == "milk":
        return fmt(milk)
    return pct(milk * 100 / (milk + water))


def _f_mad_average_cost(x):
    ca = F(x["a"] * x["x"])
    cb = F(x["b"] * x["y"])
    if x["ask"] == "avg":
        return money((ca + cb) / (x["x"] + x["y"]))
    if x["ask"] == "costA":
        return money(ca)
    if x["ask"] == "costB":
        return money(cb)
    return money(ca + cb)


def _f_mad_simple_profit(x):
    cost = F(x["c"] * x["qty"])
    rev = F(x["s"] * x["qty"])
    if x["ask"] == "profit":
        return money(rev - cost)
    if x["ask"] == "revenue":
        return money(rev)
    if x["ask"] == "cost":
        return money(cost)
    return pct(F((rev - cost) * 100, cost))


def _f_mad_pie_other(x):
    milk = F(x["T"] * x["m"], 100)
    water = F(x["T"] * x["w"], 100)
    other = F(x["T"] * (100 - x["m"] - x["w"]), 100)
    if x["ask"] == "other":
        return fmt(other)
    if x["ask"] == "milk":
        return fmt(milk)
    if x["ask"] == "water":
        return fmt(water)
    return fmt(abs(milk - water))


def _f_mad_avg_percent(x):
    values = [x["p1"], x["p2"], x["p3"], x["p4"]]
    avg = F(sum(values), 4)
    if x["ask"] == "avg":
        return pct(avg)
    if x["ask"] == "max":
        return pct(max(values))
    return fmt(max(values) - min(values))


def _f_mad_water_needed(x):
    add = F(100 * x["m"], x["t"]) - (x["m"] + x["w"])
    return fmt(add if x["ask"] == "water" else x["m"] + x["w"] + add)


def _f_mad_solute_needed(x):
    add = F(x["V"] * (x["t"] - x["c"]), 100 - x["t"])
    return fmt(add if x["ask"] == "solute" else F(x["V"] * x["c"], 100) + add)


def _f_mad_price_ratio(x):
    price_a = F(x["a"], x["x"])
    price_b = F(x["b"], x["y"])
    if x["ask"] == "ratio":
        return ratio(price_a, price_b)
    return money(price_a if x["ask"] == "A" else price_b)


def _f_mad_caselet_half(x):
    milk = F(x["x"], 2) + x["p"]
    water = F(x["y"], 2) + x["qty"]
    if x["ask"] == "ratio":
        return ratio(milk, water)
    return fmt(milk if x["ask"] == "milk" else water)


def _f_mad_discount_total(x):
    each = F(x["m"] * (100 - x["d"]), 100)
    if x["ask"] == "total":
        return money(each * x["qty"])
    if x["ask"] == "discount":
        return money(F(x["m"] * x["d"] * x["qty"], 100))
    return money(each)


def _f_mad_alloy_copper_mass(x):
    cu = F(x["x"] * x["a"] + x["y"] * x["b"], 100)
    zn = F(x["x"] * (100 - x["a"]) + x["y"] * (100 - x["b"]), 100)
    if x["ask"] == "ratio":
        return ratio(cu, zn)
    return fmt(cu if x["ask"] == "copper" else zn)


def _f_mad_double_replacement(x):
    milk = F(x["c"] * (x["V"] - x["x"]) * (x["V"] - x["x"]), x["V"] * x["V"])
    if x["ask"] == "pct":
        return pct(milk)
    return fmt(milk if x["ask"] == "milk" else x["V"] - milk)


def _f_mad_missing_price(x):
    qty_b = x["T"] - x["x"]
    price_b = F(x["C"] - x["x"] * x["a"], qty_b)
    if x["ask"] == "qtyB":
        return fmt(qty_b)
    if x["ask"] == "costA":
        return money(F(x["x"] * x["a"]))
    return money(price_b)


FORMULAS = {
    "mam_replacement_chain": lambda x: _f2_mam_replacement_chain(x),
    "mam_three_solution_mix": lambda x: _f2_mam_three_solution_mix(x),
    "mam_evap_restore": lambda x: _f2_mam_evap_restore(x),
    "mam_vessel_transfer": lambda x: _f2_mam_vessel_transfer(x),
    "mam_price_profit_mix": lambda x: _f2_mam_price_profit_mix(x),
    "mam_alloy_wastage": lambda x: _f2_mam_alloy_wastage(x),
    "mam_dilution_recovery": lambda x: _f2_mam_dilution_recovery(x),
    "mam_component_transfer_ratio": lambda x: _f2_mam_component_transfer_ratio(x),
    "mam_fractional_replace": lambda x: _f2_mam_fractional_replace(x),
    "mam_percentage_point_change": lambda x: _f2_mam_percentage_point_change(x),
    "mam_weighted_unknown": lambda x: _f2_mam_weighted_unknown(x),
    "mam_two_stage_restriction": lambda x: _f2_mam_two_stage_restriction(x),
    "mam_alloy_ratio_of_ratios": lambda x: _f2_mam_alloy_ratio_of_ratios(x),
    "mam_successive_ops": lambda x: _f2_mam_successive_ops(x),
    "mam_tea_wastage_profit": lambda x: _f2_mam_tea_wastage_profit(x),
    "mam_three_vessel_cycle": lambda x: _f2_mam_three_vessel_cycle(x),
    "mam_crystallisation": lambda x: _f2_mam_crystallisation(x),
    "mam_withdraw_readd": lambda x: _f2_mam_withdraw_readd(x),
    "mam_discount_purchase_mix": lambda x: _f2_mam_discount_purchase_mix(x),
    "mam_availability_constraint": lambda x: _f2_mam_availability_constraint(x),
    "mam_ratio_of_ratios_selection": lambda x: _f2_mam_ratio_of_ratios_selection(x),
    "mam_evap_pp_change": lambda x: _f2_mam_evap_pp_change(x),
    "mam_conditional_operations": lambda x: _f2_mam_conditional_operations(x),
    "mam_multi_stage_ratio": lambda x: _f2_mam_multi_stage_ratio(x),
    "mad_vessel_totals": lambda x: _f_mad_vessel_totals(x),
    "mad_component_difference": lambda x: _f_mad_component_difference(x),
    "mad_percentage_split": lambda x: _f_mad_percentage_split(x),
    "mad_milk_percent": lambda x: _f_mad_milk_percent(x),
    "mad_shop_cost_diff": lambda x: _f_mad_shop_cost_diff(x),
    "mad_simple_alligation": lambda x: _f_mad_simple_alligation(x),
    "mad_missing_water": lambda x: _f_mad_missing_water(x),
    "mad_weighted_average": lambda x: _f_mad_weighted_average(x),
    "mad_combined_ratio": lambda x: _f_mad_combined_ratio(x),
    "mad_simple_evaporation": lambda x: _f_mad_simple_evaporation(x),
    "mad_simple_replacement": lambda x: _f_mad_simple_replacement(x),
    "mad_addition_ratio": lambda x: _f_mad_addition_ratio(x),
    "mad_average_cost": lambda x: _f_mad_average_cost(x),
    "mad_simple_profit": lambda x: _f_mad_simple_profit(x),
    "mad_pie_other": lambda x: _f_mad_pie_other(x),
    "mad_avg_percent": lambda x: _f_mad_avg_percent(x),
    "mad_water_needed": lambda x: _f_mad_water_needed(x),
    "mad_solute_needed": lambda x: _f_mad_solute_needed(x),
    "mad_price_ratio": lambda x: _f_mad_price_ratio(x),
    "mad_caselet_half": lambda x: _f_mad_caselet_half(x),
    "mad_discount_total": lambda x: _f_mad_discount_total(x),
    "mad_alloy_copper_mass": lambda x: _f_mad_alloy_copper_mass(x),
    "mad_double_replacement": lambda x: _f_mad_double_replacement(x),
    "mad_missing_price": lambda x: _f_mad_missing_price(x),
}
