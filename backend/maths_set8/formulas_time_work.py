# -*- coding: utf-8 -*-
"""Independent answer sheet for Time & Work Set 8 (Mains).

The verifier passes the exact ``verification_data.inputs`` dictionary from a
question to the callable stored here. No chapter builder is imported.
"""

from __future__ import annotations

from .formula_helpers import F, fmt, money, ratio

FORMULAS = {}


def _inv(value):
    return F(1) / F(value)


def _cycle_days(remaining, rates):
    extra = F(0)
    index = 0
    while remaining > 0 and index < 1000:
        rate = rates[index % len(rates)]
        if remaining <= rate:
            return extra + remaining / rate
        remaining -= rate
        extra += 1
        index += 1
    return extra


def _stage_exit(d):
    a, b, c, leave = F(d["a"]), F(d["b"]), F(d["c"]), F(d["leave"])
    done = leave * (_inv(a) + _inv(b))
    remaining = F(1) - done
    return leave + remaining / (_inv(b) + _inv(c))


def _alternating_three(d):
    a, b, c = F(d["a"]), F(d["b"]), F(d["c"])
    n = int(d["n"])
    rates = [_inv(a), _inv(b), _inv(c)]
    full, tail = divmod(n, 3)
    done = full * sum(rates) + sum(rates[:tail])
    order = rates[tail:] + rates[:tail]
    return F(n) + _cycle_days(F(1) - done, order)


def _negative_contributor(d):
    a, b, c, till = F(d["a"]), F(d["b"]), F(d["c"]), F(d["till"])
    done = till * (_inv(a) - _inv(c))
    return (F(1) - done) / (_inv(a) + _inv(b) - _inv(c))


def _efficiency_change(d):
    a, b, shift = F(d["a"]), F(d["b"]), F(d["shift"])
    factor = F(1) + F(d["change"]) / F(100)
    done = shift * (_inv(a) + _inv(b))
    return shift + (F(1) - done) / (_inv(a) * factor + _inv(b))


def _wage_contribution(d):
    a, b, c = F(d["a"]), F(d["b"]), F(d["c"])
    initial, total = F(d["initial"]), F(d["total_wage"])
    done = initial * (_inv(a) + _inv(b))
    remaining = F(1) - done
    extra = remaining / (_inv(a) + _inv(b) + _inv(c))
    return total * ((initial + extra) / a)


def _man_day_absentee(d):
    men, days = F(d["men"]), F(d["days"])
    absent, early = F(d["absent"]), F(d["extra_after"])
    return days + absent * early / men


def _fractional_join(d):
    a, b = F(d["a"]), F(d["b"])
    fraction = F(d["frac"]) / F(100)
    joint = _inv(a) + _inv(b)
    return fraction / joint + (F(1) - fraction) * a


def _machine_output(d):
    a, b = F(d["a"]), F(d["b"])
    waste = F(d["waste"]) / F(100)
    good_rate = _inv(a) * (F(1) - waste) + _inv(b) * (F(1) - 2 * waste)
    return F(1) / good_rate


def _time_ratio_pair(d):
    ra, rb, together = F(d["ra"]), F(d["rb"]), F(d["together"])
    scale = together * (ra + rb) / (ra * rb)
    solo_a = ra * scale
    return together / F(2) + solo_a / F(2)


def _work_equivalence(d):
    rates = [
        F(d["m"]) / F(d["pm"]),
        F(d["w"]) / F(d["pw"]),
        F(d["b"]) / F(d["pb"]),
    ]
    return _cycle_days(F(1), rates)


def _three_team_rotation(d):
    a, b, c = F(d["a"]), F(d["b"]), F(d["c"])
    r1 = _inv(a)
    r2 = r1 + _inv(b)
    r3 = r2 + _inv(c)
    block = r1 + r2 + r3
    full = int(F(1) / block)
    return F(3 * full) + _cycle_days(F(1) - full * block, [r1, r2, r3])


def _piece_rate_drop(d):
    rate = F(d["rate"])
    pieces, after = F(d["pieces"]), F(d["after"])
    drop = F(d["drop"]) / F(100)
    reduced = rate * (F(1) - drop)
    return after * rate + (pieces - after) * reduced


FORMULAS["twm_stage_exit_join"] = lambda d: fmt(_stage_exit(d))
FORMULAS["twm_alternating_three"] = lambda d: fmt(_alternating_three(d))
FORMULAS["twm_negative_contributor"] = lambda d: fmt(_negative_contributor(d))
FORMULAS["twm_efficiency_change"] = lambda d: fmt(_efficiency_change(d))
FORMULAS["twm_wage_contribution"] = lambda d: money(_wage_contribution(d))
FORMULAS["twm_man_day_absentee"] = lambda d: fmt(_man_day_absentee(d))
FORMULAS["twm_fractional_join"] = lambda d: fmt(_fractional_join(d))
FORMULAS["twm_machine_output"] = lambda d: fmt(_machine_output(d))
FORMULAS["twm_time_ratio_pair"] = lambda d: fmt(_time_ratio_pair(d))
FORMULAS["twm_work_equivalence"] = lambda d: fmt(_work_equivalence(d))
FORMULAS["twm_three_team_rotation"] = lambda d: fmt(_three_team_rotation(d))
FORMULAS["twm_piece_rate_drop"] = lambda d: money(_piece_rate_drop(d))


def _double_half(d):
    a, b, shift = F(d["a"]), F(d["b"]), F(d["shift"])
    done = shift * (_inv(a) + _inv(b))
    new_rate = 2 * _inv(a) + _inv(b) / F(2)
    return shift + (F(1) - done) / new_rate


def _deadline_extra(d):
    a, deadline = F(d["a"]), F(d["deadline"])
    early, helpers = F(d["extra_after"]), F(d["helpers"])
    alone = deadline - early
    return deadline - (alone + (a - alone) / (helpers + F(1)))


def _trainee_growth(d):
    a, b = F(d["a"]), F(d["b"])
    factor = F(1) + F(d["growth"]) / F(100)
    n, step = int(d["n"]), int(d["step"])
    work = F(0)
    elapsed = 0
    stage = 0
    while elapsed < n:
        block = min(step, n - elapsed)
        work += F(block) * (_inv(a) * factor ** stage + _inv(b))
        elapsed += block
        stage += 1
    return work


def _contract_penalty(d):
    a, b, deadline = F(d["a"]), F(d["b"]), F(d["deadline"])
    base, bonus, penalty = F(d["base"]), F(d["bonus"]), F(d["penalty"])
    days = a * b / (a + b)
    margin = deadline - days
    return base + bonus * margin if margin >= 0 else base - penalty * (-margin)


def _partial_overlap(d):
    a, b, x, y, z = F(d["a"]), F(d["b"]), F(d["x"]), F(d["y"]), F(d["z"])
    done = x * _inv(a) + y * (_inv(a) + _inv(b)) + z * _inv(b)
    return F(1) - done


def _absentee_cycle(d):
    a, b, c = F(d["a"]), F(d["b"]), F(d["c"])
    n = int(d["n"])
    pairs = [_inv(a) + _inv(b), _inv(b) + _inv(c), _inv(c) + _inv(a)]
    full, tail = divmod(n, 3)
    return full * sum(pairs) + sum(pairs[:tail])


def _inverse_efficiency(d):
    together = F(d["together"])
    factor = F(1) + F(d["eta"]) / F(100)
    slow_rate = F(1) / (together * (factor + F(1)))
    return (F(1) - together * slow_rate) * together


def _reverse_pair(d):
    together, a = F(d["together"]), F(d["a"])
    lag = a - together
    return together * (F(1) - lag * lag / (together * a))


def _wage_after_leave(d):
    a, b, leave = F(d["a"]), F(d["b"]), F(d["leave"])
    total = F(d["total_wage"])
    done = leave * (_inv(a) + _inv(b))
    return total * (leave / b + (F(1) - done))


def _parallel_groups(d):
    m, n, a, b = F(d["m"]), F(d["n"]), F(d["a"]), F(d["b"])
    first = a / (F(2) * m)
    second = b / (F(2) * n)
    joint = m / a + n / b
    if first <= second:
        remaining = F(1, 2) - first * n / b
        return first + remaining / joint
    remaining = F(1, 2) - second * m / a
    return second + remaining / joint


def _multistage_bonus(d):
    a, b, c, after = F(d["a"]), F(d["b"]), F(d["c"]), F(d["after"])
    bonus = F(d["bonus"])
    done = after * (_inv(a) + _inv(b))
    remaining = F(1) - done
    return bonus * (a - (after + remaining / (_inv(a) + _inv(b) + _inv(c))))


def _capacity_reallocation(d):
    a, b, c, move = F(d["a"]), F(d["b"]), F(d["c"]), F(d["move_day"])
    done = move * (_inv(a) + _inv(b))
    extra = (F(1) - done) / (_inv(b) + _inv(c))
    return ratio(move + extra, extra)


FORMULAS["twm_double_half"] = lambda d: fmt(_double_half(d))
FORMULAS["twm_deadline_extra"] = lambda d: fmt(_deadline_extra(d))
FORMULAS["twm_trainee_growth"] = lambda d: fmt(_trainee_growth(d))
FORMULAS["twm_contract_penalty"] = lambda d: money(_contract_penalty(d))
FORMULAS["twm_partial_overlap"] = lambda d: fmt(_partial_overlap(d))
FORMULAS["twm_absentee_cycle"] = lambda d: fmt(_absentee_cycle(d))
FORMULAS["twm_inverse_efficiency"] = lambda d: fmt(_inverse_efficiency(d))
FORMULAS["twm_reverse_pair"] = lambda d: fmt(_reverse_pair(d))
FORMULAS["twm_wage_after_leave"] = lambda d: money(_wage_after_leave(d))
FORMULAS["twm_parallel_groups"] = lambda d: fmt(_parallel_groups(d))
FORMULAS["twm_multistage_bonus"] = lambda d: money(_multistage_bonus(d))
FORMULAS["twm_capacity_reallocation"] = lambda d: fmt(_capacity_reallocation(d))
