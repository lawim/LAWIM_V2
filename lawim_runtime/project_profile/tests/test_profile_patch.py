from __future__ import annotations

import pytest

from lawim_runtime.project_profile.patch import PatchOperation, PatchUpdate, ProfilePatch


class TestProfilePatch:
    def test_create_patch(self):
        updates = (
            PatchUpdate(operation=PatchOperation.SET, field_name="city", value="Douala", confidence=0.9),
            PatchUpdate(operation=PatchOperation.SET, field_name="budget_max", value=200000, confidence=0.8),
        )
        patch = ProfilePatch(
            project_id="proj-1",
            profile_id="prof-1",
            base_version=1,
            updates=updates,
            source="user",
        )
        assert patch.project_id == "proj-1"
        assert patch.profile_id == "prof-1"
        assert patch.base_version == 1
        assert len(patch.updates) == 2

    def test_patch_frozen(self):
        patch = ProfilePatch(project_id="p1")
        with pytest.raises(AttributeError):
            patch.project_id = "p2"

    def test_patch_updates(self):
        u1 = PatchUpdate(operation=PatchOperation.SET, field_name="city", value="Douala")
        u2 = PatchUpdate(operation=PatchOperation.REMOVE, field_name="old_field")
        u3 = PatchUpdate(operation=PatchOperation.APPEND, field_name="districts", value="Bonamoussadi")
        assert u1.operation == PatchOperation.SET
        assert u2.operation == PatchOperation.REMOVE
        assert u3.operation == PatchOperation.APPEND

    def test_patch_version_validation(self):
        patch = ProfilePatch(project_id="p1", profile_id="pr1", base_version=5)
        assert patch.base_version == 5
        assert patch.patch_id is not None
