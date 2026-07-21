from __future__ import annotations

import unittest

from lawim_v2.conversation.state.state import ConversationState
from lawim_v2.conversation.memory import (
    BusinessMemoryContext,
    CompactionStrategy,
    ConversationSummary,
    ConversationSummaryService,
    HumanHandoverContext,
    MemoryCompactionService,
    MemoryContextBuilder,
    ProviderMemoryContext,
)


class TestBusinessMemoryContext(unittest.TestCase):
    def test_defaults(self):
        ctx = BusinessMemoryContext()
        self.assertIsNone(ctx.conversation_state)
        self.assertEqual(ctx.active_slots, {})
        self.assertEqual(ctx.missing_slots, [])
        self.assertEqual(ctx.language, "fr")
        self.assertEqual(ctx.readiness, "not_started")

    def test_with_values(self):
        state = ConversationState()
        ctx = BusinessMemoryContext(
            conversation_state=state,
            active_slots={"city": "Douala"},
            missing_slots=["budget"],
            intent="rental_search",
            readiness="in_progress",
        )
        self.assertIs(ctx.conversation_state, state)
        self.assertEqual(ctx.active_slots["city"], "Douala")
        self.assertEqual(ctx.missing_slots, ["budget"])


class TestProviderMemoryContext(unittest.TestCase):
    def test_defaults(self):
        ctx = ProviderMemoryContext()
        self.assertEqual(ctx.language, "fr")
        self.assertEqual(ctx.active_facts, {})
        self.assertEqual(ctx.prohibitions, [])

    def test_no_raw_history_or_secrets(self):
        ctx = ProviderMemoryContext(
            active_facts={"city": "Douala"},
            summary="Rental search in Douala",
        )
        self.assertNotIn("raw_history", vars(ctx))
        self.assertNotIn("secrets", vars(ctx))
        self.assertNotIn("message_ids", vars(ctx))

    def test_prohibitions_loaded(self):
        builder = MemoryContextBuilder()
        ctx = builder.build_provider_context("nonexistent_conv")
        self.assertEqual(len(ctx.prohibitions), 0)

    def test_provider_context_default_when_no_state(self):
        builder = MemoryContextBuilder()
        ctx = builder.build_provider_context("nonexistent_conv")
        self.assertEqual(ctx.language, "fr")
        self.assertEqual(ctx.active_facts, {})
        self.assertEqual(ctx.last_question_text, "")
        self.assertEqual(ctx.summary, "")


class TestHumanHandoverContext(unittest.TestCase):
    def test_defaults(self):
        ctx = HumanHandoverContext()
        self.assertEqual(ctx.case_id, "")
        self.assertEqual(ctx.known_information, {})
        self.assertEqual(ctx.missing_information, [])
        self.assertEqual(ctx.language, "fr")

    def test_handover_context_builder_no_case(self):
        builder = MemoryContextBuilder()
        ctx = builder.build_handover_context("case_999")
        self.assertEqual(ctx.case_id, "case_999")
        self.assertTrue(len(ctx.limitations) >= 1)
        self.assertEqual(ctx.handover_reason, "case_not_found")


class TestMemoryContextBuilder(unittest.TestCase):
    def test_default_construction(self):
        builder = MemoryContextBuilder()
        self.assertIsNotNone(builder)

    def test_build_business_context_no_state(self):
        builder = MemoryContextBuilder()
        ctx = builder.build_business_context("conv_1")
        self.assertIsNone(ctx.conversation_state)
        self.assertEqual(ctx.intent, "")

    def test_build_provider_context_no_state(self):
        builder = MemoryContextBuilder()
        ctx = builder.build_provider_context("conv_1")
        self.assertEqual(ctx.language, "fr")
        self.assertEqual(ctx.active_facts, {})

    def test_build_resume_context_no_state(self):
        builder = MemoryContextBuilder()
        ctx = builder.build_resume_context("actor_1", "conv_1")
        self.assertEqual(ctx["actor_id"], "actor_1")
        self.assertIn("resumed_at", ctx)


class TestConversationSummary(unittest.TestCase):
    def test_defaults(self):
        s = ConversationSummary()
        self.assertEqual(s.summary_id, "")
        self.assertEqual(s.active_slots, {})
        self.assertEqual(s.important_decisions, [])
        self.assertEqual(s.version, 1)

    def test_with_values(self):
        s = ConversationSummary(
            summary_id="s1",
            conversation_id="c1",
            intent="rental_search",
            active_slots={"city": "Douala"},
            interaction_count=5,
        )
        self.assertEqual(s.summary_id, "s1")
        self.assertEqual(s.intent, "rental_search")


class TestConversationSummaryService(unittest.TestCase):
    def test_default_construction(self):
        service = ConversationSummaryService()
        self.assertIsNotNone(service)

    def test_get_summary_no_repository(self):
        service = ConversationSummaryService()
        self.assertIsNone(service.get_summary("conv_1"))

    def test_generate_or_refresh_no_repository(self):
        service = ConversationSummaryService()
        result = service.generate_or_refresh("conv_1")
        self.assertIsInstance(result, ConversationSummary)
        self.assertEqual(result.conversation_id, "conv_1")

    def test_summarize_turns_empty(self):
        service = ConversationSummaryService()
        self.assertEqual(service.summarize_turns([]), "")

    def test_summarize_turns_with_data(self):
        service = ConversationSummaryService()
        turns = [{"message": "Hello"}, {"message": "I need a 2-bedroom apartment"}]
        result = service.summarize_turns(turns)
        self.assertIn("Hello", result)
        self.assertIn("2-bedroom", result)


class TestCompactionStrategy(unittest.TestCase):
    def test_defaults(self):
        s = CompactionStrategy()
        self.assertEqual(s.recent_turn_window, 10)
        self.assertEqual(s.summary_refresh_threshold, 20)
        self.assertIn("correction", s.important_event_types)
        self.assertIn("handover", s.important_event_types)

    def test_custom_strategy(self):
        s = CompactionStrategy(recent_turn_window=5, maximum_provider_context_chars=1000)
        self.assertEqual(s.recent_turn_window, 5)
        self.assertEqual(s.maximum_provider_context_chars, 1000)


class TestMemoryCompactionService(unittest.TestCase):
    def setUp(self):
        self.service = MemoryCompactionService()

    def test_default_strategy(self):
        self.assertEqual(self.service._strategy.recent_turn_window, 10)

    def test_should_compact_under_threshold(self):
        self.assertFalse(self.service.should_compact(5, 0))

    def test_should_compact_over_window_no_summary(self):
        self.assertTrue(self.service.should_compact(15, 0))

    def test_should_compact_over_summary_threshold(self):
        self.assertTrue(self.service.should_compact(25, 1))

    def test_should_compact_negative_interaction(self):
        self.assertFalse(self.service.should_compact(-1, 0))

    def test_compact_turns_empty(self):
        self.assertEqual(self.service.compact_turns([]), [])

    def test_compact_turns_under_window(self):
        turns = [{"id": i} for i in range(5)]
        result = self.service.compact_turns(turns)
        self.assertEqual(len(result), 5)

    def test_compact_turns_over_window(self):
        turns = [{"id": i} for i in range(25)]
        result = self.service.compact_turns(turns)
        self.assertEqual(len(result), 11)
        self.assertEqual(result[0]["_type"], "summary")

    def test_compact_turns_with_custom_summary(self):
        turns = [{"id": i} for i in range(15)]
        result = self.service.compact_turns(turns, summary="Custom summary")
        self.assertEqual(result[0]["_content"], "Custom summary")

    def test_get_important_events_empty(self):
        self.assertEqual(self.service.get_important_events([]), [])

    def test_get_important_events_filters(self):
        events = [
            {"type": "greeting", "message": "Hello"},
            {"type": "correction", "message": "Correcting budget"},
            {"type": "unknown", "message": "Random"},
            {"type": "handover", "message": "Handing over"},
        ]
        important = self.service.get_important_events(events)
        self.assertEqual(len(important), 2)
        types = {e["type"] for e in important}
        self.assertIn("correction", types)
        self.assertIn("handover", types)

    def test_get_important_events_checks_action_key(self):
        events = [
            {"action": "milestone", "message": "Milestone reached"},
        ]
        important = self.service.get_important_events(events)
        self.assertEqual(len(important), 1)

    def test_get_important_events_checks_event_type_key(self):
        events = [
            {"event_type": "payment", "message": "Payment received"},
        ]
        important = self.service.get_important_events(events)
        self.assertEqual(len(important), 1)


class TestPackageExports(unittest.TestCase):
    def test_all_exports_present(self):
        from lawim_v2.conversation.memory import __all__ as exports
        expected = [
            "BusinessMemoryContext",
            "CompactionStrategy",
            "ConversationSummary",
            "ConversationSummaryService",
            "HumanHandoverContext",
            "MemoryCompactionService",
            "MemoryContextBuilder",
            "ProviderMemoryContext",
        ]
        for name in expected:
            self.assertIn(name, exports)


if __name__ == "__main__":
    unittest.main()
