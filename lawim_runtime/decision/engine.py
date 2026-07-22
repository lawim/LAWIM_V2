from __future__ import annotations
from typing import Any
from ..project_profile.base import AbstractProjectProfile
from ..project_profile.registry import FieldRegistry
from ..qualification.result import QualificationResult
from ..qualification.score import QualificationLevel
from .result import DecisionResult
from .actions import ActionCategory


class DecisionEngine:
    def __init__(self, registry: FieldRegistry) -> None:
        self._registry = registry

    def decide(self, profile: AbstractProjectProfile, qual_result: QualificationResult) -> DecisionResult:
        result = DecisionResult(
            project_id=profile.project_id,
            profile_type=profile.profile_type,
            available_actions=[],
        )
        if qual_result.blockers:
            missing = qual_result.missing_fields[:1]
            if missing:
                result.selected_action = "ASK_MISSING_FIELD"
                result.selected_category = ActionCategory.COLLECTION
                result.selected_field = missing[0]
                return result
            result.selected_action = "WAIT"
            result.selected_category = ActionCategory.QUALIFICATION
            return result

        if qual_result.level in (QualificationLevel.ACTION_READY, QualificationLevel.QUALIFIED):
            result.selected_action = "START_MATCHING"
            result.selected_category = ActionCategory.MATCHING
            return result

        next_field = self._find_next_missing(profile, qual_result)
        if next_field:
            result.selected_action = "ASK_MISSING_FIELD"
            result.selected_category = ActionCategory.COLLECTION
            result.selected_field = next_field
            return result

        if profile.conflict_status not in ("NONE", ""):
            result.selected_action = "RESOLVE_CONFLICT"
            result.selected_category = ActionCategory.CONFIRMATION
            result.selected_field = ""
            return result

        if qual_result.score.final_score >= 50:
            result.selected_action = "START_MATCHING"
            result.selected_category = ActionCategory.MATCHING
            return result

        result.selected_action = "INSUFFICIENT_DATA"
        result.selected_category = ActionCategory.QUALIFICATION
        return result

    def _find_next_missing(self, profile: AbstractProjectProfile, qual_result: QualificationResult) -> str | None:
        for field_name in qual_result.missing_fields:
            fdef = self._registry.get_field(field_name) if self._registry.has_field(field_name) else None
            if fdef and fdef.required:
                return field_name
        if qual_result.missing_fields:
            return qual_result.missing_fields[0]
        return None
