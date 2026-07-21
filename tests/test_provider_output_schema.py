from __future__ import annotations

import json
import unittest

from lawim_v2.contracts.schema import GENERATION_RESPONSE_SCHEMA, validate_response_json


class TestProviderOutputSchema(unittest.TestCase):
    def test_valid_response_passes(self) -> None:
        payload = {
            "content": "Bonjour ! Je suis LAWIM AI.",
            "language": "fr",
            "dialogue_act": "WELCOME",
            "question_count": 0,
            "confidence": 0.95,
        }
        valid, error, parsed = validate_response_json(json.dumps(payload))
        self.assertTrue(valid, f"Expected valid, got error: {error}")
        self.assertEqual(error, "")
        self.assertIsNotNone(parsed)

    def test_valid_english_passes(self) -> None:
        payload = {
            "content": "Hello! I am LAWIM AI.",
            "language": "en",
            "dialogue_act": "WELCOME",
            "question_count": 0,
        }
        valid, error, parsed = validate_response_json(json.dumps(payload))
        self.assertTrue(valid, f"Expected valid, got error: {error}")

    def test_valid_pcm_passes(self) -> None:
        payload = {
            "content": "Weldone! I be LAWIM AI.",
            "language": "pcm",
            "dialogue_act": "WELCOME",
            "question_count": 0,
        }
        valid, error, parsed = validate_response_json(json.dumps(payload))
        self.assertTrue(valid, f"Expected valid, got error: {error}")

    def test_valid_acknowledge_and_ask(self) -> None:
        payload = {
            "content": "J'ai noté votre recherche. Quel est votre budget ?",
            "language": "fr",
            "dialogue_act": "ACKNOWLEDGE_AND_ASK",
            "question_count": 1,
        }
        valid, error, parsed = validate_response_json(json.dumps(payload))
        self.assertTrue(valid, f"Expected valid, got error: {error}")

    def test_invalid_json_fails(self) -> None:
        valid, error, parsed = validate_response_json("not json at all")
        self.assertFalse(valid)
        self.assertIn("Invalid JSON", error)
        self.assertIsNone(parsed)

    def test_invalid_json_empty_string(self) -> None:
        valid, error, parsed = validate_response_json("")
        self.assertFalse(valid)
        self.assertIn("Invalid JSON", error)

    def test_missing_required_field(self) -> None:
        payload = {
            "content": "Bonjour",
            "language": "fr",
            "question_count": 0,
        }
        valid, error, parsed = validate_response_json(json.dumps(payload))
        self.assertFalse(valid)
        self.assertIn("dialogue_act", error)

    def test_missing_content_field(self) -> None:
        payload = {
            "language": "fr",
            "dialogue_act": "WELCOME",
            "question_count": 0,
        }
        valid, error, parsed = validate_response_json(json.dumps(payload))
        self.assertFalse(valid)
        self.assertIn("content", error)

    def test_wrong_language(self) -> None:
        payload = {
            "content": "Bonjour",
            "language": "de",
            "dialogue_act": "WELCOME",
            "question_count": 0,
        }
        valid, error, parsed = validate_response_json(json.dumps(payload))
        self.assertFalse(valid)
        self.assertIn("de", error)
        self.assertIn("language", error)

    def test_invalid_dialogue_act(self) -> None:
        payload = {
            "content": "Bonjour",
            "language": "fr",
            "dialogue_act": "INVALID_ACT",
            "question_count": 0,
        }
        valid, error, parsed = validate_response_json(json.dumps(payload))
        self.assertFalse(valid)
        self.assertIn("INVALID_ACT", error)

    def test_question_count_exceeds_max(self) -> None:
        payload = {
            "content": "Bonjour",
            "language": "fr",
            "dialogue_act": "WELCOME",
            "question_count": 5,
        }
        valid, error, parsed = validate_response_json(json.dumps(payload))
        self.assertFalse(valid)
        self.assertIn("5", error)
        self.assertIn("question_count", error)

    def test_question_count_zero_is_valid(self) -> None:
        payload = {
            "content": "Bonjour",
            "language": "fr",
            "dialogue_act": "WELCOME",
            "question_count": 0,
        }
        valid, error, parsed = validate_response_json(json.dumps(payload))
        self.assertTrue(valid, f"Expected valid, got error: {error}")

    def test_additional_properties_rejected(self) -> None:
        payload = {
            "content": "Bonjour",
            "language": "fr",
            "dialogue_act": "WELCOME",
            "question_count": 0,
            "extra_field": "should not be here",
        }
        valid, error, parsed = validate_response_json(json.dumps(payload))
        self.assertFalse(valid)
        self.assertIn("extra_field", error)

    def test_empty_content_rejected(self) -> None:
        payload = {
            "content": "",
            "language": "fr",
            "dialogue_act": "WELCOME",
            "question_count": 0,
        }
        valid, error, parsed = validate_response_json(json.dumps(payload))
        self.assertFalse(valid)
        self.assertIn("content", error)

    def test_confidence_out_of_range(self) -> None:
        payload = {
            "content": "Bonjour",
            "language": "fr",
            "dialogue_act": "WELCOME",
            "question_count": 0,
            "confidence": 1.5,
        }
        valid, error, parsed = validate_response_json(json.dumps(payload))
        self.assertFalse(valid)
        self.assertIn("1.5", error)

    def test_confidence_negative(self) -> None:
        payload = {
            "content": "Bonjour",
            "language": "fr",
            "dialogue_act": "WELCOME",
            "question_count": 0,
            "confidence": -0.1,
        }
        valid, error, parsed = validate_response_json(json.dumps(payload))
        self.assertFalse(valid)
        self.assertIn("-0.1", error)

    def test_root_is_not_object(self) -> None:
        valid, error, parsed = validate_response_json('["not", "an", "object"]')
        self.assertFalse(valid)
        self.assertIn("object", error.lower())


class TestSchemaStructure(unittest.TestCase):
    def test_schema_required_fields(self) -> None:
        required = GENERATION_RESPONSE_SCHEMA.get("required", [])
        self.assertIn("content", required)
        self.assertIn("language", required)
        self.assertIn("dialogue_act", required)
        self.assertIn("question_count", required)

    def test_schema_languages(self) -> None:
        lang_enum = GENERATION_RESPONSE_SCHEMA["properties"]["language"]["enum"]
        self.assertIn("fr", lang_enum)
        self.assertIn("en", lang_enum)
        self.assertIn("pcm", lang_enum)

    def test_schema_dialogue_acts(self) -> None:
        acts = GENERATION_RESPONSE_SCHEMA["properties"]["dialogue_act"]["enum"]
        self.assertIn("WELCOME", acts)
        self.assertIn("HANDOVER", acts)
        self.assertIn("CONTROLLED_ERROR", acts)
        self.assertIn("ACKNOWLEDGE_AND_ASK", acts)
        self.assertIn("SEARCH_READY", acts)
        self.assertIn("PUBLICATION_READY", acts)
        self.assertIn("VISIT_READY", acts)
        self.assertIn("TRANSACTION_READY", acts)


if __name__ == "__main__":
    unittest.main()
