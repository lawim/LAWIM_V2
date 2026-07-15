from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class MatchingSemantic:
    role_id: str
    description: str
    score_contribution: str
    evaluation_order: int
    examples: tuple[str, ...] = ()
