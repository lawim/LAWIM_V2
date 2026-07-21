from __future__ import annotations

import unittest

from lawim_v2.ai.internal_reasoning import InternalReasoningEngine, ReasoningContext


class _MockConfig:
    ai_total_timeout_seconds = 30
    ai_max_context_messages = 20
    ai_primary_provider = "deepseek"
    ai_complex_provider = "openai"
    ai_fallback_chain = ("deepseek", "openai", "gemini_primary", "gemini_secondary")
    ai_request_timeout_seconds = 5
    ai_provider_deepseek_enabled = True
    ai_provider_openai_enabled = True
    ai_provider_gemini_primary_enabled = True
    ai_provider_gemini_secondary_enabled = True
    deepseek_api_key = "test"
    deepseek_model = "test"
    deepseek_base_url = "https://test.com"
    openai_api_key = "test"
    openai_model = "test"
    gemini_primary_api_key = "test"
    gemini_primary_model = "test"
    gemini_secondary_api_key = "test"
    gemini_secondary_model = "test"


class _MockRepository:
    def search_properties(self, **kw):
        return []
    def get_ai_disclaimer_config(self):
        return None


class TestInternalFallbackGeneration(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = _MockRepository()
        self.config = _MockConfig()
        self.engine = InternalReasoningEngine(self.repo, self.config)

    def test_internal_fallback_returns_valid_response(self) -> None:
        ctx = ReasoningContext(
            user_text="Je cherche un appartement à Douala",
            language="fr",
        )
        resp = self.engine.reason(ctx)
        self.assertTrue(len(resp.content) > 0)
        self.assertIsInstance(resp.content, str)
        self.assertGreaterEqual(resp.confidence, 0.0)

    def test_internal_fallback_properly_formatted(self) -> None:
        ctx = ReasoningContext(
            user_text="Bonjour",
            language="fr",
        )
        resp = self.engine.reason(ctx)
        self.assertIn("LAWIM", resp.content)
        self.assertGreaterEqual(resp.confidence, 0.5)

    def test_internal_fallback_all_languages_french(self) -> None:
        ctx = ReasoningContext(
            user_text="Bonjour",
            language="fr",
        )
        resp = self.engine.reason(ctx)
        self.assertIn("Bonjour", resp.content)

    def test_internal_fallback_all_languages_english(self) -> None:
        ctx = ReasoningContext(
            user_text="Hello",
            language="en",
        )
        resp = self.engine.reason(ctx)
        self.assertIn("Hello", resp.content)

    def test_internal_fallback_property_search(self) -> None:
        ctx = ReasoningContext(
            user_text="Je cherche une maison à Douala avec un budget de 100 000 FCFA",
            language="fr",
            property_criteria={"city": "Douala", "property_type": "house"},
        )
        resp = self.engine.reason(ctx)
        self.assertTrue(len(resp.content) > 0)

    def test_internal_fallback_qualification(self) -> None:
        ctx = ReasoningContext(
            user_text="Je veux évaluer mon projet immobilier",
            language="fr",
        )
        resp = self.engine.reason(ctx)
        self.assertTrue(len(resp.content) > 0)

    def test_internal_fallback_farewell(self) -> None:
        ctx = ReasoningContext(
            user_text="Merci au revoir",
            language="fr",
        )
        resp = self.engine.reason(ctx)
        self.assertIn("Merci", resp.content)

    def test_internal_fallback_empty_text(self) -> None:
        ctx = ReasoningContext(user_text="", language="fr")
        resp = self.engine.reason(ctx)
        self.assertTrue(len(resp.content) > 0)
        self.assertIn("LAWIM", resp.content)


if __name__ == "__main__":
    unittest.main()
