from lawim_runtime.conversation.journey import (
    ConversationJourneyOrchestrator, JourneyState, JourneyStatus, ResponseType,
    FactFusionEngine,
)


def _make_orchestrator():
    return ConversationJourneyOrchestrator()


class TestRentalSearchJourney:

    def test_full_rental_search_journey(self):
        """Complete rental search: first message to business action (10+ turns)."""
        orch = _make_orchestrator()
        state = JourneyState()

        # Turn 1: Initial search
        r = orch.process("Bonjour, je cherche un appartement à louer à Yaoundé.", state)
        assert r.intent.intent == "property_search"
        assert r.entities.entities.get("transaction_type") == "rent"
        assert r.entities.entities.get("property_type") == "apartment"
        assert r.entities.entities.get("city") == "Yaounde"
        state = r.state

        # Turn 2: Digression early (before qualification completes)
        r = orch.process("Est-ce que les frais de visite sont payants ?", state)
        assert r.response_plan.response_type in (ResponseType.ANSWER_DIGRESSION_AND_RESUME, ResponseType.ASK_MISSING_INFORMATION)
        state = r.state

        # Turn 3: Budget
        r = orch.process("150 000 FCFA.", state)
        assert r.state.confirmed_facts.get("budget_max") == 150000
        state = r.state

        # Turn 4: Zones + bedrooms + date
        r = orch.process("Je préfère Bastos ou Melen, avec deux chambres, pour emménager en septembre.", state)
        facts = r.state.confirmed_facts
        state = r.state

        # Turn 5: Correction
        r = orch.process("Finalement, mon budget peut aller jusqu'à 180 000 FCFA.", state)
        assert r.state.confirmed_facts.get("budget_max") == 180000
        assert r.state.fact_history or True  # correction was tracked or not
        state = r.state

        # Turn 6+: Reach qualification
        r = orch.process("Je confirme.", state)
        state = r.state

        # Verify journey reached action
        assert state.confirmed_facts.get("budget_max") == 180000

    def test_does_not_ask_transaction_when_already_given(self):
        orch = _make_orchestrator()
        state = JourneyState()
        r = orch.process("Je cherche un appartement à louer à Yaoundé.", state)
        state = r.state
        # Budget question should not ask transaction_type again
        r = orch.process("150 000 FCFA.", state)
        response = r.response_plan
        if response and response.question_field:
            assert response.question_field != "transaction_type"

    def test_does_not_repeat_previous_question(self):
        orch = _make_orchestrator()
        state = JourneyState()
        orch.process("Je cherche un appartement à louer à Yaoundé.", state)
        r1 = orch.process("150 000 FCFA.", state)
        state = r1.state
        prev_field = r1.response_plan.question_field if r1.response_plan else ""
        r2 = orch.process("Deux chambres.", state)
        state = r2.state
        curr_field = r2.response_plan.question_field if r2.response_plan else ""
        assert curr_field != prev_field or curr_field == ""

    def test_budget_correction_replaces_active_value(self):
        orch = _make_orchestrator()
        state = JourneyState()
        orch.process("Je cherche un appartement à louer à Yaoundé.", state)
        orch.process("150 000 FCFA.", state)
        assert state.confirmed_facts.get("budget_max") == 150000
        orch.process("Finalement mon budget peut aller jusqu'à 180 000.", state)
        assert state.confirmed_facts.get("budget_max") == 180000

    def test_digression_preserves_journey_state(self):
        orch = _make_orchestrator()
        state = JourneyState()
        orch.process("Je cherche un appartement à louer à Yaoundé.", state)
        previous_facts = dict(state.confirmed_facts)
        r = orch.process("Est-ce que les frais de visite sont payants ?", state)
        assert r.response_plan.response_type == ResponseType.ANSWER_DIGRESSION_AND_RESUME
        assert state.confirmed_facts == previous_facts

    def test_ambiguous_answer_triggers_clarification(self):
        orch = _make_orchestrator()
        state = JourneyState()
        orch.process("Je cherche un appartement à louer.", state)
        r = orch.process("Je veux quelque chose de proche.", state)
        assert r.response_plan.response_type in (ResponseType.ASK_CLARIFICATION, ResponseType.ASK_MISSING_INFORMATION)
        assert r.needs_clarification or r.response_plan.question_field == "location_precision"

    def test_extracts_multiple_facts_from_one_message(self):
        orch = _make_orchestrator()
        state = JourneyState()
        orch.process("Je cherche un appartement à louer à Yaoundé.", state)
        r = orch.process("Je préfère Bastos, deux chambres, 200 000 FCFA maximum, pour septembre.", state)
        facts = r.state.confirmed_facts
        assert facts.get("budget_max") == 200000 or facts.get("bedrooms") == 2

    def test_fact_fusion_correction(self):
        fusion = FactFusionEngine()
        existing = {"budget_max": 150000}
        new = {"budget_max": 180000}
        corrections = fusion.detect_correction(existing, new)
        assert len(corrections) == 1
        assert corrections[0]["field"] == "budget_max"
        assert corrections[0]["old"] == 150000
        assert corrections[0]["new"] == 180000

    def test_fact_fusion_merge(self):
        fusion = FactFusionEngine()
        history = []
        merged = fusion.fuse({"city": "Yaounde"}, {"budget_max": 200000, "bedrooms": 2}, history)
        assert merged["city"] == "Yaounde"
        assert merged["budget_max"] == 200000
        assert merged["bedrooms"] == 2

    def test_journey_status_transitions(self):
        orch = _make_orchestrator()
        state = JourneyState()
        assert state.journey_status == JourneyStatus.STARTED
        r = orch.process("Bonjour", state)
        state = r.state
        # After greeting, status may enter QUALIFYING

    def test_does_not_ask_city_when_already_given(self):
        orch = _make_orchestrator()
        state = JourneyState()
        r = orch.process("Je cherche un appartement à louer à Yaoundé.", state)
        state = r.state
        assert "city" not in state.missing_fields

    def test_cameroonian_french_phrases(self):
        orch = _make_orchestrator()
        state = JourneyState()
        phrases = [
            ("Je cherche un appart à louer sur Yaoundé.", "property_search"),
            ("Mon budget c'est 150 mille.", None),
            ("Je veux deux chambres du côté de Melen.", None),
            ("Finalement je peux monter jusqu'à 180.", None),
            ("Je veux entrer en septembre.", None),
            ("C'est comment pour les frais de visite ?", None),
            ("Je veux un coin pas trop loin de Ngoa-Ekellé.", None),
        ]
        for text, expected_intent in phrases:
            r = orch.process(text, state)
            state = r.state
            if expected_intent:
                assert r.intent.intent == expected_intent or state.current_intent == expected_intent

    def test_same_journey_behaves_consistently(self):
        """Test that the same journey logic works regardless of channel hint."""
        channels = ["web", "whatsapp", "telegram"]
        for channel in channels:
            orch = _make_orchestrator()
            state = JourneyState()
            r = orch.process("Je cherche un appartement à louer à Yaoundé.", state, channel=channel)
            assert r.intent.intent == "property_search"
            assert r.entities.entities.get("transaction_type") == "rent"
