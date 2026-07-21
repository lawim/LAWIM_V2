"""Test memory compaction: thresholds, turn trimming, important event filtering."""

from __future__ import annotations

import unittest

from lawim_v2.conversation.memory import (
    CompactionStrategy,
    MemoryCompactionService,
)


class TestMemoryCompaction(unittest.TestCase):
    def setUp(self):
        self.service = MemoryCompactionService()
        self.strategy = CompactionStrategy()

    def test_should_compact_below_threshold(self):
        self.assertFalse(self.service.should_compact(5, 0))

    def test_should_compact_above_threshold(self):
        self.assertTrue(self.service.should_compact(15, 0))

    def test_should_compact_zero_interactions(self):
        self.assertFalse(self.service.should_compact(0, 1))

    def test_should_compact_negative_interactions(self):
        self.assertFalse(self.service.should_compact(-1, 0))

    def test_should_compact_no_summary_below_window(self):
        self.assertFalse(self.service.should_compact(9, 0))

    def test_should_compact_no_summary_at_window(self):
        self.assertFalse(self.service.should_compact(10, 0))

    def test_should_compact_with_summary_nonzero_version(self):
        self.assertTrue(self.service.should_compact(25, 1))

    def test_should_compact_custom_strategy(self):
        custom = MemoryCompactionService(
            CompactionStrategy(recent_turn_window=3, summary_refresh_threshold=5),
        )
        self.assertTrue(custom.should_compact(6, 1))
        self.assertTrue(custom.should_compact(4, 0))

    def test_should_compact_custom_strategy_below_both(self):
        custom = MemoryCompactionService(
            CompactionStrategy(recent_turn_window=10, summary_refresh_threshold=20),
        )
        self.assertFalse(custom.should_compact(5, 0))

    def test_compact_turns_empty(self):
        self.assertEqual(self.service.compact_turns([]), [])

    def test_compact_turns_exactly_window(self):
        turns = [{"id": i} for i in range(10)]
        result = self.service.compact_turns(turns)
        self.assertEqual(len(result), 10)
        for t in result:
            self.assertNotIn("_type", t)

    def test_compact_turns_one_over_window(self):
        turns = [{"id": i} for i in range(11)]
        result = self.service.compact_turns(turns)
        self.assertEqual(len(result), 11)
        self.assertEqual(result[0]["_type"], "summary")

    def test_compact_turns_many(self):
        turns = [{"id": i} for i in range(50)]
        result = self.service.compact_turns(turns)
        self.assertEqual(len(result), 11)
        self.assertEqual(result[0]["_type"], "summary")
        self.assertEqual(result[0]["_content"], "[40 earlier turns compacted]")

    def test_compact_turns_with_custom_summary(self):
        turns = [{"id": i} for i in range(15)]
        result = self.service.compact_turns(turns, summary="Custom overview")
        self.assertEqual(result[0]["_type"], "summary")
        self.assertEqual(result[0]["_content"], "Custom overview")

    def test_important_events_empty(self):
        self.assertEqual(self.service.get_important_events([]), [])

    def test_important_events_none_match(self):
        events = [
            {"type": "greeting"},
            {"type": "farewell"},
            {"type": "question"},
        ]
        self.assertEqual(self.service.get_important_events(events), [])

    def test_important_events_correction(self):
        events = [{"type": "correction", "field": "budget"}]
        important = self.service.get_important_events(events)
        self.assertEqual(len(important), 1)

    def test_important_events_handover(self):
        events = [{"type": "handover", "reason": "Complex case"}]
        important = self.service.get_important_events(events)
        self.assertEqual(len(important), 1)

    def test_important_events_consent(self):
        events = [{"type": "consent", "channel": "telegram"}]
        important = self.service.get_important_events(events)
        self.assertEqual(len(important), 1)

    def test_important_events_decision(self):
        events = [{"type": "decision", "action": "qualified"}]
        important = self.service.get_important_events(events)
        self.assertEqual(len(important), 1)

    def test_important_events_payment(self):
        events = [{"type": "payment", "amount": 50000}]
        important = self.service.get_important_events(events)
        self.assertEqual(len(important), 1)

    def test_important_events_document(self):
        events = [{"type": "document", "name": "lease.pdf"}]
        important = self.service.get_important_events(events)
        self.assertEqual(len(important), 1)

    def test_important_events_milestone(self):
        events = [{"event_type": "milestone", "step": "completed"}]
        important = self.service.get_important_events(events)
        self.assertEqual(len(important), 1)

    def test_important_events_action_key(self):
        events = [{"action": "contract", "status": "signed"}]
        important = self.service.get_important_events(events)
        self.assertEqual(len(important), 1)

    def test_strategy_defaults(self):
        s = CompactionStrategy()
        self.assertEqual(s.recent_turn_window, 10)
        self.assertEqual(s.summary_refresh_threshold, 20)
        self.assertEqual(s.maximum_provider_context_chars, 2000)
        self.assertIn("correction", s.important_event_types)
        self.assertIn("handover", s.important_event_types)
        self.assertIn("payment", s.important_event_types)
        self.assertIn("document", s.important_event_types)
        self.assertIn("milestone", s.important_event_types)

    def test_strategy_custom(self):
        s = CompactionStrategy(
            recent_turn_window=5,
            summary_refresh_threshold=10,
            maximum_provider_context_chars=500,
        )
        self.assertEqual(s.recent_turn_window, 5)
        self.assertEqual(s.summary_refresh_threshold, 10)
        self.assertEqual(s.maximum_provider_context_chars, 500)


if __name__ == "__main__":
    unittest.main()
