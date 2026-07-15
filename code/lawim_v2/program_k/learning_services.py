from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from .learning_models import (
    FeedbackItem,
    FeedbackOrigin,
    FeedbackTarget,
    LearningEvent,
    LearningEventSource,
    LearningEventType,
    OutcomeResult,
    OutcomeStatus,
)
from .learning_registry import learning_event_registry, outcome_registry


class LearningEventService:
    def record_h_event(self, event_type: LearningEventType, actor_id: str = "",
                        conversation_id: str = "", payload: dict[str, Any] | None = None) -> LearningEvent:
        event = LearningEvent(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            source=LearningEventSource.PROGRAM_H,
            actor_id=actor_id,
            conversation_id=conversation_id,
            payload=payload or {},
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        return learning_event_registry.record(event)

    def record_j_event(self, event_type: LearningEventType, actor_id: str = "",
                        conversation_id: str = "", channel: str = "",
                        payload: dict[str, Any] | None = None) -> LearningEvent:
        event = LearningEvent(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            source=LearningEventSource.PROGRAM_J,
            actor_id=actor_id,
            conversation_id=conversation_id,
            channel=channel,
            payload=payload or {},
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        return learning_event_registry.record(event)

    def record_outcome_event(self, event_type: LearningEventType = LearningEventType.OUTCOME_RECORDED,
                              actor_id: str = "", payload: dict[str, Any] | None = None) -> LearningEvent:
        event = LearningEvent(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            source=LearningEventSource.PROGRAM_J,
            actor_id=actor_id,
            payload=payload or {},
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        return learning_event_registry.record(event)

    def get_stats(self) -> dict[str, Any]:
        return {
            "total_events": learning_event_registry.count(),
            "by_source": learning_event_registry.count_by_source(),
            "event_types_available": len(list(LearningEventType)),
        }


class OutcomeRegistryService:
    def register_outcome(self, outcome_type: str, status: OutcomeStatus,
                          actor_id: str = "", conversation_id: str = "",
                          satisfaction_score: float = 0.0,
                          monetary_value: float = 0.0) -> OutcomeResult:
        outcome = OutcomeResult(
            outcome_id=str(uuid.uuid4()),
            outcome_type=outcome_type,
            status=status,
            actor_id=actor_id,
            conversation_id=conversation_id,
            satisfaction_score=satisfaction_score,
            monetary_value=monetary_value,
            occurred_at=datetime.now(timezone.utc).isoformat(),
        )
        return outcome_registry.register(outcome)

    def register_qualification_outcome(self, success: bool, actor_id: str = "",
                                        conversation_id: str = "") -> OutcomeResult:
        return self.register_outcome(
            "qualification",
            OutcomeStatus.SUCCESS if success else OutcomeStatus.FAILURE,
            actor_id=actor_id,
            conversation_id=conversation_id,
        )

    def register_matching_outcome(self, success: bool, actor_id: str = "",
                                   conversation_id: str = "") -> OutcomeResult:
        return self.register_outcome(
            "matching",
            OutcomeStatus.SUCCESS if success else OutcomeStatus.FAILURE,
            actor_id=actor_id,
            conversation_id=conversation_id,
        )

    def register_visit_outcome(self, completed: bool, actor_id: str = "",
                                conversation_id: str = "") -> OutcomeResult:
        return self.register_outcome(
            "visit",
            OutcomeStatus.SUCCESS if completed else OutcomeStatus.FAILURE,
            actor_id=actor_id,
            conversation_id=conversation_id,
        )

    def register_transaction_outcome(self, completed: bool, monetary_value: float = 0.0,
                                      actor_id: str = "") -> OutcomeResult:
        return self.register_outcome(
            "transaction",
            OutcomeStatus.SUCCESS if completed else OutcomeStatus.FAILURE,
            actor_id=actor_id,
            monetary_value=monetary_value,
        )

    def register_payment_outcome(self, confirmed: bool, monetary_value: float = 0.0,
                                  actor_id: str = "") -> OutcomeResult:
        return self.register_outcome(
            "payment",
            OutcomeStatus.SUCCESS if confirmed else OutcomeStatus.FAILURE,
            actor_id=actor_id,
            monetary_value=monetary_value,
        )

    def register_conversation_outcome(self, status: OutcomeStatus, actor_id: str = "",
                                       conversation_id: str = "",
                                       satisfaction_score: float = 0.0) -> OutcomeResult:
        return self.register_outcome(
            "conversation",
            status, actor_id=actor_id,
            conversation_id=conversation_id,
            satisfaction_score=satisfaction_score,
        )

    def get_success_rate(self, outcome_type: str) -> float:
        return outcome_registry.success_rate(outcome_type)

    def get_stats(self) -> dict[str, Any]:
        return {
            "total_outcomes": outcome_registry.count(),
            "successes": outcome_registry.count(OutcomeStatus.SUCCESS),
            "failures": outcome_registry.count(OutcomeStatus.FAILURE),
            "abandoned": outcome_registry.count(OutcomeStatus.ABANDONED),
        }


class FeedbackService:
    def __init__(self) -> None:
        self._feedbacks: list[FeedbackItem] = []

    def submit(self, origin: FeedbackOrigin, target: FeedbackTarget,
                target_id: str, score: float, actor_id: str = "",
                comment: str = "", confidence: float = 1.0) -> FeedbackItem:
        item = FeedbackItem(
            feedback_id=str(uuid.uuid4()),
            origin=origin,
            target=target,
            target_id=target_id,
            actor_id=actor_id,
            score=score,
            comment=comment,
            confidence=confidence,
            occurred_at=datetime.now(timezone.utc).isoformat(),
        )
        self._feedbacks.append(item)
        return item

    def submit_user_feedback(self, target: FeedbackTarget, target_id: str,
                              score: float, comment: str = "") -> FeedbackItem:
        return self.submit(FeedbackOrigin.USER, target, target_id, score,
                           comment=comment)

    def submit_satisfaction(self, score: float, conversation_id: str = "") -> FeedbackItem:
        return self.submit(FeedbackOrigin.SATISFACTION_SURVEY,
                           FeedbackTarget.CONVERSATION, conversation_id, score)

    def submit_matching_feedback(self, score: float, target_id: str,
                                  actor_id: str = "") -> FeedbackItem:
        return self.submit(FeedbackOrigin.MATCHING, FeedbackTarget.MATCHING_RESULT,
                           target_id, score, actor_id=actor_id)

    def get_by_target(self, target: FeedbackTarget, target_id: str) -> list[FeedbackItem]:
        return [f for f in self._feedbacks
                if f.target == target and f.target_id == target_id]

    def average_score(self, target: FeedbackTarget, target_id: str) -> float:
        items = self.get_by_target(target, target_id)
        if not items:
            return 0.0
        return sum(f.score for f in items) / len(items)

    def get_all(self) -> list[FeedbackItem]:
        return list(self._feedbacks)

    def count(self) -> int:
        return len(self._feedbacks)


class LearningValidationService:
    def validate_event(self, event: LearningEvent) -> list[str]:
        errors: list[str] = []
        if not event.event_type:
            errors.append("event_type is required")
        if not event.source:
            errors.append("source is required")
        if not isinstance(event.event_type, LearningEventType):
            errors.append(f"Invalid event_type: {event.event_type}")
        return errors

    def validate_outcome(self, outcome: OutcomeResult) -> list[str]:
        errors: list[str] = []
        if not outcome.outcome_type:
            errors.append("outcome_type is required")
        if not isinstance(outcome.status, OutcomeStatus):
            errors.append(f"Invalid status: {outcome.status}")
        return errors

    def validate_feedback(self, feedback: FeedbackItem) -> list[str]:
        errors: list[str] = []
        if feedback.score < feedback.min_score or feedback.score > feedback.max_score:
            errors.append(f"Score {feedback.score} out of range [{feedback.min_score}, {feedback.max_score}]")
        if not feedback.target:
            errors.append("target is required")
        return errors
