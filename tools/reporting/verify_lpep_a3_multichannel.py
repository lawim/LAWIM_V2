#!/usr/bin/env python3
"""Independent gate for LPEP A.3G multichannel evidence."""
from __future__ import annotations
import json, sys
from pathlib import Path

BASE = Path("docs/reviews/lpep-a3g-independent-multichannel-gate")
N = BASE / "evidence/normalized"

gate_file = N / "final-gate.json"
if not gate_file.is_file():
    print("FATAL: final-gate.json not found")
    sys.exit(1)

gate = json.loads(gate_file.read_text())
checks = []

def check(name, status, detail=""):
    checks.append({"name":name,"status":status,"detail":detail})
    if status not in ("PASS",):
        print(f"  {status}: {name} — {detail}")

check("sha_alignment", gate["sha_alignment"])
check("wiring_tests", "PASS" if gate["wiring_tests"]["fail"] == 0 else "FAIL")
check("v1_canonical", "PASS" if gate["v1_canonical"]["fail"] == 0 and gate["v1_canonical"]["exit"] == 0 else "FAIL")
check("lcip", "PASS" if gate["lcip"]["fail"] == 0 else "FAIL")
check("web", "PASS" if gate["web"]["real_http"] else "FAIL")
check("telegram_config", "PASS" if gate["telegram"]["config_present"] else "FAIL")
check("telegram_real_event", gate["telegram"]["real_event"])
check("telegram_outbound", gate["telegram"]["outbound"])
check("telegram_restart", gate["telegram"]["restart"])
check("telegram_idempotence", gate["telegram"]["idempotence"])
check("whatsapp_config", "PASS" if gate["whatsapp"]["config_present"] else "FAIL")
check("whatsapp_real_event", gate["whatsapp"]["real_event"])
check("whatsapp_outbound", gate["whatsapp"]["outbound"])
check("whatsapp_restart", gate["whatsapp"]["restart"])
check("whatsapp_idempotence", gate["whatsapp"]["idempotence"])
check("logs", "PASS" if gate["logs"]["blocking"] == 0 else "FAIL")
check("raw_evidence", "PASS" if gate["raw_evidence_present"] else "FAIL")

pass_c = sum(1 for c in checks if c["status"] == "PASS")
not_proven = sum(1 for c in checks if c["status"] == "NOT_PROVEN")
not_run = sum(1 for c in checks if c["status"] == "NOT_RUN")
fail_c = sum(1 for c in checks if c["status"] == "FAIL")
print(f"\nChecks: {len(checks)} total, {pass_c} PASS, {not_proven} NOT_PROVEN, {not_run} NOT_RUN, {fail_c} FAIL")
print(f"VERDICT: {gate['verdict']}")
