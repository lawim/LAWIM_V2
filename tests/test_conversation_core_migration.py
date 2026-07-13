from __future__ import annotations

import json
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

    def test_communication_dispatch_without_conversation_core_returns_error(self) -> None:
        config = replace(self.config, ai_orchestrator_enabled=True)
        services = LawimServices(self.repository, config)
        services.communication.conversation_core = None

        message_row = self.repository.create_communication_message(
            channel_type="whatsapp",
            body="Bonjour LAWIM",
            direction="inbound",
            status="delivered",
            message_key="inbound-missing-core-1",
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

        with patch.object(services.communication.repository, "send_whatsapp") as send_whatsapp:
            result = services.communication._dispatch_ai_reply(
                channel="whatsapp",
                normalized=normalized,
                message_row=message_row,
            )

        self.assertEqual(result["status"], "error")
        self.assertEqual(result["reason"], "conversation_core_missing")
        send_whatsapp.assert_not_called()

    def test_conversation_core_uses_deterministic_next_action_without_llm(self) -> None:
        services = LawimServices(self.repository, self.config)
        project_id, actor = self._project_actor()
        self.repository.update_project(project_id, project_type="buy", location_city="Douala")
        message_row = self.repository.create_communication_message(
            channel_type="web",
            body="Je veux un studio à Douala avec budget 50000 XAF",
            direction="inbound",
            status="delivered",
            message_key="core-next-action-1",
        )

        with patch.object(
            services.conversation_core.ai_orchestrator,
            "generate",
            side_effect=AssertionError("LLM should not be called for deterministic next actions"),
        ) as generate:
            result = services.conversation_core.process_message(
                channel="web",
                message="Je veux un studio à Douala avec budget 50000 XAF",
                message_row=message_row,
                project_id=project_id,
                actor=actor,
                language="fr",
            )

        self.assertEqual(result.response_kind, "search_results")
        self.assertEqual(result.plan.intent, "rent")
        self.assertEqual(result.plan.transaction_type, "rent")
        self.assertEqual(result.plan.property_type, "studio")
        self.assertEqual(result.plan.next_action, "SEARCH_LAWIM_PROPERTIES")
        self.assertIn("LAWIM", result.final_text)
        generate.assert_not_called()

    def test_conversation_core_studio_flow_persists_memory_and_executes_real_search(self) -> None:
        services = LawimServices(self.repository, self.config)
        _, actor = self._project_actor()
        project = self.repository.create_project(
            title="Studio Flow",
            project_type="rent",
            objective="Trouver un studio",
            user_id=int(actor["id"]),
            status="draft",
        )
        self.repository.create_property(
            title="Studio A",
            summary="Studio A",
            city="Yaounde",
            country="Cameroon",
            price_min=50000,
            price_max=50000,
            currency="XAF",
            status="published",
            availability="available",
            property_type="studio",
        )
        self.repository.create_property(
            title="Studio B",
            summary="Studio B",
            city="Yaounde",
            country="Cameroon",
            price_min=55000,
            price_max=55000,
            currency="XAF",
            status="published",
            availability="available",
            property_type="studio",
        )

        with patch.object(
            services.conversation_core.ai_orchestrator,
            "generate",
            side_effect=AssertionError("LLM should not be called during the studio flow"),
        ) as generate:
            rows = [
                self.repository.create_communication_message(
                    channel_type="web",
                    body=body,
                    direction="inbound",
                    status="delivered",
                    message_key=f"studio-flow-{index}",
                )
                for index, body in enumerate(["J'ai besoin d'un stuf", "Yaounde", "50 mil"], start=1)
            ]
            first = services.conversation_core.process_message(
                channel="web",
                message="J'ai besoin d'un stuf",
                message_row=rows[0],
                project_id=int(project["id"]),
                actor=dict(actor),
                language="fr",
            )
            second = services.conversation_core.process_message(
                channel="web",
                message="Yaounde",
                message_row=rows[1],
                project_id=int(project["id"]),
                actor=dict(actor),
                language="fr",
            )
            third = services.conversation_core.process_message(
                channel="web",
                message="50 mil",
                message_row=rows[2],
                project_id=int(project["id"]),
                actor=dict(actor),
                language="fr",
            )

        self.assertEqual(first.response_kind, "qualification")
        self.assertIn("ville", first.final_text.lower())
        self.assertEqual(second.response_kind, "qualification")
        self.assertIn("loyer", second.final_text.lower())
        self.assertEqual(third.response_kind, "search_results")
        self.assertIn("Studio A", third.final_text)
        self.assertIn("Studio B", third.final_text)
        self.assertNotIn("Airbnb", third.final_text)
        self.assertNotIn("Booking", third.final_text)
        self.assertEqual(third.plan.conversation_id, f"project:{project['id']}")
        self.assertEqual(third.plan.dossier_id, int(project["id"]))
        self.assertEqual(third.plan.intent, "rent")
        self.assertEqual(third.plan.transaction_type, "rent")
        self.assertEqual(third.plan.property_type, "studio")
        self.assertEqual(third.plan.response_mode, "deterministic_action")
        self.assertEqual(third.plan.business_goal, "search_properties")
        self.assertIn("Yaounde", third.metadata["business_action"]["payload"]["query"])
        self.assertIn("studio", third.metadata["business_action"]["payload"]["query"])
        self.assertIn("50000", third.metadata["business_action"]["payload"]["query"])
        self.assertGreaterEqual(int(third.metadata["business_action"]["payload"]["matching_count"]), 1)
        self.assertTrue(third.metadata["business_action"]["payload"]["search_session_key"])
        generate.assert_not_called()

        context_row = self.repository.get_project_context(int(project["id"]))
        assert context_row is not None
        context = json.loads(str(context_row["context_json"]))
        self.assertEqual(context["captured_facts"]["city"], "Yaounde")
        self.assertEqual(context["captured_facts"]["budget_max"], 50000)
        self.assertEqual(context["captured_facts"]["property_type"], "studio")
        self.assertEqual(context["captured_facts"]["transaction_type"], "rent")
        self.assertEqual(context["captured_facts"]["intent"], "rent")
        self.assertEqual(context["conversation_id"], f"project:{project['id']}")
        self.assertEqual(context["dossier_id"], int(project["id"]))

        memories = self.repository.list_brain_memory(int(project["id"]), status="active")
        field_values = {str(item.get("field_key")): str(item.get("value")) for item in memories if item.get("field_key")}
        self.assertEqual(field_values.get("city"), "Yaounde")
        self.assertEqual(field_values.get("budget_max"), "50000")
        self.assertEqual(field_values.get("property_type"), "studio")
        self.assertEqual(field_values.get("transaction_type"), "rent")
        self.assertEqual(field_values.get("intent"), "rent")

        matching_sessions = self.repository.all("SELECT * FROM rei_matching_sessions WHERE project_id = ? ORDER BY id DESC LIMIT 1", (int(project["id"]),))
        self.assertEqual(len(matching_sessions), 1)
        self.assertEqual(json.loads(str(matching_sessions[0]["criteria_json"]))["city"], "Yaounde")
        self.assertEqual(json.loads(str(matching_sessions[0]["criteria_json"]))["property_type"], "studio")
        self.assertEqual(json.loads(str(matching_sessions[0]["criteria_json"]))["budget_max"], 50000)
