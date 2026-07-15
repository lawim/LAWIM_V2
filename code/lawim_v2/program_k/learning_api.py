from __future__ import annotations

from typing import Any

from .learning_config import LearningConfig
from .learning_models import LearningEventType, OutcomeStatus
from .learning_registry import learning_event_registry, list_event_types, outcome_registry
from .learning_services import FeedbackService, LearningEventService, OutcomeRegistryService

_config = LearningConfig()
_event_svc = LearningEventService()
_outcome_svc = OutcomeRegistryService()
_feedback_svc = FeedbackService()


def handle_learning_get(path: str, query: dict[str, list[str]],
                         actor: dict[str, object]) -> dict[str, Any] | None:
    if not _config.learning_events_enabled:
        return {"status": "disabled", "message": "learning_events_enabled=false"}

    if path == "learning/events/types":
        return {"event_types": list_event_types(), "count": len(list_event_types())}

    if path == "learning/events/stats":
        return _event_svc.get_stats()

    if path.startswith("learning/events/"):
        eid = path.split("/")[-1]
        if eid and eid != "types" and eid != "stats":
            event = learning_event_registry.get_by_id(eid)
            if event is None:
                return {"error": "event_not_found"}
            return {"event": event.to_dict()}

    return None


def handle_outcome_get(path: str, query: dict[str, list[str]],
                        actor: dict[str, object]) -> dict[str, Any] | None:
    if not _config.outcome_registry_enabled:
        return {"status": "disabled", "message": "outcome_registry_enabled=false"}

    if path == "learning/outcomes/stats":
        return _outcome_svc.get_stats()

    if path.startswith("learning/outcomes/success-rate/"):
        otype = path.split("/")[-1]
        rate = _outcome_svc.get_success_rate(otype)
        return {"outcome_type": otype, "success_rate_pct": round(rate, 2)}

    if path == "learning/outcomes":
        return {"total": outcome_registry.count(),
                "by_status": {s.value: outcome_registry.count(s) for s in OutcomeStatus}}

    return None


def handle_feedback_get(path: str, query: dict[str, list[str]),
                         actor: dict[str, object]) -> dict[str, Any] | None:
    if not _config.feedback_engine_enabled:
        return {"status": "disabled", "message": "feedback_engine_enabled=false"}

    if path == "learning/feedback":
        return {"total": _feedback_svc.count(),
                "items": [f.to_dict() for f in _feedback_svc.get_all()[-50:]]}

    return None
