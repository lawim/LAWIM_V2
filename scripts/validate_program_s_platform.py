#!/usr/bin/env python3
"""Program S — Analytics, Learning, AI, Ecosystem, Future & Debt Validator."""
from __future__ import annotations

import sys

from lawim_v2.program_s.s1_analytics import MetricDomain
from lawim_v2.program_s.s2_learning import TrainingStatus
from lawim_v2.program_s.s3_agents import AGENT_ACTIVATIONS
from lawim_v2.program_s.s4_ecosystem import CONNECTOR_TYPES
from lawim_v2.program_s.s5_future import CONSTITUTION, ConstitutionalRule
from lawim_v2.program_s.s6_debt import RBAC_PERMISSIONS, FRONTEND_REQUIREMENTS

errors: list[str] = []

# S1
for d in MetricDomain:
    if not d.value:
        errors.append(f"MetricDomain {d.name} empty")

# S2
for ts in TrainingStatus:
    if not ts.value:
        errors.append(f"TrainingStatus {ts.name} empty")

# S3
if len(AGENT_ACTIVATIONS) != 16:
    errors.append(f"Expected 16 agent activations, got {len(AGENT_ACTIVATIONS)}")
codes = [a.agent_code for a in AGENT_ACTIVATIONS]
if len(codes) != len(set(codes)):
    errors.append("Duplicate agent activation codes")

# S4
if len(CONNECTOR_TYPES) != 15:
    errors.append(f"Expected 15 connector types, got {len(CONNECTOR_TYPES)}")

# S5
if len(CONSTITUTION) < 5:
    errors.append(f"Expected 5+ constitutional rules, got {len(CONSTITUTION)}")
for rule in CONSTITUTION:
    if not rule.non_negotiable:
        errors.append(f"Rule {rule.rule_id} should be non-negotiable")

# S6
if "admin" not in RBAC_PERMISSIONS:
    errors.append("RBAC missing admin role")
if len(FRONTEND_REQUIREMENTS) < 5:
    errors.append(f"Expected 5+ frontend requirements, got {len(FRONTEND_REQUIREMENTS)}")

if errors:
    print(f"ERRORS ({len(errors)}):")
    for e in errors:
        print(f"  {e}")
    sys.exit(1)
else:
    print(f"  S1-S6 bundles: 6/6")
    print(f"  VERDICT: PASS")
    sys.exit(0)
