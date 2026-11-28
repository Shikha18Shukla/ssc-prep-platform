# -*- coding: utf-8 -*-
"""Independent answer formula sheets for Banking Maths Set 8.

Each topic module is written separately from the chapter builders. The
verifier imports this merged dictionary only; it never reads a stored
``correct_answer`` when recomputing an expected result.
"""

from __future__ import annotations

from .formulas_interest import FORMULAS as INTEREST_FORMULAS
from .formulas_interest_di import FORMULAS as INTEREST_DI_FORMULAS
from .formulas_pipe import FORMULAS as PIPE_FORMULAS
from .formulas_speed import FORMULAS as SPEED_FORMULAS
from .formulas_time_work import FORMULAS as TIME_WORK_FORMULAS
from .formulas_time_work_di import FORMULAS as TIME_WORK_DI_FORMULAS

FORMULAS: dict = {}
FORMULAS.update(TIME_WORK_FORMULAS)
FORMULAS.update(TIME_WORK_DI_FORMULAS)
FORMULAS.update(SPEED_FORMULAS)
FORMULAS.update(INTEREST_FORMULAS)
FORMULAS.update(INTEREST_DI_FORMULAS)
FORMULAS.update(PIPE_FORMULAS)
