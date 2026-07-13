from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from ..ai import AIMessage, AIRequest
from ..ai.orchestrator import OrchestrationOutcome


@dataclass(slots=True)
class ConversationTurnPlan:
    channel: str
    text: str
    language: str
    normalized: dict[str, Any]
    message_row: dict[str, Any]
    conversation_key: str
    external_chat_id: str
    external_user_id: str
    message_id: str
    project_id: int | None = None
    thread_id: int | None = None
    contact_id: int | None = None
    organization_id: int | None = None
    contact: dict[str, Any] | None = None
    thread: dict[str, Any] | None = None
    project: dict[str, Any] | None = None
    analysis: dict[str, Any] = field(default_factory=dict)
    progression: dict[str, Any] = field(default_factory=dict)
    memory_summary: dict[str, Any] = field(default_factory=dict)
    context_messages: tuple[AIMessage, ...] = ()
    direct_reply: str | None = None
    reply_kind: str = "ai"
    route_reason: str = "ai"
    route_metadata: dict[str, Any] = field(default_factory=dict)
    actor: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["context_messages"] = [message.to_dict() for message in self.context_messages]
        return payload


@dataclass(slots=True)
class ConversationTurnResult:
    plan: ConversationTurnPlan
    request: AIRequest
    outcome: OrchestrationOutcome
    final_text: str
    response_quality: dict[str, Any]
    response_kind: str
    response_source: str
    fallback_used: bool
    should_escalate: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "plan": self.plan.to_dict(),
            "request": asdict(self.request),
            "outcome": self.outcome.to_dict(),
            "final_text": self.final_text,
            "response_quality": dict(self.response_quality),
            "response_kind": self.response_kind,
            "response_source": self.response_source,
            "fallback_used": self.fallback_used,
            "should_escalate": self.should_escalate,
            "metadata": dict(self.metadata),
        }
