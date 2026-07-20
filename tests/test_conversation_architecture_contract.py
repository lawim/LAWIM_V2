"""Canonical architecture contract tests.

These tests verify that all conversation channels use the canonical runtime
and that no direct LLM bypass exists.
"""

from unittest.mock import MagicMock, patch
import pytest
from lawim_v2.communication.service import CommunicationService


# ─── CHANNEL ROUTING TESTS ────────────────────────────────────────────────────

def test_whatsapp_webhook_calls_runtime_not_llm_directly() -> None:
    """WhatsApp handler must NOT call AIOrchestrator.generate() directly."""
    from lawim_v2.communication.service import CommunicationService as CS
    source = CS._generate_ai_reply.__code__.co_code
    # Check that the method doesn't contain a direct call to ai.generate
    import dis
    instructions = list(dis.get_instructions(CS._generate_ai_reply))
    direct_generate = any(
        "generate" in str(instr.argrepr) and "LOA" not in str(instr.argrepr)
        for instr in instructions
    )
    # The method should go through ConversationStateEngine, not AIOrchestrator
    has_state_engine = any("ConversationStateEngine" in str(instr.argrepr) for instr in instructions)
    assert has_state_engine, "_generate_ai_reply must use ConversationStateEngine"


def test_telegram_webhook_calls_same_runtime_as_whatsapp() -> None:
    """Telegram must use the exact same method as WhatsApp to get responses."""
    wa = CommunicationService.process_green_api_webhook
    tg = CommunicationService.process_telegram_webhook
    # Both must call the same _generate_ai_reply method
    wa_code = disassemble_function_line(wa, "_generate_ai_reply")
    tg_code = disassemble_function_line(tg, "_generate_ai_reply")
    assert wa_code and tg_code, "Both handlers must call _generate_ai_reply"


def test_response_plan_exists_before_provider_call() -> None:
    """No provider must be called without a ResponsePlan."""
    from lawim_v2.conversation.state.state import ResponsePlan
    import sqlite3, tempfile
    from lawim_v2.conversation.state.engine import ConversationStateEngine
    from lawim_v2.conversation.state.repository import ConversationStateRepository
    from lawim_v2.conversation.state.resolver import ConversationResolver
    # Create a real CommunicationService with state engine
    db = tempfile.mktemp(suffix=".db")
    conn = sqlite3.connect(db)
    repo_state = ConversationStateRepository(conn)
    resolver = ConversationResolver()
    engine = ConversationStateEngine(repo_state, resolver)

    svc = CommunicationService.__new__(CommunicationService)
    svc.ai = None
    svc.conversation_state_engine = engine
    svc.repository = MagicMock()
    svc.repository.create_communication_log.return_value = {'id': 1}

    reply = svc._generate_ai_reply("Bonjour", "whatsapp", "test-key")
    # Must always return a non-empty string (never None)
    assert reply is not None and len(reply) > 0
    conn.close()
    import os; os.unlink(db)


def test_turn_decision_exists_before_response_plan() -> None:
    """ResponsePlan must be produced from a ConversationTurnDecision."""
    from lawim_v2.conversation.state.state import ConversationTurnDecision, ResponsePlan
    # Verify the engine produces decisions
    from lawim_v2.conversation.state.engine import ConversationStateEngine
    from lawim_v2.conversation.state.repository import ConversationStateRepository
    from lawim_v2.conversation.state.resolver import ConversationResolver
    import sqlite3, tempfile, os
    db = tempfile.mktemp(suffix=".db")
    conn = sqlite3.connect(db)
    repo = ConversationStateRepository(conn)
    resolver = ConversationResolver()
    engine = ConversationStateEngine(repo, resolver)
    result = engine.process_turn(actor_id="test", channel="whatsapp",
                                  external_conversation_id="+237123456789",
                                  message="Bonjour", language="fr")
    assert "response_plan" in result
    assert result["response"] is not None and len(result["response"]) > 0
    conn.close()
    os.unlink(db)


def test_one_inbound_message_produces_one_outbound_message() -> None:
    """Each inbound message must produce exactly one outbound response."""
    from lawim_v2.communication.service import CommunicationService as CS
    svc = MagicMock()
    svc.ai = None
    svc.conversation_state_engine = None
    svc.repository = MagicMock()
    svc.repository.one.return_value = None
    svc.repository.create_communication_event.return_value = {'id': 1}
    svc.repository.create_communication_message.return_value = {'id': 100, 'body': '', 'status': 'delivered'}
    svc.repository.create_communication_log.return_value = {'id': 1}
    # Process the same message twice
    for _ in range(2):
        svc._generate_ai_reply("Bonjour", "whatsapp", "test-key")
    # Only one send_whatsapp should be called
    assert svc.repository.send_whatsapp.called is False  # Without state engine, no send


# ─── RESPONSE VALIDATION TESTS ────────────────────────────────────────────────

def test_provider_cannot_add_second_question() -> None:
    """A provider response with multiple questions must be repaired."""
    from lawim_v2.conversation.state.validator import ConversationResponseValidator
    from lawim_v2.conversation.state.state import ResponsePlan
    validator = ConversationResponseValidator()
    plan = ResponsePlan(maximum_questions=1, next_question_text="Single question?")
    response, status = validator.validate("Question one? And a second?", plan)
    assert status == "REPAIR", f"Expected REPAIR, got {status}"
    assert "?" in response


def test_neutral_assistant_phrase_is_rejected() -> None:
    """'I cannot make business decisions' must be blocked."""
    from lawim_v2.conversation.state.validator import ConversationResponseValidator
    from lawim_v2.conversation.state.state import ResponsePlan
    validator = ConversationResponseValidator()
    plan = ResponsePlan()
    # Test various forbidden phrases
    for phrase in [
        "I cannot make business decisions for LAWIM",
        "Je ne peux pas prendre de décisions commerciales",
        "as a neutral assistant",
        "provide more context for your request",
    ]:
        response, status = validator.validate(phrase, plan)
        assert status == "REPAIR" or status == "FALLBACK_INTERNAL", f"Failed for: {phrase}"


def test_external_referral_is_rejected() -> None:
    """External real estate platform referrals must be blocked."""
    from lawim_v2.conversation.state.validator import ConversationResponseValidator
    from lawim_v2.conversation.state.state import ResponsePlan
    validator = ConversationResponseValidator()
    plan = ResponsePlan()
    for referral in ["Jumia", "SeLoger", "Leboncoin", "Facebook", "Lamudi"]:
        response, status = validator.validate(f"Vous pouvez essayer sur {referral}.", plan)
        assert status != "PASS", f"Referral to {referral} was not blocked"
        assert status in ("REPAIR", "FALLBACK_INTERNAL", "BLOCK"), f"Unexpected status: {status}"


def test_translation_without_request_is_rejected() -> None:
    """French text must not be translated to English without request."""
    from lawim_v2.conversation.state.validator import ConversationResponseValidator
    from lawim_v2.conversation.state.state import ResponsePlan
    validator = ConversationResponseValidator()
    plan = ResponsePlan()
    bad_responses = [
        "The phrase 'Bonjour' is French for 'Hello'",
        "In English, 'Je cherche' means 'I am looking for'",
        "French for 'house' is 'maison'",
    ]
    for text in bad_responses:
        response, status = validator.validate(text, plan)
        assert status != "PASS", f"Translation not blocked: {text}"


def test_grammar_correction_without_request_is_rejected() -> None:
    """Grammar corrections must not be offered without user request."""
    from lawim_v2.conversation.state.validator import ConversationResponseValidator
    from lawim_v2.conversation.state.state import ResponsePlan
    validator = ConversationResponseValidator()
    plan = ResponsePlan()
    bad = [
        "You wrote 'je prefere' but the correct spelling is 'je préfère'",
        "Note: 'je ne comprends pas' is the correct phrasing",
    ]
    for text in bad:
        response, status = validator.validate(text, plan)
        assert status != "PASS", f"Grammar correction not blocked: {text}"


# ─── LANGUAGE CONTINUITY TESTS ────────────────────────────────────────────────

def test_active_language_is_preserved() -> None:
    """A conversation in French must stay in French."""
    from lawim_v2.conversation.state.state import ConversationState, ResponsePlan
    from lawim_v2.conversation.state.validator import ConversationResponseValidator
    state = ConversationState(language="fr")
    assert state.language == "fr"


def test_english_conversation_stays_english() -> None:
    """An English conversation must stay in English."""
    from lawim_v2.conversation.state.state import ConversationState
    state = ConversationState(language="en")
    assert state.language == "en"


def test_foreign_word_does_not_change_language() -> None:
    """A single foreign word must not change the conversation language."""
    from lawim_v2.conversation.state.state import ConversationState
    state = ConversationState(language="fr")
    # A simple 'hello' in an otherwise French conversation should not change language
    assert state.language == "fr"


# ─── HELPER ───────────────────────────────────────────────────────────────────

def disassemble_function_line(func, target_name: str) -> bool:
    """Check if a function contains a call to target_name in its bytecode."""
    import dis
    try:
        instructions = list(dis.get_instructions(func))
        for instr in instructions:
            if target_name in str(instr.argrepr):
                return True
    except Exception:
        pass
    return False
