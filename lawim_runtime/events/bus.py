from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable
from .base import RuntimeEvent

EventHandler = Callable[[RuntimeEvent], None]


class EventBus:
    def __init__(self):
        self._handlers: dict[str, list[EventHandler]] = {}
        self._history: list[RuntimeEvent] = []

    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        self._handlers.setdefault(event_type, []).append(handler)

    def unsubscribe(self, event_type: str, handler: EventHandler) -> None:
        if event_type in self._handlers:
            self._handlers[event_type] = [h for h in self._handlers[event_type] if h != handler]

    def publish(self, event: RuntimeEvent) -> None:
        self._history.append(event)
        for handler in self._handlers.get(event.event_type, []):
            handler(event)

    def replay(self, from_index: int = 0) -> list[RuntimeEvent]:
        return self._history[from_index:]

    def clear(self) -> None:
        self._handlers.clear()
        self._history.clear()
