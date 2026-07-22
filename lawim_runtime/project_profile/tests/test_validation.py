from __future__ import annotations

import pytest

from lawim_runtime.project_profile.definitions import FieldDefinition, ValueType
from lawim_runtime.project_profile.registry import FieldRegistry
from lawim_runtime.project_profile.validation.result import ValidationStatus
from lawim_runtime.project_profile.validation.validators import FieldValidator, ValidatorRegistry


@pytest.fixture
def registry():
    r = FieldRegistry()
    r.register_field(FieldDefinition(field_name="bedrooms", value_type=ValueType.INTEGER))
    r.register_field(FieldDefinition(field_name="city", value_type=ValueType.STRING))
    r.register_field(FieldDefinition(field_name="budget_max", value_type=ValueType.MONEY))
    r.register_field(FieldDefinition(field_name="furnished", value_type=ValueType.BOOLEAN))
    r.register_field(FieldDefinition(field_name="price", value_type=ValueType.FLOAT))
    return r


@pytest.fixture
def validator(registry):
    vreg = ValidatorRegistry()
    return FieldValidator(registry, vreg)


class TestValidation:
    def test_valid_value(self, validator):
        result = validator.validate("bedrooms", 3)
        assert result.is_valid

    def test_negative_value(self, validator):
        result = validator.validate("bedrooms", -1)
        assert not result.is_valid

    def test_none_value(self, validator):
        result = validator.validate("bedrooms", None)
        assert result.status == ValidationStatus.VALID

    def test_type_mismatch_int(self, validator):
        result = validator.validate("bedrooms", "three")
        assert not result.is_valid

    def test_type_mismatch_bool(self, validator):
        result = validator.validate("furnished", "yes")
        assert not result.is_valid

    def test_float_type_accepts_int(self, validator):
        result = validator.validate("price", 100)
        assert result.is_valid

    def test_string_type_valid(self, validator):
        result = validator.validate("city", "Douala")
        assert result.is_valid
