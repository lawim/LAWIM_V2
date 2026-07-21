from __future__ import annotations

import unittest

from lawim_v2.validation.conversation import ConversationValidator


class _MockRequest:
    pass


class TestConversationValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = ConversationValidator()
        self.request = _MockRequest()

    def test_no_neutral_assistant(self) -> None:
        content = "I am a neutral assistant and cannot make business decisions."
        valid, errors = self.validator.validate(content, self.request)
        self.assertFalse(valid)
        self.assertTrue(any("neutral assistant" in e.lower() for e in errors))

    def test_no_neutral_assistant_french(self) -> None:
        content = "Je suis un assistant neutre et je ne peux pas prendre de décisions commerciales."
        valid, errors = self.validator.validate(content, self.request)
        self.assertFalse(valid)
        self.assertTrue(any("assistant neutre" in e.lower() for e in errors))
        self.assertTrue(any("neutral" in e.lower() for e in errors) or any("commerciales" in e.lower() for e in errors))

    def test_no_external_referral_jumia(self) -> None:
        content = "Vous pouvez trouver des biens sur Jumia."
        valid, errors = self.validator.validate(content, self.request)
        self.assertFalse(valid)
        self.assertTrue(any("jumia" in e.lower() for e in errors))

    def test_no_external_referral_seloger(self) -> None:
        content = "Consultez SeLoger pour plus d'annonces."
        valid, errors = self.validator.validate(content, self.request)
        self.assertFalse(valid)
        self.assertTrue(any("seloger" in e.lower() for e in errors))

    def test_no_external_referral_leboncoin(self) -> None:
        content = "Regardez sur Leboncoin."
        valid, errors = self.validator.validate(content, self.request)
        self.assertFalse(valid)
        self.assertTrue(any("leboncoin" in e.lower() for e in errors))

    def test_no_external_referral_facebook(self) -> None:
        content = "Rejoignez notre groupe Facebook."
        valid, errors = self.validator.validate(content, self.request)
        self.assertFalse(valid)
        self.assertTrue(any("facebook" in e.lower() for e in errors))

    def test_no_external_referral_lamudi(self) -> None:
        content = "Visitez Lamudi pour plus de choix."
        valid, errors = self.validator.validate(content, self.request)
        self.assertFalse(valid)
        self.assertTrue(any("lamudi" in e.lower() for e in errors))

    def test_no_translation_french_for(self) -> None:
        content = "The French for 'house' is 'maison'."
        valid, errors = self.validator.validate(content, self.request)
        self.assertFalse(valid)
        self.assertTrue(any("french for" in e.lower() for e in errors))

    def test_no_translation_in_english(self) -> None:
        content = "Maison means 'house' in English."
        valid, errors = self.validator.validate(content, self.request)
        self.assertFalse(valid)
        self.assertTrue(any("in english" in e.lower() for e in errors))

    def test_no_translation_francais_signifie(self) -> None:
        content = "Budget, en français signifie budget."
        valid, errors = self.validator.validate(content, self.request)
        self.assertFalse(valid)
        self.assertTrue(any("français signifie" in e.lower() for e in errors))

    def test_no_grammar_correction(self) -> None:
        content = "The correct spelling is 'accommodation'."
        valid, errors = self.validator.validate(content, self.request)
        self.assertFalse(valid)
        self.assertTrue(any("correct spelling" in e.lower() for e in errors))

    def test_no_grammar_correction_french(self) -> None:
        content = "Vous avez écrit 'appartement', la bonne orthographe est 'appartement'."
        valid, errors = self.validator.validate(content, self.request)
        self.assertFalse(valid)
        self.assertTrue(any("bonne orthographe" in e.lower() for e in errors) or any("vous avez écrit" in e.lower() for e in errors))

    def test_no_grammar_correction_wrote(self) -> None:
        content = "You wrote 'appartment' but the correct phrasing is 'apartment'."
        valid, errors = self.validator.validate(content, self.request)
        self.assertFalse(valid)
        self.assertTrue(any("you wrote" in e.lower() for e in errors))

    def test_forbidden_patterns_blocked_multiple(self) -> None:
        content = "I am a neutral assistant. Check Facebook for houses."
        valid, errors = self.validator.validate(content, self.request)
        self.assertFalse(valid)
        self.assertGreaterEqual(len(errors), 2)

    def test_valid_content_passes(self) -> None:
        content = "Bonjour ! Je suis LAWIM AI. Comment puis-je vous aider avec votre projet immobilier aujourd'hui ?"
        valid, errors = self.validator.validate(content, self.request)
        self.assertTrue(valid, f"Expected valid, got errors: {errors}")

    def test_valid_english_content_passes(self) -> None:
        content = "Hello! I am LAWIM AI. How can I help you with your real estate project?"
        valid, errors = self.validator.validate(content, self.request)
        self.assertTrue(valid, f"Expected valid, got errors: {errors}")

    def test_valid_pcm_content_passes(self) -> None:
        content = "How you dey? I be LAWIM. Wetin you want for property?"
        valid, errors = self.validator.validate(content, self.request)
        self.assertTrue(valid, f"Expected valid, got errors: {errors}")

    def test_valid_acknowledge_content_passes(self) -> None:
        content = "J'ai noté votre recherche de maison à Douala."
        valid, errors = self.validator.validate(content, self.request)
        self.assertTrue(valid, f"Expected valid, got errors: {errors}")

    def test_case_insensitive_detection(self) -> None:
        content = "Check out JUMIA House for listings."
        valid, errors = self.validator.validate(content, self.request)
        self.assertFalse(valid)
        self.assertTrue(any("jumia" in e.lower() for e in errors))

    def test_i_cannot_make_business_decisions(self) -> None:
        content = "I cannot make business decisions for you."
        valid, errors = self.validator.validate(content, self.request)
        self.assertFalse(valid)
        self.assertTrue(any("cannot make business decisions" in e.lower() for e in errors))

    def test_provide_more_context(self) -> None:
        content = "Provide more context for your request please."
        valid, errors = self.validator.validate(content, self.request)
        self.assertFalse(valid)
        self.assertTrue(any("provide more context" in e.lower() for e in errors))

    def test_l_orthographe_correcte(self) -> None:
        content = "L'orthographe correcte est 'appartement'."
        valid, errors = self.validator.validate(content, self.request)
        self.assertFalse(valid)
        self.assertTrue(any("l'orthographe correcte" in e.lower() for e in errors))

    def test_the_correct_phrasing(self) -> None:
        content = "The correct phrasing is 'real estate'."
        valid, errors = self.validator.validate(content, self.request)
        self.assertFalse(valid)
        self.assertTrue(any("the correct phrasing" in e.lower() for e in errors))


if __name__ == "__main__":
    unittest.main()
