"""Tests for LAWIM Demo World V1."""

from __future__ import annotations

import yaml
import pytest


@pytest.fixture
def demo_data():
    with open("demo/reference/LAWIM-DEMO-WORLD-REFERENCE.yaml") as f:
        return yaml.safe_load(f)


class TestDemoWorldReference:
    def test_yaml_loaded(self, demo_data):
        assert demo_data["dataset"]["id"] == "LAWIM_DEMO_WORLD_V1"

    def test_required_sections_present(self, demo_data):
        for sec in ["users", "professional_profiles", "organizations", "properties", "services", "scenarios"]:
            assert sec in demo_data, f"Missing section: {sec}"

    def test_media_ids_are_unique(self, demo_data):
        media = demo_data.get("property_media", [])
        ids = [m["id"] for m in media]
        duplicates = set(i for i in ids if ids.count(i) > 1)
        assert len(duplicates) == 0, f"Duplicate media IDs: {duplicates}"

    def test_property_ids_are_unique(self, demo_data):
        props = demo_data.get("properties", [])
        ids = [p["id"] for p in props]
        duplicates = set(i for i in ids if ids.count(i) > 1)
        assert len(duplicates) == 0, f"Duplicate property IDs: {duplicates}"

    def test_user_ids_are_unique(self, demo_data):
        users = demo_data.get("users", [])
        ids = [u["id"] for u in users]
        assert len(set(ids)) == len(ids)

    def test_owner_references_exist(self, demo_data):
        user_ids = {u["id"] for u in demo_data.get("users", [])}
        for p in demo_data.get("properties", []):
            oid = p.get("owner_id", "")
            if oid:
                assert oid in user_ids, f"Property {p['id']} references unknown owner: {oid}"

    def test_service_providers_exist(self, demo_data):
        pro_ids = {p["id"] for p in demo_data.get("professional_profiles", [])}
        for s in demo_data.get("services", []):
            pid = s.get("provider_id", "")
            if pid:
                assert pid in pro_ids or pid in {u["id"] for u in demo_data.get("users", [])}, \
                    f"Service {s['id']} references unknown provider: {pid}"

    def test_scenario_personas_exist(self, demo_data):
        user_ids = {u["id"] for u in demo_data.get("users", [])}
        pro_ids = {p["id"] for p in demo_data.get("professional_profiles", [])}
        all_ids = user_ids | pro_ids
        for s in demo_data.get("scenarios", []):
            for persona in s.get("personas", []):
                assert persona in all_ids, f"Scenario {s['scenario_id']} unknown persona: {persona}"

    def test_scenario_properties_exist(self, demo_data):
        prop_ids = {p["id"] for p in demo_data.get("properties", [])}
        for s in demo_data.get("scenarios", []):
            for prop in s.get("properties", []):
                assert prop in prop_ids, f"Scenario {s['scenario_id']} unknown property: {prop}"

    def test_14_professions_present(self, demo_data):
        required = {"architect", "notary", "surveyor", "lawyer", "builder", "electrician", "plumber",
                     "real_estate_agent", "mover", "financial_advisor", "insurance_agent",
                     "maintenance_tech", "cleaner", "photographer"}
        present = {p.get("profession", "") for p in demo_data.get("professional_profiles", [])}
        missing = required - present
        assert len(missing) == 0, f"Missing professions: {missing}"

    def test_property_count_in_range(self, demo_data):
        count = len(demo_data.get("properties", []))
        assert 95 <= count <= 120, f"Property count {count} outside expected range"

    def test_mvan_matching_scenario(self, demo_data):
        props = demo_data.get("properties", [])
        mvan = [p for p in props if p.get("city") == "Yaoundé" and p.get("district") == "Mvan"]
        budget_ok = [p for p in mvan if p.get("price", 999999) <= 250000]
        budget_excluded = [p for p in mvan if p.get("price", 0) > 250000]
        bedrooms_ok = [p for p in budget_ok if p.get("bedrooms", 0) == 2]
        unavailable = [p for p in budget_ok if not p.get("available", True)]
        suspended = [p for p in mvan if p.get("status") == "suspended"]
        neighbor = [p for p in props if p.get("city") == "Yaoundé" and p.get("district") in ("Biyem-Assi", "Nlongkak", "Odza", "Essos")]
        assert len(bedrooms_ok) >= 3, f"Need >=3 exact matches, got {len(bedrooms_ok)}"
        assert len(budget_excluded) >= 2, f"Need >=2 budget excluded, got {len(budget_excluded)}"
        assert len(suspended) >= 1, "Need >=1 suspended"
        assert len(neighbor) >= 2, "Need >=2 neighbor districts"
