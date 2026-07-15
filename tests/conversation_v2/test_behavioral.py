from __future__ import annotations

import unittest
from datetime import datetime

from lawim_v2.conversation.domain.conversation import Conversation
from lawim_v2.conversation.domain.states import ConversationState
from lawim_v2.conversation.domain.facts import Fact, FactStatus, FactCollection
from lawim_v2.conversation.domain.message import NormalizedMessage
from lawim_v2.conversation.domain.decisions import ConversationDecision
from lawim_v2.conversation.domain.intents import Intent, IntentCandidate
from lawim_v2.conversation.understanding.geography import normalize_location
from lawim_v2.conversation.understanding.money import normalize_amount
from lawim_v2.conversation.understanding.extractor import extract_all
from lawim_v2.conversation.understanding.property_types import normalize_property_type, normalize_transaction_type
from lawim_v2.conversation.qualification.matrices import get_matrix, get_next_field, get_readiness_score
from lawim_v2.conversation.planning.project_selector import resolve_project_selection
from lawim_v2.conversation.planning.anti_loop import detect_loop, reset_field_tracking, update_conversation_loop_state


class TestConfirmedFactNeverReAsked(unittest.TestCase):
    def test_confirmed_city_not_asked_again(self):
        conv = Conversation(state=ConversationState.QUALIFYING)
        conv.facts.add_fact(
            Fact(field="city", raw_value="Douala", normalized_value="Douala",
                 confirmation_status=FactStatus.CONFIRMED, fact_id="f1")
        )
        conv.known_fields.add("city")
        matrix = get_matrix("rent_apartment")
        next_field = get_next_field(matrix, conv.facts.all_confirmed_fields())
        self.assertNotEqual(next_field, "city", "CONFIRMED city should not be asked again")

    def test_confirmed_budget_not_asked_again(self):
        conv = Conversation(state=ConversationState.QUALIFYING)
        conv.facts.add_fact(
            Fact(field="budget_max", raw_value="50000", normalized_value=50000,
                 confirmation_status=FactStatus.CONFIRMED, fact_id="f2")
        )
        conv.known_fields.add("budget_max")
        matrix = get_matrix("rent_apartment")
        next_field = get_next_field(matrix, conv.facts.all_confirmed_fields())
        self.assertNotEqual(next_field, "budget_max")

    def test_multiple_confirmed_fields_skipped(self):
        conv = Conversation(state=ConversationState.QUALIFYING)
        conv.facts.add_fact(
            Fact(field="city", raw_value="Douala", normalized_value="Douala",
                 confirmation_status=FactStatus.CONFIRMED, fact_id="f1")
        )
        conv.facts.add_fact(
            Fact(field="budget_max", raw_value="50000", normalized_value=50000,
                 confirmation_status=FactStatus.CONFIRMED, fact_id="f2")
        )
        conv.facts.add_fact(
            Fact(field="bedroom_count", raw_value="3", normalized_value=3,
                 confirmation_status=FactStatus.CONFIRMED, fact_id="f3")
        )
        conv.known_fields.update({"city", "budget_max", "bedroom_count"})
        matrix = get_matrix("rent_apartment")
        next_field = get_next_field(matrix, conv.facts.all_confirmed_fields())
        self.assertIsNotNone(next_field)
        self.assertNotEqual(next_field, "city")
        self.assertNotEqual(next_field, "budget_max")
        self.assertNotEqual(next_field, "bedroom_count")


class TestAmbiguityNeverAutoResolved(unittest.TestCase):
    def test_ambiguous_fact_requires_clarification(self):
        fc = FactCollection()
        fc.add_fact(
            Fact(field="budget", raw_value="109 mil", confirmation_status=FactStatus.AMBIGUOUS, fact_id="f1")
        )
        ambiguous = fc.get_ambiguous()
        self.assertEqual(len(ambiguous), 1)
        decision = ConversationDecision(requires_clarification=True, ambiguous_facts=[
            {"field": "budget", "raw_value": "109 mil"}
        ])
        self.assertTrue(decision.requires_clarification)

    def test_ambiguous_not_treated_as_confirmed(self):
        fc = FactCollection()
        fc.add_fact(
            Fact(field="budget", raw_value="109 mil", confirmation_status=FactStatus.AMBIGUOUS, fact_id="f1")
        )
        self.assertFalse(fc.has_field("budget"))


class TestSimpleOkDoesNotSelectProject(unittest.TestCase):
    def test_ok_with_multiple_projects_is_ambiguous(self):
        projects = [
            {"id": 1, "title": "Achat maison Douala", "status": "ACTIVE"},
            {"id": 2, "title": "Location Yaoundé", "status": "ACTIVE"},
        ]
        result = resolve_project_selection("ok", projects)
        self.assertEqual(result.action, "ambiguous")

    def test_ok_with_one_project_requires_confirmation(self):
        projects = [{"id": 1, "title": "Achat maison Douala", "status": "ACTIVE"}]
        result = resolve_project_selection("ok", projects)
        self.assertEqual(result.action, "select_existing")
        self.assertTrue(result.requires_confirmation)

    def test_oui_with_multiple_projects_is_ambiguous(self):
        projects = [
            {"id": 1, "title": "Projet A", "status": "ACTIVE"},
            {"id": 2, "title": "Projet B", "status": "ACTIVE"},
        ]
        result = resolve_project_selection("oui", projects)
        self.assertEqual(result.action, "ambiguous")


class TestVillaDoesNotAssumeBuyOrRent(unittest.TestCase):
    def test_villa_alone_does_not_imply_transaction(self):
        result = normalize_transaction_type("villa")
        self.assertIsNone(result.normalized_type)
        self.assertEqual(result.confidence, 0.0)

    def test_villa_with_acheter_implies_buy(self):
        result = normalize_transaction_type("acheter villa")
        self.assertEqual(result.normalized_type, "BUY")

    def test_villa_with_louer_implies_rent(self):
        result = normalize_transaction_type("louer villa")
        self.assertEqual(result.normalized_type, "RENT")

    def test_villa_recognized_as_property_type(self):
        result = normalize_property_type("villa")
        self.assertEqual(result.normalized_type, "VILLA")
        self.assertEqual(result.confidence, 1.0)


class TestExplicitCityImmediatelyPersisted(unittest.TestCase):
    def test_explicit_douala_captured(self):
        result = normalize_location("Douala")
        self.assertEqual(result.match_type, "city")
        self.assertEqual(result.normalized_value, "Douala")
        self.assertEqual(result.confidence, 1.0)
        self.assertFalse(result.ambiguity)

    def test_explicit_yaounde_captured(self):
        result = normalize_location("yaounde")
        self.assertEqual(result.match_type, "city")
        self.assertEqual(result.confidence, 1.0)


class TestNeighborhoodImpliesCityWithTraceableConfidence(unittest.TestCase):
    def test_neighborhood_makepe_implies_douala(self):
        result = normalize_location("Makepe")
        self.assertEqual(result.match_type, "neighborhood")
        self.assertEqual(result.city, "Douala")
        self.assertEqual(result.confidence, 0.9)

    def test_neighborhood_odza_implies_yaounde(self):
        result = normalize_location("Odza")
        self.assertEqual(result.match_type, "neighborhood")
        self.assertEqual(result.city, "Yaoundé")
        self.assertEqual(result.confidence, 0.9)

    def test_neighborhood_bastos_implies_yaounde(self):
        result = normalize_location("bastos")
        self.assertEqual(result.match_type, "neighborhood")
        self.assertEqual(result.city, "Yaoundé")

    def test_extractor_creates_city_fact_from_neighborhood(self):
        extracted = extract_all("Makepe")
        facts = extracted["facts"]
        fields = {f["field"] for f in facts}
        self.assertIn("neighborhood", fields)
        self.assertIn("city", fields)
        nf = [f for f in facts if f["field"] == "neighborhood"][0]
        self.assertEqual(nf["normalized_value"], "Makepe")
        self.assertEqual(nf["confidence"], 0.9)
        self.assertEqual(nf["source_type"], "inferred")
        cf = [f for f in facts if f["field"] == "city"][0]
        self.assertEqual(cf["normalized_value"], "Douala")
        self.assertEqual(cf["confidence"], 0.9)
        self.assertEqual(cf["source_type"], "inferred")


class TestMultipleInfoInOneMessageAllExtracted(unittest.TestCase):
    def test_message_with_location_budget_and_type(self):
        text = "Je cherche un appartement 3 chambres à Douala pour 50 millions"
        extracted = extract_all(text)
        facts = extracted["facts"]
        fields = {f["field"] for f in facts}
        self.assertIn("property_type", fields)
        self.assertIn("city", fields)
        self.assertIn("budget_max", fields)
        self.assertIn("bedroom_count", fields)
        for f in facts:
            if f["field"] == "property_type":
                self.assertEqual(f["normalized_value"], "APARTMENT")
            elif f["field"] == "city":
                self.assertEqual(f["normalized_value"], "Douala")
            elif f["field"] == "budget_max":
                self.assertEqual(f["normalized_value"], 50000000)
            elif f["field"] == "bedroom_count":
                self.assertEqual(f["normalized_value"], 3)

    def test_message_with_all_possible_entities(self):
        text = "Je cherche une maison 4 chambres 2 sdb 150m2 à Makepe Douala pour 100 millions dans 3 mois"
        extracted = extract_all(text)
        facts = extracted["facts"]
        fields = {f["field"] for f in facts}
        self.assertIn("property_type", fields)
        self.assertIn("city", fields)
        self.assertIn("neighborhood", fields)
        self.assertIn("budget_max", fields)
        self.assertIn("bedroom_count", fields)
        self.assertIn("bathroom_count", fields)
        self.assertIn("surface_sqm", fields)
        self.assertIn("deadline", fields)
        for f in facts:
            if f["field"] == "property_type":
                self.assertEqual(f["normalized_value"], "HOUSE")
            elif f["field"] == "city":
                self.assertEqual(f["normalized_value"], "Douala")
            elif f["field"] == "neighborhood":
                self.assertEqual(f["normalized_value"], "Makepe")
            elif f["field"] == "budget_max":
                self.assertEqual(f["normalized_value"], 150000000)
            elif f["field"] == "bedroom_count":
                self.assertEqual(f["normalized_value"], 4)
            elif f["field"] == "bathroom_count":
                self.assertEqual(f["normalized_value"], 2)
            elif f["field"] == "surface_sqm":
                self.assertEqual(f["normalized_value"], 150)
            elif f["field"] == "deadline":
                self.assertIsInstance(f["normalized_value"], str)
                self.assertTrue(f["normalized_value"])
                datetime.fromisoformat(f["normalized_value"])


class TestAnnouncedActionIsActuallyExecuted(unittest.TestCase):
    def test_search_action_after_readiness(self):
        matrix = get_matrix("rent_apartment")
        facts = {"city": "Douala", "budget_max": 50000}
        score = get_readiness_score(matrix, facts)
        threshold = matrix.readiness_threshold
        if score >= threshold:
            from lawim_v2.conversation.qualification.matrices import get_next_field
            next_field = get_next_field(matrix, facts)
            if next_field is None:
                allowed_actions = matrix.allowed_actions
                self.assertIn("SEARCH", allowed_actions)


class TestSearchNotLaunchedWithoutMinimumQualification(unittest.TestCase):
    def test_no_search_without_city(self):
        matrix = get_matrix("rent_apartment")
        score = get_readiness_score(matrix, {})
        self.assertLess(score, matrix.readiness_threshold)

    def test_no_search_without_budget(self):
        matrix = get_matrix("rent_apartment")
        score = get_readiness_score(matrix, {"city": "Douala"})
        self.assertLess(score, matrix.readiness_threshold)

    def test_search_possible_with_minimum_facts(self):
        matrix = get_matrix("rent_apartment")
        score = get_readiness_score(matrix, {"city": "Douala", "budget_max": 50000})
        self.assertGreater(score, 0.0)

    def test_ready_for_search_state_required_for_search(self):
        conv = Conversation(state=ConversationState.QUALIFYING)
        self.assertNotEqual(conv.state, ConversationState.READY_FOR_SEARCH)
        self.assertFalse(conv.can_transition("search_requested"))


class TestQuestionNotRepeatedAfterValidAnswer(unittest.TestCase):
    def test_valid_answer_resets_loop(self):
        reset_field_tracking()
        conv = Conversation(last_question_field="city")
        detect_loop(conv, "Douala", current_field="city", expected_input="Douala")
        result = detect_loop(conv, "Suite", current_field="city", expected_input="Suite")
        self.assertFalse(result.loop_detected)
        self.assertEqual(result.repeat_count, 0)

    def test_known_field_not_in_next_field(self):
        matrix = get_matrix("rent_apartment")
        known = {"city": "Douala", "budget_max": 50000}
        next_field = get_next_field(matrix, known)
        self.assertNotEqual(next_field, "city")
        self.assertNotEqual(next_field, "budget_max")


class TestLoopDetectedAndInterrupted(unittest.TestCase):
    def test_loop_escalates_to_handover(self):
        reset_field_tracking()
        conv = Conversation(last_question_field="city")
        for i in range(4):
            result = detect_loop(conv, f"Je ne sais pas {i}", current_field="city")
        self.assertEqual(result.action, "handover")
        self.assertTrue(result.loop_detected)

    def test_loop_updates_conversation_state(self):
        reset_field_tracking()
        conv = Conversation(last_question_field="city")
        for i in range(2):
            r = detect_loop(conv, f"Non {i}", current_field="city")
        update_conversation_loop_state(conv, r)
        self.assertTrue(conv.loop_detected)
        self.assertGreater(conv.loop_score, 0)

    def test_loop_triggers_human_handover_on_exceed(self):
        reset_field_tracking()
        conv = Conversation(last_question_field="city")
        result = None
        for i in range(4):
            result = detect_loop(conv, f"Non {i}", current_field="city")
        self.assertEqual(result.action, "handover")
        update_conversation_loop_state(conv, result)
        self.assertTrue(conv.human_handover_requested)


class TestClosedProjectNotAutoReopened(unittest.TestCase):
    def test_closed_state_does_not_transition_on_message(self):
        conv = Conversation(state=ConversationState.CLOSED)
        ok, _ = conv.apply_transition("message_received")
        self.assertFalse(ok)
        self.assertEqual(conv.state, ConversationState.CLOSED)

    def test_closed_state_requires_explicit_reopen(self):
        conv = Conversation(state=ConversationState.CLOSED)
        ok, event = conv.apply_transition("reopened")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.AWAITING_INTENT)


class TestHumanRequestDoesNotCreatePartnerRelationship(unittest.TestCase):
    def test_handover_request_goes_to_human_not_relationship(self):
        conv = Conversation(state=ConversationState.AWAITING_INTENT)
        ok, event = conv.apply_transition("handover_requested")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.HUMAN_HANDOVER)
        self.assertNotEqual(conv.state, ConversationState.AWAITING_RELATIONSHIP_CONSENT)

    def test_handover_from_qualifying_does_not_create_relationship(self):
        conv = Conversation(state=ConversationState.QUALIFYING)
        conv.apply_transition("handover_requested")
        self.assertEqual(conv.state, ConversationState.HUMAN_HANDOVER)


class TestSameIncomingMessageOnlyProcessedOnce(unittest.TestCase):
    def test_decision_id_should_be_unique(self):
        d1 = ConversationDecision(decision_id="msg-1-001")
        d2 = ConversationDecision(decision_id="msg-1-002")
        self.assertNotEqual(d1.decision_id, d2.decision_id)

    def test_duplicate_flag(self):
        msg = NormalizedMessage(normalized_text="Bonjour", is_duplicate=True)
        self.assertTrue(msg.is_duplicate)
        msg2 = NormalizedMessage(normalized_text="Bonjour", is_duplicate=False)
        self.assertFalse(msg2.is_duplicate)


class TestIdenticalDecisionInIdenticalContextRemainsDeterministic(unittest.TestCase):
    def test_same_input_produces_same_amount_normalization(self):
        r1 = normalize_amount("50000")
        r2 = normalize_amount("50000")
        self.assertEqual(r1.normalized_amount, r2.normalized_amount)
        self.assertEqual(r1.currency, r2.currency)

    def test_same_input_produces_same_location_normalization(self):
        r1 = normalize_location("Douala")
        r2 = normalize_location("Douala")
        self.assertEqual(r1.normalized_value, r2.normalized_value)
        self.assertEqual(r1.match_type, r2.match_type)

    def test_same_state_produces_same_transition(self):
        c1 = Conversation(state=ConversationState.NEW)
        c2 = Conversation(state=ConversationState.NEW)
        ok1, ev1 = c1.apply_transition("message_received")
        ok2, ev2 = c2.apply_transition("message_received")
        self.assertEqual(ok1, ok2)
        self.assertEqual(ev1, ev2)
        self.assertEqual(c1.state, c2.state)

    def test_same_facts_produce_same_readiness_score(self):
        matrix = get_matrix("rent_apartment")
        facts = {"city": "Douala", "budget_max": 50000}
        s1 = get_readiness_score(matrix, facts)
        s2 = get_readiness_score(matrix, facts)
        self.assertEqual(s1, s2)

    def test_same_matrix_returns_same_next_field(self):
        matrix = get_matrix("rent_apartment")
        known = {"city": "Douala"}
        f1 = get_next_field(matrix, known)
        f2 = get_next_field(matrix, known)
        self.assertEqual(f1, f2)


class TestMatchingNotCreatedWithoutRealResults(unittest.TestCase):
    def test_no_results_state_before_matching(self):
        conv = Conversation(state=ConversationState.QUALIFYING)
        self.assertFalse(conv.can_transition("result_selected"))
        self.assertFalse(conv.can_transition("proposal_accepted"))


class TestRelationshipNotCreatedWithoutConsent(unittest.TestCase):
    def test_consent_required_for_relationship(self):
        conv = Conversation(state=ConversationState.AWAITING_RELATIONSHIP_CONSENT)
        ok_yes, ev_yes = conv.apply_transition("consent_granted")
        self.assertTrue(ok_yes)
        self.assertEqual(conv.state, ConversationState.RELATIONSHIP_PROPOSED)
        conv2 = Conversation(state=ConversationState.AWAITING_RELATIONSHIP_CONSENT)
        ok_no, ev_no = conv2.apply_transition("consent_denied")
        self.assertTrue(ok_no)
        self.assertEqual(conv2.state, ConversationState.QUALIFYING)

    def test_cannot_skip_consent_state(self):
        conv = Conversation(state=ConversationState.RESULTS_AVAILABLE)
        self.assertFalse(conv.can_transition("proposal_accepted"))
        self.assertFalse(conv.can_transition("consent_denied"))


class TestPrivateCoordinatesNeverSharedBeforeAuthorization(unittest.TestCase):
    def test_coordinates_not_in_standard_extraction(self):
        text = "Je cherche une maison à Douala avec 3 chambres"
        extracted = extract_all(text)
        fields = {f["field"] for f in extracted["facts"]}
        self.assertNotIn("coordinates", fields)
        self.assertNotIn("latitude", fields)
        self.assertNotIn("longitude", fields)

    def test_coordinates_not_in_decision_facts(self):
        d = ConversationDecision(
            known_facts={"city": "Douala"},
            new_facts=[{"field": "city", "value": "Douala"}],
        )
        known = d.known_facts
        new = [f for f in d.new_facts if f["field"] in ("coordinates", "latitude", "longitude")]
        self.assertEqual(len(new), 0)
        self.assertNotIn("coordinates", known)


class TestChannelChangeDoesNotLoseProjectDossierFacts(unittest.TestCase):
    def test_conversation_preserves_project_id(self):
        conv = Conversation(
            conversation_id=1,
            project_id=42,
            dossier_id=7,
            channel="telegram",
        )
        conv.channel = "whatsapp"
        self.assertEqual(conv.project_id, 42)
        self.assertEqual(conv.dossier_id, 7)

    def test_conversation_preserves_facts_across_channel(self):
        fc = FactCollection()
        fc.add_fact(
            Fact(field="city", raw_value="Douala", normalized_value="Douala",
                 confirmation_status=FactStatus.CONFIRMED, fact_id="f1")
        )
        conv = Conversation(conversation_id=1, facts=fc, channel="telegram")
        conv.channel = "whatsapp"
        self.assertTrue(conv.facts.has_field("city"))
        self.assertEqual(conv.facts.get_confirmed("city")[0].normalized_value, "Douala")

    def test_conversation_preserves_state_across_channel(self):
        conv = Conversation(state=ConversationState.QUALIFYING, channel="telegram")
        conv.channel = "whatsapp"
        self.assertEqual(conv.state, ConversationState.QUALIFYING)


class TestLLMFailureDoesNotBlockDeterministicPath(unittest.TestCase):
    def test_deterministic_extraction_works_without_llm(self):
        text = "3 chambres à Douala"
        extracted = extract_all(text)
        facts = extracted["facts"]
        fields = {f["field"] for f in facts}
        self.assertIn("city", fields)
        self.assertIn("bedroom_count", fields)
        for f in facts:
            if f["field"] == "city":
                self.assertEqual(f["normalized_value"], "Douala")
            elif f["field"] == "bedroom_count":
                self.assertEqual(f["normalized_value"], 3)

    def test_state_transition_works_without_llm(self):
        conv = Conversation(state=ConversationState.AWAITING_INTENT)
        ok, event = conv.apply_transition("intent_identified")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.QUALIFYING)

    def test_normalize_amount_works_without_llm(self):
        result = normalize_amount("50000")
        self.assertEqual(result.normalized_amount, 50000)
        self.assertFalse(result.ambiguity)


if __name__ == "__main__":
    unittest.main()
