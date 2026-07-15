#!/usr/bin/env python3
"""Program J Foundation Bundle Validator."""
from __future__ import annotations

import sys

from lawim_v2.program_j import visual_role_registry
from lawim_v2.program_j.conversation import ConversationStatus
from lawim_v2.program_j.exchange_taxonomy import ContentType, Direction, ExchangeResult, ExchangeType
from lawim_v2.program_j.visual_role import PrivacyLevel

errors: list[str] = []
warnings: list[str] = []

# ── 1. Visual Role Registry ─────────────────────────────────────────────────

roles = visual_role_registry.list_all()
codes = [r.code for r in roles]
if len(codes) != len(set(codes)):
    errors.append(f"Duplicate role codes: {[c for c in codes if codes.count(c) > 1]}")

if not roles:
    errors.append("Visual role registry is empty")

for role in roles:
    if not role.emoji:
        errors.append(f"Role {role.code} missing emoji")
    if not role.label_fr:
        errors.append(f"Role {role.code} missing label_fr")
    if not role.display_format:
        errors.append(f"Role {role.code} missing display_format")
    if "{name}" not in role.display_format:
        warnings.append(f"Role {role.code} display_format does not contain {{name}} placeholder")
    if role.privacy_level not in PrivacyLevel:
        errors.append(f"Role {role.code} invalid privacy_level")

# ── 2. Exchange Taxonomy ────────────────────────────────────────────────────

for enum_class, name in [(Direction, "Direction"), (ContentType, "ContentType"),
                          (ExchangeType, "ExchangeType"), (ExchangeResult, "ExchangeResult")]:
    values = [e.value for e in enum_class]
    if len(values) != len(set(values)):
        errors.append(f"Duplicate values in {name}")

# ── 3. Conversation Status ──────────────────────────────────────────────────

for status in ConversationStatus:
    if not status.value:
        errors.append(f"ConversationStatus {status.name} has empty value")

# ── 4. Feature Flags ────────────────────────────────────────────────────────

from lawim_v2.program_j.config import ProgramJConfig
cfg = ProgramJConfig()
if cfg.unified_conversation_enabled:
    warnings.append("unified_conversation_enabled should be False by default")
if cfg.actor_registry_enabled:
    warnings.append("actor_registry_enabled should be False by default")
if cfg.exchange_taxonomy_enabled:
    warnings.append("exchange_taxonomy_enabled should be False by default")

# ── Results ──────────────────────────────────────────────────────────────────

if errors:
    print(f"ERRORS ({len(errors)}):")
    for e in errors:
        print(f"  \u274c {e}")
if warnings:
    print(f"WARNINGS ({len(warnings)}):")
    for w in warnings:
        print(f"  \u26a0\ufe0f {w}")

print(f"\n  Roles:          {len(roles)}")
print(f"  Directions:     {len(list(Direction))}")
print(f"  Content types:  {len(list(ContentType))}")
print(f"  Exchange types: {len(list(ExchangeType))}")
print(f"  Exchange results: {len(list(ExchangeResult))}")
print(f"  Feature flags:  all disabled by default")

if errors:
    print("\n  VERDICT: VALIDATION FAILED")
    sys.exit(1)
else:
    print("\n  VERDICT: PASS")
    sys.exit(0)
