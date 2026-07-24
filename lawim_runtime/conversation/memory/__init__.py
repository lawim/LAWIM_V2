from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass
class MemoryEntry:
    entry_id: str = field(default_factory=lambda: uuid4().hex[:16])
    role: str = "user"
    content: str = ""
    intent: str = ""
    entities: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class MemoryContext:
    short_term: list[MemoryEntry] = field(default_factory=list)
    preferences: dict[str, Any] = field(default_factory=dict)
    qualification_state: str = ""
    summary: str = ""
    turn_count: int = 0


class ConversationMemory:
    MAX_SHORT_TERM = 10

    def __init__(self) -> None:
        self._short_term: list[MemoryEntry] = []
        self._preferences: dict[str, Any] = {}
        self._qualification_state: str = "INITIAL"
        self._summary: str = ""
        self._turn_count: int = 0

    def add_entry(self, role: str, content: str, intent: str = "", entities: dict[str, Any] | None = None) -> MemoryEntry:
        entry = MemoryEntry(role=role, content=content, intent=intent, entities=entities or {})
        self._short_term.append(entry)
        self._turn_count += 1
        if len(self._short_term) > self.MAX_SHORT_TERM:
            old = self._short_term.pop(0)
            self._update_summary(old)
        return entry

    def update_preferences(self, entities: dict[str, Any]) -> None:
        for key, value in entities.items():
            if key in ("property_type", "transaction_type", "city", "district", "budget_max", "bedrooms"):
                self._preferences[key] = value

    def set_qualification(self, state: str) -> None:
        self._qualification_state = state

    def get_context(self) -> MemoryContext:
        return MemoryContext(
            short_term=list(self._short_term),
            preferences=dict(self._preferences),
            qualification_state=self._qualification_state,
            summary=self._summary,
            turn_count=self._turn_count,
        )

    def get_optimized_context(self, max_turns: int = 4) -> str:
        recent = self._short_term[-max_turns:] if self._short_term else []
        lines = [f"R\u00e9sum\u00e9: {self._summary}"] if self._summary else []
        if self._preferences:
            pref_str = ", ".join(f"{k}={v}" for k, v in self._preferences.items())
            lines.append(f"Pr\u00e9f\u00e9rences: {pref_str}")
        levels = {"INITIAL", "INCOMPLETE", "PARTIAL", "QUALIFIED", "READY_FOR_DECISION"}
        if self._qualification_state in levels:
            lines.append(f"Qualification: {self._qualification_state}")
        for entry in recent:
            lines.append(f"{entry.role}: {entry.content[:100]}")
        return "\n".join(lines)

    def _update_summary(self, entry: MemoryEntry) -> None:
        if self._summary:
            self._summary = f"{self._summary} | {entry.content[:60]}"
        else:
            self._summary = entry.content[:100]

    def reset(self) -> None:
        self._short_term.clear()
        self._preferences.clear()
        self._qualification_state = "INITIAL"
        self._summary = ""
        self._turn_count = 0
