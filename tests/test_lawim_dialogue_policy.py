from __future__ import annotations

import pytest

from lawim_v2.conversation.policy.dialogue_plan import DialoguePlan
from lawim_v2.conversation.policy.internal_engine import LawimInternalResponseEngine
from lawim_v2.conversation.policy.persona import get_lawim_persona
from lawim_v2.conversation.policy.policy import LawimConversationPolicy
from lawim_v2.conversation.state.state import ConversationState, ResponsePlan


def test_dialogue_plan_defaults() -> None:
    plan = DialoguePlan()
    assert plan.speaker == "LAWIM AI"
    assert plan.language == "fr"
    assert plan.dialogue_act == ""
    assert plan.maximum_questions == 1
    assert plan.maximum_sentences == 4
    assert plan.maximum_characters == 600
    assert plan.list_policy == "avoid"
    assert plan.footer_required is True
    assert plan.generated_by_ai is True


def test_dialogue_plan_to_dict() -> None:
    plan = DialoguePlan(dialogue_act="WELCOME", language="en")
    d = plan.to_dict()
    assert d["dialogue_act"] == "WELCOME"
    assert d["language"] == "en"
    assert d["speaker"] == "LAWIM AI"


def test_custom_dialogue_plan() -> None:
    plan = DialoguePlan(
        dialogue_act="SEARCH_READY",
        language="pcm",
        maximum_questions=0,
        footer_required=False,
        facts_to_confirm={"city": "Douala"},
    )
    assert plan.dialogue_act == "SEARCH_READY"
    assert plan.facts_to_confirm["city"] == "Douala"


def test_internal_engine_generate_welcome() -> None:
    engine = LawimInternalResponseEngine()
    plan = DialoguePlan(dialogue_act="WELCOME", language="fr")
    response = engine.generate(plan)
    assert "Bonjour" in response
    assert "bienvenue" in response
    assert "LAWIM" in response


def test_internal_engine_generate_welcome_en() -> None:
    engine = LawimInternalResponseEngine()
    plan = DialoguePlan(dialogue_act="WELCOME", language="en")
    response = engine.generate(plan)
    assert "Hello" in response
    assert "welcome" in response


def test_internal_engine_generate_welcome_pcm() -> None:
    engine = LawimInternalResponseEngine()
    plan = DialoguePlan(dialogue_act="WELCOME", language="pcm")
    response = engine.generate(plan)
    assert "Welcome" in response
    assert "LAWIM" in response


def test_internal_engine_generate_handover() -> None:
    engine = LawimInternalResponseEngine()
    plan = DialoguePlan(dialogue_act="HANDOVER", language="fr")
    response = engine.generate(plan)
    assert "conseiller" in response


def test_internal_engine_generate_rephrase() -> None:
    engine = LawimInternalResponseEngine()
    plan = DialoguePlan(
        dialogue_act="REPHRASE_LAST_QUESTION",
        language="fr",
        rendered_next_question="Quel est votre budget ?",
    )
    response = engine.generate(plan)
    assert "reformule" in response
    assert "budget" in response


def test_internal_engine_generate_acknowledge_and_ask() -> None:
    engine = LawimInternalResponseEngine()
    plan = DialoguePlan(
        dialogue_act="ACKNOWLEDGE_AND_ASK",
        language="fr",
        facts_to_confirm={"city": "Douala", "property_type": "apartment"},
        rendered_next_question="Quel est votre budget ?",
    )
    response = engine.generate(plan)
    assert "Tr\u00e8s bien" in response
    assert "Douala" in response
    assert "apartment" in response
    assert "budget" in response


def test_internal_engine_generate_acknowledge_no_question() -> None:
    engine = LawimInternalResponseEngine()
    plan = DialoguePlan(
        dialogue_act="ACKNOWLEDGE_AND_ASK",
        language="fr",
        facts_to_confirm={"city": "Douala"},
    )
    response = engine.generate(plan)
    assert "Tr\u00e8s bien" in response
    assert "Douala" in response


def test_internal_engine_generate_search_ready() -> None:
    engine = LawimInternalResponseEngine()
    plan = DialoguePlan(dialogue_act="SEARCH_READY", language="fr")
    response = engine.generate(plan)
    assert "recherche" in response


def test_internal_engine_generate_search_ready_en() -> None:
    engine = LawimInternalResponseEngine()
    plan = DialoguePlan(dialogue_act="SEARCH_READY", language="en")
    response = engine.generate(plan)
    assert "search" in response.lower()


def test_internal_engine_generate_correction() -> None:
    engine = LawimInternalResponseEngine()
    plan = DialoguePlan(
        dialogue_act="CONFIRM_CORRECTION_AND_ASK",
        language="fr",
        facts_to_confirm={"budget_max": 150000},
        rendered_next_question="Autre chose ?",
    )
    response = engine.generate(plan)
    assert "correction" in response
    assert "150000" in response


def test_internal_engine_format_fact_budget() -> None:
    formatted = LawimInternalResponseEngine._format_fact("budget_max", 100000, "fr")
    assert "100000 FCFA" in formatted


def test_internal_engine_format_fact_city() -> None:
    formatted = LawimInternalResponseEngine._format_fact("city", "Douala", "fr")
    assert "Douala" in formatted


def test_policy_creates_dialogue_plan_greeting() -> None:
    from lawim_v2.conversation.state.state import ConversationState

    state = ConversationState(language="fr")
    policy = LawimConversationPolicy()
    plan = policy.build_dialogue_plan(state=state, message="Bonjour")
    assert plan.dialogue_act == "WELCOME"
    assert plan.language == "fr"


def test_policy_creates_dialogue_plan_acknowledge() -> None:
    state = ConversationState(
        language="fr",
        current_intent="rent",
        known_slots={"city": "Douala"},
        missing_slots=["budget_max"],
    )
    policy = LawimConversationPolicy()
    plan = policy.build_dialogue_plan(state=state, message="Je cherche un appartement")
    assert plan.dialogue_act == "ACKNOWLEDGE_AND_ASK"
    assert "Douala" in str(plan.facts_to_confirm)


def test_policy_creates_dialogue_plan_handover() -> None:
    state = ConversationState(language="fr")
    response_plan = ResponsePlan(response_type="HANDOVER_ACK")
    policy = LawimConversationPolicy()
    plan = policy.build_dialogue_plan(state=state, response_plan=response_plan)
    assert plan.dialogue_act == "HANDOVER"


def test_policy_creates_dialogue_plan_rephrase() -> None:
    state = ConversationState(language="fr", last_question_key="budget_max")
    response_plan = ResponsePlan(response_type="REPHRASE")
    policy = LawimConversationPolicy()
    plan = policy.build_dialogue_plan(state=state, response_plan=response_plan)
    assert plan.dialogue_act == "REPHRASE_LAST_QUESTION"


def test_policy_creates_dialogue_plan_search_ready() -> None:
    state = ConversationState(
        language="fr",
        current_intent="rent",
        known_slots={"city": "Douala", "budget_max": 100000},
        missing_slots=[],
        qualification_status="completed",
    )
    response_plan = ResponsePlan(response_type="QUALIFICATION_COMPLETE")
    policy = LawimConversationPolicy()
    plan = policy.build_dialogue_plan(state=state, response_plan=response_plan)
    assert plan.dialogue_act == "SEARCH_READY"
