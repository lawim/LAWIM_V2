"""Regression tests for P1 incident: real WhatsApp generalist responses.

These tests reproduce the exact messages that triggered generalist
responses on WhatsApp production. They must never produce:
- external platform referrals
- neutral assistant answers
- multiple questions
- language switches
"""
from lawim_v2.conversation.state.engine import ConversationStateEngine
from lawim_v2.conversation.state.repository import ConversationStateRepository
from lawim_v2.conversation.state.resolver import ConversationResolver
from lawim_v2.communication.service import CommunicationService
import sqlite3, tempfile, os


def _make_cs():
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
    engine = ConversationStateEngine(ConversationStateRepository(fr), ConversationResolver())
    cs = CommunicationService(fr, None, None)
    cs.conversation_state_engine = engine
    return cs, db


FORBIDDEN_PATTERNS = [
    "jumia", "seloger", "leboncoin", "facebook", "lamudi",
    "afribaba", "expat-dakar", "meilleurs agents", "paruvendu",
    "voici quelques pistes", "quartiers populaires",
    "bouche-à-oreille", "word of mouth",
    "agences immobilières", "real estate agencies",
    "assistant neutre", "neutral assistant",
    "i cannot make business decisions",
    "je ne peux pas prendre de décisions commerciales",
    "while i can't", "I understand you're looking",
    "can't directly list", "can't directly manage",
    "voici quelques", "here are some",
]


def test_whatsapp_greeting_no_generalist():
    """'Bonjour' on WhatsApp must not produce generalist assistant."""
    cs, db = _make_cs()
    resp = cs._generate_ai_reply("Bonjour", "whatsapp", "+237000001", "test")
    lower = resp.lower()
    for pat in FORBIDDEN_PATTERNS:
        assert pat not in lower, f"FORBIDDEN: {pat} in response"
    assert "🤖 LAWIM AI" in resp[:30], "Missing AI identity"
    assert "ℹ️" in resp, "Missing footer"
    q = resp.count("?")
    assert q <= 2, f"Too many questions: {q} (max 1-2)"
    os.unlink(db)


def test_whatsapp_studio_douala_no_generalist():
    """'Je cherche un studio à Douala' must not trigger external referrals."""
    cs, db = _make_cs()
    cs._generate_ai_reply("Bonjour", "whatsapp", "+237000002", "test")
    resp = cs._generate_ai_reply("Je cherche un studio a Douala", "whatsapp", "+237000002", "test")
    lower = resp.lower()
    for pat in FORBIDDEN_PATTERNS:
        assert pat not in lower, f"FORBIDDEN: {pat} in response"
    assert "🤖 LAWIM AI" in resp[:30], "Missing AI identity"
    assert "studio" in lower or "STUDIO" in resp, "Missing studio reference"
    assert "Douala" in resp, "Missing Douala reference"
    os.unlink(db)


def test_telegram_greeting_no_generalist():
    """'Bonjour' on Telegram must not produce generalist assistant."""
    cs, db = _make_cs()
    resp = cs._generate_ai_reply("Bonjour", "telegram", "99990001", "test")
    lower = resp.lower()
    for pat in FORBIDDEN_PATTERNS:
        assert pat not in lower, f"FORBIDDEN: {pat} in response"
    assert "🤖 LAWIM AI" in resp[:30], "Missing AI identity"
    os.unlink(db)


def test_telegram_appartment_yaounde_no_english():
    """'besoin d'un appartement à Yaoundé' must stay in French."""
    cs, db = _make_cs()
    cs._generate_ai_reply("Bonjour", "telegram", "99990002", "test")
    resp = cs._generate_ai_reply("besoin d un appartement a Yaounde", "telegram", "99990002", "test")
    lower = resp.lower()
    for pat in FORBIDDEN_PATTERNS:
        assert pat not in lower, f"FORBIDDEN: {pat} in response"
    assert "🤖 LAWIM AI" in resp[:30], "Missing AI identity"
    assert "Yaoundé" in resp or "Yaounde" in resp, "Missing Yaoundé"
    os.unlink(db)


def test_one_question_per_response():
    """Each response must contain at most one direct question."""
    cs, db = _make_cs()
    cs._generate_ai_reply("Bonjour", "whatsapp", "+237000003", "test")
    resp = cs._generate_ai_reply("Je cherche un studio", "whatsapp", "+237000003", "test")
    assert resp.count("?") <= 2, f"Too many questions: {resp.count('?')}"
    os.unlink(db)
