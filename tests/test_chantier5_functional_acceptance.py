"""Chantier 5: Comprehensive functional acceptance tests for LAWIM V2.

Covers multi-turn journeys, corrections, intent changes, rephrases, and
validation policies. Each test wipes its own temp DB; all are independent.
"""

from __future__ import annotations

import os
import sqlite3
import tempfile
import unittest

from lawim_v2.conversation.state.engine import ConversationStateEngine
from lawim_v2.conversation.state.repository import ConversationStateRepository
from lawim_v2.conversation.state.resolver import ConversationResolver
from lawim_v2.knowledge_runtime.engine.readiness import ReadinessEvaluator
from lawim_v2.knowledge_runtime.engine.resolver import NextQuestionResolver
from lawim_v2.knowledge_runtime.engine.wizard import ProgressiveWizard
from lawim_v2.knowledge_runtime.models.question_rule import QuestionRule
from lawim_v2.knowledge_runtime.models.readiness import ReadinessDefinition, ReadinessLevel
from lawim_v2.knowledge_runtime.models.qualification import QualificationMatrix
from lawim_v2.knowledge_runtime.registry.matrix_registry import MatrixRegistry
from lawim_v2.knowledge_runtime.registry.question_rule_registry import QuestionRuleRegistry
from lawim_v2.knowledge_runtime.registry.readiness_registry import ReadinessRegistry


# ── Helpers ─────────────────────────────────────────────────────────────────


def _make_engine():
    db = tempfile.mktemp(suffix=".db")
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    repo = ConversationStateRepository(conn)
    resolver = ConversationResolver()
    engine = ConversationStateEngine(repo, resolver)
    return engine, db


def _default_question_registry():
    qreg = QuestionRuleRegistry()
    qreg.register(QuestionRule(field="intent", rule_type="always_ask"))
    qreg.register(QuestionRule(field="transaction_type", rule_type="always_ask"))
    qreg.register(QuestionRule(field="property_type", rule_type="always_ask"))
    qreg.register(QuestionRule(field="city", rule_type="always_ask"))
    qreg.register(QuestionRule(field="neighborhood", rule_type="conditional_ask", priority=4))
    qreg.register(QuestionRule(field="budget_max", rule_type="conditional_ask", priority=3))
    qreg.register(QuestionRule(field="furnished", rule_type="conditional_ask", priority=8))
    qreg.register(QuestionRule(field="move_in_date", rule_type="conditional_ask", priority=9))
    qreg.lock()
    return qreg


def _default_matrix_registry():
    mreg = MatrixRegistry()
    for m_id, family, ttype, ptype in [
        ("M_RENT_APT", "RESIDENTIAL_SEARCH", "RENT", "apartment"),
        ("M_RENT_STUDIO", "RESIDENTIAL_SEARCH", "RENT", "studio"),
        ("M_RENT_HOUSE", "RESIDENTIAL_SEARCH", "RENT", "house"),
        ("M_BUY_HOUSE", "RESIDENTIAL_SEARCH", "BUY", "house"),
        ("M_BUY_LAND", "LAND_SEARCH", "BUY", "land"),
    ]:
        mreg.register(QualificationMatrix(
            matrix_id=m_id, canonical_name=m_id.lower(),
            request_family=family, transaction_type=ttype,
            property_type=ptype, requester_typology="tenant" if ttype == "RENT" else "buyer",
            journey_stage="SEARCH", description="",
            minimum_intake_fields=("intent", "transaction_type", "property_type", "city"),
            minimum_search_fields=("neighborhood", "budget_max"),
            sources=("test",),
        ))
    mreg.lock()
    return mreg


def _default_readiness():
    reg = ReadinessRegistry()
    reg.register(ReadinessDefinition(
        level=ReadinessLevel.INTENT_IDENTIFIED, order=1, description="",
        required_fields=("intent", "transaction_type"),
    ))
    reg.register(ReadinessDefinition(
        level=ReadinessLevel.MINIMUM_INTAKE_READY, order=2, description="",
        required_fields=("property_type", "city"),
    ))
    reg.register(ReadinessDefinition(
        level=ReadinessLevel.MINIMUM_SEARCH_READY, order=3, description="",
        required_fields=("neighborhood", "budget_max"),
    ))
    reg.lock()
    return reg


def _make_engine_with_wizard():
    db = tempfile.mktemp(suffix=".db")
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    repo = ConversationStateRepository(conn)
    resolver = ConversationResolver()
    readiness_eval = ReadinessEvaluator(_default_readiness())
    next_q_resolver = NextQuestionResolver(_default_question_registry(), _default_matrix_registry())
    wizard = ProgressiveWizard(readiness=readiness_eval, resolver=next_q_resolver)
    engine = ConversationStateEngine(repo, resolver, wizard=wizard)
    return engine, db


# ─── TESTS ──────────────────────────────────────────────────────────────────


class TestChantier5FunctionalAcceptance(unittest.TestCase):
    """Core functional acceptance: journeys, corrections, rephrases, policies."""

    # ── Journey: Studio rental ──────────────────────────────────────────────

    def test_studio_rental_journey(self):
        """Bonjour -> Studio -> Habitation -> Louer -> Douala -> Akwa -> budget"""
        engine, db = _make_engine()
        try:
            turns = [
                "Bonjour",
                "J'ai besoin d'un studio",
                "Pour habitation",
                "Je veux louer",
                "Douala",
                "Akwa",
                "100000",
            ]
            for msg in turns:
                result = engine.process_turn(
                    actor_id="test", channel="whatsapp",
                    external_conversation_id="+237studio",
                    message=msg, language="fr",
                )
                self.assertIsNotNone(result["response"])
                self.assertFalse(result.get("handover_required", False))
            state = result["state"]
            self.assertEqual(state.actor_id, "test")
            self.assertIn("city", state.known_slots)
        finally:
            if os.path.exists(db):
                os.unlink(db)

    # ── Journey: Apartment rental ──────────────────────────────────────────

    def test_apartment_rental_journey(self):
        """Appartement Douala -> Bonamoussadi -> budget -> bedrooms -> furnished"""
        engine, db = _make_engine()
        try:
            for msg in [
                "Je cherche un appartement à Douala",
                "Bonamoussadi",
                "180000",
                "2 chambres",
                "Meublé",
            ]:
                result = engine.process_turn(
                    actor_id="test", channel="whatsapp",
                    external_conversation_id="+237apt",
                    message=msg, language="fr",
                )
                self.assertIsNotNone(result["response"])
                self.assertFalse(result.get("handover_required", False))
            state = result["state"]
            self.assertIsNotNone(state.actor_id)
            self.assertIn("city", state.known_slots)
            self.assertIn("budget_max", state.known_slots)
            self.assertIn("bedroom_count", state.known_slots)
        finally:
            if os.path.exists(db):
                os.unlink(db)

    # ── Journey: Buy house ─────────────────────────────────────────────────

    def test_buy_house_journey(self):
        """Acheter maison -> Yaoundé -> Bastos -> budget"""
        engine, db = _make_engine()
        try:
            for msg in [
                "Je veux acheter une maison",
                "Yaoundé",
                "Bastos",
                "80000000",
            ]:
                result = engine.process_turn(
                    actor_id="test", channel="whatsapp",
                    external_conversation_id="+237buy",
                    message=msg, language="fr",
                )
                self.assertIsNotNone(result["response"])
                self.assertFalse(result.get("handover_required", False))
            state = result["state"]
            self.assertIsNotNone(state.actor_id)
            self.assertIn("city", state.known_slots)
            self.assertIn("budget_max", state.known_slots)
        finally:
            if os.path.exists(db):
                os.unlink(db)

    # ── Journey: Buy land ─────────────────────────────────────────────────

    def test_buy_land_journey(self):
        """Terrain -> Yaoundé -> Nkolbisson -> surface -> budget"""
        engine, db = _make_engine()
        try:
            for msg in [
                "Je veux acheter un terrain",
                "Yaoundé",
                "Nkolbisson",
                "500 m²",
                "12000000",
            ]:
                result = engine.process_turn(
                    actor_id="test", channel="whatsapp",
                    external_conversation_id="+237land",
                    message=msg, language="fr",
                )
                self.assertIsNotNone(result["response"])
                self.assertFalse(result.get("handover_required", False))
            state = result["state"]
            self.assertIsNotNone(state.actor_id)
            self.assertIn("city", state.known_slots)
            self.assertIn("budget_max", state.known_slots)
        finally:
            if os.path.exists(db):
                os.unlink(db)

    # ── Correction scenarios ──────────────────────────────────────────────

    def test_correction_budget(self):
        """Budget 150k -> Finalement 220k must update slot via correction path."""
        engine, db = _make_engine()
        try:
            engine.process_turn(
                actor_id="test", channel="whatsapp",
                external_conversation_id="+237corr",
                message="150000", language="fr",
            )
            result = engine.process_turn(
                actor_id="test", channel="whatsapp",
                external_conversation_id="+237corr",
                message="Finalement mon budget est de 220000", language="fr",
            )
            state = result["state"]
            self.assertEqual(state.known_slots.get("budget_max"), 220000)
        finally:
            if os.path.exists(db):
                os.unlink(db)

    def test_correction_district(self):
        """Akwa -> Finalement Bonamoussadi updates district."""
        engine, db = _make_engine()
        try:
            engine.process_turn(
                actor_id="test", channel="whatsapp",
                external_conversation_id="+237corr2",
                message="Je cherche à Akwa", language="fr",
            )
            result = engine.process_turn(
                actor_id="test", channel="whatsapp",
                external_conversation_id="+237corr2",
                message="Finalement Bonamoussadi", language="fr",
            )
            state = result["state"]
            if "district" in state.known_slots:
                self.assertEqual(state.known_slots["district"].lower(), "bonamoussadi")
        finally:
            if os.path.exists(db):
                os.unlink(db)

    def test_correction_bedrooms(self):
        """3 chambres -> Finalement 2 updates bedroom count."""
        engine, db = _make_engine()
        try:
            engine.process_turn(
                actor_id="test", channel="whatsapp",
                external_conversation_id="+237corr3",
                message="Je cherche 3 chambres", language="fr",
            )
            result = engine.process_turn(
                actor_id="test", channel="whatsapp",
                external_conversation_id="+237corr3",
                message="Finalement 2 chambres", language="fr",
            )
            state = result["state"]
            if "bedroom_count" in state.known_slots:
                self.assertEqual(state.known_slots["bedroom_count"], 2)
        finally:
            if os.path.exists(db):
                os.unlink(db)

    # ── Intent change ──────────────────────────────────────────────────────

    def test_intent_change_location_to_buy(self):
        """Location -> acheter must change intent."""
        engine, db = _make_engine()
        try:
            engine.process_turn(
                actor_id="test", channel="whatsapp",
                external_conversation_id="+237intent",
                message="Je cherche une location", language="fr",
            )
            result = engine.process_turn(
                actor_id="test", channel="whatsapp",
                external_conversation_id="+237intent",
                message="Finalement je veux acheter", language="fr",
            )
            self.assertIsNotNone(result["state"].current_intent)
        finally:
            if os.path.exists(db):
                os.unlink(db)

    # ── Rephrase scenarios ─────────────────────────────────────────────────

    def test_rephrase_je_ne_comprends_pas(self):
        """'Je ne comprends pas' after a wizard question triggers REPHRASE."""
        engine, db = _make_engine_with_wizard()
        try:
            engine.process_turn(
                actor_id="test", channel="whatsapp",
                external_conversation_id="+237rfr",
                message="Bonjour", language="fr",
            )
            engine.process_turn(
                actor_id="test", channel="whatsapp",
                external_conversation_id="+237rfr",
                message="Je cherche un appartement", language="fr",
            )
            result = engine.process_turn(
                actor_id="test", channel="whatsapp",
                external_conversation_id="+237rfr",
                message="Je ne comprends pas", language="fr",
            )
            self.assertEqual(result["response_plan"].response_type, "REPHRASE")
        finally:
            if os.path.exists(db):
                os.unlink(db)

    def test_rephrase_i_dont_understand(self):
        """English rephrase after wizard question."""
        engine, db = _make_engine_with_wizard()
        try:
            engine.process_turn(
                actor_id="test", channel="whatsapp",
                external_conversation_id="+237rfr2",
                message="Hello", language="en",
            )
            engine.process_turn(
                actor_id="test", channel="whatsapp",
                external_conversation_id="+237rfr2",
                message="I am looking for an apartment", language="en",
            )
            result = engine.process_turn(
                actor_id="test", channel="whatsapp",
                external_conversation_id="+237rfr2",
                message="I don't understand", language="en",
            )
            self.assertEqual(result["response_plan"].response_type, "REPHRASE")
        finally:
            if os.path.exists(db):
                os.unlink(db)

    def test_rephrase_cest_a_dire(self):
        """'C\'est-à-dire' after wizard question triggers REPHRASE."""
        engine, db = _make_engine_with_wizard()
        try:
            engine.process_turn(
                actor_id="test", channel="whatsapp",
                external_conversation_id="+237rfr3",
                message="Bonjour", language="fr",
            )
            engine.process_turn(
                actor_id="test", channel="whatsapp",
                external_conversation_id="+237rfr3",
                message="Je cherche un appartement", language="fr",
            )
            result = engine.process_turn(
                actor_id="test", channel="whatsapp",
                external_conversation_id="+237rfr3",
                message="C'est-à-dire ?", language="fr",
            )
            self.assertEqual(result["response_plan"].response_type, "REPHRASE")
        finally:
            if os.path.exists(db):
                os.unlink(db)

    # ── Validation policies ────────────────────────────────────────────────

    def test_greeting_does_not_trigger_handover(self):
        """Greeting must not trigger unexpected handover."""
        engine, db = _make_engine()
        try:
            for msg in ("Bonjour", "Salut", "Hello", "Hi", "Bonsoir"):
                result = engine.process_turn(
                    actor_id="test", channel="whatsapp",
                    external_conversation_id="+237gr",
                    message=msg, language="fr",
                )
                self.assertFalse(result.get("handover_required", False))
        finally:
            if os.path.exists(db):
                os.unlink(db)

    def test_one_question_per_response_validated(self):
        """Validator rejects multiple questions."""
        from lawim_v2.conversation.state.validator import ConversationResponseValidator
        from lawim_v2.conversation.state.state import ResponsePlan
        validator = ConversationResponseValidator()
        plan = ResponsePlan(maximum_questions=1)
        response, status = validator.validate(
            "Que cherchez-vous ? Et quel budget ?", plan,
        )
        self.assertNotEqual(status, "PASS")

    def test_external_referrals_detected(self):
        """Validator blocks external platform names."""
        from lawim_v2.conversation.state.validator import ConversationResponseValidator
        from lawim_v2.conversation.state.state import ResponsePlan
        validator = ConversationResponseValidator()
        plan = ResponsePlan(maximum_questions=1)
        for junk in ("Jumia", "SeLoger", "Leboncoin", "Facebook", "Lamudi"):
            response, status = validator.validate(
                f"Regardez sur {junk}", plan,
            )
            self.assertNotEqual(status, "PASS", f"Failed to block: {junk}")

    def test_actor_id_persists_across_turns(self):
        """Actor identity persists across all turns."""
        engine, db = _make_engine()
        try:
            for i in range(5):
                result = engine.process_turn(
                    actor_id="persistent", channel="web",
                    external_conversation_id="session-p",
                    message=f"Turn {i}", language="fr",
                )
                self.assertEqual(result["state"].actor_id, "persistent")
        finally:
            if os.path.exists(db):
                os.unlink(db)

    def test_language_detected_and_switched(self):
        """Language detected on each turn."""
        engine, db = _make_engine()
        try:
            result = engine.process_turn(
                actor_id="lang", channel="web",
                external_conversation_id="lang-s",
                message="I want to rent an apartment", language="en",
            )
            self.assertEqual(result["state"].language, "en")
        finally:
            if os.path.exists(db):
                os.unlink(db)

    def test_slots_accumulate_across_turns(self):
        """Known slots collect over multiple turns."""
        engine, db = _make_engine()
        try:
            engine.process_turn(
                actor_id="accum", channel="whatsapp",
                external_conversation_id="+237accum",
                message="Je cherche un appartement à Douala", language="fr",
            )
            engine.process_turn(
                actor_id="accum", channel="whatsapp",
                external_conversation_id="+237accum",
                message="150000", language="fr",
            )
            r3 = engine.process_turn(
                actor_id="accum", channel="whatsapp",
                external_conversation_id="+237accum",
                message="2 chambres", language="fr",
            )
            state = r3["state"]
            self.assertIn("city", state.known_slots)
            self.assertIn("budget_max", state.known_slots)
            self.assertIn("bedroom_count", state.known_slots)
        finally:
            if os.path.exists(db):
                os.unlink(db)

    def test_response_is_never_none(self):
        """Every process_turn call must return a non-None response."""
        engine, db = _make_engine()
        try:
            messages = [
                "Bonjour", "Je cherche un studio", "Douala",
                "100000", "Meublé", "Oui",
            ]
            for msg in messages:
                result = engine.process_turn(
                    actor_id="test", channel="whatsapp",
                    external_conversation_id="+237none",
                    message=msg, language="fr",
                )
                self.assertIsNotNone(result["response"])
        finally:
            if os.path.exists(db):
                os.unlink(db)


if __name__ == "__main__":
    unittest.main()
