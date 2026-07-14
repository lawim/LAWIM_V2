from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .states import ConversationState


@dataclass
class ConversationDecision:
    decision_id: str = ""
    conversation_id: int | None = None
    user_id: int | None = None
    channel_identity_id: int | None = None
    channel: str = ""
    project_id: int | None = None
    dossier_id: int | None = None
    raw_message: str = ""
    normalized_message: str = ""
    state_before: ConversationState | None = None
    state_after: ConversationState | None = None
    intent_candidates: list[dict[str, Any]] = field(default_factory=list)
    selected_intent: str | None = None
    intent_confidence: float = 0.0
    transaction_type: str | None = None
    property_type: str | None = None
    known_facts: dict[str, Any] = field(default_factory=dict)
    new_facts: list[dict[str, Any]] = field(default_factory=list)
    ambiguous_facts: list[dict[str, Any]] = field(default_factory=list)
    conflicting_facts: list[dict[str, Any]] = field(default_factory=list)
    missing_required_facts: list[str] = field(default_factory=list)
    expected_input: str | None = None
    business_goal: str | None = None
    action: str | None = None
    action_parameters: dict[str, Any] = field(default_factory=dict)
    action_status: str | None = None
    allowed_capabilities: list[str] = field(default_factory=list)
    forbidden_capabilities: list[str] = field(default_factory=list)
    response_type: str | None = None
    response_constraints: list[str] = field(default_factory=list)
    requires_clarification: bool = False
    requires_human: bool = False
    loop_detected: bool = False
    loop_score: int = 0
    created_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "conversation_id": self.conversation_id,
            "user_id": self.user_id,
            "channel": self.channel,
            "project_id": self.project_id,
            "dossier_id": self.dossier_id,
            "normalized_message": self.normalized_message,
            "state_before": self.state_before.value if self.state_before else None,
            "state_after": self.state_after.value if self.state_after else None,
            "selected_intent": self.selected_intent,
            "intent_confidence": self.intent_confidence,
            "transaction_type": self.transaction_type,
            "property_type": self.property_type,
            "known_facts": self.known_facts,
            "new_facts": self.new_facts,
            "ambiguous_facts": self.ambiguous_facts,
            "conflicting_facts": self.conflicting_facts,
            "missing_required_facts": self.missing_required_facts,
            "expected_input": self.expected_input,
            "action": self.action,
            "action_parameters": self.action_parameters,
            "action_status": self.action_status,
            "requires_clarification": self.requires_clarification,
            "requires_human": self.requires_human,
            "loop_detected": self.loop_detected,
            "loop_score": self.loop_score,
            "created_at": self.created_at,
        }
