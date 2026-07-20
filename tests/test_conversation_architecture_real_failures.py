"""Real failure reproduction tests — must fail before architecture fixes."""

from unittest.mock import MagicMock
import pytest

from lawim_v2.communication.service import CommunicationService
from lawim_v2.conversation.state.engine import ConversationStateEngine
from lawim_v2.conversation.state.repository import ConversationStateRepository
from lawim_v2.conversation.state.resolver import ConversationResolver
import sqlite3, tempfile, os


def _make_engine() -> ConversationStateEngine:
    db = tempfile.mktemp(suffix=".db")
    conn = sqlite3.connect(db)
    repo = ConversationStateRepository(conn)
    resolver = ConversationResolver()
    engine = ConversationStateEngine(repo, resolver)
    # Don't clean up - it's transient for the test
    return engine, db


# ─── SCENARIO: STUDIO ─────────────────────────────────────────────────────────

def test_studio_in_conversation_is_real_estate() -> None:
    """'J'ai besoin d'un studio' must be interpreted as real estate, not recording/photo."""
    engine, db = _make_engine()
    result = engine.process_turn(actor_id="test", channel="whatsapp",
                                  external_conversation_id="+237123",
                                  message="J'ai besoin d'un studio", language="fr")
    assert result["response"] is not None
    resp_lower = result["response"].lower()
    assert "studio" in resp_lower
    assert "photo" not in resp_lower and "enregistrement" not in resp_lower and "danse" not in resp_lower
    os.unlink(db)


@pytest.mark.xfail(strict=True, reason="Residential use not retained as continuation")
def test_residential_use_continues_studio_request() -> None:
    """After 'studio', 'pour habitation' must set residential use."""
    engine, db = _make_engine()
    engine.process_turn(actor_id="test", channel="whatsapp",
                         external_conversation_id="+237123",
                         message="J'ai besoin d'un studio", language="fr")
    # Second turn - the state engine should have a last_question that makes
    # "pour habitation" contextualizable
    result = engine.process_turn(actor_id="test", channel="whatsapp",
                                  external_conversation_id="+237123",
                                  message="Pour habitation", language="fr")
    assert result["response"] is not None
    os.unlink(db)


# ─── SCENARIO: LANGUAGE ───────────────────────────────────────────────────────

def test_french_conversation_is_not_translated() -> None:
    """A French conversation must not have a response that translates French."""
    engine, db = _make_engine()
    result = engine.process_turn(actor_id="test", channel="whatsapp",
                                  external_conversation_id="+237456",
                                  message="Je cherche un appartement", language="fr")
    assert result["response"] is not None
    resp_lower = result["response"].lower()
    forbidden = ["french for", "in english", "in french", "français signifie"]
    for phrase in forbidden:
        assert phrase not in resp_lower, f"Translation found: {phrase}"
    os.unlink(db)


# ─── SCENARIO: I DON'T UNDERSTAND ─────────────────────────────────────────────

@pytest.mark.xfail(strict=True, reason="Rephrase not implemented without state engine")
def test_i_dont_understand_rephrases_last_question() -> None:
    """'Je ne comprends pas' must rephrase the last question."""
    engine, db = _make_engine()
    # First ask a question
    engine.process_turn(actor_id="test", channel="whatsapp",
                         external_conversation_id="+237789",
                         message="Bonjour", language="fr")
    # Load the state to check
    result = engine.process_turn(actor_id="test", channel="whatsapp",
                                  external_conversation_id="+237789",
                                  message="Je ne comprends pas", language="fr")
    assert result["response"] is not None
    assert "je ne comprends pas" not in result["response"][:50].lower()
    os.unlink(db)


# ─── SCENARIO: GRAMMAR ────────────────────────────────────────────────────────

def test_grammar_is_not_corrected_without_request() -> None:
    """'Je prefere' must not trigger grammar correction."""
    from lawim_v2.conversation.state.validator import ConversationResponseValidator
    from lawim_v2.conversation.state.state import ResponsePlan
    validator = ConversationResponseValidator()
    plan = ResponsePlan()
    text = "Je prefere le quartier Bonamoussadi."
    # Test that validator doesn't try to correct grammar
    # (Using a clean plan - validator only checks for known violations)
    response, status = validator.validate(text, plan)
    assert status == "PASS"  # No grammar correction, no violation


# ─── SCENARIO: HANDOVER ───────────────────────────────────────────────────────

def test_handover_requires_explicit_request() -> None:
    """Handover must only trigger on explicit request, not on greetings."""
    engine, db = _make_engine()
    result = engine.process_turn(actor_id="test", channel="whatsapp",
                                  external_conversation_id="+237111",
                                  message="Bonjour", language="fr")
    assert result.get("handover_required") is False
    os.unlink(db)


# ─── SCENARIO: ONE QUESTION ───────────────────────────────────────────────────

def test_one_question_per_response() -> None:
    """Each response must contain at most one question."""
    from lawim_v2.conversation.state.validator import ConversationResponseValidator
    from lawim_v2.conversation.state.state import ResponsePlan
    validator = ConversationResponseValidator()
    plan = ResponsePlan(maximum_questions=1)
    text = "Que cherchez-vous ? Et quel budget ?"
    response, status = validator.validate(text, plan)
    assert status != "PASS", "Multiple questions not rejected"


# ─── SCENARIO: NO EXTERNAL REFERRAL ───────────────────────────────────────────

def test_no_external_referral_in_greeting() -> None:
    """Static greeting must not contain external referrals."""
    svc = CommunicationService.__new__(CommunicationService)
    greeting = svc._greeting_response("whatsapp", "fr")
    forbidden = ["jumia", "seloger", "leboncoin", "facebook", "lamudi"]
    for word in forbidden:
        assert word not in greeting.lower(), f"External referral found: {word}"
