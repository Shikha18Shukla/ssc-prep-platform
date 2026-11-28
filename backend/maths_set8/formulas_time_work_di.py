# -*- coding: utf-8 -*-
"""Independent verifier formulas for Time and Work — Data Interpretation.

Every callable consumes only the JSON-serializable ``inputs`` stored by the
builder and returns the exact displayed answer string.
"""

from __future__ import annotations

from .formula_helpers import F, fmt, money, pct, ratio


def _money(value):
    return money(F(value))


def _pct(value):
    return pct(F(value))


# 01 ------------------------------------------------------------------------


def _f_solo_days(d):
    a, b = d["a"], d["b"]
    together = F(a * b, a + b)
    return fmt((a, b, together, a - together)[d["ask"]])


# 02 ------------------------------------------------------------------------


def _f_daily_rate(d):
    a, b, n = d["a"], d["b"], d["n"]
    return _money((a * n, b * n, a + b, (a + b) * n)[d["ask"]])


# 03 ------------------------------------------------------------------------


def _f_work_done(d):
    a, b, da, db = d["a"], d["b"], d["da"], d["db"]
    return fmt(F((a * da, b * db, a * da + b * db, abs(a * da - b * db))[
        d["ask"]
    ]))


# 04 ------------------------------------------------------------------------


def _wage_ratio_shares(d):
    a, b, total = d["a"], d["b"], d["total_wage"]
    return F(total * b, a + b), F(total * a, a + b)


def _f_wage_ratio(d):
    share_a, share_b = _wage_ratio_shares(d)
    if d["ask"] == 0:
        return ratio(share_a, share_b)
    if d["ask"] == 1:
        return _money(share_a)
    if d["ask"] == 2:
        return _money(share_b)
    return _money(abs(share_a - share_b))


# 05 ------------------------------------------------------------------------


def _f_efficiency_share(d):
    ea, eb, ec, total = d["ea"], d["eb"], d["ec"], d["total_work"]
    strength = ea + eb + ec
    if d["ask"] == 3:
        return _pct(F(100 * ea, strength))
    return fmt(F(total * (ea, eb, ec)[d["ask"]], strength))


# 06 ------------------------------------------------------------------------


def _f_man_days(d):
    men, days, absent = d["men"], d["days"], d["absent"]
    planned = men * days
    actual = planned - absent
    return fmt(F((planned, actual, absent, F(actual, men))[d["ask"]]))


# 07 ------------------------------------------------------------------------


def _f_missing_days(d):
    work, per_day = d["work"], d["per_day"]
    days = F(work, per_day)
    return fmt((days, F(work, 2 * per_day), F(2 * work, per_day), days - 5)[
        d["ask"]
    ])


# 08 ------------------------------------------------------------------------


def _f_combined_rate(d):
    a, b = d["a"], d["b"]
    rate = F(a + b)
    return fmt(F((rate, 4 * rate, F(120, a + b), 4 * abs(a - b))[d["ask"]]))


# 09 ------------------------------------------------------------------------


def _f_two_day_cycle(d):
    a, b, n = d["a"], d["b"], d["n"]
    full, extra = divmod(n, 2)
    total = full * (a + b) + (a if extra else 0)
    return fmt(F((total, (full + extra) * a, full * b, F(total, n))[d["ask"]]))


# 10 ------------------------------------------------------------------------


def _remaining_parts(d):
    a, b, days = d["a"], d["b"], d["days"]
    together = F(a * b, a + b)
    done = F(a + b, a * b) * days
    left = 1 - done
    return together, done, left, left * together, a - (days + left * together)


def _f_remaining_work(d):
    _together, done, left, rest_days, saved = _remaining_parts(d)
    return fmt((done, left, rest_days, saved)[d["ask"]])


# 11 ------------------------------------------------------------------------


def _f_average_days(d):
    a, b, c = d["a"], d["b"], d["c"]
    together = F(1, F(1, a) + F(1, b) + F(1, c))
    return fmt((F(a + b + c, 3), together, max(a, b, c) - min(a, b, c),
                F(a + b, 2))[d["ask"]])


# 12 ------------------------------------------------------------------------


def _f_ratio_fraction(d):
    a, b = d["a"], d["b"]
    if d["ask"] == 0:
        return ratio(b, a)
    if d["ask"] == 1:
        return fmt(F(b, a + b))
    if d["ask"] == 2:
        return fmt(F(a, a + b))
    return ratio(a, b)


# 13 ------------------------------------------------------------------------


def _f_piece_count(d):
    rate, days, bonus = d["rate"], d["days"], d["bonus"]
    pieces = rate * days
    if d["ask"] == 3:
        return _money(F(pieces * bonus))
    return fmt(F((pieces, 2 * rate, F(100, rate))[d["ask"]]))


# 14 ------------------------------------------------------------------------


def _f_absentee_lookup(d):
    a, b, c, idx = d["a"], d["b"], d["c"], d["absent_day"]
    outputs = (a, b, c)
    full = a + b + c
    reduced = full - outputs[idx]
    return fmt(F((reduced, full, outputs[idx], reduced + full)[d["ask"]]))


# 15 ------------------------------------------------------------------------


def _f_wage_per_worker(d):
    a, b, total = d["a"], d["b"], d["total_wage"]
    wa, wb = F(total * a, a + b), F(total * b, a + b)
    return _money((wa, wb, abs(wa - wb), F(wa, a))[d["ask"]])


# 16 ------------------------------------------------------------------------


def _f_efficiency_ratio(d):
    a, b = d["a"], d["b"]
    if d["ask"] == 0:
        return ratio(b, a)
    if d["ask"] == 1:
        return _pct(F(100 * b, a + b))
    if d["ask"] == 2:
        return _pct(F(100 * a, a + b))
    return ratio(a, b)


# 17 ------------------------------------------------------------------------


def _f_time_saved(d):
    a, b, deadline = d["a"], d["b"], d["deadline"]
    together = F(a * b, a + b)
    return fmt(F((together, deadline - together, a - together, b - together)[
        d["ask"]
    ]))


# 18 ------------------------------------------------------------------------


def _partial_parts(d):
    a, b, x = d["a"], d["b"], d["x"]
    done = F(x, a)
    left = 1 - done
    rest_days = left * F(a * b, a + b)
    return done, left, rest_days, x + rest_days


def _f_partial_work(d):
    return fmt(_partial_parts(d)[d["ask"]])


# 19 ------------------------------------------------------------------------


def _f_machine_units(d):
    ma, mb, hours = d["ma"], d["mb"], d["hours"]
    return fmt(F((ma * hours, mb * hours, (ma + mb) * hours,
                  abs(ma - mb) * hours)[d["ask"]]))


# 20 ------------------------------------------------------------------------


def _three_share_parts(d):
    a, b, c, total = d["a"], d["b"], d["c"], d["total_wage"]
    strength = a + b + c
    return F(total * a, strength), F(total * b, strength), F(total * c, strength)


def _f_three_share(d):
    wa, wb, wc = _three_share_parts(d)
    if d["ask"] == 3:
        return _money(max(wa, wb, wc) - min(wa, wb, wc))
    return _money((wa, wb, wc)[d["ask"]])


# 21 ------------------------------------------------------------------------


def _f_conditional_bonus(d):
    a, b, target, bonus = d["a"], d["b"], d["target"], d["bonus"]
    out = a + b
    payout = F(bonus) if out > target else F(0)
    if d["ask"] == 0:
        return fmt(F(out))
    if d["ask"] == 1:
        return _money(payout)
    if d["ask"] == 2:
        return _money(5 * payout)
    return fmt(F(abs(out - target)))


# 22 ------------------------------------------------------------------------


def _f_capacity_use(d):
    capacity, used, rate = d["capacity"], d["used"], d["rate"]
    if d["ask"] == 0:
        return fmt(F(capacity - used))
    if d["ask"] == 1:
        return _pct(F(100 * used, capacity))
    if d["ask"] == 2:
        return _money(F(used * rate))
    return _money(F(capacity * rate))


# 23 ------------------------------------------------------------------------


def _f_cost_job(d):
    a, b, wage_a, wage_b = d["a"], d["b"], d["wage_a"], d["wage_b"]
    ca, cb = F(a * wage_a), F(b * wage_b)
    return _money((ca, cb, ca + cb, abs(ca - cb))[d["ask"]])


# 24 ------------------------------------------------------------------------


def _f_target_days(d):
    work, rate, increment = d["work"], d["rate"], d["increment"]
    current = F(work, rate)
    improved = F(work, rate + increment)
    return fmt((current, improved, current - improved, 3 * (rate + increment))[
        d["ask"]
    ])


FORMULAS = {
    "twd_solo_days": _f_solo_days,
    "twd_daily_rate": _f_daily_rate,
    "twd_work_done": _f_work_done,
    "twd_wage_ratio": _f_wage_ratio,
    "twd_efficiency_share": _f_efficiency_share,
    "twd_man_days": _f_man_days,
    "twd_missing_days": _f_missing_days,
    "twd_combined_rate": _f_combined_rate,
    "twd_two_day_cycle": _f_two_day_cycle,
    "twd_remaining_work": _f_remaining_work,
    "twd_average_days": _f_average_days,
    "twd_ratio_fraction": _f_ratio_fraction,
    "twd_piece_count": _f_piece_count,
    "twd_absentee_lookup": _f_absentee_lookup,
    "twd_wage_per_worker": _f_wage_per_worker,
    "twd_efficiency_ratio": _f_efficiency_ratio,
    "twd_time_saved": _f_time_saved,
    "twd_partial_work": _f_partial_work,
    "twd_machine_units": _f_machine_units,
    "twd_three_share": _f_three_share,
    "twd_conditional_bonus": _f_conditional_bonus,
    "twd_capacity_use": _f_capacity_use,
    "twd_cost_job": _f_cost_job,
    "twd_target_days": _f_target_days,
}
