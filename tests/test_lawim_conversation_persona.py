from __future__ import annotations

import pytest

from lawim_v2.conversation.policy.persona import LawimConversationPersona, get_lawim_persona


def test_persona_default_code() -> None:
    persona = get_lawim_persona()
    assert persona.code == "LAWIM_AI"


def test_persona_display_name() -> None:
    persona = get_lawim_persona()
    assert persona.display_name == "LAWIM AI"


def test_persona_speaker_icon() -> None:
    persona = get_lawim_persona()
    assert persona.speaker_icon == "\U0001f916"


def test_persona_role_description_fr() -> None:
    persona = get_lawim_persona()
    desc = persona.role_description.get("fr", "")
    assert "LAWIM AI" in desc
    assert "projets immobiliers" in desc
    assert "Cameroun" in desc


def test_persona_role_description_en() -> None:
    persona = get_lawim_persona()
    desc = persona.role_description.get("en", "")
    assert "LAWIM AI" in desc
    assert "real estate" in desc
    assert "Cameroon" in desc


def test_persona_role_description_pcm() -> None:
    persona = get_lawim_persona()
    desc = persona.role_description.get("pcm", "")
    assert "LAWIM AI" in desc
    assert "property matter" in desc
    assert "Cameroon" in desc


def test_persona_has_all_languages() -> None:
    persona = get_lawim_persona()
    for lang in ("fr", "en", "pcm"):
        assert lang in persona.role_description


def test_persona_tone_list() -> None:
    persona = get_lawim_persona()
    assert "professionnel" in persona.tone
    assert "courtois" in persona.tone
    assert "direct" in persona.tone
    assert len(persona.tone) >= 5


def test_persona_limits() -> None:
    persona = get_lawim_persona()
    assert persona.maximum_questions == 1
    assert persona.maximum_sentences == 4
    assert persona.maximum_characters == 600


def test_persona_footer_policy() -> None:
    persona = get_lawim_persona()
    assert "\u2139\ufe0f" in persona.footer_policy["fr"]
    assert "LAWIM AI" in persona.footer_policy["fr"]
    assert "LAWIM AI" in persona.footer_policy["en"]
    assert "LAWIM AI" in persona.footer_policy["pcm"]


def test_persona_to_dict() -> None:
    persona = get_lawim_persona()
    d = persona.to_dict()
    assert d["code"] == "LAWIM_AI"
    assert d["display_name"] == "LAWIM AI"
    assert "fr" in d["role_description"]
    assert "en" in d["role_description"]
    assert "pcm" in d["role_description"]
    assert len(d["tone"]) >= 5
    assert d["maximum_questions"] == 1
    assert d["maximum_sentences"] == 4
    assert d["maximum_characters"] == 600
    assert "fr" in d["footer_policy"]


def test_custom_persona_override() -> None:
    persona = LawimConversationPersona(
        code="CUSTOM",
        display_name="Custom AI",
        role_description={"fr": "Custom role"},
    )
    assert persona.code == "CUSTOM"
    assert persona.display_name == "Custom AI"
    assert persona.role_description["fr"] == "Custom role"
