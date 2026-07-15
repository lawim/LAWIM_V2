from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class QuestionRule:
    field: str
    rule_type: str
    condition: str | None = None
    priority: int = 0
    channel: str | None = None
