from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class QualificationMatrix:
    matrix_id: str
    canonical_name: str
    request_family: str
    transaction_type: str
    property_type: str
    requester_typology: str
    journey_stage: str
    description: str
    minimum_intake_fields: tuple[str, ...] = ()
    minimum_search_fields: tuple[str, ...] = ()
    minimum_matching_fields: tuple[str, ...] = ()
    minimum_introduction_fields: tuple[str, ...] = ()
    minimum_visit_fields: tuple[str, ...] = ()
    minimum_transaction_fields: tuple[str, ...] = ()
    recommended_fields: tuple[str, ...] = ()
    optional_fields: tuple[str, ...] = ()
    conditional_fields: tuple[dict, ...] = ()
    sensitive_fields: tuple[str, ...] = ()
    forbidden_questions: tuple[str, ...] = ()
    source: str = "HERITAGE_VALIDATED"
    confidence: str = "HIGH"
    sources: tuple[str, ...] = ()
