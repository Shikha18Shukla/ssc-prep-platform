# -*- coding: utf-8 -*-
"""Time & Work (Mains) - 120 original, HARD, multi-step questions.

Every family has five concrete variants and is checked against the independent
formula sheet in ``formulas_time_work.py``.
"""

from __future__ import annotations

from .common import (
    F,
    build_specs,
    fmt,
    make_family,
    money,
    near_money,
    near_num,
    ratio,
    ratio_distractors,
)

SOURCE_PDF = "87fda602-e97e-4aa7-90cc-9f316d0af672.pdf"
PAGES = {
    1: f"{SOURCE_PDF}, pp. 4-5",
    2: f"{SOURCE_PDF}, pp. 6-7",
    3: f"{SOURCE_PDF}, pp. 8-9",
    4: f"{SOURCE_PDF}, pp. 10-11",
}


# ---------------------------------------------------------------------------
# Exact-arithmetic helpers (builder side)
# ---------------------------------------------------------------------------

def _inv(value):
    return F(1) / F(value)


def _cycle_days(remaining, rates):
    """Days needed to clear ``remaining`` work at cyclically repeated rates."""
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


# ---------------------------------------------------------------------------
# Exact answer functions (1-12)
# ---------------------------------------------------------------------------

def _ans_stage_exit(d):
    a, b, c, leave = F(d["a"]), F(d["b"]), F(d["c"]), F(d["leave"])
    done = leave * (_inv(a) + _inv(b))
    remaining = F(1) - done
    extra = remaining / (_inv(b) + _inv(c))
    return leave + extra


def _ans_alternating_three(d):
    a, b, c = F(d["a"]), F(d["b"]), F(d["c"])
    n = int(d["n"])
    rates = [_inv(a), _inv(b), _inv(c)]
    full, tail = divmod(n, 3)
    done = full * sum(rates) + sum(rates[:tail])
    order = rates[tail:] + rates[:tail]
    return F(n) + _cycle_days(F(1) - done, order)


def _ans_negative_contributor(d):
    a, b, c, till = F(d["a"]), F(d["b"]), F(d["c"]), F(d["till"])
    done = till * (_inv(a) - _inv(c))
    remaining = F(1) - done
    net = _inv(a) + _inv(b) - _inv(c)
    return remaining / net


def _ans_efficiency_change(d):
    a, b, shift = F(d["a"]), F(d["b"]), F(d["shift"])
    factor = F(1) + F(d["change"]) / F(100)
    done = shift * (_inv(a) + _inv(b))
    remaining = F(1) - done
    return shift + remaining / (_inv(a) * factor + _inv(b))


def _ans_wage_contribution(d):
    a, b, c = F(d["a"]), F(d["b"]), F(d["c"])
    initial, total = F(d["initial"]), F(d["total_wage"])
    done = initial * (_inv(a) + _inv(b))
    remaining = F(1) - done
    extra = remaining / (_inv(a) + _inv(b) + _inv(c))
    return total * ((initial + extra) / a)


def _ans_man_day_absentee(d):
    men, days = F(d["men"]), F(d["days"])
    absent, early = F(d["absent"]), F(d["extra_after"])
    return days + absent * early / men


def _ans_fractional_join(d):
    a, b = F(d["a"]), F(d["b"])
    fraction = F(d["frac"]) / F(100)
    joint = _inv(a) + _inv(b)
    first = fraction / joint
    return first + (F(1) - fraction) * a


def _ans_machine_output(d):
    a, b = F(d["a"]), F(d["b"])
    waste = F(d["waste"]) / F(100)
    good_rate = _inv(a) * (F(1) - waste) + _inv(b) * (F(1) - 2 * waste)
    return F(1) / good_rate


def _ans_time_ratio_pair(d):
    ra, rb, together = F(d["ra"]), F(d["rb"]), F(d["together"])
    scale = together * (ra + rb) / (ra * rb)
    solo_a = ra * scale
    return together / F(2) + solo_a / F(2)


def _ans_work_equivalence(d):
    rates = [
        F(d["m"]) / F(d["pm"]),
        F(d["w"]) / F(d["pw"]),
        F(d["b"]) / F(d["pb"]),
    ]
    return _cycle_days(F(1), rates)


def _ans_three_team_rotation(d):
    a, b, c = F(d["a"]), F(d["b"]), F(d["c"])
    r1 = _inv(a)
    r2 = r1 + _inv(b)
    r3 = r2 + _inv(c)
    block = r1 + r2 + r3
    full = int(F(1) / block)
    return F(3 * full) + _cycle_days(F(1) - full * block, [r1, r2, r3])


def _ans_piece_rate_drop(d):
    rate = F(d["rate"])
    pieces, after = F(d["pieces"]), F(d["after"])
    drop = F(d["drop"]) / F(100)
    reduced = rate * (F(1) - drop)
    return after * rate + (pieces - after) * reduced


# ---------------------------------------------------------------------------
# Exact answer functions (13-24)
# ---------------------------------------------------------------------------

def _ans_double_half(d):
    a, b, shift = F(d["a"]), F(d["b"]), F(d["shift"])
    done = shift * (_inv(a) + _inv(b))
    new_rate = 2 * _inv(a) + _inv(b) / F(2)
    return shift + (F(1) - done) / new_rate


def _ans_deadline_extra(d):
    a, deadline = F(d["a"]), F(d["deadline"])
    early, helpers = F(d["extra_after"]), F(d["helpers"])
    alone = deadline - early
    actual = alone + (a - alone) / (helpers + F(1))
    return deadline - actual


def _ans_trainee_growth(d):
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


def _ans_contract_penalty(d):
    a, b, deadline = F(d["a"]), F(d["b"]), F(d["deadline"])
    base, bonus, penalty = F(d["base"]), F(d["bonus"]), F(d["penalty"])
    days = a * b / (a + b)
    margin = deadline - days
    return base + bonus * margin if margin >= 0 else base - penalty * (-margin)


def _ans_partial_overlap(d):
    a, b, x, y, z = F(d["a"]), F(d["b"]), F(d["x"]), F(d["y"]), F(d["z"])
    done = x * _inv(a) + y * (_inv(a) + _inv(b)) + z * _inv(b)
    return F(1) - done


def _ans_absentee_cycle(d):
    a, b, c = F(d["a"]), F(d["b"]), F(d["c"])
    n = int(d["n"])
    pairs = [_inv(a) + _inv(b), _inv(b) + _inv(c), _inv(c) + _inv(a)]
    full, tail = divmod(n, 3)
    return full * sum(pairs) + sum(pairs[:tail])


def _ans_inverse_efficiency(d):
    together = F(d["together"])
    factor = F(1) + F(d["eta"]) / F(100)
    slow_rate = F(1) / (together * (factor + F(1)))
    return (F(1) - together * slow_rate) * together


def _ans_reverse_pair(d):
    together, a = F(d["together"]), F(d["a"])
    lag = a - together
    return together * (F(1) - lag * lag / (together * a))


def _ans_wage_after_leave(d):
    a, b, leave = F(d["a"]), F(d["b"]), F(d["leave"])
    total = F(d["total_wage"])
    done = leave * (_inv(a) + _inv(b))
    return total * (leave / b + (F(1) - done))


def _ans_parallel_groups(d):
    m, n, a, b = F(d["m"]), F(d["n"]), F(d["a"]), F(d["b"])
    first = a / (F(2) * m)
    second = b / (F(2) * n)
    joint = m / a + n / b
    if first <= second:
        remaining = F(1, 2) - first * n / b
        return first + remaining / joint
    remaining = F(1, 2) - second * m / a
    return second + remaining / joint


def _ans_multistage_bonus(d):
    a, b, c, after = F(d["a"]), F(d["b"]), F(d["c"]), F(d["after"])
    bonus = F(d["bonus"])
    done = after * (_inv(a) + _inv(b))
    remaining = F(1) - done
    total = after + remaining / (_inv(a) + _inv(b) + _inv(c))
    return bonus * (a - total)


def _ans_capacity_reallocation(d):
    a, b, c, move = F(d["a"]), F(d["b"]), F(d["c"]), F(d["move_day"])
    done = move * (_inv(a) + _inv(b))
    extra = (F(1) - done) / (_inv(b) + _inv(c))
    return ratio(move + extra, extra)


# ---------------------------------------------------------------------------
# Type-matched distractors for the money/ratio answers
# ---------------------------------------------------------------------------

def _dist_wage_contribution(result, d):
    return near_money(_ans_wage_contribution(d), 500)


def _dist_piece_rate_drop(result, d):
    return near_money(_ans_piece_rate_drop(d), 500)


def _dist_contract_penalty(result, d):
    return near_money(_ans_contract_penalty(d), 500)


def _dist_wage_after_leave(result, d):
    return near_money(_ans_wage_after_leave(d), 500)


def _dist_multistage_bonus(result, d):
    return near_money(_ans_multistage_bonus(d), 300)


def _dist_capacity_reallocation(result, d):
    return ratio_distractors(result)


def _near_fraction(result, d):
    return near_num(result, F(1, 10))


def _near_half(result, d):
    return near_num(result, F(1, 2))


# ---------------------------------------------------------------------------
# Families 1-6
# ---------------------------------------------------------------------------

def _t_stage_exit(d):
    return (
        f"Aarav, Meera and Rohan are engaged on the same assignment. Working alone, they would finish it in "
        f"{fmt(d['a'])}, {fmt(d['b'])} and {fmt(d['c'])} days respectively. Aarav and Meera start together; "
        f"after {fmt(d['leave'])} days Aarav is withdrawn and Rohan takes his place alongside Meera until the "
        f"assignment is over. How many days from the start does the whole assignment take?"
    )


def _e_stage_exit(d, correct):
    a, b, c, leave = F(d["a"]), F(d["b"]), F(d["c"]), F(d["leave"])
    first = leave * (_inv(a) + _inv(b))
    remaining = F(1) - first
    rate = _inv(b) + _inv(c)
    extra = remaining / rate
    return (
        f"First {fmt(leave)} days at rate {fmt(_inv(a) + _inv(b))}/day finish {fmt(first)}; "
        f"{fmt(remaining)} remains at rate {fmt(rate)}/day, needing {fmt(extra)} more days. "
        f"Total time = {correct} days."
    )


twm_stage_exit_join = make_family(
    "twm_stage_exit_join",
    ["a", "b", "c", "leave"],
    [
        (12, 18, 24, 4), (15, 20, 30, 5), (10, 15, 25, 3),
        (16, 24, 36, 6), (14, 21, 28, 4),
    ],
    _t_stage_exit, _ans_stage_exit, explain=_e_stage_exit,
)


def _t_alternating_three(d):
    return (
        f"Neha, Kabir and Priya would individually need {fmt(d['a'])}, {fmt(d['b'])} and {fmt(d['c'])} days "
        f"to finish a report. They work in strict daily rotation: Neha on day 1, Kabir on day 2, Priya on day 3, "
        f"then the same order repeats, with only the named person working on that day. After {fmt(d['n'])} days "
        f"of this pattern the rotation continues unchanged. Find the total number of days from the start when "
        f"the report is completed."
    )


def _e_alternating_three(d, correct):
    a, b, c = F(d["a"]), F(d["b"]), F(d["c"])
    n = int(d["n"])
    rates = [_inv(a), _inv(b), _inv(c)]
    full, tail = divmod(n, 3)
    done = full * sum(rates) + sum(rates[:tail])
    order = rates[tail:] + rates[:tail]
    extra = _cycle_days(F(1) - done, order)
    return (
        f"In {n} days, {full} complete rounds plus {tail} extra days finish {fmt(done)}. The remaining "
        f"{fmt(F(1) - done)} is cleared in {fmt(extra)} further rotating days, so the total is {correct} days."
    )


twm_alternating_three = make_family(
    "twm_alternating_three",
    ["a", "b", "c", "n"],
    [
        (8, 12, 16, 5), (10, 15, 20, 4), (6, 9, 18, 3),
        (12, 18, 24, 7), (9, 12, 15, 6),
    ],
    _t_alternating_three, _ans_alternating_three, explain=_e_alternating_three,
)


def _t_negative_contributor(d):
    return (
        f"Arjun can finish a consignment in {fmt(d['a'])} days and Sneha in {fmt(d['b'])} days, while Vikram can "
        f"spoil an equivalent quantum of already completed work in {fmt(d['c'])} days. Arjun starts alone and "
        f"Vikram starts spoiling work from the very first day as well. After {fmt(d['till'])} days Sneha joins "
        f"Arjun, with Vikram continuing to undo work throughout. How many more days after Sneha joins will it "
        f"take to reach one fully completed consignment?"
    )


def _e_negative_contributor(d, correct):
    a, b, c, till = F(d["a"]), F(d["b"]), F(d["c"]), F(d["till"])
    net1 = _inv(a) - _inv(c)
    net2 = _inv(a) + _inv(b) - _inv(c)
    done = till * net1
    remaining = F(1) - done
    return (
        f"Net rate before Sneha joins = {fmt(net1)}/day, so {fmt(done)} is done; {fmt(remaining)} remains. "
        f"Net rate afterwards = {fmt(net2)}/day, giving {fmt(remaining / net2)} more days = {correct}."
    )


twm_negative_contributor = make_family(
    "twm_negative_contributor",
    ["a", "b", "c", "till"],
    [
        (12, 18, 36, 5), (10, 15, 30, 4), (15, 20, 60, 6),
        (8, 12, 24, 3), (18, 24, 72, 9),
    ],
    _t_negative_contributor, _ans_negative_contributor,
    explain=_e_negative_contributor, distract=lambda result, d: _near_half(result, d),
)


def _t_efficiency_change(d):
    change = int(d["change"])
    direction = "rises by" if change >= 0 else "falls by"
    return (
        f"Ananya alone needs {fmt(d['a'])} days and Dev alone needs {fmt(d['b'])} days for a data-entry drive. "
        f"They start together, but after {fmt(d['shift'])} days Ananya's efficiency {direction} "
        f"{abs(change)}% while Dev's speed is unchanged. Find the total time taken to finish the whole drive "
        f"under this changed arrangement."
    )


def _e_efficiency_change(d, correct):
    a, b, shift = F(d["a"]), F(d["b"]), F(d["shift"])
    factor = F(1) + F(d["change"]) / F(100)
    done = shift * (_inv(a) + _inv(b))
    remaining = F(1) - done
    new_rate = _inv(a) * factor + _inv(b)
    return (
        f"Initial combined rate {fmt(_inv(a) + _inv(b))}/day gives {fmt(done)} in {fmt(shift)} days. "
        f"Ananya's new rate is {fmt(_inv(a) * factor)}/day, so the new joint rate is {fmt(new_rate)}/day. "
        f"{fmt(remaining)} left takes {fmt(remaining / new_rate)} days; total = {correct} days."
    )


twm_efficiency_change = make_family(
    "twm_efficiency_change",
    ["a", "b", "change", "shift"],
    [
        (12, 18, 25, 3), (15, 25, -20, 4), (10, 20, 50, 2),
        (16, 24, -25, 5), (14, 21, 50, 4),
    ],
    _t_efficiency_change, _ans_efficiency_change, explain=_e_efficiency_change,
)


def _t_wage_contribution(d):
    return (
        f"Nikhil, Riya and Aditya would alone finish a landscaping job in {fmt(d['a'])}, {fmt(d['b'])} and "
        f"{fmt(d['c'])} days. Nikhil and Riya begin together; after {fmt(d['initial'])} days Aditya joins them "
        f"and all three work until the job is complete. The contractor distributes a total wage of "
        f"₹{fmt(d['total_wage'])} strictly in proportion to the work actually contributed by each person. "
        f"Find Nikhil's share of the wage."
    )


def _e_wage_contribution(d, correct):
    a, b, c = F(d["a"]), F(d["b"]), F(d["c"])
    initial, total = F(d["initial"]), F(d["total_wage"])
    done = initial * (_inv(a) + _inv(b))
    remaining = F(1) - done
    extra = remaining / (_inv(a) + _inv(b) + _inv(c))
    share = (initial + extra) / a
    return (
        f"After {fmt(initial)} days {fmt(done)} is done; {fmt(remaining)} takes {fmt(extra)} more days with all "
        f"three. Nikhil contributes {fmt(share)} of the work, so his wage = {money(total * share)} = {correct}."
    )


twm_wage_contribution = make_family(
    "twm_wage_contribution",
    ["a", "b", "c", "initial", "total_wage"],
    [
        (12, 18, 36, 6, 7200), (10, 15, 30, 5, 9000), (15, 20, 60, 8, 12000),
        (8, 12, 24, 3, 9600), (18, 27, 54, 9, 10800),
    ],
    _t_wage_contribution, lambda d: money(_ans_wage_contribution(d)),
    distract=_dist_wage_contribution, explain=_e_wage_contribution,
)


def _t_man_day_absentee(d):
    return (
        f"A contractor calculates that {fmt(d['men'])} workers can finish a boundary wall in {fmt(d['days'])} "
        f"days. For the first {fmt(d['extra_after'])} days, {fmt(d['absent'])} of them fail to report and the "
        f"remaining workers carry on; from the following day all {fmt(d['men'])} workers are present. "
        f"How many days in total does the wall actually take?"
    )


def _e_man_day_absentee(d, correct):
    men, days = F(d["men"]), F(d["days"])
    absent, early = F(d["absent"]), F(d["extra_after"])
    shortfall = absent * early
    return (
        f"Total job size = {fmt(men * days)} man-days. The early shortfall is {fmt(shortfall)} man-days, which "
        f"the full {fmt(men)}-worker crew recovers in {fmt(shortfall / men)} extra days. Total = {correct} days."
    )


twm_man_day_absentee = make_family(
    "twm_man_day_absentee",
    ["men", "days", "absent", "extra_after"],
    [
        (12, 20, 3, 8), (15, 24, 4, 9), (18, 30, 6, 10),
        (10, 16, 2, 6), (20, 25, 5, 12),
    ],
    _t_man_day_absentee, _ans_man_day_absentee, explain=_e_man_day_absentee,
)


# ---------------------------------------------------------------------------
# Families 7-12
# ---------------------------------------------------------------------------

def _t_fractional_join(d):
    return (
        f"Manav alone needs {fmt(d['a'])} days and Diya alone needs {fmt(d['b'])} days to finish a consignment. "
        f"Both begin together, but once {fmt(d['frac'])}% of the whole consignment has been completed Diya is "
        f"reassigned elsewhere and Manav finishes the balance alone. Find the total time taken for the "
        f"consignment."
    )


def _e_fractional_join(d, correct):
    a, b = F(d["a"]), F(d["b"])
    fraction = F(d["frac"]) / F(100)
    joint = _inv(a) + _inv(b)
    first = fraction / joint
    second = (F(1) - fraction) * a
    return (
        f"Joint rate = {fmt(joint)}/day, so {fmt(fraction)} of work takes {fmt(first)} days. The balance "
        f"{fmt(F(1) - fraction)} at Manav's rate needs {fmt(second)} days. Total = {correct} days."
    )


twm_fractional_join = make_family(
    "twm_fractional_join",
    ["a", "b", "frac"],
    [
        (12, 18, 40), (15, 25, 30), (10, 20, 50),
        (18, 27, 60), (8, 12, 25),
    ],
    _t_fractional_join, _ans_fractional_join,
    explain=_e_fractional_join, distract=_near_half,
)


def _t_machine_output(d):
    return (
        f"Two packing machines M and N can each handle an entire order alone in {fmt(d['a'])} and "
        f"{fmt(d['b'])} hours. At quality check, {fmt(d['waste'])}% of M's output and twice that percentage of "
        f"N's output are rejected as defective. Both machines run together from the start; how many hours do "
        f"they need to deliver one full order of accepted goods?"
    )


def _e_machine_output(d, correct):
    a, b = F(d["a"]), F(d["b"])
    waste = F(d["waste"]) / F(100)
    rate_m = _inv(a) * (F(1) - waste)
    rate_n = _inv(b) * (F(1) - 2 * waste)
    return (
        f"Accepted rate of M = {fmt(rate_m)}/hour and of N = {fmt(rate_n)}/hour. Combined accepted rate = "
        f"{fmt(rate_m + rate_n)}/hour, so one order needs {correct} hours."
    )


twm_machine_output = make_family(
    "twm_machine_output",
    ["a", "b", "waste"],
    [
        (10, 15, 10), (12, 18, 5), (8, 20, 8),
        (15, 25, 4), (9, 12, 12),
    ],
    _t_machine_output, _ans_machine_output,
    explain=_e_machine_output, distract=_near_half,
)


def _t_time_ratio_pair(d):
    return (
        f"Rehan and Sania together finish a job in {fmt(d['together'])} days, and the numbers of days they "
        f"would take alone are in the ratio {fmt(d['ra'])}:{fmt(d['rb'])} (Rehan:Sania). They work together "
        f"until exactly half of their joint completion time has elapsed; then Sania is called away and Rehan "
        f"finishes the remaining work alone. Find the total duration of the work."
    )


def _e_time_ratio_pair(d, correct):
    ra, rb, together = F(d["ra"]), F(d["rb"]), F(d["together"])
    scale = together * (ra + rb) / (ra * rb)
    solo_a = ra * scale
    return (
        f"Let solo times be {fmt(ra)}k and {fmt(rb)}k. Since joint time = {fmt(together)}, k = {fmt(scale)} and "
        f"Rehan's solo time = {fmt(solo_a)} days. Half the joint time completes half the work; the other half "
        f"takes Rehan {fmt(solo_a / F(2))} days. Total = {correct} days."
    )


twm_time_ratio_pair = make_family(
    "twm_time_ratio_pair",
    ["ra", "rb", "together"],
    [
        (2, 3, 6), (3, 4, 12), (4, 5, 20),
        (3, 5, 15), (5, 6, 30),
    ],
    _t_time_ratio_pair, _ans_time_ratio_pair, explain=_e_time_ratio_pair,
)


def _t_work_equivalence(d):
    return (
        f"On a repair job a crew has {fmt(d['m'])} men, {fmt(d['w'])} women and {fmt(d['b'])} boys. One man, "
        f"one woman and one boy would each need {fmt(d['pm'])}, {fmt(d['pw'])} and {fmt(d['pb'])} days "
        f"respectively to finish the whole job alone. They follow a daily rotation: all men work on day 1, all "
        f"women on day 2, all boys on day 3, and the same cycle repeats until completion. How many days does "
        f"the crew need?"
    )


def _e_work_equivalence(d, correct):
    rates = [F(d["m"]) / F(d["pm"]), F(d["w"]) / F(d["pw"]), F(d["b"]) / F(d["pb"])]
    cycle = sum(rates)
    full = int(F(1) / cycle)
    return (
        f"Daily rates of the three groups are {fmt(rates[0])}, {fmt(rates[1])} and {fmt(rates[2])}; one "
        f"three-day round contributes {fmt(cycle)}. After {full} rounds, {fmt(F(1) - full * cycle)} remains and "
        f"is finished within the next round. Total = {correct} days."
    )


twm_work_equivalence = make_family(
    "twm_work_equivalence",
    ["m", "w", "b", "pm", "pw", "pb"],
    [
        (2, 3, 4, 20, 30, 40), (3, 2, 5, 24, 30, 60), (4, 3, 2, 30, 45, 60),
        (1, 4, 6, 12, 40, 60), (5, 2, 3, 40, 25, 50),
    ],
    _t_work_equivalence, _ans_work_equivalence,
    explain=_e_work_equivalence, distract=_near_half,
)


def _t_three_team_rotation(d):
    return (
        f"Three specialist teams P, Q and R would need {fmt(d['a'])}, {fmt(d['b'])} and {fmt(d['c'])} days "
        f"respectively to complete a project alone. They adopt an expanding work pattern: on day 1 only P works, "
        f"on day 2 P and Q work together, on day 3 all three work together, and this three-day block is repeated "
        f"until the project ends. Find the total number of days needed."
    )


def _e_three_team_rotation(d, correct):
    a, b, c = F(d["a"]), F(d["b"]), F(d["c"])
    r1 = _inv(a)
    r2 = r1 + _inv(b)
    r3 = r2 + _inv(c)
    block = r1 + r2 + r3
    full = int(F(1) / block)
    extra = _cycle_days(F(1) - full * block, [r1, r2, r3])
    return (
        f"Work in one block = {fmt(r1)} + {fmt(r2)} + {fmt(r3)} = {fmt(block)}. After {full} complete blocks "
        f"{fmt(full * block)} is done and {fmt(extra)} days handle the residue. Total = {correct} days."
    )


twm_three_team_rotation = make_family(
    "twm_three_team_rotation",
    ["a", "b", "c"],
    [
        (12, 18, 24), (15, 20, 30), (10, 15, 30),
        (18, 27, 36), (8, 12, 16),
    ],
    _t_three_team_rotation, _ans_three_team_rotation,
    explain=_e_three_team_rotation,
)


def _t_piece_rate_drop(d):
    return (
        f"A newspaper agent is paid ₹{fmt(d['rate'])} for each of the first {fmt(d['after'])} copies delivered; "
        f"for every subsequent copy the per-copy rate is reduced by {fmt(d['drop'])}%. If the agent delivers "
        f"{fmt(d['pieces'])} copies in all, find the total payment due."
    )


def _e_piece_rate_drop(d, correct):
    rate = F(d["rate"])
    pieces, after = F(d["pieces"]), F(d["after"])
    drop = F(d["drop"]) / F(100)
    reduced = rate * (F(1) - drop)
    return (
        f"First {fmt(after)} copies earn {money(after * rate)}. The revised rate is {money(reduced)} per copy, "
        f"so the remaining {fmt(pieces - after)} copies earn {money((pieces - after) * reduced)}. "
        f"Total payment = {correct}."
    )


twm_piece_rate_drop = make_family(
    "twm_piece_rate_drop",
    ["rate", "pieces", "after", "drop"],
    [
        (50, 120, 50, 20), (80, 200, 80, 25), (90, 150, 60, 10),
        (100, 180, 100, 15), (75, 240, 90, 20),
    ],
    _t_piece_rate_drop, lambda d: money(_ans_piece_rate_drop(d)),
    distract=_dist_piece_rate_drop, explain=_e_piece_rate_drop,
)


# ---------------------------------------------------------------------------
# Families 13-18
# ---------------------------------------------------------------------------

def _t_double_half(d):
    return (
        f"Priya and Arjun alone need {fmt(d['a'])} and {fmt(d['b'])} days respectively for a digitisation task. "
        f"They work together for {fmt(d['shift'])} days; from then on Priya works twice as fast as before while "
        f"Arjun works at half his earlier speed. Find the total time required to finish the task."
    )


def _e_double_half(d, correct):
    a, b, shift = F(d["a"]), F(d["b"]), F(d["shift"])
    done = shift * (_inv(a) + _inv(b))
    new_rate = 2 * _inv(a) + _inv(b) / F(2)
    remaining = F(1) - done
    return (
        f"Initial rate {fmt(_inv(a) + _inv(b))}/day for {fmt(shift)} days finishes {fmt(done)}. New rate = "
        f"{fmt(new_rate)}/day; {fmt(remaining)} remains and takes {fmt(remaining / new_rate)} days. "
        f"Total = {correct} days."
    )


twm_double_half = make_family(
    "twm_double_half",
    ["a", "b", "shift"],
    [
        (12, 18, 3), (15, 20, 2), (10, 15, 2),
        (18, 24, 4), (8, 12, 2),
    ],
    _t_double_half, _ans_double_half,
    explain=_e_double_half, distract=_near_half,
)


def _t_deadline_extra(d):
    return (
        f"Sneha needs {fmt(d['a'])} days to finish a file alone and must submit it within {fmt(d['deadline'])} "
        f"days. She works alone until {fmt(d['extra_after'])} days before the deadline, at which point "
        f"{fmt(d['helpers'])} colleagues with exactly the same work rate join her. How many days before the "
        f"deadline is the file actually completed?"
    )


def _e_deadline_extra(d, correct):
    a, deadline = F(d["a"]), F(d["deadline"])
    early, helpers = F(d["extra_after"]), F(d["helpers"])
    alone = deadline - early
    actual = alone + (a - alone) / (helpers + F(1))
    return (
        f"She works alone for {fmt(alone)} days, leaving {fmt(a - alone)} solo-days of work. With "
        f"{fmt(helpers + F(1))} equally efficient workers this takes {fmt((a - alone) / (helpers + F(1)))} days, "
        f"so finishing time is {fmt(actual)} days. Margin before deadline = {correct} days."
    )


twm_deadline_extra = make_family(
    "twm_deadline_extra",
    ["a", "deadline", "extra_after", "helpers"],
    [
        (20, 12, 4, 3), (24, 15, 6, 2), (30, 18, 5, 4),
        (18, 11, 3, 4), (28, 16, 7, 3),
    ],
    _t_deadline_extra, _ans_deadline_extra,
    explain=_e_deadline_extra, distract=_near_half,
)


def _t_trainee_growth(d):
    return (
        f"Trainees Riya and Kabir, at their initial speeds, would need {fmt(d['a'])} and {fmt(d['b'])} days "
        f"respectively for a training module. At the end of every {fmt(d['step'])} days Riya's efficiency "
        f"improves by {fmt(d['growth'])}%, while Kabir's speed stays constant; both work together throughout. "
        f"After {fmt(d['n'])} days, what fraction of the module has been completed?"
    )


def _e_trainee_growth(d, correct):
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
    return (
        f"Riya's rate in successive {step}-day stages is multiplied by {fmt(factor)} each time. Summing each "
        f"stage's joint output with Kabir over {n} days gives completed work {fmt(work)} = {correct}."
    )


twm_trainee_growth = make_family(
    "twm_trainee_growth",
    ["a", "b", "growth", "n", "step"],
    [
        (20, 30, 25, 6, 2), (24, 36, 50, 6, 3), (15, 25, 20, 8, 4),
        (30, 40, 10, 9, 3), (18, 27, 25, 6, 2),
    ],
    _t_trainee_growth, _ans_trainee_growth,
    explain=_e_trainee_growth, distract=_near_fraction,
)


def _t_contract_penalty(d):
    return (
        f"Ananya and Sahil alone need {fmt(d['a'])} and {fmt(d['b'])} days for a contract carrying a "
        f"{fmt(d['deadline'])}-day deadline and a base fee of ₹{fmt(d['base'])}. The fee rises by "
        f"₹{fmt(d['bonus'])} for every day (including a fraction of a day) saved on the deadline, but falls by "
        f"₹{fmt(d['penalty'])} for every day of delay. They work together from day one. Find the final amount "
        f"paid to them."
    )


def _e_contract_penalty(d, correct):
    a, b, deadline = F(d["a"]), F(d["b"]), F(d["deadline"])
    base, bonus, penalty = F(d["base"]), F(d["bonus"]), F(d["penalty"])
    days = a * b / (a + b)
    margin = deadline - days
    adjustment = bonus * margin if margin >= 0 else -penalty * (-margin)
    return (
        f"Working together they take {fmt(days)} days against a {fmt(deadline)}-day deadline, giving a margin "
        f"of {fmt(margin)} days. The adjustment is {money(adjustment)}, so final payment = {correct}."
    )


twm_contract_penalty = make_family(
    "twm_contract_penalty",
    ["a", "b", "deadline", "base", "bonus", "penalty"],
    [
        (12, 18, 12, 10000, 500, 400), (20, 30, 9, 15000, 600, 600),
        (15, 10, 8, 9000, 750, 500), (24, 36, 16, 18000, 1000, 800),
        (18, 12, 6, 11000, 700, 1250),
    ],
    _t_contract_penalty, lambda d: money(_ans_contract_penalty(d)),
    distract=_dist_contract_penalty, explain=_e_contract_penalty,
)


def _t_partial_overlap(d):
    return (
        f"On an assembly task Diya and Manav would alone need {fmt(d['a'])} and {fmt(d['b'])} days. Diya works "
        f"alone for {fmt(d['x'])} days, then both work together for {fmt(d['y'])} days, and finally Manav works "
        f"alone for {fmt(d['z'])} days. What fraction of the whole task is still unfinished after these three "
        f"phases?"
    )


def _e_partial_overlap(d, correct):
    a, b, x, y, z = F(d["a"]), F(d["b"]), F(d["x"]), F(d["y"]), F(d["z"])
    first = x * _inv(a)
    middle = y * (_inv(a) + _inv(b))
    last = z * _inv(b)
    return (
        f"Contributions are {fmt(first)} + {fmt(middle)} + {fmt(last)} = {fmt(first + middle + last)}. "
        f"Hence unfinished work = {correct}."
    )


twm_partial_overlap = make_family(
    "twm_partial_overlap",
    ["a", "b", "x", "y", "z"],
    [
        (12, 18, 2, 3, 4), (15, 25, 3, 4, 2), (10, 20, 1, 2, 3),
        (18, 24, 4, 5, 3), (20, 30, 2, 6, 5),
    ],
    _t_partial_overlap, _ans_partial_overlap,
    explain=_e_partial_overlap, distract=_near_fraction,
)


def _t_absentee_cycle(d):
    return (
        f"Pooja, Rehan and Sania need {fmt(d['a'])}, {fmt(d['b'])} and {fmt(d['c'])} days alone for a survey. "
        f"They work under a rotating pair system for {fmt(d['n'])} days: day 1 Pooja and Rehan, day 2 Rehan and "
        f"Sania, day 3 Sania and Pooja, and then the same three-day pattern repeats. What fraction of the "
        f"survey is completed in these {fmt(d['n'])} days?"
    )


def _e_absentee_cycle(d, correct):
    a, b, c = F(d["a"]), F(d["b"]), F(d["c"])
    n = int(d["n"])
    pairs = [_inv(a) + _inv(b), _inv(b) + _inv(c), _inv(c) + _inv(a)]
    full, tail = divmod(n, 3)
    return (
        f"Day-rates of the pairs are {fmt(pairs[0])}, {fmt(pairs[1])} and {fmt(pairs[2])}. One full round "
        f"gives {fmt(sum(pairs))}; {full} rounds plus {tail} days give {correct} of the work."
    )


twm_absentee_cycle = make_family(
    "twm_absentee_cycle",
    ["a", "b", "c", "n"],
    [
        (12, 18, 24, 5), (15, 20, 30, 4), (10, 15, 30, 7),
        (18, 27, 36, 6), (8, 12, 24, 5),
    ],
    _t_absentee_cycle, _ans_absentee_cycle,
    explain=_e_absentee_cycle, distract=_near_fraction,
)


# ---------------------------------------------------------------------------
# Families 19-24
# ---------------------------------------------------------------------------

def _t_inverse_efficiency(d):
    return (
        f"Kavya is {fmt(d['eta'])}% more efficient than Nikhil. Working together they finish an assignment in "
        f"{fmt(d['together'])} days. Nikhil starts alone and works for {fmt(d['together'])} days before Kavya "
        f"joins him. How many more days after Kavya joins are needed to finish the assignment?"
    )


def _e_inverse_efficiency(d, correct):
    together = F(d["together"])
    factor = F(1) + F(d["eta"]) / F(100)
    slow_rate = F(1) / (together * (factor + F(1)))
    done = together * slow_rate
    return (
        f"If Nikhil's rate is r, Kavya's is {fmt(factor)}r and the joint rate is {fmt(factor + F(1))}r = "
        f"{fmt(F(1) / together)}/day, giving r = {fmt(slow_rate)}/day. In {fmt(together)} days Nikhil alone "
        f"finishes {fmt(done)}, so {fmt(F(1) - done)} remains; together they need {correct} more days."
    )


twm_inverse_efficiency = make_family(
    "twm_inverse_efficiency",
    ["together", "eta"],
    [
        (12, 50), (10, 25), (15, 100), (8, 60), (20, 80),
    ],
    _t_inverse_efficiency, _ans_inverse_efficiency,
    explain=_e_inverse_efficiency, distract=_near_half,
)


def _t_reverse_pair(d):
    lag = int(d["a"] - d["together"])
    return (
        f"Rohan and Kavya together complete a dataset in {fmt(d['together'])} days, while Rohan alone would "
        f"need {fmt(d['a'])} days. Kavya works alone for {lag} days and then Rohan joins her. How many more "
        f"days do the two of them need together to complete the dataset?"
    )


def _e_reverse_pair(d, correct):
    together, a = F(d["together"]), F(d["a"])
    lag = a - together
    b_rate = F(1) / together - _inv(a)
    done = lag * b_rate
    return (
        f"Kavya's rate = 1/{fmt(together)} - 1/{fmt(a)} = {fmt(b_rate)}/day. In {fmt(lag)} solo days she "
        f"finishes {fmt(done)}, leaving {fmt(F(1) - done)}; at the joint rate 1/{fmt(together)} this needs "
        f"{correct} more days."
    )


twm_reverse_pair = make_family(
    "twm_reverse_pair",
    ["together", "a"],
    [
        (6, 12), (8, 20), (10, 15), (12, 18), (9, 16),
    ],
    _t_reverse_pair, _ans_reverse_pair,
    explain=_e_reverse_pair, distract=_near_half,
)


def _t_wage_after_leave(d):
    return (
        f"Isha alone needs {fmt(d['a'])} days and Kunal alone needs {fmt(d['b'])} days for a job. They begin "
        f"together, but Isha leaves after {fmt(d['leave'])} days and Kunal finishes the balance alone. The "
        f"total wage for the job is ₹{fmt(d['total_wage'])}, shared in exact proportion to the work done by "
        f"each. Find Kunal's share."
    )


def _e_wage_after_leave(d, correct):
    a, b, leave = F(d["a"]), F(d["b"]), F(d["leave"])
    total = F(d["total_wage"])
    done = leave * (_inv(a) + _inv(b))
    share = leave / b + (F(1) - done)
    return (
        f"In {fmt(leave)} days they finish {fmt(done)}; Kunal alone completes the remaining "
        f"{fmt(F(1) - done)}. His total contribution is {fmt(share)}, so his wage is {correct}."
    )


twm_wage_after_leave = make_family(
    "twm_wage_after_leave",
    ["a", "b", "leave", "total_wage"],
    [
        (12, 18, 4, 9000), (15, 20, 5, 12000), (10, 15, 3, 10000),
        (18, 27, 6, 13500), (20, 30, 8, 15000),
    ],
    _t_wage_after_leave, lambda d: money(_ans_wage_after_leave(d)),
    distract=_dist_wage_after_leave, explain=_e_wage_after_leave,
)


def _t_parallel_groups(d):
    return (
        f"A project consists of two equal halves. The first half is assigned to {fmt(d['m'])} workers, each of "
        f"whom would need {fmt(d['a'])} days to finish that half alone; the second half goes to {fmt(d['n'])} "
        f"workers, each of whom would need {fmt(d['b'])} days for that half alone. Both groups start at once, "
        f"and any group that finishes its own half immediately moves to help with the other half. Find the "
        f"total time until both halves are complete."
    )


def _e_parallel_groups(d, correct):
    m, n, a, b = F(d["m"]), F(d["n"]), F(d["a"]), F(d["b"])
    first = a / (F(2) * m)
    second = b / (F(2) * n)
    joint = m / a + n / b
    if first <= second:
        remaining = F(1, 2) - first * n / b
        return (
            f"Group 1 finishes its half in {fmt(first)} days; group 2 has done {fmt(first * n / b)} of its "
            f"half, leaving {fmt(remaining)}. Combined rate {fmt(joint)}/day adds {fmt(remaining / joint)} days, "
            f"so total = {correct} days."
        )
    remaining = F(1, 2) - second * m / a
    return (
        f"Group 2 finishes its half in {fmt(second)} days; group 1 has done {fmt(second * m / a)} of its half, "
        f"leaving {fmt(remaining)}. Combined rate {fmt(joint)}/day adds {fmt(remaining / joint)} days, so "
        f"total = {correct} days."
    )


twm_parallel_groups = make_family(
    "twm_parallel_groups",
    ["m", "n", "a", "b"],
    [
        (2, 3, 12, 24), (3, 2, 24, 20), (2, 4, 20, 30),
        (5, 2, 30, 24), (4, 3, 20, 30),
    ],
    _t_parallel_groups, _ans_parallel_groups,
    explain=_e_parallel_groups, distract=_near_half,
)


def _t_multistage_bonus(d):
    return (
        f"Sneha, Vikram and Diya alone need {fmt(d['a'])}, {fmt(d['b'])} and {fmt(d['c'])} days for a campaign. "
        f"Sneha and Vikram start together and work for {fmt(d['after'])} days, after which Diya joins them "
        f"until the campaign ends. The team earns a bonus of ₹{fmt(d['bonus'])} for each day by which the "
        f"actual completion beats Sneha's solo time of {fmt(d['a'])} days. Find the bonus earned."
    )


def _e_multistage_bonus(d, correct):
    a, b, c, after = F(d["a"]), F(d["b"]), F(d["c"]), F(d["after"])
    bonus = F(d["bonus"])
    done = after * (_inv(a) + _inv(b))
    remaining = F(1) - done
    total = after + remaining / (_inv(a) + _inv(b) + _inv(c))
    saved = a - total
    return (
        f"After {fmt(after)} days {fmt(done)} is done; all three clear {fmt(remaining)} in "
        f"{fmt(remaining / (_inv(a) + _inv(b) + _inv(c)))} days, so total time = {fmt(total)} days. Days saved "
        f"= {fmt(saved)}, giving bonus {correct}."
    )


twm_multistage_bonus = make_family(
    "twm_multistage_bonus",
    ["a", "b", "c", "after", "bonus"],
    [
        (12, 18, 24, 3, 1300), (15, 20, 30, 4, 900), (10, 15, 30, 2, 450),
        (18, 27, 36, 5, 520), (20, 30, 60, 6, 800),
    ],
    _t_multistage_bonus, lambda d: money(_ans_multistage_bonus(d)),
    distract=_dist_multistage_bonus, explain=_e_multistage_bonus,
)


def _t_capacity_reallocation(d):
    return (
        f"Neha, Kabir and Arjun would need {fmt(d['a'])}, {fmt(d['b'])} and {fmt(d['c'])} days alone for a "
        f"consignment. Neha and Kabir start together; after {fmt(d['move_day'])} days Neha is transferred to "
        f"another site and Arjun joins Kabir for the balance. Find the ratio of the total number of days "
        f"Kabir works to the total number of days Arjun works."
    )


def _e_capacity_reallocation(d, correct):
    a, b, c, move = F(d["a"]), F(d["b"]), F(d["c"]), F(d["move_day"])
    done = move * (_inv(a) + _inv(b))
    extra = (F(1) - done) / (_inv(b) + _inv(c))
    return (
        f"First {fmt(move)} days at rate {fmt(_inv(a) + _inv(b))} finish {fmt(done)}; the remaining "
        f"{fmt(F(1) - done)} takes {fmt(extra)} days at rate {fmt(_inv(b) + _inv(c))}. Kabir works "
        f"{fmt(move + extra)} days and Arjun {fmt(extra)} days, giving {correct}."
    )


twm_capacity_reallocation = make_family(
    "twm_capacity_reallocation",
    ["a", "b", "c", "move_day"],
    [
        (12, 18, 24, 4), (15, 20, 30, 5), (10, 15, 25, 3),
        (16, 24, 36, 6), (14, 21, 28, 4),
    ],
    _t_capacity_reallocation, _ans_capacity_reallocation,
    distract=_dist_capacity_reallocation, explain=_e_capacity_reallocation,
)


# ---------------------------------------------------------------------------
# Family registry
# ---------------------------------------------------------------------------

FAMILIES = [
    twm_stage_exit_join,
    twm_alternating_three,
    twm_negative_contributor,
    twm_efficiency_change,
    twm_wage_contribution,
    twm_man_day_absentee,
    twm_fractional_join,
    twm_machine_output,
    twm_time_ratio_pair,
    twm_work_equivalence,
    twm_three_team_rotation,
    twm_piece_rate_drop,
    twm_double_half,
    twm_deadline_extra,
    twm_trainee_growth,
    twm_contract_penalty,
    twm_partial_overlap,
    twm_absentee_cycle,
    twm_inverse_efficiency,
    twm_reverse_pair,
    twm_wage_after_leave,
    twm_parallel_groups,
    twm_multistage_bonus,
    twm_capacity_reallocation,
]


def build_time_and_work_mains():
    return build_specs(FAMILIES, mains=True)
