from __future__ import annotations

from typing import Any

from ...runtime.errors import RuntimeError
from ..base import AbstractProjectProfile
from ..history.snapshot import ProfileSnapshot
from ..merge.strategies import ConflictRecord
from ..patch import ProfilePatch


class ProjectProfileRepository:
    def __init__(self) -> None:
        self._profiles: dict[str, AbstractProjectProfile] = {}
        self._patches: list[ProfilePatch] = []
        self._snapshots: list[ProfileSnapshot] = []
        self._conflicts: list[ConflictRecord] = []

    def create_profile(self, profile: AbstractProjectProfile) -> AbstractProjectProfile:
        if profile.profile_id in self._profiles:
            raise RuntimeError(f"Profile {profile.profile_id} already exists")
        self._profiles[profile.profile_id] = profile
        return profile

    def get_profile(self, profile_id: str) -> AbstractProjectProfile | None:
        return self._profiles.get(profile_id)

    def save_profile(self, profile: AbstractProjectProfile) -> AbstractProjectProfile:
        self._profiles[profile.profile_id] = profile
        return profile

    def delete_profile(self, profile_id: str) -> None:
        self._profiles.pop(profile_id, None)

    def list_profiles_by_project(self, project_id: str) -> list[AbstractProjectProfile]:
        return [p for p in self._profiles.values() if p.project_id == project_id]

    def list_all_profiles(self) -> list[AbstractProjectProfile]:
        return list(self._profiles.values())

    def save_patch(self, patch: ProfilePatch) -> None:
        self._patches.append(patch)

    def list_patches(self, profile_id: str = "") -> list[ProfilePatch]:
        if not profile_id:
            return list(self._patches)
        return [p for p in self._patches if p.profile_id == profile_id]

    def save_snapshot(self, snapshot: ProfileSnapshot) -> None:
        self._snapshots.append(snapshot)

    def list_snapshots(self, profile_id: str = "") -> list[ProfileSnapshot]:
        if not profile_id:
            return list(self._snapshots)
        return [s for s in self._snapshots if s.profile_id == profile_id]

    def save_conflict(self, conflict: ConflictRecord) -> None:
        self._conflicts.append(conflict)

    def resolve_conflict(self, conflict_id: str, resolution: str) -> None:
        for c in self._conflicts:
            if c.conflict_id == conflict_id:
                c.resolved = True
                c.resolution = resolution
                break

    def list_conflicts(self, profile_id: str = "") -> list[ConflictRecord]:
        if not profile_id:
            return list(self._conflicts)
        return [c for c in self._conflicts if c.profile_id == profile_id]
