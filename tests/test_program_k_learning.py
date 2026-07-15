# Program K — Learning Machine Foundation Tests
from __future__ import annotations

import json
import unittest
from datetime import datetime, timezone

from lawim_v2.program_k import (
    FeedbackItem,
    FeedbackOrigin,
    FeedbackTarget,
    LearningConfig,
    LearningEvent,
    LearningEventSource,
    LearningEventType,
    LearningValidationService,
    OutcomeResult,
    OutcomeStatus,
    learning_event_registry,
    outcome_registry,
)
from lawim_v2.program_k.learning_services import (
    FeedbackService,
    LearningEventService,
    OutcomeRegistryService,
)

# ── Setup ─────────────────────────────────────────────────────────────────


def setUpModule():
    learning_event_registry.clear()
    outcome_registry.clear()


def tearDownModule():
    learning_event_registry.clear()
    outcome_registry.clear()


# ── Learning Event Model Tests ────────────────────────────────────────────


class LearningEventModelTest(unittest.TestCase):
    def test_create_h_event(self):
        event = LearningEvent(event_type=LearningEventType.H_QUALIFICATION_STARTED,
                               source=LearningEventSource.PROGRAM_H,
                               actor_id="actor1", conversation_id="conv1")
        self.assertEqual(event.source, LearningEventSource.PROGRAM_H)
        self.assertEqual(event.actor_id, "actor1")

    def test_create_j_event(self):
        event = LearningEvent(event_type=LearningEventType.J_CONVERSATION_STARTED,
                               source=LearningEventSource.PROGRAM_J,
                               channel="whatsapp", correlation_id="corr1")
        self.assertEqual(event.source, LearningEventSource.PROGRAM_J)
        self.assertEqual(event.channel, "whatsapp")

    def test_to_dict(self):
        event = LearningEvent(event_type=LearningEventType.J_REDIRECT_RECORDED,
                               source=LearningEventSource.PROGRAM_J,
                               actor_id="a1", event_id="e1")
        d = event.to_dict()
        self.assertEqual(d["event_id"], "e1")
        self.assertEqual(d["event_type"], "J_REDIRECT_RECORDED")

    def test_anonymize_removes_sensitive(self):
        event = LearningEvent(event_type=LearningEventType.J_CONVERSATION_MESSAGE,
                               source=LearningEventSource.PROGRAM_J,
                               payload={"phone": "+237600000000", "email": "test@test.com",
                                         "raw_text": "Bonjour", "normalized_text": "hello"})
        anon = event.anonymize()
        self.assertNotIn("phone", anon.payload)
        self.assertNotIn("email", anon.payload)
        self.assertIn("normalized_text", anon.payload)

    def test_event_version_default(self):
        event = LearningEvent()
        self.assertEqual(event.event_version, "1.0")

    def test_confidence_default(self):
        event = LearningEvent()
        self.assertEqual(event.confidence, 1.0)

    def test_h_event_types_exist(self):
        self.assertIsNotNone(LearningEventType.H_QUALIFICATION_STARTED)
        self.assertIsNotNone(LearningEventType.H_QUALIFICATION_COMPLETED)
        self.assertIsNotNone(LearningEventType.H_QUALIFICATION_ESCALATED)

    def test_j_event_types_exist(self):
        self.assertIsNotNone(LearningEventType.J_CONVERSATION_STARTED)
        self.assertIsNotNone(LearningEventType.J_CONVERSION_RECORDED)
        self.assertIsNotNone(LearningEventType.J_PAYMENT_CONFIRMED)

    def test_outcome_event_type(self):
        self.assertEqual(LearningEventType.OUTCOME_RECORDED.value, "OUTCOME_RECORDED")

    def test_feedback_event_type(self):
        self.assertEqual(LearningEventType.FEEDBACK_RECEIVED.value, "FEEDBACK_RECEIVED")


# ── Outcome Model Tests ────────────────────────────────────────────────────


class OutcomeModelTest(unittest.TestCase):
    def test_success_status(self):
        o = OutcomeResult(outcome_id="o1", outcome_type="qualification",
                           status=OutcomeStatus.SUCCESS)
        self.assertEqual(o.status, OutcomeStatus.SUCCESS)

    def test_failure_status(self):
        o = OutcomeResult(outcome_id="o2", outcome_type="matching",
                           status=OutcomeStatus.FAILURE)
        self.assertEqual(o.status, OutcomeStatus.FAILURE)

    def test_abandoned_status(self):
        o = OutcomeResult(outcome_id="o3", outcome_type="visit",
                           status=OutcomeStatus.ABANDONED)
        self.assertEqual(o.status, OutcomeStatus.ABANDONED)

    def test_to_dict(self):
        o = OutcomeResult(outcome_id="o1", outcome_type="payment",
                           status=OutcomeStatus.SUCCESS, monetary_value=500000)
        d = o.to_dict()
        self.assertEqual(d["outcome_type"], "payment")
        self.assertEqual(d["monetary_value"], 500000)

    def test_satisfaction_score(self):
        o = OutcomeResult(outcome_id="o1", outcome_type="conversation",
                           status=OutcomeStatus.SUCCESS, satisfaction_score=8.5)
        self.assertEqual(o.satisfaction_score, 8.5)

    def test_tracking_code(self):
        o = OutcomeResult(outcome_id="o1", outcome_type="conversion",
                           tracking_code="FB-LAWIM-000001-2026-06-001")
        self.assertEqual(o.tracking_code, "FB-LAWIM-000001-2026-06-001")

    def test_campaign_and_publication(self):
        o = OutcomeResult(outcome_id="o1", outcome_type="conversion",
                           campaign_id="c1", publication_id="p1")
        self.assertEqual(o.campaign_id, "c1")
        self.assertEqual(o.publication_id, "p1")


# ── Feedback Model Tests ──────────────────────────────────────────────────


class FeedbackModelTest(unittest.TestCase):
    def test_create_user_feedback(self):
        f = FeedbackItem(feedback_id="f1", origin=FeedbackOrigin.USER,
                          target=FeedbackTarget.AI_RESPONSE, score=8.0)
        self.assertEqual(f.origin, FeedbackOrigin.USER)
        self.assertEqual(f.score, 8.0)

    def test_create_satisfaction(self):
        f = FeedbackItem(feedback_id="f2", origin=FeedbackOrigin.SATISFACTION_SURVEY,
                          target=FeedbackTarget.CONVERSATION, score=9.0)
        self.assertEqual(f.origin, FeedbackOrigin.SATISFACTION_SURVEY)

    def test_create_matching_feedback(self):
        f = FeedbackItem(feedback_id="f3", origin=FeedbackOrigin.MATCHING,
                          target=FeedbackTarget.MATCHING_RESULT, score=7.5)
        self.assertEqual(f.origin, FeedbackOrigin.MATCHING)

    def test_normalized_score(self):
        f = FeedbackItem(feedback_id="f1", score=8.0, min_score=0.0, max_score=10.0)
        self.assertEqual(f.normalized_score(), 0.8)

    def test_normalized_score_min_max(self):
        f = FeedbackItem(feedback_id="f1", score=5.0, min_score=1.0, max_score=5.0)
        self.assertEqual(f.normalized_score(), 1.0)

    def test_normalized_score_equal(self):
        f = FeedbackItem(feedback_id="f1", score=5.0, min_score=5.0, max_score=5.0)
        self.assertEqual(f.normalized_score(), 0.5)

    def test_to_dict(self):
        f = FeedbackItem(feedback_id="f1", origin=FeedbackOrigin.USER,
                          target=FeedbackTarget.PROPERTY, score=7.0)
        d = f.to_dict()
        self.assertEqual(d["target"], "PROPERTY")

    def test_confidence_default(self):
        f = FeedbackItem(feedback_id="f1", score=5.0)
        self.assertEqual(f.confidence, 1.0)

    def test_with_comment(self):
        f = FeedbackItem(feedback_id="f1", score=5.0, comment="Très satisfait")
        self.assertEqual(f.comment, "Très satisfait")

    def test_all_origins(self):
        for origin in FeedbackOrigin:
            f = FeedbackItem(feedback_id="t", origin=origin, score=5.0)
            self.assertEqual(f.origin, origin)

    def test_all_targets(self):
        for target in FeedbackTarget:
            f = FeedbackItem(feedback_id="t", target=target, score=5.0)
            self.assertEqual(f.target, target)


# ── LearningEventService Tests ────────────────────────────────────────────


class LearningEventServiceTest(unittest.TestCase):
    def setUp(self):
        self.svc = LearningEventService()
        learning_event_registry.clear()

    def test_record_h_event(self):
        event = self.svc.record_h_event(LearningEventType.H_QUALIFICATION_STARTED,
                                         actor_id="a1", conversation_id="c1")
        self.assertIsNotNone(event.event_id)
        self.assertEqual(event.source, LearningEventSource.PROGRAM_H)

    def test_record_j_event(self):
        event = self.svc.record_j_event(LearningEventType.J_CONVERSATION_STARTED,
                                         actor_id="a1", channel="whatsapp")
        self.assertEqual(event.source, LearningEventSource.PROGRAM_J)
        self.assertEqual(event.channel, "whatsapp")

    def test_record_outcome_event(self):
        event = self.svc.record_outcome_event(actor_id="a1")
        self.assertEqual(event.event_type, LearningEventType.OUTCOME_RECORDED)

    def test_get_stats(self):
        self.svc.record_h_event(LearningEventType.H_QUALIFICATION_STARTED)
        self.svc.record_j_event(LearningEventType.J_CONVERSATION_STARTED)
        stats = self.svc.get_stats()
        self.assertGreaterEqual(stats["total_events"], 2)
        self.assertIn("PROGRAM_H", stats["by_source"])
        self.assertIn("PROGRAM_J", stats["by_source"])

    def test_event_registry_query_by_type(self):
        self.svc.record_h_event(LearningEventType.H_QUALIFICATION_STARTED)
        results = learning_event_registry.query(
            event_type=LearningEventType.H_QUALIFICATION_STARTED)
        self.assertGreaterEqual(len(results), 1)


# ── OutcomeRegistryService Tests ──────────────────────────────────────────


class OutcomeRegistryServiceTest(unittest.TestCase):
    def setUp(self):
        self.svc = OutcomeRegistryService()
        outcome_registry.clear()

    def test_register_qualification_success(self):
        o = self.svc.register_qualification_outcome(True, actor_id="a1")
        self.assertEqual(o.status, OutcomeStatus.SUCCESS)
        self.assertEqual(o.outcome_type, "qualification")

    def test_register_qualification_failure(self):
        o = self.svc.register_qualification_outcome(False)
        self.assertEqual(o.status, OutcomeStatus.FAILURE)

    def test_register_matching_success(self):
        o = self.svc.register_matching_outcome(True)
        self.assertEqual(o.status, OutcomeStatus.SUCCESS)

    def test_register_visit_outcome(self):
        o = self.svc.register_visit_outcome(True)
        self.assertEqual(o.status, OutcomeStatus.SUCCESS)

    def test_register_transaction_with_value(self):
        o = self.svc.register_transaction_outcome(True, monetary_value=500000)
        self.assertEqual(o.monetary_value, 500000)

    def test_register_payment_outcome(self):
        o = self.svc.register_payment_outcome(True, monetary_value=25000)
        self.assertEqual(o.status, OutcomeStatus.SUCCESS)
        self.assertEqual(o.monetary_value, 25000)

    def test_register_conversation_closed(self):
        o = self.svc.register_conversation_outcome(
            OutcomeStatus.SUCCESS, conversation_id="c1", satisfaction_score=8.0)
        self.assertEqual(o.satisfaction_score, 8.0)

    def test_success_rate(self):
        self.svc.register_qualification_outcome(True)
        self.svc.register_qualification_outcome(True)
        self.svc.register_qualification_outcome(False)
        rate = self.svc.get_success_rate("qualification")
        self.assertAlmostEqual(rate, 66.666, delta=0.01)

    def test_get_stats(self):
        self.svc.register_qualification_outcome(True)
        self.svc.register_matching_outcome(False)
        stats = self.svc.get_stats()
        self.assertGreaterEqual(stats["total_outcomes"], 2)


# ── FeedbackService Tests ─────────────────────────────────────────────────


class FeedbackServiceTest(unittest.TestCase):
    def setUp(self):
        self.svc = FeedbackService()

    def test_submit_user_feedback(self):
        f = self.svc.submit_user_feedback(FeedbackTarget.AI_RESPONSE, "ai1", 8.0, "Good")
        self.assertEqual(f.origin, FeedbackOrigin.USER)
        self.assertEqual(f.score, 8.0)

    def test_submit_satisfaction(self):
        f = self.svc.submit_satisfaction(9.0, "conv1")
        self.assertEqual(f.origin, FeedbackOrigin.SATISFACTION_SURVEY)
        self.assertEqual(f.target, FeedbackTarget.CONVERSATION)

    def test_submit_matching_feedback(self):
        f = self.svc.submit_matching_feedback(7.5, "match1", "agent1")
        self.assertEqual(f.origin, FeedbackOrigin.MATCHING)
        self.assertEqual(f.score, 7.5)

    def test_get_by_target(self):
        self.svc.submit_user_feedback(FeedbackTarget.PROPERTY, "prop1", 8.0)
        self.svc.submit_user_feedback(FeedbackTarget.PROPERTY, "prop1", 9.0)
        items = self.svc.get_by_target(FeedbackTarget.PROPERTY, "prop1")
        self.assertEqual(len(items), 2)

    def test_average_score(self):
        self.svc.submit_user_feedback(FeedbackTarget.AGENT_PERFORMANCE, "agent1", 8.0)
        self.svc.submit_user_feedback(FeedbackTarget.AGENT_PERFORMANCE, "agent1", 10.0)
        avg = self.svc.average_score(FeedbackTarget.AGENT_PERFORMANCE, "agent1")
        self.assertEqual(avg, 9.0)

    def test_average_score_empty(self):
        avg = self.svc.average_score(FeedbackTarget.PROPERTY, "nonexistent")
        self.assertEqual(avg, 0.0)

    def test_count(self):
        self.svc.submit_user_feedback(FeedbackTarget.AI_RESPONSE, "ai1", 5.0)
        self.assertGreaterEqual(self.svc.count(), 1)

    def test_get_all(self):
        self.svc.submit_user_feedback(FeedbackTarget.AI_RESPONSE, "ai1", 5.0)
        all_f = self.svc.get_all()
        self.assertGreaterEqual(len(all_f), 1)

    def test_submit_admin_feedback(self):
        f = self.svc.submit(FeedbackOrigin.ADMIN, FeedbackTarget.SERVICE, "svc1", 10.0)
        self.assertEqual(f.origin, FeedbackOrigin.ADMIN)


# ── LearningValidationService Tests ───────────────────────────────────────


class LearningValidationServiceTest(unittest.TestCase):
    def setUp(self):
        self.svc = LearningValidationService()

    def test_validate_valid_event(self):
        event = LearningEvent(event_type=LearningEventType.H_QUALIFICATION_STARTED,
                               source=LearningEventSource.PROGRAM_H)
        errors = self.svc.validate_event(event)
        self.assertEqual(len(errors), 0)

    def test_validate_event_invalid_type(self):
        event = LearningEvent(source=LearningEventSource.PROGRAM_H)
        event.event_type = "INVALID_TYPE"  # type: ignore
        errors = self.svc.validate_event(event)
        self.assertGreaterEqual(len(errors), 1)

    def test_validate_outcome_valid(self):
        o = OutcomeResult(outcome_type="test", status=OutcomeStatus.SUCCESS)
        errors = self.svc.validate_outcome(o)
        self.assertEqual(len(errors), 0)

    def test_validate_outcome_no_type(self):
        o = OutcomeResult(status=OutcomeStatus.SUCCESS)
        errors = self.svc.validate_outcome(o)
        self.assertGreaterEqual(len(errors), 1)

    def test_validate_feedback_valid(self):
        f = FeedbackItem(feedback_id="f1", score=5.0)
        errors = self.svc.validate_feedback(f)
        self.assertEqual(len(errors), 0)

    def test_validate_feedback_out_of_range(self):
        f = FeedbackItem(feedback_id="f1", score=15.0, min_score=0.0, max_score=10.0)
        errors = self.svc.validate_feedback(f)
        self.assertGreaterEqual(len(errors), 1)


# ── LearningConfig Tests ───────────────────────────────────────────────────


class LearningConfigTest(unittest.TestCase):
    def test_default_disabled(self):
        cfg = LearningConfig()
        self.assertFalse(cfg.learning_events_enabled)
        self.assertFalse(cfg.outcome_registry_enabled)
        self.assertFalse(cfg.feedback_engine_enabled)

    def test_enable_events(self):
        cfg = LearningConfig(learning_events_enabled=True)
        self.assertTrue(cfg.learning_events_enabled)

    def test_enable_outcome(self):
        cfg = LearningConfig(outcome_registry_enabled=True)
        self.assertTrue(cfg.outcome_registry_enabled)

    def test_enable_feedback(self):
        cfg = LearningConfig(feedback_engine_enabled=True)
        self.assertTrue(cfg.feedback_engine_enabled)


# ── JSON Serialization ─────────────────────────────────────────────────────


class LearningSerializationTest(unittest.TestCase):
    def test_event_json(self):
        e = LearningEvent(event_id="e1", event_type=LearningEventType.H_QUALIFICATION_STARTED,
                           source=LearningEventSource.PROGRAM_H)
        s = json.dumps(e.to_dict(), ensure_ascii=False, sort_keys=True)
        self.assertIn("H_QUALIFICATION_STARTED", s)

    def test_outcome_json(self):
        o = OutcomeResult(outcome_id="o1", outcome_type="qualification",
                           status=OutcomeStatus.SUCCESS, monetary_value=500000)
        s = json.dumps(o.to_dict(), ensure_ascii=False, sort_keys=True)
        self.assertIn("500000", s)

    def test_feedback_json(self):
        f = FeedbackItem(feedback_id="f1", origin=FeedbackOrigin.USER,
                          target=FeedbackTarget.AI_RESPONSE, score=8.0)
        s = json.dumps(f.to_dict(), ensure_ascii=False, sort_keys=True)
        self.assertIn("8.0", s)


# ── Event Source Enum Tests ───────────────────────────────────────────────


class LearningEventSourceTest(unittest.TestCase):
    def test_h_source(self):
        self.assertEqual(LearningEventSource.PROGRAM_H.value, "PROGRAM_H")

    def test_j_source(self):
        self.assertEqual(LearningEventSource.PROGRAM_J.value, "PROGRAM_J")

    def test_ai_source(self):
        self.assertEqual(LearningEventSource.AI_SYSTEM.value, "AI_SYSTEM")


class FeedbackOriginEnumTest(unittest.TestCase):
    def test_user(self):
        self.assertEqual(FeedbackOrigin.USER.value, "USER")

    def test_agent(self):
        self.assertEqual(FeedbackOrigin.AGENT.value, "AGENT")

    def test_payment(self):
        self.assertEqual(FeedbackOrigin.PAYMENT.value, "PAYMENT")


class FeedbackTargetEnumTest(unittest.TestCase):
    def test_ai_response(self):
        self.assertEqual(FeedbackTarget.AI_RESPONSE.value, "AI_RESPONSE")

    def test_matching_result(self):
        self.assertEqual(FeedbackTarget.MATCHING_RESULT.value, "MATCHING_RESULT")


class OutcomeStatusEnumTest(unittest.TestCase):
    def test_success(self):
        self.assertEqual(OutcomeStatus.SUCCESS.value, "SUCCESS")

    def test_failure(self):
        self.assertEqual(OutcomeStatus.FAILURE.value, "FAILURE")

    def test_abandoned(self):
        self.assertEqual(OutcomeStatus.ABANDONED.value, "ABANDONED")


# ── Run ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    unittest.main()
