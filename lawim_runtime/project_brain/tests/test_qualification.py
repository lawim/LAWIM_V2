from __future__ import annotations

import pytest

from lawim_runtime.qualification.engine import QualificationEngine
from lawim_runtime.qualification.registry import RequirementRegistry, RequirementRegistryError
from lawim_runtime.qualification.requirements import RequirementDefinition, RequirementType
from lawim_runtime.qualification.score import QualificationLevel
from lawim_runtime.project_profile.profile import ProjectProfile
from lawim_runtime.project_profile.registry import FieldRegistry
from lawim_runtime.project_profile.definitions import FieldDefinition, ValueType


@pytest.fixture
def field_registry():
    r = FieldRegistry()
    r.register_field(FieldDefinition(field_name="city", value_type=ValueType.STRING, required=True))
    r.register_field(FieldDefinition(field_name="property_type", value_type=ValueType.ENUM, required=True, allowed_values=("APARTMENT", "HOUSE")))
    r.register_field(FieldDefinition(field_name="transaction_type", value_type=ValueType.ENUM, required=True, allowed_values=("RENT", "BUY")))
    r.register_field(FieldDefinition(field_name="budget_max", value_type=ValueType.MONEY, required=True))
    r.register_field(FieldDefinition(field_name="bedrooms", value_type=ValueType.INTEGER, required=False))
    return r


@pytest.fixture
def registry():
    r = RequirementRegistry()
    r.register(RequirementDefinition(requirement_id="city", field_name="city", requirement_type=RequirementType.MANDATORY, weight=30.0, profile_types=("RENTAL_SEARCH",)))
    r.register(RequirementDefinition(requirement_id="property_type", field_name="property_type", requirement_type=RequirementType.MANDATORY, weight=25.0, profile_types=("RENTAL_SEARCH",)))
    r.register(RequirementDefinition(requirement_id="transaction_type", field_name="transaction_type", requirement_type=RequirementType.MANDATORY, weight=25.0, profile_types=("RENTAL_SEARCH",)))
    r.register(RequirementDefinition(requirement_id="budget_max", field_name="budget_max", requirement_type=RequirementType.IMPORTANT, weight=15.0, profile_types=("RENTAL_SEARCH",)))
    r.register(RequirementDefinition(requirement_id="bedrooms", field_name="bedrooms", requirement_type=RequirementType.OPTIONAL, weight=5.0, profile_types=("RENTAL_SEARCH",)))
    return r


@pytest.fixture
def engine(registry, field_registry):
    return QualificationEngine(registry, field_registry)


class TestRequirementRegistration:
    def test_requirement_registration(self):
        r = RequirementRegistry()
        req = RequirementDefinition(requirement_id="city", field_name="city", requirement_type=RequirementType.MANDATORY, weight=30.0)
        r.register(req)
        loaded = r.get("city")
        assert loaded.field_name == "city"
        assert loaded.requirement_type == RequirementType.MANDATORY

    def test_list_all(self, registry):
        all_reqs = registry.list_all()
        assert len(all_reqs) == 5

    def test_list_for_profile(self, registry):
        reqs = registry.list_for_profile("RENTAL_SEARCH")
        assert len(reqs) == 5

    def test_list_for_profile_empty(self, registry):
        reqs = registry.list_for_profile("UNKNOWN_TYPE")
        assert len(reqs) == 0

    def test_not_found(self):
        r = RequirementRegistry()
        with pytest.raises(RequirementRegistryError):
            r.get("nonexistent")


class TestQualification:
    def test_qualification_score_calculation(self, engine):
        profile = ProjectProfile(project_id="p1", profile_type="RENTAL_SEARCH")
        profile.set_field("city", "Douala")
        profile.set_field("property_type", "APARTMENT")
        profile.set_field("transaction_type", "RENT")
        result = engine.evaluate(profile)
        assert result.score.final_score > 0.0
        assert result.score.final_score < 100.0
        assert len(result.required_missing) == 0
        assert len(result.blockers) == 0

    def test_qualification_empty(self, engine):
        profile = ProjectProfile(project_id="p1", profile_type="RENTAL_SEARCH")
        result = engine.evaluate(profile)
        assert result.level == QualificationLevel.UNQUALIFIED
        assert result.score.final_score == 0.0
        assert len(result.required_missing) == 3

    def test_qualification_full(self, engine):
        profile = ProjectProfile(project_id="p1", profile_type="RENTAL_SEARCH")
        profile.set_field("city", "Douala")
        profile.set_field("property_type", "APARTMENT")
        profile.set_field("transaction_type", "RENT")
        profile.set_field("budget_max", 200000)
        profile.set_field("bedrooms", 2)
        result = engine.evaluate(profile)
        assert result.level == QualificationLevel.ACTION_READY
        assert result.level == QualificationLevel.ACTION_READY
        assert len(result.blockers) == 0

    def test_qualification_without_optional(self, engine):
        profile = ProjectProfile(project_id="p1", profile_type="RENTAL_SEARCH")
        profile.set_field("city", "Douala")
        profile.set_field("property_type", "APARTMENT")
        profile.set_field("transaction_type", "RENT")
        profile.set_field("budget_max", 200000)
        result = engine.evaluate(profile)
        assert result.level in (QualificationLevel.QUALIFIED, QualificationLevel.ACTION_READY)
        assert result.score.final_score > 90.0

    def test_qualification_levels(self, engine):
        profile = ProjectProfile(project_id="p1", profile_type="RENTAL_SEARCH")
        profile.set_field("city", "Douala")
        result = engine.evaluate(profile)
        assert result.level == QualificationLevel.UNQUALIFIED

        profile.set_field("property_type", "APARTMENT")
        profile.set_field("transaction_type", "RENT")
        result2 = engine.evaluate(profile)
        assert result2.level in (QualificationLevel.PARTIALLY_QUALIFIED, QualificationLevel.QUALIFIED)

    def test_blocker_detection(self, engine):
        profile = ProjectProfile(project_id="p1", profile_type="RENTAL_SEARCH")
        result = engine.evaluate(profile)
        assert len(result.blockers) == 0

    def test_qualification_result_properties(self, engine):
        profile = ProjectProfile(project_id="p1", profile_type="RENTAL_SEARCH")
        result = engine.evaluate(profile)
        assert result.score.final_score == 0.0
        assert len(result.required_missing) == 3
        assert len(result.missing_fields) == 5

        profile.set_field("city", "Douala")
        profile.set_field("property_type", "APARTMENT")
        profile.set_field("transaction_type", "RENT")
        profile.set_field("budget_max", 200000)
        profile.set_field("bedrooms", 2)
        result2 = engine.evaluate(profile)
        assert result2.score.final_score == 94.5
        assert len(result2.required_missing) == 0
        assert len(result2.missing_fields) == 0
