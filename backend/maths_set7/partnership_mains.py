# -*- coding: utf-8 -*-
"""Partnership (Mains) — 120 original, independently recomputed HARD questions."""

from __future__ import annotations

from .bank import fmt
from .common import F, build_specs, money, near_money, near_pct, pct, q, ratio

SOURCE = "Partnership Mains class notes (local PDF)"
PAGES = {
    1: 'cc2c97f4-4d95-4e6e-964f-d9318068eb13.pdf, pp. 4-5',
    2: 'cc2c97f4-4d95-4e6e-964f-d9318068eb13.pdf, pp. 6-8',
    3: 'cc2c97f4-4d95-4e6e-964f-d9318068eb13.pdf, pp. 9-12',
    4: 'cc2c97f4-4d95-4e6e-964f-d9318068eb13.pdf, pp. 4-13',
}


def pm_timeline_add_withdraw(r, v):
    cA, cB, add, am, wd, wm, P = (
        (120000, 90000, 30000, 7, 20000, 5, 254000),
        (150000, 120000, 30000, 4, 20000, 9, 343000),
        (180000, 150000, 60000, 10, 30000, 3, 384000),
        (200000, 160000, 40000, 6, 40000, 8, 440000),
        (240000, 200000, 60000, 8, 50000, 4, 513000),
    )[v]
    wa = cA * 12 + add * (13 - am)
    wb = cB * 12 - wd * (13 - wm)
    share = F(P * wa, wa + wb)
    naive = F(P * cA, cA + cB)
    return q(
        "pm_timeline_add_withdraw", v,
        f"A starts with Rs {cA} and B with Rs {cB}. A adds Rs {add} at the start of "
        f"month {am}, while B withdraws Rs {wd} at the start of month {wm}. The year's "
        f"profit is Rs {P}. Find A's share.",
        money(share), [money(naive), money(share + 5000), money(share - 5000)],
        f"A's time-weighted capital = {cA}*12 + {add}*{13 - am} = {wa}; B's = "
        f"{cB}*12 - {wd}*{13 - wm} = {wb}. A's share = {P}*{wa}/({wa}+{wb}) "
        f"= Rs {fmt(share)}; ignoring the timing changes would wrongly give Rs {fmt(naive)}.",
        {"cA": cA, "cB": cB, "add": add, "am": am, "wd": wd, "wm": wm, "P": P},
    )


def pm_late_join_withdraw_diff(r, v):
    cA, cB, jm, wd, wm, P = (
        (120000, 90000, 4, 30000, 6, 204000),
        (150000, 120000, 3, 20000, 8, 290000),
        (180000, 150000, 5, 60000, 10, 318000),
        (200000, 160000, 2, 40000, 7, 392000),
        (240000, 180000, 6, 60000, 9, 390000),
    )[v]
    wa = cA * 12 - wd * (13 - wm)
    wb = cB * (13 - jm)
    sa = F(P * wa, wa + wb)
    sb = F(P * wb, wa + wb)
    diff = abs(sa - sb)
    return q(
        "pm_late_join_withdraw_diff", v,
        f"A invests Rs {cA} for the year but withdraws Rs {wd} at the start of month "
        f"{wm}. B joins with Rs {cB} at the start of month {jm}. Profit is Rs {P}. "
        f"Find the absolute difference between their profit shares.",
        money(diff), [money(sa), money(sb), money(diff + 10000)],
        f"A's time-weighted capital = {cA}*12 - {wd}*{13 - wm} = {wa}; B's = "
        f"{cB}*{13 - jm} = {wb}. Shares are Rs {fmt(sa)} and Rs {fmt(sb)} after "
        f"division in {wa}:{wb}, so the difference is Rs {fmt(diff)}.",
        {"cA": cA, "cB": cB, "jm": jm, "wd": wd, "wm": wm, "P": P},
    )


def pm_working_salary_commission(r, v):
    cA, cB, P, basis, sal, months, rate, threshold = (
        (180000, 120000, 300000, "monthly", 8000, 12, 0, 0),
        (200000, 120000, 320000, "profit_pct", 0, 0, 15, 0),
        (240000, 160000, 360000, "excess_pct", 0, 0, 25, 200000),
        (300000, 100000, 480000, "monthly", 12000, 9, 0, 0),
        (270000, 180000, 500000, "excess_pct", 0, 0, 20, 250000),
    )[v]
    if basis == "monthly":
        remuneration = F(sal * months)
    elif basis == "profit_pct":
        remuneration = F(P * rate, 100)
    else:
        remuneration = F(max(0, P - threshold) * rate, 100)
    remainder = F(P) - remuneration
    share_b = F(remainder * cB, cA + cB)
    return q(
        "pm_working_salary_commission", v,
        f"A and B invest Rs {cA} and Rs {cB}. A works for the firm and is paid "
        f"{basis.replace('_', ' ')} ({sal} per month for {months} months / {rate}% "
        f"of profit / {rate}% of profit above Rs {threshold}) before the balance "
        f"profit of Rs {P} is split in capital ratio. Find B's share.",
        money(share_b), [money(F(P * cB, cA + cB)), money(share_b + 4000), money(share_b - 4000)],
        f"Working partner's remuneration is separated first: Rs {fmt(remuneration)} "
        f"({basis}). Balance = {P} - {fmt(remuneration)} = Rs {fmt(remainder)}; "
        f"B's share = {fmt(remainder)}*{cB}/({cA}+{cB}) = Rs {fmt(share_b)}.",
        {"cA": cA, "cB": cB, "P": P, "basis": basis, "sal": sal,
         "months": months, "rate": rate, "threshold": threshold},
    )


def pm_guaranteed_min_deficiency(r, v):
    a, b, c, P, guar, bearer = (
        (3, 2, 1, 360000, 200000, "B_only"),
        (4, 3, 1, 400000, 250000, "BC_ratio"),
        (5, 3, 2, 500000, 260000, "B_only"),
        (2, 3, 1, 300000, 120000, "BC_ratio"),
        (3, 4, 1, 540000, 240000, "B_only"),
    )[v]
    total = a + b + c
    raw_a = F(P * a, total)
    raw_b = F(P * b, total)
    shortfall = max(F(0), F(guar) - raw_a)
    burden = shortfall if bearer == "B_only" else F(shortfall * b, b + c)
    final_b = raw_b - burden
    return q(
        "pm_guaranteed_min_deficiency", v,
        f"A, B and C share profits in the ratio {a}:{b}:{c} out of Rs {P}. A is "
        f"guaranteed at least Rs {guar}. Any shortfall is borne by "
        f"{'B alone' if bearer == 'B_only' else 'B and C in their profit ratio'}. "
        f"Find B's final share.",
        money(final_b), [money(raw_b), money(final_b + 5000), money(final_b - 5000)],
        f"Raw shares: A = {P}*{a}/{total} = Rs {fmt(raw_a)}, B = Rs {fmt(raw_b)}. "
        f"Guarantee shortfall = {guar} - {fmt(raw_a)} = Rs {fmt(shortfall)}, borne by "
        f"{bearer}; B's burden = Rs {fmt(burden)}. B's final share = Rs {fmt(final_b)}.",
        {"a": a, "b": b, "c": c, "P": P, "guar": guar, "bearer": bearer},
    )


def pm_admission_new_ratio(r, v):
    a, b, new_share, na, nb, P = (
        (3, 2, 20, 3, 2, 300000),
        (3, 2, 25, 1, 1, 360000),
        (4, 3, 10, 4, 3, 420000),
        (5, 3, 30, 2, 1, 480000),
        (2, 1, 15, 3, 2, 520000),
    )[v]
    balance = F(P * (100 - new_share), 100)
    final_a = F(balance * na, na + nb)
    return q(
        "pm_admission_new_ratio", v,
        f"A and B share in {a}:{b}. A new partner is admitted for {new_share}% of "
        f"the profits, and the old partners then share the balance in {na}:{nb}. "
        f"With total profit Rs {P}, find A's final share.",
        money(final_a), [money(F(P * a, a + b)), money(final_a + 6000), money(final_a - 6000)],
        f"New partner's slice is {new_share}% of {P} = Rs {fmt(F(P * new_share, 100))}; "
        f"balance = Rs {fmt(balance)}. A's share = {fmt(balance)}*{na}/({na}+{nb}) "
        f"= Rs {fmt(final_a)}; the pre-admission ratio {a}:{b} applies only to the balance.",
        {"a": a, "b": b, "new_share": new_share, "na": na, "nb": nb, "P": P},
    )


def pm_retirement_split_share(r, v):
    a, b, c, retire, to_a, to_other, P = (
        (3, 2, 1, "B", 2, 1, 360000),
        (4, 3, 1, "C", 1, 0, 480000),
        (5, 3, 2, "B", 1, 1, 500000),
        (2, 3, 1, "C", 3, 2, 420000),
        (3, 4, 1, "B", 3, 1, 480000),
    )[v]
    total = a + b + c
    raw_a = F(P * a, total)
    outgoing = F(P * (b if retire == "B" else c), total)
    added = F(outgoing * to_a, to_a + to_other)
    final_a = raw_a + added
    return q(
        "pm_retirement_split_share", v,
        f"A, B and C share in {a}:{b}:{c}. Partner {retire} retires and that share "
        f"is assigned to the continuing partners in {to_a}:{to_other} (A first). "
        f"Find A's share of profit Rs {P} after retirement.",
        money(final_a), [money(raw_a), money(final_a + 5000), money(outgoing)],
        f"A's own share = {P}*{a}/{total} = Rs {fmt(raw_a)}. Retiring partner's share "
        f"= Rs {fmt(outgoing)}; A receives {to_a}/({to_a}+{to_other}) of it = "
        f"Rs {fmt(added)}. Final A share = Rs {fmt(final_a)}.",
        {"a": a, "b": b, "c": c, "retire": retire, "to_a": to_a,
         "to_other": to_other, "P": P},
    )


def pm_fractional_time_interest(r, v):
    cA, cB, an, ad, bn, bd, rate, P = (
        (120000, 120000, 2, 3, 3, 4, 10, 187000),
        (150000, 120000, 3, 4, 2, 3, 8, 207900),
        (180000, 150000, 1, 2, 5, 6, 12, 240800),
        (200000, 160000, 3, 5, 4, 5, 10, 272800),
        (240000, 180000, 2, 3, 1, 2, 15, 287500),
    )[v]
    wa, wb = F(cA * an, ad), F(cB * bn, bd)
    ia = F(cA * rate * an, 100 * ad)
    ib = F(cB * rate * bn, 100 * bd)
    balance = F(P) - ia - ib
    share_b = F(balance * wb, wa + wb)
    total_b = share_b + ib
    return q(
        "pm_fractional_time_interest", v,
        f"A invests Rs {cA} for {an}/{ad} of a year and B invests Rs {cB} for "
        f"{bn}/{bd} of a year. Interest on capital is allowed at {rate}% p.a. and "
        f"the remaining profit of Rs {P} is shared in time-weighted capital ratio. "
        f"Find B's total receipt.",
        money(total_b), [money(share_b), money(total_b + 5000), money(ib)],
        f"Time-weighted capitals are {fmt(wa)} and {fmt(wb)}. Interest is separated "
        f"first: A Rs {fmt(ia)}, B Rs {fmt(ib)}; balance = Rs {fmt(balance)}. "
        f"B's profit share = Rs {fmt(share_b)}; total receipt = Rs {fmt(total_b)}.",
        {"cA": cA, "cB": cB, "an": an, "ad": ad, "bn": bn, "bd": bd,
         "rate": rate, "P": P},
    )


def pm_loan_interest_tax_cess(r, v):
    cA, cB, loan, lender, rate, tax, cess, P = (
        (180000, 120000, 100000, "B", 12, 10, 2, 310776),
        (150000, 100000, 80000, "A", 10, 20, 3, 263352),
        (200000, 150000, 120000, "B", 15, 10, 1, 296182),
        (240000, 180000, 90000, "A", 8, 15, 5, 356066),
        (160000, 120000, 150000, "B", 10, 5, 4, 294220),
    )[v]
    gross = F(loan * rate, 100)
    tax_amt = F(gross * tax, 100)
    cess_amt = F(tax_amt * cess, 100)
    net_interest = gross - tax_amt - cess_amt
    balance = F(P) - net_interest
    capital_share = F(balance * cA, cA + cB)
    total_a = capital_share + (net_interest if lender == "A" else F(0))
    return q(
        "pm_loan_interest_tax_cess", v,
        f"A and B have capitals Rs {cA} and Rs {cB}. The firm takes a loan of "
        f"Rs {loan} from {lender} at {rate}% interest; tax of {tax}% and cess of "
        f"{cess}% on that tax are deducted from the interest. Profit before this "
        f"adjustment is Rs {P}. Find A's final receipt.",
        money(total_a), [money(capital_share), money(total_a + 5000), money(net_interest)],
        f"Gross interest = Rs {fmt(gross)}; tax = Rs {fmt(tax_amt)} and cess = "
        f"Rs {fmt(cess_amt)} are deducted, leaving net interest Rs {fmt(net_interest)} "
        f"(paid to {lender}). Balance for capital division = Rs {fmt(balance)}; "
        f"A's capital share = Rs {fmt(capital_share)} and total = Rs {fmt(total_a)}.",
        {"cA": cA, "cB": cB, "loan": loan, "lender": lender, "rate": rate,
         "tax": tax, "cess": cess, "P": P},
    )


def pm_reinvest_different_rates(r, v):
    cA, cB, P1, ra, rb, rateA, rateB, years, basis = (
        (180000, 120000, 150000, 3, 2, 10, 12, 2, "simple"),
        (180000, 120000, 150000, 3, 2, 8, 10, 2, "compound"),
        (180000, 120000, 150000, 3, 2, 12, 9, 3, "simple"),
        (180000, 120000, 150000, 3, 2, 10, 5, 2, "compound"),
        (180000, 120000, 150000, 3, 2, 15, 8, 4, "simple"),
    )[v]
    share_a = F(P1 * ra, ra + rb)
    share_b = F(P1 * rb, ra + rb)
    if basis == "simple":
        fa = 1 + F(rateA * years, 100)
        fb = 1 + F(rateB * years, 100)
    else:
        fa = (1 + F(rateA, 100)) ** years
        fb = (1 + F(rateB, 100)) ** years
    diff = abs(share_a * fa - share_b * fb)
    return q(
        "pm_reinvest_different_rates", v,
        f"A and B invest Rs {cA} and Rs {cB} and earn Rs {P1}, split in {ra}:{rb}. "
        f"Each reinvests his share for {years} years: A at {rateA}% and B at "
        f"{rateB}% p.a. on a {basis} interest basis. Find the difference between "
        f"their maturity amounts.",
        money(diff), [money(share_a), money(share_b), money(diff + 1000)],
        f"First profit split: A Rs {fmt(share_a)}, B Rs {fmt(share_b)}. Growth "
        f"factors are {fmt(fa)} and {fmt(fb)} ({basis}); maturities are "
        f"Rs {fmt(share_a * fa)} and Rs {fmt(share_b * fb)}, so the gap is Rs {fmt(diff)}.",
        {"cA": cA, "cB": cB, "P1": P1, "ra": ra, "rb": rb,
         "rateA": rateA, "rateB": rateB, "years": years, "basis": basis},
    )


def pm_target_bonus(r, v):
    P, target, a, b, bonus, basis = (
        (300000, 200000, 3, 2, 20, "excess_pct"),
        (360000, 250000, 5, 4, 10, "total_pct"),
        (420000, 400000, 3, 1, 50, "excess_pct"),
        (480000, 300000, 4, 1, 25, "flat"),
        (540000, 450000, 4, 2, 15, "total_pct"),
    )[v]
    if basis == "excess_pct":
        incentive = F(max(0, P - target) * bonus, 100)
    elif basis == "total_pct":
        incentive = F(P * bonus, 100)
    else:
        incentive = F(bonus)
    balance = F(P) - incentive
    share_b = F(balance * b, a + b)
    return q(
        "pm_target_bonus", v,
        f"A profit of Rs {P} is shared between A and B in {a}:{b}, but A first gets "
        f"a bonus of {bonus}% ({'of profit above Rs ' + str(target) if basis == 'excess_pct' else 'of total profit' if basis == 'total_pct' else 'flat Rs'}) "
        f"because the target Rs {target} is crossed. Find B's share.",
        money(share_b), [money(F(P * b, a + b)), money(share_b + 3000), money(incentive)],
        f"Target condition holds. Bonus is computed separately: Rs {fmt(incentive)} "
        f"({basis}); balance = Rs {fmt(balance)}. B receives {b}/({a}+{b}) of the "
        f"balance = Rs {fmt(share_b)}.",
        {"P": P, "target": target, "a": a, "b": b, "bonus": bonus, "basis": basis},
    )


def pm_three_overlapping(r, v):
    cA, cB, cC, jb, jc, wa_month, wd, P = (
        (180000, 120000, 90000, 4, 7, 9, 30000, 366000),
        (180000, 120000, 90000, 3, 5, 10, 60000, 390000),
        (240000, 180000, 120000, 5, 8, 6, 40000, 464000),
        (200000, 150000, 100000, 2, 6, 8, 50000, 450000),
        (300000, 200000, 150000, 4, 9, 7, 60000, 564000),
    )[v]
    wA = cA * 12 - wd * (13 - wa_month)
    wB = cB * (13 - jb)
    wC = cC * (13 - jc)
    share_c = F(P * wC, wA + wB + wC)
    return q(
        "pm_three_overlapping", v,
        f"A starts with Rs {cA}; B joins with Rs {cB} in month {jb}; C joins with "
        f"Rs {cC} in month {jc}. A withdraws Rs {wd} in month {wa_month}. Profit is "
        f"Rs {P}. Find C's share.",
        money(share_c), [money(F(P * wC, wA + wB)), money(share_c + 4000), money(F(P, 3))],
        f"Time-weighted capitals: A = {cA}*12 - {wd}*{13 - wa_month} = {wA}, "
        f"B = {cB}*{13 - jb} = {wB}, C = {cC}*{13 - jc} = {wC}. Total = "
        f"{wA + wB + wC}; C's share = {P}*{wC}/{wA + wB + wC} = Rs {fmt(share_c)}.",
        {"cA": cA, "cB": cB, "cC": cC, "jb": jb, "jc": jc,
         "wa_month": wa_month, "wd": wd, "P": P},
    )


def pm_reverse_total_share(r, v):
    cA, cB, jm, add, am, given, S = (
        (120000, 90000, 4, 30000, 7, "A", 162000),
        (150000, 120000, 3, 20000, 5, "B", 120000),
        (180000, 150000, 6, 60000, 10, "A", 234000),
        (200000, 160000, 5, 40000, 8, "B", 128000),
        (240000, 180000, 2, 60000, 6, "A", 324000),
    )[v]
    wA = cA * 12 + add * (13 - am)
    wB = cB * (13 - jm)
    known_weight = wA if given == "A" else wB
    total_profit = F(S * (wA + wB), known_weight)
    return q(
        "pm_reverse_total_share", v,
        f"A starts with Rs {cA} and adds Rs {add} in month {am}; B joins with "
        f"Rs {cB} in month {jm}. {given}'s profit share is Rs {S}. Find the total "
        f"profit for the year.",
        money(total_profit), [money(S * 2), money(total_profit + 10000), money(S + cB)],
        f"Time-weighted capitals are {wA} for A and {wB} for B, so weights are "
        f"{wA}:{wB}. Since {given}'s share is Rs {S}, total profit = "
        f"{S}*({wA}+{wB})/{known_weight} = Rs {fmt(total_profit)}.",
        {"cA": cA, "cB": cB, "jm": jm, "add": add, "am": am, "given": given, "S": S},
    )


def pm_reverse_unknown_capital(r, v):
    d, months, P, given, S = (
        (30000, 9, 279000, "B", 135000),
        (40000, 7, 313000, "B", 133000),
        (60000, 11, 480000, "A", 216000),
        (-30000, 10, 410000, "B", 170000),
        (50000, 5, 433000, "B", 145000),
    )[v]
    if given == "B":
        capital_a = F(d * months * (P - S), S * (12 + months) - P * months)
    else:
        capital_a = F(S * months * d, 12 * P - S * (12 + months))
    relation = f"Rs {d} more than" if d >= 0 else f"Rs {-d} less than"
    return q(
        "pm_reverse_unknown_capital", v,
        f"A invests x for 12 months; B invests {relation} x and stays in the "
        f"business for {months} months. Total profit is Rs {P} and {given}'s share "
        f"is Rs {S}. Find x, A's capital.",
        money(capital_a), [money(S), money(capital_a + 10000), money(capital_a - d)],
        f"Let A's capital be x, so B's is x{'+' if d >= 0 else '-'}{abs(d)} and "
        f"weights are 12x and {months}(x{'+' if d >= 0 else '-'}{abs(d)}). Solving "
        f"Rs {S} = {P} * (B's weight)/(total weight) gives x = Rs {fmt(capital_a)}.",
        {"d": d, "months": months, "P": P, "given": given, "S": S},
    )


def pm_equal_share_join_month(r, v):
    cA, cB, mode = (
        (120000, 180000, "equal"),
        (200000, 120000, "A_twice"),
        (100000, 240000, "B_twice"),
        (160000, 240000, "equal"),
        (180000, 120000, "A_twice"),
    )[v]
    if mode == "equal":
        join_after = 12 - F(12 * cA, cB)
    elif mode == "A_twice":
        join_after = 12 - F(12 * cA, 2 * cB)
    else:
        join_after = 12 - F(24 * cA, cB)
    condition = {"equal": "equal shares", "A_twice": "A's share twice B's",
                 "B_twice": "B's share twice A's"}[mode]
    return q(
        "pm_equal_share_join_month", v,
        f"A invests Rs {cA} for the full 12 months. B invests Rs {cB} later. "
        f"For {condition}, after how many months from the start must B join?",
        fmt(join_after),
        [fmt(join_after + 1), fmt(join_after - 1), fmt(12 - join_after)],
        f"Using time-weighted capitals, A's weight is {cA}*12 = {cA * 12}. For "
        f"{condition}, B's weight must be {fmt(F(cA * 12, 1 if mode == 'equal' else 2 if mode == 'A_twice' else 1))}"
        f"{'*2' if mode == 'B_twice' else ''} of the comparable base, so "
        f"{cB}*(12 - x) is set accordingly; solving gives x = {fmt(join_after)} months.",
        {"cA": cA, "cB": cB, "mode": mode},
    )


def pm_interest_capital_final_ratio(r, v):
    cA, cB, an, ad, bn, bd, rate, P, basis = (
        (120000, 90000, 12, 12, 9, 12, 10, 150000, "weighted"),
        (150000, 90000, 12, 12, 6, 12, 8, 139200, "capital"),
        (180000, 120000, 10, 12, 8, 12, 12, 257600, "weighted"),
        (150000, 100000, 12, 12, 6, 12, 10, 200000, "capital"),
        (200000, 150000, 9, 12, 12, 12, 8, 260000, "weighted"),
    )[v]
    wa, wb = F(cA * an, ad), F(cB * bn, bd)
    ia, ib = F(cA * rate * an, 100 * ad), F(cB * rate * bn, 100 * bd)
    balance = F(P) - ia - ib
    if basis == "weighted":
        sa, sb = F(balance * wa, wa + wb), F(balance * wb, wa + wb)
    else:
        sa, sb = F(balance * cA, cA + cB), F(balance * cB, cA + cB)
    final = ratio(ia + sa, ib + sb)
    return q(
        "pm_interest_capital_final_ratio", v,
        f"A invests Rs {cA} for {an}/{ad} year and B Rs {cB} for {bn}/{bd} year. "
        f"Interest at {rate}% p.a. is credited first; the balance of profit Rs {P} "
        f"is split in the {basis} capital ratio. Find the ratio of A's total receipt "
        f"to B's total receipt.",
        final, [ratio(wa, wb), ratio(cA, cB), ratio(ia, ib)],
        f"Time-weighted capitals are {fmt(wa)} and {fmt(wb)}. Interest: "
        f"A Rs {fmt(ia)}, B Rs {fmt(ib)}; balance = Rs {fmt(balance)}. Profit shares "
        f"are Rs {fmt(sa)} and Rs {fmt(sb)}; adding interest gives the ratio {final}.",
        {"cA": cA, "cB": cB, "an": an, "ad": ad, "bn": bn, "bd": bd,
         "rate": rate, "P": P, "basis": basis},
    )


def pm_manager_commission_three(r, v):
    cA, cB, cC, mA, mB, mC, P, manager, rate, basis, threshold = (
        (120000, 90000, 60000, 12, 9, 6, 261000, "A", 10, "gross", 0),
        (120000, 90000, 60000, 12, 9, 6, 276250, "C", 20, "excess", 200000),
        (150000, 120000, 90000, 12, 10, 5, 414000, "B", 12, "gross", 0),
        (180000, 150000, 120000, 12, 8, 4, 417500, "A", 20, "excess", 250000),
        (200000, 160000, 100000, 12, 9, 5, 457500, "C", 20, "excess", 340000),
    )[v]
    wA, wB, wC = cA * mA, cB * mB, cC * mC
    total_w = wA + wB + wC
    if basis == "gross":
        commission = F(P * rate, 100)
    else:
        commission = F(max(0, P - threshold) * rate, 100)
    balance = F(P) - commission
    weights = {"A": wA, "B": wB, "C": wC}
    share = F(balance * weights[manager], total_w)
    total_manager = share + commission
    return q(
        "pm_manager_commission_three", v,
        f"Capitals of A, B, C are Rs {cA}, Rs {cB}, Rs {cC} invested for {mA}, {mB} "
        f"and {mC} months. {manager} is the manager and receives {rate}% commission "
        f"on {'total profit' if basis == 'gross' else 'profit above Rs ' + str(threshold)} "
        f"before the balance of Rs {P} is divided by time-weighted capitals. "
        f"Find {manager}'s total receipt.",
        money(total_manager), [money(share), money(F(P * weights[manager], total_w)), money(commission)],
        f"Weights are {wA}:{wB}:{wC}. Commission is separated first: Rs {fmt(commission)}; "
        f"balance = Rs {fmt(balance)}. {manager}'s share of balance = Rs {fmt(share)}; "
        f"total receipt = Rs {fmt(total_manager)}.",
        {"cA": cA, "cB": cB, "cC": cC, "mA": mA, "mB": mB, "mC": mC,
         "P": P, "manager": manager, "rate": rate, "basis": basis, "threshold": threshold},
    )


def pm_successive_ratio_amendment(r, v):
    oa, ob, na, nb, change_month, P = (
        (3, 2, 1, 1, 5, 360000),
        (4, 3, 2, 1, 7, 378000),
        (5, 3, 1, 1, 6, 480000),
        (2, 1, 3, 2, 3, 300000),
        (3, 1, 2, 3, 8, 600000),
    )[v]
    early = F(oa, oa + ob) * change_month
    late = F(na, na + nb) * (12 - change_month)
    share_a = F(P, 12) * (early + late)
    return q(
        "pm_successive_ratio_amendment", v,
        f"A and B begin the year sharing in {oa}:{ob}. From the start of month "
        f"{change_month} they amend the ratio to {na}:{nb} for the rest of the year. "
        f"Find A's share of the annual profit Rs {P}.",
        money(share_a), [money(F(P * oa, oa + ob)), money(F(P * na, na + nb)), money(share_a + 5000)],
        f"The year is split into two periods: {change_month} months at {oa}:{ob} and "
        f"{12 - change_month} months at {na}:{nb}. A's weighted fraction = "
        f"({fmt(early)} + {fmt(late)})/12; share = Rs {fmt(share_a)}.",
        {"oa": oa, "ob": ob, "na": na, "nb": nb, "change_month": change_month, "P": P},
    )


def pm_partner_replacement(r, v):
    cA, cB, cC, month, fn, fd, P = (
        (180000, 120000, 90000, 5, 1, 1, 336000),
        (180000, 120000, 90000, 4, 1, 2, 387000),
        (180000, 120000, 90000, 7, 3, 4, 360000),
        (240000, 180000, 120000, 6, 1, 3, 546000),
        (200000, 150000, 100000, 9, 1, 2, 430000),
    )[v]
    wA = cA * 12
    wB = cB * (month - 1) + (cB - F(cB * fn, fd)) * (13 - month)
    wC = cC * (13 - month)
    share_c = F(P * wC, wA + wB + wC)
    return q(
        "pm_partner_replacement", v,
        f"A invests Rs {cA} all year; B invests Rs {cB} but withdraws {fn}/{fd} of "
        f"his capital at the start of month {month}, when C joins with Rs {cC}. "
        f"Find C's share of profit Rs {P}.",
        money(share_c), [money(F(P * cC, cA + cB + cC)), money(share_c + 4000), money(F(P, 3))],
        f"Time-weighted capitals: A = {wA}; B = {cB}*{month - 1} + "
        f"{fmt(cB - F(cB * fn, fd))}*{13 - month} = {fmt(wB)}; C = "
        f"{cC}*{13 - month} = {wC}. C's share = {P}*{wC}/({fmt(wA + wB + wC)}) "
        f"= Rs {fmt(share_c)}.",
        {"cA": cA, "cB": cB, "cC": cC, "month": month,
         "fn": fn, "fd": fd, "P": P},
    )


def pm_salary_commission_net(r, v):
    cA, cB, P, salary, rate, basis, threshold = (
        (180000, 120000, 300000, 24000, 10, "after_salary", 0),
        (270000, 90000, 350000, 30000, 8, "before_salary", 0),
        (250000, 100000, 400000, 20000, 20, "excess", 250000),
        (240000, 160000, 420000, 36000, 12, "after_salary", 0),
        (240000, 180000, 500000, 40000, 15, "before_salary", 0),
    )[v]
    if basis == "before_salary":
        commission = F(P * rate, 100)
    elif basis == "after_salary":
        commission = F((P - salary) * rate, 100)
    else:
        commission = F(max(0, P - threshold) * rate, 100)
    balance = F(P) - salary - commission
    share_b = F(balance * cB, cA + cB)
    return q(
        "pm_salary_commission_net", v,
        f"Capital ratio of working partner A to B is {cA}:{cB}. A gets a salary of "
        f"Rs {salary} plus {rate}% commission on "
        f"{'profit before salary' if basis == 'before_salary' else 'profit after salary' if basis == 'after_salary' else 'profit above Rs ' + str(threshold)}. "
        f"From profit Rs {P}, find B's share.",
        money(share_b), [money(F((P - salary) * cB, cA + cB)), money(share_b + 4000), money(commission)],
        f"Salary Rs {salary} is kept apart and commission on the stated basis is "
        f"Rs {fmt(commission)}; balance = {P} - {salary} - {fmt(commission)} = "
        f"Rs {fmt(balance)}. B's share = {fmt(balance)}*{cB}/({cA}+{cB}) = "
        f"Rs {fmt(share_b)}.",
        {"cA": cA, "cB": cB, "P": P, "salary": salary, "rate": rate,
         "basis": basis, "threshold": threshold},
    )


def pm_three_share_spread(r, v):
    cA, cB, cC, jB, jC, wd_month, wd, P = (
        (120000, 100000, 80000, 3, 6, 8, 20000, 290000),
        (120000, 100000, 80000, 5, 8, 10, 40000, 252000),
        (180000, 150000, 90000, 4, 7, 9, 30000, 393000),
        (200000, 160000, 120000, 2, 5, 6, 50000, 477000),
        (240000, 180000, 120000, 6, 9, 11, 60000, 450000),
    )[v]
    wA = cA * 12 - wd * (13 - wd_month)
    wB = cB * (13 - jB)
    wC = cC * (13 - jC)
    shares = [F(P * w, wA + wB + wC) for w in (wA, wB, wC)]
    spread = max(shares) - min(shares)
    return q(
        "pm_three_share_spread", v,
        f"A invests Rs {cA} but withdraws Rs {wd} in month {wd_month}; B joins with "
        f"Rs {cB} in month {jB} and C with Rs {cC} in month {jC}. Profit is Rs {P}. "
        f"Find the difference between the largest and smallest profit shares.",
        money(spread), [money(shares[0]), money(shares[2]), money(spread + 5000)],
        f"Time-weighted capitals are {wA}, {wB} and {wC}. The three shares are "
        f"Rs {fmt(shares[0])}, Rs {fmt(shares[1])} and Rs {fmt(shares[2])}; "
        f"their spread is Rs {fmt(spread)}.",
        {"cA": cA, "cB": cB, "cC": cC, "jB": jB, "jC": jC,
         "wd_month": wd_month, "wd": wd, "P": P},
    )


def pm_guarantee_time_weighted(r, v):
    cA, cB, cC, jB, jC, P, guar, bearer = (
        (120000, 90000, 60000, 4, 7, 261000, 170000, "ratio"),
        (150000, 120000, 90000, 3, 6, 363000, 200000, "equal"),
        (180000, 150000, 90000, 5, 8, 381000, 249000, "ratio"),
        (200000, 160000, 120000, 2, 6, 500000, 280000, "equal"),
        (240000, 180000, 120000, 4, 9, 498000, 323000, "ratio"),
    )[v]
    wA, wB, wC = cA * 12, cB * (13 - jB), cC * (13 - jC)
    total_w = wA + wB + wC
    raw_a, raw_b = F(P * wA, total_w), F(P * wB, total_w)
    shortfall = max(F(0), F(guar) - raw_a)
    burden = shortfall / 2 if bearer == "equal" else F(shortfall * wB, wB + wC)
    final_b = raw_b - burden
    return q(
        "pm_guarantee_time_weighted", v,
        f"A (Rs {cA}, full year), B (Rs {cB}, from month {jB}) and C "
        f"(Rs {cC}, from month {jC}) share Rs {P} by time-weighted capital. "
        f"A is guaranteed Rs {guar}; any shortfall is borne "
        f"{'equally by B and C' if bearer == 'equal' else 'by B and C in their time-weighted ratio'}. "
        f"Find B's final share.",
        money(final_b), [money(raw_b), money(final_b + 5000), money(raw_a)],
        f"Weights are {wA}:{wB}:{wC}. Raw shares A Rs {fmt(raw_a)}, B Rs {fmt(raw_b)}; "
        f"guarantee shortfall = Rs {fmt(shortfall)}, borne {bearer}, so B's burden is "
        f"Rs {fmt(burden)}. B's final share = Rs {fmt(final_b)}.",
        {"cA": cA, "cB": cB, "cC": cC, "jB": jB, "jC": jC,
         "P": P, "guar": guar, "bearer": bearer},
    )


def pm_tax_cess_profit_split(r, v):
    cA, cB, jB, P, tax, cess, basis = (
        (180000, 120000, 4, 300000, 10, 2, "gross_profit"),
        (150000, 100000, 4, 360000, 12, 5, "partner_share"),
        (240000, 180000, 6, 517500, 8, 1, "gross_profit"),
        (200000, 120000, 5, 336000, 15, 2, "partner_share"),
        (300000, 200000, 3, 560000, 10, 4, "gross_profit"),
    )[v]
    wA, wB = cA * 12, cB * (13 - jB)
    total_w = wA + wB
    if basis == "gross_profit":
        tax_amt = F(P * tax, 100)
        cess_amt = F(tax_amt * cess, 100)
        receipt_a = F((P - tax_amt - cess_amt) * wA, total_w)
    else:
        raw_a = F(P * wA, total_w)
        tax_amt = F(raw_a * tax, 100)
        cess_amt = F(tax_amt * cess, 100)
        receipt_a = raw_a - tax_amt - cess_amt
    return q(
        "pm_tax_cess_profit_split", v,
        f"A invests Rs {cA} for 12 months and B invests Rs {cB} from month {jB}. "
        f"Profit is Rs {P}; tax of {tax}% with a {cess}% cess on the tax is deducted "
        f"{'from total profit before division' if basis == 'gross_profit' else 'from each partner share'}. "
        f"Find A's net receipt.",
        money(receipt_a), [money(F(P * wA, total_w)), money(receipt_a + 5000), money(tax_amt)],
        f"Weights are {wA}:{wB}. Tax Rs {fmt(tax_amt)} and cess Rs {fmt(cess_amt)} "
        f"are handled separately ({basis}); A's net receipt after the capital split "
        f"and deductions is Rs {fmt(receipt_a)}.",
        {"cA": cA, "cB": cB, "jB": jB, "P": P, "tax": tax,
         "cess": cess, "basis": basis},
    )


def pm_reverse_total_difference(r, v):
    cA, cB, jB, wd, wm, S = (
        (120000, 90000, 4, 30000, 8, 48000),
        (150000, 120000, 3, 20000, 9, 52000),
        (180000, 150000, 5, 60000, 10, 78000),
        (200000, 160000, 2, 40000, 7, 40000),
        (240000, 180000, 6, 60000, 11, 150000),
    )[v]
    wA = cA * 12 - wd * (13 - wm)
    wB = cB * (13 - jB)
    total_profit = F(S * (wA + wB), abs(wA - wB))
    return q(
        "pm_reverse_total_difference", v,
        f"A invests Rs {cA} and withdraws Rs {wd} in month {wm}; B joins with "
        f"Rs {cB} in month {jB}. The gap between their profit shares is Rs {S}. "
        f"Find the total profit.",
        money(total_profit), [money(S * 4), money(total_profit + 10000), money(S + cA)],
        f"Time-weighted capitals are {wA} for A and {wB} for B. The share gap "
        f"corresponds to weight gap {abs(wA - wB)} out of {wA + wB}; hence total "
        f"profit = {S}*({wA}+{wB})/{abs(wA - wB)} = Rs {fmt(total_profit)}.",
        {"cA": cA, "cB": cB, "jB": jB, "wd": wd, "wm": wm, "S": S},
    )


def pm_capstone_guarantee_bonus(r, v):
    cA, cB, cC, jB, jC, salary, rate, basis, target, guar, P = (
        (120000, 90000, 60000, 4, 7, 30000, 10, "excess", 201000, 45000, 301000),
        (150000, 120000, 90000, 3, 6, 40000, 25, "net", 0, 80000, 524000),
        (180000, 150000, 90000, 5, 8, 50000, 20, "excess", 300000, 73000, 463750),
        (200000, 160000, 120000, 2, 6, 60000, 20, "net", 0, 110000, 685000),
        (240000, 180000, 120000, 4, 9, 70000, 20, "excess", 350000, 65000, 622500),
    )[v]
    wA, wB, wC = cA * 12, cB * (13 - jB), cC * (13 - jC)
    total_w = wA + wB + wC
    if basis == "net":
        bonus = F((P - salary) * rate, 100)
    else:
        bonus = F(max(0, P - target) * rate, 100)
    balance = F(P) - salary - bonus
    raw_b = F(balance * wB, total_w)
    raw_c = F(balance * wC, total_w)
    shortfall = max(F(0), F(guar) - raw_c)
    burden = F(shortfall * wB, wA + wB)
    final_b = raw_b - burden
    return q(
        "pm_capstone_guarantee_bonus", v,
        f"Capitals are Rs {cA}, Rs {cB} (from month {jB}) and Rs {cC} "
        f"(from month {jC}). A gets a salary of Rs {salary} and a {rate}% bonus on "
        f"{'profit after salary' if basis == 'net' else 'profit above Rs ' + str(target)}. "
        f"C is guaranteed Rs {guar}, with any shortfall borne by A and B in their "
        f"time-weighted ratio. From profit Rs {P}, find B's final share.",
        money(final_b), [money(raw_b), money(F(P * wB, total_w)), money(final_b + 5000)],
        f"Weights are {wA}:{wB}:{wC}. Salary Rs {salary} and bonus Rs {fmt(bonus)} "
        f"are removed first, leaving Rs {fmt(balance)}. Raw shares B Rs {fmt(raw_b)}, "
        f"C Rs {fmt(raw_c)}; C's guarantee shortfall Rs {fmt(shortfall)} puts "
        f"Rs {fmt(burden)} of burden on B, so B ends with Rs {fmt(final_b)}.",
        {"cA": cA, "cB": cB, "cC": cC, "jB": jB, "jC": jC,
         "salary": salary, "rate": rate, "basis": basis, "target": target,
         "guar": guar, "P": P},
    )


FAMILIES = (
    pm_timeline_add_withdraw,
    pm_late_join_withdraw_diff,
    pm_working_salary_commission,
    pm_guaranteed_min_deficiency,
    pm_admission_new_ratio,
    pm_retirement_split_share,
    pm_fractional_time_interest,
    pm_loan_interest_tax_cess,
    pm_reinvest_different_rates,
    pm_target_bonus,
    pm_three_overlapping,
    pm_reverse_total_share,
    pm_reverse_unknown_capital,
    pm_equal_share_join_month,
    pm_interest_capital_final_ratio,
    pm_manager_commission_three,
    pm_successive_ratio_amendment,
    pm_partner_replacement,
    pm_salary_commission_net,
    pm_three_share_spread,
    pm_guarantee_time_weighted,
    pm_tax_cess_profit_split,
    pm_reverse_total_difference,
    pm_capstone_guarantee_bonus,
)


def build_partnership_mains():
    return build_specs(FAMILIES, mains=True)
