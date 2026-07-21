from __future__ import annotations

import json
import time
import unittest

from lawim_v2.ai.contracts import AIRequest, AIResponse
from lawim_v2.ai.internal_reasoning import InternalReasoningEngine, ReasoningContext
from lawim_v2.orchestration.errors import AllProvidersFailedError
from lawim_v2.orchestration.orchestrator import (
    ControlledGenerationRequest,
    ProviderOrchestrator,
)
from lawim_v2.orchestration.provider_registry import ProviderRegistry
from lawim_v2.orchestration.selection import ProviderSelectionPolicy


class _MockInternalEngine:
    def __init__(self, content: str = "Internal fallback response"):
        self.content = content

    def reason(self, ctx: ReasoningContext):
        class _Resp:
            content = self.content
        return _Resp()


class _ErrorProvider:
    def __init__(self, name: str, error_type: str = "provider_error"):
        self.name = name
        self.model = name + "-model"
        self._error_type = error_type

    def generate(self, request: AIRequest) -> AIResponse:
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
            error_type=self._error_type,
            error_code=self._error_type.upper(),
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


class _EmptyResponseProvider:
    def __init__(self, name: str):
        self.name = name
        self.model = name + "-model"

    def generate(self, request: AIRequest) -> AIResponse:
        return AIResponse(
            provider=self.name,
            model=self.model,
            success=True,
            content="",
            latency_ms=10,
            input_tokens=0,
            output_tokens=0,
            estimated_cost=0.0,
            finish_reason="stop",
            error_type=None,
            error_code=None,
            retryable=False,
            fallback_required=False,
            request_id=request.request_id,
            provider_request_id=None,
            valid=False,
            complete=False,
            relevant=False,
            safe=True,
            well_formed=False,
            confidence_score=0.0,
        )


class TestProviderFailureScenarios(unittest.TestCase):
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

    def _make_request(self, text: str = "Bonjour") -> ControlledGenerationRequest:
        return ControlledGenerationRequest(
            text=text,
            conversation_key="conv-1",
            channel="test",
            language="fr",
        )

    def test_all_providers_unavailable(self) -> None:
        self.registry.register("provider_a", _ErrorProvider("provider_a"))
        self.registry.register("provider_b", _ErrorProvider("provider_b"))

        result = self.orchestrator.generate(self._make_request())

        self.assertTrue(result.success, "Internal fallback should save the request")
        self.assertEqual(result.provider, "internal")
        self.assertIn("Internal fallback", result.content)

    def test_429_rate_limit(self) -> None:
        self.registry.register("provider_a", _ErrorProvider("provider_a", error_type="429_rate_limit"))
        self.registry.register("provider_b", _ErrorProvider("provider_b", error_type="rate_limit"))

        result = self.orchestrator.generate(self._make_request())

        self.assertTrue(result.success)
        self.assertEqual(result.provider, "internal")

    def test_500_server_error(self) -> None:
        self.registry.register("provider_a", _ErrorProvider("provider_a", error_type="500_server_error"))
        self.registry.register("provider_b", _ErrorProvider("provider_b", error_type="server_error"))

        result = self.orchestrator.generate(self._make_request())

        self.assertTrue(result.success)
        self.assertEqual(result.provider, "internal")

    def test_empty_response(self) -> None:
        self.registry.register("provider_a", _EmptyResponseProvider("provider_a"))

        result = self.orchestrator.generate(self._make_request())

        self.assertTrue(result.success)
        self.assertEqual(result.provider, "internal")

    def test_all_fail_no_internal_fallback(self) -> None:
        orchestrator = ProviderOrchestrator(
            registry=self.registry,
            selection_policy=self.policy,
            internal_engine=None,
        )
        self.registry.register("provider_a", _ErrorProvider("provider_a"))

        with self.assertRaises(AllProvidersFailedError) as ctx:
            orchestrator.generate(self._make_request())
        self.assertIn("All providers failed", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
