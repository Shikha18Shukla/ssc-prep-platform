"""Compatibility entry point for the reviewed Maximum/Minimum batch builder."""
import runpy
from pathlib import Path

builder = Path(__file__).with_name("build_max_minimum_equations_verified_batch.py")
runpy.run_path(str(builder))["main"]()
