from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import uuid

from .safety import redact_sensitive_object, redact_sensitive_text, stable_hash


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(frozen=True, slots=True)
class LearningSample:
    sample_key: str
    intent: str
    conversation_key: str
    language: str
    question_examples: tuple[str, ...]
    proposed_answer: str
    source_count: int
    confidence: float
    risk_level: str
    recommended_action: str
    supporting_conversation_ids_anonymized: tuple[str, ...]
    status: str = "candidate"
    created_at: str = ""
    updated_at: str = ""

    def to_dict(self) -> dict[str, object]:
        return {
            "candidate_key": self.sample_key,
            "intent": self.intent,
            "conversation_key": self.conversation_key,
            "language": self.language,
            "question_examples": list(self.question_examples),
            "proposed_answer": self.proposed_answer,
            "source_count": self.source_count,
            "confidence": self.confidence,
            "risk_level": self.risk_level,
            "recommended_action": self.recommended_action,
            "supporting_conversation_ids_anonymized": list(self.supporting_conversation_ids_anonymized),
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class LearningEngine:
    def __init__(self, repository, config) -> None:
        self.repository = repository
        self.config = config

    def anonymize_message(self, text: str | None) -> str:
        return redact_sensitive_text(text)

    def anonymize_payload(self, payload: dict[str, object]) -> dict[str, object]:
        return redact_sensitive_object(payload)  # type: ignore[return-value]

    def maybe_create_candidate(self, *, request, response, reason: str) -> dict[str, object] | None:
        if not self.config.ai_learning_enabled:
            return None
        sample_key = f"lc-{uuid.uuid4().hex[:10]}"
        response_content = str(getattr(response, "content", "") or "").strip()
        proposed_answer = response_content or self.config.fallback_message
        confidence_score = float(getattr(response, "confidence_score", 0.0) or 0.0)
        candidate = LearningSample(
            sample_key=sample_key,
            intent=reason,
            conversation_key=request.conversation_key,
            language=request.language,
            question_examples=(redact_sensitive_text(request.text),),
            proposed_answer=proposed_answer,
            source_count=1,
            confidence=max(0.35, confidence_score),
            risk_level="low" if bool(getattr(response, "safe", True)) else "medium",
            recommended_action="review_required" if self.config.ai_learning_requires_human_approval else "approved",
            supporting_conversation_ids_anonymized=(stable_hash(request.conversation_key),),
            created_at=_utcnow(),
            updated_at=_utcnow(),
        )
        row = self.repository.create_ai_learning_candidate(**candidate.to_dict())
        return row
