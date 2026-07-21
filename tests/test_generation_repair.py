from __future__ import annotations

import json
import unittest

from lawim_v2.validation.business import BusinessValidator
from lawim_v2.validation.conversation import ConversationValidator
from lawim_v2.validation.repair import RepairHandler
from lawim_v2.validation.structural import StructuralValidator


class _MockRequest:
    def __init__(self, language: str = "fr", maximum_length: int = 500):
        self.language = language
        self.maximum_length = maximum_length


class _MockDialoguePlan:
    def __init__(self, next_question_key: str = "", dialogue_act: str = ""):
        self.next_question_key = next_question_key
        self.dialogue_act = dialogue_act


class TestRepairHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.structural = StructuralValidator()
        self.business = BusinessValidator()
        self.conversation = ConversationValidator()
        self.repairer = RepairHandler(self.structural, self.business, self.conversation)
        self.request = _MockRequest(language="fr")

    def test_repair_non_json_content(self) -> None:
        raw = "Bonjour, je suis LAWIM AI. Comment puis-je vous aider ?"
        repaired, success = self.repairer.repair(raw, self.request)
        self.assertIsNotNone(repaired, "Expected repair to succeed")
        self.assertTrue(success)
        parsed = json.loads(repaired)
        self.assertIn("Bonjour", parsed["content"])
        self.assertEqual(parsed["language"], "fr")
        self.assertEqual(parsed["dialogue_act"], "ACKNOWLEDGE_AND_ASK")

    def test_repair_non_json_content_with_question(self) -> None:
        raw = "Quel est votre budget pour ce projet ?"
        repaired, success = self.repairer.repair(raw, self.request)
        self.assertIsNotNone(repaired)
        self.assertTrue(success)
        parsed = json.loads(repaired)
        self.assertIn("budget", parsed["content"])
        self.assertGreaterEqual(parsed["question_count"], 1)

    def test_repair_non_json_empty_returns_none(self) -> None:
        raw = "  "
        repaired, success = self.repairer.repair(raw, self.request)
        self.assertIsNone(repaired)
        self.assertFalse(success)

    def test_repair_non_json_single_char_returns_none(self) -> None:
        raw = "A"
        repaired, success = self.repairer.repair(raw, self.request)
        self.assertIsNone(repaired)
        self.assertFalse(success)

    def test_repair_missing_fields(self) -> None:
        raw = '{"content": "Bonjour"}'
        repaired, success = self.repairer.repair(raw, self.request)
        self.assertIsNone(repaired)
        self.assertFalse(success)

    def test_repair_wrong_language(self) -> None:
        raw = json.dumps({
            "content": "Hello",
            "language": "de",
            "dialogue_act": "WELCOME",
            "question_count": 0,
        })
        repaired, success = self.repairer.repair(raw, self.request)
        self.assertIsNone(repaired)
        self.assertFalse(success)

    def test_repair_forbidden_content_neutral_assistant(self) -> None:
        raw = json.dumps({
            "content": "I am a neutral assistant and cannot make business decisions.",
            "language": "fr",
            "dialogue_act": "WELCOME",
            "question_count": 0,
        })
        repaired, success = self.repairer.repair(raw, self.request)
        self.assertIsNotNone(repaired)
        self.assertTrue(success)
        parsed = json.loads(repaired)
        self.assertNotIn("neutral assistant", parsed["content"])

    def test_repair_forbidden_content_external_referral(self) -> None:
        raw = json.dumps({
            "content": "Check Jumia for more listings.",
            "language": "en",
            "dialogue_act": "SEARCH_READY",
            "question_count": 0,
        })
        repaired, success = self.repairer.repair(raw, self.request)
        self.assertIsNotNone(repaired)
        self.assertTrue(success)
        parsed = json.loads(repaired)
        self.assertNotIn("Jumia", parsed["content"])

    def test_repair_removes_forbidden_sentence_keeps_rest(self) -> None:
        raw = json.dumps({
            "content": "Voici les biens disponibles. Consultez SeLoger pour plus d'options. Quel est votre budget ?",
            "language": "fr",
            "dialogue_act": "ACKNOWLEDGE_AND_ASK",
            "question_count": 1,
        })
        repaired, success = self.repairer.repair(raw, self.request)
        self.assertIsNotNone(repaired)
        self.assertTrue(success)
        parsed = json.loads(repaired)
        self.assertNotIn("SeLoger", parsed["content"])
        self.assertIn("budget", parsed["content"])

    def test_repair_never_changes_business_logic(self) -> None:
        raw = json.dumps({
            "content": "J'ai noté votre recherche de maison à Douala. Quel est votre budget ?",
            "language": "fr",
            "dialogue_act": "ACKNOWLEDGE_AND_ASK",
            "question_count": 1,
        })
        repaired, success = self.repairer.repair(raw, self.request)
        self.assertIsNotNone(repaired)
        self.assertTrue(success)
        parsed = json.loads(repaired)
        self.assertEqual(parsed["dialogue_act"], "ACKNOWLEDGE_AND_ASK")
        self.assertEqual(parsed["language"], "fr")
        self.assertEqual(parsed["question_count"], 1)

    def test_repair_failure_returns_none_for_missing_all_fields(self) -> None:
        raw = json.dumps({
            "content": "Test",
            "language": "fr",
            "dialogue_act": "WELCOME",
            "question_count": 0,
        })
        repaired, success = self.repairer.repair(raw, self.request)
        self.assertIsNotNone(repaired)
        self.assertTrue(success)

    def test_repair_dialogue_plan_with_forbidden_content(self) -> None:
        raw = json.dumps({
            "content": "Provide more context for your request please.",
            "language": "en",
            "dialogue_act": "ACKNOWLEDGE_AND_ASK",
            "question_count": 0,
        })
        dialogue_plan = _MockDialoguePlan(dialogue_act="ACKNOWLEDGE_AND_ASK")
        repaired, success = self.repairer.repair(raw, self.request, dialogue_plan)
        self.assertIsNotNone(repaired)
        self.assertTrue(success)
        parsed = json.loads(repaired)
        self.assertNotIn("provide more context", parsed["content"].lower())


if __name__ == "__main__":
    unittest.main()
