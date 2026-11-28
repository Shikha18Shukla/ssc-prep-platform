# -*- coding: utf-8 -*-
"""Simple & Compound Interest (Mains) - 120 original, HARD, multi-step questions."""

from __future__ import annotations

from fractions import Fraction

from .common import (
    F,
    NAMES,
    build_specs,
    data,
    fmt,
    make_family,
    money,
    near_money,
    near_num,
    near_pct,
    pct,
)

SOURCE_PDF = "Simple and Compound Interest Mains 01  Class Notes.pdf"
PAGES = {
    1: f"{SOURCE_PDF}, pp. 3-5",
    2: f"{SOURCE_PDF}, pp. 6-8",
    3: f"{SOURCE_PDF}, pp. 9-11",
    4: f"{SOURCE_PDF}, pp. 3-12",
}


# ---------------------------------------------------------------------------
# Shared presentation helpers
# ---------------------------------------------------------------------------

def _who(v):
    key = v.get("principal", v.get("total", v.get("population", v.get("deposit", v.get("si", 0)))))
    return NAMES[int(key) % len(NAMES)]


def _shown(v, money_keys=(), pct_keys=()):
    out = {"who": _who(v)}
    for key, value in v.items():
        if key in money_keys:
            out[key] = money(value)
        elif key in pct_keys:
            out[key] = pct(value)
        else:
            out[key] = str(value)
    return out


def _story(v, template, money_keys=(), pct_keys=()):
    return template.format(**_shown(v, money_keys, pct_keys)) + " " + data(list(v.items()))


def _steps(parts, correct):
    return " ".join(parts) + f" Hence the required result is {correct}."


def _money_distract(result, v):
    del v
    return near_money(Fraction(str(result).replace("₹", "")), 50)


def _pct_distract(result, v):
    del v
    return near_pct(Fraction(str(result).rstrip("%")), 5)


def _count_distract(result, v):
    del v
    return near_num(Fraction(str(result)), 5)


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


def _relation_rate(v):
    si = F(v["si"])
    ci = F(v["ci"])
    principal = F(v["principal"])
    for years in range(2, 13):
        x = F(si, principal * years)
        if principal * ((1 + x) ** years - 1) == ci:
            return x * 100, years
    raise ValueError("no consistent whole-number period for rate/time relation")


# ---------------------------------------------------------------------------
# 1. Successive annual rates
# ---------------------------------------------------------------------------

SUCCESSIVE_ROWS = (
    (12000, 10, 12, 15, 4),
    (15000, 8, 10, 12, 5),
    (18000, 12, 15, 18, 4),
    (20000, 5, 8, 10, 5),
    (24000, 10, 15, 20, 3),
)


def _successive_answer(v):
    amount = F(v["principal"]) * (1 + F(v["r1"], 100)) * (1 + F(v["r2"], 100))
    amount *= (1 + F(v["r3"], 100)) ** (v["years"] - 2)
    return money(amount)


def _successive_text(v):
    return _story(
        v,
        "{who} invests {principal} for {years} years. The annual credit rate is {r1} "
        "in the first year, {r2} in the second year and {r3} in every later year. "
        "Find the maturity amount at the end of the full period.",
        ("principal",), ("r1", "r2", "r3"),
    )


def _successive_explain(v, correct):
    p = F(v["principal"])
    a1 = p * (1 + F(v["r1"], 100))
    a2 = a1 * (1 + F(v["r2"], 100))
    final = a2 * (1 + F(v["r3"], 100)) ** (v["years"] - 2)
    return _steps([
        f"After year 1: {money(p)}×(1+{F(v['r1'], 100)}) = {money(a1)}.",
        f"After year 2: ×(1+{F(v['r2'], 100)}) = {money(a2)}.",
        f"For the remaining {v['years'] - 2} years at {pct(v['r3'])}: ×(1+{F(v['r3'], 100)})^{v['years'] - 2} = {money(final)}.",
    ], correct)


cim_successive_rates = make_family(
    "cim_successive_rates",
    ("principal", "r1", "r2", "r3", "years"),
    SUCCESSIVE_ROWS,
    _successive_text,
    _successive_answer,
    _money_distract,
    _successive_explain,
)


# ---------------------------------------------------------------------------
# 2. Half-yearly compounding
# ---------------------------------------------------------------------------

HALF_YEARLY_ROWS = (
    (20000, 10, 2),
    (16000, 12, 3),
    (24000, 8, 2),
    (18000, 15, 3),
    (12000, 20, 2),
)


def _half_yearly_answer(v):
    return money(F(v["principal"]) * (1 + F(v["rate"], 200)) ** (2 * v["years"]))


def _half_yearly_text(v):
    return _story(
        v,
        "{who} deposits {principal} in a scheme paying {rate} per annum with interest "
        "credited half-yearly. Find the amount standing to {who}'s credit after {years} years.",
        ("principal",), ("rate",),
    )


def _half_yearly_explain(v, correct):
    p = F(v["principal"])
    half_rate = F(v["rate"], 200)
    periods = 2 * v["years"]
    amount = p * (1 + half_rate) ** periods
    return _steps([
        f"Rate per half-year = {v['rate']}/2% = {pct(half_rate * 100)}.",
        f"Number of half-years = 2×{v['years']} = {periods}.",
        f"Amount = {money(p)}×(1+{half_rate})^{periods} = {money(amount)}.",
    ], correct)


cim_half_yearly = make_family(
    "cim_half_yearly",
    ("principal", "rate", "years"),
    HALF_YEARLY_ROWS,
    _half_yearly_text,
    _half_yearly_answer,
    _money_distract,
    _half_yearly_explain,
)


# ---------------------------------------------------------------------------
# 3. Quarterly compounding
# ---------------------------------------------------------------------------

QUARTERLY_ROWS = (
    (20000, 12, 2),
    (16000, 16, 2),
    (24000, 8, 3),
    (18000, 20, 2),
    (12000, 10, 3),
)


def _quarterly_answer(v):
    return money(F(v["principal"]) * (1 + F(v["rate"], 400)) ** (4 * v["years"]))


def _quarterly_text(v):
    return _story(
        v,
        "{who} places {principal} on compound interest at {rate} per annum, compounded "
        "quarterly. What will the deposit be worth after {years} years?",
        ("principal",), ("rate",),
    )


def _quarterly_explain(v, correct):
    p = F(v["principal"])
    qrate = F(v["rate"], 400)
    periods = 4 * v["years"]
    amount = p * (1 + qrate) ** periods
    return _steps([
        f"Quarterly rate = {v['rate']}/4% = {pct(qrate * 100)}.",
        f"Quarters in {v['years']} years = {periods}.",
        f"Amount = {money(p)}×(1+{qrate})^{periods} = {money(amount)}.",
    ], correct)


cim_quarterly = make_family(
    "cim_quarterly",
    ("principal", "rate", "years"),
    QUARTERLY_ROWS,
    _quarterly_text,
    _quarterly_answer,
    _money_distract,
    _quarterly_explain,
)


# ---------------------------------------------------------------------------
# 4. Difference between compound and simple interest
# ---------------------------------------------------------------------------

CI_SI_DIFF_ROWS = (
    (10000, 10, 2),
    (12000, 5, 3),
    (15000, 8, 2),
    (18000, 12, 3),
    (20000, 15, 2),
)


def _ci_si_diff_answer(v):
    p = F(v["principal"])
    x = F(v["rate"], 100)
    n = v["years"]
    si = p * x * n
    ci = p * (1 + x) ** n - p
    return money(ci - si)


def _ci_si_diff_text(v):
    return _story(
        v,
        "On a sum of {principal}, compare simple interest at {rate} per annum for {years} "
        "years with compound interest at the same rate for the same period, compounded "
        "annually. How much more does the compound interest earn?",
        ("principal",), ("rate",),
    )


def _ci_si_diff_explain(v, correct):
    p = F(v["principal"])
    x = F(v["rate"], 100)
    n = v["years"]
    si = p * x * n
    ci = p * (1 + x) ** n - p
    return _steps([
        f"Simple interest = {money(p)}×{x}×{n} = {money(si)}.",
        f"Compound interest = {money(p)}×[(1+{x})^{n}−1] = {money(ci)}.",
        f"Excess = {money(ci)}−{money(si)} = {money(ci - si)}.",
    ], correct)


cim_ci_si_diff = make_family(
    "cim_ci_si_diff",
    ("principal", "rate", "years"),
    CI_SI_DIFF_ROWS,
    _ci_si_diff_text,
    _ci_si_diff_answer,
    _money_distract,
    _ci_si_diff_explain,
)


# ---------------------------------------------------------------------------
# 5. Recovering rate from SI and CI over an unknown whole period
# ---------------------------------------------------------------------------

RATE_TIME_ROWS = (
    (1000, 1050, 5000),
    (1200, 1261, 8000),
    (1800, 1890, 9000),
    (1600, 1664, 10000),
    (3600, 3972, 12000),
)


def _rate_time_answer(v):
    rate, years = _relation_rate(v)
    del years
    return pct(rate)


def _rate_time_text(v):
    return _story(
        v,
        "{who} notices that the same principal fetched {si} as simple interest and {ci} "
        "as compound interest over the same whole number of years at the same annual rate. "
        "The compound interest is larger. Find the annual rate.",
        ("si", "ci"), (),
    )


def _rate_time_explain(v, correct):
    rate, years = _relation_rate(v)
    si = F(v["si"])
    ci = F(v["ci"])
    p = F(v["principal"])
    x = F(si, p * years)
    return _steps([
        f"For {years} years, SI = P×x×{years}, so x = {fmt(si)}/({fmt(p)}×{years}) = {x}.",
        f"Check: P×[(1+{x})^{years}−1] = {money(p * ((1 + x) ** years - 1))} = {money(ci)}.",
        f"Annual rate = {x}×100 = {pct(rate)}.",
    ], correct)


cim_rate_time_relation = make_family(
    "cim_rate_time_relation",
    ("si", "ci", "principal"),
    RATE_TIME_ROWS,
    _rate_time_text,
    _rate_time_answer,
    _pct_distract,
    _rate_time_explain,
)


# ---------------------------------------------------------------------------
# 6. Additional deposit part-way through the term
# ---------------------------------------------------------------------------

VARIABLE_PRINCIPAL_ROWS = (
    (10000, 5000, 10, 4, 2),
    (12000, 8000, 12, 5, 3),
    (15000, 6000, 8, 4, 1),
    (18000, 9000, 10, 5, 2),
    (20000, 10000, 15, 4, 2),
)


def _variable_principal_answer(v):
    p = F(v["principal"])
    addition = F(v["addition"])
    x = F(v["rate"], 100)
    k = v["add_after"]
    n = v["years"]
    return money((p * (1 + x) ** k + addition) * (1 + x) ** (n - k))


def _variable_principal_text(v):
    return _story(
        v,
        "{who} starts with {principal} at {rate} per annum compounded yearly. After "
        "{add_after} years {who} adds {addition} to the same account. Find the balance "
        "at the end of {years} years.",
        ("principal", "addition"), ("rate",),
    )


def _variable_principal_explain(v, correct):
    p = F(v["principal"])
    addition = F(v["addition"])
    x = F(v["rate"], 100)
    k = v["add_after"]
    n = v["years"]
    grown = p * (1 + x) ** k
    base = grown + addition
    final = base * (1 + x) ** (n - k)
    return _steps([
        f"Initial sum after {k} years = {money(p)}×(1+{x})^{k} = {money(grown)}.",
        f"After adding {money(addition)}, the base for the last {n - k} years is {money(base)}.",
        f"Final amount = {money(base)}×(1+{x})^{n - k} = {money(final)}.",
    ], correct)


cim_variable_principal = make_family(
    "cim_variable_principal",
    ("principal", "addition", "rate", "years", "add_after"),
    VARIABLE_PRINCIPAL_ROWS,
    _variable_principal_text,
    _variable_principal_answer,
    _money_distract,
    _variable_principal_explain,
)


# ---------------------------------------------------------------------------
# 7. Equal instalments paid at the start of each year (annuity due)
# ---------------------------------------------------------------------------

INSTALLMENTS_ROWS = (
    (10000, 10, 5),
    (12000, 12, 4),
    (15000, 8, 6),
    (18000, 15, 3),
    (20000, 10, 4),
)


def _installments_answer(v):
    p = F(v["principal"])
    x = F(v["rate"], 100)
    n = v["installments"]
    return money(p * x * (1 + x) ** (n - 1) / ((1 + x) ** n - 1))


def _installments_text(v):
    return _story(
        v,
        "A loan of {principal} is to be cleared in {installments} equal annual instalments, "
        "each paid at the beginning of a year, with interest at {rate} per annum compounded "
        "yearly. Find the amount of each instalment.",
        ("principal",), ("rate",),
    )


def _installments_explain(v, correct):
    p = F(v["principal"])
    x = F(v["rate"], 100)
    n = v["installments"]
    factor = (1 + x) * (1 - (1 + x) ** (-n)) / x
    value = p * x * (1 + x) ** (n - 1) / ((1 + x) ** n - 1)
    return _steps([
        f"Because the first of {n} instalments is paid at once, P = a×[(1+x)×(1−(1+x)^−{n})/x].",
        f"With x = {x}, the present-value factor is {fmt(factor)}.",
        f"a = {money(p)}×{x}×(1+{x})^{n - 1}/[(1+{x})^{n}−1] = {money(value)}.",
    ], correct)


cim_installments = make_family(
    "cim_installments",
    ("principal", "rate", "installments"),
    INSTALLMENTS_ROWS,
    _installments_text,
    _installments_answer,
    _money_distract,
    _installments_explain,
)


# ---------------------------------------------------------------------------
# 8. Effective annual rate of two successive rates
# ---------------------------------------------------------------------------

EFFECTIVE_RATE_ROWS = (
    (10000, 10, 20),
    (12000, 5, 15),
    (15000, 8, 12),
    (18000, 20, 10),
    (20000, 12, 18),
)


def _effective_rate_answer(v):
    p = F(v["principal"])
    amount = p * (1 + F(v["r1"], 100)) * (1 + F(v["r2"], 100))
    return pct((amount - p) * 100 / p)


def _effective_rate_text(v):
    return _story(
        v,
        "A sum of {principal} is grown by {r1} in the first period and by {r2} in the "
        "second period, each applied to the previous balance. Find the single equivalent "
        "rate of return over the whole two-period span.",
        ("principal",), ("r1", "r2"),
    )


def _effective_rate_explain(v, correct):
    p = F(v["principal"])
    amount = p * (1 + F(v["r1"], 100)) * (1 + F(v["r2"], 100))
    return _steps([
        f"Growth factor = (1+{F(v['r1'], 100)})×(1+{F(v['r2'], 100)}) = {fmt(amount / p)}.",
        f"Amount from {money(p)} = {money(amount)}.",
        f"Equivalent rate = ({money(amount)}−{money(p)})×100/{money(p)} = {pct((amount - p) * 100 / p)}.",
    ], correct)


cim_effective_rate = make_family(
    "cim_effective_rate",
    ("principal", "r1", "r2"),
    EFFECTIVE_RATE_ROWS,
    _effective_rate_text,
    _effective_rate_answer,
    _pct_distract,
    _effective_rate_explain,
)


# ---------------------------------------------------------------------------
# 9. Partial withdrawal midway
# ---------------------------------------------------------------------------

PARTIAL_WITHDRAWAL_ROWS = (
    (20000, 10, 5, 8000, 2),
    (24000, 12, 4, 10000, 2),
    (18000, 8, 5, 6000, 3),
    (15000, 15, 4, 5000, 1),
    (12000, 20, 3, 4000, 1),
)


def _partial_withdrawal_answer(v):
    p = F(v["principal"])
    x = F(v["rate"], 100)
    balance = p * (1 + x) ** v["after"] - F(v["withdraw"])
    return money(balance * (1 + x) ** (v["years"] - v["after"]))


def _partial_withdrawal_text(v):
    return _story(
        v,
        "{who} invests {principal} at {rate} per annum compounded annually. At the end of "
        "{after} years {who} withdraws {withdraw}, leaving the rest invested until the end "
        "of year {years}. Find the final balance.",
        ("principal", "withdraw"), ("rate",),
    )


def _partial_withdrawal_explain(v, correct):
    p = F(v["principal"])
    x = F(v["rate"], 100)
    grown = p * (1 + x) ** v["after"]
    balance = grown - F(v["withdraw"])
    final = balance * (1 + x) ** (v["years"] - v["after"])
    return _steps([
        f"At year {v['after']}: {money(p)}×(1+{x})^{v['after']} = {money(grown)}.",
        f"After withdrawing {money(v['withdraw'])}, balance = {money(balance)}.",
        f"For the last {v['years'] - v['after']} years: {money(balance)}×(1+{x})^{v['years'] - v['after']} = {money(final)}.",
    ], correct)


cim_partial_withdrawal = make_family(
    "cim_partial_withdrawal",
    ("principal", "rate", "years", "withdraw", "after"),
    PARTIAL_WITHDRAWAL_ROWS,
    _partial_withdrawal_text,
    _partial_withdrawal_answer,
    _money_distract,
    _partial_withdrawal_explain,
)


# ---------------------------------------------------------------------------
# 10. Two competing schemes
# ---------------------------------------------------------------------------

TWO_SCHEMES_ROWS = (
    (12000, 10, 5, 4),
    (15000, 12, 6, 4),
    (18000, 15, 8, 2),
    (20000, 10, 4, 6),
    (24000, 12, 5, 4),
)


def _two_schemes_answer(v):
    p = F(v["principal"])
    r1 = F(v["rate1"], 100)
    r2 = F(v["rate2"], 100)
    n = v["years"]
    half = n // 2
    scheme_a = p * (1 + r1) ** half * (1 + r2) ** (n - half)
    scheme_b = p * (1 + r2 * n)
    return money(scheme_a - scheme_b)


def _two_schemes_text(v):
    return _story(
        v,
        "Scheme A pays {rate1} per annum compounded yearly for the first half of a "
        "{years}-year term and {rate2} per annum for the second half. Scheme B pays simple "
        "interest at {rate2} per annum for the whole term. If {who} invests {principal} in "
        "each, how much more does the better scheme return?",
        ("principal",), ("rate1", "rate2"),
    )


def _two_schemes_explain(v, correct):
    p = F(v["principal"])
    r1 = F(v["rate1"], 100)
    r2 = F(v["rate2"], 100)
    n = v["years"]
    half = n // 2
    a = p * (1 + r1) ** half * (1 + r2) ** (n - half)
    b = p * (1 + r2 * n)
    return _steps([
        f"Scheme A: {money(p)}×(1+{r1})^{half}×(1+{r2})^{n - half} = {money(a)}.",
        f"Scheme B: {money(p)}×(1+{r2}×{n}) = {money(b)}.",
        f"Advantage of A = {money(a)}−{money(b)} = {money(a - b)}.",
    ], correct)


cim_two_schemes = make_family(
    "cim_two_schemes",
    ("principal", "rate1", "rate2", "years"),
    TWO_SCHEMES_ROWS,
    _two_schemes_text,
    _two_schemes_answer,
    _money_distract,
    _two_schemes_explain,
)


# ---------------------------------------------------------------------------
# 11. Simple interest rate changing midway
# ---------------------------------------------------------------------------

SIMPLE_CHANGE_ROWS = (
    (10000, 10, 12, 2, 5),
    (12000, 8, 10, 3, 5),
    (15000, 12, 9, 2, 4),
    (18000, 15, 10, 1, 4),
    (20000, 6, 12, 3, 5),
)


def _simple_change_answer(v):
    p = F(v["principal"])
    amount = p * (1 + F(v["r1"], 100) * v["change_after"])
    amount *= 1 + F(v["r2"], 100) * (v["years"] - v["change_after"])
    return money(amount)


def _simple_change_text(v):
    return _story(
        v,
        "{who} lends {principal} on simple interest at {r1} per annum for the first "
        "{change_after} years and at {r2} per annum for the rest of a {years}-year term. "
        "Find the total amount receivable at the end.",
        ("principal",), ("r1", "r2"),
    )


def _simple_change_explain(v, correct):
    p = F(v["principal"])
    first = p * (1 + F(v["r1"], 100) * v["change_after"])
    amount = first * (1 + F(v["r2"], 100) * (v["years"] - v["change_after"]))
    return _steps([
        f"First {v['change_after']} years: {money(p)}×(1+{F(v['r1'], 100)}×{v['change_after']}) = {money(first)}.",
        f"Last {v['years'] - v['change_after']} years at {pct(v['r2'])} simple: factor = 1+{F(v['r2'], 100)}×{v['years'] - v['change_after']}.",
        f"Amount = {money(first)}×{fmt(1 + F(v['r2'], 100) * (v['years'] - v['change_after']))} = {money(amount)}.",
    ], correct)


cim_simple_change = make_family(
    "cim_simple_change",
    ("principal", "r1", "r2", "change_after", "years"),
    SIMPLE_CHANGE_ROWS,
    _simple_change_text,
    _simple_change_answer,
    _money_distract,
    _simple_change_explain,
)


# ---------------------------------------------------------------------------
# 12. Population growth then decline
# ---------------------------------------------------------------------------

POPULATION_ROWS = (
    (20000, 10, 4),
    (16000, 15, 4),
    (24000, 20, 3),
    (18000, 8, 5),
    (12000, 25, 4),
)


def _population_answer(v):
    population = F(v["population"])
    growth = F(v["growth"], 100)
    n = v["years"]
    up = (n + 1) // 2
    down = n // 2
    return fmt(population * (1 + growth) ** up * (1 - growth / 2) ** down)


def _population_text(v):
    return _story(
        v,
        "A town begins with {population} residents. Its population grows at {growth} per "
        "annum for the first half of a {years}-year span and then declines at half that "
        "rate for the remaining years. Find the population at the end of the span.",
        (), ("growth",),
    )


def _population_explain(v, correct):
    population = F(v["population"])
    growth = F(v["growth"], 100)
    n = v["years"]
    up = (n + 1) // 2
    down = n // 2
    grown = population * (1 + growth) ** up
    final = grown * (1 - growth / 2) ** down
    return _steps([
        f"Growth years = {up}: {fmt(population)}×(1+{growth})^{up} = {fmt(grown)}.",
        f"Decline rate = {pct(growth * 50)} for {down} years: factor (1−{growth / 2})^{down}.",
        f"Final population = {fmt(final)}.",
    ], correct)


cim_population = make_family(
    "cim_population",
    ("population", "growth", "years"),
    POPULATION_ROWS,
    _population_text,
    _population_answer,
    _count_distract,
    _population_explain,
)


# ---------------------------------------------------------------------------
# 13. Rate that takes a sum to a stated maturity value
# ---------------------------------------------------------------------------

DOUBLING_ROWS = (
    (5000, 3, 8640),
    (8000, 2, 8820),
    (10000, 4, 14641),
    (12000, 3, 20736),
    (16000, 2, 17640),
)


def _doubling_answer(v):
    factor = F(v["amount"], v["principal"])
    root = _root_fraction(factor, v["years"])
    return pct((root - 1) * 100)


def _doubling_text(v):
    return _story(
        v,
        "{who} places {principal} in an annual compound deposit. It matures at {amount} "
        "after {years} years. Find the annual rate of interest.",
        ("principal", "amount"), (),
    )


def _doubling_explain(v, correct):
    factor = F(v["amount"], v["principal"])
    root = _root_fraction(factor, v["years"])
    return _steps([
        f"Overall growth factor = {fmt(v['amount'])}/{fmt(v['principal'])} = {fmt(factor)}.",
        f"Annual factor is the {v['years']}th root of {fmt(factor)}, namely {fmt(root)}.",
        f"Rate = ({fmt(root)}−1)×100 = {pct((root - 1) * 100)}.",
    ], correct)


cim_doubling = make_family(
    "cim_doubling",
    ("principal", "years", "amount"),
    DOUBLING_ROWS,
    _doubling_text,
    _doubling_answer,
    _pct_distract,
    _doubling_explain,
)


# ---------------------------------------------------------------------------
# 14. Interest earned on interest as a share of principal
# ---------------------------------------------------------------------------

INTEREST_ON_INTEREST_ROWS = (
    (10000, 10),
    (12000, 15),
    (15000, 8),
    (18000, 12),
    (20000, 5),
)


def _interest_on_interest_answer(v):
    p = F(v["principal"])
    x = F(v["rate"], 100)
    extra = p * ((1 + x) ** 2 - 1 - 2 * x)
    return pct(extra * 100 / p)


def _interest_on_interest_text(v):
    return _story(
        v,
        "A deposit of {principal} earns {rate} per annum, compounded annually, for two "
        "years. What per cent of the original principal is the interest earned on the "
        "first year's interest during the second year?",
        ("principal",), ("rate",),
    )


def _interest_on_interest_explain(v, correct):
    p = F(v["principal"])
    x = F(v["rate"], 100)
    first = p * x
    on_interest = first * x
    ci_si = p * ((1 + x) ** 2 - 1 - 2 * x)
    return _steps([
        f"First-year interest = {money(p)}×{x} = {money(first)}.",
        f"Second-year interest on that interest = {money(first)}×{x} = {money(on_interest)}.",
        f"As a share of principal: {money(ci_si)}×100/{money(p)} = {pct(ci_si * 100 / p)}.",
    ], correct)


cim_interest_on_interest = make_family(
    "cim_interest_on_interest",
    ("principal", "rate"),
    INTEREST_ON_INTEREST_ROWS,
    _interest_on_interest_text,
    _interest_on_interest_answer,
    _pct_distract,
    _interest_on_interest_explain,
)


# ---------------------------------------------------------------------------
# 15. Simple interest on one sum plus half-yearly compound interest on another
# ---------------------------------------------------------------------------

MIXED_FREQUENCY_ROWS = (
    (20000, 8, 10, 2),
    (16000, 6, 12, 2),
    (24000, 10, 8, 3),
    (18000, 12, 16, 2),
    (12000, 5, 10, 3),
)


def _mixed_frequency_answer(v):
    p = F(v["principal"])
    si = p * F(v["si_rate"], 100) * v["years"]
    ci = p * (1 + F(v["ci_rate"], 200)) ** (2 * v["years"]) - p
    return money(si + ci)


def _mixed_frequency_text(v):
    return _story(
        v,
        "Two equal deposits of {principal} each are made. The first earns simple interest "
        "at {si_rate} per annum; the second earns compound interest at {ci_rate} per annum "
        "credited half-yearly. Both run for {years} years. Find the total interest earned.",
        ("principal",), ("si_rate", "ci_rate"),
    )


def _mixed_frequency_explain(v, correct):
    p = F(v["principal"])
    si = p * F(v["si_rate"], 100) * v["years"]
    ci = p * (1 + F(v["ci_rate"], 200)) ** (2 * v["years"]) - p
    return _steps([
        f"Simple side: {money(p)}×{F(v['si_rate'], 100)}×{v['years']} = {money(si)}.",
        f"Compound side: {money(p)}×[(1+{F(v['ci_rate'], 200)})^{2 * v['years']}−1] = {money(ci)}.",
        f"Total interest = {money(si)} + {money(ci)} = {money(si + ci)}.",
    ], correct)


cim_mixed_frequency = make_family(
    "cim_mixed_frequency",
    ("principal", "si_rate", "ci_rate", "years"),
    MIXED_FREQUENCY_ROWS,
    _mixed_frequency_text,
    _mixed_frequency_answer,
    _money_distract,
    _mixed_frequency_explain,
)


# ---------------------------------------------------------------------------
# 16. Equal instalments paid at the end of each year (ordinary annuity)
# ---------------------------------------------------------------------------

EQUAL_INSTALLMENT_ROWS = (
    (10000, 10, 5),
    (12000, 12, 4),
    (15000, 8, 6),
    (18000, 15, 3),
    (20000, 10, 4),
)


def _equal_installment_answer(v):
    p = F(v["principal"])
    x = F(v["rate"], 100)
    n = v["years"]
    return money(p * x * (1 + x) ** n / ((1 + x) ** n - 1))


def _equal_installment_text(v):
    return _story(
        v,
        "A debt of {principal} is discharged by {years} equal annual payments made at the "
        "end of each year, interest being {rate} per annum compounded annually. Find each payment.",
        ("principal",), ("rate",),
    )


def _equal_installment_explain(v, correct):
    p = F(v["principal"])
    x = F(v["rate"], 100)
    n = v["years"]
    payment = p * x * (1 + x) ** n / ((1 + x) ** n - 1)
    return _steps([
        f"Ordinary annuity: P = a×[(1−(1+x)^−{n})/x], with x = {x}.",
        f"a = {money(p)}×{x}×(1+{x})^{n}/[(1+{x})^{n}−1].",
        f"Each end-of-year payment = {money(payment)}.",
    ], correct)


cim_equal_installment = make_family(
    "cim_equal_installment",
    ("principal", "rate", "years"),
    EQUAL_INSTALLMENT_ROWS,
    _equal_installment_text,
    _equal_installment_answer,
    _money_distract,
    _equal_installment_explain,
)


# ---------------------------------------------------------------------------
# 17. Recurring monthly deposit with monthly compounding
# ---------------------------------------------------------------------------

RECURRING_ROWS = (
    (1000, 12, 12),
    (1500, 9, 24),
    (2000, 10, 12),
    (1200, 8, 18),
    (2500, 12, 24),
)


def _recurring_answer(v):
    deposit = F(v["deposit"])
    rate = F(v["rate"], 1200)
    months = v["months"]
    return money(deposit * ((1 + rate) ** months - 1) / rate)


def _recurring_text(v):
    return _story(
        v,
        "{who} deposits {deposit} at the end of every month in a recurring account paying "
        "{rate} per annum compounded monthly. Find the maturity value after {months} months.",
        ("deposit",), ("rate",),
    )


def _recurring_explain(v, correct):
    deposit = F(v["deposit"])
    rate = F(v["rate"], 1200)
    months = v["months"]
    value = deposit * ((1 + rate) ** months - 1) / rate
    return _steps([
        f"Monthly rate = {v['rate']}/1200 = {fmt(rate)}.",
        f"Maturity factor for {months} end-of-month deposits = [(1+{rate})^{months}−1]/{rate}.",
        f"Maturity value = {money(deposit)}×that factor = {money(value)}.",
    ], correct)


cim_recurring = make_family(
    "cim_recurring",
    ("deposit", "rate", "months"),
    RECURRING_ROWS,
    _recurring_text,
    _recurring_answer,
    _money_distract,
    _recurring_explain,
)


# ---------------------------------------------------------------------------
# 18. Discovering the rate from SI and CI figures
# ---------------------------------------------------------------------------

RATE_DISCOVERY_ROWS = (
    (5000, 1000, 1050, 2),
    (8000, 1200, 1261, 3),
    (10000, 1600, 1664, 2),
    (12000, 3600, 3972, 3),
    (6000, 2400, 2640, 2),
)


def _rate_discovery_answer(v):
    p = F(v["principal"])
    n = v["years"]
    x = F(v["si_amount"], p * n)
    if p * ((1 + x) ** n - 1) != F(v["ci_amount"]):
        root = _root_fraction(1 + F(v["ci_amount"], p), n)
        x = root - 1
    return pct(x * 100)


def _rate_discovery_text(v):
    return _story(
        v,
        "Over {years} years a principal of {principal} earned {si_amount} as simple "
        "interest and {ci_amount} as compound interest at the same annual rate. Find that rate.",
        ("principal", "si_amount", "ci_amount"), (),
    )


def _rate_discovery_explain(v, correct):
    p = F(v["principal"])
    n = v["years"]
    x = F(v["si_amount"], p * n)
    check = p * ((1 + x) ** n - 1)
    return _steps([
        f"From SI: rate fraction x = {money(v['si_amount'])}/({money(p)}×{n}) = {x}.",
        f"Cross-check with CI: {money(p)}×[(1+{x})^{n}−1] = {money(check)} = {money(v['ci_amount'])}.",
        f"Annual rate = {x}×100 = {pct(x * 100)}.",
    ], correct)


cim_rate_discovery = make_family(
    "cim_rate_discovery",
    ("principal", "si_amount", "ci_amount", "years"),
    RATE_DISCOVERY_ROWS,
    _rate_discovery_text,
    _rate_discovery_answer,
    _pct_distract,
    _rate_discovery_explain,
)


# ---------------------------------------------------------------------------
# 19. Fractional year: compound for whole years, simple for the fraction
# ---------------------------------------------------------------------------

FRACTIONAL_YEAR_ROWS = (
    (10000, 10, "3.5"),
    (12000, 8, "4.25"),
    (15000, 12, "2.5"),
    (18000, 6, "3.25"),
    (20000, 15, "5.5"),
)


def _fractional_year_answer(v):
    p = F(v["principal"])
    x = F(v["rate"], 100)
    years = Fraction(v["years"])
    whole = int(years)
    fraction = years - whole
    return money(p * (1 + x) ** whole * (1 + fraction * x))


def _fractional_year_text(v):
    return _story(
        v,
        "{who} invests {principal} at {rate} per annum compounded annually for the whole "
        "years and at simple interest for the fractional part of a {years}-year term. "
        "Find the amount at the end.",
        ("principal",), ("rate",),
    )


def _fractional_year_explain(v, correct):
    p = F(v["principal"])
    x = F(v["rate"], 100)
    years = Fraction(v["years"])
    whole = int(years)
    fraction = years - whole
    grown = p * (1 + x) ** whole
    amount = grown * (1 + fraction * x)
    return _steps([
        f"Whole years = {whole}, remaining fraction = {fmt(fraction)} of a year.",
        f"After whole years: {money(p)}×(1+{x})^{whole} = {money(grown)}.",
        f"Simple factor for the fraction = 1+{fmt(fraction)}×{x}; amount = {money(amount)}.",
    ], correct)


cim_fractional_year = make_family(
    "cim_fractional_year",
    ("principal", "rate", "years"),
    FRACTIONAL_YEAR_ROWS,
    _fractional_year_text,
    _fractional_year_answer,
    _money_distract,
    _fractional_year_explain,
)


# ---------------------------------------------------------------------------
# 20. Total split in a ratio and invested at the two ratio rates
# ---------------------------------------------------------------------------

RATIO_PRINCIPAL_ROWS = (
    (25000, 10, 15, 3),
    (30000, 8, 12, 4),
    (36000, 12, 18, 2),
    (42000, 5, 10, 3),
    (48000, 15, 20, 2),
)


def _ratio_principal_answer(v):
    total = F(v["total"])
    r1, r2 = v["r1"], v["r2"]
    n = v["years"]
    first = total * F(r1, r1 + r2)
    second = total * F(r2, r1 + r2)
    return money(first * (1 + F(r1, 100)) ** n + second * (1 + F(r2, 100)) ** n)


def _ratio_principal_text(v):
    return _story(
        v,
        "A sum of {total} is divided between two annual-compound deposits in the ratio "
        "{r1}:{r2}. The first deposit earns {r1}% per annum and the second earns {r2}% per "
        "annum for {years} years. Find their combined maturity value.",
        ("total",), (),
    )


def _ratio_principal_explain(v, correct):
    total = F(v["total"])
    r1, r2 = v["r1"], v["r2"]
    n = v["years"]
    first = total * F(r1, r1 + r2)
    second = total * F(r2, r1 + r2)
    a1 = first * (1 + F(r1, 100)) ** n
    a2 = second * (1 + F(r2, 100)) ** n
    return _steps([
        f"Shares: {money(total)}×{r1}/{r1 + r2} = {money(first)} and {money(total)}×{r2}/{r1 + r2} = {money(second)}.",
        f"Matured values: {money(first)}×(1+{F(r1, 100)})^{n} = {money(a1)}; {money(second)}×(1+{F(r2, 100)})^{n} = {money(a2)}.",
        f"Combined maturity value = {money(a1 + a2)}.",
    ], correct)


cim_ratio_principal = make_family(
    "cim_ratio_principal",
    ("total", "r1", "r2", "years"),
    RATIO_PRINCIPAL_ROWS,
    _ratio_principal_text,
    _ratio_principal_answer,
    _money_distract,
    _ratio_principal_explain,
)


# ---------------------------------------------------------------------------
# 21. A loss followed by a gain
# ---------------------------------------------------------------------------

LOSS_GAIN_ROWS = (
    (10000, 10, 20),
    (12000, 20, 25),
    (15000, 15, 20),
    (18000, 25, 20),
    (20000, 10, 15),
)


def _loss_gain_answer(v):
    p = F(v["principal"])
    final = p * (1 - F(v["loss"], 100)) * (1 + F(v["gain"], 100))
    return pct((final - p) * 100 / p)


def _loss_gain_text(v):
    return _story(
        v,
        "An investment of {principal} first falls by {loss} and then rises by {gain} on "
        "the reduced value. Find the net percentage change from the original investment.",
        ("principal",), ("loss", "gain"),
    )


def _loss_gain_explain(v, correct):
    p = F(v["principal"])
    lower = p * (1 - F(v["loss"], 100))
    final = lower * (1 + F(v["gain"], 100))
    return _steps([
        f"After the loss: {money(p)}×(1−{F(v['loss'], 100)}) = {money(lower)}.",
        f"After the gain: {money(lower)}×(1+{F(v['gain'], 100)}) = {money(final)}.",
        f"Net change = ({money(final)}−{money(p)})×100/{money(p)} = {pct((final - p) * 100 / p)}.",
    ], correct)


cim_loss_gain = make_family(
    "cim_loss_gain",
    ("principal", "loss", "gain"),
    LOSS_GAIN_ROWS,
    _loss_gain_text,
    _loss_gain_answer,
    _pct_distract,
    _loss_gain_explain,
)


# ---------------------------------------------------------------------------
# 22. Loan balance after a part repayment
# ---------------------------------------------------------------------------

LOAN_REPAYMENT_ROWS = (
    (20000, 10, 4, 8000, 2),
    (24000, 12, 5, 10000, 3),
    (18000, 8, 4, 6000, 2),
    (15000, 15, 3, 5000, 1),
    (12000, 20, 4, 4000, 2),
)


def _loan_repayment_answer(v):
    p = F(v["principal"])
    x = F(v["rate"], 100)
    k = v["after"]
    n = v["years"]
    repay = F(v["repay"])
    balance = p * (1 + x) ** k - repay
    final = balance * (1 + x) ** (n - k)
    return money(repay + final - p)


def _loan_repayment_text(v):
    return _story(
        v,
        "{who} borrows {principal} at {rate} per annum compound interest. After {after} "
        "years {who} repays {repay}, and the balance is settled at the end of year {years}. "
        "Find the total interest paid over the whole transaction.",
        ("principal", "repay"), ("rate",),
    )


def _loan_repayment_explain(v, correct):
    p = F(v["principal"])
    x = F(v["rate"], 100)
    k = v["after"]
    n = v["years"]
    repay = F(v["repay"])
    owed = p * (1 + x) ** k
    balance = owed - repay
    final = balance * (1 + x) ** (n - k)
    return _steps([
        f"Amount owed at year {k} = {money(p)}×(1+{x})^{k} = {money(owed)}.",
        f"Balance after paying {money(repay)} = {money(balance)}; at year {n} it becomes {money(final)}.",
        f"Total interest = {money(repay)} + {money(final)} − {money(p)} = {money(repay + final - p)}.",
    ], correct)


cim_loan_repayment = make_family(
    "cim_loan_repayment",
    ("principal", "rate", "years", "repay", "after"),
    LOAN_REPAYMENT_ROWS,
    _loan_repayment_text,
    _loan_repayment_answer,
    _money_distract,
    _loan_repayment_explain,
)


# ---------------------------------------------------------------------------
# 23. Two different rates within every year
# ---------------------------------------------------------------------------

MIDYEAR_RATE_ROWS = (
    (10000, 8, 12, 3),
    (12000, 10, 14, 2),
    (15000, 6, 10, 4),
    (18000, 12, 16, 2),
    (20000, 5, 15, 3),
)


def _midyear_rate_answer(v):
    p = F(v["principal"])
    factor = (1 + F(v["r1"], 200)) * (1 + F(v["r2"], 200))
    return money(p * factor ** v["years"])


def _midyear_rate_text(v):
    return _story(
        v,
        "In each year, {who}'s deposit of {principal} earns {r1} per annum during the first "
        "half-year and {r2} per annum during the second half-year, both credited half-yearly. "
        "Find the amount after {years} full years.",
        ("principal",), ("r1", "r2"),
    )


def _midyear_rate_explain(v, correct):
    p = F(v["principal"])
    factor = (1 + F(v["r1"], 200)) * (1 + F(v["r2"], 200))
    amount = p * factor ** v["years"]
    return _steps([
        f"First-half factor = 1+{F(v['r1'], 200)}; second-half factor = 1+{F(v['r2'], 200)}.",
        f"Effective yearly factor = {fmt(factor)}.",
        f"Amount = {money(p)}×{fmt(factor)}^{v['years']} = {money(amount)}.",
    ], correct)


cim_midyear_rate = make_family(
    "cim_midyear_rate",
    ("principal", "r1", "r2", "years"),
    MIDYEAR_RATE_ROWS,
    _midyear_rate_text,
    _midyear_rate_answer,
    _money_distract,
    _midyear_rate_explain,
)


# ---------------------------------------------------------------------------
# 24. Monthly compounding on a lump sum
# ---------------------------------------------------------------------------

MONTHLY_COMPOUND_ROWS = (
    (20000, 12, 2),
    (16000, 9, 3),
    (24000, 6, 2),
    (18000, 18, 2),
    (12000, 24, 3),
)


def _monthly_compound_answer(v):
    p = F(v["principal"])
    rate = F(v["annual_rate"], 1200)
    return money(p * (1 + rate) ** (12 * v["years"]))


def _monthly_compound_text(v):
    return _story(
        v,
        "{who} invests {principal} at {annual_rate} per annum with interest compounded "
        "every month. What is the maturity value after {years} years?",
        ("principal",), ("annual_rate",),
    )


def _monthly_compound_explain(v, correct):
    p = F(v["principal"])
    rate = F(v["annual_rate"], 1200)
    months = 12 * v["years"]
    amount = p * (1 + rate) ** months
    return _steps([
        f"Monthly rate = {v['annual_rate']}/1200 = {fmt(rate)}.",
        f"Number of months = 12×{v['years']} = {months}.",
        f"Amount = {money(p)}×(1+{rate})^{months} = {money(amount)}.",
    ], correct)


cim_monthly_compound = make_family(
    "cim_monthly_compound",
    ("principal", "annual_rate", "years"),
    MONTHLY_COMPOUND_ROWS,
    _monthly_compound_text,
    _monthly_compound_answer,
    _money_distract,
    _monthly_compound_explain,
)


FAMILIES = [
    cim_successive_rates,
    cim_half_yearly,
    cim_quarterly,
    cim_ci_si_diff,
    cim_rate_time_relation,
    cim_variable_principal,
    cim_installments,
    cim_effective_rate,
    cim_partial_withdrawal,
    cim_two_schemes,
    cim_simple_change,
    cim_population,
    cim_doubling,
    cim_interest_on_interest,
    cim_mixed_frequency,
    cim_equal_installment,
    cim_recurring,
    cim_rate_discovery,
    cim_fractional_year,
    cim_ratio_principal,
    cim_loss_gain,
    cim_loan_repayment,
    cim_midyear_rate,
    cim_monthly_compound,
]


def build_simple_and_compound_interest_mains():
    return build_specs(FAMILIES, mains=True)


def self_test():
    """Check all 120 builder answers against the independent formula sheet."""
    from .formulas_interest import FORMULAS

    assert len(FAMILIES) == 24
    assert len(FORMULAS) == 24
    seen = set()
    matches = 0
    for builder in FAMILIES:
        first = builder(None, 0)
        family = first["verification_data"]["family"]
        assert family not in seen, family
        seen.add(family)
        assert family in FORMULAS, family
        for variant in range(5):
            spec = builder(None, variant)
            inputs = spec["verification_data"]["inputs"]
            assert set(inputs) == set(first["verification_data"]["inputs"]), family
            assert len(spec["distractors"]) == 3, (family, variant)
            expected = FORMULAS[family](inputs)
            assert spec["correct"] == expected, (family, variant, spec["correct"], expected)
            matches += 1
    assert seen == set(FORMULAS)
    assert matches == 120
    return matches


if __name__ == "__main__":
    print(f"self-test: {self_test()} matches")
