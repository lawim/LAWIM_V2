from __future__ import annotations

import pytest

from lawim_runtime.project_profile.definitions import FieldDefinition, MergeStrategy, ValueType
from lawim_runtime.project_profile.merge.merger import ProfileMerger, VersionConflictError
from lawim_runtime.project_profile.patch import PatchOperation, PatchUpdate, ProfilePatch
from lawim_runtime.project_profile.profile import ProjectProfile
from lawim_runtime.project_profile.registry import FieldRegistry


@pytest.fixture
def registry():
    r = FieldRegistry()
    r.register_field(FieldDefinition(field_name="city", value_type=ValueType.STRING, merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE))
    r.register_field(FieldDefinition(field_name="budget_max", value_type=ValueType.MONEY, merge_strategy=MergeStrategy.MIN_VALUE))
    r.register_field(FieldDefinition(field_name="districts", value_type=ValueType.LIST, merge_strategy=MergeStrategy.APPEND_UNIQUE))
    r.register_field(FieldDefinition(field_name="furnished", value_type=ValueType.BOOLEAN, merge_strategy=MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE))
    return r


@pytest.fixture
def merger(registry):
    return ProfileMerger(registry)


@pytest.fixture
def profile():
    return ProjectProfile(project_id="p1", profile_type="RENTAL_SEARCH", version=1)


class TestMerge:
    def test_new_field_addition(self, merger, profile):
        patch = ProfilePatch(
            project_id="p1", profile_id=profile.profile_id, base_version=1,
            updates=(PatchUpdate(operation=PatchOperation.SET, field_name="city", value="Douala", confidence=0.9),),
        )
        result = merger.apply_patch(profile, patch)
        fv = result.get_field("city")
        assert fv is not None
        assert fv.value == "Douala"

    def test_value_replacement(self, merger, profile):
        profile.set_field("city", "Yaounde", confidence=0.5)
        profile.version = 1
        patch = ProfilePatch(
            project_id="p1", profile_id=profile.profile_id, base_version=1,
            updates=(PatchUpdate(operation=PatchOperation.SET, field_name="city", value="Douala", confidence=0.9),),
        )
        result = merger.apply_patch(profile, patch)
        fv = result.get_field("city")
        assert fv.value == "Douala"

    def test_higher_confidence_wins(self, merger, profile):
        profile.set_field("city", "Yaounde", confidence=0.3)
        profile.version = 1
        patch = ProfilePatch(
            project_id="p1", profile_id=profile.profile_id, base_version=1,
            updates=(PatchUpdate(operation=PatchOperation.SET, field_name="city", value="Douala", confidence=0.9),),
        )
        result = merger.apply_patch(profile, patch)
        assert result.get_field("city").value == "Douala"

    def test_lower_confidence_keeps(self, merger, profile):
        profile.set_field("city", "Yaounde", confidence=0.9)
        profile.version = 1
        patch = ProfilePatch(
            project_id="p1", profile_id=profile.profile_id, base_version=1,
            updates=(PatchUpdate(operation=PatchOperation.SET, field_name="city", value="Douala", confidence=0.3),),
        )
        result = merger.apply_patch(profile, patch)
        assert result.get_field("city").value == "Yaounde"

    def test_append_unique_to_list(self, merger, profile):
        profile.set_field("districts", ["Bonamoussadi"])
        profile.version = 1
        patch = ProfilePatch(
            project_id="p1", profile_id=profile.profile_id, base_version=1,
            updates=(PatchUpdate(operation=PatchOperation.SET, field_name="districts", value="Makepe"),),
        )
        result = merger.apply_patch(profile, patch)
        fv = result.get_field("districts")
        assert "Bonamoussadi" in fv.value
        assert "Makepe" in fv.value

    def test_version_conflict(self, merger, profile):
        profile.version = 2
        patch = ProfilePatch(
            project_id="p1", profile_id=profile.profile_id, base_version=1,
            updates=(PatchUpdate(operation=PatchOperation.SET, field_name="city", value="Douala"),),
        )
        with pytest.raises(VersionConflictError):
            merger.apply_patch(profile, patch)

    def test_idempotent_apply(self, merger, profile):
        patch = ProfilePatch(
            project_id="p1", profile_id=profile.profile_id, base_version=1,
            updates=(PatchUpdate(operation=PatchOperation.SET, field_name="city", value="Douala", confidence=0.9),),
        )
        r1 = merger.apply_patch(profile, patch)
        assert r1.get_field("city").value == "Douala"
        assert r1.version == 2
