from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from ..base import AbstractProjectProfile
from ..candidate import CandidateUpdate
from ..definitions import ConflictStrategy, FieldDefinition, MergeStrategy
from ..patch import PatchOperation, PatchUpdate, ProfilePatch
from ..registry import FieldNotFoundError, FieldRegistry
from lawim_runtime.runtime.errors import RuntimeError
from ..validation.result import ValidationIssue, ValidationResult, ValidationStatus
from ..values import FieldValue, FieldValueStatus
from .strategies import ConflictRecord, ConflictResolution, ConflictType


class MergeError(RuntimeError):
    pass


class VersionConflictError(MergeError):
    pass


class ProfileMerger:
    def __init__(self, registry: FieldRegistry) -> None:
        self._registry = registry

    def apply_patch(
        self,
        profile: AbstractProjectProfile,
        patch: ProfilePatch,
        validation: ValidationResult | None = None,
    ) -> AbstractProjectProfile:
        if profile.version != patch.base_version:
            raise VersionConflictError(
                f"Profile version {profile.version} != patch base version {patch.base_version}"
            )
        for update in patch.updates:
            self._apply_update(profile, update, patch)
        profile.version += 1
        profile.updated_at = datetime.now(timezone.utc).isoformat()
        return profile

    def _apply_update(
        self,
        profile: AbstractProjectProfile,
        update: PatchUpdate,
        patch: ProfilePatch,
    ) -> None:
        try:
            fdef = self._registry.get_field(update.field_name)
        except FieldNotFoundError:
            profile.set_field(
                update.field_name,
                update.value,
                update.confidence,
            )
            return

        current_fv = profile.get_field(update.field_name)
        if current_fv is None:
            profile.set_field(
                update.field_name,
                update.value,
                update.confidence,
                source=patch.source,
                correlation_id=patch.correlation_id,
            )
            return

        strategy = fdef.merge_strategy
        new_value = self._resolve_strategy(
            current_fv.value,
            update.value,
            current_fv.confidence,
            update.confidence,
            strategy,
        )
        if new_value != current_fv.value:
            current_fv.previous_value = current_fv.value
            current_fv.value = new_value
            current_fv.confidence = max(current_fv.confidence, update.confidence)
            current_fv.version += 1
            current_fv.correlation_id = patch.correlation_id
        current_fv.status = FieldValueStatus.VALIDATED

    def _resolve_strategy(
        self,
        current: Any,
        candidate: Any,
        curr_conf: float,
        cand_conf: float,
        strategy: MergeStrategy,
    ) -> Any:
        strategies = {
            MergeStrategy.REPLACE_ALWAYS: lambda: candidate,
            MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE: lambda: candidate if cand_conf > curr_conf else current,
            MergeStrategy.REPLACE_IF_NEWER: lambda: candidate,
            MergeStrategy.KEEP_EXISTING: lambda: current,
            MergeStrategy.APPEND_UNIQUE: lambda: self._append_unique(current, candidate),
            MergeStrategy.MAX_VALUE: lambda: max(current, candidate) if current is not None and candidate is not None else candidate,
            MergeStrategy.MIN_VALUE: lambda: min(current, candidate) if current is not None and candidate is not None else candidate,
            MergeStrategy.USER_CONFIRMED_WINS: lambda: candidate if cand_conf >= 0.9 else current,
        }
        resolver = strategies.get(strategy)
        if resolver is None:
            return candidate if cand_conf > curr_conf else current
        return resolver()

    @staticmethod
    def _append_unique(current: Any, candidate: Any) -> list:
        if isinstance(current, list) and isinstance(candidate, list):
            result = list(current)
            for item in candidate:
                if item not in result:
                    result.append(item)
            return result
        if isinstance(current, list):
            if candidate not in current:
                return list(current) + [candidate]
            return list(current)
        return [current, candidate] if current != candidate else [current]
