from __future__ import annotations

import sqlite3
import tempfile
from unittest.mock import MagicMock

import pytest

from lawim_v2.communication.service import CommunicationService
from lawim_v2.conversation.state.engine import ConversationStateEngine as _CSE
from lawim_v2.conversation.state.repository import ConversationStateRepository as _CSR
from lawim_v2.conversation.state.resolver import ConversationResolver as _CR


@pytest.fixture
def svc() -> CommunicationService:
    repo = MagicMock()
    repo.one.return_value = None
    repo.create_communication_event.return_value = {"id": 1}
    repo.create_communication_message.return_value = {"id": 100, "body": "", "status": "delivered"}
    repo.create_communication_log.return_value = {"id": 1}
    db = tempfile.mktemp(suffix=".db")
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    state_repo = _CSR(conn)
    resolver = _CR()
    cse = _CSE(state_repo, resolver)
    return CommunicationService(
        repository=repo,
        project_service=MagicMock(),
        policy=MagicMock(),
        config=MagicMock(),
        ai_orchestrator=None,
        disclaimer_manager=MagicMock(),
        conversation_state_engine=cse,
    )


def test_bonjour_routes_to_greeting_not_handover(svc: CommunicationService) -> None:
    reply = svc._generate_ai_reply("Bonjour", "whatsapp", "conv-1")
    assert "bienvenue" in reply.lower() or "welcome" in reply.lower()
    assert "parler à une personne" not in reply.lower()
    assert "conseiller" not in reply.lower()


def test_apartment_search_routes_to_qualification(svc: CommunicationService) -> None:
    reply = svc._generate_ai_reply("Je cherche un appartement à Douala", "whatsapp", "conv-1")
    assert reply != ""
    assert "parler à une personne" not in reply.lower()


def test_budget_response_is_continuation(svc: CommunicationService) -> None:
    reply = svc._generate_ai_reply("Mon budget est de 180 000 FCFA", "whatsapp", "conv-1")
    assert reply != ""
    assert "parler à une personne" not in reply.lower()


def test_district_response_is_continuation(svc: CommunicationService) -> None:
    reply = svc._generate_ai_reply("Je préfère Bonamoussadi", "whatsapp", "conv-1")
    assert reply != ""
    assert "?parler" not in reply.lower()


def test_human_handover_triggers(svc: CommunicationService) -> None:
    reply = svc._generate_ai_reply("Je veux parler à une personne", "whatsapp", "conv-1")
    assert "parler" in reply.lower() or "conseiller" in reply.lower()


def test_bonjour_does_not_route_to_support(svc: CommunicationService) -> None:
    reply = svc._generate_ai_reply("Bonjour", "whatsapp", "conv-1")
    assert "assistance" not in reply.lower()
    assert "support" not in reply.lower()
    assert "help" not in reply.lower() and "aide" not in reply.lower()
