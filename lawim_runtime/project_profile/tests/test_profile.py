from __future__ import annotations

import pytest

from lawim_runtime.project_profile.profile import ProjectProfile
from lawim_runtime.project_profile.values import FieldValueStatus


@pytest.fixture
def profile():
    return ProjectProfile(project_id="proj-1", profile_type="RENTAL_SEARCH")


class TestProjectProfile:
    def test_create_rental_profile(self):
        p = ProjectProfile(project_id="p1", profile_type="RENTAL_SEARCH")
        assert p.profile_type == "RENTAL_SEARCH"
        assert p.project_id == "p1"
        assert p.version == 1
        assert p.status == "DRAFT"

    def test_create_purchase_profile(self):
        p = ProjectProfile(project_id="p2", profile_type="PURCHASE_SEARCH")
        assert p.profile_type == "PURCHASE_SEARCH"

    def test_set_field(self, profile):
        fv = profile.set_field("city", "Douala", confidence=0.9)
        assert fv.field_name == "city"
        assert fv.value == "Douala"
        assert fv.confidence == 0.9
        assert fv.status == FieldValueStatus.CANDIDATE

    def test_get_field(self, profile):
        profile.set_field("city", "Yaounde")
        fv = profile.get_field("city")
        assert fv is not None
        assert fv.value == "Yaounde"

    def test_get_field_missing(self, profile):
        assert profile.get_field("nonexistent") is None

    def test_has_field(self, profile):
        profile.set_field("bedrooms", 2)
        assert profile.has_field("bedrooms")
        assert not profile.has_field("bathrooms")

    def test_remove_field(self, profile):
        profile.set_field("city", "Douala")
        assert profile.has_field("city")
        profile.remove_field("city")
        assert not profile.has_field("city")

    def test_to_dict(self, profile):
        profile.set_field("city", "Douala")
        profile.set_field("bedrooms", 2)
        d = profile.to_dict()
        assert d["profile_type"] == "RENTAL_SEARCH"
        assert d["project_id"] == "proj-1"
        assert d["version"] == 1
        assert d["fields"]["city"] == "Douala"
        assert d["fields"]["bedrooms"] == 2

    def test_profile_type(self, profile):
        assert profile.profile_type == "RENTAL_SEARCH"

    def test_version_init(self, profile):
        assert profile.version == 1

    def test_set_field_with_metadata(self, profile):
        fv = profile.set_field("city", "Douala", source="user", correlation_id="c01")
        assert fv.value == "Douala"
