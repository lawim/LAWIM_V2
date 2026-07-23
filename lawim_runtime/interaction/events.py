from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from lawim_runtime.events.base import RuntimeEvent


INTERACTION_RECEIVED = "INTERACTION_RECEIVED"
INTERACTION_DUPLICATE_DETECTED = "INTERACTION_DUPLICATE_DETECTED"
INTERACTION_NORMALIZED = "INTERACTION_NORMALIZED"
IDENTITY_RESOLVED = "IDENTITY_RESOLVED"
IDENTITY_RESOLUTION_FAILED = "IDENTITY_RESOLUTION_FAILED"
SESSION_CREATED = "SESSION_CREATED"
SESSION_RESUMED = "SESSION_RESUMED"
SESSION_EXPIRED = "SESSION_EXPIRED"
PROJECT_RESOLVED = "PROJECT_RESOLVED"
PROJECT_RESOLUTION_AMBIGUOUS = "PROJECT_RESOLUTION_AMBIGUOUS"
EXTRACTION_REQUESTED = "EXTRACTION_REQUESTED"
EXTRACTION_COMPLETED = "EXTRACTION_COMPLETED"
PROFILE_PATCH_CREATED = "PROFILE_PATCH_CREATED"
INTERACTION_DECISION_COMPLETED = "INTERACTION_DECISION_COMPLETED"
RESPONSE_PLAN_CREATED = "RESPONSE_PLAN_CREATED"
RESPONSE_WRITING_REQUESTED = "RESPONSE_WRITING_REQUESTED"
RESPONSE_WRITTEN = "RESPONSE_WRITTEN"
DELIVERY_REQUESTED = "DELIVERY_REQUESTED"
DELIVERY_STARTED = "DELIVERY_STARTED"
DELIVERY_SENT = "DELIVERY_SENT"
DELIVERY_CONFIRMED = "DELIVERY_CONFIRMED"
DELIVERY_FAILED = "DELIVERY_FAILED"
INTERACTION_COMPLETED = "INTERACTION_COMPLETED"
INTERACTION_FAILED = "INTERACTION_FAILED"
V2_V3_DIVERGENCE_DETECTED = "V2_V3_DIVERGENCE_DETECTED"


def build_interaction_event(
    event_type: str,
    interaction_id: str = "",
    channel: str = "",
    session_id: str = "",
    conversation_id: str = "",
    project_id: str = "",
    correlation_id: str = "",
    causation_id: str = "",
    payload: dict[str, Any] | None = None,
) -> RuntimeEvent:
    return RuntimeEvent(
        event_type=event_type,
        project_id=project_id,
        actor="interaction_gateway",
        source="interaction",
        payload={
            "interaction_id": interaction_id,
            "channel": channel,
            "session_id": session_id,
            "conversation_id": conversation_id,
            **(payload or {}),
        },
        correlation_id=correlation_id,
        causation_id=causation_id,
    )
