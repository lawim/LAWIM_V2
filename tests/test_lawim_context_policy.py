from __future__ import annotations

import pytest

from lawim_v2.conversation.policy.persona import get_lawim_persona
from lawim_v2.conversation.policy.dialogue_plan import DialoguePlan
from lawim_v2.conversation.policy.internal_engine import LawimInternalResponseEngine


class TestStudioToRealEstateContext:
    """Studio should be contextualized as a property type, not a workspace."""

    def test_studio_detected_as_property_type(self) -> None:
        engine = LawimInternalResponseEngine()
        formatted = engine._format_fact("property_type", "studio", "fr")
        assert "studio" in formatted

    def test_studio_with_rent_context(self) -> None:
        plan = DialoguePlan(
            dialogue_act="ACKNOWLEDGE_AND_ASK",
            language="fr",
            facts_to_confirm={"property_type": "studio", "transaction_type": "rent"},
        )
        engine = LawimInternalResponseEngine()
        response = engine.generate(plan)
        assert "studio" in response


class TestAkwaToDistrictContext:
    """Akwa should be categorized as a district, not just a neighborhood."""

    def test_akwa_formatted_as_district(self) -> None:
        engine = LawimInternalResponseEngine()
        formatted = engine._format_fact("district", "Akwa", "fr")
        assert "Akwa" in formatted

    def test_akwa_in_full_context(self) -> None:
        plan = DialoguePlan(
            dialogue_act="ACKNOWLEDGE_AND_ASK",
            language="fr",
            facts_to_confirm={"district": "Akwa", "city": "Douala"},
        )
        engine = LawimInternalResponseEngine()
        response = engine.generate(plan)
        assert "Akwa" in response
        assert "Douala" in response


class TestBudgetContextualization:
    """Budget amounts should include FCFA currency context."""

    def test_budget_formatted_with_fcfa(self) -> None:
        engine = LawimInternalResponseEngine()
        formatted = engine._format_fact("budget_max", 100000, "fr")
        assert "FCFA" in formatted
        assert "100000" in formatted

    def test_budget_in_acknowledgement(self) -> None:
        plan = DialoguePlan(
            dialogue_act="ACKNOWLEDGE_AND_ASK",
            language="fr",
            facts_to_confirm={"budget_max": 200000},
        )
        engine = LawimInternalResponseEngine()
        response = engine.generate(plan)
        assert "200000" in response
        assert "FCFA" in response

    def test_budget_in_english(self) -> None:
        engine = LawimInternalResponseEngine()
        formatted = engine._format_fact("budget_max", 150000, "en")
        assert "FCFA" in formatted
