from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class CompactionStrategy:
    recent_turn_window: int = 10
    summary_refresh_threshold: int = 20
    maximum_provider_context_chars: int = 2000
    important_event_types: set[str] = field(default_factory=lambda: {
        "correction", "consent", "decision", "handover",
        "payment", "document", "contract", "milestone",
    })


class MemoryCompactionService:
    def __init__(self, strategy: CompactionStrategy | None = None) -> None:
        self._strategy = strategy or CompactionStrategy()

    def should_compact(self, interaction_count: int, last_summary_version: int) -> bool:
        if interaction_count <= 0:
            return False
        if last_summary_version <= 0:
            return interaction_count > self._strategy.recent_turn_window
        return interaction_count > self._strategy.summary_refresh_threshold * last_summary_version

    def compact_turns(
        self,
        turns: list[dict[str, Any]],
        summary: str | None = None,
    ) -> list[dict[str, Any]]:
        if not turns:
            return []

        window = self._strategy.recent_turn_window
        if len(turns) <= window:
            return list(turns)

        kept = list(turns[-window:])
        summary_placeholder: dict[str, Any] = {
            "_type": "summary",
            "_content": summary or f"[{len(turns) - window} earlier turns compacted]",
        }
        kept.insert(0, summary_placeholder)
        return kept

    def get_important_events(self, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if not events:
            return []
        important_types = self._strategy.important_event_types
        result: list[dict[str, Any]] = []
        for ev in events:
            ev_type = (
                ev.get("type")
                or ev.get("event_type")
                or ev.get("action")
                or ""
            )
            if ev_type in important_types:
                result.append(ev)
        return result
