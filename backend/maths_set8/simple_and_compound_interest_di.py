# -*- coding: utf-8 -*-
"""Simple and Compound Interest – Data Interpretation — 120 Prelims-level questions."""

from __future__ import annotations

from fractions import Fraction

from .common import (
    F,
    build_specs,
    data,
    fmt,
    make_family,
    money,
    near_money,
    near_num,
    near_pct,
    pct,
    table,
)

SOURCE_PDF = "f5b22d88-8d5a-494e-b7b2-9e5b1b05d260.pdf"
PAGES = {
    1: f"{SOURCE_PDF}, pp. 2-4",
    2: f"{SOURCE_PDF}, pp. 5-7",
    3: f"{SOURCE_PDF}, pp. 8-10",
    4: f"{SOURCE_PDF}, pp. 11-13",
}


# ---------------------------------------------------------------------------
# Shared calculation and option helpers (builder side only).
# ---------------------------------------------------------------------------

def _si(principal, rate, years):
    return F(principal) * F(rate) * F(years) / F(100)


def _ci_amount(principal, rate, years):
    return F(principal) * (F(1) + F(rate, 100)) ** int(years)


def _ci_periodic(principal, rate, per_year, years):
    return F(principal) * (F(1) + F(rate, 100 * per_year)) ** (per_year * int(years))


def _step(value):
    value = abs(Fraction(str(value)))
    if value >= 100000:
        return F(1000)
    if value >= 10000:
        return F(500)
    if value >= 1000:
        return F(100)
    if value >= 100:
        return F(25)
    return F(5)


def _money_value(text):
    return Fraction(str(text).replace("₹", "").replace(",", "").strip())


def _pct_value(text):
    return Fraction(str(text).replace("%", "").strip())


def _money_distract(result, d):
    value = _money_value(result)
    return near_money(value, _step(value))


def _num_distract(result, d):
    return near_num(Fraction(str(result)), _step(result))


def _pct_distract(result, d):
    return near_pct(_pct_value(result), F(5))


def _mixed_distract(result, d):
    if d["ask"] in ("rate", "rate_percent", "effective", "share", "effective_rate"):
        return _pct_distract(result, d)
    if d["ask"] in ("years", "time"):
        return _num_distract(result, d)
    return _money_distract(result, d)


def _explain_inputs(d, correct, note):
    shown = table([(key, value) for key, value in d.items() if key != "ask"])
    return f"Using {shown}, {note} Hence the required value is {correct}."


# ---------------------------------------------------------------------------
# 1. cid_principal_rate
# ---------------------------------------------------------------------------

def _t1(d):
    block = data([
        ("principal", money(d["principal"])),
        ("rate", pct(d["rate"])),
        ("years", d["years"]),
    ])
    return f"{block} Find {'the simple interest' if d['ask'] == 'si' else 'the amount at the end'}."


def _a1(d):
    interest = _si(d["principal"], d["rate"], d["years"])
    return money(interest if d["ask"] == "si" else F(d["principal"]) + interest)


cid_principal_rate = make_family(
    "cid_principal_rate",
    ("principal", "rate", "years", "ask"),
    [
        (12000, 5, 2, "si"),
        (18000, 6, 3, "amount"),
        (25000, 4, 2, "si"),
        (15000, 8, 3, "amount"),
        (36000, 5, 4, "si"),
    ],
    _t1,
    _a1,
    distract=_money_distract,
    explain=lambda d, c: _explain_inputs(
        d, c, "simple interest is principal × rate × years ÷ 100, and the amount adds this interest to the principal."
    ),
)


# ---------------------------------------------------------------------------
# 2. cid_si_lookup
# ---------------------------------------------------------------------------

ASK2 = {
    "si": "the simple interest for the full period",
    "yearly_si": "the simple interest earned in one year",
    "amount": "the amount at the end of the period",
}


def _t2(d):
    block = data([
        ("deposit", money(d["principal"])),
        ("rate", pct(d["rate"])),
        ("years", d["years"]),
    ])
    return f"{block} Find {ASK2[d['ask']]}."


def _a2(d):
    yearly = F(d["principal"]) * F(d["rate"]) / F(100)
    full = _si(d["principal"], d["rate"], d["years"])
    if d["ask"] == "yearly_si":
        return money(yearly)
    if d["ask"] == "si":
        return money(full)
    return money(F(d["principal"]) + full)


cid_si_lookup = make_family(
    "cid_si_lookup",
    ("principal", "rate", "years", "ask"),
    [
        (9000, 6, 2, "si"),
        (24000, 5, 3, "yearly_si"),
        (15000, 4, 5, "amount"),
        (36000, 7, 2, "si"),
        (12500, 8, 4, "yearly_si"),
    ],
    _t2,
    _a2,
    distract=_money_distract,
    explain=lambda d, c: _explain_inputs(
        d, c, "one year's interest is principal × rate ÷ 100; multiplying by the years gives total interest, and adding it to the principal gives the amount."
    ),
)


# ---------------------------------------------------------------------------
# 3. cid_ci_lookup
# ---------------------------------------------------------------------------

ASK3 = {"ci": "the compound interest", "amount": "the compound amount"}


def _t3(d):
    block = data([
        ("principal", money(d["principal"])),
        ("rate", pct(d["rate"])),
        ("years", d["years"]),
    ])
    return f"{block} Find {ASK3[d['ask']]}."


def _a3(d):
    amount = _ci_amount(d["principal"], d["rate"], d["years"])
    return money(amount if d["ask"] == "amount" else amount - F(d["principal"]))


cid_ci_lookup = make_family(
    "cid_ci_lookup",
    ("principal", "rate", "years", "ask"),
    [
        (10000, 10, 2, "ci"),
        (8000, 5, 2, "amount"),
        (20000, 10, 3, "ci"),
        (12000, 20, 2, "ci"),
        (15000, 4, 2, "amount"),
    ],
    _t3,
    _a3,
    distract=_money_distract,
    explain=lambda d, c: _explain_inputs(
        d, c, "the compound amount is principal × (1 + rate/100)^years and compound interest is the amount minus the principal."
    ),
)


# ---------------------------------------------------------------------------
# 4. cid_amount_lookup
# ---------------------------------------------------------------------------

ASK4 = {
    "si": "the amount using simple interest",
    "ci": "the amount using compound interest",
}


def _t4(d):
    block = data([
        ("principal", money(d["principal"])),
        ("rate", pct(d["rate"])),
        ("years", d["years"]),
    ])
    return f"{block} Find {ASK4[d['ask']]}."


def _a4(d):
    principal = F(d["principal"])
    if d["ask"] == "si":
        return money(principal + _si(principal, d["rate"], d["years"]))
    return money(_ci_amount(principal, d["rate"], d["years"]))


cid_amount_lookup = make_family(
    "cid_amount_lookup",
    ("principal", "rate", "years", "ask"),
    [
        (20000, 5, 2, "si"),
        (10000, 10, 2, "ci"),
        (40000, 6, 3, "si"),
        (25000, 8, 2, "ci"),
        (18000, 12, 2, "si"),
    ],
    _t4,
    _a4,
    distract=_money_distract,
    explain=lambda d, c: _explain_inputs(
        d, c, "simple amount is principal plus principal × rate × years ÷ 100, while compound amount is principal × (1 + rate/100)^years."
    ),
)


# ---------------------------------------------------------------------------
# 5. cid_si_ci_gap
# ---------------------------------------------------------------------------

ASK5 = {
    "gap": "the excess of compound interest over simple interest",
    "si": "the simple interest",
    "ci": "the compound interest",
}


def _t5(d):
    block = data([
        ("deposit principal", money(d["principal"])),
        ("annual rate", pct(d["rate"])),
        ("duration (years)", d["years"]),
    ])
    return f"{block} Find {ASK5[d['ask']]}."


def _a5(d):
    principal = F(d["principal"])
    simple = _si(principal, d["rate"], d["years"])
    compound = _ci_amount(principal, d["rate"], d["years"]) - principal
    if d["ask"] == "gap":
        return money(compound - simple)
    if d["ask"] == "si":
        return money(simple)
    return money(compound)


cid_si_ci_gap = make_family(
    "cid_si_ci_gap",
    ("principal", "rate", "years", "ask"),
    [
        (30000, 10, 2, "gap"),
        (20000, 5, 2, "si"),
        (40000, 8, 2, "ci"),
        (15000, 12, 2, "gap"),
        (25000, 6, 2, "si"),
    ],
    _t5,
    _a5,
    distract=_money_distract,
    explain=lambda d, c: _explain_inputs(
        d, c, "compute simple interest as P × r × t ÷ 100 and compound interest as P × (1 + r/100)^t − P; the gap is their difference."
    ),
)


# ---------------------------------------------------------------------------
# 6. cid_rate_table
# ---------------------------------------------------------------------------

ASK6 = {"rate": "the rate of simple interest per annum", "si": "the simple interest earned"}


def _t6(d):
    block = data([
        ("principal", money(d["principal"])),
        ("amount", money(d["amount"])),
        ("years", d["years"]),
    ])
    return f"{block} Find {ASK6[d['ask']]}."


def _a6(d):
    interest = F(d["amount"]) - F(d["principal"])
    if d["ask"] == "si":
        return money(interest)
    rate = interest * F(100) / (F(d["principal"]) * F(d["years"]))
    return pct(rate)


cid_rate_table = make_family(
    "cid_rate_table",
    ("principal", "amount", "years", "ask"),
    [
        (10000, 12000, 2, "rate"),
        (20000, 26000, 3, "si"),
        (15000, 19500, 2, "rate"),
        (25000, 35000, 4, "si"),
        (18000, 23400, 3, "rate"),
    ],
    _t6,
    _a6,
    distract=_mixed_distract,
    explain=lambda d, c: _explain_inputs(
        d, c, "simple interest equals amount minus principal, and the yearly rate is interest × 100 ÷ (principal × years)."
    ),
)


# ---------------------------------------------------------------------------
# 7. cid_time_table
# ---------------------------------------------------------------------------

ASK7 = {"years": "the number of years", "amount": "the amount at the end"}


def _t7(d):
    block = data([
        ("principal", money(d["principal"])),
        ("rate", pct(d["rate"])),
        ("interest", money(d["interest"])),
    ])
    return f"{block} Find {ASK7[d['ask']]}."


def _a7(d):
    if d["ask"] == "amount":
        return money(F(d["principal"]) + F(d["interest"]))
    return fmt(F(d["interest"]) * F(100) / (F(d["principal"]) * F(d["rate"])))


cid_time_table = make_family(
    "cid_time_table",
    ("principal", "rate", "interest", "ask"),
    [
        (10000, 5, 1500, "years"),
        (20000, 8, 6400, "years"),
        (15000, 6, 2700, "amount"),
        (25000, 4, 3000, "years"),
        (12000, 10, 3600, "amount"),
    ],
    _t7,
    _a7,
    distract=_mixed_distract,
    explain=lambda d, c: _explain_inputs(
        d, c, "time in years is interest × 100 ÷ (principal × rate); the amount is principal plus interest."
    ),
)


# ---------------------------------------------------------------------------
# 8. cid_two_deposits
# ---------------------------------------------------------------------------

ASK8 = {
    "total_si": "the total simple interest from both deposits",
    "total_amount": "the combined amount from both deposits",
    "diff": "the positive difference between the two interest amounts",
}


def _t8(d):
    block = data([
        ("deposit A", money(d["p1"])),
        ("rate A", pct(d["r1"])),
        ("deposit B", money(d["p2"])),
        ("rate B", pct(d["r2"])),
        ("years", d["years"]),
    ])
    return f"{block} Find {ASK8[d['ask']]}."


def _a8(d):
    i1 = _si(d["p1"], d["r1"], d["years"])
    i2 = _si(d["p2"], d["r2"], d["years"])
    if d["ask"] == "total_si":
        return money(i1 + i2)
    if d["ask"] == "diff":
        return money(abs(i1 - i2))
    return money(F(d["p1"]) + F(d["p2"]) + i1 + i2)


cid_two_deposits = make_family(
    "cid_two_deposits",
    ("p1", "p2", "r1", "r2", "years", "ask"),
    [
        (10000, 15000, 5, 6, 2, "total_si"),
        (20000, 12000, 4, 5, 3, "total_amount"),
        (25000, 15000, 6, 4, 2, "diff"),
        (30000, 20000, 5, 8, 2, "total_si"),
        (18000, 12000, 10, 5, 3, "total_amount"),
    ],
    _t8,
    _a8,
    distract=_money_distract,
    explain=lambda d, c: _explain_inputs(
        d, c, "each deposit earns principal × rate × years ÷ 100; add the two interests (or the two principals and interests) as asked."
    ),
)


# ---------------------------------------------------------------------------
# 9. cid_half_yearly
# ---------------------------------------------------------------------------

ASK9 = {"ci": "the compound interest", "amount": "the compound amount"}


def _t9(d):
    block = data([
        ("principal", money(d["principal"])),
        ("annual rate", pct(d["rate"])),
        ("years", d["years"]),
        ("compounds per year", 2),
    ])
    return f"{block} Find {ASK9[d['ask']]} when interest is compounded half-yearly."


def _a9(d):
    amount = _ci_periodic(d["principal"], d["rate"], 2, d["years"])
    return money(amount if d["ask"] == "amount" else amount - F(d["principal"]))


cid_half_yearly = make_family(
    "cid_half_yearly",
    ("principal", "rate", "years", "ask"),
    [
        (20000, 10, 1, "ci"),
        (40000, 8, 1, "amount"),
        (10000, 20, 2, "ci"),
        (25000, 12, 1, "ci"),
        (32000, 20, 1, "amount"),
    ],
    _t9,
    _a9,
    distract=_money_distract,
    explain=lambda d, c: _explain_inputs(
        d, c, "half-yearly compounding uses half the annual rate per half-year and twice as many periods: P × (1 + r/200)^(2t)."
    ),
)


# ---------------------------------------------------------------------------
# 10. cid_quarterly
# ---------------------------------------------------------------------------

ASK10 = {"ci": "the compound interest", "amount": "the compound amount"}


def _t10(d):
    block = data([
        ("principal", money(d["principal"])),
        ("annual rate", pct(d["rate"])),
        ("years", d["years"]),
        ("compounds per year", 4),
    ])
    return f"{block} Find {ASK10[d['ask']]} when interest is compounded quarterly."


def _a10(d):
    amount = _ci_periodic(d["principal"], d["rate"], 4, d["years"])
    return money(amount if d["ask"] == "amount" else amount - F(d["principal"]))


cid_quarterly = make_family(
    "cid_quarterly",
    ("principal", "rate", "years", "ask"),
    [
        (320000, 20, 1, "ci"),
        (50000, 40, 1, "amount"),
        (160000, 20, 1, "amount"),
        (20000, 40, 1, "ci"),
        (40000, 40, 1, "ci"),
    ],
    _t10,
    _a10,
    distract=_money_distract,
    explain=lambda d, c: _explain_inputs(
        d, c, "quarterly compounding uses one-fourth of the annual rate per quarter and four times as many periods: P × (1 + r/400)^(4t)."
    ),
)


# ---------------------------------------------------------------------------
# 11. cid_successive
# ---------------------------------------------------------------------------

ASK11 = {"amount": "the final amount", "gain": "the total percentage gain in rupees"}


def _t11(d):
    block = data([
        ("principal", money(d["principal"])),
        ("first increase", pct(d["r1"])),
        ("second increase", pct(d["r2"])),
    ])
    return f"{block} Find {ASK11[d['ask']]} after the two successive increases."


def _a11(d):
    final = F(d["principal"]) * (F(1) + F(d["r1"], 100)) * (F(1) + F(d["r2"], 100))
    return money(final if d["ask"] == "amount" else final - F(d["principal"]))


cid_successive = make_family(
    "cid_successive",
    ("principal", "r1", "r2", "ask"),
    [
        (20000, 10, 20, "amount"),
        (15000, 20, 10, "gain"),
        (25000, 10, 10, "amount"),
        (12000, 25, 20, "gain"),
        (18000, 5, 10, "amount"),
    ],
    _t11,
    _a11,
    distract=_money_distract,
    explain=lambda d, c: _explain_inputs(
        d, c, "successive increases multiply the principal by (1 + r1/100) and then by (1 + r2/100); the gain is the final amount minus the principal."
    ),
)


# ---------------------------------------------------------------------------
# 12. cid_withdrawal
# ---------------------------------------------------------------------------

ASK12 = {
    "amount": "the amount left at the end of the full period",
    "interest": "the total simple interest earned over the full period",
}


def _t12(d):
    block = data([
        ("principal", money(d["principal"])),
        ("rate", pct(d["rate"])),
        ("total years", d["years"]),
        ("withdrawal", money(d["withdraw"])),
        ("withdrawal after years", d["after"]),
    ])
    return f"{block} Find {ASK12[d['ask']]}. Interest after the withdrawal is charged on the reduced principal."


def _a12(d):
    before = _si(d["principal"], d["rate"], d["after"])
    reduced = F(d["principal"]) - F(d["withdraw"])
    after = _si(reduced, d["rate"], d["years"] - d["after"])
    interest = before + after
    if d["ask"] == "interest":
        return money(interest)
    return money(reduced + interest)


cid_withdrawal = make_family(
    "cid_withdrawal",
    ("principal", "rate", "years", "withdraw", "after", "ask"),
    [
        (20000, 5, 4, 5000, 2, "amount"),
        (30000, 6, 5, 10000, 2, "interest"),
        (25000, 4, 3, 5000, 1, "amount"),
        (40000, 5, 4, 10000, 3, "amount"),
        (15000, 8, 3, 3000, 1, "interest"),
    ],
    _t12,
    _a12,
    distract=_money_distract,
    explain=lambda d, c: _explain_inputs(
        d, c, "interest for the first part is P × r × t ÷ 100; after withdrawal, interest uses (P − withdrawal) for the remaining years."
    ),
)


# ---------------------------------------------------------------------------
# 13. cid_addition
# ---------------------------------------------------------------------------

ASK13 = {
    "amount": "the amount at the end of the full period",
    "interest": "the total simple interest earned over the full period",
}


def _t13(d):
    block = data([
        ("principal", money(d["principal"])),
        ("rate", pct(d["rate"])),
        ("total years", d["years"]),
        ("addition", money(d["addition"])),
        ("added after years", d["after"]),
    ])
    return f"{block} Find {ASK13[d['ask']]}. Interest after the addition is charged on the increased principal."


def _a13(d):
    before = _si(d["principal"], d["rate"], d["after"])
    increased = F(d["principal"]) + F(d["addition"])
    after = _si(increased, d["rate"], d["years"] - d["after"])
    interest = before + after
    if d["ask"] == "interest":
        return money(interest)
    return money(increased + interest)


cid_addition = make_family(
    "cid_addition",
    ("principal", "rate", "years", "addition", "after", "ask"),
    [
        (20000, 5, 4, 10000, 2, "amount"),
        (30000, 6, 5, 5000, 3, "interest"),
        (15000, 4, 3, 5000, 1, "amount"),
        (25000, 8, 4, 10000, 2, "amount"),
        (12000, 10, 3, 3000, 1, "interest"),
    ],
    _t13,
    _a13,
    distract=_money_distract,
    explain=lambda d, c: _explain_inputs(
        d, c, "interest for the first part uses the original principal; after the addition it uses (principal + addition) for the remaining years."
    ),
)


# ---------------------------------------------------------------------------
# 14. cid_population
# ---------------------------------------------------------------------------

ASK14 = {"population": "the population at the end", "increase": "the increase in population"}


def _t14(d):
    block = data([
        ("population", d["population"]),
        ("growth rate", pct(d["rate"])),
        ("years", d["years"]),
    ])
    return f"{block} Find {ASK14[d['ask']]}."


def _a14(d):
    final = F(d["population"]) * (F(1) + F(d["rate"], 100)) ** int(d["years"])
    return fmt(final if d["ask"] == "population" else final - F(d["population"]))


cid_population = make_family(
    "cid_population",
    ("population", "rate", "years", "ask"),
    [
        (20000, 5, 2, "population"),
        (50000, 10, 2, "increase"),
        (40000, 5, 3, "population"),
        (80000, 10, 3, "increase"),
        (12000, 20, 2, "population"),
    ],
    _t14,
    _a14,
    distract=_num_distract,
    explain=lambda d, c: _explain_inputs(
        d, c, "compound growth gives final population = initial × (1 + rate/100)^years, and the increase is final minus initial."
    ),
)


# ---------------------------------------------------------------------------
# 15. cid_ratio_invest
# ---------------------------------------------------------------------------

ASK15 = {
    "first_interest": "the simple interest on the first part",
    "second_interest": "the simple interest on the second part",
    "total_interest": "the total simple interest from both parts",
}


def _t15(d):
    block = data([
        ("total investment", money(d["total"])),
        ("split ratio", f"{d['r1']}:{d['r2']}"),
        ("rate on first part", pct(d["r1"])),
        ("rate on second part", pct(d["r2"])),
        ("years", d["years"]),
    ])
    return f"{block} Find {ASK15[d['ask']]}."


def _a15(d):
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


cid_ratio_invest = make_family(
    "cid_ratio_invest",
    ("total", "r1", "r2", "years", "ask"),
    [
        (18000, 2, 1, 2, "total_interest"),
        (24000, 3, 1, 3, "first_interest"),
        (20000, 1, 1, 2, "second_interest"),
        (30000, 4, 2, 2, "total_interest"),
        (15000, 2, 3, 4, "second_interest"),
    ],
    _t15,
    _a15,
    distract=_money_distract,
    explain=lambda d, c: _explain_inputs(
        d, c, "split the total in the stated ratio, then apply P × r × t ÷ 100 to each part using its own stated rate."
    ),
)


# ---------------------------------------------------------------------------
# 16. cid_effective
# ---------------------------------------------------------------------------

ASK16 = {
    "effective": "the single effective rate of increase",
    "amount": "the final amount",
    "gain": "the gain in rupees",
}


def _t16(d):
    block = data([
        ("principal", money(d["principal"])),
        ("first rate", pct(d["r1"])),
        ("second rate", pct(d["r2"])),
    ])
    return f"{block} Find {ASK16[d['ask']]} after two successive increases."


def _a16(d):
    r1, r2 = F(d["r1"]), F(d["r2"])
    effective = r1 + r2 + r1 * r2 / F(100)
    amount = F(d["principal"]) * (F(1) + r1 / F(100)) * (F(1) + r2 / F(100))
    if d["ask"] == "effective":
        return pct(effective)
    if d["ask"] == "amount":
        return money(amount)
    return money(amount - F(d["principal"]))


cid_effective = make_family(
    "cid_effective",
    ("principal", "r1", "r2", "ask"),
    [
        (10000, 10, 20, "effective"),
        (20000, 5, 10, "gain"),
        (15000, 20, 20, "amount"),
        (25000, 8, 12, "effective"),
        (12000, 10, 10, "gain"),
    ],
    _t16,
    _a16,
    distract=_mixed_distract,
    explain=lambda d, c: _explain_inputs(
        d, c, "the effective successive rate is r1 + r2 + r1×r2/100; applying it to the principal gives the amount and gain."
    ),
)


# ---------------------------------------------------------------------------
# 17. cid_installment_factor
# ---------------------------------------------------------------------------

ASK17 = {
    "installment": "the value of each equal yearly instalment",
    "total_interest": "the total simple interest paid",
}


def _t17(d):
    block = data([
        ("loan", money(d["principal"])),
        ("rate", pct(d["rate"])),
        ("yearly instalments", d["installments"]),
    ])
    return f"{block} Find {ASK17[d['ask']]}. Interest is charged on the original loan for the full term."


def _a17(d):
    interest = _si(d["principal"], d["rate"], d["installments"])
    if d["ask"] == "total_interest":
        return money(interest)
    return money((F(d["principal"]) + interest) / F(d["installments"]))


cid_installment_factor = make_family(
    "cid_installment_factor",
    ("principal", "rate", "installments", "ask"),
    [
        (12000, 5, 4, "installment"),
        (20000, 6, 5, "total_interest"),
        (18000, 10, 3, "installment"),
        (25000, 4, 2, "installment"),
        (30000, 8, 3, "total_interest"),
    ],
    _t17,
    _a17,
    distract=_money_distract,
    explain=lambda d, c: _explain_inputs(
        d, c, "total interest is loan × rate × number of instalments ÷ 100; each instalment is (loan + interest) ÷ number of instalments."
    ),
)


# ---------------------------------------------------------------------------
# 18. cid_recurring
# ---------------------------------------------------------------------------

ASK18 = {"maturity": "the maturity value", "interest": "the interest earned"}


def _t18(d):
    block = data([
        ("monthly deposit", money(d["deposit"])),
        ("annual rate", pct(d["rate"])),
        ("months", d["months"]),
    ])
    return f"{block} Find {ASK18[d['ask']]} for the recurring deposit."


def _a18(d):
    months = F(d["months"])
    interest = (
        F(d["deposit"]) * months * (months + F(1)) / F(2) * F(d["rate"]) / F(1200)
    )
    if d["ask"] == "interest":
        return money(interest)
    return money(F(d["deposit"]) * months + interest)


cid_recurring = make_family(
    "cid_recurring",
    ("deposit", "rate", "months", "ask"),
    [
        (5000, 12, 12, "maturity"),
        (10000, 8, 12, "interest"),
        (8000, 5, 12, "maturity"),
        (4000, 6, 24, "interest"),
        (10000, 10, 12, "maturity"),
    ],
    _t18,
    _a18,
    distract=_money_distract,
    explain=lambda d, c: _explain_inputs(
        d, c, "recurring-deposit interest is deposit × n(n+1)/2 × rate ÷ (100 × 12); maturity adds all deposits to this interest."
    ),
)


# ---------------------------------------------------------------------------
# 19. cid_discount_rate
# ---------------------------------------------------------------------------

ASK19 = {"discount": "the discount", "proceeds": "the proceeds after discount"}


def _t19(d):
    block = data([
        ("face value", money(d["face"])),
        ("discount rate", pct(d["rate"])),
        ("months", d["months"]),
    ])
    return f"{block} Find {ASK19[d['ask']]}."


def _a19(d):
    discount = F(d["face"]) * F(d["rate"]) * F(d["months"]) / F(1200)
    if d["ask"] == "discount":
        return money(discount)
    return money(F(d["face"]) - discount)


cid_discount_rate = make_family(
    "cid_discount_rate",
    ("face", "rate", "months", "ask"),
    [
        (12000, 5, 6, "discount"),
        (18000, 6, 4, "proceeds"),
        (24000, 8, 9, "discount"),
        (15000, 10, 3, "proceeds"),
        (20000, 12, 6, "discount"),
    ],
    _t19,
    _a19,
    distract=_money_distract,
    explain=lambda d, c: _explain_inputs(
        d, c, "discount is face value × rate × months ÷ (100 × 12); proceeds are face value minus the discount."
    ),
)


# ---------------------------------------------------------------------------
# 20. cid_simple_growth
# ---------------------------------------------------------------------------

ASK20 = {
    "first": "the interest earned at the initial rate",
    "second": "the interest earned at the revised rate",
    "total": "the total interest over both periods",
}


def _t20(d):
    block = data([
        ("principal", money(d["principal"])),
        ("initial rate", pct(d["r1"])),
        ("revised rate", pct(d["r2"])),
        ("years at each rate", d["change_after"]),
    ])
    return f"{block} Find {ASK20[d['ask']]}."


def _a20(d):
    first = _si(d["principal"], d["r1"], d["change_after"])
    second = _si(d["principal"], d["r2"], d["change_after"])
    if d["ask"] == "first":
        return money(first)
    if d["ask"] == "second":
        return money(second)
    return money(first + second)


cid_simple_growth = make_family(
    "cid_simple_growth",
    ("principal", "r1", "r2", "change_after", "ask"),
    [
        (20000, 5, 8, 2, "total"),
        (15000, 6, 4, 3, "first"),
        (25000, 8, 5, 2, "second"),
        (12000, 10, 6, 4, "total"),
        (18000, 4, 5, 3, "second"),
    ],
    _t20,
    _a20,
    distract=_money_distract,
    explain=lambda d, c: _explain_inputs(
        d, c, "each period's simple interest is principal × that period's rate × years ÷ 100; add them for the total."
    ),
)


# ---------------------------------------------------------------------------
# 21. cid_interest_share
# ---------------------------------------------------------------------------

ASK21 = {
    "interest": "the simple interest",
    "total": "the amount at the end",
    "share": "the interest as a percentage of the other amount",
}


def _t21(d):
    block = data([
        ("principal", money(d["principal"])),
        ("rate", pct(d["rate"])),
        ("years", d["years"]),
        ("other amount", money(d["other"])),
    ])
    return f"{block} Find {ASK21[d['ask']]}."


def _a21(d):
    interest = _si(d["principal"], d["rate"], d["years"])
    if d["ask"] == "interest":
        return money(interest)
    if d["ask"] == "total":
        return money(F(d["principal"]) + interest)
    return pct(interest * F(100) / F(d["other"]))


cid_interest_share = make_family(
    "cid_interest_share",
    ("principal", "rate", "years", "other", "ask"),
    [
        (20000, 5, 2, 4000, "interest"),
        (15000, 6, 3, 9000, "share"),
        (25000, 4, 4, 5000, "total"),
        (18000, 10, 2, 12000, "share"),
        (30000, 5, 3, 6000, "interest"),
    ],
    _t21,
    _a21,
    distract=_mixed_distract,
    explain=lambda d, c: _explain_inputs(
        d, c, "find simple interest first; the amount adds it to the principal, and the share is interest × 100 ÷ other amount."
    ),
)


# ---------------------------------------------------------------------------
# 22. cid_target_amount
# ---------------------------------------------------------------------------

ASK22 = {
    "years": "the number of years needed to reach the target",
    "interest": "the interest needed to reach the target",
}


def _t22(d):
    block = data([
        ("principal", money(d["principal"])),
        ("rate", pct(d["rate"])),
        ("target amount", money(d["target"])),
    ])
    return f"{block} Find {ASK22[d['ask']]} under simple interest."


def _a22(d):
    interest = F(d["target"]) - F(d["principal"])
    if d["ask"] == "interest":
        return money(interest)
    return fmt(interest * F(100) / (F(d["principal"]) * F(d["rate"])))


cid_target_amount = make_family(
    "cid_target_amount",
    ("principal", "rate", "target", "ask"),
    [
        (10000, 5, 12000, "years"),
        (20000, 8, 28000, "interest"),
        (15000, 10, 21000, "years"),
        (25000, 4, 30000, "years"),
        (12000, 6, 16560, "interest"),
    ],
    _t22,
    _a22,
    distract=_mixed_distract,
    explain=lambda d, c: _explain_inputs(
        d, c, "the needed interest is target minus principal; the years under simple interest are interest × 100 ÷ (principal × rate)."
    ),
)


# ---------------------------------------------------------------------------
# 23. cid_mixed_period
# ---------------------------------------------------------------------------

ASK23 = {
    "first": "the interest in the first year",
    "second": "the interest in the second year",
    "total": "the total interest over the two years",
    "amount": "the amount at the end of the second year",
}


def _t23(d):
    block = data([
        ("initial principal", money(d["principal"])),
        ("annual rate", pct(d["rate"])),
        ("extra added after first year", money(d["extra"])),
    ])
    return f"{block} Find {ASK23[d['ask']]}."


def _a23(d):
    first = _si(d["principal"], d["rate"], 1)
    second = _si(F(d["principal"]) + F(d["extra"]), d["rate"], 1)
    if d["ask"] == "first":
        return money(first)
    if d["ask"] == "second":
        return money(second)
    if d["ask"] == "total":
        return money(first + second)
    return money(F(d["principal"]) + F(d["extra"]) + first + second)


cid_mixed_period = make_family(
    "cid_mixed_period",
    ("principal", "rate", "extra", "ask"),
    [
        (20000, 5, 5000, "total"),
        (15000, 6, 3000, "second"),
        (25000, 4, 5000, "amount"),
        (12000, 10, 2000, "first"),
        (30000, 5, 10000, "total"),
    ],
    _t23,
    _a23,
    distract=_money_distract,
    explain=lambda d, c: _explain_inputs(
        d, c, "the first year uses the original principal; the second year uses principal plus the extra amount added after year one."
    ),
)


# ---------------------------------------------------------------------------
# 24. cid_comparison
# ---------------------------------------------------------------------------

ASK24 = {
    "A_interest": "the interest from investment A",
    "B_interest": "the interest from investment B",
    "difference": "the positive difference between the two interests",
    "total": "the total interest from both investments",
}


def _t24(d):
    block = data([
        ("investment A", money(d["p1"])),
        ("rate A", pct(d["r1"])),
        ("years A", d["t1"]),
        ("investment B", money(d["p2"])),
        ("rate B", pct(d["r2"])),
        ("years B", d["t2"]),
    ])
    return f"{block} Find {ASK24[d['ask']]} under simple interest."


def _a24(d):
    i1 = _si(d["p1"], d["r1"], d["t1"])
    i2 = _si(d["p2"], d["r2"], d["t2"])
    if d["ask"] == "A_interest":
        return money(i1)
    if d["ask"] == "B_interest":
        return money(i2)
    if d["ask"] == "difference":
        return money(abs(i1 - i2))
    return money(i1 + i2)


cid_comparison = make_family(
    "cid_comparison",
    ("p1", "r1", "t1", "p2", "r2", "t2", "ask"),
    [
        (20000, 5, 2, 15000, 6, 3, "difference"),
        (10000, 8, 3, 12000, 5, 4, "A_interest"),
        (25000, 4, 2, 20000, 6, 3, "total"),
        (18000, 6, 4, 15000, 8, 3, "B_interest"),
        (30000, 5, 3, 25000, 4, 4, "difference"),
    ],
    _t24,
    _a24,
    distract=_money_distract,
    explain=lambda d, c: _explain_inputs(
        d, c, "each investment's interest is principal × rate × years ÷ 100; compare or add the two results as asked."
    ),
)


FAMILIES = [
    cid_principal_rate,
    cid_si_lookup,
    cid_ci_lookup,
    cid_amount_lookup,
    cid_si_ci_gap,
    cid_rate_table,
    cid_time_table,
    cid_two_deposits,
    cid_half_yearly,
    cid_quarterly,
    cid_successive,
    cid_withdrawal,
    cid_addition,
    cid_population,
    cid_ratio_invest,
    cid_effective,
    cid_installment_factor,
    cid_recurring,
    cid_discount_rate,
    cid_simple_growth,
    cid_interest_share,
    cid_target_amount,
    cid_mixed_period,
    cid_comparison,
]


def build_simple_and_compound_interest_di():
    return build_specs(FAMILIES, mains=False)
