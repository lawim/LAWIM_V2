from __future__ import annotations
from typing import Any
from .registry import RequirementRegistry
from .requirements import RequirementType
from .result import QualificationResult
from .score import QualificationLevel, QualificationScore, SCORE_THRESHOLDS
from ..project_profile.base import AbstractProjectProfile
from ..project_profile.registry import FieldRegistry
from ..project_profile.values import FieldValueStatus


class QualificationEngine:
    def __init__(self, req_registry: RequirementRegistry, field_registry: FieldRegistry) -> None:
        self._req_registry = req_registry
        self._field_registry = field_registry

    def evaluate(
        self, profile: AbstractProjectProfile, policy_id: str = "", policy_version: int = 0
    ) -> QualificationResult:
        reqs = self._req_registry.list_for_profile(profile.profile_type)
        required_present = 0
        required_missing: list[str] = []
        important_missing: list[str] = []
        optional_missing: list[str] = []
        invalid_fields: list[str] = []
        conflicted_fields: list[str] = []
        low_confidence_fields: list[str] = []
        confirmation_fields: list[str] = []
        blockers: list[str] = []
        warnings: list[str] = []
        total_weight = 0.0
        earned_weight = 0.0

        for req in reqs:
            fv = profile.get_field(req.field_name)
            present = (
                fv is not None
                and fv.status
                not in (
                    FieldValueStatus.REJECTED,
                    FieldValueStatus.SUPERSEDED,
                    FieldValueStatus.UNKNOWN,
                )
            )
            valid = present and (fv.validation_status if hasattr(fv, "validation_status") else True)
            total_weight += req.weight

            if req.requirement_type in (RequirementType.MANDATORY, RequirementType.BLOCKING):
                if present and valid:
                    required_present += 1
                    earned_weight += req.weight
                else:
                    required_missing.append(req.field_name)
                    if req.blocking:
                        blockers.append(f"Missing blocking field: {req.field_name}")

            elif req.requirement_type == RequirementType.IMPORTANT:
                if present and valid:
                    earned_weight += req.weight * 0.8
                else:
                    important_missing.append(req.field_name)

            elif req.requirement_type in (
                RequirementType.OPTIONAL,
                RequirementType.CONFIRMATION_REQUIRED,
            ):
                if present:
                    earned_weight += req.weight * 0.5
                else:
                    optional_missing.append(req.field_name)

            if present and hasattr(fv, "status") and fv.status == FieldValueStatus.CONFLICTED:
                conflicted_fields.append(req.field_name)
                if req.blocking:
                    blockers.append(f"Conflict on blocking field: {req.field_name}")

            if present and fv.confidence < req.minimum_confidence:
                low_confidence_fields.append(req.field_name)
                if req.blocking:
                    blockers.append(f"Low confidence on blocking field: {req.field_name}")

            if req.requirement_type == RequirementType.CONFIRMATION_REQUIRED and present and fv.confidence < 0.9:
                confirmation_fields.append(req.field_name)

        final_score_value = round(
            (earned_weight / total_weight * 100) if total_weight > 0 else 0, 2
        )
        if blockers:
            final_score_value = max(0, final_score_value - len(blockers) * 10)
        if conflicted_fields:
            final_score_value = max(0, final_score_value - len(conflicted_fields) * 5)
        if low_confidence_fields:
            final_score_value = max(0, final_score_value - len(low_confidence_fields) * 3)

        level = QualificationLevel.UNQUALIFIED
        for lvl, (lo, hi) in SCORE_THRESHOLDS.items():
            if lo <= final_score_value <= hi:
                level = lvl
                break

        result = QualificationResult(
            project_id=profile.project_id,
            profile_id=profile.profile_id,
            profile_version=profile.version,
            policy_id=policy_id,
            policy_version=policy_version,
            score=QualificationScore(final_score=final_score_value),
            level=level,
            status=level.value,
            required_present=required_present,
            required_missing=required_missing,
            important_missing=important_missing,
            optional_missing=optional_missing,
            invalid_fields=invalid_fields,
            conflicted_fields=conflicted_fields,
            low_confidence_fields=low_confidence_fields,
            confirmation_required_fields=confirmation_fields,
            blockers=blockers,
            warnings=warnings,
        )
        return result
