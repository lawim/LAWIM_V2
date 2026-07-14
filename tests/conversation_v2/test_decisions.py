from __future__ import annotations

import unittest
from datetime import datetime

from lawim_v2.conversation.domain.decisions import ConversationDecision
from lawim_v2.conversation.domain.states import ConversationState


class TestConversationDecision(unittest.TestCase):
    def test_create_decision_with_defaults(self):
        d = ConversationDecision()
        self.assertEqual(d.decision_id, "")
        self.assertIsNone(d.conversation_id)
        self.assertIsNone(d.user_id)
        self.assertEqual(d.channel, "")
        self.assertIsNone(d.state_before)
        self.assertIsNone(d.state_after)
        self.assertEqual(d.known_facts, {})
        self.assertEqual(d.new_facts, [])
        self.assertEqual(d.ambiguous_facts, [])
        self.assertEqual(d.loop_score, 0)
        self.assertFalse(d.loop_detected)
        self.assertFalse(d.requires_clarification)
        self.assertFalse(d.requires_human)

    def test_decision_with_states(self):
        d = ConversationDecision(
            conversation_id=1,
            user_id=42,
            channel="telegram",
            project_id=5,
            dossier_id=10,
            normalized_message="Je cherche un appartement",
            state_before=ConversationState.AWAITING_INTENT,
            state_after=ConversationState.QUALIFYING,
            selected_intent="rent_apartment",
            intent_confidence=0.85,
            transaction_type="RENT",
            property_type="APARTMENT",
        )
        self.assertEqual(d.conversation_id, 1)
        self.assertEqual(d.user_id, 42)
        self.assertEqual(d.channel, "telegram")
        self.assertEqual(d.project_id, 5)
        self.assertEqual(d.dossier_id, 10)
        self.assertEqual(d.normalized_message, "Je cherche un appartement")
        self.assertEqual(d.state_before, ConversationState.AWAITING_INTENT)
        self.assertEqual(d.state_after, ConversationState.QUALIFYING)
        self.assertEqual(d.selected_intent, "rent_apartment")
        self.assertEqual(d.intent_confidence, 0.85)
        self.assertEqual(d.transaction_type, "RENT")
        self.assertEqual(d.property_type, "APARTMENT")

    def test_to_dict_serialization(self):
        d = ConversationDecision(
            decision_id="dec-1",
            conversation_id=1,
            user_id=42,
            channel="whatsapp",
            project_id=5,
            dossier_id=10,
            normalized_message="bonjour",
            state_before=ConversationState.NEW,
            state_after=ConversationState.AWAITING_INTENT,
            selected_intent="greeting",
            intent_confidence=1.0,
            transaction_type=None,
            property_type=None,
            known_facts={"city": "Douala"},
            new_facts=[{"field": "city", "value": "Douala"}],
            ambiguous_facts=[],
            conflicting_facts=[],
            missing_required_facts=["budget"],
            expected_input="city",
            business_goal="qualify",
            action="ask_city",
            action_parameters={"field": "city"},
            action_status="pending",
            allowed_capabilities=["search", "match"],
            forbidden_capabilities=["handover"],
            response_type="question",
            response_constraints=["no_markdown"],
            requires_clarification=False,
            requires_human=False,
            loop_detected=False,
            loop_score=0,
            created_at="2025-01-01T00:00:00",
        )
        dumped = d.to_dict()
        self.assertEqual(dumped["decision_id"], "dec-1")
        self.assertEqual(dumped["conversation_id"], 1)
        self.assertEqual(dumped["user_id"], 42)
        self.assertEqual(dumped["channel"], "whatsapp")
        self.assertEqual(dumped["project_id"], 5)
        self.assertEqual(dumped["dossier_id"], 10)
        self.assertEqual(dumped["normalized_message"], "bonjour")
        self.assertEqual(dumped["state_before"], "NEW")
        self.assertEqual(dumped["state_after"], "AWAITING_INTENT")
        self.assertEqual(dumped["selected_intent"], "greeting")
        self.assertEqual(dumped["intent_confidence"], 1.0)
        self.assertIsNone(dumped["transaction_type"])
        self.assertIsNone(dumped["property_type"])
        self.assertEqual(dumped["known_facts"], {"city": "Douala"})
        self.assertEqual(dumped["new_facts"], [{"field": "city", "value": "Douala"}])
        self.assertEqual(dumped["missing_required_facts"], ["budget"])
        self.assertEqual(dumped["expected_input"], "city")
        self.assertEqual(dumped["action"], "ask_city")
        self.assertEqual(dumped["action_parameters"], {"field": "city"})
        self.assertEqual(dumped["action_status"], "pending")
        self.assertEqual(dumped["requires_clarification"], False)
        self.assertEqual(dumped["requires_human"], False)
        self.assertEqual(dumped["loop_detected"], False)
        self.assertEqual(dumped["loop_score"], 0)
        self.assertEqual(dumped["created_at"], "2025-01-01T00:00:00")

    def test_to_dict_with_none_state_before(self):
        d = ConversationDecision()
        dumped = d.to_dict()
        self.assertIsNone(dumped["state_before"])
        self.assertIsNone(dumped["state_after"])

    def test_with_facts_populated(self):
        d = ConversationDecision(
            known_facts={"city": "Douala", "budget_max": 50000},
            new_facts=[{"field": "bedroom_count", "value": 3}],
            ambiguous_facts=[{"field": "budget", "raw_value": "109 mil"}],
            conflicting_facts=[{"field": "city", "value": "Yaoundé"}],
            missing_required_facts=["surface_sqm"],
        )
        self.assertEqual(d.known_facts["city"], "Douala")
        self.assertEqual(len(d.new_facts), 1)
        self.assertEqual(len(d.ambiguous_facts), 1)
        self.assertEqual(len(d.conflicting_facts), 1)
        self.assertEqual(d.missing_required_facts, ["surface_sqm"])

    def test_loop_detection_fields(self):
        d = ConversationDecision(
            loop_detected=True,
            loop_score=45,
        )
        self.assertTrue(d.loop_detected)
        self.assertEqual(d.loop_score, 45)

    def test_action_fields(self):
        d = ConversationDecision(
            action="start_search",
            action_parameters={"criteria": {"city": "Douala"}},
            action_status="completed",
        )
        self.assertEqual(d.action, "start_search")
        self.assertEqual(d.action_parameters["criteria"]["city"], "Douala")
        self.assertEqual(d.action_status, "completed")

    def test_capability_fields(self):
        d = ConversationDecision(
            allowed_capabilities=["search", "match", "visit"],
            forbidden_capabilities=["handover"],
        )
        self.assertIn("search", d.allowed_capabilities)
        self.assertIn("handover", d.forbidden_capabilities)

    def test_response_fields(self):
        d = ConversationDecision(
            response_type="question",
            response_constraints=["no_markdown", "keep_it_short"],
        )
        self.assertEqual(d.response_type, "question")
        self.assertEqual(len(d.response_constraints), 2)

    def test_decision_requires_clarification(self):
        d = ConversationDecision(requires_clarification=True)
        self.assertTrue(d.to_dict()["requires_clarification"])

    def test_decision_requires_human(self):
        d = ConversationDecision(requires_human=True)
        self.assertTrue(d.to_dict()["requires_human"])

    def test_to_dict_does_not_include_decision_id_typo(self):
        d = ConversationDecision(decision_id="test-1")
        dumped = d.to_dict()
        self.assertIn("decision_id", dumped)
        self.assertEqual(dumped["decision_id"], "test-1")


if __name__ == "__main__":
    unittest.main()
