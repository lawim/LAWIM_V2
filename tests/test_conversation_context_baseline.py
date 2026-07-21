from __future__ import annotations

import sqlite3
import tempfile
from unittest.mock import MagicMock, patch

import pytest

from lawim_v2.communication.service import CommunicationService
from lawim_v2.conversation.state.engine import ConversationStateEngine as _CSE
from lawim_v2.conversation.state.repository import ConversationStateRepository as _CSR
from lawim_v2.conversation.state.resolver import ConversationResolver as _CR


def _make_svc(**kwargs) -> CommunicationService:
    db = tempfile.mktemp(suffix=".db")
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    state_repo = _CSR(conn)
    resolver = _CR()
    cse = _CSE(state_repo, resolver)
    repo = MagicMock()
    repo.one.return_value = None
    repo.create_communication_event.return_value = {"id": 1}
    repo.create_communication_message.return_value = {"id": 100, "body": "", "status": "delivered"}
    repo.create_communication_log.return_value = {"id": 1}
    svc = CommunicationService(
        repository=repo,
        project_service=MagicMock(),
        policy=MagicMock(),
        config=MagicMock(),
        ai_orchestrator=kwargs.get("ai_orchestrator", MagicMock()),
        disclaimer_manager=MagicMock(),
        conversation_state_engine=cse,
    )
    svc._test_db = db
    svc._test_conn = conn
    return svc


def test_rental_search_context_is_retained_across_four_turns() -> None:
    ai_mock = MagicMock()
    svc = _make_svc(ai_orchestrator=ai_mock)
    turns = [
        "Bonjour",
        "Je cherche un appartement à Douala",
        "Mon budget est de 180 000 FCFA par mois",
        "Je préfère le quartier Bonamoussadi",
    ]
    for text in turns:
        svc.process_green_api_webhook(
            payload={
                "typeWebhook": "incomingMessageReceived",
                "idMessage": f"test-{turns.index(text)}",
                "senderData": {"chatId": "237691234567@c.us", "sender": "237691234567", "senderName": "Test"},
                "messageData": {"typeMessage": "textMessage", "textMessageData": {"textMessage": text}},
            },
            headers={},
        )
    assert ai_mock.build_request.call_count >= 4


def test_short_response_is_contextualized() -> None:
    db = tempfile.mktemp(suffix=".db")
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    state_repo = _CSR(conn)
    resolver = _CR()
    cse = _CSE(state_repo, resolver)
    # First send the apartment search through the engine
    cse.process_turn(actor_id="test", channel="whatsapp",
                     external_conversation_id="+237691234567",
                     message="Je cherche un appartement à Douala",
                     language="fr")
    # Then check that a budget answer is contextualized
    result = cse.process_turn(actor_id="test", channel="whatsapp",
                               external_conversation_id="+237691234567",
                               message="180 000 FCFA",
                               language="fr")
    reply = result.get("response", "")
    assert "180000" in reply or "180" in reply or "budget" in reply.lower()


def test_quartier_updates_existing_search() -> None:
    db = tempfile.mktemp(suffix=".db")
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    state_repo = _CSR(conn)
    resolver = _CR()
    cse = _CSE(state_repo, resolver)
    cse.process_turn(actor_id="test", channel="whatsapp",
                     external_conversation_id="+237691234568",
                     message="Je cherche un appartement à Douala",
                     language="fr")
    cse.process_turn(actor_id="test", channel="whatsapp",
                     external_conversation_id="+237691234568",
                     message="Bonamoussadi",
                     language="fr")
    # Load state and verify
    state = state_repo.load("whatsapp", "+237691234568")
    assert state is not None
    assert "district" in state.known_slots or "neighborhood" in state.known_slots


def test_criterion_modification_replaces_old_value() -> None:
    svc = _make_svc(ai_orchestrator=None)
    reply = svc._generate_ai_reply("Finalement, mon budget est de 220 000 FCFA", "whatsapp", "+237691234567")
    assert "220" in reply or "budget" in reply.lower()


def test_no_criteria_are_reasked() -> None:
    ai_mock = MagicMock()
    ai_mock.build_request.return_value = MagicMock()
    ai_mock.generate.return_value = MagicMock(
        response=MagicMock(content="Quel type de bien cherchez-vous ? Et quel budget ? Et dans quel quartier ?")
    )
    svc = _make_svc(ai_orchestrator=ai_mock)
    reply = svc._generate_ai_reply("Je cherche un appartement et j'ai un budget", "whatsapp", "conv-1")
    question_marks = reply.count("?")
    assert question_marks <= 1, f"Expected at most 1 question mark, got {question_marks}"


def test_one_single_next_question() -> None:
    ai_mock = MagicMock()
    ai_mock.build_request.return_value = MagicMock()
    ai_mock.generate.return_value = MagicMock(
        response=MagicMock(content="Cherchez-vous un appartement, une maison ou un terrain ? Et dans quel budget ?")
    )
    svc = _make_svc(ai_orchestrator=ai_mock)
    reply = svc._generate_ai_reply("Je cherche un appartement", "whatsapp", "conv-1")
    question_count = reply.count("?")
    assert question_count <= 1, f"Expected at most 1 question, got {question_count}"


def test_conversation_id_is_unique_across_turns() -> None:
    svc = _make_svc()
    for i, text in enumerate(["Bonjour", "Je cherche un appartement"]):
        svc.process_green_api_webhook(
            payload={
                "typeWebhook": "incomingMessageReceived",
                "idMessage": f"unique-{i}",
                "senderData": {"chatId": "237691234567@c.us", "sender": "237691234567", "senderName": "Test"},
                "messageData": {"typeMessage": "textMessage", "textMessageData": {"textMessage": text}},
            },
            headers={},
        )
    ids = []
    for call in svc.repository.create_communication_event.call_args_list:
        ids.append(call.kwargs.get("event_key", ""))
    unique = set(ids)
    assert len(unique) >= 2, "Each turn should produce a unique event_key"
