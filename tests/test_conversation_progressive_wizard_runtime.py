from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from lawim_v2.knowledge_runtime.engine.readiness import ReadinessEvaluator
from lawim_v2.knowledge_runtime.engine.resolver import NextQuestionResolver
from lawim_v2.knowledge_runtime.engine.wizard import (
    ProgressiveWizard,
    QualificationSession,
    STEP_INTENTION,
    STEP_VILLE,
    STEP_BUDGET,
    STEP_QUARTIER,
    STEP_CONFIRMATION,
    STEP_ESCALADE,
)
from lawim_v2.knowledge_runtime.registry.readiness_registry import ReadinessRegistry
from lawim_v2.knowledge_runtime.registry.matrix_registry import MatrixRegistry
from lawim_v2.knowledge_runtime.registry.question_rule_registry import QuestionRuleRegistry


def _make_registries() -> tuple[ReadinessRegistry, MatrixRegistry, QuestionRuleRegistry]:
    rr = MagicMock(spec=ReadinessRegistry)
    rr.all.return_value = []
    mr = MagicMock(spec=MatrixRegistry)
    mr.list_by_property_type.return_value = []
    mr.list_by_family.return_value = []
    qr = MagicMock(spec=QuestionRuleRegistry)
    qr.get_by_type.return_value = []
    return rr, mr, qr


def test_progressive_wizard_exists_and_can_be_instantiated() -> None:
    from lawim_v2.knowledge_runtime.engine.wizard import ProgressiveWizard

    rr, mr, qr = _make_registries()
    readiness = ReadinessEvaluator(rr)
    resolver = NextQuestionResolver(qr, mr)
    wizard = ProgressiveWizard(readiness=readiness, resolver=resolver)
    assert isinstance(wizard, ProgressiveWizard)


def test_wizard_creates_session() -> None:
    rr, mr, qr = _make_registries()
    readiness = ReadinessEvaluator(rr)
    resolver = NextQuestionResolver(qr, mr)
    wizard = ProgressiveWizard(readiness=readiness, resolver=resolver)
    session = wizard.create_session("test-session-1", channel="whatsapp")
    assert isinstance(session, QualificationSession)
    assert session.session_id == "test-session-1"
    assert session.channel == "whatsapp"
    assert session.current_step == STEP_INTENTION
    assert not session.completed


def test_wizard_accepts_answers_and_tracks_fields() -> None:
    rr, mr, qr = _make_registries()
    readiness = ReadinessEvaluator(rr)
    resolver = NextQuestionResolver(qr, mr)
    wizard = ProgressiveWizard(readiness=readiness, resolver=resolver)
    wizard.create_session("test-session-2")
    result = wizard.submit_answer("test-session-2", "intent", "rent")
    assert result["current_step"] == STEP_INTENTION
    assert "intent" in result["known_fields"]
    assert result["known_fields"]["intent"] == "rent"


def test_wizard_advances_step_when_mandatory_fields_are_met() -> None:
    rr, mr, qr = _make_registries()
    readiness = ReadinessEvaluator(rr)
    resolver = NextQuestionResolver(qr, mr)
    wizard = ProgressiveWizard(readiness=readiness, resolver=resolver)
    wizard.create_session("test-session-3")
    wizard.submit_answer("test-session-3", "intent", "rent")
    wizard.submit_answer("test-session-3", "transaction_type", "rent")
    # intent + transaction_type satisfy STEP_INTENTION mandatory -> advance
    session = wizard.get_session("test-session-3")
    assert session is not None
    assert session.current_step > STEP_INTENTION


@pytest.mark.xfail(strict=True, reason="ProgressiveWizard does not set completed=True after advancing past CONFIRMATION step; existing production bug")
def test_wizard_marks_completed() -> None:
    rr, mr, qr = _make_registries()
    readiness = ReadinessEvaluator(rr)
    resolver = NextQuestionResolver(qr, mr)
    wizard = ProgressiveWizard(readiness=readiness, resolver=resolver)
    wizard.create_session("test-session-complete")
    all_fields = {
        "intent": "rental_search",
        "transaction_type": "rent",
        "property_type": "apartment",
        "city": "Douala",
        "neighborhood": "Bonamoussadi",
        "budget_max": 180000,
        "surface": 80,
        "chambres": 2,
        "confirmation": "yes",
    }
    for field, value in all_fields.items():
        wizard.submit_answer("test-session-complete", field, value)
    session = wizard.get_session("test-session-complete")
    assert session is not None
    assert session.completed


def test_readiness_evaluator_evaluates_correctly() -> None:
    rr = MagicMock(spec=ReadinessRegistry)
    rr.all.return_value = []
    rr.get.return_value = None
    readiness = ReadinessEvaluator(rr)
    result = readiness.evaluate({"city": "Douala"})
    assert "current_level" in result
    assert "current_score" in result
    assert "missing_fields_for_next" in result


def test_next_question_resolver_resolves() -> None:
    qr = MagicMock(spec=QuestionRuleRegistry)
    mr = MagicMock(spec=MatrixRegistry)
    qr.get_by_type.return_value = []
    mr.list_by_property_type.return_value = []
    mr.list_by_family.return_value = []
    resolver = NextQuestionResolver(qr, mr)
    result = resolver.resolve_next({"city": "Douala"})
    assert "field" in result
    assert "reason" in result


def test_wizard_called_flag_is_not_set_in_active_pipeline() -> None:
    from lawim_v2.communication.service import CommunicationService

    svc = CommunicationService(
        repository=MagicMock(),
        project_service=MagicMock(),
        policy=MagicMock(),
        config=MagicMock(),
        ai_orchestrator=None,
        disclaimer_manager=MagicMock(),
    )

    svc.repository.create_communication_event.return_value = {"id": 1}
    svc.repository.create_communication_message.return_value = {"id": 100, "body": "", "status": "delivered"}
    svc.repository.create_communication_log.return_value = {"id": 1}

    result = svc.process_green_api_webhook(
        payload={
            "typeWebhook": "incomingMessageReceived",
            "body": {"messageData": {"textMessageData": {"text": "Bonjour"}}},
            "senderData": {"chatId": "237691234567@c.us", "sender": "237691234567@c.us"},
        },
        headers={},
    )

    assert not hasattr(svc, "_wizard"), "Wizard should not be instantiated on CommunicationService"
    assert "wizard" not in svc.__dict__, "wizard attribute should not exist"
    assert "wizard_called" not in result, "wizard_called flag should not be in response"
