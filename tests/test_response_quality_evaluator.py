from __future__ import annotations

import unittest

from lawim_v2.validation.quality import ResponseQualityEvaluator


class _MockRequest:
    pass


class TestResponseQualityEvaluator(unittest.TestCase):
    def setUp(self) -> None:
        self.evaluator = ResponseQualityEvaluator()
        self.request = _MockRequest()

    def test_perfect_response(self) -> None:
        content = "J'ai noté votre recherche de maison à Douala. Quel est votre budget ?"
        score, details = self.evaluator.evaluate(content, self.request)
        self.assertGreaterEqual(score, 0.6)
        self.assertIn("accuracy", details)
        self.assertIn("relevance", details)
        self.assertIn("conciseness", details)
        self.assertIn("clarity", details)

    def test_low_quality_response_empty(self) -> None:
        content = ""
        score, details = self.evaluator.evaluate(content, self.request)
        self.assertAlmostEqual(score, 0.0)

    def test_low_quality_response_gibberish(self) -> None:
        content = "lol omg wtf btw idk stfu"
        score, details = self.evaluator.evaluate(content, self.request)
        self.assertLess(details["professional_tone"], 1.0)

    def test_is_acceptable_above_threshold(self) -> None:
        content = "Bonjour, je suis LAWIM AI. Comment puis-je vous aider aujourd'hui ?"
        acceptable = self.evaluator.is_acceptable(content, self.request, threshold=0.5)
        self.assertTrue(acceptable)

    def test_is_acceptable_below_threshold(self) -> None:
        content = ""
        acceptable = self.evaluator.is_acceptable(content, self.request, threshold=0.5)
        self.assertFalse(acceptable)

    def test_custom_threshold(self) -> None:
        content = "Bonjour"
        acceptable_low = self.evaluator.is_acceptable(content, self.request, threshold=0.1)
        acceptable_high = self.evaluator.is_acceptable(content, self.request, threshold=0.99)
        self.assertTrue(acceptable_low)
        self.assertFalse(acceptable_high)

    def test_conciseness_scoring(self) -> None:
        short = "Bonjour LAWIM AI."
        short_score, _ = self.evaluator.evaluate(short, self.request)
        long = " ".join(["word"] * 200)
        long_score, _ = self.evaluator.evaluate(long, self.request)
        self.assertGreaterEqual(short_score, long_score)

    def test_professional_tone_detects_unprofessional(self) -> None:
        content = "lol check this property omg"
        score, details = self.evaluator.evaluate(content, self.request)
        self.assertLess(details["professional_tone"], 1.0)

    def test_professional_tone_clean(self) -> None:
        content = "Je vous propose une visite du bien demain."
        score, details = self.evaluator.evaluate(content, self.request)
        self.assertEqual(details["professional_tone"], 1.0)

    def test_clarity_scoring(self) -> None:
        clear = "Bonjour. Voici le bien. Quel est votre budget ?"
        clear_score, _ = self.evaluator.evaluate(clear, self.request)
        verbose = " ".join(["A"] * 100) + "."
        verbose_score, _ = self.evaluator.evaluate(verbose, self.request)
        self.assertGreaterEqual(clear_score, verbose_score)

    def test_evaluate_returns_details(self) -> None:
        content = "Bonjour LAWIM AI"
        score, details = self.evaluator.evaluate(content, self.request)
        expected_criteria = {
            "accuracy", "relevance", "conciseness", "clarity",
            "naturalness", "professional_tone", "language_consistency",
            "no_jargon",
        }
        self.assertEqual(set(details.keys()), expected_criteria)

    def test_default_threshold_is_0_6(self) -> None:
        content = "Bonjour LAWIM AI"
        acceptable = self.evaluator.is_acceptable(content, self.request)
        score, _ = self.evaluator.evaluate(content, self.request)
        self.assertEqual(acceptable, score >= 0.6)


if __name__ == "__main__":
    unittest.main()
