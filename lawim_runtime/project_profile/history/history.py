from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from ..base import AbstractProjectProfile
from ..patch import ProfilePatch
from ..values import FieldValue, FieldValueStatus
from .snapshot import ProfileSnapshot


class ProfileHistory:
    def __init__(self) -> None:
        self._snapshots: list[ProfileSnapshot] = []
        self._patches: list[ProfilePatch] = []

    def record_snapshot(self, snapshot: ProfileSnapshot) -> None:
        self._snapshots.append(snapshot)

    def record_patch(self, patch: ProfilePatch) -> None:
        self._patches.append(patch)

    def get_snapshots(self, profile_id: str = "") -> list[ProfileSnapshot]:
        if not profile_id:
            return list(self._snapshots)
        return [s for s in self._snapshots if s.profile_id == profile_id]

    def get_patches(self, profile_id: str = "") -> list[ProfilePatch]:
        if not profile_id:
            return list(self._patches)
        return [p for p in self._patches if p.profile_id == profile_id]

    def restore_snapshot(
        self,
        profile: AbstractProjectProfile,
        snapshot: ProfileSnapshot,
    ) -> AbstractProjectProfile:
        self._snapshots.append(ProfileSnapshot.create(profile, "pre-restore"))
        profile.fields.clear()
        for field_name, value in snapshot.fields.items():
            profile.fields[field_name] = FieldValue(
                field_name=field_name,
                value=value,
                status=FieldValueStatus.CONFIRMED,
            )
        profile.version = snapshot.profile_version + 1
        profile.completion_score = snapshot.completion_score
        profile.confidence_score = snapshot.confidence_score
        profile.updated_at = datetime.now(timezone.utc).isoformat()
        return profile

    def compare_snapshots(
        self,
        s1: ProfileSnapshot,
        s2: ProfileSnapshot,
    ) -> dict[str, Any]:
        added = {k: v for k, v in s2.fields.items() if k not in s1.fields}
        removed = {k: v for k, v in s1.fields.items() if k not in s2.fields}
        changed = {
            k: (s1.fields[k], s2.fields[k])
            for k in s1.fields
            if k in s2.fields and s1.fields[k] != s2.fields[k]
        }
        return {"added": added, "removed": removed, "changed": changed}
