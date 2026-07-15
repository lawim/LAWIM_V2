from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── Learning Event Types (from H and J programs) ──────────────────────────


class LearningEventSource(str, Enum):
    PROGRAM_H = "PROGRAM_H"
    PROGRAM_J = "PROGRAM_J"
    AI_SYSTEM = "AI_SYSTEM"
    USER_FEEDBACK = "USER_FEEDBACK"
    CRM = "CRM"
    EXTERNAL = "EXTERNAL"


class LearningEventType(str, Enum):
    # H Program events
    H_QUALIFICATION_STARTED = "H_QUALIFICATION_STARTED"
    H_QUALIFICATION_COMPLETED = "H_QUALIFICATION_COMPLETED"
    H_QUALIFICATION_ABANDONED = "H_QUALIFICATION_ABANDONED"
    H_QUALIFICATION_ESCALATED = "H_QUALIFICATION_ESCALATED"
    H_READINESS_EVALUATED = "H_READINESS_EVALUATED"
    H_NEXT_QUESTION_RESOLVED = "H_NEXT_QUESTION_RESOLVED"

    # J2 Conversation events
    J_CONVERSATION_STARTED = "J_CONVERSATION_STARTED"
    J_CONVERSATION_MESSAGE = "J_CONVERSATION_MESSAGE"
    J_CONVERSATION_CLOSED = "J_CONVERSATION_CLOSED"
    J_CHANNEL_SESSION_ACTIVE = "J_CHANNEL_SESSION_ACTIVE"

    # J3/J4 Tracking & Attribution events
    J_PUBLICATION_CREATED = "J_PUBLICATION_CREATED"
    J_REDIRECT_RECORDED = "J_REDIRECT_RECORDED"
    J_TOUCHPOINT_RECORDED = "J_TOUCHPOINT_RECORDED"
    J_ATTRIBUTION_CALCULATED = "J_ATTRIBUTION_CALCULATED"

    # J5 Exchange Taxonomy events
    J_EXCHANGE_INBOUND = "J_EXCHANGE_INBOUND"
    J_EXCHANGE_OUTBOUND = "J_EXCHANGE_OUTBOUND"

    # J6/J8 Conversion events
    J_CONVERSION_RECORDED = "J_CONVERSION_RECORDED"
    J_MATCHING_CREATED = "J_MATCHING_CREATED"
    J_VISIT_REQUESTED = "J_VISIT_REQUESTED"
    J_PAYMENT_INITIATED = "J_PAYMENT_INITIATED"
    J_PAYMENT_CONFIRMED = "J_PAYMENT_CONFIRMED"

    # Outcome events
    OUTCOME_RECORDED = "OUTCOME_RECORDED"
    FEEDBACK_RECEIVED = "FEEDBACK_RECEIVED"
    FEEDBACK_AGGREGATED = "FEEDBACK_AGGREGATED"


# ── Learning Event (canonical, immutable) ────────────────────────────────


@dataclass
class LearningEvent:
    event_id: str = ""
    event_type: LearningEventType = LearningEventType.J_CONVERSATION_STARTED
    source: LearningEventSource = LearningEventSource.PROGRAM_J
    actor_id: str = ""
    conversation_id: str = ""
    property_id: int | None = None
    transaction_id: str = ""
    channel: str = ""
    correlation_id: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    event_version: str = "1.0"
    confidence: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "source": self.source.value,
            "actor_id": self.actor_id,
            "conversation_id": self.conversation_id,
            "channel": self.channel,
            "correlation_id": self.correlation_id,
            "event_version": self.event_version,
            "confidence": self.confidence,
            "timestamp": self.timestamp,
        }

    def anonymize(self) -> LearningEvent:
        import copy
        e = copy.copy(self)
        e.metadata = {}
        e.payload = {k: v for k, v in self.payload.items()
                     if k not in ("phone", "email", "raw_text", "full_name")}
        return e


# ── Outcome Registry ─────────────────────────────────────────────────────


class OutcomeStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    ABANDONED = "ABANDONED"
    PENDING = "PENDING"
    UNKNOWN = "UNKNOWN"


@dataclass
class OutcomeResult:
    outcome_id: str = ""
    outcome_type: str = ""
    status: OutcomeStatus = OutcomeStatus.UNKNOWN
    event_id: str = ""
    actor_id: str = ""
    conversation_id: str = ""
    channel: str = ""
    property_id: int | None = None
    transaction_id: str = ""
    payment_id: str = ""
    tracking_code: str = ""
    campaign_id: str = ""
    publication_id: str = ""
    satisfaction_score: float = 0.0
    monetary_value: float = 0.0
    currency: str = "XAF"
    occurred_at: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    event_version: str = "1.0"

    def to_dict(self) -> dict[str, Any]:
        return {
            "outcome_id": self.outcome_id,
            "outcome_type": self.outcome_type,
            "status": self.status.value,
            "event_id": self.event_id,
            "actor_id": self.actor_id,
            "conversation_id": self.conversation_id,
            "satisfaction_score": self.satisfaction_score,
            "monetary_value": self.monetary_value,
            "currency": self.currency,
        }


# ── Feedback System ──────────────────────────────────────────────────────


class FeedbackOrigin(str, Enum):
    USER = "USER"
    AGENT = "AGENT"
    ADMIN = "ADMIN"
    BUSINESS_EVENT = "BUSINESS_EVENT"
    PAYMENT = "PAYMENT"
    TRANSACTION = "TRANSACTION"
    MATCHING = "MATCHING"
    VISIT = "VISIT"
    SATISFACTION_SURVEY = "SATISFACTION_SURVEY"


class FeedbackTarget(str, Enum):
    AI_RESPONSE = "AI_RESPONSE"
    MATCHING_RESULT = "MATCHING_RESULT"
    AGENT_PERFORMANCE = "AGENT_PERFORMANCE"
    PROPERTY = "PROPERTY"
    SERVICE = "SERVICE"
    CONVERSATION = "CONVERSATION"
    RECOMMENDATION = "RECOMMENDATION"
    PUBLICATION = "PUBLICATION"
    CAMPAIGN = "CAMPAIGN"


@dataclass
class FeedbackItem:
    feedback_id: str = ""
    origin: FeedbackOrigin = FeedbackOrigin.USER
    target: FeedbackTarget = FeedbackTarget.AI_RESPONSE
    target_id: str = ""
    actor_id: str = ""
    score: float = 0.0
    min_score: float = 0.0
    max_score: float = 10.0
    comment: str = ""
    occurred_at: str = ""
    confidence: float = 1.0
    source_event_id: str = ""
    justification: str = ""
    feedback_version: str = "1.0"
    metadata: dict[str, Any] = field(default_factory=dict)

    def normalized_score(self) -> float:
        if self.max_score == self.min_score:
            return 0.5
        return (self.score - self.min_score) / (self.max_score - self.min_score)

    def to_dict(self) -> dict[str, Any]:
        return {
            "feedback_id": self.feedback_id,
            "origin": self.origin.value,
            "target": self.target.value,
            "target_id": self.target_id,
            "actor_id": self.actor_id,
            "score": self.score,
            "normalized_score": round(self.normalized_score(), 4),
            "occurred_at": self.occurred_at,
            "confidence": self.confidence,
            "feedback_version": self.feedback_version,
        }
