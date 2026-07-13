from __future__ import annotations

import unittest
from pathlib import Path

from lawim_v2.ai.orchestrator import AIMessage, AIOrchestrator, build_provider_chain
from lawim_v2.config import AppConfig


class FakeRepository:
    pass


class AiOrchestratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = AppConfig.for_test(
            db_path=Path("/tmp/lawim-ai-tests.db"),
            media_storage_path=Path("/tmp/lawim-ai-media"),
            ai_orchestrator_enabled=True,
            ai_provider_deepseek_enabled=True,
            ai_provider_openai_enabled=True,
            ai_provider_gemini_primary_enabled=True,
            ai_provider_gemini_secondary_enabled=True,
            ai_primary_provider="deepseek",
            ai_complex_provider="openai",
            ai_fallback_chain=("deepseek", "openai", "gemini_primary", "gemini_secondary", "internal"),
        )
        self.orchestrator = AIOrchestrator(repository=FakeRepository(), config=self.config, providers={})

    def test_build_provider_chain_orders_simple_and_complex_requests(self) -> None:
        simple_chain = build_provider_chain(
            complexity="simple",
            primary_provider="deepseek",
            complex_provider="openai",
            fallback_chain=("deepseek", "openai", "gemini_primary", "gemini_secondary", "internal"),
        )
        complex_chain = build_provider_chain(
            complexity="complex",
            primary_provider="deepseek",
            complex_provider="openai",
            fallback_chain=("deepseek", "openai", "gemini_primary", "gemini_secondary", "internal"),
        )
        self.assertEqual(simple_chain[0], "deepseek")
        self.assertEqual(simple_chain[1], "openai")
        self.assertEqual(complex_chain[0], "openai")
        self.assertEqual(complex_chain[1], "deepseek")
        self.assertEqual(simple_chain[-1], "internal")
        self.assertEqual(complex_chain[-1], "internal")

    def test_build_request_preserves_metadata(self) -> None:
        request = self.orchestrator.build_request(
            channel="whatsapp",
            text="Bonjour LAWIM",
            conversation_key="conversation-1",
            external_chat_id="12345@c.us",
            external_user_id="12345",
            message_id="msg-1",
            context_messages=(AIMessage(role="assistant", content="Salut"),),
            metadata={"system_prompt": "SYS"},
            max_output_tokens=128,
        )
        self.assertEqual(request.channel, "whatsapp")
        self.assertEqual(request.conversation_key, "conversation-1")
        self.assertEqual(request.external_chat_id, "12345@c.us")
        self.assertEqual(request.message_id, "msg-1")
        self.assertEqual(request.context_messages[0].content, "Salut")
        self.assertIn("LAWIM", request.metadata["system_prompt"])
        self.assertEqual(request.max_output_tokens, 128)

    def test_classify_detects_simple_and_complex_requests(self) -> None:
        simple = self.orchestrator.classify("Bonjour")
        complex_report = self.orchestrator.classify("Analyse détaillée de plusieurs points avec comparaison")
        self.assertEqual(simple.complexity, "simple")
        self.assertEqual(complex_report.complexity, "complex")
        self.assertEqual(simple.reason, "heuristic_simple")
        self.assertEqual(complex_report.reason, "heuristic_complexity")


if __name__ == "__main__":
    unittest.main()
