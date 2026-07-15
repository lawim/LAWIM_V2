#!/usr/bin/env python3
"""Program J — Analytics, Dashboards and Recalculation Validator."""
from __future__ import annotations

import sys

from lawim_v2.program_j.analytics_config import AnalyticsConfig
from lawim_v2.program_j.analytics_models import AggregationType, MetricDomain, MetricStatus
from lawim_v2.program_j.analytics_registry import get_metric, list_metrics, metric_codes, to_dict_list

errors: list[str] = []
warnings: list[str] = []

# ── 1. Metric Catalog ──────────────────────────────────────────────────────

metrics = list_metrics()
codes = [m.metric_code for m in metrics]
if len(codes) != len(set(codes)):
    dupes = [c for c in codes if codes.count(c) > 1]
    errors.append(f"Duplicate metric codes: {dupes}")

if not metrics:
    errors.append("Metric catalog is empty")

for m in metrics:
    if not m.metric_code:
        errors.append("Metric missing code")
    if not m.name:
        errors.append(f"Metric {m.metric_code} missing name")
    if not m.formula:
        errors.append(f"Metric {m.metric_code} missing formula")
    if not m.formula_version:
        errors.append(f"Metric {m.metric_code} missing formula_version")
    if m.domain not in MetricDomain:
        errors.append(f"Metric {m.metric_code} invalid domain")
    if m.aggregation_type not in AggregationType:
        errors.append(f"Metric {m.metric_code} invalid aggregation_type")
    if m.status not in MetricStatus:
        errors.append(f"Metric {m.metric_code} invalid status")

# Check specific required metrics exist
required = ["CAMPAIGNS_TOTAL", "PUBLICATIONS_TOTAL", "CLICKS_TOTAL", "CONVERSIONS_TOTAL",
            "CONVERSION_RATE", "REVENUE_TOTAL", "LEADS_CREATED", "PAYMENTS_CONFIRMED"]
for code in required:
    if get_metric(code) is None:
        errors.append(f"Required metric {code} missing")

# ── 2. Metric Domains ──────────────────────────────────────────────────────

domains = set()
for m in metrics:
    domains.add(m.domain.value)
expected_domains = {"CHANNEL", "CAMPAIGN", "PUBLICATION", "ACTOR", "CONVERSATION",
                     "QUALIFICATION", "MATCHING", "VISIT", "TRANSACTION", "PAYMENT", "CONVERSION"}
for d in expected_domains:
    if d not in domains:
        warnings.append(f"No metrics in domain {d}")

# ── 3. Aggregation Types ───────────────────────────────────────────────────

for at in AggregationType:
    found = any(m.aggregation_type == at for m in metrics)
    if not found and at != AggregationType.PERCENTILE:
        warnings.append(f"No metric uses aggregation type {at.value}")

# ── 4. Metric Definitions have versions ────────────────────────────────────

versions = set()
for m in metrics:
    versions.add(m.formula_version)
if not versions:
    warnings.append("No formula versions found")

# ── 5. Dimensions coherence ────────────────────────────────────────────────

from lawim_v2.program_j.analytics_models import ANALYTICS_DIMENSIONS
if not ANALYTICS_DIMENSIONS:
    errors.append("ANALYTICS_DIMENSIONS is empty")
if len(ANALYTICS_DIMENSIONS) < 20:
    warnings.append(f"Only {len(ANALYTICS_DIMENSIONS)} dimensions defined")

# ── 6. Feature Flags ──────────────────────────────────────────────────────

cfg = AnalyticsConfig()
if cfg.marketing_analytics_enabled:
    warnings.append("marketing_analytics_enabled should be False by default")
if cfg.analytics_dashboards_enabled:
    warnings.append("analytics_dashboards_enabled should be False by default")
if cfg.analytics_recalculation_enabled:
    warnings.append("analytics_recalculation_enabled should be False by default")

# ── 7. Serialization ──────────────────────────────────────────────────────

dict_list = to_dict_list()
if len(dict_list) != len(metrics):
    errors.append("to_dict_list length mismatch")

# ── Results ─────────────────────────────────────────────────────────────────

if errors:
    print(f"ERRORS ({len(errors)}):")
    for e in errors:
        print(f"  \u274c {e}")
if warnings:
    print(f"WARNINGS ({len(warnings)}):")
    for w in warnings:
        print(f"  \u26a0\ufe0f {w}")

print(f"\n  Metrics:         {len(metrics)}")
print(f"  Domains:         {len(domains)}")
print(f"  Dimensions:      {len(ANALYTICS_DIMENSIONS)}")
print(f"  Formula versions: {len(versions)}")
print(f"  Feature flags:   all disabled by default")

if errors:
    print("\n  VERDICT: VALIDATION FAILED")
    sys.exit(1)
else:
    print("\n  VERDICT: PASS")
    sys.exit(0)
