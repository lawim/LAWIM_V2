"""Chantier 5: Security and privacy tests.

Verifies that:
  - ProviderMemoryContext contains no secrets
  - No cross-case data exposure between different actors
  - No intent/slot modification by provider (through validation)
  - Consent is respected
  - Forbidden content is detected
  - Response validation blocks external referrals
"""

from __future__ import annotations

import os
import sqlite3
import tempfile
import unittest

from lawim_v2.conversation.memory.context_builder import (
    BusinessMemoryContext,
    MemoryContextBuilder,
    ProviderMemoryContext,
)
from lawim_v2.conversation.state.engine import ConversationStateEngine
from lawim_v2.conversation.state.repository import ConversationStateRepository
from lawim_v2.conversation.state.resolver import ConversationResolver
from lawim_v2.conversation.state.state import ConversationState, ResponsePlan
from lawim_v2.conversation.state.validator import ConversationResponseValidator
from lawim_v2.validation.conversation import ConversationValidator
from lawim_v2.validation.structural import StructuralValidator


class TestChantier5SecurityPrivacy(unittest.TestCase):
    """Security and privacy validation tests."""

    # ── ProviderMemoryContext contains no secrets ─────────────────────────

    def test_provider_context_no_secrets(self):
        """ProviderMemoryContext must not contain password, token, or key fields."""
        ctx = ProviderMemoryContext(
            language="fr",
            intent="rental_search",
            active_facts={"city": "Douala", "budget_max": 150000},
            last_question_text="Quel est votre budget ?",
            response_instructions=["Answer the question"],
            prohibitions=["Do not talk about internal systems"],
        )
        serialized = str(ctx.__dict__)
        secret_keywords = ["token", "secret", "api_key", "private_key",
                           "credential", "jwt", "session_key"]
        for kw in secret_keywords:
            self.assertNotIn(kw, serialized.lower(), f"Secret keyword found: {kw}")

    def test_business_context_no_secrets(self):
        """BusinessMemoryContext must not leak secret information."""
        ctx = BusinessMemoryContext(
            conversation_state=None,
            case=None,
            active_slots={"city": "Douala"},
            last_question="Quel est votre budget ?",
            intent="rental_search",
        )
        serialized = str(ctx.__dict__)
        self.assertNotIn("password", serialized.lower())
        self.assertNotIn("token", serialized.lower())
        self.assertNotIn("secret", serialized.lower())
        self.assertNotIn("api_key", serialized.lower())

    # ── No cross-case data exposure ───────────────────────────────────────

    def test_cross_case_isolation(self):
        """Two different actors must have independent state in the same DB."""
        db = tempfile.mktemp(suffix=".db")
        try:
            conn = sqlite3.connect(db)
            conn.row_factory = sqlite3.Row
            repo = ConversationStateRepository(conn)
            resolver = ConversationResolver()
            engine = ConversationStateEngine(repo, resolver)

            engine.process_turn(
                actor_id="actor_a", channel="whatsapp",
                external_conversation_id="+237600000010",
                message="Je cherche un appartement à Douala", language="fr",
            )
            engine.process_turn(
                actor_id="actor_b", channel="whatsapp",
                external_conversation_id="+237600000011",
                message="Je veux acheter une maison à Yaoundé", language="fr",
            )

            state_a = repo.load("whatsapp", "+237600000010")
            state_b = repo.load("whatsapp", "+237600000011")

            self.assertIsNotNone(state_a)
            self.assertIsNotNone(state_b)
            self.assertNotEqual(
                state_a.known_slots.get("city"),
                state_b.known_slots.get("city"),
                "Cities must differ across actors",
            )
        finally:
            if os.path.exists(db):
                os.unlink(db)

    def test_cross_channel_isolation_same_actor(self):
        """Same actor on different channels must have independent state."""
        db = tempfile.mktemp(suffix=".db")
        try:
            conn = sqlite3.connect(db)
            conn.row_factory = sqlite3.Row
            repo = ConversationStateRepository(conn)
            resolver = ConversationResolver()
            engine = ConversationStateEngine(repo, resolver)

            engine.process_turn(
                actor_id="actor_w", channel="whatsapp",
                external_conversation_id="+237111",
                message="Je cherche à Douala", language="fr",
            )
            engine.process_turn(
                actor_id="actor_w", channel="telegram",
                external_conversation_id="tg_111",
                message="Je cherche à Yaoundé", language="fr",
            )

            wa_state = repo.load("whatsapp", "+237111")
            tg_state = repo.load("telegram", "tg_111")

            self.assertIsNotNone(wa_state)
            self.assertIsNotNone(tg_state)
            self.assertEqual(wa_state.actor_id, "actor_w")
            self.assertEqual(tg_state.actor_id, "actor_w")
        finally:
            if os.path.exists(db):
                os.unlink(db)

    # ── Consent respected ─────────────────────────────────────────────────

    def test_consent_enforcement(self):
        """Unverified identity must not auto-merge across channels."""
        from lawim_v2.conversation.identity.models import IdentitySource
        from lawim_v2.conversation.identity.resolver import (
            CrossChannelConsentRepository,
            CrossChannelIdentityResolver,
            IdentityBindingRepository,
        )

        conn = sqlite3.connect(":memory:")
        conn.row_factory = sqlite3.Row
        try:
            binding_repo = IdentityBindingRepository(conn)
            consent_repo = CrossChannelConsentRepository(conn)
            resolver = CrossChannelIdentityResolver(binding_repo, consent_repo)

            resolver.bind_identity(
                actor_id="actor_consent",
                channel="whatsapp",
                channel_identifier="+237600000009",
                source=IdentitySource.WHATSAPP_CHAT_ID,
            )
            resolved, has_consent = resolver.resolve_with_consent(
                "whatsapp", "+237600000009", "telegram",
            )
            self.assertFalse(has_consent,
                             "Unverified identity must not have auto-consent")
        finally:
            conn.close()

    # ── No intent/slot modification by provider (via validation) ──────────

    def test_validator_detects_forbidden_content(self):
        """ConversationValidator must detect forbidden patterns."""
        validator = ConversationValidator()
        forbidden_texts = [
            "Je suis un assistant neutre",
            "neutral assistant",
            "I cannot make business decisions",
            "je ne peux pas prendre de décisions commerciales",
            "provide more context for your request",
            "Regardez sur Jumia",
            "Consultez SeLoger",
            "Voir sur Leboncoin",
        ]
        for text in forbidden_texts:
            is_valid, errors = validator.validate(text, request=None)
            self.assertFalse(is_valid, f"Failed to block: {text[:40]}")
            self.assertGreater(len(errors), 0)

    def test_validator_allows_legitimate_content(self):
        """ConversationValidator must allow legitimate property content."""
        validator = ConversationValidator()
        legitimate_texts = [
            "Je cherche un appartement à Douala",
            "Quel est votre budget ?",
            "Merci de votre intérêt pour LAWIM",
            "Nous avons trouvé 3 biens correspondant à votre recherche",
            "Souhaitez-vous visiter ce bien ?",
        ]
        for text in legitimate_texts:
            is_valid, errors = validator.validate(text, request=None)
            self.assertTrue(is_valid, f"False positive blocked: {text[:40]} -- {errors}")

    def test_validator_detects_external_referrals(self):
        """ConversationResponseValidator must detect platform referrals."""
        validator = ConversationResponseValidator()
        plan = ResponsePlan(maximum_questions=1)
        for platform in ("Jumia", "SeLoger", "Leboncoin", "Facebook", "Lamudi"):
            response, status = validator.validate(
                f"Vous pouvez trouver cela sur {platform}", plan,
            )
            self.assertNotEqual(status, "PASS",
                                f"Failed to block referral: {platform}")

    def test_validator_detects_grammar_correction(self):
        """Validator must block unsolicited grammar corrections."""
        validator = ConversationResponseValidator()
        plan = ResponsePlan(maximum_questions=1)
        corrections = [
            "the correct spelling is appartement",
            "vous avez écrit studio",
            "l'orthographe correcte est",
        ]
        for text in corrections:
            response, status = validator.validate(text, plan)
            self.assertNotEqual(status, "PASS",
                                f"Failed to block grammar: {text[:40]}")

    def test_validator_allows_single_question(self):
        """Responses with exactly one question must pass."""
        validator = ConversationResponseValidator()
        plan = ResponsePlan(maximum_questions=1)
        response, status = validator.validate("Quel est votre budget ?", plan)
        self.assertEqual(status, "PASS")

    def test_validator_rejects_multiple_questions(self):
        """Responses with >1 questions must be repaired."""
        validator = ConversationResponseValidator()
        plan = ResponsePlan(maximum_questions=1)
        response, status = validator.validate(
            "Quel est votre budget ? Et combien de chambres ?", plan,
        )
        self.assertNotEqual(status, "PASS")

    # ── Structural validation privacy ────────────────────────────────────

    def test_structural_validator_checks_json(self):
        """StructuralValidator must reject non-JSON responses."""
        validator = StructuralValidator()
        is_valid, errors = validator.validate("Not JSON at all", request=None)
        self.assertFalse(is_valid)
        self.assertTrue(any("Invalid JSON" in e for e in errors))

    def test_structural_validator_checks_required_fields(self):
        """StructuralValidator must require content, dialogue_act, language."""
        validator = StructuralValidator()
        request = MagicMock(spec=["maximum_length"])
        request.maximum_length = 500
        is_valid, errors = validator.validate('{"content": "Hello"}', request)
        self.assertFalse(is_valid)
        self.assertTrue(any("dialogue_act" in e for e in errors))
        self.assertTrue(any("language" in e for e in errors))

    # ── Response plan does not leak data ──────────────────────────────────

    def test_response_plan_no_forbidden_defaults(self):
        """Default ResponsePlan must not contain forbidden content."""
        plan = ResponsePlan()
        self.assertEqual(plan.maximum_questions, 1)
        self.assertEqual(plan.speaker, "LAWIM AI")
        forbidden = ["jumia", "seloger", "leboncoin", "facebook", "lamudi"]
        for f in forbidden:
            self.assertNotIn(f, plan.response_template.lower())


from unittest.mock import MagicMock


if __name__ == "__main__":
    unittest.main()
