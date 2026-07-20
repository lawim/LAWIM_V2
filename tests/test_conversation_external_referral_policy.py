from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from lawim_v2.communication.service import CommunicationService

FORBIDDEN_EXTERNAL_REFERRALS = (
    "Jumia House",
    "Jumia",
    "SeLoger",
    "Leboncoin",
    "Facebook",
    "groupe Facebook",
    "agence immobilière externe",
    "site d'annonces",
    "plateforme immobilière",
)


def _make_svc() -> CommunicationService:
    return CommunicationService(
        repository=MagicMock(),
        project_service=MagicMock(),
        policy=MagicMock(),
        config=MagicMock(),
        ai_orchestrator=None,
        disclaimer_manager=MagicMock(),
    )


@pytest.mark.parametrize("referral", FORBIDDEN_EXTERNAL_REFERRALS)
def test_static_greeting_does_not_refer_to_external(referral: str) -> None:
    svc = _make_svc()
    for channel in ("whatsapp", "telegram"):
        for lang in ("fr", "en", "pcm"):
            response = svc._greeting_response(channel, language=lang)
            assert referral.lower() not in response.lower(), (
                f"Greeting response for {channel}/{lang} contains forbidden referral: {referral}"
            )


@pytest.mark.parametrize("referral", FORBIDDEN_EXTERNAL_REFERRALS)
def test_format_ai_footer_does_not_contain_external_referral(referral: str) -> None:
    svc = _make_svc()
    for lang in ("fr", "en", "pcm"):
        for channel in ("whatsapp", "telegram"):
            footer = svc._format_ai_footer(lang, channel)
            assert referral.lower() not in footer.lower(), (
                f"Footer for {channel}/{lang} contains forbidden referral: {referral}"
            )


def test_ai_footer_texts_are_clean() -> None:
    svc = _make_svc()
    for lang, text in svc.AI_FOOTER_TEXTS.items():
        for ref in FORBIDDEN_EXTERNAL_REFERRALS:
            assert ref.lower() not in text.lower(), (
                f"AI_FOOTER_TEXTS['{lang}'] contains forbidden referral: {ref}"
            )
