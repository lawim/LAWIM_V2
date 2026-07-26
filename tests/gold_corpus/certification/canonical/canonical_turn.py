"""Canonical turn model — format-independent conversation turn representation."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class CanonicalValue:
    value: Any = None
    source: str = ""
    source_type: str = ""
    inferred: bool = False
    defaulted: bool = False
    confidence: float = 1.0


@dataclass
class CanonicalTurn:
    conversation_id: str = ""
    turn_index: int = 0
    intent: CanonicalValue = field(default_factory=CanonicalValue)
    facts: Dict[str, CanonicalValue] = field(default_factory=dict)
    phase: CanonicalValue = field(default_factory=CanonicalValue)
    pending_user_action: CanonicalValue = field(default_factory=CanonicalValue)
    conversation_language: CanonicalValue = field(default_factory=CanonicalValue)
    effective_language: CanonicalValue = field(default_factory=CanonicalValue)
    question_semantic_type: CanonicalValue = field(default_factory=CanonicalValue)
    business_action: CanonicalValue = field(default_factory=CanonicalValue)
    business_object_count: int = 0
    business_object_id: Optional[str] = None
    status: str = "unknown"

    def to_dict(self) -> Dict[str, Any]:
        def _serialize(cv):
            if isinstance(cv, CanonicalValue):
                return {"value": cv.value, "source": cv.source,
                        "source_type": cv.source_type, "inferred": cv.inferred,
                        "defaulted": cv.defaulted, "confidence": cv.confidence}
            return cv
        return {
            "conversation_id": self.conversation_id,
            "turn_index": self.turn_index,
            "intent": _serialize(self.intent),
            "facts": {k: _serialize(v) for k, v in self.facts.items()},
            "phase": _serialize(self.phase),
            "pending_user_action": _serialize(self.pending_user_action),
            "conversation_language": _serialize(self.conversation_language),
            "effective_language": _serialize(self.effective_language),
            "question_semantic_type": _serialize(self.question_semantic_type),
            "business_action": _serialize(self.business_action),
            "business_object_count": self.business_object_count,
            "business_object_id": self.business_object_id,
            "status": self.status,
        }
