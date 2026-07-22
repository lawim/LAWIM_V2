from __future__ import annotations
from typing import Any
from ..events.base import RuntimeEvent
from ..events.bus import EventBus


class ConversationRuntimeAdapter:
    """Adapts V2 ConversationStateEngine calls to LROS runtime events.

    This adapter allows the existing ConversationStateEngine to publish
    events to the runtime without modifying the V2 engine.
    """

    def __init__(self, bus: EventBus) -> None:
        self._bus = bus

    def on_message_received(
        self, project_id: str, actor: str, message: str, channel: str
    ) -> RuntimeEvent:
        event = RuntimeEvent(
            event_type="CONVERSATION_MESSAGE_RECEIVED",
            project_id=project_id,
            actor=actor,
            source=channel,
            payload={"message": message, "channel": channel},
        )
        self._bus.publish(event)
        return event

    def on_intent_detected(
        self, project_id: str, actor: str, intent: str, confidence: float
    ) -> RuntimeEvent:
        event = RuntimeEvent(
            event_type="CONVERSATION_INTENT_DETECTED",
            project_id=project_id,
            actor=actor,
            source="conversation_engine",
            payload={"intent": intent, "confidence": confidence},
        )
        self._bus.publish(event)
        return event

    def on_slot_updated(
        self, project_id: str, actor: str, field: str, value: Any
    ) -> RuntimeEvent:
        event = RuntimeEvent(
            event_type="CONVERSATION_SLOT_UPDATED",
            project_id=project_id,
            actor=actor,
            source="conversation_engine",
            payload={"field": field, "value": value},
        )
        self._bus.publish(event)
        return event

    def on_qualification_ready(
        self, project_id: str, actor: str, qualification: dict[str, Any]
    ) -> RuntimeEvent:
        event = RuntimeEvent(
            event_type="QUALIFICATION_READY",
            project_id=project_id,
            actor=actor,
            source="conversation_engine",
            payload=qualification,
        )
        self._bus.publish(event)
        return event
