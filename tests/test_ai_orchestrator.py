from __future__ import annotations

import json
from dataclasses import dataclass, field, replace
from http import HTTPStatus

from lawim_v2.ai import AIOrchestrator, AIRequest, AIResponse, CostEstimate, ProviderHealth, UsageStatus
from lawim_v2.ai.fallback import FallbackEngine
from lawim_v2.ai.providers.internal_fallback import InternalFallbackProvider
from tests.lawim_harness import DummyHandler, LawimTestHarness


def _response(
    *,
    provider: str,
    model: str,
    content: str,
    success: bool = True,
    error_type: str | None = None,
    error_code: str | None = None,
    retryable: bool = False,
    fallback_required: bool = False,
    valid: bool = True,
    complete: bool = True,
    relevant: bool = True,
    safe: bool = True,
    well_formed: bool = True,
    confidence_score: float = 0.92,
    latency_ms: int = 7,
    input_tokens: int = 12,
    output_tokens: int = 18,
    estimated_cost: float = 0.001,
    finish_reason: str | None = "stop",
    provider_request_id: str | None = None,
) -> AIResponse:
    return AIResponse(
        provider=provider,
        model=model,
        success=success,
        content=content,
        latency_ms=latency_ms,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        estimated_cost=estimated_cost,
        finish_reason=finish_reason,
        error_type=error_type,
        error_code=error_code,
        retryable=retryable,
        fallback_required=fallback_required,
        request_id="request-1",
        provider_request_id=provider_request_id or f"{provider}-provider-request",
        valid=valid,
        complete=complete,
        relevant=relevant,
        safe=safe,
        well_formed=well_formed,
        confidence_score=confidence_score,
        metadata={"provider": provider},
    )


@dataclass
class StubProvider:
    name: str
    result: AIResponse | Exception
    enabled: bool = True
    calls: list[str] = field(default_factory=list)

    def is_enabled(self) -> bool:
        return self.enabled

    def health_check(self) -> ProviderHealth:
        return ProviderHealth(
            provider=self.name,
            model=self.result.model if isinstance(self.result, AIResponse) else self.name,
            enabled=self.enabled,
            available=self.enabled,
            state="ready" if self.enabled else "disabled",
            checked_at="2026-07-12T00:00:00+00:00",
            latency_ms=1,
        )

    def generate(self, request: AIRequest) -> AIResponse:
        self.calls.append(self.name)
        if isinstance(self.result, Exception):
            raise self.result
        return self.result

    def estimate_cost(self, request: AIRequest) -> CostEstimate:
        content = self.result.content if isinstance(self.result, AIResponse) else ""
        return CostEstimate(
            provider=self.name,
            model=self.result.model if isinstance(self.result, AIResponse) else self.name,
            input_tokens=max(1, len(request.text) // 4),
            output_tokens=max(1, len(content) // 4),
            estimated_cost=0.0,
        )

    def get_usage_status(self) -> UsageStatus:
        return UsageStatus(provider=self.name, model=self.name)


class OrchestratorTestMixin(LawimTestHarness):
    def _build_orchestrator(self, providers: dict[str, StubProvider | InternalFallbackProvider]) -> AIOrchestrator:
        return AIOrchestrator(self.repository, self.config, providers=providers)  # type: ignore[arg-type]


class AIOrchestratorTests(OrchestratorTestMixin):
    def setUp(self) -> None:
        super().setUp()
        self.config = replace(
            self.config,
            ai_orchestrator_enabled=True,
            ai_learning_enabled=True,
            ai_learning_requires_human_approval=True,
        )

    def test_simple_request_routes_to_deepseek(self) -> None:
        providers = {
            "deepseek": StubProvider("deepseek", _response(provider="deepseek", model="deepseek-v4-flash", content="Réponse DeepSeek")),
            "openai": StubProvider("openai", _response(provider="openai", model="gpt-4o-mini", content="Réponse OpenAI")),
            "gemini_primary": StubProvider("gemini_primary", _response(provider="gemini_primary", model="gemini-3.5-flash", content="Réponse Gemini")),
            "gemini_secondary": StubProvider("gemini_secondary", _response(provider="gemini_secondary", model="gemini-2.5-flash", content="Réponse Gemini 2")),
            "internal": InternalFallbackProvider(enabled=True, resolver=FallbackEngine(self.repository, self.config)),
        }
        orchestrator = self._build_orchestrator(providers)
        request = orchestrator.build_request(
            channel="whatsapp",
            text="Bonjour LAWIM",
            conversation_key="whatsapp:+237600000000",
            external_chat_id="+237600000000",
            message_id="msg-1",
        )

        outcome = orchestrator.generate(request)

        self.assertEqual(outcome.decision.selected_provider, "deepseek")
        self.assertEqual(outcome.response.provider, "deepseek")
        self.assertEqual(outcome.response.content, "Réponse DeepSeek")
        self.assertEqual(self.repository.scalar("SELECT COUNT(*) FROM ai_requests"), 1)
        self.assertEqual(self.repository.scalar("SELECT COUNT(*) FROM ai_responses"), 1)
        self.assertEqual(self.repository.scalar("SELECT COUNT(*) FROM ai_routing_decisions"), 1)

    def test_complex_request_routes_to_openai(self) -> None:
        providers = {
            "deepseek": StubProvider("deepseek", _response(provider="deepseek", model="deepseek-v4-flash", content="Réponse DeepSeek")),
            "openai": StubProvider("openai", _response(provider="openai", model="gpt-4o-mini", content="Analyse OpenAI")),
            "gemini_primary": StubProvider("gemini_primary", _response(provider="gemini_primary", model="gemini-3.5-flash", content="Réponse Gemini")),
            "gemini_secondary": StubProvider("gemini_secondary", _response(provider="gemini_secondary", model="gemini-2.5-flash", content="Réponse Gemini 2")),
            "internal": InternalFallbackProvider(enabled=True, resolver=FallbackEngine(self.repository, self.config)),
        }
        orchestrator = self._build_orchestrator(providers)
        request = orchestrator.build_request(
            channel="telegram",
            text="Analyse juridique détaillée de ce contrat et comparaison avec plusieurs options",
            conversation_key="telegram:123456789",
            external_chat_id="123456789",
            message_id="msg-2",
        )

        outcome = orchestrator.generate(request)

        self.assertEqual(outcome.decision.selected_provider, "openai")
        self.assertEqual(outcome.response.provider, "openai")
        self.assertEqual(outcome.response.content, "Analyse OpenAI")
        self.assertEqual([provider for provider in outcome.decision.chain[:2]], ["openai", "deepseek"])

    def test_fallback_chain_uses_gemini_then_internal(self) -> None:
        call_order: list[str] = []

        def failing(provider_name: str) -> StubProvider:
            return StubProvider(provider_name, _response(provider=provider_name, model=f"{provider_name}-model", content="", success=False, error_type="request_failed", error_code="500", valid=False, complete=False, relevant=False, safe=True, well_formed=False), calls=call_order)

        providers = {
            "deepseek": failing("deepseek"),
            "openai": failing("openai"),
            "gemini_primary": StubProvider("gemini_primary", _response(provider="gemini_primary", model="gemini-3.5-flash", content="Réponse Gemini primaire"), calls=call_order),
            "gemini_secondary": StubProvider("gemini_secondary", _response(provider="gemini_secondary", model="gemini-2.5-flash", content="Réponse Gemini secondaire"), calls=call_order),
            "internal": InternalFallbackProvider(enabled=True, resolver=FallbackEngine(self.repository, self.config)),
        }
        orchestrator = self._build_orchestrator(providers)
        request = orchestrator.build_request(
            channel="whatsapp",
            text="Aide-moi à résoudre ce cas simple",
            conversation_key="whatsapp:+237611111111",
            external_chat_id="+237611111111",
            message_id="msg-3",
        )

        outcome = orchestrator.generate(request)

        self.assertEqual(outcome.response.provider, "gemini_primary")
        self.assertEqual(outcome.decision.selected_provider, "gemini_primary")
        self.assertEqual(call_order[:3], ["deepseek", "openai", "gemini_primary"])

    def test_internal_fallback_is_used_when_all_external_providers_fail(self) -> None:
        providers = {
            "deepseek": StubProvider("deepseek", _response(provider="deepseek", model="deepseek-v4-flash", content="", success=False, error_type="request_failed", error_code="500", valid=False, complete=False, relevant=False, safe=True, well_formed=False)),
            "openai": StubProvider("openai", _response(provider="openai", model="gpt-4o-mini", content="", success=False, error_type="request_failed", error_code="500", valid=False, complete=False, relevant=False, safe=True, well_formed=False)),
            "gemini_primary": StubProvider("gemini_primary", _response(provider="gemini_primary", model="gemini-3.5-flash", content="", success=False, error_type="request_failed", error_code="500", valid=False, complete=False, relevant=False, safe=True, well_formed=False)),
            "gemini_secondary": StubProvider("gemini_secondary", _response(provider="gemini_secondary", model="gemini-2.5-flash", content="", success=False, error_type="request_failed", error_code="500", valid=False, complete=False, relevant=False, safe=True, well_formed=False)),
            "internal": InternalFallbackProvider(enabled=True, resolver=FallbackEngine(self.repository, self.config)),
        }
        orchestrator = self._build_orchestrator(providers)
        request = orchestrator.build_request(
            channel="whatsapp",
            text="Contact: example@example.com. Mon token est sk-1234567890123456789012345.",
            conversation_key="whatsapp:+237620000000",
            external_chat_id="+237620000000",
            message_id="msg-4",
        )

        outcome = orchestrator.generate(request)

        self.assertEqual(outcome.response.provider, "internal")
        self.assertTrue(outcome.decision.fallback_used)
        candidate = self.repository.one("SELECT * FROM ai_learning_candidates ORDER BY id DESC LIMIT 1")
        self.assertIsNotNone(candidate)
        assert candidate is not None
        question_examples = str(candidate["question_examples_json"])
        self.assertNotIn("example@example.com", question_examples)
        self.assertNotIn("sk-1234567890123456789012345", question_examples)


class WebhookAIReplyTests(OrchestratorTestMixin):
    def setUp(self) -> None:
        super().setUp()
        self.config = replace(
            self.config,
            ai_orchestrator_enabled=True,
            ai_learning_enabled=True,
            green_api_webhook_secret="green-api-webhook-secret",
            telegram_webhook_secret="telegram-webhook-secret",
        )

    def _incoming_whatsapp_payload(self) -> dict[str, object]:
        return {
            "typeWebhook": "incomingMessageReceived",
            "instanceData": {
                "idInstance": 7107644927,
                "wid": "7107644927@c.us",
                "typeInstance": "whatsapp",
            },
            "timestamp": 1727698597,
            "idMessage": "AI-WA-1",
            "senderData": {
                "chatId": "237650000000@c.us",
                "sender": "237650000000@c.us",
                "senderName": "Test Sender",
                "senderContactName": "Test Sender",
            },
            "messageData": {
                "typeMessage": "textMessage",
                "textMessageData": {
                    "textMessage": "Bonjour LAWIM",
                },
            },
        }

    def _incoming_telegram_payload(self) -> dict[str, object]:
        return {
            "update_id": 1000001,
            "message": {
                "message_id": 42,
                "date": 1727698597,
                "chat": {
                    "id": 123456789,
                    "type": "private",
                    "username": "tester",
                },
                "from": {
                    "id": 987654321,
                    "is_bot": False,
                    "first_name": "Jane",
                    "last_name": "Doe",
                    "username": "janedoe",
                },
                "text": "Bonjour LAWIM sur Telegram",
            },
        }

    def _invoke_with_orchestrator(
        self,
        path: str,
        *,
        method: str = "POST",
        body: dict[str, object] | None = None,
        raw_body: bytes | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
        orchestrator: AIOrchestrator,
    ) -> DummyHandler:
        request_headers: dict[str, str] = dict(headers or {})
        payload = b""
        if raw_body is not None:
            payload = raw_body
            request_headers.setdefault("Content-Length", str(len(payload)))
        if body is not None:
            payload = json.dumps(body).encode("utf-8")
            request_headers.setdefault("Content-Length", str(len(payload)))
            request_headers.setdefault("Content-Type", "application/json")
        if token:
            request_headers["Authorization"] = f"Bearer {token}"

        handler = DummyHandler(self.repository, self.config, path, method=method, headers=request_headers, body=payload)
        handler.services.ai = orchestrator
        handler.services.communication.ai_orchestrator = orchestrator
        handler.client_address = ("127.0.0.1", 0)
        handler.auth_limiter = self.auth_limiter
        if method == "POST":
            handler.do_POST()
        elif method == "GET":
            handler.do_GET()
        else:
            raise AssertionError(f"Unsupported method: {method}")
        return handler

    def test_whatsapp_incoming_message_triggers_ai_reply(self) -> None:
        providers = {
            "deepseek": StubProvider("deepseek", _response(provider="deepseek", model="deepseek-v4-flash", content="Bonjour, je prends en charge votre demande.")),
            "openai": StubProvider("openai", _response(provider="openai", model="gpt-4o-mini", content="Réponse OpenAI")),
            "gemini_primary": StubProvider("gemini_primary", _response(provider="gemini_primary", model="gemini-3.5-flash", content="Réponse Gemini")),
            "gemini_secondary": StubProvider("gemini_secondary", _response(provider="gemini_secondary", model="gemini-2.5-flash", content="Réponse Gemini 2")),
            "internal": InternalFallbackProvider(enabled=True, resolver=FallbackEngine(self.repository, self.config)),
        }
        orchestrator = self._build_orchestrator(providers)
        before_messages = self.repository.scalar("SELECT COUNT(*) FROM communication_messages")

        response = self._invoke_with_orchestrator(
            "/api/notifications/whatsapp/webhook",
            body=self._incoming_whatsapp_payload(),
            token="green-api-webhook-secret",
            orchestrator=orchestrator,
        )

        self.assertEqual(response.status, HTTPStatus.OK, msg=response.body_text())
        body = response.body_json()
        self.assertEqual(body["ai_reply"]["status"], "sent")
        self.assertEqual(body["ai_reply"]["provider"], "deepseek")
        self.assertEqual(self.repository.scalar("SELECT COUNT(*) FROM communication_messages"), before_messages + 2)
        outbound = self.repository.one(
            "SELECT * FROM communication_messages WHERE channel_type = 'whatsapp' AND direction = 'outbound' ORDER BY id DESC LIMIT 1"
        )
        self.assertIsNotNone(outbound)
        assert outbound is not None
        self.assertEqual(str(outbound["status"]), "sent")
        self.assertIn("Bonjour, je prends en charge votre demande.", str(outbound["body"]))

    def test_telegram_incoming_message_triggers_ai_reply(self) -> None:
        providers = {
            "deepseek": StubProvider("deepseek", _response(provider="deepseek", model="deepseek-v4-flash", content="Réponse Telegram LAWIM.")),
            "openai": StubProvider("openai", _response(provider="openai", model="gpt-4o-mini", content="Réponse OpenAI")),
            "gemini_primary": StubProvider("gemini_primary", _response(provider="gemini_primary", model="gemini-3.5-flash", content="Réponse Gemini")),
            "gemini_secondary": StubProvider("gemini_secondary", _response(provider="gemini_secondary", model="gemini-2.5-flash", content="Réponse Gemini 2")),
            "internal": InternalFallbackProvider(enabled=True, resolver=FallbackEngine(self.repository, self.config)),
        }
        orchestrator = self._build_orchestrator(providers)
        before_messages = self.repository.scalar("SELECT COUNT(*) FROM communication_messages")

        response = self._invoke_with_orchestrator(
            "/api/notifications/telegram/webhook",
            body=self._incoming_telegram_payload(),
            headers={"X-Telegram-Bot-Api-Secret-Token": "telegram-webhook-secret"},
            orchestrator=orchestrator,
        )

        self.assertEqual(response.status, HTTPStatus.OK, msg=response.body_text())
        body = response.body_json()
        self.assertEqual(body["ai_reply"]["status"], "sent")
        self.assertEqual(body["ai_reply"]["provider"], "deepseek")
        self.assertEqual(self.repository.scalar("SELECT COUNT(*) FROM communication_messages"), before_messages + 2)
        outbound = self.repository.one(
            "SELECT * FROM communication_messages WHERE channel_type = 'telegram' AND direction = 'outbound' ORDER BY id DESC LIMIT 1"
        )
        self.assertIsNotNone(outbound)
        assert outbound is not None
        self.assertEqual(str(outbound["status"]), "sent")
        self.assertIn("Réponse Telegram LAWIM.", str(outbound["body"]))
