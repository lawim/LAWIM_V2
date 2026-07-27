#!/usr/bin/env python3
"""Independent pre-deployment gate for LPEP A.2 production wiring."""

from __future__ import annotations

import hashlib
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "code"))
sys.path.insert(0, str(REPO / "lawim_runtime"))

CHECKS: list[dict] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    CHECKS.append({"name": name, "status": "PASS" if ok else "FAIL", "detail": detail})
    if not ok:
        print(f"  FAIL: {name} — {detail}")


def sha256_of(path: str) -> str:
    p = REPO / path
    if p.is_file():
        return hashlib.sha256(p.read_bytes()).hexdigest()[:16]
    return "NOT_FOUND"


print("=== LPEP A.2 Independent Gate ===")
print()

# 1. entrypoint
ep = REPO / "scripts" / "entrypoint.sh"
ep_text = ep.read_text(encoding="utf-8")
check("entrypoint_exists", ep.is_file(), str(ep))
check("no_healthhandler_inline", "HealthHandler" not in ep_text)
check("full_server_started", "exec python -m lawim_v2" in ep_text)
check("import_validation", "IMPORT_PASS" in ep_text)
check("import_fail_handling", "IMPORT_FAIL" in ep_text)
check("systemexit_on_fail", "raise SystemExit(1)" in ep_text)
check("build_sha_display", "LAWIM_BUILD_SHA" in ep_text)
check("set_eu", "set -eu" in ep_text)

# 2. Dockerfile
df = REPO / "Dockerfile"
df_text = df.read_text(encoding="utf-8")
check("dockerfile_exists", df.is_file(), str(df))
check("lawim_runtime_copied", "lawim_runtime" in df_text)
check("conversation_v2_flag", "LAWIM_FEATURE_CONVERSATION_V2=true" in df_text)
check("program_f_flag", "PROGRAM_F_ENABLED=true" in df_text)

# 3. services.py
svc = REPO / "code" / "lawim_v2" / "services.py"
svc_text = svc.read_text(encoding="utf-8")
check("services_pf_critical_on_missing", "logger.critical" in svc_text)
check("services_pf_raise_on_missing", "raise" in svc_text and "ImportError" in svc_text)
check("services_pf_flag_read", "PROGRAM_F_ENABLED" in svc_text)
check("services_pf_disabled_graceful", "PROGRAM_F_ENABLED=false" in svc_text)

# 4. server.py routes
srv = REPO / "code" / "lawim_v2" / "server.py"
srv_text = srv.read_text(encoding="utf-8")
check("server_py_exists", srv.is_file(), str(srv))
check("health_route", '"/health"' in srv_text or "'/health'" in srv_text or "{'/health'" in srv_text)
check("healthz_route", '"/healthz"' in srv_text)
check("readyz_route", '"/readyz"' in srv_text)
check("web_conversations_route", '"/api/conversations"' in srv_text)
check("telegram_webhook_route", '"/api/notifications/telegram/webhook"' in srv_text)
check("whatsapp_webhook_route", '"/api/notifications/whatsapp/webhook"' in srv_text)
check("v3_conversations_route", '"/api/v3/conversations"' in srv_text)

# 5. compose
compose = REPO / "deployment" / "compose" / "docker-compose.prod.yml"
comp_text = compose.read_text(encoding="utf-8")
check("compose_exists", compose.is_file(), str(compose))
check("compose_conversation_v2_flag", "LAWIM_FEATURE_CONVERSATION_V2" in comp_text)
check("compose_program_f_flag", "PROGRAM_F_ENABLED" in comp_text)

# 6. test pass
result = subprocess.run(
    [
        sys.executable, "-m", "pytest",
        str(REPO / "tests/test_production_entrypoint.py"),
        str(REPO / "tests/test_production_composition_root.py"),
        str(REPO / "tests/test_production_route_registration.py"),
        str(REPO / "tests/test_conversation_runtime_startup_policy.py"),
        "-q", "-ra",
    ],
    capture_output=True, text=True,
    cwd=str(REPO),
)
test_ok = result.returncode == 0
check("production_wiring_tests_pass", test_ok, f"returncode={result.returncode}")
if not test_ok:
    for line in result.stdout.splitlines():
        print(f"    {line}")
    for line in result.stderr.splitlines():
        print(f"    {line}")

# 7. key file integrity (file presence)
for fp in ["scripts/entrypoint.sh", "Dockerfile", "deployment/compose/docker-compose.prod.yml",
           "code/lawim_v2/services.py", "code/lawim_v2/server.py",
           "code/lawim_v2/conversation/program_f_adapter.py"]:
    p = REPO / fp
    check(f"file_present_{fp}", p.is_file(), str(p))

# Summary
pass_count = sum(1 for c in CHECKS if c["status"] == "PASS")
fail_count = sum(1 for c in CHECKS if c["status"] == "FAIL")
total = len(CHECKS)
print()
print(f"=== SUMMARY: {pass_count}/{total} PASS, {fail_count}/{total} FAIL ===")
verdict = "LPEP_A2_INDEPENDENT_GATE_PASS" if fail_count == 0 else "LPEP_A2_INDEPENDENT_GATE_FAIL"
print(f"VERDICT: {verdict}")

if fail_count > 0:
    sys.exit(1)
