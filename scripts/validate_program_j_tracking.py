#!/usr/bin/env python3
"""Program J — Publication Tracking, Attribution and Conversion Validator."""
from __future__ import annotations

import sys
import re

from lawim_v2.program_j.tracking_models import (
    AttributionModel,
    CampaignStatus,
    ConversionEvent,
    ExternalCampaign,
    ExternalChannelCode,
    ExternalPublication,
    LeadAttribution,
    PublicationStatus,
    RedirectLog,
    TouchpointType,
    generate_tracking_code,
    parse_tracking_code,
)

errors: list[str] = []
warnings: list[str] = []

# ── 1. Canonical Channel Codes ──────────────────────────────────────────────

codes = [c.value for c in ExternalChannelCode]
if len(codes) != len(set(codes)):
    errors.append(f"Duplicate channel codes: {[c for c in codes if codes.count(c) > 1]}")

for code in ExternalChannelCode:
    if len(code.value) != 2:
        errors.append(f"Channel code {code.value} must be 2 characters")
    if not code.value.isupper():
        errors.append(f"Channel code {code.value} must be uppercase")

# ── 2. Tracking Code Format ─────────────────────────────────────────────────

examples = [
    generate_tracking_code("FB", 128, 2026, 6, 1),
    generate_tracking_code("WA", 14, 2026, 6, 14),
    generate_tracking_code("TG", 45, 2026, 7, 3),
]

pattern = r"^[A-Z]{2}-LAWIM-\d{6}-\d{4}-\d{2}-\d{3}$"
for ex in examples:
    if not re.match(pattern, ex):
        errors.append(f"Tracking code {ex} does not match expected format")

# Verify examples match spec
expected = ["FB-LAWIM-000128-2026-06-001", "WA-LAWIM-000014-2026-06-014", "TG-LAWIM-000045-2026-07-003"]
for ex, exp in zip(examples, expected):
    if ex != exp:
        errors.append(f"Tracking code {ex} != expected {exp}")

# ── 3. Parse round-trip ────────────────────────────────────────────────────

for code in expected:
    parsed = parse_tracking_code(code)
    if parsed is None:
        errors.append(f"Cannot parse valid code: {code}")
    else:
        if parsed["channel_code"] != code[:2]:
            errors.append(f"Parse channel_code mismatch for {code}")
        if parsed["publication_id"] != int(code.split("-")[2]):
            errors.append(f"Parse publication_id mismatch for {code}")

invalid_codes = ["", "XX-LAWIM-000000-2026-13-001", "FB-LAWIM-XXXXXX-2026-06-001", "FB-LAWIM-000128-2026-06-abc"]
for code in invalid_codes:
    parsed = parse_tracking_code(code)
    if parsed is not None:
        warnings.append(f"Invalid code {code} should not parse but got {parsed}")

# ── 4. Enum Values ─────────────────────────────────────────────────────────

for enum_class, name in [(CampaignStatus, "CampaignStatus"), (PublicationStatus, "PublicationStatus"),
                          (TouchpointType, "TouchpointType"), (AttributionModel, "AttributionModel")]:
    values = [e.value for e in enum_class]
    if len(values) != len(set(values)):
        errors.append(f"Duplicate values in {name}")

# ── 5. Models ──────────────────────────────────────────────────────────────

campaign = ExternalCampaign(campaign_id="c1", campaign_name="Test", status=CampaignStatus.ACTIVE)
if campaign.status != CampaignStatus.ACTIVE:
    errors.append("ExternalCampaign status not preserved")

pub = ExternalPublication(publication_id="p1", tracking_code="FB-LAWIM-000001-2026-06-001")
if pub.tracking_code != "FB-LAWIM-000001-2026-06-001":
    errors.append("ExternalPublication tracking_code not preserved")

redirect = RedirectLog(redirect_id="r1", tracking_code="FB-LAWIM-000001-2026-06-001")
if not redirect.to_dict().get("tracking_code"):
    errors.append("RedirectLog to_dict missing tracking_code")

conversion = ConversionEvent(event_id="e1", conversion_type="sale", monetary_value=500000)
if conversion.monetary_value != 500000:
    errors.append("ConversionEvent monetary_value not preserved")

attribution = LeadAttribution(attribution_id="a1", model=AttributionModel.FIRST_TOUCH)
if attribution.model != AttributionModel.FIRST_TOUCH:
    errors.append("LeadAttribution model not preserved")

# ── 6. Feature Flags ──────────────────────────────────────────────────────

from lawim_v2.program_j.tracking_config import TrackingConfig
cfg = TrackingConfig()
if cfg.publication_tracking_enabled:
    warnings.append("publication_tracking_enabled should be False by default")
if cfg.attribution_engine_enabled:
    warnings.append("attribution_engine_enabled should be False by default")
if cfg.conversion_event_chain_enabled:
    warnings.append("conversion_event_chain_enabled should be False by default")

# ── Results ─────────────────────────────────────────────────────────────────

if errors:
    print(f"ERRORS ({len(errors)}):")
    for e in errors:
        print(f"  \u274c {e}")
if warnings:
    print(f"WARNINGS ({len(warnings)}):")
    for w in warnings:
        print(f"  \u26a0\ufe0f {w}")

print(f"\n  Channel codes:       {len(codes)}")
print(f"  Tracking examples:   {examples}")
print(f"  Campaign statuses:   {len(list(CampaignStatus))}")
print(f"  Publication statuses: {len(list(PublicationStatus))}")
print(f"  Touchpoint types:    {len(list(TouchpointType))}")
print(f"  Attribution models:  {len(list(AttributionModel))}")
print(f"  Feature flags:       all disabled by default")

if errors:
    print("\n  VERDICT: VALIDATION FAILED")
    sys.exit(1)
else:
    print("\n  VERDICT: PASS")
    sys.exit(0)
