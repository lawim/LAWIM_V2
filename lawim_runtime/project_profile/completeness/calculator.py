from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from ..base import AbstractProjectProfile
from ..registry import FieldRegistry
from ..values import FieldValueStatus


@dataclass
class CompletenessResult:
    score: float = 0.0
    required_fields_total: int = 0
    required_fields_present: int = 0
    optional_fields_total: int = 0
    optional_fields_present: int = 0
    missing_required_fields: list[str] = field(default_factory=list)
    missing_optional_fields: list[str] = field(default_factory=list)
    invalid_fields: list[str] = field(default_factory=list)
    conflicted_fields: list[str] = field(default_factory=list)


WEIGHTS: dict[str, float] = {
    "intent": 15.0, "transaction_type": 15.0, "property_type": 15.0,
    "city": 15.0, "district": 10.0, "budget_max": 15.0, "bedrooms": 5.0,
    "move_in_date": 5.0, "furnished": 3.0, "parking": 2.0,
}


class ProfileCompletenessCalculator:
    def __init__(self, registry: FieldRegistry) -> None:
        self._registry = registry

    def calculate(self, profile: AbstractProjectProfile) -> CompletenessResult:
        required = self._registry.list_required_fields(profile.profile_type)
        all_fields = self._registry.list_fields_by_profile(profile.profile_type)
        result = CompletenessResult()
        for fdef in required:
            result.required_fields_total += 1
            fv = profile.get_field(fdef.field_name)
            if fv is not None and fv.status not in (FieldValueStatus.REJECTED, FieldValueStatus.SUPERSEDED):
                result.required_fields_present += 1
            else:
                result.missing_required_fields.append(fdef.field_name)
        for fdef in all_fields:
            if not fdef.required:
                result.optional_fields_total += 1
                fv = profile.get_field(fdef.field_name)
                if fv is not None and fv.status not in (FieldValueStatus.REJECTED, FieldValueStatus.SUPERSEDED):
                    result.optional_fields_present += 1
                else:
                    result.missing_optional_fields.append(fdef.field_name)
        total_weight = sum(WEIGHTS.get(f.field_name, 0) for f in required + [f for f in all_fields if not f.required])
        earned = sum(WEIGHTS.get(f.field_name, 0) for f in required if f.field_name not in result.missing_required_fields)
        earned += sum(WEIGHTS.get(f.field_name, 0) for f in all_fields if not f.required and f.field_name not in result.missing_optional_fields)
        result.score = round((earned / total_weight * 100) if total_weight > 0 else 0, 2)
        return result
