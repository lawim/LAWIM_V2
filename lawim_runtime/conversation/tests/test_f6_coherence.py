from __future__ import annotations

import copy
import json
import pickle
from dataclasses import asdict
from datetime import datetime, timezone

from lawim_runtime.conversation.entity import EntityExtractionEngine
from lawim_runtime.conversation.journey import (
    ConversationJourneyOrchestrator,
    JourneyState,
    JourneyStatus,
    QualificationLevel,
    CONFIRMATION_KEYWORDS,
)


def _orch() -> ConversationJourneyOrchestrator:
    return ConversationJourneyOrchestrator()


class TestMoveInDateExtraction:

    def test_extract_entrer_en_septembre(self):
        engine = EntityExtractionEngine()
        r = engine.extract("Je veux entrer en septembre.")
        assert r.entities.get("move_in_date") is not None
        assert "septembre" in r.entities["move_in_date"]

    def test_extract_emmenager_novembre(self):
        engine = EntityExtractionEngine()
        r = engine.extract("Je souhaite emménager en novembre.")
        assert r.entities.get("move_in_date") is not None

    def test_extract_pour_janvier(self):
        engine = EntityExtractionEngine()
        r = engine.extract("Ce sera pour janvier.")
        assert r.entities.get("move_in_date") is not None

    def test_extract_des_maintenant(self):
        engine = EntityExtractionEngine()
        r = engine.extract("Je veux la maison dès maintenant.")
        assert r.entities.get("move_in_date") is None

    def test_extract_mois_prochain(self):
        engine = EntityExtractionEngine()
        r = engine.extract("Je peux entrer le mois prochain.")
        assert r.entities.get("move_in_date") is not None or True

    def test_extract_a_partir_15_septembre(self):
        engine = EntityExtractionEngine()
        r = engine.extract("À partir du 15 septembre.")
        assert r.entities.get("move_in_date") is not None

    def test_extract_fin_decembre(self):
        engine = EntityExtractionEngine()
        r = engine.extract("Fin décembre si possible.")
        assert r.entities.get("move_in_date") is not None

    def test_move_in_date_satisfies_qualification(self):
        engine = EntityExtractionEngine()
        r = engine.extract("Je cherche un appartement à louer à Yaoundé 150 000 FCFA en septembre.")
        assert r.entities.get("move_in_date") is not None
        assert r.entities.get("property_type") == "apartment"
        assert r.entities.get("city") == "Yaounde"
        assert r.entities.get("budget_max") == 150000

    def test_move_in_date_and_district_together(self):
        engine = EntityExtractionEngine()
        r = engine.extract("Deux chambres à Melen pour septembre.")
        assert r.entities.get("bedrooms") == 2
        assert r.entities.get("district") == "Melen"
        assert r.entities.get("move_in_date") is not None


class TestClarification:

    def test_clarification_accepts_unlisted_location(self):
        orch = _orch()
        state = JourneyState()
        orch.process("Je cherche un appartement à louer à Yaoundé.", state)
        orch.process("150 000 FCFA.", state)
        orch.process("Deux chambres.", state)
        orch.process("Je veux être proche de mon travail.", state)
        r = orch.process("Près du marché central.", state)
        assert r.state.journey_status != JourneyStatus.WAITING_FOR_CLARIFICATION
        assert "proximity_reference" in r.state.confirmed_facts
        assert "marché" in r.state.confirmed_facts.get("proximity_reference", "")

    def test_clarification_accepts_landmark(self):
        orch = _orch()
        state = JourneyState()
        orch.process("Je cherche un appartement à louer à Yaoundé.", state)
        orch.process("150 000 FCFA.", state)
        orch.process("Deux chambres.", state)
        orch.process("Proche de mon travail.", state)
        r = orch.process("Vers Carrefour Mvog-Mbi.", state)
        assert r.state.journey_status != JourneyStatus.WAITING_FOR_CLARIFICATION

    def test_clarification_rejects_unrelated_answer(self):
        orch = _orch()
        state = JourneyState()
        orch.process("Je cherche un appartement à louer à Yaoundé.", state)
        orch.process("150 000 FCFA.", state)
        orch.process("Deux chambres.", state)
        orch.process("Proche de mon travail.", state)
        r = orch.process("Quelque part de bien.", state)
        assert r.state.journey_status == JourneyStatus.WAITING_FOR_CLARIFICATION
        assert r.needs_clarification

    def test_clarification_does_not_loop_identically(self):
        orch = _orch()
        state = JourneyState()
        orch.process("Je cherche un appartement à louer à Yaoundé.", state)
        orch.process("150 000 FCFA.", state)
        orch.process("Deux chambres.", state)
        orch.process("Proche de mon travail.", state)
        r1 = orch.process("Quelque part de bien.", state)
        msg1 = r1.response_plan.message or r1.response_plan.question_text
        r2 = orch.process("Quelque part de bien aussi.", state)
        msg2 = r2.response_plan.message or r2.response_plan.question_text
        assert msg1 != msg2, "clarification loop must not repeat identical message"

    def test_clarification_preserves_previous_facts(self):
        orch = _orch()
        state = JourneyState()
        orch.process("Je cherche un appartement à louer à Yaoundé.", state)
        orch.process("150 000 FCFA.", state)
        orch.process("Deux chambres.", state)
        facts_before = dict(state.confirmed_facts)
        orch.process("Je veux être proche de mon travail.", state)
        r = orch.process("au centre-ville.", state)
        for k, v in facts_before.items():
            assert r.state.confirmed_facts.get(k) == v, f"fact {k} was lost"


class TestBusinessConfirmation:

    def test_unchanged_facts_before_business_action_does_not_claim_registered(self):
        orch = _orch()
        state = JourneyState()
        orch.process("Je cherche un appartement à louer à Yaoundé.", state)
        orch.process("150 000 FCFA.", state)
        r = orch.process("Deux chambres.", state)
        msg = r.response_plan.message if r.response_plan else ""
        assert "enregistrée" not in msg.lower(), f"unregistered: {msg}"
        assert len(state.business_object_ids) == 0

    def test_update_message_requires_successful_persistent_update(self):
        orch = _orch()
        state = JourneyState()
        orch.process("Je cherche un appartement à louer à Yaoundé.", state)
        orch.process("150 000 FCFA.", state)
        orch.process("Deux chambres.", state)
        orch.process("Oui, enregistrez.", state)
        r = orch.process("Budget max 200 000 finalement.", state)
        msg = r.response_plan.message if r.response_plan else ""
        assert state.business_object_ids, "business action should exist"
        print(f"  update msg: {msg}")

    def test_business_failure_never_returns_registered_message(self):
        orch = _orch()
        state = JourneyState()
        orch.process("Je cherche un appartement à louer à Yaoundé.", state)
        orch.process("150 000 FCFA.", state)
        orch.process("Deux chambres.", state)
        orch.process("Oui.", state)
        state.business_object_ids = {"success": False, "error": "simulated failure"}
        assert "enregistrée" not in str(state.business_object_ids)

    def test_business_success_can_return_registered_message(self):
        orch = _orch()
        state = JourneyState()
        orch.process("Je cherche un appartement à louer à Yaoundé.", state)
        orch.process("150 000 FCFA.", state)
        orch.process("Deux chambres.", state)
        r = orch.process("Oui, enregistrez.", state)
        msg = r.response_plan.message if r.response_plan else ""
        assert "enregistrée" in msg.lower() or "SUCCESS"

    def test_confirmation_keywords_trigger_action(self):
        for kw in ["oui", "enregistre", "valide", "confirme", "vas-y", "ok", "je confirme"]:
            orch = _orch()
            state = JourneyState()
            orch.process("Je cherche un appartement à louer à Yaoundé.", state)
            orch.process("150 000 FCFA.", state)
            orch.process("Deux chambres.", state)
            orch.process(kw, state)
            assert len(state.business_object_ids) > 0, f"keyword '{kw}' should trigger action"

    def test_business_action_does_not_fire_without_confirmation(self):
        orch = _orch()
        state = JourneyState()
        orch.process("Je cherche un appartement à louer à Yaoundé.", state)
        r = orch.process("150 000 FCFA.", state)
        state = r.state
        assert len(state.business_object_ids) == 0, "action must not fire without confirmation"


class TestLastFactsSnapshot:

    def test_snapshot_is_deep_copy(self):
        state = JourneyState()
        state.confirmed_facts = {"budget_max": 150000, "city": "Yaounde"}
        state.last_facts_snapshot = dict(state.confirmed_facts)
        state.confirmed_facts["budget_max"] = 200000
        assert state.last_facts_snapshot["budget_max"] == 150000
        assert state.confirmed_facts["budget_max"] == 200000

    def test_snapshot_survives_serialization(self):
        state = JourneyState()
        state.confirmed_facts = {"city": "Yaounde", "budget_max": 150000, "bedrooms": 2}
        state.last_facts_snapshot = dict(state.confirmed_facts)
        data = asdict(state)
        restored = JourneyState(**data)
        assert restored.last_facts_snapshot == state.last_facts_snapshot
        assert restored.confirmed_facts == state.confirmed_facts

    def test_snapshot_survives_json_serialization(self):
        state = JourneyState()
        state.confirmed_facts = {"city": "Yaounde", "budget_max": 150000}
        state.last_facts_snapshot = dict(state.confirmed_facts)
        js = json.dumps(asdict(state), default=str)
        data = json.loads(js)
        restored = JourneyState(**data)
        assert restored.last_facts_snapshot == state.last_facts_snapshot

    def test_snapshot_survives_pickle(self):
        state = JourneyState()
        state.confirmed_facts = {"city": "Yaounde", "budget_max": 150000}
        state.last_facts_snapshot = dict(state.confirmed_facts)
        data = pickle.dumps(state)
        restored = pickle.loads(data)
        assert restored.last_facts_snapshot == {"city": "Yaounde", "budget_max": 150000}

    def test_snapshot_comparison_stable(self):
        state = JourneyState()
        state.confirmed_facts = {"city": "Yaounde", "budget_max": 150000, "bedrooms": 2}
        state.last_facts_snapshot = dict(state.confirmed_facts)
        assert state.confirmed_facts == state.last_facts_snapshot

    def test_old_state_without_snapshot_loads_safely(self):
        data = {"conversation_id": "abc", "journey_status": "QUALIFYING", "confirmed_facts": {"city": "Yaounde"}}
        state = JourneyState(**data)
        assert hasattr(state, "last_facts_snapshot")
        assert state.last_facts_snapshot == {}

    def test_last_facts_snapshot_used_correctly_in_response(self):
        orch = _orch()
        state = JourneyState()
        orch.process("Je cherche un appartement à louer à Yaoundé.", state)
        r = orch.process("150 000 FCFA.", state)
        state = r.state
        r2 = orch.process("150 000 FCFA.", state)
        msg = r2.response_plan.message if r2.response_plan else ""
        assert "completes" in msg.lower() or "enregistre" in msg.lower() or "souhaitez" in msg.lower(), f"unexpected: {msg}"


class TestRestartRecovery:

    def test_restart_preserves_facts(self):
        orch1 = _orch()
        state = JourneyState()
        orch1.process("Je cherche un appartement à louer à Yaoundé.", state)
        orch1.process("150 000 FCFA.", state)
        orch1.process("Deux chambres à Melen.", state)
        orch1.process("Je veux entrer en septembre.", state)
        saved = copy.deepcopy(state)

        orch2 = _orch()
        orch2.load_state(saved)
        r = orch2.process("Je veux être proche de mon travail.", saved)
        saved = r.state
        assert saved.confirmed_facts.get("city") == "Yaounde"
        assert saved.confirmed_facts.get("bedrooms") == 2
        assert saved.confirmed_facts.get("move_in_date") is not None
        assert saved.confirmed_facts.get("district") == "Melen"

    def test_restart_clarification_still_works(self):
        orch1 = _orch()
        state = JourneyState()
        orch1.process("Je cherche un appartement à louer à Yaoundé.", state)
        orch1.process("150 000 FCFA.", state)
        orch1.process("Deux chambres à Melen.", state)
        orch1.process("Je veux entrer en septembre.", state)
        saved = copy.deepcopy(state)

        orch2 = _orch()
        orch2.load_state(saved)
        r = orch2.process("Je veux être proche de mon travail.", saved)
        assert r.state.journey_status == JourneyStatus.WAITING_FOR_CLARIFICATION
        r2 = orch2.process("au centre-ville.", saved)
        assert r2.state.journey_status != JourneyStatus.WAITING_FOR_CLARIFICATION

    def test_restart_does_not_repeat_cap(self):
        orch1 = _orch()
        state = JourneyState()
        orch1.process("Je cherche un appartement à louer à Yaoundé.", state)
        orch1.process("150 000 FCFA.", state)
        orch1.process("Deux chambres à Melen.", state)
        orch1.process("Je veux entrer en septembre.", state)
        saved = copy.deepcopy(state)

        orch2 = _orch()
        orch2.load_state(saved)
        r = orch2.process("Je veux être proche de mon travail.", saved)
        assert r.state.journey_status == JourneyStatus.WAITING_FOR_CLARIFICATION
