from __future__ import annotations

import unittest

from lawim_v2.conversation.domain.states import (
    ConversationState,
    StateTransition,
    STATE_TRANSITIONS,
)


class TestStateTransitions(unittest.TestCase):
    def test_transition_new_to_awaiting_intent(self):
        conv = _make_conversation(ConversationState.NEW)
        ok, event = conv.apply_transition("message_received")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.AWAITING_INTENT)
        self.assertEqual(event, "conversation.started")

    def test_transition_new_to_awaiting_project_selection(self):
        conv = _make_conversation(ConversationState.NEW)
        ok, event = conv.apply_transition("user_identified")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.AWAITING_PROJECT_SELECTION)
        self.assertEqual(event, "user.identified")

    def test_transition_awaiting_project_selection_project_selected(self):
        conv = _make_conversation(ConversationState.AWAITING_PROJECT_SELECTION)
        ok, event = conv.apply_transition("project_selected")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.AWAITING_INTENT)
        self.assertEqual(event, "project.selected")

    def test_transition_awaiting_project_selection_new_project(self):
        conv = _make_conversation(ConversationState.AWAITING_PROJECT_SELECTION)
        ok, event = conv.apply_transition("new_project_requested")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.AWAITING_INTENT)
        self.assertEqual(event, "project.created")

    def test_transition_awaiting_project_selection_ambiguous(self):
        conv = _make_conversation(ConversationState.AWAITING_PROJECT_SELECTION)
        ok, event = conv.apply_transition("ambiguity_detected")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.AWAITING_PROJECT_SELECTION)
        self.assertEqual(event, "project.selection.ambiguous")

    def test_transition_awaiting_intent_to_qualifying(self):
        conv = _make_conversation(ConversationState.AWAITING_INTENT)
        ok, event = conv.apply_transition("intent_identified")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.QUALIFYING)
        self.assertEqual(event, "intent.identified")

    def test_transition_awaiting_intent_ambiguous(self):
        conv = _make_conversation(ConversationState.AWAITING_INTENT)
        ok, event = conv.apply_transition("ambiguity_detected")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.AWAITING_INTENT)

    def test_transition_qualifying_fact_confirmed(self):
        conv = _make_conversation(ConversationState.QUALIFYING)
        ok, event = conv.apply_transition("fact_confirmed")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.QUALIFYING)
        self.assertEqual(event, "fact.confirmed")

    def test_transition_qualifying_fact_ambiguous(self):
        conv = _make_conversation(ConversationState.QUALIFYING)
        ok, event = conv.apply_transition("fact_ambiguous")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.AWAITING_CLARIFICATION)
        self.assertEqual(event, "fact.ambiguous")

    def test_transition_qualifying_clarification_provided(self):
        conv = _make_conversation(ConversationState.QUALIFYING)
        ok, event = conv.apply_transition("clarification_provided")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.QUALIFYING)
        self.assertEqual(event, "clarification.provided")

    def test_transition_qualifying_minimum_readiness(self):
        conv = _make_conversation(ConversationState.QUALIFYING)
        ok, event = conv.apply_transition("minimum_readiness")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.READY_FOR_SEARCH)
        self.assertEqual(event, "qualification.minimum_ready")

    def test_transition_awaiting_clarification_clarification_provided(self):
        conv = _make_conversation(ConversationState.AWAITING_CLARIFICATION)
        ok, event = conv.apply_transition("clarification_provided")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.QUALIFYING)
        self.assertEqual(event, "clarification.resolved")

    def test_transition_awaiting_clarification_loop_detected(self):
        conv = _make_conversation(ConversationState.AWAITING_CLARIFICATION)
        ok, event = conv.apply_transition("loop_detected")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.AWAITING_CLARIFICATION)

    def test_transition_awaiting_clarification_loop_exceeded(self):
        conv = _make_conversation(ConversationState.AWAITING_CLARIFICATION)
        ok, event = conv.apply_transition("loop_exceeded")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.HUMAN_HANDOVER)

    def test_transition_ready_for_search_to_searching(self):
        conv = _make_conversation(ConversationState.READY_FOR_SEARCH)
        ok, event = conv.apply_transition("search_requested")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.SEARCHING)
        self.assertEqual(event, "search.requested")

    def test_transition_searching_results_available(self):
        conv = _make_conversation(ConversationState.SEARCHING)
        ok, event = conv.apply_transition("results_available")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.RESULTS_AVAILABLE)

    def test_transition_searching_zero_results(self):
        conv = _make_conversation(ConversationState.SEARCHING)
        ok, event = conv.apply_transition("zero_results")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.QUALIFYING)

    def test_transition_results_selected_to_awaiting_consent(self):
        conv = _make_conversation(ConversationState.RESULTS_AVAILABLE)
        ok, event = conv.apply_transition("result_selected")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.AWAITING_RELATIONSHIP_CONSENT)
        self.assertEqual(event, "match.selected")

    def test_transition_results_dismissed_to_qualifying(self):
        conv = _make_conversation(ConversationState.RESULTS_AVAILABLE)
        ok, event = conv.apply_transition("result_dismissed")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.QUALIFYING)

    def test_transition_consent_granted(self):
        conv = _make_conversation(ConversationState.AWAITING_RELATIONSHIP_CONSENT)
        ok, event = conv.apply_transition("consent_granted")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.RELATIONSHIP_PROPOSED)
        self.assertEqual(event, "consent.granted")

    def test_transition_consent_denied(self):
        conv = _make_conversation(ConversationState.AWAITING_RELATIONSHIP_CONSENT)
        ok, event = conv.apply_transition("consent_denied")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.QUALIFYING)
        self.assertEqual(event, "consent.denied")

    def test_transition_proposal_accepted(self):
        conv = _make_conversation(ConversationState.RELATIONSHIP_PROPOSED)
        ok, event = conv.apply_transition("proposal_accepted")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.RELATIONSHIP_ACTIVE)
        self.assertEqual(event, "relationship.created")

    def test_transition_proposal_rejected(self):
        conv = _make_conversation(ConversationState.RELATIONSHIP_PROPOSED)
        ok, event = conv.apply_transition("proposal_rejected")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.QUALIFYING)
        self.assertEqual(event, "relationship.rejected")

    def test_transition_visit_requested(self):
        conv = _make_conversation(ConversationState.RELATIONSHIP_ACTIVE)
        ok, event = conv.apply_transition("visit_requested")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.VISIT_PENDING)

    def test_transition_visit_confirmed(self):
        conv = _make_conversation(ConversationState.VISIT_PENDING)
        ok, event = conv.apply_transition("visit_confirmed")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.VISIT_CONFIRMED)

    def test_transition_visit_completed(self):
        conv = _make_conversation(ConversationState.VISIT_CONFIRMED)
        ok, event = conv.apply_transition("visit_completed")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.VISIT_COMPLETED)

    def test_transition_follow_up_needed(self):
        conv = _make_conversation(ConversationState.VISIT_COMPLETED)
        ok, event = conv.apply_transition("follow_up_needed")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.FOLLOW_UP)

    def test_transition_all_complete_to_closed(self):
        conv = _make_conversation(ConversationState.FOLLOW_UP)
        ok, event = conv.apply_transition("all_complete")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.CLOSED)

    def test_transition_handover_resolved(self):
        conv = _make_conversation(ConversationState.HUMAN_HANDOVER)
        ok, event = conv.apply_transition("resolved")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.QUALIFYING)

    def test_transition_error_recover(self):
        conv = _make_conversation(ConversationState.ERROR)
        ok, event = conv.apply_transition("recover")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.QUALIFYING)

    def test_transition_closed_reopened(self):
        conv = _make_conversation(ConversationState.CLOSED)
        ok, event = conv.apply_transition("reopened")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.AWAITING_INTENT)

    def test_transition_handover_from_any_state(self):
        handover_sources = [
            ConversationState.NEW,
            ConversationState.AWAITING_PROJECT_SELECTION,
            ConversationState.AWAITING_INTENT,
            ConversationState.QUALIFYING,
            ConversationState.AWAITING_CLARIFICATION,
            ConversationState.READY_FOR_SEARCH,
            ConversationState.SEARCHING,
            ConversationState.RESULTS_AVAILABLE,
            ConversationState.AWAITING_RESULT_SELECTION,
            ConversationState.AWAITING_RELATIONSHIP_CONSENT,
            ConversationState.RELATIONSHIP_PROPOSED,
            ConversationState.RELATIONSHIP_PENDING,
            ConversationState.VISIT_PENDING,
            ConversationState.VISIT_CONFIRMED,
            ConversationState.VISIT_COMPLETED,
            ConversationState.FOLLOW_UP,
        ]
        for state in handover_sources:
            conv = _make_conversation(state)
            ok, event = conv.apply_transition("handover_requested")
            self.assertTrue(ok, f"handover_requested should work from {state}")
            self.assertEqual(conv.state, ConversationState.HUMAN_HANDOVER, f"from {state}")
            self.assertEqual(event, "handover.requested")

    def test_invalid_transition_returns_false(self):
        conv = _make_conversation(ConversationState.NEW)
        ok, _ = conv.apply_transition("intent_identified")
        self.assertFalse(ok)
        self.assertEqual(conv.state, ConversationState.NEW)

    def test_invalid_transition_does_not_change_state(self):
        conv = _make_conversation(ConversationState.CLOSED)
        ok, _ = conv.apply_transition("message_received")
        self.assertFalse(ok)
        self.assertEqual(conv.state, ConversationState.CLOSED)

    def test_can_transition_positive(self):
        conv = _make_conversation(ConversationState.NEW)
        self.assertTrue(conv.can_transition("message_received"))
        self.assertTrue(conv.can_transition("user_identified"))

    def test_can_transition_negative(self):
        conv = _make_conversation(ConversationState.CLOSED)
        self.assertFalse(conv.can_transition("message_received"))

    def test_get_expected_next_events_from_new(self):
        conv = _make_conversation(ConversationState.NEW)
        events = conv.gets_expected_next_events()
        self.assertIn("message_received", events)
        self.assertIn("user_identified", events)

    def test_all_states_represented(self):
        states_with_transitions = {t.source for t in STATE_TRANSITIONS}
        all_states = set(ConversationState)
        unreachable = all_states - states_with_transitions - {ConversationState.HUMAN_HANDOVER}
        self.assertEqual(
            unreachable, set(),
            f"Every state should be reachable as a source, missing: {unreachable}",
        )

    def test_every_transition_has_audit_event(self):
        for t in STATE_TRANSITIONS:
            self.assertIsNotNone(t.audit_event, f"Transition {t.source}->{t.event} missing audit_event")
            self.assertIsInstance(t.audit_event, str)
            self.assertTrue(len(t.audit_event) > 0)

    def test_state_transition_immutable_properties(self):
        t = STATE_TRANSITIONS[0]
        self.assertIsInstance(t.source, ConversationState)
        self.assertIsInstance(t.event, str)
        self.assertIsInstance(t.destination, ConversationState)
        self.assertIn(t.destination, list(ConversationState))

    def test_guard_condition_present_on_some_transitions(self):
        guards_found = [t for t in STATE_TRANSITIONS if t.guard is not None]
        guard_events = {t.event for t in guards_found}
        self.assertIn("user_identified", guard_events)
        self.assertIn("fact_confirmed", guard_events)
        self.assertIn("loop_detected", guard_events)
        self.assertIn("zero_results", guard_events)

    def test_can_transition_returns_false_for_event_on_wrong_state(self):
        conv = _make_conversation(ConversationState.CLOSED)
        self.assertFalse(conv.can_transition("handover_requested"))

    def test_handover_transitions_have_correct_audit_event(self):
        for t in STATE_TRANSITIONS:
            if t.event == "handover_requested":
                self.assertEqual(t.audit_event, "handover.requested")

    def test_qualifying_to_clarification_preserves_state_on_loop(self):
        conv = _make_conversation(ConversationState.AWAITING_CLARIFICATION)
        ok, _ = conv.apply_transition("loop_detected")
        self.assertTrue(ok)
        self.assertEqual(conv.state, ConversationState.AWAITING_CLARIFICATION)


def _make_conversation(state: ConversationState):
    from lawim_v2.conversation.domain.conversation import Conversation
    return Conversation(state=state)


if __name__ == "__main__":
    unittest.main()
