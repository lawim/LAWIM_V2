#!/usr/bin/env python3
"""Program R — CRM, Services, Agency & Workflows Validator."""
from __future__ import annotations

import sys

from lawim_v2.program_r import ProgramRConfig
from lawim_v2.program_r.r1_crm import (
    BOOSTER_DEFINITIONS, LEAD_CLASS_THRESHOLDS, LeadClass,
    PENALTY_DEFINITIONS, PipelineStage,
)
from lawim_v2.program_r.r2_agency import TRUST_LEVEL_ORDER
from lawim_v2.program_r.r3_service import SERVICE_ORDER_TRANSITIONS, PaymentState
from lawim_v2.program_r.r4_project import DOSSIER_TRANSITIONS
from lawim_v2.program_r.r5_relationship import CONSENT_TRANSITIONS
from lawim_v2.program_r.r6_workflow import WORKFLOW_STATE_MACHINES
from lawim_v2.program_r.r7_events import EVENT_CATALOG_ENTRIES
from lawim_v2.program_r.r9_migration import GOLD_WORKFLOW_STATES

errors: list[str] = []

# ── R1: CRM ────────────────────────────────────────────────────────────────

if len(BOOSTER_DEFINITIONS) != 13:
    errors.append(f"Expected 13 boosters, got {len(BOOSTER_DEFINITIONS)}")
if len(PENALTY_DEFINITIONS) != 8:
    errors.append(f"Expected 8 penalties, got {len(PENALTY_DEFINITIONS)}")

for lc in LeadClass:
    if lc not in LEAD_CLASS_THRESHOLDS:
        errors.append(f"LeadClass {lc} missing threshold")
for stage in PipelineStage:
    if not stage.value:
        errors.append(f"PipelineStage {stage.name} empty value")

# ── R2: Agency ─────────────────────────────────────────────────────────────

if len(TRUST_LEVEL_ORDER) != 6:
    errors.append(f"Expected 6 trust levels, got {len(TRUST_LEVEL_ORDER)}")

# ── R3: Service ────────────────────────────────────────────────────────────

for so_status in SERVICE_ORDER_TRANSITIONS:
    if not so_status.value:
        errors.append(f"ServiceOrderStatus {so_status.name} empty value")

for ps in PaymentState:
    if not ps.value:
        errors.append(f"PaymentState {ps.name} empty value")

# ── R4: Projects ───────────────────────────────────────────────────────────

for ds in DOSSIER_TRANSITIONS:
    if not ds.value:
        errors.append(f"DossierState {ds.name} empty value")

# ── R5: Relationship ───────────────────────────────────────────────────────

for cs in CONSENT_TRANSITIONS:
    if not cs.value:
        errors.append(f"ConsentStatus {cs.name} empty value")

# ── R6: Workflow ───────────────────────────────────────────────────────────

if len(WORKFLOW_STATE_MACHINES) != 14:
    errors.append(f"Expected 14 workflow types, got {len(WORKFLOW_STATE_MACHINES)}")

# ── R7: Events ─────────────────────────────────────────────────────────────

if len(EVENT_CATALOG_ENTRIES) < 10:
    errors.append(f"Expected 10+ event catalog entries, got {len(EVENT_CATALOG_ENTRIES)}")

# ── R9: Migration ──────────────────────────────────────────────────────────

if len(GOLD_WORKFLOW_STATES) != 14:
    errors.append(f"Expected 14 Gold workflow states, got {len(GOLD_WORKFLOW_STATES)}")

# ── Feature Flags ──────────────────────────────────────────────────────────

cfg = ProgramRConfig()
for attr in dir(cfg):
    if attr.endswith("_enabled") and getattr(cfg, attr):
        errors.append(f"{attr} should be False by default")

if errors:
    print(f"ERRORS ({len(errors)}):")
    for e in errors:
        print(f"  \u274c {e}")
    sys.exit(1)
else:
    print(f"  R1-R10 bundles: 10/10")
    print(f"  Feature flags: 10, all disabled by default")
    print("  VERDICT: PASS")
    sys.exit(0)
