from __future__ import annotations

import unittest

from lawim_v2.validation.business import BusinessValidator


class _MockRequest:
    def __init__(self, known_facts: dict | None = None):
        self.known_facts = known_facts or {}


class _MockDialoguePlan:
    def __init__(self, next_question_key: str = "", dialogue_act: str = ""):
        self.next_question_key = next_question_key
        self.dialogue_act = dialogue_act


class TestBusinessValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = BusinessValidator()

    def test_valid_response_passes(self) -> None:
        response_json = {
            "content": "J'ai noté votre recherche à Douala. Quel est votre budget ?",
            "dialogue_act": "ACKNOWLEDGE_AND_ASK",
            "question_count": 1,
            "language": "fr",
        }
        request = _MockRequest(known_facts={"city": "Douala"})
        dialogue_plan = _MockDialoguePlan(
            next_question_key="budget",
            dialogue_act="ACKNOWLEDGE_AND_ASK",
        )
        valid, errors = self.validator.validate(response_json, request, dialogue_plan)
        self.assertTrue(valid, f"Expected valid, got errors: {errors}")

    def test_valid_no_question_response(self) -> None:
        response_json = {
            "content": "Merci pour ces informations.",
            "dialogue_act": "ACKNOWLEDGE",
            "question_count": 0,
            "language": "fr",
        }
        request = _MockRequest()
        dialogue_plan = _MockDialoguePlan()
        valid, errors = self.validator.validate(response_json, request, dialogue_plan)
        self.assertTrue(valid, f"Expected valid, got errors: {errors}")

    def test_valid_english(self) -> None:
        response_json = {
            "content": "I noted your search in Douala. What is your budget?",
            "dialogue_act": "ACKNOWLEDGE_AND_ASK",
            "question_count": 1,
            "language": "en",
        }
        request = _MockRequest(known_facts={"city": "Douala"})
        dialogue_plan = _MockDialoguePlan(
            next_question_key="budget",
            dialogue_act="ACKNOWLEDGE_AND_ASK",
        )
        valid, errors = self.validator.validate(response_json, request, dialogue_plan)
        self.assertTrue(valid, f"Expected valid, got errors: {errors}")

    def test_two_questions_in_content(self) -> None:
        response_json = {
            "content": "Quel est votre budget ? Et quelle ville préférez-vous ?",
            "dialogue_act": "ACKNOWLEDGE_AND_ASK",
            "question_count": 2,
            "language": "fr",
        }
        request = _MockRequest()
        dialogue_plan = _MockDialoguePlan()
        valid, errors = self.validator.validate(response_json, request, dialogue_plan)
        self.assertFalse(valid)
        self.assertTrue(any("question" in e.lower() and "2" in e for e in errors))

    def test_no_request_known_facts_empty(self) -> None:
        response_json = {
            "content": "Bonjour",
            "dialogue_act": "WELCOME",
            "question_count": 0,
            "language": "fr",
        }
        request = None
        dialogue_plan = None
        valid, errors = self.validator.validate(response_json, request, dialogue_plan)
        self.assertTrue(valid, f"Expected valid, got errors: {errors}")

    def test_empty_content_passes(self) -> None:
        response_json = {
            "content": "",
            "dialogue_act": "WELCOME",
            "question_count": 0,
            "language": "fr",
        }
        request = _MockRequest()
        dialogue_plan = _MockDialoguePlan()
        valid, errors = self.validator.validate(response_json, request, dialogue_plan)
        self.assertTrue(valid, f"Expected valid, got errors: {errors}")

    def test_single_question_passes(self) -> None:
        response_json = {
            "content": "Quel est votre budget ?",
            "dialogue_act": "ACKNOWLEDGE_AND_ASK",
            "question_count": 1,
            "language": "fr",
        }
        request = _MockRequest()
        dialogue_plan = _MockDialoguePlan()
        valid, errors = self.validator.validate(response_json, request, dialogue_plan)
        self.assertTrue(valid, f"Expected valid, got errors: {errors}")


if __name__ == "__main__":
    unittest.main()
