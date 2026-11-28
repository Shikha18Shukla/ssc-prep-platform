# -*- coding: utf-8 -*-
"""Independent answer formula sheets for Banking Maths Set 7.

Each topic module is written separately from the chapter builders. The
verifier imports this merged dictionary only; it never reads a stored
``correct_answer`` when recomputing an expected result.
"""

from __future__ import annotations

from .formulas_ages import FORMULAS as AGES_FORMULAS
from .formulas_mixture import FORMULAS as MIXTURE_FORMULAS
from .formulas_partnership import FORMULAS as PARTNERSHIP_FORMULAS

FORMULAS: dict = {}
FORMULAS.update(MIXTURE_FORMULAS)
FORMULAS.update(AGES_FORMULAS)
FORMULAS.update(PARTNERSHIP_FORMULAS)
