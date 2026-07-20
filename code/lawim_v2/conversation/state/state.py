from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class ConversationTurnContext:
    actor_id: int | str | None = None
    channel: str = ""
    external_conversation_id: str = ""
    message: str = ""
    language: str = "fr"
    previous_intent: str | None = None
    previous_question_field: str | None = None
    is_continuation: bool = False


@dataclass
class ConversationState:
    conversation_id: int | None = None
    actor_id: int | str | None = None
    channel: str = ""
    channel_session_id: str = ""
    language: str = "fr"
    current_intent: str | None = None
    intent_confidence: float = 0.0
    previous_intent: str | None = None
    transaction_type: str | None = None
    known_slots: dict[str, Any] = field(default_factory=dict)
    missing_slots: list[str] = field(default_factory=list)
    changed_slots: dict[str, Any] = field(default_factory=dict)
    last_user_message: str = ""
    last_lawim_message: str = ""
    last_question_key: str = ""
    last_action: str = ""
    qualification_status: str = "unqualified"
    qualification_step: int = 0
    selected_agent: str | None = None
    handover_status: str | None = None
    wizard_session_id: str | None = None
    created_at: str = ""
    updated_at: str = ""
    version: int = 1

    def to_dict(self) -> dict[str, Any]:
        return {
            "conversation_id": self.conversation_id,
            "actor_id": str(self.actor_id) if self.actor_id else None,
            "channel": self.channel,
            "channel_session_id": self.channel_session_id,
            "language": self.language,
            "current_intent": self.current_intent,
            "intent_confidence": self.intent_confidence,
            "previous_intent": self.previous_intent,
            "transaction_type": self.transaction_type,
            "known_slots": dict(self.known_slots),
            "missing_slots": list(self.missing_slots),
            "last_user_message": self.last_user_message,
            "last_lawim_message": self.last_lawim_message,
            "last_question_key": self.last_question_key,
            "qualification_status": self.qualification_status,
            "qualification_step": self.qualification_step,
            "selected_agent": self.selected_agent,
            "handover_status": self.handover_status,
            "wizard_session_id": self.wizard_session_id,
            "version": self.version,
        }


@dataclass
class ConversationStateUpdate:
    new_intent: str | None = None
    new_slots: dict[str, Any] = field(default_factory=dict)
    corrected_slots: dict[str, Any] = field(default_factory=dict)
    removed_slots: list[str] = field(default_factory=list)
    language_change: str | None = None
    reset_requested: bool = False


@dataclass
class ResponsePlan:
    speaker: str = "LAWIM AI"
    language: str = "fr"
    response_type: str = "ACKNOWLEDGE"
    acknowledgement_facts: dict[str, Any] = field(default_factory=dict)
    next_action: str = ""
    next_question_key: str = ""
    next_question_text: str = ""
    allowed_content: list[str] = field(default_factory=list)
    forbidden_content: list[str] = field(default_factory=list)
    maximum_questions: int = 1
    maximum_length: int = 500
    generated_by_ai: bool = True
    handover_required: bool = False
    handover_reason: str = ""
    handover_target_team: str = ""
    response_template: str = ""
    response_slots: dict[str, Any] = field(default_factory=dict)


@dataclass
class ConversationTurnDecision:
    intent: str | None = None
    known_slots: dict[str, Any] = field(default_factory=dict)
    missing_slots: list[str] = field(default_factory=list)
    qualification_ready: bool = False
    next_action: str = ""
    next_question_key: str = ""
    next_question_text: str = ""
    selected_agent: str | None = None
    handover_required: bool = False
    allowed_response_content: list[str] = field(default_factory=list)
    forbidden_response_content: list[str] = field(default_factory=list)
