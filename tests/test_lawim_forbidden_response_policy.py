from __future__ import annotations

import pytest

from lawim_v2.conversation.policy.validator import LawimConversationPolicyValidator
from lawim_v2.conversation.policy.dialogue_plan import DialoguePlan


@pytest.fixture
def validator() -> LawimConversationPolicyValidator:
    return LawimConversationPolicyValidator()


@pytest.fixture
def plan() -> DialoguePlan:
    return DialoguePlan(language="fr", dialogue_act="ACKNOWLEDGE_AND_ASK")


class TestForbiddenPhrases:
    def test_neutral_assistant_rejected(self, validator: LawimConversationPolicyValidator, plan: DialoguePlan) -> None:
        response, status = validator.validate("Je suis un assistant neutre.", plan)
        assert status == "REPAIR"

    def test_neutral_assistant_english_rejected(self, validator: LawimConversationPolicyValidator, plan: DialoguePlan) -> None:
        response, status = validator.validate("I am a neutral assistant.", plan)
        assert status == "REPAIR"

    def test_business_decision_refusal_rejected(self, validator: LawimConversationPolicyValidator, plan: DialoguePlan) -> None:
        response, status = validator.validate("Je ne peux pas prendre de décisions commerciales.", plan)
        assert status == "REPAIR"

    def test_how_can_i_help_allowed_in_welcome(self, validator: LawimConversationPolicyValidator) -> None:
        welcome_plan = DialoguePlan(dialogue_act="WELCOME")
        response, status = validator.validate("How can I help you today?", welcome_plan)
        assert status == "PASS"

    def test_how_can_i_help_rejected_in_other_acts(self, validator: LawimConversationPolicyValidator, plan: DialoguePlan) -> None:
        response, status = validator.validate("How can I help you today?", plan)
        assert status == "REPAIR"


class TestExternalReferrals:
    def test_jumia_rejected(self, validator: LawimConversationPolicyValidator, plan: DialoguePlan) -> None:
        response, status = validator.validate("Vous pouvez trouver des annonces sur Jumia.", plan)
        assert status == "REPAIR"

    def test_seloger_rejected(self, validator: LawimConversationPolicyValidator, plan: DialoguePlan) -> None:
        response, status = validator.validate("Consultez SeLoger pour plus d'offres.", plan)
        assert status == "REPAIR"

    def test_leboncoin_rejected(self, validator: LawimConversationPolicyValidator, plan: DialoguePlan) -> None:
        response, status = validator.validate("Regardez sur Leboncoin.", plan)
        assert status == "REPAIR"


class TestTranslationMarkers:
    def test_french_for_rejected(self, validator: LawimConversationPolicyValidator, plan: DialoguePlan) -> None:
        response, status = validator.validate("The French for apartment is appartement.", plan)
        assert status == "REPAIR"

    def test_in_english_rejected(self, validator: LawimConversationPolicyValidator, plan: DialoguePlan) -> None:
        response, status = validator.validate("In English this is called a house.", plan)
        assert status == "REPAIR"


class TestGrammarCorrection:
    def test_correct_spelling_rejected(self, validator: LawimConversationPolicyValidator, plan: DialoguePlan) -> None:
        response, status = validator.validate("The correct spelling is appartement.", plan)
        assert status == "REPAIR"

    def test_correct_phrasing_rejected(self, validator: LawimConversationPolicyValidator, plan: DialoguePlan) -> None:
        response, status = validator.validate("The correct phrasing would be...", plan)
        assert status == "REPAIR"


class TestQuestionCount:
    def test_exceeds_max_questions(self, validator: LawimConversationPolicyValidator) -> None:
        plan = DialoguePlan(maximum_questions=0)
        response, status = validator.validate("Voulez-vous acheter? Voulez-vous louer?", plan)
        assert status == "REPAIR"

    def test_allows_one_question(self, validator: LawimConversationPolicyValidator) -> None:
        plan = DialoguePlan(maximum_questions=1)
        response, status = validator.validate("Quel est votre budget?", plan)
        assert status == "PASS"


class TestBlocking:
    def test_empty_response_blocked(self, validator: LawimConversationPolicyValidator, plan: DialoguePlan) -> None:
        response, status = validator.validate("", plan)
        assert status == "BLOCK"

    def test_whitespace_only_blocked(self, validator: LawimConversationPolicyValidator, plan: DialoguePlan) -> None:
        response, status = validator.validate("   ", plan)
        assert status == "BLOCK"
