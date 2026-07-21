from __future__ import annotations

import pytest

from lawim_v2.conversation.policy.policy import LawimConversationPolicy
from lawim_v2.conversation.policy.internal_engine import LawimInternalResponseEngine
from lawim_v2.conversation.policy.dialogue_plan import DialoguePlan
from lawim_v2.conversation.state.state import ConversationState, ResponsePlan


@pytest.fixture
def policy() -> LawimConversationPolicy:
    return LawimConversationPolicy()


@pytest.fixture
def engine() -> LawimInternalResponseEngine:
    return LawimInternalResponseEngine()


class TestStudioRentalFullJourney:
    """Full multi-turn scenario: user wants to rent a studio."""

    def test_turn_1_greeting(self, policy: LawimConversationPolicy, engine: LawimInternalResponseEngine) -> None:
        state = ConversationState(language="fr")
        plan = policy.build_dialogue_plan(state=state, message="Bonjour")
        assert plan.dialogue_act == "WELCOME"
        response = engine.generate(plan)
        assert "Bonjour" in response
        assert "LAWIM" in response

    def test_turn_2_acknowledge_and_ask_city(self, policy: LawimConversationPolicy, engine: LawimInternalResponseEngine) -> None:
        state = ConversationState(
            language="fr",
            current_intent="rent",
            known_slots={
                "transaction_type": "rent",
                "property_type": "studio",
                "property_usage": "residential",
            },
            missing_slots=["city", "budget_max"],
        )
        response_plan = ResponsePlan(
            response_type="QUESTION",
            next_question_key="city",
            next_question_text="Dans quelle ville ?",
        )
        plan = policy.build_dialogue_plan(state=state, response_plan=response_plan)
        assert plan.dialogue_act == "ACKNOWLEDGE_AND_ASK"
        assert "city" in str(plan.facts_to_confirm) or "studio" in str(plan.facts_to_confirm)
        response = engine.generate(plan)
        assert "studio" in response.lower() or "Tr\u00e8s bien" in response
        assert "ville" in response or "Douala" in response

    def test_turn_3_budget_question(self, policy: LawimConversationPolicy, engine: LawimInternalResponseEngine) -> None:
        state = ConversationState(
            language="fr",
            current_intent="rent",
            known_slots={
                "transaction_type": "rent",
                "property_type": "studio",
                "city": "Douala",
            },
            missing_slots=["budget_max"],
            last_question_key="city",
        )
        response_plan = ResponsePlan(
            response_type="QUESTION",
            next_question_key="budget_max",
            next_question_text="Quel est votre budget maximum ?",
            updated_slots={"city": "Douala"},
        )
        plan = policy.build_dialogue_plan(state=state, response_plan=response_plan)
        if plan.dialogue_act == "ACKNOWLEDGE_AND_ASK":
            response = engine.generate(plan)
            assert "Douala" in response
            assert "budget" in response

    def test_turn_4_search_ready(self, policy: LawimConversationPolicy, engine: LawimInternalResponseEngine) -> None:
        state = ConversationState(
            language="fr",
            current_intent="rent",
            known_slots={
                "transaction_type": "rent",
                "property_type": "studio",
                "city": "Douala",
                "budget_max": 100000,
            },
            missing_slots=[],
            qualification_status="completed",
        )
        response_plan = ResponsePlan(response_type="QUALIFICATION_COMPLETE")
        plan = policy.build_dialogue_plan(state=state, response_plan=response_plan)
        assert plan.dialogue_act == "SEARCH_READY"
        response = engine.generate(plan)
        assert "recherche" in response


class TestApartmentRentalFullJourney:
    """Full multi-turn scenario: user wants to rent an apartment in Akwa."""

    def test_turn_1_greeting(self, policy: LawimConversationPolicy, engine: LawimInternalResponseEngine) -> None:
        state = ConversationState(language="fr")
        plan = policy.build_dialogue_plan(state=state, message="Bonjour")
        assert plan.dialogue_act == "WELCOME"

    def test_turn_2_akwa_location(self, policy: LawimConversationPolicy, engine: LawimInternalResponseEngine) -> None:
        state = ConversationState(
            language="fr",
            current_intent="rent",
            known_slots={
                "transaction_type": "rent",
                "property_type": "apartment",
            },
            missing_slots=["city", "district", "budget_max"],
            last_question_key="city",
        )
        response_plan = ResponsePlan(
            response_type="QUESTION",
            next_question_key="city",
            next_question_text="Dans quelle ville ?",
            updated_slots={"district": "Akwa"},
        )
        plan = policy.build_dialogue_plan(state=state, response_plan=response_plan)
        assert plan.dialogue_act in ("ACKNOWLEDGE_AND_ASK", "CLARIFY_CURRENT_SLOT")

    def test_turn_3_budget_with_fcfa(self, policy: LawimConversationPolicy, engine: LawimInternalResponseEngine) -> None:
        state = ConversationState(
            language="fr",
            current_intent="rent",
            known_slots={
                "transaction_type": "rent",
                "property_type": "apartment",
                "city": "Douala",
                "district": "Akwa",
            },
            missing_slots=["budget_max"],
        )
        response_plan = ResponsePlan(
            response_type="QUESTION",
            next_question_key="budget_max",
            next_question_text="Quel est votre budget maximum ?",
            updated_slots={"city": "Douala", "district": "Akwa"},
        )
        plan = policy.build_dialogue_plan(state=state, response_plan=response_plan)
        assert plan.dialogue_act == "ACKNOWLEDGE_AND_ASK"
        response = engine.generate(plan)
        assert "Akwa" in response or "Douala" in response


class TestLanguageSwitchScenario:
    """User starts in French then switches to English over multiple turns."""

    def test_initial_french(self, policy: LawimConversationPolicy, engine: LawimInternalResponseEngine) -> None:
        state = ConversationState(language="fr")
        plan = policy.build_dialogue_plan(state=state, message="Bonjour")
        assert plan.language == "fr"

    def test_single_english_word_does_not_switch(
        self, policy: LawimConversationPolicy
    ) -> None:
        from lawim_v2.conversation.policy.language_policy import LawimLanguagePolicy
        lang_policy = LawimLanguagePolicy()
        assert lang_policy.should_switch("fr", "en", "OK", 0) is False

    def test_full_english_sentence_after_two_messages_switches(
        self, policy: LawimConversationPolicy
    ) -> None:
        from lawim_v2.conversation.policy.language_policy import LawimLanguagePolicy
        lang_policy = LawimLanguagePolicy()
        assert lang_policy.should_switch("fr", "en", "I am looking for a house in Douala", 2) is True


class TestHandoverScenario:
    """User asks for human assistance."""

    def test_handover_detected(self, policy: LawimConversationPolicy, engine: LawimInternalResponseEngine) -> None:
        state = ConversationState(language="fr")
        response_plan = ResponsePlan(response_type="HANDOVER_ACK")
        plan = policy.build_dialogue_plan(state=state, response_plan=response_plan)
        assert plan.dialogue_act == "HANDOVER"
        response = engine.generate(plan)
        assert "conseiller" in response


class TestRephraseScenario:
    """User asks for rephrasing."""

    def test_rephrase_plan(self, policy: LawimConversationPolicy, engine: LawimInternalResponseEngine) -> None:
        state = ConversationState(language="fr", last_question_key="budget_max")
        response_plan = ResponsePlan(
            response_type="REPHRASE",
            next_question_key="budget_max",
            next_question_text="Quel est votre budget maximum ?",
        )
        plan = policy.build_dialogue_plan(state=state, response_plan=response_plan)
        assert plan.dialogue_act == "REPHRASE_LAST_QUESTION"
        response = engine.generate(plan)
        assert "budget" in response


class TestEmptyInitialMessage:
    def test_no_intent_leads_to_welcome(self, policy: LawimConversationPolicy) -> None:
        state = ConversationState(language="fr")
        plan = policy.build_dialogue_plan(state=state)
        assert plan.dialogue_act == "WELCOME"
