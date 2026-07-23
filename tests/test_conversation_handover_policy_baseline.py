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


def test_greeting_does_not_trigger_handover(svc: CommunicationService) -> None:
    for greeting in ("Bonjour", "Salut", "Hello", "Bonsoir"):
        reply = svc._generate_ai_reply(greeting, "whatsapp", "conv-1")
        assert "bienvenue" in reply.lower() or "welcome" in reply.lower()
        assert "parler à" not in reply.lower()


def test_ordinary_search_does_not_trigger_handover(svc: CommunicationService) -> None:
    reply = svc._generate_ai_reply("Je cherche une maison à vendre à Douala", "whatsapp", "conv-1")
    assert reply != ""
    assert "transféré" not in reply.lower()
    assert "redirigé" not in reply.lower()


def test_handover_request_triggers_handover(svc: CommunicationService) -> None:
    reply = svc._generate_ai_reply("Je veux parler à une personne", "whatsapp", "conv-1")
    assert "parler" in reply.lower() or "conseiller" in reply.lower() or "assistance" in reply.lower()


def test_handover_requires_id_reason_target(svc: CommunicationService) -> None:
    from lawim_v2.conversation.domain.states import ConversationState

    message = MagicMock()
    message.normalized_text = "Je veux parler à une personne"
    message.is_handover_request.return_value = True
    message.channel = "whatsapp"
    message.channel_message_id = "msg-1"
    message.metadata = {}

    from lawim_v2.conversation.service import ConversationService as DomainConversationService

    repo = MagicMock()
    domain_svc = DomainConversationService(repository=repo, memory_repo=MagicMock(), config=MagicMock())
    domain_svc._resolve_conversation = MagicMock(return_value=MagicMock())
    domain_svc._ensure_channel_continuity = MagicMock()
    domain_svc._load_active_projects = MagicMock(return_value=[])
    domain_svc._load_active_dossiers = MagicMock(return_value=[])
    domain_svc._load_known_facts = MagicMock(return_value={})
    domain_svc._build_intent_candidates = MagicMock(
        return_value=[{"intent": "HANDOVER", "confidence": 1.0, "source": "detected"}]
    )
    domain_svc._persist_message_facts = MagicMock()
    domain_svc._evaluate_readiness = MagicMock()
    domain_svc._persist_conversation = MagicMock()
    domain_svc._persist_decision = MagicMock()
    domain_svc._record_metrics = MagicMock()
    domain_svc._log_shadow_decision = MagicMock()
    domain_svc._build_actions_from_decision = MagicMock(return_value=[])
    domain_svc._audit = MagicMock()

    decision = domain_svc.process_message(message)
    assert decision["decision"].requires_human
    assert decision["decision"].action_parameters.get("handover_id") is not None
    assert decision["decision"].action_parameters.get("reason") is not None
    assert decision["decision"].action_parameters.get("target_team") is not None


def test_ambiguous_responses_lead_to_clarification_not_handover(svc: CommunicationService) -> None:
    reply = svc._generate_ai_reply("Je ne sais pas", "whatsapp", "conv-1")
    assert "parler à" not in reply.lower()
    assert "transféré" not in reply.lower()
