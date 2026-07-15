from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# ── Rule Conflict Resolver ─────────────────────────────────────────────────


class ConflictType(str, Enum):
    OVERLAP = "OVERLAP"
    CONTRADICTION = "CONTRADICTION"
    CIRCULAR = "CIRCULAR"


@dataclass
class RuleConflictResolver:
    def detect(self, rules: list[dict[str, Any]]) -> list[dict[str, Any]]:
        conflicts: list[dict[str, Any]] = []
        seen: dict[str, list[str]] = {}
        for rule in rules:
            rid = rule.get("id", "")
            domain = rule.get("domain", "")
            if rid in seen:
                conflicts.append({
                    "type": ConflictType.OVERLAP.value, "rule_id": rid,
                    "domains": [seen[rid], domain],
                    "message": f"Rule {rid} appears in multiple domains",
                })
            seen[rid] = domain
        return conflicts

    def resolve(self, conflicts: list[dict[str, Any]]) -> list[dict[str, str]]:
        return [{"rule_id": c["rule_id"], "resolution": "use_highest_priority",
                 "reason": "Resolved by domain priority ordering"}
                for c in conflicts]


def resolve_rule_conflict(rules: list[dict[str, Any]]) -> list[dict[str, str]]:
    return RuleConflictResolver().resolve(RuleConflictResolver().detect(rules))


# ── SLA Registry ───────────────────────────────────────────────────────────


@dataclass
class SLARegistryEntry:
    entity_type: str = ""
    state: str = ""
    threshold_ms: int = 0
    severity: str = "LOW"
    escalation_chain: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {"entity_type": self.entity_type, "state": self.state,
                "threshold_ms": self.threshold_ms, "severity": self.severity}


# ── NBA Priority Matrix ────────────────────────────────────────────────────


@dataclass
class NBAPriorityMatrix:
    state: str = ""
    priority_domain: str = ""
    next_action: str = ""

    def resolve(self, state: str, priority_domain: str) -> str:
        matrix = {
            ("qualifying", "response"): "ask_next_question",
            ("searching", "results"): "present_results",
            ("matching", "selection"): "propose_match",
            ("visit", "scheduling"): "schedule_visit",
            ("negotiation", "commercial"): "prepare_offer",
            ("closing", "transaction"): "initiate_payment",
        }
        return matrix.get((state, priority_domain), "monitor")


# ── Scoring Harmonizer ─────────────────────────────────────────────────────


@dataclass
class ScoringHarmonizer:
    def v1_to_v5(self, score_v1: float) -> float:
        """Convert V1 (0-100) score to V5 (0.0-1.0)"""
        return max(0.0, min(1.0, score_v1 / 100.0))

    def v5_to_v1(self, score_v5: float) -> float:
        """Convert V5 (0.0-1.0) score to V1 (0-100)"""
        return max(0.0, min(100.0, score_v5 * 100.0))


# ── Memory Retention Policy ────────────────────────────────────────────────


@dataclass
class MemoryRetentionPolicy:
    retention_days: int = 365
    policy_source: str = "code"

    def apply(self, created_at: str) -> bool:
        from datetime import datetime, timezone, timedelta
        try:
            dt = datetime.fromisoformat(created_at)
            age = datetime.now(timezone.utc) - dt
            return age.days < self.retention_days
        except (ValueError, TypeError):
            return True


# ── Geo Hierarchy Policy ───────────────────────────────────────────────────


@dataclass
class GeoHierarchyPolicy:
    implemented_levels: int = 8
    gold_levels: int = 9

    def is_compatible(self) -> bool:
        return self.implemented_levels == self.gold_levels

    def gap(self) -> int:
        return self.gold_levels - self.implemented_levels
