from __future__ import annotations

from lawim_runtime.project_profile.definitions import ValueType
from lawim_runtime.project_profile.field_definitions import create_default_registry


class TestAllFieldsRegistered:
    def test_all_fields_registered(self):
        registry = create_default_registry()
        fields = registry.list_fields()
        names = {f.field_name for f in fields}
        expected = {
            "intent", "transaction_type", "property_type", "city", "district", "districts",
            "budget_min", "budget_max", "currency",
            "bedrooms", "bathrooms", "surface_min", "surface_max", "furnished", "parking",
            "move_in_date", "visit_availability", "urgency", "purchase_timeline", "lease_duration",
            "asking_price", "occupancy_status", "property_condition", "media_available", "sale_urgency",
            "land_area", "land_use", "ownership_document", "financing_required",
            "construction_type", "estimated_surface", "floors", "construction_budget",
            "desired_start_date", "desired_completion_date", "permit_status",
            "investment_type", "investment_budget", "target_return", "investment_horizon",
            "risk_tolerance", "management_preference",
            "asset_type", "verification_type", "document_types", "owner_identity_status", "verification_urgency",
        }
        assert names == expected, f"Missing: {expected - names}, Extra: {names - expected}"

    def test_rental_search_fields(self):
        registry = create_default_registry()
        fields = registry.list_fields_by_profile("RENTAL_SEARCH")
        names = {f.field_name for f in fields}
        assert "intent" in names
        assert "transaction_type" in names
        assert "property_type" in names
        assert "city" in names
        assert "budget_max" in names
        assert "bedrooms" in names
        assert "urgency" in names

    def test_purchase_search_fields(self):
        registry = create_default_registry()
        fields = registry.list_fields_by_profile("PURCHASE_SEARCH")
        names = {f.field_name for f in fields}
        assert "surface_min" in names
        assert "surface_max" in names
        assert "purchase_timeline" in names

    def test_sale_project_fields(self):
        registry = create_default_registry()
        fields = registry.list_fields_by_profile("SALE_PROJECT")
        names = {f.field_name for f in fields}
        assert "asking_price" in names
        assert "occupancy_status" in names
        assert "media_available" in names
        assert "property_type" in names

    def test_land_project_fields(self):
        registry = create_default_registry()
        fields = registry.list_fields_by_profile("LAND_PROJECT")
        names = {f.field_name for f in fields}
        assert "land_area" in names
        assert "land_use" in names
        assert "ownership_document" in names

    def test_construction_project_fields(self):
        registry = create_default_registry()
        fields = registry.list_fields_by_profile("CONSTRUCTION_PROJECT")
        names = {f.field_name for f in fields}
        assert "construction_type" in names
        assert "estimated_surface" in names
        assert "floors" in names
        assert "construction_budget" in names
        assert "permit_status" in names

    def test_alias_resolution(self):
        registry = create_default_registry()
        assert registry.get_field("ville").field_name == "city"
        assert registry.get_field("type_bien").field_name == "property_type"
        assert registry.get_field("budget").field_name == "budget_max"
        assert registry.get_field("chambres").field_name == "bedrooms"
