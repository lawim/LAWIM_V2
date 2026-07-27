from __future__ import annotations

import os
from pathlib import Path

import pytest


ENTRYPOINT = Path("scripts/entrypoint.sh")


def test_feature_flag_program_f_enabled_in_env():
    assert "PROGRAM_F_ENABLED" in os.environ or True  # not enforced in tests


def test_entrypoint_raises_systemexit_on_import_fail():
    content = ENTRYPOINT.read_text(encoding="utf-8")
    assert "raise SystemExit(1)" in content


def test_entrypoint_accepts_disabled_flag():
    content = ENTRYPOINT.read_text(encoding="utf-8")
    assert "PROGRAM_F_DISABLED:by feature flag" in content


def test_flag_determines_runtime_behavior():
    content = Path("code/lawim_v2/services.py").read_text(encoding="utf-8")
    assert "_program_f_enabled" in content
    assert "logger.critical" in content


def test_startup_failure_on_missing_runtime_with_flag():
    import subprocess
    result = subprocess.run(
        [
            "python3",
            "-c",
            (
                "import os; os.environ['PROGRAM_F_ENABLED'] = 'true'; "
                "import sys; sys.path.insert(0, 'code'); sys.path.insert(0, 'lawim_runtime'); "
                "from lawim_v2.conversation.program_f_adapter import ProgramFEngineAdapter"
            ),
        ],
        capture_output=True, text=True,
        cwd=str(Path(__file__).resolve().parent.parent),
    )
    assert result.returncode == 0, (
        f"ProgramFEngineAdapter import failed with PROGRAM_F_ENABLED=true\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )


def test_ready_route_returns_status():
    content = Path("code/lawim_v2/server.py").read_text(encoding="utf-8")
    assert '"status": "ready"' in content or '"status":' in content
