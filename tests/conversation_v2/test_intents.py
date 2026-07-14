from __future__ import annotations

import unittest

from lawim_v2.conversation.domain.intents import Intent, IntentCandidate


class TestIntentEnum(unittest.TestCase):
    def test_searchable_intents(self):
        searchable = Intent.searchable()
        self.assertIn(Intent.RENT_APARTMENT, searchable)
        self.assertIn(Intent.BUY_HOUSE, searchable)
        self.assertIn(Intent.SELL_LAND, searchable)
        self.assertNotIn(Intent.GREETING, searchable)
        self.assertNotIn(Intent.INFORMATION, searchable)
        self.assertNotIn(Intent.HANDOVER, searchable)
        self.assertNotIn(Intent.COMPLAINT, searchable)
        self.assertNotIn(Intent.OTHER, searchable)

    def test_requires_property_intents(self):
        prop_intents = Intent.requires_property()
        self.assertIn(Intent.RENT_APARTMENT, prop_intents)
        self.assertIn(Intent.BUY_LAND, prop_intents)
        self.assertIn(Intent.BUY_VILLA, prop_intents)
        self.assertNotIn(Intent.SELL_LAND, prop_intents)
        self.assertNotIn(Intent.CONSTRUCT, prop_intents)
        self.assertNotIn(Intent.FIND_ARCHITECT, prop_intents)
        self.assertNotIn(Intent.INFORMATION, prop_intents)

    def test_requires_professional_intents(self):
        prof_intents = Intent.requires_professional()
        self.assertIn(Intent.FIND_ARCHITECT, prof_intents)
        self.assertIn(Intent.FIND_ENGINEER, prof_intents)
        self.assertIn(Intent.FIND_TECHNICIAN, prof_intents)
        self.assertIn(Intent.FIND_NOTARY, prof_intents)
        self.assertIn(Intent.FIND_AGENT, prof_intents)
        self.assertIn(Intent.FIND_CONTRACTOR, prof_intents)
        self.assertIn(Intent.FIND_LAWYER, prof_intents)
        self.assertNotIn(Intent.RENT_APARTMENT, prof_intents)
        self.assertNotIn(Intent.BUY_HOUSE, prof_intents)


class TestIntentCandidate(unittest.TestCase):
    def test_candidate_creation(self):
        c = IntentCandidate(intent=Intent.RENT_APARTMENT, confidence=0.85, source="explicit", raw_trigger="appartement")
        self.assertEqual(c.intent, Intent.RENT_APARTMENT)
        self.assertEqual(c.confidence, 0.85)
        self.assertEqual(c.source, "explicit")
        self.assertEqual(c.raw_trigger, "appartement")

    def test_is_confident_above_threshold(self):
        c = IntentCandidate(intent=Intent.BUY_HOUSE, confidence=0.75, source="inferred")
        self.assertTrue(c.is_confident())
        self.assertTrue(c.is_confident(threshold=0.5))

    def test_is_confident_below_threshold(self):
        c = IntentCandidate(intent=Intent.BUY_HOUSE, confidence=0.4, source="inferred")
        self.assertFalse(c.is_confident())

    def test_is_confident_at_threshold(self):
        c = IntentCandidate(intent=Intent.RENT_STUDIO, confidence=0.6, source="llm_classification")
        self.assertTrue(c.is_confident())

    def test_candidate_frozen_dataclass(self):
        c = IntentCandidate(intent=Intent.RENT_ROOM, confidence=0.9, source="explicit")
        with self.assertRaises(AttributeError):
            c.confidence = 0.5

    def test_candidate_default_raw_trigger(self):
        c = IntentCandidate(intent=Intent.GREETING, confidence=1.0, source="explicit")
        self.assertIsNone(c.raw_trigger)


class TestIntentCompleteness(unittest.TestCase):
    def test_all_intents_in_searchable_or_not(self):
        non_searchable = {Intent.GREETING, Intent.INFORMATION, Intent.COMPLAINT, Intent.HANDOVER, Intent.OTHER, Intent.DOCUMENTATION}
        for intent in Intent:
            if intent in non_searchable:
                self.assertNotIn(intent, Intent.searchable(), f"{intent} should not be searchable")
            else:
                self.assertIn(intent, Intent.searchable(), f"{intent} should be searchable")

    def test_all_property_intents_in_searchable(self):
        for intent in Intent.requires_property():
            self.assertIn(intent, Intent.searchable())

    def test_professional_intents_not_in_property(self):
        for intent in Intent.requires_professional():
            self.assertNotIn(intent, Intent.requires_property())

    def test_professional_intents_in_searchable(self):
        for intent in Intent.requires_professional():
            self.assertIn(intent, Intent.searchable())


if __name__ == "__main__":
    unittest.main()
