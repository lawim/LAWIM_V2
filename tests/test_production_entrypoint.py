from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
ENTRYPOINT = REPO / "scripts" / "entrypoint.sh"


def test_entrypoint_no_healthhandler_inline():
    content = ENTRYPOINT.read_text(encoding="utf-8")
    assert "HealthHandler" not in content, "entrypoint must not define HealthHandler"
    assert "class HealthHandler" not in content
    assert "http.server.BaseHTTPRequestHandler" not in content


def test_entrypoint_starts_full_server():
    content = ENTRYPOINT.read_text(encoding="utf-8")
    assert "python -m lawim_v2" in content, "entrypoint must start full server via python -m"


def test_entrypoint_validates_runtime_imports():
    content = ENTRYPOINT.read_text(encoding="utf-8")
    assert "IMPORT_PASS" in content, "entrypoint must validate runtime imports"
    assert "lawim_runtime.conversation.journey" in content


def test_entrypoint_fails_on_missing_runtime():
    content = ENTRYPOINT.read_text(encoding="utf-8")
    assert "IMPORT_FAIL" in content, "entrypoint must report import failures"
    assert "raise SystemExit(1)" in content


def test_entrypoint_disables_pf_gracefully():
    content = ENTRYPOINT.read_text(encoding="utf-8")
    assert "PROGRAM_F_DISABLED:by feature flag" in content


def test_entrypoint_uses_exec():
    content = ENTRYPOINT.read_text(encoding="utf-8")
    assert content.strip().startswith("#!/usr/bin/env sh")
    assert "exec python -m lawim_v2" in content


def test_entrypoint_sets_eu():
    content = ENTRYPOINT.read_text(encoding="utf-8")
    assert "set -eu" in content


def test_entrypoint_shows_build_sha():
    content = ENTRYPOINT.read_text(encoding="utf-8")
    assert "LAWIM_BUILD_SHA=" in content


def test_entrypoint_syntax_valid():
    result = subprocess.run(
        ["sh", "-n", str(ENTRYPOINT)],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, f"Shell syntax error: {result.stderr}"


def test_entrypoint_python_syntax_valid():
    import re
    content = ENTRYPOINT.read_text(encoding="utf-8")
    m = re.search(r"python3 - <<'PY'\n(.*?)\nPY", content, re.DOTALL)
    assert m, "Could not find inline Python block"
    py_block = m.group(1)
    compile(py_block, "<entrypoint-py-block>", "exec")
