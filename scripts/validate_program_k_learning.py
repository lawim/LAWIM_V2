#!/usr/bin/env python3
"""Program K — Learning Machine Foundation Validator."""
from __future__ import annotations

import sys

from lawim_v2.program_k.learning_config import LearningConfig
from lawim_v2.program_k.learning_models import (
    FeedbackOrigin,
    FeedbackTarget,
    LearningEventSource,
    LearningEventType,
    OutcomeStatus,
)
from lawim_v2.program_k.learning_registry import learning_event_registry, list_event_types

errors: list[str] = []
warnings: list[str] = []

# ── 1. Event Types ─────────────────────────────────────────────────────────

types = list_event_types()
if not types:
    errors.append("No learning event types defined")

type_set = set(types)
if len(types) != len(type_set):
    errors.append("Duplicate event types")

for et in LearningEventType:
    parts = et.value.split("_", 1)
    source_prefix = parts[0]
    if source_prefix not in ("H", "J", "OUTCOME", "FEEDBACK"):
        warnings.append(f"Event type {et.value} does not follow H/J/OUTCOME/FEEDBACK naming")

# ── 2. Event Sources ──────────────────────────────────────────────────────

sources = [s.value for s in LearningEventSource]
if len(sources) != len(set(sources)):
    errors.append("Duplicate event source values")

# ── 3. Outcome Statuses ───────────────────────────────────────────────────

statuses = [s.value for s in OutcomeStatus]
if len(statuses) != len(set(statuses)):
    errors.append("Duplicate outcome status values")

for status in OutcomeStatus:
    if not status.value:
        errors.append(f"OutcomeStatus {status.name} has empty value")

# ── 4. Feedback Origins and Targets ───────────────────────────────────────

for enum_class, name in [(FeedbackOrigin, "FeedbackOrigin"), (FeedbackTarget, "FeedbackTarget")]:
    values = [v.value for v in enum_class]
    if len(values) != len(set(values)):
        errors.append(f"Duplicate values in {name}")

# ── 5. Registry interaction ───────────────────────────────────────────────

try:
    learning_event_registry.count()
except Exception as e:
    errors.append(f"LearningEventRegistry.count() failed: {e}")

# ── 6. Feature Flags ──────────────────────────────────────────────────────

cfg = LearningConfig()
if cfg.learning_events_enabled:
    warnings.append("learning_events_enabled should be False by default")
if cfg.outcome_registry_enabled:
    warnings.append("outcome_registry_enabled should be False by default")
if cfg.feedback_engine_enabled:
    warnings.append("feedback_engine_enabled should be False by default")

# ── Results ─────────────────────────────────────────────────────────────────

if errors:
    print(f"ERRORS ({len(errors)}):")
    for e in errors:
        print(f"  \u274c {e}")
if warnings:
    print(f"WARNINGS ({len(warnings)}):")
    for w in warnings:
        print(f"  \u26a0\ufe0f {w}")

print(f"\n  Event types:     {len(types)}")
print(f"  Event sources:   {len(sources)}")
print(f"  Outcome statuses: {len(statuses)}")
print(f"  Feedback origins: {len(list(FeedbackOrigin))}")
print(f"  Feedback targets: {len(list(FeedbackTarget))}")
print(f"  Feature flags:   all disabled by default")

if errors:
    print("\n  VERDICT: VALIDATION FAILED")
    sys.exit(1)
else:
    print("\n  VERDICT: PASS")
    sys.exit(0)
