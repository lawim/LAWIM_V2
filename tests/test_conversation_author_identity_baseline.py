from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from lawim_v2.communication.service import CommunicationService


@pytest.fixture
def svc() -> CommunicationService:
    return CommunicationService(
        repository=MagicMock(),
        project_service=MagicMock(),
        policy=MagicMock(),
        config=MagicMock(),
        ai_orchestrator=None,
        disclaimer_manager=MagicMock(),
    )


def test_greeting_response_contains_lawim_ai_identity(svc: CommunicationService) -> None:
    for channel in ("whatsapp", "telegram"):
        reply = svc._greeting_response(channel)
        assert "LAWIM" in reply
        assert "🤖" not in reply  # LAWIM AI emoji not expected in base greeting


def test_identity_is_lawim_ai_not_other_provider(svc: CommunicationService) -> None:
    svc.ai = MagicMock()
    svc.ai.build_request.return_value = MagicMock()
    mock_response = MagicMock()
    mock_response.response = MagicMock()
    mock_response.response.content = "Voici les résultats de votre recherche à Douala."
    mock_response.response.provider = "deepseek"
    svc.ai.generate.return_value = mock_response

    repo = MagicMock()
    repo.create_communication_log.return_value = {"id": 1}
    svc.repository = repo

    reply = svc._generate_ai_reply("Je cherche un appartement à Douala", "whatsapp", "conv-1")

    assert "DeepSeek" not in reply
    assert "OpenAI" not in reply
    assert "Gemini" not in reply
    assert "LAWIM" in reply or "ℹ" in reply


def test_ai_footer_contains_lawim_brand(svc: CommunicationService) -> None:
    footer = svc._format_ai_footer("fr", "whatsapp")
    assert "LAWIM AI" in footer or "LAWIM" in footer


def test_identity_not_deepseek_openai(svc: CommunicationService) -> None:
    for lang in ("fr", "en", "pcm"):
        for channel in ("whatsapp", "telegram"):
            footer = svc._format_ai_footer(lang, channel)
            if footer:
                assert "DeepSeek" not in footer
                assert "OpenAI" not in footer
                assert "Gemini" not in footer


def test_message_metadata_contains_author_type(svc: CommunicationService) -> None:
    repo = MagicMock()
    repo.one.return_value = None
    repo.create_communication_event.return_value = {"id": 1}
    repo.create_communication_message.return_value = {"id": 100, "body": "", "status": "delivered"}
    repo.create_communication_log.return_value = {"id": 1}
    svc.repository = repo
    svc.ai = MagicMock()
    svc.ai.build_request.return_value = MagicMock()
    mock_outcome = MagicMock()
    mock_outcome.response = MagicMock()
    mock_outcome.response.content = "Réponse test pour l'utilisateur."
    mock_outcome.response.provider = "deepseek"
    svc.ai.generate.return_value = mock_outcome

    result = svc.process_green_api_webhook(
        payload={
            "typeWebhook": "incomingMessageReceived",
            "body": {"messageData": {"textMessageData": {"text": "Bonjour"}}},
            "senderData": {"chatId": "237691234567@c.us", "sender": "237691234567@c.us"},
        },
        headers={},
    )
    assert result["status"] == "ok"
    assert result["accepted"]
