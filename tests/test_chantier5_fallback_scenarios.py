"""Chantier 5: Provider fallback and circuit breaker tests.

Verifies the fallback chain behavior:
  - First provider fails -> second succeeds
  - All providers fail -> internal fallback
  - Circuit breaker opens after threshold failures
  - Timeout handling
  - Recovery after circuit opens
"""

from __future__ import annotations

import time
import unittest
from unittest.mock import MagicMock

from lawim_v2.ai.contracts import AIRequest, AIResponse
from lawim_v2.ai.internal_reasoning import InternalReasoningEngine, ReasoningContext
from lawim_v2.orchestration.errors import AllProvidersFailedError
from lawim_v2.orchestration.orchestrator import (
    ControlledGenerationRequest,
    ProviderOrchestrator,
    GenerationResult,
)
from lawim_v2.orchestration.provider_registry import ProviderRegistry, ProviderStatus
from lawim_v2.orchestration.selection import ProviderSelectionPolicy


class _MockProvider:
    """Simulates an AI provider that can be configured to succeed or fail."""

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
        self.content_text = content

    def reason(self, ctx: ReasoningContext):
        class _Resp:
            content = ""
        _Resp.content = self.content_text
        return _Resp()


class _MockTimeoutProvider:
    """Provider that simulates a timeout."""

    def __init__(self, name: str):
        self.name = name
        self.model = name + "-model"

    def generate(self, request: AIRequest) -> AIResponse:
        from lawim_v2.orchestration.errors import ProviderTimeoutError
        raise ProviderTimeoutError("Simulated timeout")


class TestChantier5FallbackScenarios(unittest.TestCase):
    """Provider orchestration fallback and circuit breaker behavior."""

    def setUp(self):
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
            conversation_key="conv-fallback",
            channel="test",
            language=language,
        )

    # ── Happy path ────────────────────────────────────────────────────────

    def test_first_provider_succeeds(self):
        self.registry.register("provider_a", _MockProvider("provider_a", fail=False))
        self.registry.register("provider_b", _MockProvider("provider_b", fail=False))
        result = self.orchestrator.generate(self._make_request())
        self.assertTrue(result.success)
        self.assertEqual(result.provider, "provider_a")
        self.assertIn("Response from provider_a", result.content)
        self.assertFalse(result.fallback_used)
        self.assertFalse(result.internal_fallback)

    # ── Fallback: first fails, second succeeds ────────────────────────────

    def test_fallback_to_second_provider(self):
        self.registry.register("provider_a", _MockProvider("provider_a", fail=True))
        self.registry.register("provider_b", _MockProvider("provider_b", fail=False))
        result = self.orchestrator.generate(self._make_request())
        self.assertTrue(result.success)
        self.assertEqual(result.provider, "provider_b")
        self.assertIn("Response from provider_b", result.content)
        self.assertTrue(result.fallback_used)
        self.assertFalse(result.internal_fallback)

    # ── All providers fail -> internal fallback ───────────────────────────

    def test_all_providers_fail_internal_fallback(self):
        self.registry.register("provider_a", _MockProvider("provider_a", fail=True))
        self.registry.register("provider_b", _MockProvider("provider_b", fail=True))
        result = self.orchestrator.generate(self._make_request())
        self.assertTrue(result.success, "Internal fallback should succeed")
        self.assertEqual(result.provider, "internal")
        self.assertEqual(result.content, "Internal fallback response")
        self.assertTrue(result.fallback_used)
        self.assertTrue(result.internal_fallback)

    def test_no_internal_engine_raises(self):
        orchestrator_no_internal = ProviderOrchestrator(
            registry=self.registry,
            selection_policy=self.policy,
            internal_engine=None,
        )
        self.registry.register("provider_a", _MockProvider("provider_a", fail=True))
        with self.assertRaises(AllProvidersFailedError):
            orchestrator_no_internal.generate(self._make_request())

    # ── Circuit breaker ───────────────────────────────────────────────────

    def test_circuit_breaker_opens_after_three_failures(self):
        self.registry.register("provider_a", _MockProvider("provider_a", fail=True))
        self.registry.register("provider_b", _MockProvider("provider_b", fail=True))
        for i in range(4):
            try:
                if i == 3:
                    self.registry.set_chain(["provider_a", "provider_b", "internal"])
                self.orchestrator.generate(self._make_request())
            except AllProvidersFailedError:
                pass
        health = self.registry.get_health("provider_a")
        self.assertIsNotNone(health)
        if health is not None:
            self.assertGreaterEqual(health.consecutive_failures, 3)

    def test_circuit_open_provider_skipped(self):
        self.registry.register("provider_a", _MockProvider("provider_a", fail=True))
        self.registry.register("provider_b", _MockProvider("provider_b", fail=False))
        self.registry.record_failure("provider_a", "error")
        self.registry.record_failure("provider_a", "error")
        self.registry.record_failure("provider_a", "error")
        self.assertFalse(self.registry.is_available("provider_a"))
        result = self.orchestrator.generate(self._make_request())
        self.assertTrue(result.success)
        self.assertEqual(result.provider, "provider_b")

    def test_circuit_recovery_after_timeout(self):
        self.registry.register("provider_a", _MockProvider("provider_a", fail=True))
        self.registry.register("provider_b", _MockProvider("provider_b", fail=False))
        for _ in range(3):
            self.registry.record_failure("provider_a", "error")
        self.assertFalse(self.registry.is_available("provider_a"))
        self.registry.record_success("provider_a")
        self.assertTrue(self.registry.is_available("provider_a"))

    # ── Timeout handling ──────────────────────────────────────────────────

    def test_timeout_triggers_fallback(self):
        self.registry.register("provider_a", _MockTimeoutProvider("provider_a"))
        self.registry.register("provider_b", _MockProvider("provider_b", fail=False))
        result = self.orchestrator.generate(self._make_request())
        self.assertTrue(result.success)
        self.assertEqual(result.provider, "provider_b")
        self.assertTrue(result.fallback_used)

    def test_timeout_recorded_as_failure(self):
        self.registry.register("provider_a", _MockTimeoutProvider("provider_a"))
        self.registry.register("provider_b", _MockTimeoutProvider("provider_b"))
        self.registry.register("provider_c", _MockProvider("provider_c", fail=False))
        self.registry.set_chain(["provider_a", "provider_b", "provider_c"])
        result = self.orchestrator.generate(self._make_request())
        self.assertTrue(result.success)
        health_a = self.registry.get_health("provider_a")
        if health_a is not None:
            self.assertGreater(health_a.consecutive_failures, 0)

    # ── All providers timeout -> internal fallback ────────────────────────

    def test_all_timeout_internal_fallback(self):
        self.registry.register("provider_a", _MockTimeoutProvider("provider_a"))
        self.registry.register("provider_b", _MockTimeoutProvider("provider_b"))
        result = self.orchestrator.generate(self._make_request())
        self.assertTrue(result.success)
        self.assertEqual(result.provider, "internal")
        self.assertTrue(result.internal_fallback)

    # ── Result metadata ───────────────────────────────────────────────────

    def test_generation_result_contains_all_attempts(self):
        self.registry.register("provider_a", _MockProvider("provider_a", fail=True))
        self.registry.register("provider_b", _MockProvider("provider_b", fail=False))
        result = self.orchestrator.generate(self._make_request())
        self.assertGreater(len(result.all_attempts), 0)
        self.assertTrue(any(
            a.provider == "provider_a" and not a.success
            for a in result.all_attempts
        ))
        self.assertTrue(any(
            a.provider == "provider_b" and a.success
            for a in result.all_attempts
        ))

    def test_attempts_detail_recorded(self):
        self.registry.register("provider_a", _MockProvider("provider_a", fail=True))
        self.registry.register("provider_b", _MockProvider("provider_b", fail=False))
        result = self.orchestrator.generate(self._make_request())
        self.assertGreater(len(result.all_attempts), 1)
        self.assertIsNotNone(result.all_attempts[0].latency_ms)
        self.assertIsNotNone(result.all_attempts[0].provider)

    # ── Chain and availability ────────────────────────────────────────────

    def test_chain_skips_unavailable_providers(self):
        self.registry.register("provider_a", _MockProvider("provider_a", fail=False))
        self.registry.register("provider_b", _MockProvider("provider_b", fail=False))
        self.registry.set_chain(["provider_a", "provider_b"])
        self.registry.record_failure("provider_a", "error")
        self.registry.record_failure("provider_a", "error")
        self.registry.record_failure("provider_a", "error")
        result = self.orchestrator.generate(self._make_request())
        self.assertEqual(result.provider, "provider_b")

    def test_health_metrics_tracked(self):
        self.registry.register("provider_a", _MockProvider("provider_a", fail=True))
        self.registry.register("provider_b", _MockProvider("provider_b", fail=False))
        try:
            self.orchestrator.generate(self._make_request())
        except AllProvidersFailedError:
            pass
        health_a = self.registry.get_health("provider_a")
        if health_a is not None:
            self.assertGreaterEqual(health_a.consecutive_failures, 1)
            # is_available stays True until circuit opens (3 failures)
        health_b = self.registry.get_health("provider_b")
        if health_b is not None:
            self.assertTrue(health_b.is_available)

    def test_initial_registry_state(self):
        self.registry.register("provider_a", _MockProvider("provider_a"))
        self.assertTrue(self.registry.is_available("provider_a"))
        self.assertIn("provider_a", self.registry.get_available_providers())

    def test_unregistered_provider_not_available(self):
        self.assertFalse(self.registry.is_available("nonexistent"))


if __name__ == "__main__":
    unittest.main()
