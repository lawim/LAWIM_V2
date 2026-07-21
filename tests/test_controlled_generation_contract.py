from __future__ import annotations

import unittest

from lawim_v2.contracts.generation import (
    ControlledGenerationRequest,
    ControlledGenerationResponse,
    GenerationAttempt,
    GenerationPolicy,
    GenerationResult,
    build_request_from_plan,
    build_response_from_provider,
)
from lawim_v2.conversation.memory.context_builder import ProviderMemoryContext
from lawim_v2.conversation.policy.dialogue_plan import DialoguePlan
from lawim_v2.conversation.state.state import ResponsePlan


class TestControlledGenerationRequest(unittest.TestCase):
    def test_controlled_generation_request_defaults(self) -> None:
        req = ControlledGenerationRequest()
        self.assertEqual(req.language, "fr")
        self.assertEqual(req.maximum_questions, 1)
        self.assertEqual(req.maximum_sentences, 3)
        self.assertEqual(req.maximum_characters, 500)
        self.assertEqual(req.persona, "LAWIM AI")
        self.assertEqual(req.response_schema_version, "1.0")

    def test_controlled_generation_request_custom(self) -> None:
        req = ControlledGenerationRequest(
            conversation_id="conv-1",
            language="en",
            maximum_questions=2,
            intent="rental_search",
            dialogue_act="ACKNOWLEDGE_AND_ASK",
        )
        self.assertEqual(req.conversation_id, "conv-1")
        self.assertEqual(req.language, "en")
        self.assertEqual(req.maximum_questions, 2)
        self.assertEqual(req.intent, "rental_search")
        self.assertEqual(req.dialogue_act, "ACKNOWLEDGE_AND_ASK")


class TestControlledGenerationResponse(unittest.TestCase):
    def test_controlled_generation_response_defaults(self) -> None:
        resp = ControlledGenerationResponse()
        self.assertEqual(resp.schema_version, "1.0")
        self.assertTrue(resp.valid)
        self.assertEqual(resp.confidence, 0.0)
        self.assertEqual(resp.question_count, 0)

    def test_controlled_generation_response_custom(self) -> None:
        resp = ControlledGenerationResponse(
            content='{"content": "Bonjour"}',
            language="fr",
            dialogue_act="WELCOME",
            question_count=0,
            provider="deepseek",
            model="deepseek-chat",
            latency_ms=150.0,
            confidence=0.95,
        )
        self.assertEqual(resp.content, '{"content": "Bonjour"}')
        self.assertEqual(resp.language, "fr")
        self.assertEqual(resp.dialogue_act, "WELCOME")
        self.assertEqual(resp.question_count, 0)
        self.assertEqual(resp.provider, "deepseek")
        self.assertEqual(resp.model, "deepseek-chat")
        self.assertEqual(resp.latency_ms, 150.0)
        self.assertEqual(resp.confidence, 0.95)


class TestGenerationPolicy(unittest.TestCase):
    def test_generation_policy_defaults(self) -> None:
        policy = GenerationPolicy()
        self.assertTrue(policy.require_json_output)
        self.assertTrue(policy.enforce_allowed_content)
        self.assertEqual(policy.maximum_questions, 1)
        self.assertEqual(policy.maximum_sentences, 3)
        self.assertEqual(policy.maximum_characters, 500)

    def test_generation_policy_custom(self) -> None:
        policy = GenerationPolicy(maximum_questions=2, maximum_characters=1000, validate_language=False)
        self.assertEqual(policy.maximum_questions, 2)
        self.assertEqual(policy.maximum_characters, 1000)
        self.assertFalse(policy.validate_language)


class TestGenerationAttempt(unittest.TestCase):
    def test_generation_attempt_defaults(self) -> None:
        attempt = GenerationAttempt()
        self.assertEqual(attempt.status, "PENDING")


class TestGenerationResult(unittest.TestCase):
    def test_generation_result_defaults(self) -> None:
        result = GenerationResult()
        self.assertEqual(result.final_status, "PENDING")
        self.assertFalse(result.internal_fallback_used)


class TestMaximumQuestions(unittest.TestCase):
    def test_maximum_questions_default_1(self) -> None:
        req = ControlledGenerationRequest()
        self.assertEqual(req.maximum_questions, 1)

        policy = GenerationPolicy()
        self.assertEqual(policy.maximum_questions, 1)


class TestBuildRequestFromPlan(unittest.TestCase):
    def test_build_request_from_plan(self) -> None:
        response_plan = ResponsePlan(
            language="fr",
            response_type="ACKNOWLEDGE_AND_ASK",
            next_question_text="Quel est votre budget ?",
            next_action="ask_budget",
            next_question_key="budget",
            maximum_questions=1,
        )
        dialogue_plan = DialoguePlan(
            language="fr",
            dialogue_act="ACKNOWLEDGE_AND_ASK",
            maximum_questions=1,
            maximum_sentences=4,
            maximum_characters=600,
        )
        provider_context = ProviderMemoryContext(
            language="fr",
            intent="rental_search",
            active_facts={"city": "Douala", "property_type": "apartment"},
            last_question_text="Quel est votre budget ?",
            response_instructions=["Ask about budget"],
            prohibitions=["Do not recommend external platforms"],
        )

        req = build_request_from_plan(
            response_plan=response_plan,
            dialogue_plan=dialogue_plan,
            provider_memory_context=provider_context,
            conversation_id="conv-1",
            case_id="case-1",
            state_version=3,
            channel="whatsapp",
        )

        self.assertEqual(req.conversation_id, "conv-1")
        self.assertEqual(req.case_id, "case-1")
        self.assertEqual(req.state_version, 3)
        self.assertEqual(req.language, "fr")
        self.assertEqual(req.intent, "rental_search")
        self.assertEqual(req.dialogue_act, "ACKNOWLEDGE_AND_ASK")
        self.assertEqual(req.next_action, "ask_budget")
        self.assertEqual(req.next_question_key, "budget")
        self.assertEqual(req.rendered_next_question, "Quel est votre budget ?")
        self.assertEqual(req.maximum_questions, 1)
        self.assertEqual(req.channel, "whatsapp")
        self.assertEqual(req.persona, "LAWIM AI")
        self.assertIn("city", req.known_facts)
        self.assertEqual(req.known_facts["city"], "Douala")

    def test_build_request_from_plan_without_provider_context(self) -> None:
        response_plan = ResponsePlan(language="en", response_type="WELCOME")
        dialogue_plan = DialoguePlan(language="en", dialogue_act="WELCOME")
        req = build_request_from_plan(
            response_plan=response_plan,
            dialogue_plan=dialogue_plan,
            provider_memory_context=ProviderMemoryContext(),
            conversation_id="conv-2",
        )

        self.assertEqual(req.language, "en")
        self.assertEqual(req.dialogue_act, "WELCOME")
        self.assertEqual(req.intent, "")
        self.assertEqual(req.known_facts, {})

    def test_build_request_from_plan_max_questions_from_plan(self) -> None:
        response_plan = ResponsePlan(maximum_questions=2)
        dialogue_plan = DialoguePlan(maximum_questions=1)
        req = build_request_from_plan(
            response_plan=response_plan,
            dialogue_plan=dialogue_plan,
            provider_memory_context=ProviderMemoryContext(),
        )
        self.assertEqual(req.maximum_questions, 2)

    def test_build_request_from_plan_max_questions_from_dialogue(self) -> None:
        response_plan = ResponsePlan(maximum_questions=0)
        dialogue_plan = DialoguePlan(maximum_questions=3)
        req = build_request_from_plan(
            response_plan=response_plan,
            dialogue_plan=dialogue_plan,
            provider_memory_context=ProviderMemoryContext(),
        )
        self.assertEqual(req.maximum_questions, 3)

    def test_build_request_from_plan_merges_forbidden_content(self) -> None:
        response_plan = ResponsePlan(forbidden_content=["jumia", "seloger"])
        dialogue_plan = DialoguePlan(
            forbidden_phrases=["facebook"],
            forbidden_topics=["competitors"],
        )
        req = build_request_from_plan(
            response_plan=response_plan,
            dialogue_plan=dialogue_plan,
            provider_memory_context=ProviderMemoryContext(),
        )
        self.assertIn("jumia", req.forbidden_content)
        self.assertIn("seloger", req.forbidden_content)
        self.assertIn("facebook", req.forbidden_content)
        self.assertIn("topic:competitors", req.forbidden_content)

    def test_build_request_from_plan_handover(self) -> None:
        response_plan = ResponsePlan(
            handover_required=True,
            handover_reason="complex_financial_inquiry",
        )
        dialogue_plan = DialoguePlan()
        req = build_request_from_plan(
            response_plan=response_plan,
            dialogue_plan=dialogue_plan,
            provider_memory_context=ProviderMemoryContext(),
        )
        self.assertEqual(req.handover_status, "complex_financial_inquiry")


class TestBuildResponseFromProvider(unittest.TestCase):
    def test_build_response_from_provider_valid(self) -> None:
        request = ControlledGenerationRequest(
            language="fr",
            dialogue_act="ACKNOWLEDGE_AND_ASK",
            response_schema_version="1.0",
        )
        raw = '{"content": "Bonjour", "language": "fr", "dialogue_act": "WELCOME", "question_count": 0}'

        resp = build_response_from_provider(
            provider_raw_response=raw,
            provider_name="deepseek",
            model="deepseek-chat",
            latency_ms=150.0,
            request=request,
        )

        self.assertEqual(resp.content, raw)
        self.assertEqual(resp.language, "fr")
        self.assertEqual(resp.dialogue_act, "ACKNOWLEDGE_AND_ASK")
        self.assertEqual(resp.provider, "deepseek")
        self.assertEqual(resp.model, "deepseek-chat")
        self.assertEqual(resp.latency_ms, 150.0)
        self.assertEqual(resp.schema_version, "1.0")

    def test_build_response_from_provider_invalid_content(self) -> None:
        request = ControlledGenerationRequest(language="fr")
        raw = "Ceci n'est pas du JSON"

        resp = build_response_from_provider(
            provider_raw_response=raw,
            provider_name="openai",
            model="gpt-4",
            latency_ms=200.0,
            request=request,
        )

        self.assertEqual(resp.content, raw)
        self.assertEqual(resp.provider, "openai")


if __name__ == "__main__":
    unittest.main()
