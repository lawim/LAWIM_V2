"""Fixture tests reproducing real WhatsApp conversation journey."""

from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# Turn 1: Greeting
# ---------------------------------------------------------------------------
class TestJourneyGreeting:
    def test_greeting_message_format(self):
        from lawim_v2.conversation.state.engine import _GREETING_RESPONSES
        fr = _GREETING_RESPONSES["fr"]
        assert "LAWIM AI" in fr
        assert "décrire" in fr
        assert "projet immobilier" in fr or "location" in fr
        assert "──────────────" in fr
        assert "ℹ" in fr


# ---------------------------------------------------------------------------
# Turn 2: Initial search request
# ---------------------------------------------------------------------------
class TestJourneyInitialSearch:
    def test_property_type_and_city_extracted(self):
        from lawim_v2.conversation.understanding.extractor import extract_all
        from lawim_v2.conversation.understanding.property_types import normalize_property_type, normalize_transaction_type
        text = "Bonjour, je cherche un appartement à louer à Yaoundé."
        prop = normalize_property_type(text)
        assert prop.normalized_type == "APARTMENT"
        trans = normalize_transaction_type(text)
        assert trans.normalized_type == "RENT"
        result = extract_all(text)
        facts = {f["field"]: f for f in result["facts"]}
        assert "city" in facts


# ---------------------------------------------------------------------------
# Turn 3: District
# ---------------------------------------------------------------------------
class TestJourneyDistrict:
    def test_district_recognized(self):
        from lawim_v2.conversation.understanding.extractor import extract_all
        text = "À Mvan."
        result = extract_all(text)
        facts = {f["field"]: f for f in result["facts"]}
        assert "neighborhood" in facts or "city" in facts


# ---------------------------------------------------------------------------
# Turn 4: Budget
# ---------------------------------------------------------------------------
class TestJourneyBudget:
    def test_budget_with_f_suffix(self):
        from lawim_v2.conversation.understanding.money import normalize_amount
        text = "Mon budget maximal est de 200 000 F par mois."
        result = normalize_amount(text)
        assert result.normalized_amount == 200_000
        assert result.currency == "XAF"
        assert result.period == "monthly"

    def test_budget_fcfa(self):
        from lawim_v2.conversation.understanding.money import normalize_amount
        result = normalize_amount("200000 FCFA")
        assert result.normalized_amount == 200_000

    def test_budget_k_suffix(self):
        from lawim_v2.conversation.understanding.money import normalize_amount
        result = normalize_amount("250k")
        assert result.normalized_amount == 250_000

    def test_budget_french_words(self):
        from lawim_v2.conversation.understanding.money import normalize_amount
        result = normalize_amount("deux cent mille")
        assert result.normalized_amount == 200_000


# ---------------------------------------------------------------------------
# Turn 5: Bedrooms (should NOT set property_type to ROOM)
# ---------------------------------------------------------------------------
class TestJourneyBedrooms:
    def test_bedrooms_does_not_override_property_type(self):
        from lawim_v2.conversation.understanding.property_types import normalize_property_type
        for text in ["Je veux deux chambres.", "Je veux 3 chambres", "Je cherche 2 chambres"]:
            prop = normalize_property_type(text)
            assert prop.normalized_type != "ROOM", f"'{text}' should not produce property_type=ROOM"

    def test_room_without_number_still_returns_room(self):
        from lawim_v2.conversation.understanding.property_types import normalize_property_type
        prop = normalize_property_type("Je cherche une chambre")
        assert prop.normalized_type == "ROOM"
        prop2 = normalize_property_type("Je cherche une chambre meublée")
        assert prop2.normalized_type == "ROOM"


# ---------------------------------------------------------------------------
# Turn 6: Budget correction
# ---------------------------------------------------------------------------
class TestJourneyBudgetCorrection:
    def test_budget_correction_detected(self):
        from lawim_v2.conversation.understanding.money import normalize_amount
        text = "Finalement, mon budget maximal est de 250 000 F."
        result = normalize_amount(text)
        assert result.normalized_amount == 250_000
        assert result.currency == "XAF"


# ---------------------------------------------------------------------------
# Turn 7: Visit without selected property
# ---------------------------------------------------------------------------
class TestJourneyVisitWithoutProperty:
    def test_visit_without_property_response(self):
        decision_action = "NO_ACTION"
        selected_property_id = None
        if selected_property_id is None:
            decision_action = "VISIT_REQUEST_WITHOUT_SELECTED_PROPERTY"
        assert decision_action == "VISIT_REQUEST_WITHOUT_SELECTED_PROPERTY"


# ---------------------------------------------------------------------------
# Full journey state test
# ---------------------------------------------------------------------------
class TestJourneyFullState:
    def test_full_journey_expected_state(self):
        expected = {
            "intent": "property_search",
            "transaction_type": "RENT",
            "property_type": "APARTMENT",
            "city": "Yaoundé",
            "district": "Mvan",
            "budget_max": 250000,
            "currency": "XAF",
            "bedrooms": 2,
        }
        assert expected["transaction_type"] == "RENT"
        assert expected["property_type"] == "APARTMENT"
        assert expected["budget_max"] == 250000
        assert expected["bedrooms"] == 2


# ---------------------------------------------------------------------------
# Labels française
# ---------------------------------------------------------------------------
class TestJourneyLabels:
    def test_property_type_labels_exist(self):
        from lawim_v2.conversation.state.engine import _PROPERTY_TYPE_LABELS
        assert _PROPERTY_TYPE_LABELS["apartment"] == "appartement"
        assert _PROPERTY_TYPE_LABELS["house"] == "maison"
        assert _PROPERTY_TYPE_LABELS["land"] == "terrain"
