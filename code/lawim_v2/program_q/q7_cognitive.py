from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


# ── Explainability Guardrail ────────────────────────────────────────────────


@dataclass
class ExplainabilityGuardrail:
    decision_id: str = ""
    rule_ids: list[str] = field(default_factory=list)
    input_snapshot: dict[str, Any] = field(default_factory=dict)
    reasoning: str = ""
    confidence: float = 0.0
    alternatives: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {"decision_id": self.decision_id, "reasoning": self.reasoning,
                "confidence": self.confidence, "rule_count": len(self.rule_ids)}


def explain_decision(decision_id: str, rules: list[str], reasoning: str,
                      confidence: float = 1.0) -> ExplainabilityGuardrail:
    return ExplainabilityGuardrail(
        decision_id=decision_id, rule_ids=rules, reasoning=reasoning, confidence=confidence)


# ── State Management Guard ──────────────────────────────────────────────────


@dataclass
class StateManagementGuard:
    allowed_transitions: dict[str, list[str]] = field(default_factory=dict)
    current_state: str = ""

    def can_transition(self, target: str) -> bool:
        allowed = self.allowed_transitions.get(self.current_state, [])
        return target in allowed

    def transition(self, target: str) -> bool:
        if self.can_transition(target):
            self.current_state = target
            return True
        return False


def validate_state_transition(current: str, target: str,
                               transitions: dict[str, list[str]]) -> bool:
    allowed = transitions.get(current, [])
    return target in allowed


# ── Cognitive Decision ──────────────────────────────────────────────────────


@dataclass
class CognitiveDecision:
    decision_id: str = ""
    decision_type: str = ""
    actor_id: str = ""
    context: dict[str, Any] = field(default_factory=dict)
    rationale: str = ""
    risk_level: str = "LOW"
    requires_approval: bool = False
    approved_by: str = ""
    created_at: str = ""
    guardrail: ExplainabilityGuardrail | None = None

    def to_dict(self) -> dict[str, Any]:
        return {"decision_id": self.decision_id, "decision_type": self.decision_type,
                "risk_level": self.risk_level, "requires_approval": self.requires_approval}


# ── Permanent Conversation ──────────────────────────────────────────────────


@dataclass
class PermanentConversation:
    conversation_id: str = ""
    retention_days: int = 365
    summary: str = ""
    extract_count: int = 0
    last_activity: str = ""
    status: str = "ACTIVE"

    def is_expired(self) -> bool:
        try:
            from datetime import datetime, timezone, timedelta
            dt = datetime.fromisoformat(self.last_activity)
            age = datetime.now(timezone.utc) - dt
            return age.days > self.retention_days
        except (ValueError, TypeError):
            return False


# ── Workflow Preview ────────────────────────────────────────────────────────


@dataclass
class WorkflowPreview:
    workflow_id: str = ""
    name: str = ""
    description: str = ""
    steps: list[dict[str, Any]] = field(default_factory=list)
    safety_gates: list[str] = field(default_factory=list)
    requires_approval: bool = True
    status: str = "PREVIEW"

    def to_dict(self) -> dict[str, Any]:
        return {"workflow_id": self.workflow_id, "name": self.name,
                "step_count": len(self.steps), "requires_approval": self.requires_approval}


# ── Cognitive Audit Record ──────────────────────────────────────────────────


@dataclass
class CognitiveAuditRecord:
    audit_id: str = ""
    decision_id: str = ""
    actor_id: str = ""
    action: str = ""
    previous_state: str = ""
    new_state: str = ""
    risk_level: str = "LOW"
    timestamp: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {"audit_id": self.audit_id, "actor_id": self.actor_id,
                "action": self.action, "risk_level": self.risk_level}
