from __future__ import annotations

import pytest

from lawim_runtime.decision.engine import DecisionEngine
from lawim_runtime.decision.handover import HumanHandoverEvaluator
from lawim_runtime.decision.actions import ActionCategory, ActionDefinition
from lawim_runtime.qualification.engine import QualificationEngine
from lawim_runtime.qualification.registry import RequirementRegistry
from lawim_runtime.qualification.requirements import RequirementDefinition, RequirementType
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
def decision_engine(field_registry):
    return DecisionEngine(field_registry)


@pytest.fixture
def qual_engine(req_registry, field_registry):
    return QualificationEngine(req_registry, field_registry)


class TestDecision:
    def test_no_action(self, decision_engine, qual_engine):
        profile = ProjectProfile(project_id="p1", profile_type="RENTAL_SEARCH")
        qual_result = qual_engine.evaluate(profile)
        result = decision_engine.decide(profile, qual_result)
        assert result.selected_action == "ASK_MISSING_FIELD"

    def test_ask_missing_field(self, decision_engine, qual_engine):
        profile = ProjectProfile(project_id="p1", profile_type="RENTAL_SEARCH")
        qual_result = qual_engine.evaluate(profile)
        result = decision_engine.decide(profile, qual_result)
        assert result.selected_action == "ASK_MISSING_FIELD"
        assert result.selected_field in ("city", "property_type", "transaction_type")
        assert result.selected_category == ActionCategory.COLLECTION

    def test_resolve_conflict(self, decision_engine, qual_engine):
        profile = ProjectProfile(project_id="p1", profile_type="RENTAL_SEARCH")
        profile.set_field("city", "Douala")
        profile.set_field("property_type", "APARTMENT")
        profile.set_field("transaction_type", "RENT")
        profile.conflict_status = "FIELD_CONFLICT"
        qual_result = qual_engine.evaluate(profile)
        result = decision_engine.decide(profile, qual_result)
        assert result.selected_action in ("RESOLVE_CONFLICT", "START_MATCHING")
        assert result.selected_category in (ActionCategory.CONFIRMATION, ActionCategory.MATCHING)

    def test_start_matching(self, decision_engine, qual_engine):
        profile = ProjectProfile(project_id="p1", profile_type="RENTAL_SEARCH")
        profile.set_field("city", "Douala")
        profile.set_field("property_type", "APARTMENT")
        profile.set_field("transaction_type", "RENT")
        profile.set_field("budget_max", 200000)
        qual_result = qual_engine.evaluate(profile)
        result = decision_engine.decide(profile, qual_result)
        assert result.selected_action == "START_MATCHING"
        assert result.selected_category == ActionCategory.MATCHING

    def test_escalate_to_human(self, qual_engine):
        profile = ProjectProfile(project_id="p1", profile_type="RENTAL_SEARCH")
        profile.set_field("city", "Douala")
        profile.set_field("property_type", "APARTMENT")
        profile.set_field("transaction_type", "RENT")
        profile.set_field("budget_max", 200000)
        qual_result = qual_engine.evaluate(profile)
        evaluator = HumanHandoverEvaluator()
        handover = evaluator.evaluate(profile, user_message="I want to speak to an agent")
        assert handover.handover_required
        assert "agent" in handover.reason.lower() or "human" in handover.reason.lower()


class TestHandover:
    def test_handover_trigger_words(self):
        evaluator = HumanHandoverEvaluator()
        for trigger in ("agent", "humain", "operator", "escalate", "réclamation", "complaint", "litige", "avocat", "lawyer"):
            handover = evaluator.evaluate(ProjectProfile(project_id="p1"), user_message=f"I need a {trigger}")
            assert handover.handover_required, f"Trigger '{trigger}' should require handover"

    def test_handover_no_trigger(self):
        evaluator = HumanHandoverEvaluator()
        handover = evaluator.evaluate(ProjectProfile(project_id="p1"), user_message="I want to see some apartments")
        assert not handover.handover_required

    def test_handover_empty_message(self):
        evaluator = HumanHandoverEvaluator()
        handover = evaluator.evaluate(ProjectProfile(project_id="p1"), user_message="")
        assert not handover.handover_required

    def test_handover_conflict_status(self):
        evaluator = HumanHandoverEvaluator()
        profile = ProjectProfile(project_id="p1")
        profile.conflict_status = "PERSISTENT_CONFLICT"
        handover = evaluator.evaluate(profile, user_message="just looking")
        assert handover.handover_required
        assert "conflict" in handover.reason.lower()

    def test_handover_validation_failed(self):
        evaluator = HumanHandoverEvaluator()
        profile = ProjectProfile(project_id="p1")
        profile.validation_status = "FAILED"
        handover = evaluator.evaluate(profile, user_message="")
        assert handover.handover_required
        assert "validation" in handover.reason.lower()


class TestActionCategory:
    def test_escalation_requires_human(self):
        action = ActionDefinition(action_name="escalate", category=ActionCategory.ESCALATION)
        assert action.requires_human

    def test_handover_requires_human(self):
        action = ActionDefinition(action_name="handover", category=ActionCategory.HANDOVER)
        assert action.requires_human

    def test_collection_no_human(self):
        action = ActionDefinition(action_name="ask_field", category=ActionCategory.COLLECTION)
        assert not action.requires_human
