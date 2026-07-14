from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .states import ConversationState, STATE_TRANSITIONS
from .facts import FactCollection
from .errors import StateError


@dataclass
class Conversation:
    conversation_id: int | None = None
    user_id: int | None = None
    channel_identity_id: int | None = None
    channel: str = ""
    state: ConversationState = ConversationState.NEW
    project_id: int | None = None
    dossier_id: int | None = None
    facts: FactCollection = field(default_factory=FactCollection)
    known_fields: set[str] = field(default_factory=set)
    expected_input: str | None = None
    last_question_field: str | None = None
    last_question_text: str | None = None
    question_repeat_count: int = 0
    last_validated_fact: str | None = None
    last_transition: str | None = None
    loop_score: int = 0
    loop_detected: bool = False
    human_handover_requested: bool = False
    created_at: str | None = None
    updated_at: str | None = None

    def apply_transition(self, event: str) -> tuple[bool, str | None]:
        for transition in STATE_TRANSITIONS:
            if transition.source == self.state and transition.event == event:
                old_state = self.state
                self.state = transition.destination
                self.last_transition = transition.audit_event
                self.updated_at = datetime.utcnow().isoformat()
                return True, transition.audit_event
        return False, None

    def can_transition(self, event: str) -> bool:
        return any(t.source == self.state and t.event == event for t in STATE_TRANSITIONS)

    def gets_expected_next_events(self) -> list[str]:
        return [t.event for t in STATE_TRANSITIONS if t.source == self.state]

    def mark_field_known(self, field: str) -> None:
        self.known_fields.add(field)
        self.last_validated_fact = field

    def is_field_known(self, field: str) -> bool:
        return field in self.known_fields or self.facts.has_field(field)

    def to_dict(self) -> dict[str, Any]:
        return {
            "conversation_id": self.conversation_id,
            "user_id": self.user_id,
            "channel": self.channel,
            "state": self.state.value,
            "project_id": self.project_id,
            "dossier_id": self.dossier_id,
            "facts": self.facts.to_dict(),
            "known_fields": list(self.known_fields),
            "expected_input": self.expected_input,
            "loop_detected": self.loop_detected,
            "loop_score": self.loop_score,
            "human_handover_requested": self.human_handover_requested,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
