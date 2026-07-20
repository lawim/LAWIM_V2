from __future__ import annotations

from unittest.mock import MagicMock, patch

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


def test_french_footer_has_ten_words_or_less(svc: CommunicationService) -> None:
    footer = svc.AI_FOOTER_TEXTS.get("fr", "")
    word_count = len(footer.split())
    assert word_count <= 10, f"FR footer has {word_count} words, expected ≤ 10"
    assert "ℹ️" in footer


def test_english_footer_has_ten_words_or_less(svc: CommunicationService) -> None:
    footer = svc.AI_FOOTER_TEXTS.get("en", "")
    word_count = len(footer.split())
    assert word_count <= 10, f"EN footer has {word_count} words, expected ≤ 10"


def test_pcm_footer_has_ten_words_or_less(svc: CommunicationService) -> None:
    footer = svc.AI_FOOTER_TEXTS.get("pcm", "")
    word_count = len(footer.split())
    assert word_count <= 10, f"PCM footer has {word_count} words, expected ≤ 10"


def test_footer_present_when_generated_by_ai(svc: CommunicationService) -> None:
    svc.ai = MagicMock()
    svc.ai.build_request.return_value = MagicMock()
    mock_outcome = MagicMock()
    mock_outcome.response = MagicMock()
    mock_outcome.response.content = "Voici des annonces à Douala."
    mock_outcome.response.provider = "deepseek"
    svc.ai.generate.return_value = mock_outcome
    svc.repository = MagicMock()
    svc.repository.create_communication_log.return_value = {"id": 1}

    reply = svc._generate_ai_reply("Je cherche un appartement à Douala", "whatsapp", "conv-1")
    assert "ℹ️" in reply or "──────────────" in reply


def test_footer_absent_when_generated_by_ai_false(svc: CommunicationService) -> None:
    reply = svc._greeting_response("dashboard")
    assert "ℹ️" not in reply
    assert "──────────────" not in reply


def test_footer_non_blocking_on_exception(svc: CommunicationService) -> None:
    svc.ai = MagicMock()
    svc.ai.build_request.side_effect = Exception("AI unavailable")

    with patch.object(svc, "_format_ai_footer", side_effect=Exception("Footer crash")):
        reply = svc._generate_ai_reply("Je cherche un appartement", "whatsapp", "conv-1")
        assert reply != ""
        assert isinstance(reply, str)


def test_footer_separated_from_content(svc: CommunicationService) -> None:
    for channel in ("whatsapp", "telegram"):
        footer = svc._format_ai_footer("fr", channel)
        if footer:
            assert "\n" in footer, "Footer should have newline separator"
            assert "──────────────" in footer, "Footer should have visual separator"
