from __future__ import annotations

import json
import unittest
from types import SimpleNamespace

from lawim_v2.validation.structural import StructuralValidator


class _MockRequest:
    def __init__(self, maximum_length: int = 500):
        self.maximum_length = maximum_length


class TestStructuralValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = StructuralValidator()
        self.valid_request = _MockRequest(maximum_length=500)

    def test_valid_response(self) -> None:
        data = {
            "content": "Bonjour, je suis LAWIM AI.",
            "language": "fr",
            "dialogue_act": "WELCOME",
            "question_count": 0,
        }
        valid, errors = self.validator.validate(json.dumps(data), self.valid_request)
        self.assertTrue(valid, f"Expected valid, got errors: {errors}")

    def test_invalid_json(self) -> None:
        valid, errors = self.validator.validate("not json", self.valid_request)
        self.assertFalse(valid)
        self.assertTrue(any("Invalid JSON" in e for e in errors))

    def test_invalid_json_empty_string(self) -> None:
        valid, errors = self.validator.validate("", self.valid_request)
        self.assertFalse(valid)
        self.assertTrue(any("Invalid JSON" in e for e in errors))

    def test_missing_fields(self) -> None:
        data = {"content": "Bonjour"}
        valid, errors = self.validator.validate(json.dumps(data), self.valid_request)
        self.assertFalse(valid)
        field_names = {e.split(":")[-1].strip() if ":" in e else e for e in errors}
        self.assertTrue(
            any("dialogue_act" in e for e in errors),
            f"Expected dialogue_act error, got {errors}",
        )
        self.assertTrue(
            any("language" in e for e in errors),
            f"Expected language error, got {errors}",
        )

    def test_wrong_types(self) -> None:
        data = {
            "content": "Bonjour",
            "language": 123,
            "dialogue_act": "WELCOME",
            "question_count": 0,
        }
        valid, errors = self.validator.validate(json.dumps(data), self.valid_request)
        self.assertFalse(valid)
        self.assertTrue(
            any("language" in e and "string" in e.lower() for e in errors),
            f"Expected language type error, got {errors}",
        )

    def test_empty_content(self) -> None:
        data = {
            "content": "",
            "language": "fr",
            "dialogue_act": "WELCOME",
            "question_count": 0,
        }
        valid, errors = self.validator.validate(json.dumps(data), self.valid_request)
        self.assertFalse(valid)
        self.assertTrue(any("empty" in e.lower() for e in errors))

    def test_content_whitespace_only(self) -> None:
        data = {
            "content": "   ",
            "language": "fr",
            "dialogue_act": "WELCOME",
            "question_count": 0,
        }
        valid, errors = self.validator.validate(json.dumps(data), self.valid_request)
        self.assertFalse(valid)
        self.assertTrue(any("empty" in e.lower() for e in errors))

    def test_unsupported_language(self) -> None:
        data = {
            "content": "Bonjour",
            "language": "de",
            "dialogue_act": "WELCOME",
            "question_count": 0,
        }
        valid, errors = self.validator.validate(json.dumps(data), self.valid_request)
        self.assertFalse(valid)
        self.assertTrue(any("de" in e for e in errors))

    def test_invalid_dialogue_act(self) -> None:
        data = {
            "content": "Bonjour",
            "language": "fr",
            "dialogue_act": "INVALID_ACT",
            "question_count": 0,
        }
        valid, errors = self.validator.validate(json.dumps(data), self.valid_request)
        self.assertFalse(valid)
        self.assertTrue(any("INVALID_ACT" in e for e in errors))

    def test_question_count_defaults_to_1(self) -> None:
        data = {
            "content": "Question 1 ? Question 2 ?",
            "language": "fr",
            "dialogue_act": "ACKNOWLEDGE_AND_ASK",
            "question_count": 2,
        }
        valid, errors = self.validator.validate(json.dumps(data), self.valid_request)
        self.assertFalse(valid)
        self.assertTrue(any("question_count" in e for e in errors))

    def test_response_too_long(self) -> None:
        content = "A" * 600
        data = {
            "content": content,
            "language": "fr",
            "dialogue_act": "WELCOME",
            "question_count": 0,
        }
        request = _MockRequest(maximum_length=500)
        valid, errors = self.validator.validate(json.dumps(data), request)
        self.assertFalse(valid)
        self.assertTrue(any("length" in e.lower() for e in errors))
        self.assertTrue(any("600" in e for e in errors))

    def test_valid_acknowledge_and_ask(self) -> None:
        data = {
            "content": "J'ai noté votre budget. Quelle est votre ville préférée ?",
            "language": "fr",
            "dialogue_act": "ACKNOWLEDGE_AND_ASK",
            "question_count": 1,
        }
        valid, errors = self.validator.validate(json.dumps(data), self.valid_request)
        self.assertTrue(valid, f"Expected valid, got errors: {errors}")

    def test_valid_handover_act(self) -> None:
        data = {
            "content": "Je transfère votre demande au service compétent.",
            "language": "fr",
            "dialogue_act": "HANDOVER",
            "question_count": 0,
        }
        valid, errors = self.validator.validate(json.dumps(data), self.valid_request)
        self.assertTrue(valid, f"Expected valid, got errors: {errors}")

    def test_valid_controlled_error(self) -> None:
        data = {
            "content": "Désolé, je n'ai pas pu traiter votre demande.",
            "language": "fr",
            "dialogue_act": "CONTROLLED_ERROR",
            "question_count": 0,
        }
        valid, errors = self.validator.validate(json.dumps(data), self.valid_request)
        self.assertTrue(valid, f"Expected valid, got errors: {errors}")

    def test_question_count_exceeds_default_max(self) -> None:
        data = {
            "content": "A",
            "language": "fr",
            "dialogue_act": "ACKNOWLEDGE_AND_ASK",
            "question_count": 2,
        }
        valid, errors = self.validator.validate(json.dumps(data), self.valid_request)
        self.assertFalse(valid)
        self.assertTrue(any("2" in e for e in errors))

    def test_question_count_zero_with_no_questions(self) -> None:
        data = {
            "content": "Merci pour ces informations.",
            "language": "fr",
            "dialogue_act": "SUMMARIZE_AND_CONFIRM",
            "question_count": 0,
        }
        valid, errors = self.validator.validate(json.dumps(data), self.valid_request)
        self.assertTrue(valid, f"Expected valid, got errors: {errors}")

    def test_request_none_fallback_to_500(self) -> None:
        data = {
            "content": "A" * 600,
            "language": "fr",
            "dialogue_act": "WELCOME",
            "question_count": 0,
        }
        valid, errors = self.validator.validate(json.dumps(data), None)
        self.assertFalse(valid)
        self.assertTrue(any("600" in e for e in errors))

    def test_response_within_limit(self) -> None:
        data = {
            "content": "Bonjour LAWIM AI",
            "language": "fr",
            "dialogue_act": "WELCOME",
            "question_count": 0,
        }
        valid, errors = self.validator.validate(json.dumps(data), self.valid_request)
        self.assertTrue(valid, f"Expected valid, got errors: {errors}")


if __name__ == "__main__":
    unittest.main()
