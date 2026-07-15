#!/usr/bin/env python3
"""Program Q — Knowledge & Decision Validator."""
from __future__ import annotations

import sys

from lawim_v2.program_q import ProgramQConfig
from lawim_v2.program_q.q1_property import PropertyState, PROPERTY_TRANSITIONS
from lawim_v2.program_q.q2_qualification import QuestionPriority
from lawim_v2.program_q.q3_geography import MobilityMode, EXPANSION_STAGES
from lawim_v2.program_q.q4_intent import BusinessTransactionType
from lawim_v2.program_q.q5_matching import (
    CompatibilityLevel, GeoScoringTier, MatchingRole, ScoringDimension,
)
from lawim_v2.program_q.q6_architecture import ConflictType
from lawim_v2.program_q.q7_cognitive import WorkflowPreview

errors: list[str] = []

# ── Q1: Property ──────────────────────────────────────────────────────────

for state in PropertyState:
    if state in PROPERTY_TRANSITIONS:
        for target in PROPERTY_TRANSITIONS[state]:
            if target not in PropertyState:
                errors.append(f"Invalid transition target {target} from {state}")

# ── Q2: Qualification ─────────────────────────────────────────────────────

for pq in QuestionPriority:
    if not pq.value:
        errors.append(f"QuestionPriority {pq.name} empty value")

# ── Q3: Geography ─────────────────────────────────────────────────────────

if len(EXPANSION_STAGES) != 9:
    errors.append(f"Expected 9 expansion stages, got {len(EXPANSION_STAGES)}")

# ── Q4: Intent ────────────────────────────────────────────────────────────

for tt in BusinessTransactionType:
    if not tt.value:
        errors.append(f"BusinessTransactionType {tt.name} empty value")

# ── Q5: Matching ──────────────────────────────────────────────────────────

for enum_class, name in [(ScoringDimension, "ScoringDimension"),
                          (GeoScoringTier, "GeoScoringTier"),
                          (CompatibilityLevel, "CompatibilityLevel"),
                          (MatchingRole, "MatchingRole")]:
    values = [e.value for e in enum_class]
    if len(values) != len(set(values)):
        errors.append(f"Duplicate values in {name}")

# ── Q6: Architecture ──────────────────────────────────────────────────────

for ct in ConflictType:
    if not ct.value:
        errors.append(f"ConflictType {ct.name} empty value")

# ── Q7: Cognitive ─────────────────────────────────────────────────────────

wp = WorkflowPreview(workflow_id="w1", name="test")
if wp.to_dict().get("workflow_id") != "w1":
    errors.append("WorkflowPreview to_dict failed")

# ── Feature Flags ─────────────────────────────────────────────────────────

cfg = ProgramQConfig()
for f in ("property_model_extensions_enabled", "qualification_enhancements_enabled",
           "geography_search_enabled", "intent_detection_enabled",
           "matching_scoring_enabled", "architecture_open_points_enabled",
           "cognitive_core_enabled"):
    if getattr(cfg, f):
        errors.append(f"{f} should be False by default")

if errors:
    print(f"ERRORS ({len(errors)}):")
    for e in errors:
        print(f"  \u274c {e}")
    print("\n  VERDICT: VALIDATION FAILED")
    sys.exit(1)
else:
    print(f"  Q1-Q7 bundles: 7/7")
    print(f"  Feature flags: 7, all disabled by default")
    print("\n  VERDICT: PASS")
    sys.exit(0)
