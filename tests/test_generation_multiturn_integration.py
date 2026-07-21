from __future__ import annotations

import json
import unittest

from lawim_v2.contracts.generation import (
    ControlledGenerationRequest,
    ControlledGenerationResponse,
    GenerationPolicy,
    build_request_from_plan,
    build_response_from_provider,
)
from lawim_v2.contracts.schema import validate_response_json
from lawim_v2.conversation.memory.context_builder import ProviderMemoryContext
from lawim_v2.conversation.policy.dialogue_plan import DialoguePlan
from lawim_v2.conversation.state.state import ResponsePlan
from lawim_v2.validation.business import BusinessValidator
from lawim_v2.validation.conversation import ConversationValidator
from lawim_v2.validation.structural import StructuralValidator


class _MockRequest:
    def __init__(self, language: str = "fr", maximum_length: int = 500):
        self.language = language
        self.maximum_length = maximum_length


class TestGenerationMultiturnIntegration(unittest.TestCase):
    def setUp(self) -> None:
        self.structural = StructuralValidator()
        self.business = BusinessValidator()
        self.conversation = ConversationValidator()

    def _build_and_validate(
        self,
        response_plan: ResponsePlan,
        dialogue_plan: DialoguePlan,
        provider_context: ProviderMemoryContext,
        provider_raw_response: str,
        conversation_id: str = "conv-1",
    ) -> tuple[ControlledGenerationResponse, list[str]]:
        request = build_request_from_plan(
            response_plan=response_plan,
            dialogue_plan=dialogue_plan,
            provider_memory_context=provider_context,
            conversation_id=conversation_id,
        )

        response = build_response_from_provider(
            provider_raw_response=provider_raw_response,
            provider_name="test-provider",
            model="test-model",
            latency_ms=100.0,
            request=request,
        )

        mock_req = _MockRequest(language=request.language)
        struct_valid, struct_errors = self.structural.validate(response.content, mock_req)

        conv_valid, conv_errors = True, []
        if struct_valid or provider_raw_response.startswith("{"):
            try:
                data = json.loads(response.content)
                content = data.get("content", "")
                conv_valid, conv_errors = self.conversation.validate(content, mock_req)
            except (json.JSONDecodeError, TypeError):
                pass

        all_errors = struct_errors + conv_errors
        return response, all_errors

    def test_studio_tour(self) -> None:
        """Tour 1: User asks for studio in Douala -> system asks budget."""
        response_plan = ResponsePlan(
            language="fr",
            response_type="ACKNOWLEDGE_AND_ASK",
            next_question_key="budget",
            next_question_text="Quel est votre budget maximum par mois ?",
            acknowledgement_facts={"city": "Douala", "property_type": "studio"},
            maximum_questions=1,
        )
        dialogue_plan = DialoguePlan(
            language="fr",
            dialogue_act="ACKNOWLEDGE_AND_ASK",
            maximum_questions=1,
        )
        provider_context = ProviderMemoryContext(
            language="fr",
            intent="rental_search",
            active_facts={"city": "Douala", "property_type": "studio"},
            last_question_text="Quel type de bien recherchez-vous ?",
        )

        raw = json.dumps({
            "content": "J'ai noté votre recherche de studio à Douala. Quel est votre budget maximum par mois ?",
            "language": "fr",
            "dialogue_act": "ACKNOWLEDGE_AND_ASK",
            "question_count": 1,
            "confidence": 0.95,
        })

        response, errors = self._build_and_validate(
            response_plan, dialogue_plan, provider_context, raw,
        )

        self.assertEqual(len(errors), 0, f"Expected no errors, got: {errors}")
        self.assertIsNotNone(response)
        schema_valid, schema_error, _ = validate_response_json(raw)
        self.assertTrue(schema_valid, f"Schema invalid: {schema_error}")

    def test_appartement_tour(self) -> None:
        """Tour 2: User specifies budget 180k -> system asks district."""
        response_plan = ResponsePlan(
            language="fr",
            response_type="ACKNOWLEDGE_AND_ASK",
            next_question_key="district",
            next_question_text="Quel quartier préférez-vous à Douala ?",
            acknowledgement_facts={"budget_xaf": 180000},
            maximum_questions=1,
        )
        dialogue_plan = DialoguePlan(
            language="fr",
            dialogue_act="ACKNOWLEDGE_AND_ASK",
            maximum_questions=1,
        )
        provider_context = ProviderMemoryContext(
            language="fr",
            intent="rental_search",
            active_facts={
                "city": "Douala",
                "property_type": "apartment",
                "budget_xaf": 180000,
            },
            last_question_text="Quel est votre budget maximum par mois ?",
        )

        raw = json.dumps({
            "content": "J'ai noté votre budget de 180 000 FCFA. Dans quel quartier de Douala préférez-vous chercher ?",
            "language": "fr",
            "dialogue_act": "ACKNOWLEDGE_AND_ASK",
            "question_count": 1,
            "confidence": 0.95,
        })

        response, errors = self._build_and_validate(
            response_plan, dialogue_plan, provider_context, raw,
        )

        self.assertEqual(len(errors), 0, f"Expected no errors, got: {errors}")
        schema_valid, schema_error, _ = validate_response_json(raw)
        self.assertTrue(schema_valid, f"Schema invalid: {schema_error}")

    def test_correction_tour(self) -> None:
        """Tour 3: User says Bonamoussadi -> system confirms and asks if ready."""
        response_plan = ResponsePlan(
            language="fr",
            response_type="CONFIRM_CORRECTION_AND_ASK",
            next_question_key="ready_to_search",
            next_question_text="Souhaitez-vous que je lance la recherche maintenant ?",
            acknowledgement_facts={"district": "Bonamoussadi"},
            maximum_questions=1,
        )
        dialogue_plan = DialoguePlan(
            language="fr",
            dialogue_act="CONFIRM_CORRECTION_AND_ASK",
            maximum_questions=1,
        )
        provider_context = ProviderMemoryContext(
            language="fr",
            intent="rental_search",
            active_facts={
                "city": "Douala",
                "property_type": "apartment",
                "budget_xaf": 180000,
                "district": "Bonamoussadi",
            },
            last_question_text="Quel quartier préférez-vous à Douala ?",
        )

        raw = json.dumps({
            "content": "J'ai bien noté Bonamoussadi. Souhaitez-vous que je lance la recherche des appartements à Douala dans votre budget ?",
            "language": "fr",
            "dialogue_act": "CONFIRM_CORRECTION_AND_ASK",
            "question_count": 1,
            "confidence": 0.95,
        })

        response, errors = self._build_and_validate(
            response_plan, dialogue_plan, provider_context, raw,
        )

        self.assertEqual(len(errors), 0, f"Expected no errors, got: {errors}")
        schema_valid, schema_error, _ = validate_response_json(raw)
        self.assertTrue(schema_valid, f"Schema invalid: {schema_error}")


if __name__ == "__main__":
    unittest.main()
