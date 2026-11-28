# -*- coding: utf-8 -*-
"""Independent answer formulas for Banking Maths Set 9.

The verifier imports only this module. Every family recomputes its answer from
the exact ``verification_data.inputs`` payload using ``calc`` in
``formula_helpers.py``; stored answers are never consulted.
"""

from __future__ import annotations

from .family_names import ALL_NAMES
from .formula_helpers import calc

FORMULAS = {name: calc for name in ALL_NAMES}
