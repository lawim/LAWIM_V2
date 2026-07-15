from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FieldDefinition:
    field_id: str
    label: str
    description: str
    data_type: str
    validation_rules: str
    normalization_rules: str
    question_template: str
    matching_role: str
    privacy_level: str
    source: str = "HERITAGE_VALIDATED"
    confidence: str = "HIGH"
    appears_in: tuple[str, ...] = ()
    sources: tuple[str, ...] = ()
