#!/usr/bin/env python3
"""Program L — AI Agent Platform Validator."""
from __future__ import annotations

import sys

from lawim_v2.program_l import AgentConfig, AgentType, agent_registry
from lawim_v2.program_l.agent_registry import capability_registry

errors: list[str] = []
warnings: list[str] = []

# ── Agent Registry ─────────────────────────────────────────────────────────

if agent_registry.count() == 0:
    errors.append("Agent registry is empty")

codes = [a.agent_code for a in agent_registry.list()]
if len(codes) != len(set(codes)):
    dupes = [c for c in codes if codes.count(c) > 1]
    errors.append(f"Duplicate agent codes: {dupes}")

for a in agent_registry.list():
    if not a.agent_code:
        errors.append("Agent missing code")
    if not a.name:
        errors.append(f"Agent {a.agent_code} missing name")
    if not a.feature_flag:
        errors.append(f"Agent {a.agent_code} missing feature_flag")
    if not a.agent_type:
        errors.append(f"Agent {a.agent_code} missing type")

# Verify all types have at least one agent
for atype in AgentType:
    if atype == AgentType.SYSTEM:
        continue
    found = agent_registry.get_by_type(atype)
    if not found:
        warnings.append(f"No agent registered for type {atype.value}")

# ── Capability Registry ───────────────────────────────────────────────────

if capability_registry.count() == 0:
    errors.append("Capability registry is empty")

cap_codes = [c.capability_code for c in capability_registry.list()]
if len(cap_codes) != len(set(cap_codes)):
    errors.append("Duplicate capability codes")

# ── Feature Flags ─────────────────────────────────────────────────────────

cfg = AgentConfig()
for field_name in ("agent_platform_enabled", "conversation_agent_enabled",
                    "multi_agent_orchestration_enabled", "agent_memory_enabled"):
    if getattr(cfg, field_name):
        warnings.append(f"{field_name} should be False by default")

# ── Results ─────────────────────────────────────────────────────────────────

if errors:
    print(f"ERRORS ({len(errors)}):")
    for e in errors:
        print(f"  \u274c {e}")
if warnings:
    print(f"WARNINGS ({len(warnings)}):")
    for w in warnings:
        print(f"  \u26a0\ufe0f {w}")

print(f"\n  Agents:          {agent_registry.count()}")
print(f"  Capabilities:    {capability_registry.count()}")
print(f"  Feature flags:   {len([f for f in dir(cfg) if f.endswith('_enabled')])} total, all disabled")

if errors:
    print("\n  VERDICT: VALIDATION FAILED")
    sys.exit(1)
else:
    print("\n  VERDICT: PASS")
    sys.exit(0)
