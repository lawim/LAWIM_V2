from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from lawim_v2.ai.contracts import AIRequest, AIResponse
from lawim_v2.ai.internal_reasoning import InternalReasoningEngine, ReasoningContext
from lawim_v2.orchestration.errors import AllProvidersFailedError
from lawim_v2.orchestration.orchestrator import (
    ControlledGenerationRequest,
    ProviderOrchestrator,
)
from lawim_v2.orchestration.provider_registry import ProviderRegistry
from lawim_v2.orchestration.selection import ProviderSelectionPolicy


class _MockProvider:
    def __init__(self, name: str, fail: bool = False, latency: float = 0.01):
        self.name = name
        self.model = name + "-model"
        self._fail = fail
        self._latency = latency
        self._call_count = 0

    def generate(self, request: AIRequest) -> AIResponse:
        self._call_count += 1
        if self._fail:
            return AIResponse(
                provider=self.name,
                model=self.model,
                success=False,
                content="",
                latency_ms=10,
                input_tokens=0,
                output_tokens=0,
                estimated_cost=0.0,
                finish_reason="error",
                error_type="provider_error",
                error_code="ERR",
                retryable=True,
                fallback_required=True,
                request_id=request.request_id,
                provider_request_id=None,
                valid=False,
                complete=False,
                relevant=False,
                safe=True,
                well_formed=False,
                confidence_score=0.0,
            )
        return AIResponse(
            provider=self.name,
            model=self.model,
            success=True,
            content=f"Response from {self.name}",
            latency_ms=10,
            input_tokens=50,
            output_tokens=20,
            estimated_cost=0.001,
            finish_reason="stop",
            error_type=None,
            error_code=None,
            retryable=False,
            fallback_required=False,
            request_id=request.request_id,
            provider_request_id=f"req_{self._call_count}",
            valid=True,
            complete=True,
            relevant=True,
            safe=True,
            well_formed=True,
            confidence_score=0.95,
        )


class _MockInternalEngine:
    def __init__(self, content: str = "Internal fallback response"):
        self.content = content

    def reason(self, ctx: ReasoningContext):
        class _Resp:
            content = self.content
        return _Resp()


class TestProviderOrchestrator(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = ProviderRegistry()
        self.policy = ProviderSelectionPolicy(self.registry)
        self.internal = _MockInternalEngine()
        self.orchestrator = ProviderOrchestrator(
            registry=self.registry,
            selection_policy=self.policy,
            internal_engine=self.internal,
        )
        self.registry.set_chain(["provider_a", "provider_b", "internal"])

    def _make_request(self, text: str = "Bonjour", language: str = "fr") -> ControlledGenerationRequest:
        return ControlledGenerationRequest(
            text=text,
            conversation_key="conv-1",
            channel="test",
            language=language,
        )

    def test_first_provider_succeeds(self) -> None:
        self.registry.register("provider_a", _MockProvider("provider_a", fail=False))
        self.registry.register("provider_b", _MockProvider("provider_b", fail=False))

        result = self.orchestrator.generate(self._make_request())

        self.assertTrue(result.success)
        self.assertEqual(result.provider, "provider_a")
        self.assertIn("Response from provider_a", result.content)
        self.assertFalse(result.fallback_used)
        self.assertFalse(result.internal_fallback)

    def test_fallback_to_second_provider(self) -> None:
        self.registry.register("provider_a", _MockProvider("provider_a", fail=True))
        self.registry.register("provider_b", _MockProvider("provider_b", fail=False))

        result = self.orchestrator.generate(self._make_request())

        self.assertTrue(result.success)
        self.assertEqual(result.provider, "provider_b")
        self.assertIn("Response from provider_b", result.content)
        self.assertTrue(result.fallback_used)

    def test_all_providers_fail_internal_fallback(self) -> None:
        self.registry.register("provider_a", _MockProvider("provider_a", fail=True))
        self.registry.register("provider_b", _MockProvider("provider_b", fail=True))

        result = self.orchestrator.generate(self._make_request())

        self.assertTrue(result.success, "Internal fallback should succeed")
        self.assertEqual(result.provider, "internal")
        self.assertEqual(result.content, "Internal fallback response")
        self.assertTrue(result.fallback_used)
        self.assertTrue(result.internal_fallback)

    def test_no_internal_engine_raises(self) -> None:
        orchestrator = ProviderOrchestrator(
            registry=self.registry,
            selection_policy=self.policy,
            internal_engine=None,
        )
        self.registry.register("provider_a", _MockProvider("provider_a", fail=True))

        with self.assertRaises(AllProvidersFailedError):
            orchestrator.generate(self._make_request())

    def test_timeout_triggers_next_provider(self) -> None:
        self.registry.register("provider_a", _MockProvider("provider_a", fail=True))
        self.registry.register("provider_b", _MockProvider("provider_b", fail=False))

        result = self.orchestrator.generate(
            self._make_request(),
            timeout_seconds=5.0,
        )

        self.assertTrue(result.success)
        self.assertEqual(result.provider, "provider_b")

    def test_circuit_breaker_skips_failing_provider(self) -> None:
        fail_provider = _MockProvider("provider_a", fail=True)
        self.registry.register("provider_a", fail_provider)
        self.registry.register("provider_b", _MockProvider("provider_b", fail=False))

        for _ in range(5):
            self.registry.record_failure("provider_a", "provider_error")

        result = self.orchestrator.generate(self._make_request())

        self.assertTrue(result.success)
        self.assertEqual(result.provider, "provider_b")

    def test_no_double_delivery(self) -> None:
        provider_a = _MockProvider("provider_a", fail=False)
        self.registry.register("provider_a", provider_a)

        result = self.orchestrator.generate(self._make_request())

        self.assertTrue(result.success)
        self.assertEqual(provider_a._call_count, 1)

    def test_all_attempts_recorded(self) -> None:
        self.registry.register("provider_a", _MockProvider("provider_a", fail=True))
        self.registry.register("provider_b", _MockProvider("provider_b", fail=False))

        result = self.orchestrator.generate(self._make_request())

        self.assertEqual(len(result.all_attempts), 2)
        self.assertFalse(result.all_attempts[0].success)
        self.assertTrue(result.all_attempts[1].success)

    def test_successful_result_metadata(self) -> None:
        self.registry.register("provider_a", _MockProvider("provider_a", fail=False))

        result = self.orchestrator.generate(self._make_request())

        self.assertEqual(result.model, "provider_a-model")
        self.assertGreaterEqual(result.latency_ms, 0)
        self.assertIsNone(result.error)

    def test_no_available_providers_uses_internal_fallback(self) -> None:
        self.registry.register("provider_a", _MockProvider("provider_a", fail=True))

        result = self.orchestrator.generate(self._make_request())

        self.assertTrue(result.success)
        self.assertEqual(result.provider, "internal")


if __name__ == "__main__":
    unittest.main()
