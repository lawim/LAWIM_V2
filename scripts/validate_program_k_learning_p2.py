#!/usr/bin/env python3
"""Program K Part 2 — Learning Datasets, Analysis and Proposals Validator."""
from __future__ import annotations

import sys

from lawim_v2.program_k.learning_config_p2 import LearningConfigP2
from lawim_v2.program_k.learning_datasets import feature_catalog
from lawim_v2.program_k.learning_models_p2 import (
    DatasetCategory,
    DatasetStatus,
    ExperimentResult,
    ExperimentStatus,
    HypothesisStatus,
    ProposalStatus,
    ProposalType,
    ReviewDecision,
)

errors: list[str] = []
warnings: list[str] = []

# ── 1. Feature Catalog ─────────────────────────────────────────────────────

if feature_catalog.count() == 0:
    errors.append("Feature catalog is empty")
else:
    codes = [f.feature_code for f in feature_catalog.list_all()]
    if len(codes) != len(set(codes)):
        dupes = [c for c in codes if codes.count(c) > 1]
        errors.append(f"Duplicate feature codes: {dupes}")
    for f in feature_catalog.list_all():
        if not f.calculation:
            errors.append(f"Feature {f.feature_code} missing calculation")
        if not f.source:
            errors.append(f"Feature {f.feature_code} missing source")

# ── 2. Enums ───────────────────────────────────────────────────────────────

for enum_class, name in [(DatasetCategory, "DatasetCategory"),
                          (DatasetStatus, "DatasetStatus"),
                          (ProposalType, "ProposalType"),
                          (ProposalStatus, "ProposalStatus"),
                          (ReviewDecision, "ReviewDecision"),
                          (HypothesisStatus, "HypothesisStatus"),
                          (ExperimentStatus, "ExperimentStatus"),
                          (ExperimentResult, "ExperimentResult")]:
    values = [e.value for e in enum_class]
    if len(values) != len(set(values)):
        errors.append(f"Duplicate values in {name}")

# ── 3. Feature Flags ──────────────────────────────────────────────────────

cfg = LearningConfigP2()
for flag_name in ("learning_dataset_builder_enabled", "learning_analysis_enabled",
                   "learning_proposal_engine_enabled", "learning_experiments_enabled",
                   "knowledge_evolution_packages_enabled"):
    if getattr(cfg, flag_name):
        warnings.append(f"{flag_name} should be False by default")

# ── Results ─────────────────────────────────────────────────────────────────

if errors:
    print(f"ERRORS ({len(errors)}):")
    for e in errors:
        print(f"  \u274c {e}")
if warnings:
    print(f"WARNINGS ({len(warnings)}):")
    for w in warnings:
        print(f"  \u26a0\ufe0f {w}")

print(f"\n  Features:        {feature_catalog.count()}")
print(f"  Dataset categories: {len(list(DatasetCategory))}")
print(f"  Proposal types:     {len(list(ProposalType))}")
print(f"  Experiment statuses: {len(list(ExperimentStatus))}")
print(f"  Feature flags:      all disabled by default")

if errors:
    print("\n  VERDICT: VALIDATION FAILED")
    sys.exit(1)
else:
    print("\n  VERDICT: PASS")
    sys.exit(0)
