#!/usr/bin/env python3
"""Program K Final — Governance, Publication, Rollout, Monitoring Validator."""
from __future__ import annotations

import sys

from lawim_v2.program_k.learning_governance import (
    LEARNING_PERMISSIONS, RELEASE_GATES, DriftType, GuardrailAction,
    PackageStatus, PostPublicationResult, RiskLevel, RolloutStage,
    RolloutStrategy, VersionStatus,
)

errors: list[str] = []
warnings: list[str] = []

# ── Permissions ────────────────────────────────────────────────────────────

if not LEARNING_PERMISSIONS:
    errors.append("LEARNING_PERMISSIONS is empty")
if len(LEARNING_PERMISSIONS) != len(set(LEARNING_PERMISSIONS)):
    errors.append("Duplicate permissions")

required_perms = ["learning.events.read", "learning.publications.approve",
                   "learning.emergency_stop"]
for p in required_perms:
    if p not in LEARNING_PERMISSIONS:
        errors.append(f"Required permission {p} missing")

# ── Release Gates ──────────────────────────────────────────────────────────

if not RELEASE_GATES:
    errors.append("RELEASE_GATES is empty")
if len(RELEASE_GATES) != len(set(RELEASE_GATES)):
    errors.append("Duplicate release gates")
required_gates = ["SCHEMA_VALID", "UNIT_TESTS_PASS", "NON_REGRESSION_PASS",
                   "APPROVALS_COMPLETE", "FEATURE_FLAGS_READY"]
for g in required_gates:
    if g not in RELEASE_GATES:
        errors.append(f"Required release gate {g} missing")

# ── Risk Levels ────────────────────────────────────────────────────────────

for rl in RiskLevel:
    if not rl.value:
        errors.append(f"RiskLevel {rl.name} has empty value")

# ── Enums ──────────────────────────────────────────────────────────────────

for enum_class, name in [(PackageStatus, "PackageStatus"),
                          (RolloutStage, "RolloutStage"),
                          (RolloutStrategy, "RolloutStrategy"),
                          (VersionStatus, "VersionStatus"),
                          (DriftType, "DriftType"),
                          (GuardrailAction, "GuardrailAction"),
                          (PostPublicationResult, "PostPublicationResult")]:
    values = [e.value for e in enum_class]
    if len(values) != len(set(values)):
        errors.append(f"Duplicate values in {name}")

# ── Results ─────────────────────────────────────────────────────────────────

if errors:
    print(f"ERRORS ({len(errors)}):")
    for e in errors:
        print(f"  \u274c {e}")
if warnings:
    print(f"WARNINGS ({len(warnings)}):")
    for w in warnings:
        print(f"  \u26a0\ufe0f {w}")

print(f"\n  Permissions:     {len(LEARNING_PERMISSIONS)}")
print(f"  Release gates:   {len(RELEASE_GATES)}")
print(f"  Risk levels:     {len(list(RiskLevel))}")
print(f"  Package statuses: {len(list(PackageStatus))}")
print(f"  Rollout stages:  {len(list(RolloutStage))}")

if errors:
    print("\n  VERDICT: VALIDATION FAILED")
    sys.exit(1)
else:
    print("\n  VERDICT: PASS")
    sys.exit(0)
