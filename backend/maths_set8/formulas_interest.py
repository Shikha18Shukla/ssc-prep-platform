# -*- coding: utf-8 -*-
"""Independent answer sheet for Simple & Compound Interest (Mains).

The verifier passes the exact ``verification_data.inputs`` dictionary from a
question to the function stored here. This module imports only the separate
formatting helpers; it never imports a builder, ``common`` or ``bank``.
"""

from __future__ import annotations

from .formula_helpers import F, fmt, money, pct

FORMULAS = {}


# ---------------------------------------------------------------------------
# Local duplicated arithmetic (no builder imports)
# ---------------------------------------------------------------------------

def _int_root(value, n):
    if value < 0:
        return None
    if value in (0, 1) or n == 1:
        return value
    lo, hi = 1, 1
    while hi ** n < value:
        hi *= 2
    while lo <= hi:
        mid = (lo + hi) // 2
        power = mid ** n
        if power == value:
            return mid
        if power < value:
            lo = mid + 1
        else:
            hi = mid - 1
    return None


def _root_fraction(value, n):
    top = _int_root(value.numerator, n)
    bottom = _int_root(value.denominator, n)
    if top is None or bottom is None:
        return None
    return F(top, bottom)


def _relation_rate(d):
    si = F(d["si"])
    ci = F(d["ci"])
    principal = F(d["principal"])
    for years in range(2, 13):
        x = F(si, principal * years)
        if principal * ((1 + x) ** years - 1) == ci:
            return x * 100, years
    raise ValueError("no consistent whole-number period for rate/time relation")


def _read_years(value):
    text = str(value)
    if "/" in text:
        top, bottom = text.split("/")
        return F(int(top), int(bottom))
    if "." in text:
        whole, frac = text.split(".")
        return F(int(whole + frac), 10 ** len(frac))
    return F(int(text))


# ---------------------------------------------------------------------------
# 1. cim_successive_rates
# ---------------------------------------------------------------------------

def _cim_successive_rates(d):
    amount = F(d["principal"]) * (1 + F(d["r1"], 100)) * (1 + F(d["r2"], 100))
    amount *= (1 + F(d["r3"], 100)) ** (d["years"] - 2)
    return money(amount)


FORMULAS["cim_successive_rates"] = _cim_successive_rates


# ---------------------------------------------------------------------------
# 2. cim_half_yearly
# ---------------------------------------------------------------------------

def _cim_half_yearly(d):
    return money(F(d["principal"]) * (1 + F(d["rate"], 200)) ** (2 * d["years"]))


FORMULAS["cim_half_yearly"] = _cim_half_yearly


# ---------------------------------------------------------------------------
# 3. cim_quarterly
# ---------------------------------------------------------------------------

def _cim_quarterly(d):
    return money(F(d["principal"]) * (1 + F(d["rate"], 400)) ** (4 * d["years"]))


FORMULAS["cim_quarterly"] = _cim_quarterly


# ---------------------------------------------------------------------------
# 4. cim_ci_si_diff
# ---------------------------------------------------------------------------

def _cim_ci_si_diff(d):
    p = F(d["principal"])
    x = F(d["rate"], 100)
    n = d["years"]
    si = p * x * n
    ci = p * (1 + x) ** n - p
    return money(ci - si)


FORMULAS["cim_ci_si_diff"] = _cim_ci_si_diff


# ---------------------------------------------------------------------------
# 5. cim_rate_time_relation
# ---------------------------------------------------------------------------

def _cim_rate_time_relation(d):
    rate, years = _relation_rate(d)
    del years
    return pct(rate)


FORMULAS["cim_rate_time_relation"] = _cim_rate_time_relation


# ---------------------------------------------------------------------------
# 6. cim_variable_principal
# ---------------------------------------------------------------------------

def _cim_variable_principal(d):
    p = F(d["principal"])
    addition = F(d["addition"])
    x = F(d["rate"], 100)
    k = d["add_after"]
    n = d["years"]
    return money((p * (1 + x) ** k + addition) * (1 + x) ** (n - k))


FORMULAS["cim_variable_principal"] = _cim_variable_principal


# ---------------------------------------------------------------------------
# 7. cim_installments (annuity due)
# ---------------------------------------------------------------------------

def _cim_installments(d):
    p = F(d["principal"])
    x = F(d["rate"], 100)
    n = d["installments"]
    return money(p * x * (1 + x) ** (n - 1) / ((1 + x) ** n - 1))


FORMULAS["cim_installments"] = _cim_installments


# ---------------------------------------------------------------------------
# 8. cim_effective_rate
# ---------------------------------------------------------------------------

def _cim_effective_rate(d):
    p = F(d["principal"])
    amount = p * (1 + F(d["r1"], 100)) * (1 + F(d["r2"], 100))
    return pct((amount - p) * 100 / p)


FORMULAS["cim_effective_rate"] = _cim_effective_rate


# ---------------------------------------------------------------------------
# 9. cim_partial_withdrawal
# ---------------------------------------------------------------------------

def _cim_partial_withdrawal(d):
    p = F(d["principal"])
    x = F(d["rate"], 100)
    balance = p * (1 + x) ** d["after"] - F(d["withdraw"])
    return money(balance * (1 + x) ** (d["years"] - d["after"]))


FORMULAS["cim_partial_withdrawal"] = _cim_partial_withdrawal


# ---------------------------------------------------------------------------
# 10. cim_two_schemes
# ---------------------------------------------------------------------------

def _cim_two_schemes(d):
    p = F(d["principal"])
    r1 = F(d["rate1"], 100)
    r2 = F(d["rate2"], 100)
    n = d["years"]
    half = n // 2
    scheme_a = p * (1 + r1) ** half * (1 + r2) ** (n - half)
    scheme_b = p * (1 + r2 * n)
    return money(scheme_a - scheme_b)


FORMULAS["cim_two_schemes"] = _cim_two_schemes


# ---------------------------------------------------------------------------
# 11. cim_simple_change
# ---------------------------------------------------------------------------

def _cim_simple_change(d):
    p = F(d["principal"])
    amount = p * (1 + F(d["r1"], 100) * d["change_after"])
    amount *= 1 + F(d["r2"], 100) * (d["years"] - d["change_after"])
    return money(amount)


FORMULAS["cim_simple_change"] = _cim_simple_change


# ---------------------------------------------------------------------------
# 12. cim_population
# ---------------------------------------------------------------------------

def _cim_population(d):
    population = F(d["population"])
    growth = F(d["growth"], 100)
    n = d["years"]
    up = (n + 1) // 2
    down = n // 2
    return fmt(population * (1 + growth) ** up * (1 - growth / 2) ** down)


FORMULAS["cim_population"] = _cim_population


# ---------------------------------------------------------------------------
# 13. cim_doubling
# ---------------------------------------------------------------------------

def _cim_doubling(d):
    factor = F(d["amount"], d["principal"])
    root = _root_fraction(factor, d["years"])
    return pct((root - 1) * 100)


FORMULAS["cim_doubling"] = _cim_doubling


# ---------------------------------------------------------------------------
# 14. cim_interest_on_interest
# ---------------------------------------------------------------------------

def _cim_interest_on_interest(d):
    p = F(d["principal"])
    x = F(d["rate"], 100)
    extra = p * ((1 + x) ** 2 - 1 - 2 * x)
    return pct(extra * 100 / p)


FORMULAS["cim_interest_on_interest"] = _cim_interest_on_interest


# ---------------------------------------------------------------------------
# 15. cim_mixed_frequency
# ---------------------------------------------------------------------------

def _cim_mixed_frequency(d):
    p = F(d["principal"])
    si = p * F(d["si_rate"], 100) * d["years"]
    ci = p * (1 + F(d["ci_rate"], 200)) ** (2 * d["years"]) - p
    return money(si + ci)


FORMULAS["cim_mixed_frequency"] = _cim_mixed_frequency


# ---------------------------------------------------------------------------
# 16. cim_equal_installment (ordinary annuity)
# ---------------------------------------------------------------------------

def _cim_equal_installment(d):
    p = F(d["principal"])
    x = F(d["rate"], 100)
    n = d["years"]
    return money(p * x * (1 + x) ** n / ((1 + x) ** n - 1))


FORMULAS["cim_equal_installment"] = _cim_equal_installment


# ---------------------------------------------------------------------------
# 17. cim_recurring
# ---------------------------------------------------------------------------

def _cim_recurring(d):
    deposit = F(d["deposit"])
    rate = F(d["rate"], 1200)
    months = d["months"]
    return money(deposit * ((1 + rate) ** months - 1) / rate)


FORMULAS["cim_recurring"] = _cim_recurring


# ---------------------------------------------------------------------------
# 18. cim_rate_discovery
# ---------------------------------------------------------------------------

def _cim_rate_discovery(d):
    p = F(d["principal"])
    n = d["years"]
    x = F(d["si_amount"], p * n)
    if p * ((1 + x) ** n - 1) != F(d["ci_amount"]):
        root = _root_fraction(1 + F(d["ci_amount"], p), n)
        x = root - 1
    return pct(x * 100)


FORMULAS["cim_rate_discovery"] = _cim_rate_discovery


# ---------------------------------------------------------------------------
# 19. cim_fractional_year
# ---------------------------------------------------------------------------

def _cim_fractional_year(d):
    p = F(d["principal"])
    x = F(d["rate"], 100)
    years = _read_years(d["years"])
    whole = int(years)
    fraction = years - whole
    return money(p * (1 + x) ** whole * (1 + fraction * x))


FORMULAS["cim_fractional_year"] = _cim_fractional_year


# ---------------------------------------------------------------------------
# 20. cim_ratio_principal
# ---------------------------------------------------------------------------

def _cim_ratio_principal(d):
    total = F(d["total"])
    r1, r2 = d["r1"], d["r2"]
    n = d["years"]
    first = total * F(r1, r1 + r2)
    second = total * F(r2, r1 + r2)
    return money(first * (1 + F(r1, 100)) ** n + second * (1 + F(r2, 100)) ** n)


FORMULAS["cim_ratio_principal"] = _cim_ratio_principal


# ---------------------------------------------------------------------------
# 21. cim_loss_gain
# ---------------------------------------------------------------------------

def _cim_loss_gain(d):
    p = F(d["principal"])
    final = p * (1 - F(d["loss"], 100)) * (1 + F(d["gain"], 100))
    return pct((final - p) * 100 / p)


FORMULAS["cim_loss_gain"] = _cim_loss_gain


# ---------------------------------------------------------------------------
# 22. cim_loan_repayment
# ---------------------------------------------------------------------------

def _cim_loan_repayment(d):
    p = F(d["principal"])
    x = F(d["rate"], 100)
    k = d["after"]
    n = d["years"]
    repay = F(d["repay"])
    balance = p * (1 + x) ** k - repay
    final = balance * (1 + x) ** (n - k)
    return money(repay + final - p)


FORMULAS["cim_loan_repayment"] = _cim_loan_repayment


# ---------------------------------------------------------------------------
# 23. cim_midyear_rate
# ---------------------------------------------------------------------------

def _cim_midyear_rate(d):
    p = F(d["principal"])
    factor = (1 + F(d["r1"], 200)) * (1 + F(d["r2"], 200))
    return money(p * factor ** d["years"])


FORMULAS["cim_midyear_rate"] = _cim_midyear_rate


# ---------------------------------------------------------------------------
# 24. cim_monthly_compound
# ---------------------------------------------------------------------------

def _cim_monthly_compound(d):
    p = F(d["principal"])
    rate = F(d["annual_rate"], 1200)
    return money(p * (1 + rate) ** (12 * d["years"]))


FORMULAS["cim_monthly_compound"] = _cim_monthly_compound
