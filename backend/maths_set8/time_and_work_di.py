# -*- coding: utf-8 -*-
"""Time and Work — Data Interpretation (Prelims) — 120 self-contained questions."""

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
    ratio,
    ratio_distractors,
)

SOURCE_PDF = "ce788d06-e730-4963-97ca-208b2af36699 (2).pdf"
PAGES = {
    1: f"{SOURCE_PDF}, pp. 4-5",
    2: f"{SOURCE_PDF}, pp. 6-7",
    3: f"{SOURCE_PDF}, pp. 8-9",
    4: f"{SOURCE_PDF}, pp. 10-11",
}


# ---------------------------------------------------------------------------
# Shared formatting / distractor helpers
# ---------------------------------------------------------------------------


def _money(value):
    return money(F(value))


def _pct(value):
    return pct(F(value))


def _num_distract(step=1):
    return lambda result, _inputs: near_num(result, step)


def _money_distract(step=50):
    return lambda result, _inputs: near_money(Fraction(str(result).lstrip("₹")), step)


def _pct_distract(step=5):
    return lambda result, _inputs: near_pct(Fraction(str(result).rstrip("%")), step)


def _ratio_distract(result, _inputs):
    return ratio_distractors(result)


def _by_ask(mapping):
    return lambda result, inputs: mapping[inputs["ask"]](result, inputs)


def _question(rows, ask_text):
    return f"{data(rows)} {ask_text}"


# ---------------------------------------------------------------------------
# 01. twd_solo_days
# ---------------------------------------------------------------------------

_SOLO_ASKS = (
    "How many days does A take to finish the work alone?",
    "How many days does B take to finish the work alone?",
    "How many days do A and B take to finish the work together?",
    "How many days are saved compared with A working alone when both work together?",
)


def _solo_answer(inputs):
    a, b = inputs["a"], inputs["b"]
    together = F(a * b, a + b)
    return (a, b, together, a - together)[inputs["ask"]]


def _solo_explain(inputs, correct):
    a, b = inputs["a"], inputs["b"]
    together = F(a * b, a + b)
    return (
        f"Combined rate = 1/{a} + 1/{b}, so together they need {fmt(together)} "
        f"days. The requested value is {correct}."
    )


twd_solo_days = make_family(
    "twd_solo_days",
    ("a", "b", "ask"),
    ((12, 24, 2), (15, 30, 0), (18, 9, 2), (20, 30, 3), (24, 16, 1)),
    lambda d: (
        f"{data([('A alone (days)', d['a']), ('B alone (days)', d['b'])])} "
        f"{_SOLO_ASKS[d['ask']]}"
    ),
    _solo_answer,
    _num_distract(1),
    _solo_explain,
)


# ---------------------------------------------------------------------------
# 02. twd_daily_rate
# ---------------------------------------------------------------------------

_DAILY_ASKS = (
    "Find A's total wage for the full period.",
    "Find B's total wage for the full period.",
    "Find their combined daily wage.",
    "Find their combined wage for the full period.",
)


def _daily_answer(inputs):
    a, b, n = inputs["a"], inputs["b"], inputs["n"]
    return _money((a * n, b * n, a + b, (a + b) * n)[inputs["ask"]])


def _daily_explain(inputs, correct):
    a, b, n = inputs["a"], inputs["b"], inputs["n"]
    return (
        f"A earns {a}*{n} = {a * n}; B earns {b}*{n} = {b * n}; together "
        f"their daily wage is {a + b} and their {n}-day wage is {(a + b) * n}. "
        f"The requested value is {correct}."
    )


twd_daily_rate = make_family(
    "twd_daily_rate",
    ("a", "b", "n", "ask"),
    ((450, 350, 6, 0), (500, 400, 8, 1), (600, 450, 5, 2),
     (720, 480, 10, 3), (800, 550, 12, 0)),
    lambda d: _question(
        [("A daily wage (Rs)", d["a"]), ("B daily wage (Rs)", d["b"]),
         ("days worked", d["n"])],
        _DAILY_ASKS[d["ask"]],
    ),
    _daily_answer,
    _money_distract(50),
    _daily_explain,
)


# ---------------------------------------------------------------------------
# 03. twd_work_done
# ---------------------------------------------------------------------------

_WORK_ASKS = (
    "How many units did A produce?",
    "How many units did B produce?",
    "How many units did they produce in total?",
    "How many more units did A produce than B?",
)


def _work_answer(inputs):
    a, b, da, db = inputs["a"], inputs["b"], inputs["da"], inputs["db"]
    return F((a * da, b * db, a * da + b * db, abs(a * da - b * db))[inputs["ask"]])


def _work_explain(inputs, correct):
    a, b, da, db = inputs["a"], inputs["b"], inputs["da"], inputs["db"]
    return (
        f"A: {a}*{da} = {a * da} units; B: {b}*{db} = {b * db} units; "
        f"combined = {a * da + b * db} units. The requested value is {correct}."
    )


twd_work_done = make_family(
    "twd_work_done",
    ("a", "b", "da", "db", "ask"),
    ((12, 15, 6, 4, 2), (14, 11, 5, 7, 3), (18, 12, 8, 6, 0),
     (20, 16, 4, 5, 1), (25, 20, 6, 3, 2)),
    lambda d: _question(
        [("A rate (units/day)", d["a"]), ("B rate (units/day)", d["b"]),
         ("A days", d["da"]), ("B days", d["db"])],
        _WORK_ASKS[d["ask"]],
    ),
    _work_answer,
    _num_distract(2),
    _work_explain,
)


# ---------------------------------------------------------------------------
# 04. twd_wage_ratio
# ---------------------------------------------------------------------------

_WAGE_RATIO_ASKS = (
    "Find the ratio of A's wage to B's wage.",
    "Find A's wage.",
    "Find B's wage.",
    "Find the difference between A's wage and B's wage.",
)


def _wage_ratio_shares(inputs):
    a, b, total = inputs["a"], inputs["b"], inputs["total_wage"]
    return F(total * b, a + b), F(total * a, a + b)


def _wage_ratio_answer(inputs):
    share_a, share_b = _wage_ratio_shares(inputs)
    if inputs["ask"] == 0:
        return ratio(share_a, share_b)
    if inputs["ask"] == 1:
        return _money(share_a)
    if inputs["ask"] == 2:
        return _money(share_b)
    return _money(abs(share_a - share_b))


def _wage_ratio_distract(result, inputs):
    if inputs["ask"] == 0:
        return _ratio_distract(result, inputs)
    return _money_distract(100)(result, inputs)


def _wage_ratio_explain(inputs, correct):
    a, b = inputs["a"], inputs["b"]
    share_a, share_b = _wage_ratio_shares(inputs)
    return (
        f"Wages are shared in the inverse ratio of days: {b}:{a}. Hence A gets "
        f"{fmt(share_a)} and B gets {fmt(share_b)}. The requested value is {correct}."
    )


twd_wage_ratio = make_family(
    "twd_wage_ratio",
    ("a", "b", "total_wage", "ask"),
    ((12, 18, 1500, 0), (15, 10, 2000, 1), (20, 30, 2500, 2),
     (8, 12, 1800, 3), (24, 16, 2400, 0)),
    lambda d: _question(
        [("A alone (days)", d["a"]), ("B alone (days)", d["b"]),
         ("total wage (Rs)", d["total_wage"])],
        _WAGE_RATIO_ASKS[d["ask"]],
    ),
    _wage_ratio_answer,
    _wage_ratio_distract,
    _wage_ratio_explain,
)


# ---------------------------------------------------------------------------
# 05. twd_efficiency_share
# ---------------------------------------------------------------------------

_EFF_SHARE_ASKS = (
    "Find A's share of the work in units.",
    "Find B's share of the work in units.",
    "Find C's share of the work in units.",
    "Find A's percentage share of the total efficiency.",
)


def _eff_share_answer(inputs):
    ea, eb, ec, total = inputs["ea"], inputs["eb"], inputs["ec"], inputs["total_work"]
    strength = ea + eb + ec
    if inputs["ask"] == 3:
        return _pct(F(100 * ea, strength))
    return F(total * (ea, eb, ec)[inputs["ask"]], strength)


def _eff_share_distract(result, inputs):
    if inputs["ask"] == 3:
        return _pct_distract(5)(result, inputs)
    return _num_distract(2)(result, inputs)


def _eff_share_explain(inputs, correct):
    ea, eb, ec, total = inputs["ea"], inputs["eb"], inputs["ec"], inputs["total_work"]
    strength = ea + eb + ec
    return (
        f"Efficiency total = {ea}+{eb}+{ec} = {strength}; work is split in "
        f"that ratio. A's percent = 100*{ea}/{strength}. Requested value: {correct}."
    )


twd_efficiency_share = make_family(
    "twd_efficiency_share",
    ("ea", "eb", "ec", "total_work", "ask"),
    ((4, 3, 5, 240, 0), (6, 4, 2, 360, 1), (5, 5, 6, 320, 2),
     (3, 7, 4, 280, 3), (8, 6, 6, 400, 3)),
    lambda d: _question(
        [("A efficiency (units/day)", d["ea"]),
         ("B efficiency (units/day)", d["eb"]),
         ("C efficiency (units/day)", d["ec"]),
         ("total work (units)", d["total_work"])],
        _EFF_SHARE_ASKS[d["ask"]],
    ),
    _eff_share_answer,
    _eff_share_distract,
    _eff_share_explain,
)


# ---------------------------------------------------------------------------
# 06. twd_man_days
# ---------------------------------------------------------------------------

_MAN_DAYS_ASKS = (
    "Find the planned number of man-days.",
    "Find the actual number of man-days after absences.",
    "Find the worker-days lost to absence.",
    "How many full-strength days are needed to match the actual work done?",
)


def _man_days_answer(inputs):
    men, days, absent = inputs["men"], inputs["days"], inputs["absent"]
    planned = men * days
    actual = planned - absent
    return F((planned, actual, absent, F(actual, men))[inputs["ask"]])


def _man_days_explain(inputs, correct):
    men, days, absent = inputs["men"], inputs["days"], inputs["absent"]
    planned = men * days
    actual = planned - absent
    return (
        f"Planned man-days = {men}*{days} = {planned}; after {absent} lost "
        f"worker-days, actual = {actual}. At full strength that is "
        f"{fmt(F(actual, men))} days. Requested value: {correct}."
    )


twd_man_days = make_family(
    "twd_man_days",
    ("men", "days", "absent", "ask"),
    ((12, 20, 15, 1), (10, 18, 12, 0), (15, 16, 20, 2),
     (8, 25, 10, 3), (20, 12, 18, 1)),
    lambda d: _question(
        [("workers", d["men"]), ("planned days", d["days"]),
         ("worker-days absent", d["absent"])],
        _MAN_DAYS_ASKS[d["ask"]],
    ),
    _man_days_answer,
    _num_distract(1),
    _man_days_explain,
)


# ---------------------------------------------------------------------------
# 07. twd_missing_days
# ---------------------------------------------------------------------------

_MISSING_ASKS = (
    "How many days are needed to finish the work?",
    "How many days are needed for half of the work?",
    "How many days are needed for twice the work?",
    "How many days is that beyond a 5-day schedule?",
)


def _missing_answer(inputs):
    work, per_day = inputs["work"], inputs["per_day"]
    days = F(work, per_day)
    return (days, F(work, 2 * per_day), F(2 * work, per_day), days - 5)[inputs["ask"]]


def _missing_explain(inputs, correct):
    work, per_day = inputs["work"], inputs["per_day"]
    return (
        f"Days = work/rate = {work}/{per_day} = {fmt(F(work, per_day))}. "
        f"The requested value is {correct}."
    )


twd_missing_days = make_family(
    "twd_missing_days",
    ("work", "per_day", "ask"),
    ((240, 20, 0), (360, 24, 1), (180, 15, 2), (300, 25, 3), (420, 30, 0)),
    lambda d: _question(
        [("total work (units)", d["work"]),
         ("output per day (units)", d["per_day"])],
        _MISSING_ASKS[d["ask"]],
    ),
    _missing_answer,
    _num_distract(1),
    _missing_explain,
)


# ---------------------------------------------------------------------------
# 08. twd_combined_rate
# ---------------------------------------------------------------------------

_COMBINED_ASKS = (
    "Find their combined output per day.",
    "Find their combined output in 4 days.",
    "How many days are needed for 120 units at the combined rate?",
    "How many more units does A make than B in 4 days?",
)


def _combined_answer(inputs):
    a, b = inputs["a"], inputs["b"]
    rate = F(a + b)
    return (rate, 4 * rate, F(120, a + b), 4 * abs(a - b))[inputs["ask"]]


def _combined_explain(inputs, correct):
    a, b = inputs["a"], inputs["b"]
    return (
        f"Combined daily output = {a}+{b} = {a + b} units; 4 days give "
        f"{4 * (a + b)} units and 120 units need {fmt(F(120, a + b))} days. "
        f"The requested value is {correct}."
    )


twd_combined_rate = make_family(
    "twd_combined_rate",
    ("a", "b", "ask"),
    ((18, 12, 0), (20, 15, 2), (24, 16, 1), (30, 20, 3), (14, 10, 0)),
    lambda d: _question(
        [("A rate (units/day)", d["a"]), ("B rate (units/day)", d["b"])],
        _COMBINED_ASKS[d["ask"]],
    ),
    _combined_answer,
    _num_distract(2),
    _combined_explain,
)


# ---------------------------------------------------------------------------
# 09. twd_two_day_cycle
# ---------------------------------------------------------------------------

_CYCLE_ASKS = (
    "How many units are produced over the whole period?",
    "How many units does A produce?",
    "How many units does B produce?",
    "What is the average daily output over the period?",
)


def _cycle_answer(inputs):
    a, b, n = inputs["a"], inputs["b"], inputs["n"]
    full, extra = divmod(n, 2)
    total = full * (a + b) + (a if extra else 0)
    a_units = (full + extra) * a
    b_units = full * b
    return F((total, a_units, b_units, F(total, n))[inputs["ask"]])


def _cycle_explain(inputs, correct):
    a, b, n = inputs["a"], inputs["b"], inputs["n"]
    full, extra = divmod(n, 2)
    total = full * (a + b) + (a if extra else 0)
    return (
        f"There are {full} complete two-day cycles plus {extra} extra A day, "
        f"giving {total} units in {n} days. The requested value is {correct}."
    )


twd_two_day_cycle = make_family(
    "twd_two_day_cycle",
    ("a", "b", "n", "ask"),
    ((18, 12, 7, 0), (20, 15, 8, 1), (24, 16, 5, 2),
     (30, 25, 9, 3), (16, 14, 6, 0)),
    lambda d: _question(
        [("A output (units/day)", d["a"]), ("B output (units/day)", d["b"]),
         ("days in cycle", d["n"])],
        f"A works first and they alternate daily. {_CYCLE_ASKS[d['ask']]}",
    ),
    _cycle_answer,
    _num_distract(2),
    _cycle_explain,
)


# ---------------------------------------------------------------------------
# 10. twd_remaining_work
# ---------------------------------------------------------------------------

_REMAINING_ASKS = (
    "What fraction of the work has been completed?",
    "What fraction of the work remains?",
    "How many more days do they need together to finish?",
    "How many days are saved versus A doing the entire job alone?",
)


def _remaining_parts(inputs):
    a, b, days = inputs["a"], inputs["b"], inputs["days"]
    together = F(a * b, a + b)
    done = F(a + b, a * b) * days
    left = 1 - done
    return together, done, left, left * together, a - (days + left * together)


def _remaining_answer(inputs):
    together, done, left, rest_days, saved = _remaining_parts(inputs)
    return (done, left, rest_days, saved)[inputs["ask"]]


def _remaining_distract(result, inputs):
    step = F(1, 12) if inputs["ask"] in (0, 1) else 1
    return _num_distract(step)(result, inputs)


def _remaining_explain(inputs, correct):
    together, done, left, rest_days, _saved = _remaining_parts(inputs)
    return (
        f"Together they finish in {fmt(together)} days; after the stated days, "
        f"{fmt(done)} is done and {fmt(left)} is left, needing {fmt(rest_days)} "
        f"more days. The requested value is {correct}."
    )


twd_remaining_work = make_family(
    "twd_remaining_work",
    ("a", "b", "days", "ask"),
    ((20, 30, 5, 0), (18, 9, 4, 1), (24, 12, 3, 2),
     (30, 20, 7, 3), (15, 10, 2, 1)),
    lambda d: _question(
        [("A alone (days)", d["a"]), ("B alone (days)", d["b"]),
         ("days already worked together", d["days"])],
        _REMAINING_ASKS[d["ask"]],
    ),
    _remaining_answer,
    _remaining_distract,
    _remaining_explain,
)


# ---------------------------------------------------------------------------
# 11. twd_average_days
# ---------------------------------------------------------------------------

_AVERAGE_ASKS = (
    "Find the average of the three solo completion times.",
    "How many days do all three take working together?",
    "Find the range of the three solo completion times.",
    "Find the average of A's and B's solo completion times.",
)


def _average_answer(inputs):
    a, b, c = inputs["a"], inputs["b"], inputs["c"]
    together = F(1, F(1, a) + F(1, b) + F(1, c))
    return (F(a + b + c, 3), together, max(a, b, c) - min(a, b, c), F(a + b, 2))[
        inputs["ask"]
    ]


def _average_explain(inputs, correct):
    a, b, c = inputs["a"], inputs["b"], inputs["c"]
    return (
        f"Solo times are {a}, {b} and {c}; their average is "
        f"{fmt(F(a + b + c, 3))} and combined rate gives "
        f"{fmt(F(1, F(1, a) + F(1, b) + F(1, c)))} days. Requested value: {correct}."
    )


twd_average_days = make_family(
    "twd_average_days",
    ("a", "b", "c", "ask"),
    ((12, 18, 24, 1), (15, 20, 30, 0), (10, 15, 30, 2),
     (16, 24, 48, 3), (20, 30, 60, 1)),
    lambda d: _question(
        [("A alone (days)", d["a"]), ("B alone (days)", d["b"]),
         ("C alone (days)", d["c"])],
        _AVERAGE_ASKS[d["ask"]],
    ),
    _average_answer,
    _num_distract(1),
    _average_explain,
)


# ---------------------------------------------------------------------------
# 12. twd_ratio_fraction
# ---------------------------------------------------------------------------

_RATIO_FRACTION_ASKS = (
    "Find the efficiency ratio A:B.",
    "Find A's fraction of the combined work rate.",
    "Find B's fraction of the combined work rate.",
    "Find the ratio of A's solo days to B's solo days.",
)


def _ratio_fraction_answer(inputs):
    a, b = inputs["a"], inputs["b"]
    if inputs["ask"] == 0:
        return ratio(b, a)
    if inputs["ask"] == 1:
        return F(b, a + b)
    if inputs["ask"] == 2:
        return F(a, a + b)
    return ratio(a, b)


def _ratio_fraction_distract(result, inputs):
    if inputs["ask"] in (0, 3):
        return _ratio_distract(result, inputs)
    return _num_distract(F(1, 5))(result, inputs)


def _ratio_fraction_explain(inputs, correct):
    a, b = inputs["a"], inputs["b"]
    return (
        f"Efficiency is inverse of days, so A:B = {b}:{a} = {ratio(b, a)}; "
        f"the rate fractions are {fmt(F(b, a + b))} and {fmt(F(a, a + b))}. "
        f"Requested value: {correct}."
    )


twd_ratio_fraction = make_family(
    "twd_ratio_fraction",
    ("a", "b", "ask"),
    ((12, 18, 0), (15, 20, 1), (24, 16, 2), (10, 15, 3), (18, 12, 1)),
    lambda d: (
        f"{data([('A alone (days)', d['a']), ('B alone (days)', d['b'])])} "
        f"{_RATIO_FRACTION_ASKS[d['ask']]}"
    ),
    _ratio_fraction_answer,
    _ratio_fraction_distract,
    _ratio_fraction_explain,
)


# ---------------------------------------------------------------------------
# 13. twd_piece_count
# ---------------------------------------------------------------------------

_PIECE_ASKS = (
    "How many pieces are produced?",
    "How many pieces are produced in 2 days?",
    "How many days are needed for 100 pieces?",
    "Find the total pay at the stated bonus per piece.",
)


def _piece_answer(inputs):
    rate, days, bonus = inputs["rate"], inputs["days"], inputs["bonus"]
    pieces = rate * days
    if inputs["ask"] == 3:
        return _money(F(pieces * bonus))
    return F((pieces, 2 * rate, F(100, rate))[inputs["ask"]])


def _piece_distract(result, inputs):
    if inputs["ask"] == 3:
        return _money_distract(100)(result, inputs)
    return _num_distract(2)(result, inputs)


def _piece_explain(inputs, correct):
    rate, days, bonus = inputs["rate"], inputs["days"], inputs["bonus"]
    return (
        f"Pieces = {rate}*{days} = {rate * days}; pay = {rate * days}*{bonus} "
        f"= {rate * days * bonus}. The requested value is {correct}."
    )


twd_piece_count = make_family(
    "twd_piece_count",
    ("rate", "days", "bonus", "ask"),
    ((25, 8, 20, 0), (30, 6, 25, 1), (20, 10, 30, 2),
     (40, 5, 18, 3), (24, 9, 22, 3)),
    lambda d: _question(
        [("output rate (pieces/day)", d["rate"]), ("days worked", d["days"]),
         ("bonus (Rs/piece)", d["bonus"])],
        _PIECE_ASKS[d["ask"]],
    ),
    _piece_answer,
    _piece_distract,
    _piece_explain,
)


# ---------------------------------------------------------------------------
# 14. twd_absentee_lookup
# ---------------------------------------------------------------------------

_ABS_LABELS = ("A", "B", "C")
_ABSENTEE_ASKS = (
    "How many units were produced on the day with the absence?",
    "How many units are produced on a full day with all three present?",
    "How many units were lost because of the absence?",
    "How many units were produced over one absent day and one full day?",
)


def _absentee_answer(inputs):
    a, b, c, idx = inputs["a"], inputs["b"], inputs["c"], inputs["absent_day"]
    outputs = (a, b, c)
    full = a + b + c
    reduced = full - outputs[idx]
    return F((reduced, full, outputs[idx], reduced + full)[inputs["ask"]])


def _absentee_explain(inputs, correct):
    a, b, c, idx = inputs["a"], inputs["b"], inputs["c"], inputs["absent_day"]
    outputs = (a, b, c)
    full = a + b + c
    reduced = full - outputs[idx]
    return (
        f"Full-day output is {a}+{b}+{c} = {full}; with {_ABS_LABELS[idx]} absent "
        f"it is {full}-{outputs[idx]} = {reduced}. Requested value: {correct}."
    )


twd_absentee_lookup = make_family(
    "twd_absentee_lookup",
    ("a", "b", "c", "absent_day", "ask"),
    ((18, 15, 12, 1, 0), (20, 16, 14, 0, 2), (22, 18, 10, 2, 1),
     (25, 20, 15, 1, 3), (30, 24, 18, 0, 0)),
    lambda d: _question(
        [("A output (units/day)", d["a"]), ("B output (units/day)", d["b"]),
         ("C output (units/day)", d["c"]),
         ("worker absent", _ABS_LABELS[d["absent_day"]])],
        _ABSENTEE_ASKS[d["ask"]],
    ),
    _absentee_answer,
    _num_distract(2),
    _absentee_explain,
)


# ---------------------------------------------------------------------------
# 15. twd_wage_per_worker
# ---------------------------------------------------------------------------

_WAGE_WORKER_ASKS = (
    "Find A's wage.",
    "Find B's wage.",
    "Find the difference between their wages.",
    "Find A's daily wage rate.",
)


def _wage_worker_answer(inputs):
    a, b, total = inputs["a"], inputs["b"], inputs["total_wage"]
    wa, wb = F(total * a, a + b), F(total * b, a + b)
    return _money((wa, wb, abs(wa - wb), F(wa, a))[inputs["ask"]])


def _wage_worker_explain(inputs, correct):
    a, b, total = inputs["a"], inputs["b"], inputs["total_wage"]
    wa, wb = F(total * a, a + b), F(total * b, a + b)
    return (
        f"Wages follow days worked: A = {fmt(wa)}, B = {fmt(wb)}; A's rate is "
        f"{fmt(F(wa, a))} per day. The requested value is {correct}."
    )


twd_wage_per_worker = make_family(
    "twd_wage_per_worker",
    ("a", "b", "total_wage", "ask"),
    ((6, 4, 1200, 0), (8, 5, 1560, 1), (7, 3, 1400, 2),
     (9, 6, 1800, 3), (5, 10, 1500, 0)),
    lambda d: _question(
        [("A days worked", d["a"]), ("B days worked", d["b"]),
         ("total wage (Rs)", d["total_wage"])],
        _WAGE_WORKER_ASKS[d["ask"]],
    ),
    _wage_worker_answer,
    _money_distract(50),
    _wage_worker_explain,
)


# ---------------------------------------------------------------------------
# 16. twd_efficiency_ratio
# ---------------------------------------------------------------------------

_EFFICIENCY_RATIO_ASKS = (
    "Find the efficiency ratio A:B.",
    "Find A's percentage share of the combined efficiency.",
    "Find B's percentage share of the combined efficiency.",
    "Find the ratio of A's solo days to B's solo days.",
)


def _efficiency_ratio_answer(inputs):
    a, b = inputs["a"], inputs["b"]
    if inputs["ask"] == 0:
        return ratio(b, a)
    if inputs["ask"] == 1:
        return _pct(F(100 * b, a + b))
    if inputs["ask"] == 2:
        return _pct(F(100 * a, a + b))
    return ratio(a, b)


def _efficiency_ratio_distract(result, inputs):
    if inputs["ask"] in (0, 3):
        return _ratio_distract(result, inputs)
    return _pct_distract(5)(result, inputs)


def _efficiency_ratio_explain(inputs, correct):
    a, b = inputs["a"], inputs["b"]
    return (
        f"Efficiency ratio A:B = 1/{a}:1/{b} = {b}:{a} = {ratio(b, a)}; "
        f"percentage shares are {fmt(pct(F(100 * b, a + b)))} and "
        f"{fmt(pct(F(100 * a, a + b)))}. Requested value: {correct}."
    )


twd_efficiency_ratio = make_family(
    "twd_efficiency_ratio",
    ("a", "b", "ask"),
    ((15, 20, 0), (12, 18, 1), (24, 16, 2), (10, 15, 3), (18, 12, 1)),
    lambda d: (
        f"{data([('Worker A (days alone)', d['a']), ('Worker B (days alone)', d['b'])])} "
        f"{_EFFICIENCY_RATIO_ASKS[d['ask']]}"
    ),
    _efficiency_ratio_answer,
    _efficiency_ratio_distract,
    _efficiency_ratio_explain,
)


# ---------------------------------------------------------------------------
# 17. twd_time_saved
# ---------------------------------------------------------------------------

_TIME_SAVED_ASKS = (
    "How many days do they need working together?",
    "How many days are saved compared with the deadline?",
    "How many days are saved compared with A alone?",
    "How many days are saved compared with B alone?",
)


def _time_saved_answer(inputs):
    a, b, deadline = inputs["a"], inputs["b"], inputs["deadline"]
    together = F(a * b, a + b)
    return F((together, deadline - together, a - together, b - together)[inputs["ask"]])


def _time_saved_explain(inputs, correct):
    a, b, deadline = inputs["a"], inputs["b"], inputs["deadline"]
    together = F(a * b, a + b)
    return (
        f"Together they need {fmt(together)} days against a {deadline}-day "
        f"deadline, {a} days for A alone and {b} days for B alone. "
        f"The requested value is {correct}."
    )


twd_time_saved = make_family(
    "twd_time_saved",
    ("a", "b", "deadline", "ask"),
    ((20, 30, 15, 1), (18, 9, 10, 0), (24, 12, 9, 2),
     (30, 20, 14, 3), (15, 10, 8, 1)),
    lambda d: _question(
        [("A alone (days)", d["a"]), ("B alone (days)", d["b"]),
         ("deadline (days)", d["deadline"])],
        _TIME_SAVED_ASKS[d["ask"]],
    ),
    _time_saved_answer,
    _num_distract(1),
    _time_saved_explain,
)


# ---------------------------------------------------------------------------
# 18. twd_partial_work
# ---------------------------------------------------------------------------

_PARTIAL_ASKS = (
    "What fraction of the work did A complete alone?",
    "What fraction of the work is left?",
    "How many days do A and B need together to finish the rest?",
    "What is the total duration including A's solo work?",
)


def _partial_parts(inputs):
    a, b, x = inputs["a"], inputs["b"], inputs["x"]
    done = F(x, a)
    left = 1 - done
    rest_days = left * F(a * b, a + b)
    return done, left, rest_days, x + rest_days


def _partial_answer(inputs):
    return _partial_parts(inputs)[inputs["ask"]]


def _partial_distract(result, inputs):
    step = F(1, 8) if inputs["ask"] in (0, 1) else 1
    return _num_distract(step)(result, inputs)


def _partial_explain(inputs, correct):
    done, left, rest_days, total = _partial_parts(inputs)
    return (
        f"A completes {fmt(done)} first, leaving {fmt(left)}, which takes "
        f"{fmt(rest_days)} days together for a total of {fmt(total)} days. "
        f"The requested value is {correct}."
    )


twd_partial_work = make_family(
    "twd_partial_work",
    ("a", "b", "x", "ask"),
    ((20, 30, 5, 0), (24, 12, 6, 1), (15, 10, 3, 2),
     (18, 9, 4, 3), (30, 20, 10, 1)),
    lambda d: _question(
        [("A alone (days)", d["a"]), ("B alone (days)", d["b"]),
         ("days A worked first", d["x"])],
        _PARTIAL_ASKS[d["ask"]],
    ),
    _partial_answer,
    _partial_distract,
    _partial_explain,
)


# ---------------------------------------------------------------------------
# 19. twd_machine_units
# ---------------------------------------------------------------------------

_MACHINE_ASKS = (
    "How many units does machine A produce?",
    "How many units does machine B produce?",
    "How many units do both machines produce together?",
    "How many extra units does A produce compared with B?",
)


def _machine_answer(inputs):
    ma, mb, hours = inputs["ma"], inputs["mb"], inputs["hours"]
    return F((ma * hours, mb * hours, (ma + mb) * hours, abs(ma - mb) * hours)[
        inputs["ask"]
    ])


def _machine_explain(inputs, correct):
    ma, mb, hours = inputs["ma"], inputs["mb"], inputs["hours"]
    return (
        f"In {hours} hours A makes {ma * hours} units and B makes {mb * hours} "
        f"units, for {((ma + mb) * hours)} units in total. Requested value: {correct}."
    )


twd_machine_units = make_family(
    "twd_machine_units",
    ("ma", "mb", "hours", "ask"),
    ((40, 25, 6, 2), (35, 20, 8, 0), (50, 30, 5, 3),
     (45, 36, 4, 1), (60, 40, 7, 2)),
    lambda d: _question(
        [("machine A rate (units/hour)", d["ma"]),
         ("machine B rate (units/hour)", d["mb"]),
         ("hours run", d["hours"])],
        _MACHINE_ASKS[d["ask"]],
    ),
    _machine_answer,
    _num_distract(5),
    _machine_explain,
)


# ---------------------------------------------------------------------------
# 20. twd_three_share
# ---------------------------------------------------------------------------

_THREE_SHARE_ASKS = (
    "Find A's wage.",
    "Find B's wage.",
    "Find C's wage.",
    "Find the gap between the largest and smallest wage shares.",
)


def _three_share_parts(inputs):
    a, b, c, total = inputs["a"], inputs["b"], inputs["c"], inputs["total_wage"]
    strength = a + b + c
    return (
        F(total * a, strength),
        F(total * b, strength),
        F(total * c, strength),
    )


def _three_share_answer(inputs):
    wa, wb, wc = _three_share_parts(inputs)
    if inputs["ask"] == 3:
        return _money(max(wa, wb, wc) - min(wa, wb, wc))
    return _money((wa, wb, wc)[inputs["ask"]])


def _three_share_explain(inputs, correct):
    wa, wb, wc = _three_share_parts(inputs)
    return (
        f"Wages are divided in the work ratio, giving {fmt(wa)}, {fmt(wb)} and "
        f"{fmt(wc)}. The requested value is {correct}."
    )


twd_three_share = make_family(
    "twd_three_share",
    ("a", "b", "c", "total_wage", "ask"),
    ((4, 3, 5, 2400, 0), (5, 4, 3, 1800, 1), (2, 3, 5, 2000, 2),
     (6, 5, 4, 3000, 3), (7, 3, 2, 2400, 3)),
    lambda d: _question(
        [("A work units", d["a"]), ("B work units", d["b"]),
         ("C work units", d["c"]), ("total wage (Rs)", d["total_wage"])],
        _THREE_SHARE_ASKS[d["ask"]],
    ),
    _three_share_answer,
    _money_distract(100),
    _three_share_explain,
)


# ---------------------------------------------------------------------------
# 21. twd_conditional_bonus
# ---------------------------------------------------------------------------

_CONDITIONAL_ASKS = (
    "Find the combined daily output in units.",
    "Find the bonus earned in one day.",
    "Find the bonus earned in 5 days.",
    "Find the absolute gap between output and the daily target.",
)


def _conditional_answer(inputs):
    a, b, target, bonus = inputs["a"], inputs["b"], inputs["target"], inputs["bonus"]
    out = a + b
    payout = F(bonus) if out > target else F(0)
    if inputs["ask"] == 0:
        return F(out)
    if inputs["ask"] == 1:
        return _money(payout)
    if inputs["ask"] == 2:
        return _money(5 * payout)
    return F(abs(out - target))


def _conditional_distract(result, inputs):
    if inputs["ask"] in (1, 2):
        return _money_distract(100)(result, inputs)
    return _num_distract(2)(result, inputs)


def _conditional_explain(inputs, correct):
    a, b, target, bonus = inputs["a"], inputs["b"], inputs["target"], inputs["bonus"]
    out = a + b
    payout = bonus if out > target else 0
    return (
        f"Combined output is {a}+{b} = {out} units against a {target}-unit "
        f"target, so the daily bonus is Rs {payout}. Requested value: {correct}."
    )


twd_conditional_bonus = make_family(
    "twd_conditional_bonus",
    ("a", "b", "target", "bonus", "ask"),
    ((18, 12, 25, 200, 0), (20, 15, 30, 250, 1), (25, 10, 32, 300, 2),
     (16, 14, 35, 400, 3), (22, 18, 36, 350, 1)),
    lambda d: _question(
        [("A output (units/day)", d["a"]), ("B output (units/day)", d["b"]),
         ("daily target (units)", d["target"]),
         ("bonus if target met (Rs/day)", d["bonus"])],
        _CONDITIONAL_ASKS[d["ask"]],
    ),
    _conditional_answer,
    _conditional_distract,
    _conditional_explain,
)


# ---------------------------------------------------------------------------
# 22. twd_capacity_use
# ---------------------------------------------------------------------------

_CAPACITY_ASKS = (
    "Find the unused capacity in units.",
    "Find the capacity utilisation percentage.",
    "Find the revenue from the units actually used.",
    "Find the revenue at full capacity.",
)


def _capacity_answer(inputs):
    capacity, used, rate = inputs["capacity"], inputs["used"], inputs["rate"]
    if inputs["ask"] == 0:
        return F(capacity - used)
    if inputs["ask"] == 1:
        return _pct(F(100 * used, capacity))
    if inputs["ask"] == 2:
        return _money(F(used * rate))
    return _money(F(capacity * rate))


def _capacity_distract(result, inputs):
    if inputs["ask"] == 1:
        return _pct_distract(5)(result, inputs)
    if inputs["ask"] in (2, 3):
        return _money_distract(100)(result, inputs)
    return _num_distract(10)(result, inputs)


def _capacity_explain(inputs, correct):
    capacity, used, rate = inputs["capacity"], inputs["used"], inputs["rate"]
    return (
        f"Utilisation is {fmt(pct(F(100 * used, capacity)))}; revenue from "
        f"{used} units is Rs {used * rate} and from {capacity} units is "
        f"Rs {capacity * rate}. The requested value is {correct}."
    )


twd_capacity_use = make_family(
    "twd_capacity_use",
    ("capacity", "used", "rate", "ask"),
    ((500, 375, 20, 1), (600, 450, 15, 2), (400, 320, 25, 0),
     (800, 600, 12, 3), (250, 200, 30, 1)),
    lambda d: _question(
        [("capacity (units)", d["capacity"]), ("units used", d["used"]),
         ("rate (Rs/unit)", d["rate"])],
        _CAPACITY_ASKS[d["ask"]],
    ),
    _capacity_answer,
    _capacity_distract,
    _capacity_explain,
)


# ---------------------------------------------------------------------------
# 23. twd_cost_job
# ---------------------------------------------------------------------------

_COST_ASKS = (
    "Find the cost of A's work.",
    "Find the cost of B's work.",
    "Find the total cost of the job.",
    "Find the difference between the two costs.",
)


def _cost_answer(inputs):
    a, b, wage_a, wage_b = (
        inputs["a"], inputs["b"], inputs["wage_a"], inputs["wage_b"]
    )
    ca, cb = F(a * wage_a), F(b * wage_b)
    return _money((ca, cb, ca + cb, abs(ca - cb))[inputs["ask"]])


def _cost_explain(inputs, correct):
    a, b, wage_a, wage_b = (
        inputs["a"], inputs["b"], inputs["wage_a"], inputs["wage_b"]
    )
    ca, cb = a * wage_a, b * wage_b
    return (
        f"A costs {a}*{wage_a} = {ca} and B costs {b}*{wage_b} = {cb}, so the "
        f"job costs {ca + cb}. The requested value is {correct}."
    )


twd_cost_job = make_family(
    "twd_cost_job",
    ("a", "b", "wage_a", "wage_b", "ask"),
    ((8, 6, 500, 400, 2), (10, 7, 450, 350, 0), (12, 9, 600, 500, 1),
     (5, 8, 800, 600, 3), (15, 10, 400, 300, 2)),
    lambda d: _question(
        [("A days", d["a"]), ("B days", d["b"]),
         ("A daily wage (Rs)", d["wage_a"]),
         ("B daily wage (Rs)", d["wage_b"])],
        _COST_ASKS[d["ask"]],
    ),
    _cost_answer,
    _money_distract(100),
    _cost_explain,
)


# ---------------------------------------------------------------------------
# 24. twd_target_days
# ---------------------------------------------------------------------------

_TARGET_ASKS = (
    "How many days are needed at the current rate?",
    "How many days are needed at the improved rate?",
    "How many days are saved after the improvement?",
    "How many units are produced in 3 days at the improved rate?",
)


def _target_answer(inputs):
    work, rate, increment = inputs["work"], inputs["rate"], inputs["increment"]
    current = F(work, rate)
    improved = F(work, rate + increment)
    return (current, improved, current - improved, 3 * (rate + increment))[
        inputs["ask"]
    ]


def _target_explain(inputs, correct):
    work, rate, increment = inputs["work"], inputs["rate"], inputs["increment"]
    return (
        f"At {rate} units/day the work needs {fmt(F(work, rate))} days; at "
        f"{rate + increment} units/day it needs {fmt(F(work, rate + increment))} "
        f"days. The requested value is {correct}."
    )


twd_target_days = make_family(
    "twd_target_days",
    ("work", "rate", "increment", "ask"),
    ((600, 50, 10, 0), (720, 60, 12, 1), (480, 40, 8, 2),
     (900, 75, 15, 3), (360, 30, 6, 2)),
    lambda d: _question(
        [("total work (units)", d["work"]),
         ("current rate (units/day)", d["rate"]),
         ("rate increase (units/day)", d["increment"])],
        _TARGET_ASKS[d["ask"]],
    ),
    _target_answer,
    _num_distract(1),
    _target_explain,
)


# ---------------------------------------------------------------------------
# Family registry and specs
# ---------------------------------------------------------------------------

FAMILIES = [
    twd_solo_days,
    twd_daily_rate,
    twd_work_done,
    twd_wage_ratio,
    twd_efficiency_share,
    twd_man_days,
    twd_missing_days,
    twd_combined_rate,
    twd_two_day_cycle,
    twd_remaining_work,
    twd_average_days,
    twd_ratio_fraction,
    twd_piece_count,
    twd_absentee_lookup,
    twd_wage_per_worker,
    twd_efficiency_ratio,
    twd_time_saved,
    twd_partial_work,
    twd_machine_units,
    twd_three_share,
    twd_conditional_bonus,
    twd_capacity_use,
    twd_cost_job,
    twd_target_days,
]


SPECS = build_specs(FAMILIES, mains=False)


def build_time_and_work_di():
    return build_specs(FAMILIES, mains=False)
