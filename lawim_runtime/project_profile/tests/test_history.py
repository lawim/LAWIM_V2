from __future__ import annotations

from lawim_runtime.project_profile.base import AbstractProjectProfile
from lawim_runtime.project_profile.history.history import ProfileHistory
from lawim_runtime.project_profile.history.snapshot import ProfileSnapshot
from lawim_runtime.project_profile.patch import PatchOperation, PatchUpdate, ProfilePatch
from lawim_runtime.project_profile.profile import ProjectProfile


class TestProfileHistory:
    def test_create_snapshot(self):
        p = ProjectProfile(project_id="p1", profile_type="RENTAL_SEARCH")
        p.set_field("city", "Douala")
        p.set_field("budget_max", 200000)
        snapshot = ProfileSnapshot.create(p, "c01")
        assert snapshot.project_id == "p1"
        assert snapshot.profile_id == p.profile_id
        assert snapshot.profile_version == 1
        assert snapshot.fields.get("city") == "Douala"
        assert snapshot.fields.get("budget_max") == 200000

    def test_snapshot_checksum(self):
        p = ProjectProfile(project_id="p1", profile_type="RENTAL_SEARCH")
        p.set_field("city", "Douala")
        s1 = ProfileSnapshot.create(p, "c01")
        s2 = ProfileSnapshot.create(p, "c02")
        assert s1.checksum == s2.checksum

    def test_compare_snapshots(self):
        history = ProfileHistory()
        p = ProjectProfile(project_id="p1", profile_type="RENTAL_SEARCH")
        p.set_field("city", "Douala")
        s1 = ProfileSnapshot.create(p, "c01")
        p.set_field("city", "Yaounde")
        p.set_field("bedrooms", 2)
        s2 = ProfileSnapshot.create(p, "c02")
        diff = history.compare_snapshots(s1, s2)
        assert "city" in diff["changed"]
        assert "bedrooms" in diff["added"]

    def test_restore_snapshot(self):
        p = ProjectProfile(project_id="p1", profile_type="RENTAL_SEARCH")
        p.set_field("city", "Douala")
        p.set_field("budget_max", 200000)
        snapshot = ProfileSnapshot.create(p, "c01")
        p.set_field("city", "Yaounde")
        history = ProfileHistory()
        restored = history.restore_snapshot(p, snapshot)
        fv = restored.get_field("city")
        assert fv.value == "Douala"

    def test_record_patch(self):
        history = ProfileHistory()
        patch = ProfilePatch(
            project_id="p1", profile_id="pr1", base_version=1,
            updates=(PatchUpdate(operation=PatchOperation.SET, field_name="city", value="Douala"),),
        )
        history.record_patch(patch)
        patches = history.get_patches("pr1")
        assert len(patches) == 1
        assert patches[0].patch_id == patch.patch_id

    def test_get_snapshots_by_profile(self):
        history = ProfileHistory()
        p1 = ProjectProfile(project_id="p1", profile_type="RENTAL_SEARCH")
        p2 = ProjectProfile(project_id="p2", profile_type="PURCHASE_SEARCH")
        s1 = ProfileSnapshot.create(p1)
        s2 = ProfileSnapshot.create(p2)
        history.record_snapshot(s1)
        history.record_snapshot(s2)
        snapshots = history.get_snapshots(p1.profile_id)
        assert len(snapshots) == 1
        assert snapshots[0].profile_id == p1.profile_id
