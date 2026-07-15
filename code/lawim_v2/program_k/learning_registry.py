from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from .learning_models import (
    FeedbackItem,
    LearningEvent,
    LearningEventSource,
    LearningEventType,
    OutcomeResult,
    OutcomeStatus,
)


class LearningEventRegistry:
    def __init__(self) -> None:
        self._events: list[LearningEvent] = []

    def record(self, event: LearningEvent) -> LearningEvent:
        if not event.event_id:
            event.event_id = str(uuid.uuid4())
        if not event.timestamp:
            event.timestamp = datetime.now(timezone.utc).isoformat()
        self._events.append(event)
        return event

    def get_by_id(self, event_id: str) -> LearningEvent | None:
        for e in self._events:
            if e.event_id == event_id:
                return e
        return None

    def query(self, event_type: LearningEventType | None = None,
               source: LearningEventSource | None = None,
               actor_id: str | None = None,
               conversation_id: str | None = None,
               limit: int = 100) -> list[LearningEvent]:
        results = list(self._events)
        if event_type is not None:
            results = [e for e in results if e.event_type == event_type]
        if source is not None:
            results = [e for e in results if e.source == source]
        if actor_id is not None:
            results = [e for e in results if e.actor_id == actor_id]
        if conversation_id is not None:
            results = [e for e in results if e.conversation_id == conversation_id]
        return results[-limit:]

    def count(self, event_type: LearningEventType | None = None) -> int:
        if event_type is None:
            return len(self._events)
        return sum(1 for e in self._events if e.event_type == event_type)

    def count_by_source(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for e in self._events:
            s = e.source.value
            counts[s] = counts.get(s, 0) + 1
        return counts

    def clear(self) -> None:
        self._events.clear()


class OutcomeRegistry:
    def __init__(self) -> None:
        self._outcomes: list[OutcomeResult] = []

    def register(self, outcome: OutcomeResult) -> OutcomeResult:
        if not outcome.outcome_id:
            outcome.outcome_id = str(uuid.uuid4())
        if not outcome.occurred_at:
            outcome.occurred_at = datetime.now(timezone.utc).isoformat()
        self._outcomes.append(outcome)
        return outcome

    def get_by_id(self, outcome_id: str) -> OutcomeResult | None:
        for o in self._outcomes:
            if o.outcome_id == outcome_id:
                return o
        return None

    def query(self, outcome_type: str | None = None,
               status: OutcomeStatus | None = None,
               actor_id: str | None = None,
               conversation_id: str | None = None,
               limit: int = 100) -> list[OutcomeResult]:
        results = list(self._outcomes)
        if outcome_type is not None:
            results = [o for o in results if o.outcome_type == outcome_type]
        if status is not None:
            results = [o for o in results if o.status == status]
        if actor_id is not None:
            results = [o for o in results if o.actor_id == actor_id]
        if conversation_id is not None:
            results = [o for o in results if o.conversation_id == conversation_id]
        return results[-limit:]

    def count(self, status: OutcomeStatus | None = None) -> int:
        if status is None:
            return len(self._outcomes)
        return sum(1 for o in self._outcomes if o.status == status)

    def success_rate(self, outcome_type: str) -> float:
        total = sum(1 for o in self._outcomes if o.outcome_type == outcome_type)
        if total == 0:
            return 0.0
        successes = sum(1 for o in self._outcomes
                        if o.outcome_type == outcome_type and o.status == OutcomeStatus.SUCCESS)
        return successes / total * 100

    def clear(self) -> None:
        self._outcomes.clear()


learning_event_registry = LearningEventRegistry()
outcome_registry = OutcomeRegistry()


def list_event_types() -> list[str]:
    return [t.value for t in LearningEventType]


def get_event_types() -> list[LearningEventType]:
    return list(LearningEventType)
