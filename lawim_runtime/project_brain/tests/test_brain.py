from __future__ import annotations

import pytest

from lawim_runtime.project_brain.brain import ProjectBrain
from lawim_runtime.project_brain.persistence import ProjectBrainRepository
from lawim_runtime.project_brain.adapters.v2_qualification import V2ReadinessEvaluatorAdapter
from lawim_runtime.project_brain.adapters.progressive_wizard import ProgressiveWizardDecisionAdapter
from lawim_runtime.qualification.engine import QualificationEngine
from lawim_runtime.qualification.registry import RequirementRegistry
from lawim_runtime.qualification.requirements import RequirementDefinition, RequirementType
from lawim_runtime.qualification.score import QualificationLevel
from lawim_runtime.decision.engine import DecisionEngine
from lawim_runtime.decision.handover import HumanHandoverEvaluator
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
    r.register_profile_fields("RENTAL_SEARCH", ["city", "property_type", "transaction_type", "budget_max", "bedrooms"])
    return r


@pytest.fixture
def req_registry():
    r = RequirementRegistry()
    r.register(RequirementDefinition(requirement_id="city", field_name="city", requirement_type=RequirementType.MANDATORY, weight=30.0, profile_types=("RENTAL_SEARCH",)))
    r.register(RequirementDefinition(requirement_id="property_type", field_name="property_type", requirement_type=RequirementType.MANDATORY, weight=25.0, profile_types=("RENTAL_SEARCH",)))
    r.register(RequirementDefinition(requirement_id="transaction_type", field_name="transaction_type", requirement_type=RequirementType.MANDATORY, weight=25.0, profile_types=("RENTAL_SEARCH",)))
    r.register(RequirementDefinition(requirement_id="budget_max", field_name="budget_max", requirement_type=RequirementType.IMPORTANT, weight=15.0, profile_types=("RENTAL_SEARCH",)))
    r.register(RequirementDefinition(requirement_id="bedrooms", field_name="bedrooms", requirement_type=RequirementType.OPTIONAL, weight=5.0, profile_types=("RENTAL_SEARCH",)))
    return r


@pytest.fixture
def qual_engine(req_registry, field_registry):
    return QualificationEngine(req_registry, field_registry)


@pytest.fixture
def decision_engine(field_registry):
    return DecisionEngine(field_registry)


@pytest.fixture
def handover_evaluator():
    return HumanHandoverEvaluator()


@pytest.fixture
def brain(qual_engine, decision_engine, handover_evaluator):
    return ProjectBrain(qual_engine, decision_engine, handover_evaluator)


@pytest.fixture
def empty_profile():
    return ProjectProfile(project_id="proj-1", profile_type="RENTAL_SEARCH")


@pytest.fixture
def partial_profile():
    p = ProjectProfile(project_id="proj-1", profile_type="RENTAL_SEARCH")
    p.set_field("city", "Douala")
    p.set_field("transaction_type", "RENT")
    return p


@pytest.fixture
def full_profile():
    p = ProjectProfile(project_id="proj-1", profile_type="RENTAL_SEARCH")
    p.set_field("city", "Douala", confidence=0.9)
    p.set_field("property_type", "APARTMENT", confidence=0.9)
    p.set_field("transaction_type", "RENT", confidence=0.9)
    p.set_field("budget_max", 200000, confidence=0.9)
    return p


class TestProjectBrain:
    def test_qualification_empty_profile(self, brain, empty_profile):
        qual_result, decision, state = brain.evaluate(empty_profile, user_message="")
        assert qual_result.level in (QualificationLevel.UNQUALIFIED, QualificationLevel.PARTIALLY_QUALIFIED)
        assert qual_result.score.final_score >= 0.0
        assert state.qualification_level in ("UNQUALIFIED", "PARTIALLY_QUALIFIED")

    def test_qualification_partial(self, brain, partial_profile):
        qual_result, decision, state = brain.evaluate(partial_profile, user_message="")
        assert qual_result.score.final_score > 0.0
        assert qual_result.score.final_score < 100.0
        assert "property_type" in qual_result.required_missing
        assert "budget_max" in qual_result.important_missing
        assert "city" not in qual_result.required_missing

    def test_decision_missing_field(self, brain, empty_profile):
        qual_result, decision, state = brain.evaluate(empty_profile, user_message="")
        assert decision.selected_action == "ASK_MISSING_FIELD"

    def test_decision_ready_for_matching(self, brain, full_profile):
        qual_result, decision, state = brain.evaluate(full_profile, user_message="")
        assert decision.selected_action == "START_MATCHING"

    def test_decision_handover(self, brain, full_profile):
        qual_result, decision, state = brain.evaluate(full_profile, user_message="I want to speak to an agent")
        assert state.human_required

    def test_brain_evaluate_full(self, brain, full_profile):
        qual_result, decision, state = brain.evaluate(full_profile, user_message="")
        assert qual_result.project_id == "proj-1"
        assert decision.project_id == "proj-1"
        assert state.project_id == "proj-1"
        assert state.project_type == "RENTAL_SEARCH"

    def test_brain_persistence(self, brain, partial_profile, full_profile):
        repo = ProjectBrainRepository()
        qual_result, decision, state = brain.evaluate(partial_profile, user_message="")
        repo.save_qualification(qual_result)
        repo.save_decision(decision)
        repo.save_brain_state(state)

        loaded_qual = repo.get_latest_qualification("proj-1")
        assert loaded_qual is not None
        assert loaded_qual.project_id == "proj-1"

        loaded_dec = repo.get_latest_decision("proj-1")
        assert loaded_dec is not None

        loaded_state = repo.get_brain_state("proj-1")
        assert loaded_state is not None
        assert loaded_state.project_id == "proj-1"

        qual_result2, decision2, state2 = brain.evaluate(full_profile, user_message="")
        repo.save_qualification(qual_result2)
        repo.save_decision(decision2)
        repo.save_brain_state(state2)

        assert repo.get_brain_state("nonexistent") is None


class TestV2Adapter:
    def test_v2_adapter(self):
        adapter = V2ReadinessEvaluatorAdapter()
        result = adapter.evaluate({"city": "Douala", "property_type": "APARTMENT", "transaction_type": "RENT"})
        assert result["ready"]
        assert len(result["missing"]) == 0

        result = adapter.evaluate({"city": "Douala"})
        assert not result["ready"]
        assert "property_type" in result["missing"]
        assert "transaction_type" in result["missing"]


class TestProgressiveWizardAdapter:
    def test_progressive_wizard_adapter(self):
        adapter = ProgressiveWizardDecisionAdapter()
        missing = ["bedrooms", "budget_max", "city"]
        priority = {"city": 1, "property_type": 2, "transaction_type": 3, "budget_max": 4, "bedrooms": 5}
        result = adapter.to_next_field(missing, priority)
        assert result == "city"

    def test_progressive_wizard_empty(self):
        adapter = ProgressiveWizardDecisionAdapter()
        assert adapter.to_next_field([], {}) is None

    def test_progressive_wizard_no_match(self):
        adapter = ProgressiveWizardDecisionAdapter()
        assert adapter.to_next_field(["unknown_field"], {}) == "unknown_field"
