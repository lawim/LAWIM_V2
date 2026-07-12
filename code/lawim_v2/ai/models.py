from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class RoutingDecision:
    request_id: str
    conversation_key: str
    complexity: str
    selected_provider: str
    chain: tuple[str, ...]
    reason: str
    fallback_used: bool
    created_at: str

    def to_dict(self) -> dict[str, object]:
        return {
            "request_id": self.request_id,
            "conversation_key": self.conversation_key,
            "complexity": self.complexity,
            "selected_provider": self.selected_provider,
            "chain": list(self.chain),
            "reason": self.reason,
            "fallback_used": self.fallback_used,
            "created_at": self.created_at,
        }


@dataclass(frozen=True, slots=True)
class FallbackResolution:
    provider: str
    model: str
    content: str
    used_generic: bool
    entry_key: str | None = None
    intent: str | None = None
    confidence: float = 0.0
    metadata: dict[str, object] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        payload = {
            "provider": self.provider,
            "model": self.model,
            "content": self.content,
            "used_generic": self.used_generic,
            "entry_key": self.entry_key,
            "intent": self.intent,
            "confidence": self.confidence,
            "metadata": self.metadata,
        }
        return {key: value for key, value in payload.items() if value is not None}


@dataclass(frozen=True, slots=True)
class LearningCandidateProposal:
    candidate_key: str
    intent: str
    question_examples: tuple[str, ...]
    proposed_answer: str
    source_count: int
    confidence: float
    risk_level: str
    language: str
    recommended_action: str
    supporting_conversation_ids_anonymized: tuple[str, ...]
    status: str = "candidate"
    created_at: str = ""
    updated_at: str = ""

    def to_dict(self) -> dict[str, object]:
        return {
            "candidate_key": self.candidate_key,
            "intent": self.intent,
            "question_examples": list(self.question_examples),
            "proposed_answer": self.proposed_answer,
            "source_count": self.source_count,
            "confidence": self.confidence,
            "risk_level": self.risk_level,
            "language": self.language,
            "recommended_action": self.recommended_action,
            "supporting_conversation_ids_anonymized": list(self.supporting_conversation_ids_anonymized),
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
