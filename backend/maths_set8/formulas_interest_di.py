# -*- coding: utf-8 -*-
"""Independent answer sheet for Simple and Compound Interest DI (Set 8).

The verifier passes ``verification_data.inputs`` to these formulas. This sheet
recomputes every answer from scratch and imports nothing from the builders.
"""

from __future__ import annotations

from .formula_helpers import F, fmt, money, pct


def _si(principal, rate, years):
    return F(principal) * F(rate) * F(years) / F(100)


def _ci_amount(principal, rate, years):
    return F(principal) * (F(1) + F(rate, 100)) ** int(years)


def _ci_periodic(principal, rate, per_year, years):
    return F(principal) * (F(1) + F(rate, 100 * per_year)) ** (per_year * int(years))


def _cid_principal_rate(d):
    interest = _si(d["principal"], d["rate"], d["years"])
    return money(interest if d["ask"] == "si" else F(d["principal"]) + interest)


def _cid_si_lookup(d):
    yearly = F(d["principal"]) * F(d["rate"]) / F(100)
    full = _si(d["principal"], d["rate"], d["years"])
    if d["ask"] == "yearly_si":
        return money(yearly)
    if d["ask"] == "si":
        return money(full)
    return money(F(d["principal"]) + full)


def _cid_ci_lookup(d):
    amount = _ci_amount(d["principal"], d["rate"], d["years"])
    return money(amount if d["ask"] == "amount" else amount - F(d["principal"]))


def _cid_amount_lookup(d):
    principal = F(d["principal"])
    if d["ask"] == "si":
        return money(principal + _si(principal, d["rate"], d["years"]))
    return money(_ci_amount(principal, d["rate"], d["years"]))


def _cid_si_ci_gap(d):
    principal = F(d["principal"])
    simple = _si(principal, d["rate"], d["years"])
    compound = _ci_amount(principal, d["rate"], d["years"]) - principal
    if d["ask"] == "gap":
        return money(compound - simple)
    if d["ask"] == "si":
        return money(simple)
    return money(compound)


def _cid_rate_table(d):
    interest = F(d["amount"]) - F(d["principal"])
    if d["ask"] == "si":
        return money(interest)
    return pct(interest * F(100) / (F(d["principal"]) * F(d["years"])))


def _cid_time_table(d):
    if d["ask"] == "amount":
        return money(F(d["principal"]) + F(d["interest"]))
    return fmt(F(d["interest"]) * F(100) / (F(d["principal"]) * F(d["rate"])))


def _cid_two_deposits(d):
    i1 = _si(d["p1"], d["r1"], d["years"])
    i2 = _si(d["p2"], d["r2"], d["years"])
    if d["ask"] == "total_si":
        return money(i1 + i2)
    if d["ask"] == "diff":
        return money(abs(i1 - i2))
    return money(F(d["p1"]) + F(d["p2"]) + i1 + i2)


def _cid_half_yearly(d):
    amount = _ci_periodic(d["principal"], d["rate"], 2, d["years"])
    return money(amount if d["ask"] == "amount" else amount - F(d["principal"]))


def _cid_quarterly(d):
    amount = _ci_periodic(d["principal"], d["rate"], 4, d["years"])
    return money(amount if d["ask"] == "amount" else amount - F(d["principal"]))


def _cid_successive(d):
    final = F(d["principal"]) * (F(1) + F(d["r1"], 100)) * (F(1) + F(d["r2"], 100))
    return money(final if d["ask"] == "amount" else final - F(d["principal"]))


def _cid_withdrawal(d):
    before = _si(d["principal"], d["rate"], d["after"])
    reduced = F(d["principal"]) - F(d["withdraw"])
    after = _si(reduced, d["rate"], d["years"] - d["after"])
    interest = before + after
    if d["ask"] == "interest":
        return money(interest)
    return money(reduced + interest)


def _cid_addition(d):
    before = _si(d["principal"], d["rate"], d["after"])
    increased = F(d["principal"]) + F(d["addition"])
    after = _si(increased, d["rate"], d["years"] - d["after"])
    interest = before + after
    if d["ask"] == "interest":
        return money(interest)
    return money(increased + interest)


def _cid_population(d):
    final = F(d["population"]) * (F(1) + F(d["rate"], 100)) ** int(d["years"])
    return fmt(final if d["ask"] == "population" else final - F(d["population"]))


def _cid_ratio_invest(d):
    denominator = F(d["r1"] + d["r2"])
    first = F(d["total"]) * F(d["r1"]) / denominator
    second = F(d["total"]) * F(d["r2"]) / denominator
    i1 = _si(first, d["r1"], d["years"])
    i2 = _si(second, d["r2"], d["years"])
    if d["ask"] == "first_interest":
        return money(i1)
    if d["ask"] == "second_interest":
        return money(i2)
    return money(i1 + i2)


def _cid_effective(d):
    r1, r2 = F(d["r1"]), F(d["r2"])
    effective = r1 + r2 + r1 * r2 / F(100)
    amount = F(d["principal"]) * (F(1) + r1 / F(100)) * (F(1) + r2 / F(100))
    if d["ask"] == "effective":
        return pct(effective)
    if d["ask"] == "amount":
        return money(amount)
    return money(amount - F(d["principal"]))


def _cid_installment_factor(d):
    interest = _si(d["principal"], d["rate"], d["installments"])
    if d["ask"] == "total_interest":
        return money(interest)
    return money((F(d["principal"]) + interest) / F(d["installments"]))


def _cid_recurring(d):
    months = F(d["months"])
    interest = F(d["deposit"]) * months * (months + F(1)) / F(2) * F(d["rate"]) / F(1200)
    if d["ask"] == "interest":
        return money(interest)
    return money(F(d["deposit"]) * months + interest)


def _cid_discount_rate(d):
    discount = F(d["face"]) * F(d["rate"]) * F(d["months"]) / F(1200)
    if d["ask"] == "discount":
        return money(discount)
    return money(F(d["face"]) - discount)


def _cid_simple_growth(d):
    first = _si(d["principal"], d["r1"], d["change_after"])
    second = _si(d["principal"], d["r2"], d["change_after"])
    if d["ask"] == "first":
        return money(first)
    if d["ask"] == "second":
        return money(second)
    return money(first + second)


def _cid_interest_share(d):
    interest = _si(d["principal"], d["rate"], d["years"])
    if d["ask"] == "interest":
        return money(interest)
    if d["ask"] == "total":
        return money(F(d["principal"]) + interest)
    return pct(interest * F(100) / F(d["other"]))


def _cid_target_amount(d):
    interest = F(d["target"]) - F(d["principal"])
    if d["ask"] == "interest":
        return money(interest)
    return fmt(interest * F(100) / (F(d["principal"]) * F(d["rate"])))


def _cid_mixed_period(d):
    first = _si(d["principal"], d["rate"], 1)
    second = _si(F(d["principal"]) + F(d["extra"]), d["rate"], 1)
    if d["ask"] == "first":
        return money(first)
    if d["ask"] == "second":
        return money(second)
    if d["ask"] == "total":
        return money(first + second)
    return money(F(d["principal"]) + F(d["extra"]) + first + second)


def _cid_comparison(d):
    i1 = _si(d["p1"], d["r1"], d["t1"])
    i2 = _si(d["p2"], d["r2"], d["t2"])
    if d["ask"] == "A_interest":
        return money(i1)
    if d["ask"] == "B_interest":
        return money(i2)
    if d["ask"] == "difference":
        return money(abs(i1 - i2))
    return money(i1 + i2)


FORMULAS = {
    "cid_principal_rate": _cid_principal_rate,
    "cid_si_lookup": _cid_si_lookup,
    "cid_ci_lookup": _cid_ci_lookup,
    "cid_amount_lookup": _cid_amount_lookup,
    "cid_si_ci_gap": _cid_si_ci_gap,
    "cid_rate_table": _cid_rate_table,
    "cid_time_table": _cid_time_table,
    "cid_two_deposits": _cid_two_deposits,
    "cid_half_yearly": _cid_half_yearly,
    "cid_quarterly": _cid_quarterly,
    "cid_successive": _cid_successive,
    "cid_withdrawal": _cid_withdrawal,
    "cid_addition": _cid_addition,
    "cid_population": _cid_population,
    "cid_ratio_invest": _cid_ratio_invest,
    "cid_effective": _cid_effective,
    "cid_installment_factor": _cid_installment_factor,
    "cid_recurring": _cid_recurring,
    "cid_discount_rate": _cid_discount_rate,
    "cid_simple_growth": _cid_simple_growth,
    "cid_interest_share": _cid_interest_share,
    "cid_target_amount": _cid_target_amount,
    "cid_mixed_period": _cid_mixed_period,
    "cid_comparison": _cid_comparison,
}
