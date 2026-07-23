from __future__ import annotations

import sqlite3
import tempfile

import pytest

from lawim_v2.conversation.state.engine import ConversationStateEngine as _CSE
from lawim_v2.conversation.state.repository import ConversationStateRepository as _CSR
from lawim_v2.conversation.state.resolver import ConversationResolver as _CR


@pytest.fixture
def engine():
    db = tempfile.mktemp(suffix=".db")
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    state_repo = _CSR(conn)
    resolver = _CR()
    cse = _CSE(state_repo, resolver)
    return cse, state_repo


GREETINGS = ["Bonjour", "Bonsoir", "Salut", "Hello"]

HANDOVER_MARKERS = [
    "parler à une personne",
    "Je veux parler à un conseiller",
    "humain",
    "assistance",
]


def test_all_greetings_return_welcome(engine):
    cse, _ = engine
    for greeting in GREETINGS:
        result = cse.process_turn(
            actor_id="test", channel="whatsapp",
            external_conversation_id="+237600000",
            message=greeting, language="fr",
        )
        reply = result.get("response", "")
        assert "bienvenue" in reply.lower() or "welcome" in reply.lower(), \
            f"greeting '{greeting}' should contain welcome, got: {reply[:100]}"


def test_greetings_do_not_trigger_handover(engine):
    cse, _ = engine
    for greeting in GREETINGS:
        result = cse.process_turn(
            actor_id="test", channel="whatsapp",
            external_conversation_id="+237600001",
            message=greeting, language="fr",
        )
        reply = result.get("response", "")
        assert "handover" not in result, \
            f"greeting '{greeting}' should not produce handover"
        assert "parler à" not in reply.lower(), \
            f"greeting '{greeting}' should not produce handover text"


def test_greeting_followed_by_real_estate_request(engine):
    cse, state_repo = engine
    cse.process_turn(
        actor_id="test", channel="whatsapp",
        external_conversation_id="+237600002",
        message="Bonjour", language="fr",
    )
    result = cse.process_turn(
        actor_id="test", channel="whatsapp",
        external_conversation_id="+237600002",
        message="Je cherche un appartement à Douala", language="fr",
    )
    reply = result.get("response", "")
    assert reply != "", "response should not be empty"
    state = state_repo.load("whatsapp", "+237600002")
    assert state is not None, "state should exist after two turns"
    assert "handover" not in result, "real estate request after greeting should not trigger handover"


def test_rental_search_retains_structured_context(engine):
    cse, state_repo = engine
    turns = [
        ("Bonjour", {}),
        ("Je cherche un studio à Makepe", {"city": "Douala", "neighborhood": "Makepe"}),
        ("80 000 FCFA par mois", {"budget_max": "80000"}),
        ("Je suis disponible samedi", {}),
    ]
    for text, _ in turns:
        cse.process_turn(
            actor_id="test", channel="whatsapp",
            external_conversation_id="+237600003",
            message=text, language="fr",
        )
    state = state_repo.load("whatsapp", "+237600003")
    assert state is not None, "state must exist"
    known = state.known_slots if hasattr(state, "known_slots") else {}
    assert "city" in known or "neighborhood" in known, \
        f"city or neighborhood should be in known_slots: {known}"
    assert "budget_max" in known or "budget" in known or "budget_xaf" in known, \
        f"budget should be in known_slots: {known}"


def test_handover_only_when_justified(engine):
    cse, _ = engine
    for marker in HANDOVER_MARKERS:
        result = cse.process_turn(
            actor_id="test", channel="whatsapp",
            external_conversation_id="+237600004",
            message=marker, language="fr",
        )
        reply = result.get("response", "")
        assert "parler" in reply.lower() or "conseiller" in reply.lower() or "assistance" in reply.lower(), \
            f"handover marker '{marker}' should produce handover response"


def test_bonjour_not_routed_to_support(engine):
    cse, _ = engine
    result = cse.process_turn(
        actor_id="test", channel="whatsapp",
        external_conversation_id="+237600005",
        message="Bonjour", language="fr",
    )
    reply = result.get("response", "")
    assert "assistance" not in reply.lower()
    assert "support" not in reply.lower()
    assert "help" not in reply.lower() and "aide" not in reply.lower()
