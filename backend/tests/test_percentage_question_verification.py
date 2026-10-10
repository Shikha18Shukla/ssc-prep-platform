"""Regression coverage for the PowerShell post-import verifier."""

import shutil
import subprocess
from pathlib import Path

import pytest


TEST_SCRIPT = Path(__file__).with_suffix(".ps1")


def test_verifier_normalizes_matching_and_reports_a_missing_candidate_without_batch_failure():
    powershell = shutil.which("powershell.exe") or shutil.which("pwsh")
    if powershell is None:
        pytest.skip("PowerShell is required to exercise the PowerShell verification helper")

    result = subprocess.run(
        [
            powershell,
            "-NoLogo",
            "-NoProfile",
            "-NonInteractive",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(TEST_SCRIPT),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "absent candidate reported MISSING" in result.stdout
    assert "UTF-8 candidate 2 verified active" in result.stdout
    assert "no batch failure" in result.stdout
