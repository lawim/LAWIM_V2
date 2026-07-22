from __future__ import annotations

import pytest

from lawim_runtime.project_profile.definitions import FieldDefinition, ValueType, MergeStrategy
from lawim_runtime.project_profile.registry import FieldRegistry, FieldAlreadyExistsError, FieldNotFoundError


@pytest.fixture
def registry():
    return FieldRegistry()


@pytest.fixture
def populated_registry(registry):
    registry.register_field(FieldDefinition(field_name="city", value_type=ValueType.STRING, aliases=("ville",)))
    registry.register_field(FieldDefinition(field_name="budget_max", value_type=ValueType.MONEY, required=True))
    registry.register_field(FieldDefinition(field_name="property_type", value_type=ValueType.ENUM, allowed_values=("APARTMENT", "HOUSE")))
    registry.register_profile_fields("RENTAL_SEARCH", ["city", "budget_max"])
    return registry


class TestFieldRegistry:
    def test_register_field(self, registry):
        fd = FieldDefinition(field_name="city", value_type=ValueType.STRING)
        registry.register_field(fd)
        assert registry.has_field("city")

    def test_get_field(self, populated_registry):
        fd = populated_registry.get_field("city")
        assert fd.field_name == "city"
        assert fd.value_type == ValueType.STRING

    def test_alias_resolution(self, populated_registry):
        fd = populated_registry.get_field("ville")
        assert fd.field_name == "city"

    def test_field_not_found(self, registry):
        with pytest.raises(FieldNotFoundError):
            registry.get_field("nonexistent")

    def test_field_already_exists(self, populated_registry):
        with pytest.raises(FieldAlreadyExistsError):
            populated_registry.register_field(FieldDefinition(field_name="city", value_type=ValueType.STRING))

    def test_list_fields(self, populated_registry):
        fields = populated_registry.list_fields()
        assert len(fields) == 3

    def test_list_required_fields(self, populated_registry):
        required = populated_registry.list_required_fields()
        assert len(required) == 1
        assert required[0].field_name == "budget_max"

    def test_list_fields_by_profile(self, populated_registry):
        fields = populated_registry.list_fields_by_profile("RENTAL_SEARCH")
        names = {f.field_name for f in fields}
        assert names == {"city", "budget_max"}

    def test_register_profile_fields(self, registry):
        registry.register_field(FieldDefinition(field_name="bedrooms", value_type=ValueType.INTEGER))
        registry.register_field(FieldDefinition(field_name="city", value_type=ValueType.STRING))
        registry.register_profile_fields("PURCHASE_SEARCH", ["bedrooms", "city"])
        fields = registry.list_fields_by_profile("PURCHASE_SEARCH")
        assert len(fields) == 2
