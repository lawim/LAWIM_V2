from __future__ import annotations

from dataclasses import replace
from types import SimpleNamespace
from unittest.mock import patch

from lawim_v2.services import LawimServices

from tests.lawim_harness import LawimTestHarness


def _fake_core_result(
    *,
    final_text: str = "Réponse LAWIM",
    provider: str = "internal",
    selected_provider: str = "internal",
    fallback_used: bool = True,
    response_source: str = "deterministic",
    analysis: dict[str, object] | None = None,
    progression: dict[str, object] | None = None,
    language: str = "fr",
    conversation_key: str = "project:1",
    thread_id: int | None = 42,
    contact: dict[str, object] | None = None,
    request_id: str = "ai-test-1",
    provider_request_id: str = "prov-1",
) -> SimpleNamespace:
    analysis_payload = analysis or {
        "primary_intent": "buy",
        "primary_score": 83,
        "is_multi_intent": False,
        "intents": [{"intent": "buy", "score": 83, "confidence": 0.9}],
        "entities": {"cities": ["Douala"], "budgets": [], "property_types": [], "surfaces_m2": [], "bedrooms": []},
        "language": language,
        "is_confirmation": None,
        "is_rejection": None,
    }
    progression_payload = progression or {
        "intent": "buy",
        "progress_pct": 50,
        "total_steps": 6,
        "known_fields": ["city"],
        "known_labels": ["ville"],
        "missing_fields": ["budget_max"],
        "next_question": "Quel est votre budget maximum ?",
        "next_key": "buy_budget",
        "complete": False,
        "next_actions": ["Rechercher des biens", "Préparer un dossier"],
    }
    request = SimpleNamespace(request_id=request_id)
    decision = SimpleNamespace(selected_provider=selected_provider, fallback_used=fallback_used)
    response = SimpleNamespace(provider=provider, provider_request_id=provider_request_id)
    outcome = SimpleNamespace(request=request, decision=decision, response=response)
    plan = SimpleNamespace(
        conversation_key=conversation_key,
        thread_id=thread_id,
        contact=contact,
        analysis=analysis_payload,
        progression=progression_payload,
        memory_summary={"total": 0, "confirmed_facts": []},
        language=language,
    )
    return SimpleNamespace(
        plan=plan,
        request=request,
        outcome=outcome,
        final_text=final_text,
        response_quality={"valid": True, "complete": True, "relevant": True, "safe": True, "well_formed": True, "confidence_score": 0.95},
        response_kind="ai",
        response_source=response_source,
        fallback_used=fallback_used,
        should_escalate=False,
        metadata={"conversation_key": conversation_key},
    )


class ConversationCoreMigrationTests(LawimTestHarness):
    def _project_actor(self) -> tuple[int, dict[str, object]]:
        project = self.repository.one("SELECT * FROM projects ORDER BY id ASC LIMIT 1")
        assert project is not None
        actor = self.repository.get_user_by_id(int(project["user_id"]))
        return int(project["id"]), dict(actor)

    def test_conversation_core_blocks_external_services_with_refusal(self) -> None:
        services = LawimServices(self.repository, self.config)
        project_id, actor = self._project_actor()
        message_row = self.repository.create_communication_message(
            channel_type="web",
            body="Peux-tu chercher sur Airbnb ?",
            direction="inbound",
            status="delivered",
            message_key="core-refusal-1",
        )

        result = services.conversation_core.process_message(
            channel="web",
            message="Peux-tu chercher sur Airbnb ?",
            message_row=message_row,
            project_id=project_id,
            actor=actor,
            language="fr",
        )
        persisted = self.repository.get_communication_message(int(message_row["id"]))

        self.assertEqual(result.response_kind, "refusal")
        self.assertEqual(result.response_source, "deterministic")
        self.assertIn("LAWIM", result.final_text)
        self.assertIn("plateforme extérieure", result.final_text)
        self.assertTrue(result.response_quality["valid"])
        self.assertEqual(persisted["status"], "processed")

    def test_ai_request_uses_requested_language(self) -> None:
        services = LawimServices(self.repository, self.config)
        request = services.ai.build_request(
            channel="web",
            text="Bonjour LAWIM",
            conversation_key="web:test-language",
            language="pcm",
        )

        self.assertEqual(request.language, "pcm")
        self.assertIn("LAWIM AI", str(request.metadata.get("system_prompt")))

    def test_assistant_chat_routes_through_shared_conversation_core(self) -> None:
        services = LawimServices(self.repository, self.config)
        fake_result = _fake_core_result(final_text="Réponse LAWIM via le noyau partagé")
        services.assistant.conversation_core = SimpleNamespace(process_message=lambda **kwargs: fake_result)

        project_id, actor = self._project_actor()
        payload = services.assistant.chat(
            actor=actor,
            project_id=project_id,
            message="Bonjour LAWIM",
        )
        chat = payload["chat"]

        self.assertEqual(chat["assistant_message"]["content"], fake_result.final_text)
        self.assertEqual(chat["provider"], "internal")
        self.assertTrue(chat["fallback_used"])
        self.assertEqual(chat["turn"]["provider"], "internal")

    def test_brain_chat_routes_through_shared_conversation_core(self) -> None:
        services = LawimServices(self.repository, self.config)
        fake_result = _fake_core_result(
            final_text="Réponse LAWIM pour le brain",
            response_source="ai",
            progression={
                "intent": "buy",
                "progress_pct": 33,
                "total_steps": 6,
                "known_fields": ["city"],
                "known_labels": ["ville"],
                "missing_fields": ["budget_max"],
                "next_question": "Quel est votre budget maximum ?",
                "next_key": "buy_budget",
                "complete": False,
                "next_actions": ["Comparer des biens"],
            },
        )
        services.brain.conversation_core = SimpleNamespace(process_message=lambda **kwargs: fake_result)

        project_id, actor = self._project_actor()
        result = services.brain.process_chat(
            actor=actor,
            project_id=project_id,
            message="Je cherche un logement",
            language="fr",
            channel="web",
        )

        self.assertEqual(result["analysis"]["primary_intent"], "buy")
        self.assertEqual(result["detected_language"], "fr")
        self.assertEqual(result["progression"]["next_question"], "Quel est votre budget maximum ?")
        self.assertGreaterEqual(len(result["suggestions"]), 1)

    def test_communication_dispatch_routes_through_shared_conversation_core(self) -> None:
        config = replace(self.config, ai_orchestrator_enabled=True)
        services = LawimServices(self.repository, config)
        fake_result = _fake_core_result(
            final_text="Réponse LAWIM livrée",
            provider_request_id="prov-out-1",
            conversation_key="whatsapp:237686822667@c.us",
            thread_id=7,
            contact={"id": 11, "organization_id": 1},
        )
        services.communication.conversation_core = SimpleNamespace(process_message=lambda **kwargs: fake_result)

        message_row = self.repository.create_communication_message(
            channel_type="whatsapp",
            body="Bonjour LAWIM",
            direction="inbound",
            status="delivered",
            message_key="inbound-test-1",
        )
        normalized = {
            "chat_id": "237686822667@c.us",
            "chat_id_raw": "237686822667@c.us",
            "sender": "237686822667@c.us",
            "user_id": "237686822667",
            "language": "fr",
            "message_body": "Bonjour LAWIM",
            "sender_name": "Client LAWIM",
            "type_webhook": "incomingMessageReceived",
        }

        with patch.object(
            services.communication.repository,
            "send_whatsapp",
            return_value={
                "id": 99,
                "delivery_status": "sent",
                "delivery": {
                    "delivery_status": "sent",
                    "http_status": 200,
                    "provider_message_id": "prov-out-1",
                    "resolved_ipv4": "149.154.166.110",
                    "sanitized_url": "https://api.greenapi.com/[redacted]",
                    "ok": True,
                    "response_json": {"description": "OK"},
                },
            },
        ) as send_whatsapp:
            result = services.communication._dispatch_ai_reply(
                channel="whatsapp",
                normalized=normalized,
                message_row=message_row,
            )

        self.assertIsNotNone(result)
        self.assertEqual(result["status"], "sent")
        self.assertEqual(result["provider_message_id"], "prov-out-1")
        self.assertEqual(result["selected_provider"], "internal")
        self.assertTrue(send_whatsapp.called)
