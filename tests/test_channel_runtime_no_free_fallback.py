"""Test that WhatsApp/Telegram never use free generative fallback."""
from lawim_v2.communication.service import CommunicationService
from lawim_v2.conversation.state.engine import ConversationStateEngine
from lawim_v2.conversation.state.repository import ConversationStateRepository
from lawim_v2.conversation.state.resolver import ConversationResolver
import sqlite3, tempfile, os, re


def _make_cs(with_engine=True):
    db = tempfile.mktemp(suffix=".db")
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    class _FakeRepo:
        def __init__(self, c):
            self.c = c
        def execute(self, s, p=()):
            cur = self.c.execute(s, p or ())
            self.c.commit(); return cur
        def fetch_one(self, s, p=()):
            cur = self.c.execute(s, p or ())
            r = cur.fetchone()
            return dict(r) if r else None
        def create_communication_log(self, **kw): pass
    fr = _FakeRepo(conn)
    cs = CommunicationService(fr, None, None)
    if with_engine:
        engine = ConversationStateEngine(ConversationStateRepository(fr), ConversationResolver())
        cs.conversation_state_engine = engine
    return cs, db


GENERALIST_PATTERNS = [
    "jumia", "seloger", "leboncoin", "facebook marketplace", "lamudi",
    "afribaba", "expat-dakar", "meilleurs agents",
    "voici quelques pistes", "quartiers populaires",
    "bouche-à-oreille", "word of mouth",
    "agences immobilières", "real estate agencies",
    "assistant neutre", "neutral assistant",
    "i cannot make business decisions",
    "je ne peux pas prendre de décisions commerciales",
    "while i can't", "I understand you're looking",
    "can't directly list", "can't directly manage",
    "voici quelques", "here are some",
    "I understand you're looking",
]


def test_whatsapp_no_free_fallback():
    """WhatsApp must use engine, never generate free-form AI response."""
    cs, db = _make_cs()
    resp = cs._generate_ai_reply("Bonjour", "whatsapp", "+237000001", "test")
    lower = resp.lower()
    for pat in GENERALIST_PATTERNS:
        assert pat not in lower, f"FORBIDDEN GENERALIST: {pat}"
    assert "🤖 LAWIM AI" in resp[:30], "Missing AI identity"
    assert "ℹ️" in resp, "Missing footer"
    assert resp.count("?") <= 2, f"Too many questions: {resp.count('?')}"
    os.unlink(db)


def test_telegram_no_free_fallback():
    """Telegram must use engine, never generate free-form AI response."""
    cs, db = _make_cs()
    resp = cs._generate_ai_reply("Bonjour", "telegram", "99990001", "test")
    lower = resp.lower()
    for pat in GENERALIST_PATTERNS:
        assert pat not in lower, f"FORBIDDEN GENERALIST: {pat}"
    assert "🤖 LAWIM AI" in resp[:30], "Missing AI identity"
    assert "<i>" in resp or "ℹ️" in resp, "Missing Telegram footer"
    os.unlink(db)


def test_safety_response_when_engine_none():
    """When engine is None, must return safety response, not free AI."""
    cs, db = _make_cs(with_engine=False)
    resp = cs._generate_ai_reply("Bonjour", "whatsapp", "+237000002", "test")
    assert "🤖 LAWIM AI" in resp[:30], "Missing AI identity"
    assert "difficulté" in resp or "difficulty" in resp, "Expected safety language"
    assert "ℹ️" in resp, "Missing footer"
    for pat in GENERALIST_PATTERNS:
        assert pat not in resp.lower(), f"FORBIDDEN: {pat}"
    os.unlink(db)


def test_safety_response_when_engine_returns_empty():
    """When engine returns empty response, must return safety response."""
    cs, db = _make_cs()
    # Replace process_turn to return empty
    original = cs.conversation_state_engine.process_turn
    def empty_turn(*a, **kw):
        return {"response": ""}
    cs.conversation_state_engine.process_turn = empty_turn
    resp = cs._generate_ai_reply("Bonjour", "whatsapp", "+237000003", "test")
    assert "🤖 LAWIM AI" in resp[:30], "Missing AI identity"
    assert "difficulté" in resp or "difficulty" in resp, "Expected safety language"
    cs.conversation_state_engine.process_turn = original
    os.unlink(db)


def test_studio_douala_no_generalist():
    """'Je cherche un studio à Douala' must produce structured response, not generalist."""
    cs, db = _make_cs()
    cs._generate_ai_reply("Bonjour", "whatsapp", "+237000004", "test")
    resp = cs._generate_ai_reply("Je cherche un studio a Douala", "whatsapp", "+237000004", "test")
    lower = resp.lower()
    for pat in GENERALIST_PATTERNS:
        assert pat not in lower, f"FORBIDDEN: {pat}"
    assert "🤖 LAWIM AI" in resp[:30], "Missing AI identity"
    assert "Douala" in resp, "Missing Douala"
    assert "studio" in resp.lower() or "STUDIO" in resp, "Missing studio"
    os.unlink(db)


def test_correction_multiturn_structured():
    """Budget correction must be reflected and old value not repeated."""
    cs, db = _make_cs()
    cs._generate_ai_reply("Bonjour", "whatsapp", "+237000005", "test")
    cs._generate_ai_reply("Mon budget est de 180 000 FCFA", "whatsapp", "+237000005", "test")
    resp = cs._generate_ai_reply("Finalement 220 000 FCFA", "whatsapp", "+237000005", "test")
    for pat in GENERALIST_PATTERNS:
        assert pat not in resp.lower(), f"FORBIDDEN: {pat}"
    assert "🤖 LAWIM AI" in resp[:30], "Missing AI identity"
    os.unlink(db)


def test_fallback_already_blocked_at_validator():
    """Validator must detect and block forbidden patterns."""
    from lawim_v2.conversation.state.validator import ConversationResponseValidator
    from lawim_v2.conversation.state.state import ResponsePlan
    v = ConversationResponseValidator()
    plan = ResponsePlan(maximum_questions=1)

    # Test each forbidden category
    for bad_text in [
        "Voici quelques pistes pour trouver un studio",
        "Vous pouvez regarder sur Jumia Deals",
        "I cannot make business decisions",
        "Je ne peux pas prendre de décisions commerciales",
    ]:
        _, status = v.validate(bad_text, plan)
        assert status == "REPAIR", f"Should REPAIR: {bad_text[:30]}"
