from __future__ import annotations

import pytest

from lawim_v2.conversation.policy.language_policy import LawimLanguagePolicy


@pytest.fixture
def policy() -> LawimLanguagePolicy:
    return LawimLanguagePolicy()


class TestDetectLanguage:
    def test_detect_french(self, policy: LawimLanguagePolicy) -> None:
        assert policy.detect_language("Bonjour je cherche un appartement") == "fr"
        assert policy.detect_language("Merci beaucoup pour votre aide") == "fr"

    def test_detect_english(self, policy: LawimLanguagePolicy) -> None:
        assert policy.detect_language("Hello I am looking for an apartment") == "en"
        assert policy.detect_language("Thank you for your help") == "en"

    def test_detect_pcm(self, policy: LawimLanguagePolicy) -> None:
        assert policy.detect_language("Wetin you dey find for property") == "pcm"

    def test_detect_none_on_empty(self, policy: LawimLanguagePolicy) -> None:
        assert policy.detect_language("") is None

    def test_detect_none_on_gibberish(self, policy: LawimLanguagePolicy) -> None:
        assert policy.detect_language("xyz 123") is None


class TestShouldSwitch:
    def test_fr_with_no_detection_stays_fr(self, policy: LawimLanguagePolicy) -> None:
        assert policy.should_switch("fr", None, "xyz") is False

    def test_fr_with_detected_english_but_single_word(
        self, policy: LawimLanguagePolicy
    ) -> None:
        assert policy.should_switch("fr", "en", "hello", 0) is False

    def test_fr_english_after_multiple_messages(
        self, policy: LawimLanguagePolicy
    ) -> None:
        assert policy.should_switch("fr", "en", "I am looking for a house", 2) is True

    def test_fr_english_below_threshold(
        self, policy: LawimLanguagePolicy
    ) -> None:
        assert policy.should_switch("fr", "en", "I want this", 1) is False

    def test_fr_user_explicitly_refuses_english(
        self, policy: LawimLanguagePolicy
    ) -> None:
        msg = "I don't understand English. Je parle français."
        assert policy.should_switch("fr", "en", msg, 2) is False

    def test_same_language_no_switch(self, policy: LawimLanguagePolicy) -> None:
        assert policy.should_switch("fr", "fr", "Bonjour", 0) is False


class TestTranslation:
    def test_is_translation_french_for(self, policy: LawimLanguagePolicy) -> None:
        assert policy.is_translation("What is the French for apartment?") is True

    def test_is_translation_in_english(self, policy: LawimLanguagePolicy) -> None:
        assert policy.is_translation("Say this in English") is True

    def test_not_translation(self, policy: LawimLanguagePolicy) -> None:
        assert policy.is_translation("Je cherche un appartement") is False


class TestGrammarCorrection:
    def test_is_grammar_correction(self, policy: LawimLanguagePolicy) -> None:
        assert policy.is_grammar_correction("The correct spelling is...") is True
        assert policy.is_grammar_correction("Vous avez écrit...") is True

    def test_not_grammar_correction(self, policy: LawimLanguagePolicy) -> None:
        assert policy.is_grammar_correction("Je cherche un bien") is False
