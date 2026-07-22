from __future__ import annotations

import copy

from lawim_runtime.project_profile.definitions import FieldDefinition, MergeStrategy, ValueType
from lawim_runtime.project_profile.field_definitions import create_default_registry
from lawim_runtime.project_profile.merge.merger import ProfileMerger
from lawim_runtime.project_profile.patch import PatchOperation, PatchUpdate, ProfilePatch
from lawim_runtime.project_profile.persistence.repository import ProjectProfileRepository
from lawim_runtime.project_profile.profile import ProjectProfile
from lawim_runtime.project_profile.values import FieldValueStatus


def _make_merger():
    registry = create_default_registry()
    return ProfileMerger(registry)


class TestScenarios:
    def test_rental_progressive(self):
        merger = _make_merger()
        profile = ProjectProfile(project_id="p1", profile_type="RENTAL_SEARCH", version=1)

        p1 = ProfilePatch(project_id="p1", profile_id=profile.profile_id, base_version=1,
            updates=(PatchUpdate(operation=PatchOperation.SET, field_name="intent", value="rent", confidence=0.9),))
        merger.apply_patch(profile, p1)
        assert profile.get_field("intent").value == "rent"

        p2 = ProfilePatch(project_id="p1", profile_id=profile.profile_id, base_version=2,
            updates=(PatchUpdate(operation=PatchOperation.SET, field_name="city", value="Douala", confidence=0.9),))
        merger.apply_patch(profile, p2)
        assert profile.get_field("city").value == "Douala"

        p3 = ProfilePatch(project_id="p1", profile_id=profile.profile_id, base_version=3,
            updates=(PatchUpdate(operation=PatchOperation.SET, field_name="budget_max", value=200000, confidence=0.8),))
        merger.apply_patch(profile, p3)
        assert profile.get_field("budget_max").value == 200000

        p4 = ProfilePatch(project_id="p1", profile_id=profile.profile_id, base_version=4,
            updates=(PatchUpdate(operation=PatchOperation.SET, field_name="bedrooms", value=2, confidence=0.9),))
        merger.apply_patch(profile, p4)
        assert profile.get_field("bedrooms").value == 2
        assert profile.version == 5

    def test_rich_message(self):
        merger = _make_merger()
        profile = ProjectProfile(project_id="p1", profile_type="RENTAL_SEARCH", version=1)

        patch = ProfilePatch(project_id="p1", profile_id=profile.profile_id, base_version=1,
            updates=(
                PatchUpdate(operation=PatchOperation.SET, field_name="intent", value="rent", confidence=0.9),
                PatchUpdate(operation=PatchOperation.SET, field_name="city", value="Douala", confidence=0.9),
                PatchUpdate(operation=PatchOperation.SET, field_name="budget_max", value=200000, confidence=0.8),
                PatchUpdate(operation=PatchOperation.SET, field_name="bedrooms", value=2, confidence=0.9),
            ))
        merger.apply_patch(profile, patch)
        assert profile.get_field("intent").value == "rent"
        assert profile.get_field("city").value == "Douala"
        assert profile.get_field("budget_max").value == 200000
        assert profile.get_field("bedrooms").value == 2

    def test_budget_correction(self):
        merger = _make_merger()
        profile = ProjectProfile(project_id="p1", profile_type="RENTAL_SEARCH", version=1)

        p1 = ProfilePatch(project_id="p1", profile_id=profile.profile_id, base_version=1,
            updates=(PatchUpdate(operation=PatchOperation.SET, field_name="budget_max", value=300000, confidence=0.7),))
        merger.apply_patch(profile, p1)
        assert profile.get_field("budget_max").value == 300000

        p2 = ProfilePatch(project_id="p1", profile_id=profile.profile_id, base_version=2,
            updates=(PatchUpdate(operation=PatchOperation.SET, field_name="budget_max", value=200000, confidence=0.9),))
        merger.apply_patch(profile, p2)
        fv = profile.get_field("budget_max")
        assert fv.value == 200000
        assert fv.status == FieldValueStatus.VALIDATED

    def test_multiple_districts(self):
        merger = _make_merger()
        profile = ProjectProfile(project_id="p1", profile_type="RENTAL_SEARCH", version=1)

        p1 = ProfilePatch(project_id="p1", profile_id=profile.profile_id, base_version=1,
            updates=(PatchUpdate(operation=PatchOperation.SET, field_name="districts", value="Bonamoussadi"),))
        merger.apply_patch(profile, p1)

        p2 = ProfilePatch(project_id="p1", profile_id=profile.profile_id, base_version=2,
            updates=(PatchUpdate(operation=PatchOperation.SET, field_name="districts", value="Makepe"),))
        merger.apply_patch(profile, p2)

        p3 = ProfilePatch(project_id="p1", profile_id=profile.profile_id, base_version=3,
            updates=(PatchUpdate(operation=PatchOperation.SET, field_name="districts", value="Bonamoussadi"),))
        merger.apply_patch(profile, p3)

        fv = profile.get_field("districts")
        assert "Bonamoussadi" in fv.value
        assert "Makepe" in fv.value
        assert fv.value.count("Bonamoussadi") == 1

    def test_city_conflict(self):
        merger = _make_merger()
        profile = ProjectProfile(project_id="p1", profile_type="RENTAL_SEARCH", version=1)

        p1 = ProfilePatch(project_id="p1", profile_id=profile.profile_id, base_version=1,
            updates=(PatchUpdate(operation=PatchOperation.SET, field_name="city", value="Yaounde", confidence=0.5),))
        merger.apply_patch(profile, p1)

        p2 = ProfilePatch(project_id="p1", profile_id=profile.profile_id, base_version=2,
            updates=(PatchUpdate(operation=PatchOperation.SET, field_name="city", value="Douala", confidence=0.4),))
        merger.apply_patch(profile, p2)

        assert profile.get_field("city").value == "Yaounde"

    def test_user_confirmed_override(self):
        merger = _make_merger()
        profile = ProjectProfile(project_id="p1", profile_type="RENTAL_SEARCH", version=1)

        p1 = ProfilePatch(project_id="p1", profile_id=profile.profile_id, base_version=1,
            updates=(PatchUpdate(operation=PatchOperation.SET, field_name="city", value="Yaounde", confidence=0.3),))
        merger.apply_patch(profile, p1)

        p2 = ProfilePatch(project_id="p1", profile_id=profile.profile_id, base_version=2,
            updates=(PatchUpdate(operation=PatchOperation.SET, field_name="city", value="Douala", confidence=0.95),))
        merger.apply_patch(profile, p2)

        assert profile.get_field("city").value == "Douala"

    def test_restart_recovery(self):
        registry = create_default_registry()
        merger = ProfileMerger(registry)
        repo = ProjectProfileRepository()

        profile = ProjectProfile(project_id="p1", profile_type="RENTAL_SEARCH", version=1)

        p1 = ProfilePatch(project_id="p1", profile_id=profile.profile_id, base_version=1,
            updates=(PatchUpdate(operation=PatchOperation.SET, field_name="city", value="Douala", confidence=0.9),))
        merger.apply_patch(profile, p1)

        p2 = ProfilePatch(project_id="p1", profile_id=profile.profile_id, base_version=2,
            updates=(PatchUpdate(operation=PatchOperation.SET, field_name="budget_max", value=200000, confidence=0.8),))
        merger.apply_patch(profile, p2)

        repo.save_profile(profile)

        loaded = repo.get_profile(profile.profile_id)
        assert loaded is not None
        assert loaded.get_field("city").value == "Douala"
        assert loaded.get_field("budget_max").value == 200000
        assert loaded.version == 3

        p3 = ProfilePatch(project_id="p1", profile_id=profile.profile_id, base_version=3,
            updates=(PatchUpdate(operation=PatchOperation.SET, field_name="bedrooms", value=2, confidence=0.9),))
        merger.apply_patch(loaded, p3)
        assert loaded.get_field("bedrooms").value == 2
        assert loaded.version == 4
