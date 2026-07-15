from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SourceTrace:
    concept_id: str
    concept_type: str
    source_path: str
    source_section: str
    source_rule_ids: tuple[str, ...] = ()
    confidence: str = "HIGH"
