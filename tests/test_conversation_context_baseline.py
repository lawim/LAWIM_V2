from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from lawim_v2.communication.service import CommunicationService
from tests.lawim_harness import LawimTestHarness


def test_rental_search_context_is_retained_across_four_turns() -> None:
    repo = MagicMock()
    project_service = MagicMock()
    policy = MagicMock()
    config = MagicMock()
    ai_orchestrator = MagicMock()
    disclaimer = MagicMock()
    svc = CommunicationService(
        repository=repo,
        project_service=project_service,
        policy=policy,
        config=config,
        ai_orchestrator=ai_orchestrator,
        disclaimer_manager=disclaimer,
    )

    repo.one.return_value = None
    repo.create_communication_event.return_value = {"id": 1}
    repo.create_communication_message.return_value = {"id": 100, "body": "", "status": "delivered"}
    repo.create_communication_log.return_value = {"id": 1}

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
                "body": {"messageData": {"textMessageData": {"text": text}}},
                "senderData": {"chatId": "237691234567@c.us", "sender": "237691234567@c.us"},
            },
            headers={},
        )

    assert ai_orchestrator.build_request.call_count >= 4
    last_request_kwargs = {}
    for call in ai_orchestrator.build_request.call_args_list:
        last_request_kwargs = call.kwargs
    conversation_key = last_request_kwargs.get("conversation_key", "")
    assert conversation_key != "", "a conversation_key should be threaded through turns"


def test_short_response_is_contextualized() -> None:
    repo = MagicMock()
    svc = CommunicationService(
        repository=repo,
        project_service=MagicMock(),
        policy=MagicMock(),
        config=MagicMock(),
        ai_orchestrator=None,
        disclaimer_manager=MagicMock(),
    )
    repo.one.return_value = None
    repo.create_communication_event.return_value = {"id": 1}
    repo.create_communication_message.return_value = {"id": 100, "body": "", "status": "delivered"}
    repo.create_communication_log.return_value = {"id": 1}

    svc.process_green_api_webhook(
        payload={
            "typeWebhook": "incomingMessageReceived",
            "body": {"messageData": {"textMessageData": {"text": "Je cherche un appartement à Douala"}}},
            "senderData": {"chatId": "237691234567@c.us", "sender": "237691234567@c.us"},
        },
        headers={},
    )

    with patch.object(svc, "_generate_ai_reply", return_value="Quel budget mensuel avez-vous prévu ?"):
        svc.process_green_api_webhook(
            payload={
                "typeWebhook": "incomingMessageReceived",
                "body": {"messageData": {"textMessageData": {"text": "Quel budget mensuel avez-vous prévu ?"}}},
                "senderData": {"chatId": "237691234567@c.us", "sender": "237691234567@c.us"},
            },
            headers={},
        )

    reply = svc._generate_ai_reply("180 000 FCFA.", "whatsapp", "conv-1")
    assert "180000" in reply or "180 000" in reply
    assert "budget" in reply.lower()


def test_quartier_updates_existing_search() -> None:
    repo = MagicMock()
    svc = CommunicationService(
        repository=repo,
        project_service=MagicMock(),
        policy=MagicMock(),
        config=MagicMock(),
        ai_orchestrator=None,
        disclaimer_manager=MagicMock(),
    )
    repo.one.return_value = None
    repo.create_communication_event.return_value = {"id": 1}
    repo.create_communication_message.return_value = {"id": 100, "body": "", "status": "delivered"}
    repo.create_communication_log.return_value = {"id": 1}

    svc.process_green_api_webhook(
        payload={
            "typeWebhook": "incomingMessageReceived",
            "body": {"messageData": {"textMessageData": {"text": "Je cherche un appartement à Douala"}}},
            "senderData": {"chatId": "237691234567@c.us", "sender": "237691234567@c.us"},
        },
        headers={},
    )

    reply = svc._generate_ai_reply("Bonamoussadi.", "whatsapp", "conv-1")
    assert "bonamoussadi" in reply.lower()


def test_criterion_modification_replaces_old_value() -> None:
    repo = MagicMock()
    svc = CommunicationService(
        repository=repo,
        project_service=MagicMock(),
        policy=MagicMock(),
        config=MagicMock(),
        ai_orchestrator=None,
        disclaimer_manager=MagicMock(),
    )
    reply = svc._generate_ai_reply("Finalement, mon budget est de 220 000 FCFA", "whatsapp", "conv-1")
    assert "220000" in reply or "220" in reply


def test_no_criteria_are_reasked() -> None:
    ai_mock = MagicMock()
    ai_mock.build_request.return_value = MagicMock()
    ai_mock.generate.return_value = MagicMock(
        response=MagicMock(content="Quel type de bien cherchez-vous ? Et quel budget ? Et dans quel quartier ?")
    )
    repo = MagicMock()
    svc = CommunicationService(
        repository=repo,
        project_service=MagicMock(),
        policy=MagicMock(),
        config=MagicMock(),
        ai_orchestrator=ai_mock,
        disclaimer_manager=MagicMock(),
    )
    repo.create_communication_log.return_value = {"id": 1}
    reply = svc._generate_ai_reply("Je cherche un appartement et j'ai un budget", "whatsapp", "conv-1")
    question_marks = reply.count("?")
    assert question_marks <= 1, f"Expected at most 1 question mark, got {question_marks}"


def test_one_single_next_question() -> None:
    ai_mock = MagicMock()
    ai_mock.build_request.return_value = MagicMock()
    ai_mock.generate.return_value = MagicMock(
        response=MagicMock(content="Cherchez-vous un appartement, une maison ou un terrain ? Et dans quel budget ?")
    )
    repo = MagicMock()
    svc = CommunicationService(
        repository=repo,
        project_service=MagicMock(),
        policy=MagicMock(),
        config=MagicMock(),
        ai_orchestrator=ai_mock,
        disclaimer_manager=MagicMock(),
    )
    repo.create_communication_log.return_value = {"id": 1}
    reply = svc._generate_ai_reply("Je cherche un appartement", "whatsapp", "conv-1")
    question_count = reply.count("?")
    assert question_count <= 1, f"Expected at most 1 question, got {question_count}"


def test_conversation_id_is_unique_across_turns() -> None:
    repo = MagicMock()
    svc = CommunicationService(
        repository=repo,
        project_service=MagicMock(),
        policy=MagicMock(),
        config=MagicMock(),
        ai_orchestrator=MagicMock(),
        disclaimer_manager=MagicMock(),
    )
    repo.create_communication_event.return_value = {"id": 1}
    repo.create_communication_message.return_value = {"id": 100, "body": "", "status": "delivered"}
    repo.create_communication_log.return_value = {"id": 1}

    for text in ["Bonjour", "Je cherche un appartement"]:
        svc.process_green_api_webhook(
            payload={
                "typeWebhook": "incomingMessageReceived",
                "body": {"messageData": {"textMessageData": {"text": text}}},
                "senderData": {"chatId": "237691234567@c.us", "sender": "237691234567@c.us"},
            },
            headers={},
        )

    ids = []
    for call in repo.create_communication_event.call_args_list:
        ids.append(call.kwargs.get("event_key", ""))
    unique = set(ids)
    assert len(unique) >= 2, "Each turn should produce a unique event_key"
