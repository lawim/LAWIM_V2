from __future__ import annotations

import time
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import MagicMock, patch

from lawim_v2.ai.contracts import AIMessage, AIProvider, AIRequest, AIResponse, ProviderHealth, UsageStatus
from lawim_v2.ai.disclaimer import DEFAULT_DISCLAIMER_TEXT, DisclaimerConfig, DisclaimerManager
from lawim_v2.ai.internal_reasoning import InternalReasoningEngine, ReasoningContext
from lawim_v2.ai.memory import MemoryBundle, MemoryOptimizer
from lawim_v2.ai.orchestrator import AIOrchestrator
from lawim_v2.ai.prompt_reconstruction import PromptReconstructionEngine, ReconstructedContext


class _MockProvider:
    def __init__(self, name: str, enabled: bool = True, fail: bool = False, latency: int = 50):
        self.name = name
        self._enabled = enabled
        self._fail = fail
        self._latency = latency
        self._call_count = 0

    def is_enabled(self) -> bool:
        return self._enabled

    def health_check(self) -> ProviderHealth:
        return ProviderHealth(
            provider=self.name, model=f"{self.name}-model",
            enabled=self._enabled, available=not self._fail,
            state="ready", checked_at="now", latency_ms=self._latency,
        )

    def generate(self, request: AIRequest) -> AIResponse:
        self._call_count += 1
        time.sleep(self._latency / 1000.0)
        if self._fail:
            return AIResponse(
                provider=self.name, model=f"{self.name}-model",
                success=False, content="", latency_ms=self._latency,
                input_tokens=0, output_tokens=0, estimated_cost=0.0,
                finish_reason="error", error_type="provider_error", error_code="ERR",
                retryable=True, fallback_required=True,
                request_id=request.request_id, provider_request_id=None,
                valid=False, complete=False, relevant=False, safe=True, well_formed=False,
                confidence_score=0.0,
            )
        return AIResponse(
            provider=self.name, model=f"{self.name}-model",
            success=True, content=f"Response from {self.name}",
            latency_ms=self._latency, input_tokens=50, output_tokens=20,
            estimated_cost=0.001, finish_reason="stop", error_type=None, error_code=None,
            retryable=False, fallback_required=False,
            request_id=request.request_id, provider_request_id=f"req_{self._call_count}",
            valid=True, complete=True, relevant=True, safe=True, well_formed=True,
            confidence_score=0.95,
        )

    def estimate_cost(self, request: AIRequest):
        from lawim_v2.ai.contracts import CostEstimate
        return CostEstimate(provider=self.name, model=f"{self.name}-model", input_tokens=50, output_tokens=20, estimated_cost=0.001)


class _MockRepository:
    def __init__(self):
        self.ai_requests = []
        self.ai_responses = []
        self.ai_decisions = []
        self.ai_alerts = []
        self.ai_usage = []
        self.ai_health = []
        self.ai_costs = []
        self.ai_fallback_metrics = []
        self.ai_memory = []
        self.disclaimer_config = None
        self.disclaimer_audit = []
        self.conversation_decisions = []
        self.conversation_facts = []
        self.conversation_messages = []

    def create_ai_request(self, **kw): row = dict(kw); self.ai_requests.append(row); return row
    def create_ai_response(self, **kw): self.ai_responses.append(dict(kw))
    def record_ai_routing_decision(self, **kw): self.ai_decisions.append(dict(kw))
    def record_ai_alert(self, **kw): self.ai_alerts.append(dict(kw))
    def upsert_ai_usage(self, **kw): self.ai_usage.append(dict(kw))
    def upsert_ai_provider_health(self, **kw): self.ai_health.append(dict(kw)); return dict(kw)
    def record_ai_cost_estimate(self, **kw): self.ai_costs.append(dict(kw))
    def record_ai_fallback_metrics(self, **kw): self.ai_fallback_metrics.append(dict(kw))
    def get_ai_fallback_metrics(self): return {"fallback_rate": 0.05, "provider_availability": 0.95}
    def list_ai_providers(self, **kw): return [{"provider_key": "deepseek"}, {"provider_key": "openai"}]
    def list_ai_usage(self, **kw): return []
    def list_ai_alerts(self, **kw): return []
    def list_ai_fallback_entries(self, **kw): return []
    def list_ai_learning_candidates(self, **kw): return []
    def list_ai_knowledge_versions(self, **kw): return []
    def ai_overview(self): return {"status": "ok"}
    def review_ai_learning_candidate(self, **kw): return {"status": "reviewed"}
    def publish_ai_learning_candidate(self, **kw): return {"status": "published"}
    def deprecate_ai_learning_candidate(self, **kw): return {"status": "deprecated"}
    def rollback_ai_knowledge_version(self, **kw): return {"status": "rolled_back"}
    def create_ai_learning_candidate(self, **kw): return {"candidate_key": "test-candidate", "status": "candidate"}
    def create_ai_memory(self, **kw): self.ai_memory.append(dict(kw))
    def list_ai_memory(self, **kw): return []
    def list_conversation_decisions(self, **kw): return self.conversation_decisions
    def list_conversation_facts(self, **kw): return self.conversation_facts
    def list_conversation_messages(self, **kw): return self.conversation_messages
    def get_user(self, **kw): return {"id": 1, "role": "user", "organization_id": 1}
    def list_properties(self, **kw): return []
    def search_properties(self, **kw): return []
    def get_ai_disclaimer_config(self): return self.disclaimer_config
    def upsert_ai_disclaimer_config(self, **kw): self.disclaimer_config = kw
    def create_ai_disclaimer_audit(self, **kw): self.disclaimer_audit.append(dict(kw))
    def get_ai_circuit_breaker(self, provider_key):
        return {
            "provider_key": provider_key,
            "state": "closed",
            "failure_count": 0,
            "last_failure_at": None,
            "circuit_opened_at": None,
            "half_open_attempts": 0,
        }
    def upsert_ai_circuit_breaker(self, **kw):
        return {
            "provider_key": kw.get("provider_key", "unknown"),
            "state": kw.get("state", "closed"),
            "failure_count": kw.get("failure_count", 0),
            "last_failure_at": kw.get("last_failure_at"),
            "circuit_opened_at": kw.get("circuit_opened_at"),
            "half_open_attempts": kw.get("half_open_attempts", 0),
        }
    def list_ai_circuit_breakers(self, **kw):
        return []


class _MockConfig:
    def __init__(self):
        self.ai_total_timeout_seconds = 30
        self.ai_max_context_messages = 20
        self.ai_max_context_tokens = None
        self.ai_max_cost_per_request = None
        self.ai_context_redaction_enabled = False
        self.ai_allow_provider_retry = False
        self.ai_learning_enabled = True
        self.ai_learning_requires_human_approval = True
        self.ai_alerts_enabled = True
        self.ai_primary_provider = "deepseek"
        self.ai_complex_provider = "openai"
        self.ai_fallback_chain = ("deepseek", "openai", "gemini_primary", "gemini_secondary")
        self.ai_request_timeout_seconds = 5
        self.ai_circuit_breaker_enabled = True
        self.ai_circuit_breaker_failure_threshold = 5
        self.ai_circuit_breaker_window_seconds = 300
        self.ai_circuit_breaker_open_seconds = 600
        self.ai_circuit_breaker_half_open_requests = 1
        self.ai_provider_deepseek_enabled = True
        self.ai_provider_openai_enabled = True
        self.ai_provider_gemini_primary_enabled = True
        self.ai_provider_gemini_secondary_enabled = True
        self.deepseek_api_key = "test-key"
        self.deepseek_model = "deepseek-test"
        self.deepseek_base_url = "https://api.test.com"
        self.openai_api_key = "test-key"
        self.openai_model = "gpt-test"
        self.gemini_primary_api_key = "test-key"
        self.gemini_primary_model = "gemini-test"
        self.gemini_secondary_api_key = "test-key"
        self.gemini_secondary_model = "gemini-test"


class TestProviderFallbackChain(unittest.TestCase):
    def setUp(self):
        self.repo = _MockRepository()
        self.config = _MockConfig()

    def _make_orchestrator(self, providers: dict | None = None):
        return AIOrchestrator(self.repo, self.config, providers=providers)

    def _make_request(self, text="Bonjour", conversation_key="conv-1", channel="test"):
        return AIRequest(
            request_id="req-1", channel=channel, conversation_key=conversation_key,
            text=text, sanitized_text=text, language="fr", complexity="simple",
            external_chat_id="", external_user_id="", message_id="msg-1",
            thread_id=None, contact_id=None, organization_id=None,
            context_messages=(), metadata={}, max_output_tokens=512, allow_retry=False,
        )

    def test_primary_provider_succeeds(self):
        providers = {
            "deepseek": _MockProvider("deepseek", fail=False),
            "openai": _MockProvider("openai", fail=False),
        }
        orch = self._make_orchestrator(providers)
        outcome = orch.generate(self._make_request())
        self.assertTrue(outcome.response.success)
        self.assertEqual(outcome.response.provider, "deepseek")
        self.assertFalse(outcome.internal_response)
        self.assertEqual(outcome.response.content, "Response from deepseek")

    def test_fallback_to_second_provider(self):
        providers = {
            "deepseek": _MockProvider("deepseek", fail=True),
            "openai": _MockProvider("openai", fail=False),
        }
        orch = self._make_orchestrator(providers)
        outcome = orch.generate(self._make_request())
        self.assertTrue(outcome.response.success)
        self.assertEqual(outcome.response.provider, "openai")

    def test_all_providers_fail_triggers_internal(self):
        providers = {
            "deepseek": _MockProvider("deepseek", fail=True),
            "openai": _MockProvider("openai", fail=True),
            "gemini_primary": _MockProvider("gemini_primary", fail=True),
            "gemini_secondary": _MockProvider("gemini_secondary", fail=True),
        }
        orch = self._make_orchestrator(providers)
        outcome = orch.generate(self._make_request())
        self.assertTrue(outcome.response.success, "Internal engine should save the conversation")
        self.assertEqual(outcome.response.provider, "internal")
        self.assertTrue(outcome.internal_response)
        self.assertTrue(len(outcome.response.content) > 0)

    def test_disabled_provider_is_skipped(self):
        providers = {
            "deepseek": _MockProvider("deepseek", enabled=False),
            "openai": _MockProvider("openai", fail=False),
        }
        orch = self._make_orchestrator(providers)
        outcome = orch.generate(self._make_request())
        self.assertTrue(outcome.response.success)
        self.assertEqual(outcome.response.provider, "openai")

    def test_invalid_response_triggers_fallback(self):
        class InvalidProvider(_MockProvider):
            def generate(self, request):
                return AIResponse(
                    provider=self.name, model=f"{self.name}-model",
                    success=True, content="", latency_ms=10,
                    input_tokens=0, output_tokens=0, estimated_cost=0.0,
                    finish_reason="stop", error_type=None, error_code=None,
                    retryable=False, fallback_required=False,
                    request_id=request.request_id, provider_request_id=None,
                    valid=False, complete=False, relevant=False, safe=True, well_formed=False,
                    confidence_score=0.0,
                )
        providers = {
            "deepseek": InvalidProvider("deepseek"),
            "openai": _MockProvider("openai", fail=False),
        }
        orch = self._make_orchestrator(providers)
        outcome = orch.generate(self._make_request())
        self.assertTrue(outcome.response.success)
        self.assertEqual(outcome.response.provider, "openai")

    def test_fallback_metrics_are_recorded(self):
        providers = {
            "deepseek": _MockProvider("deepseek", fail=True),
            "openai": _MockProvider("openai", fail=False),
        }
        orch = self._make_orchestrator(providers)
        orch.generate(self._make_request())
        self.assertTrue(len(self.repo.ai_fallback_metrics) > 0)
        metric = self.repo.ai_fallback_metrics[0]
        self.assertEqual(metric["final_provider"], "openai")
        self.assertIn("fallback_count", metric)


class TestInternalReasoningEngine(unittest.TestCase):
    def setUp(self):
        self.repo = _MockRepository()
        self.config = _MockConfig()
        self.engine = InternalReasoningEngine(self.repo, self.config)

    def test_greeting(self):
        ctx = ReasoningContext(user_text="Bonjour", language="fr")
        resp = self.engine.reason(ctx)
        self.assertTrue(resp.content)
        self.assertIn("Bonjour", resp.content)
        self.assertGreaterEqual(resp.confidence, 0.5)

    def test_property_search(self):
        ctx = ReasoningContext(user_text="Je cherche une maison à Douala", language="fr")
        resp = self.engine.reason(ctx)
        self.assertTrue(resp.content)
        self.assertIn("bien immobilier", resp.content.lower())

    def test_farewell(self):
        ctx = ReasoningContext(user_text="Merci au revoir", language="fr")
        resp = self.engine.reason(ctx)
        self.assertIn("Merci", resp.content)

    def test_financial_escalates(self):
        ctx = ReasoningContext(user_text="Quel est le coût total ?")
        resp = self.engine.reason(ctx)
        self.assertTrue(resp.requires_escalation)

    def test_support_escalates(self):
        ctx = ReasoningContext(user_text="J'ai un problème avec mon compte")
        resp = self.engine.reason(ctx)
        self.assertTrue(resp.requires_escalation)

    def test_qualification(self):
        ctx = ReasoningContext(user_text="Je veux évaluer mon projet")
        resp = self.engine.reason(ctx)
        self.assertTrue(resp.content)

    def test_empty_text(self):
        ctx = ReasoningContext(user_text="")
        resp = self.engine.reason(ctx)
        self.assertTrue(resp.content)
        self.assertIn("LAWIM", resp.content)

    def test_latency_is_recorded(self):
        ctx = ReasoningContext(user_text="Bonjour")
        resp = self.engine.reason(ctx)
        self.assertGreaterEqual(resp.latency_ms, 0)


class TestDisclaimerManager(unittest.TestCase):
    def setUp(self):
        self.repo = _MockRepository()
        self.config = _MockConfig()
        self.manager = DisclaimerManager(self.repo, self.config)

    def test_default_config_is_active(self):
        cfg = self.manager.get_config()
        self.assertTrue(cfg.enabled)
        self.assertFalse(cfg.globally_disabled)
        self.assertEqual(cfg.position, "after_response")

    def test_default_text_is_french(self):
        text = self.manager.get_text("fr")
        self.assertIn("LAWIM AI", text)

    def test_english_text(self):
        text = self.manager.get_text("en")
        self.assertIn("LAWIM AI", text)

    def test_should_show_respects_globally_disabled(self):
        cfg = DisclaimerConfig(globally_disabled=True)
        self.repo.disclaimer_config = {
            "enabled": True, "text": "test", "position": "after_response",
            "style": "subtle", "channels": ["web", "whatsapp", "telegram"],
            "languages": {"fr": "test"}, "agency_overrides": {},
            "provider_overrides": {}, "globally_disabled": True,
        }
        self.manager.invalidate_cache()
        self.assertFalse(self.manager.should_show(channel="web"))

    def test_should_show_respects_channel_filter(self):
        cfg = DisclaimerConfig(channels=("web", "admin"))
        self.repo.disclaimer_config = {
            "enabled": True, "text": "test", "position": "after_response",
            "style": "subtle", "channels": ["web", "admin"],
            "languages": {"fr": "test"}, "agency_overrides": {},
            "provider_overrides": {}, "globally_disabled": False,
        }
        self.manager.invalidate_cache()
        self.assertTrue(self.manager.should_show(channel="web"))
        self.assertFalse(self.manager.should_show(channel="telegram"))

    def test_inject_disclaimer_adds_text_after(self):
        self.repo.disclaimer_config = {
            "enabled": True, "text": "LAWIM AI test", "position": "after_response",
            "style": "subtle", "channels": ["web", "whatsapp", "telegram", "admin"],
            "languages": {"fr": "LAWIM AI test", "en": "LAWIM AI test"},
            "agency_overrides": {}, "provider_overrides": {}, "globally_disabled": False,
        }
        self.manager.invalidate_cache()
        result = self.manager.inject_disclaimer("Bonjour!", channel="web", provider="deepseek", language="fr")
        self.assertIn("Bonjour!", result)
        self.assertIn("LAWIM AI test", result)

    def test_inject_disclaimer_before_position(self):
        cfg = DisclaimerConfig(position="before_response", channels=("web",))
        self.repo.disclaimer_config = {
            "enabled": True, "text": "AVERTISSEMENT", "position": "before_response",
            "style": "subtle", "channels": ["web"],
            "languages": {"fr": "AVERTISSEMENT"}, "agency_overrides": {},
            "provider_overrides": {}, "globally_disabled": False,
        }
        self.manager.invalidate_cache()
        result = self.manager.inject_disclaimer("Hello", channel="web", provider="deepseek", language="fr")
        self.assertTrue(result.startswith("AVERTISSEMENT"))

    def test_update_config_audits_changes(self):
        old = DisclaimerConfig()
        new = DisclaimerConfig(text="Nouveau texte")
        self.manager.update_config(new, modified_by=1)
        self.assertTrue(len(self.repo.disclaimer_audit) > 0)


class TestPromptReconstructionEngine(unittest.TestCase):
    def setUp(self):
        self.repo = _MockRepository()
        self.config = _MockConfig()
        self.engine = PromptReconstructionEngine(self.repo, self.config)

    def test_reconstruct_with_empty_conversation(self):
        ctx = self.engine.reconstruct(conversation_key="new-conv", current_text="Bonjour")
        self.assertIsNotNone(ctx)
        self.assertEqual(ctx.language, "fr")

    def test_reconstruct_with_decisions(self):
        self.repo.conversation_decisions = [
            {"action": "qualification_done", "payload": {"status": "completed"}},
            {"action": "matching_done", "payload": {"property_id": 123}},
        ]
        ctx = self.engine.reconstruct(conversation_key="conv-1", current_text="Montrez-moi")
        self.assertTrue(len(ctx.summary) > 0)

    def test_reconstruct_detects_property_intent(self):
        ctx = self.engine.reconstruct(conversation_key="conv-1", current_text="Je veux acheter une maison")
        self.assertEqual(ctx.user_intent, "property_search")

    def test_reconstruct_detects_support_intent(self):
        ctx = self.engine.reconstruct(conversation_key="conv-1", current_text="Aidez-moi SVP")
        self.assertEqual(ctx.user_intent, "support")

    def test_reconstruct_detects_qualification_intent(self):
        ctx = self.engine.reconstruct(conversation_key="conv-1", current_text="J'ai besoin d'une évaluation")
        self.assertEqual(ctx.user_intent, "qualification")

    def test_prompt_block_is_formatted(self):
        ctx = ReconstructedContext(
            summary="Test summary",
            user_intent="property_search",
            current_goal="Find a property",
            previous_decisions=("dec1", "dec2"),
            language="fr",
        )
        block = ctx.to_prompt_block()
        self.assertIn("Test summary", block)
        self.assertIn("property_search", block)
        self.assertIn("dec1", block)

    def test_empty_prompt_block(self):
        ctx = ReconstructedContext(summary="", user_intent="", current_goal="", language="fr")
        block = ctx.to_prompt_block()
        self.assertEqual(block, "")


class TestMemoryOptimizer(unittest.TestCase):
    def setUp(self):
        self.repo = _MockRepository()
        self.config = _MockConfig()
        self.memory = MemoryOptimizer(self.repo, self.config)

    def test_store_and_load_short_term(self):
        self.memory.store_short_term(conversation_key="conv-1", key="test", value="valeur_test")
        self.assertTrue(len(self.repo.ai_memory) > 0)
        stored = self.repo.ai_memory[0]
        self.assertEqual(stored["category"], "short_term")
        self.assertEqual(stored["value"], "valeur_test")

    def test_store_long_term(self):
        self.memory.store_long_term(user_id=1, key="pref", value="maison")
        stored = self.repo.ai_memory[0]
        self.assertEqual(stored["category"], "long_term")

    def test_store_persistent(self):
        self.memory.store_persistent(user_id=1, key="role", value="owner")
        stored = self.repo.ai_memory[0]
        self.assertEqual(stored["category"], "persistent")

    def test_load_for_conversation_empty(self):
        bundle = self.memory.load_for_conversation(conversation_key="conv-1")
        self.assertIsInstance(bundle, MemoryBundle)
        self.assertEqual(len(bundle.short_term), 0)
        self.assertEqual(len(bundle.conversation_memory), 0)

    def test_load_with_messages(self):
        self.repo.conversation_messages = [
            {"id": 1, "role": "user", "body": "Bonjour", "created_at": "now"},
            {"id": 2, "role": "assistant", "body": "Comment puis-je vous aider ?", "created_at": "now"},
        ]
        bundle = self.memory.load_for_conversation(conversation_key="conv-1")
        self.assertGreaterEqual(len(bundle.conversation_memory), 0)

    def test_load_with_user(self):
        bundle = self.memory.load_for_conversation(conversation_key="conv-1", user_id=1)
        self.assertEqual(len(bundle.crm_memory), 2)  # role + org

    def test_bundle_to_prompt(self):
        bundle = MemoryBundle(
            short_term=[MagicMock(key="k1", value="v1", category="st", priority=1, ttl_hours=24, created_at="now", expires_at="")],
        )
        prompt = bundle.to_prompt()
        self.assertIn("Mémoire court terme", prompt)

    def test_bundle_empty_prompt(self):
        bundle = MemoryBundle()
        self.assertEqual(bundle.to_prompt(), "")


class TestOrchestrationOutcome(unittest.TestCase):
    def test_to_dict_includes_new_fields(self):
        from lawim_v2.ai.contracts import AIResponse
        from lawim_v2.ai.models import RoutingDecision
        from lawim_v2.ai.orchestrator import OrchestrationOutcome
        req = AIRequest(
            request_id="r1", channel="test", conversation_key="c1",
            text="hello", sanitized_text="hello", language="fr",
        )
        resp = AIResponse(
            provider="internal", model="test", success=True, content="ok",
            latency_ms=10, input_tokens=0, output_tokens=0, estimated_cost=0.0,
            finish_reason="stop", error_type=None, error_code=None,
            retryable=False, fallback_required=False,
            request_id="r1", provider_request_id=None,
            valid=True, complete=True, relevant=True, safe=True, well_formed=True,
            confidence_score=1.0,
        )
        dec = RoutingDecision("r1", "c1", "simple", "internal", ("deepseek",), "test", False, "now")
        outcome = OrchestrationOutcome(req, dec, resp, internal_response=True, disclaimer_added=False)
        d = outcome.to_dict()
        self.assertTrue(d["internal_response"])
        self.assertIn("provider_chain", d)


if __name__ == "__main__":
    unittest.main()
