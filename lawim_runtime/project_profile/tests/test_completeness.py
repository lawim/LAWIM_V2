from __future__ import annotations

from lawim_runtime.project_profile.completeness.calculator import ProfileCompletenessCalculator
from lawim_runtime.project_profile.definitions import FieldDefinition, MergeStrategy, ValueType
from lawim_runtime.project_profile.profile import ProjectProfile
from lawim_runtime.project_profile.registry import FieldRegistry


def _make_registry():
    r = FieldRegistry()
    r.register_field(FieldDefinition(field_name="intent", value_type=ValueType.STRING, required=True))
    r.register_field(FieldDefinition(field_name="transaction_type", value_type=ValueType.ENUM, required=True, allowed_values=("RENT", "BUY")))
    r.register_field(FieldDefinition(field_name="property_type", value_type=ValueType.ENUM, required=True, allowed_values=("APARTMENT", "HOUSE")))
    r.register_field(FieldDefinition(field_name="city", value_type=ValueType.STRING, required=True))
    r.register_field(FieldDefinition(field_name="budget_max", value_type=ValueType.MONEY, required=True))
    r.register_field(FieldDefinition(field_name="bedrooms", value_type=ValueType.INTEGER, required=False))
    r.register_field(FieldDefinition(field_name="furnished", value_type=ValueType.BOOLEAN, required=False))
    r.register_profile_fields("RENTAL_SEARCH", ["intent", "transaction_type", "property_type", "city", "budget_max", "bedrooms", "furnished"])
    return r


class TestCompleteness:
    def test_empty_profile_score(self):
        registry = _make_registry()
        calculator = ProfileCompletenessCalculator(registry)
        p = ProjectProfile(project_id="p1", profile_type="RENTAL_SEARCH")
        result = calculator.calculate(p)
        assert result.score == 0.0
        assert len(result.missing_required_fields) == 5

    def test_partial_profile_score(self):
        registry = _make_registry()
        calculator = ProfileCompletenessCalculator(registry)
        p = ProjectProfile(project_id="p1", profile_type="RENTAL_SEARCH")
        p.set_field("intent", "rent")
        p.set_field("city", "Douala")
        result = calculator.calculate(p)
        assert result.score > 0.0
        assert result.score < 100.0

    def test_full_profile_score(self):
        registry = _make_registry()
        calculator = ProfileCompletenessCalculator(registry)
        p = ProjectProfile(project_id="p1", profile_type="RENTAL_SEARCH")
        p.set_field("intent", "rent")
        p.set_field("transaction_type", "RENT")
        p.set_field("property_type", "APARTMENT")
        p.set_field("city", "Douala")
        p.set_field("budget_max", 200000)
        p.set_field("bedrooms", 2)
        p.set_field("furnished", True)
        result = calculator.calculate(p)
        assert result.score == 100.0
        assert len(result.missing_required_fields) == 0

    def test_missing_required_fields(self):
        registry = _make_registry()
        calculator = ProfileCompletenessCalculator(registry)
        p = ProjectProfile(project_id="p1", profile_type="RENTAL_SEARCH")
        p.set_field("intent", "rent")
        result = calculator.calculate(p)
        assert "transaction_type" in result.missing_required_fields
        assert "property_type" in result.missing_required_fields
        assert "city" in result.missing_required_fields
        assert "budget_max" in result.missing_required_fields
