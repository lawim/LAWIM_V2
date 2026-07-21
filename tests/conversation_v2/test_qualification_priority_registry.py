from __future__ import annotations

import unittest

from lawim_v2.conversation.qualification.priority_registry import (
    QualificationJourneyDefinition,
    QualificationPriorityRegistry,
    QualificationSlotDefinition,
)
from lawim_v2.conversation.qualification.question_catalog import (
    QUESTION_CATALOG,
    has_language,
)

JOURNEY_CODES = [
    "SEARCH_RENTAL",
    "SEARCH_PURCHASE",
    "SEARCH_LAND",
    "SELL_PROPERTY",
    "RENT_OUT_PROPERTY",
    "PUBLISH_LISTING",
    "PROPERTY_VISIT",
    "DOCUMENT_ASSISTANCE",
    "CONSTRUCTION_SERVICE",
    "PROFESSIONAL_SERVICE",
]


class TestQualificationPriorityRegistry(unittest.TestCase):

    def setUp(self) -> None:
        self.registry = QualificationPriorityRegistry()

    def test_all_journeys_defined(self) -> None:
        found = {j.journey_code for j in self.registry.all_journeys()}
        for code in JOURNEY_CODES:
            self.assertIn(code, found, f"Missing journey: {code}")
        self.assertEqual(len(found), len(JOURNEY_CODES))

    def test_each_journey_has_priority_order(self) -> None:
        for j in self.registry.all_journeys():
            self.assertGreater(
                len(j.priority_order), 0,
                f"Journey {j.journey_code} has empty priority_order",
            )

    def test_each_journey_has_intent_code(self) -> None:
        for j in self.registry.all_journeys():
            self.assertTrue(j.intent_code, f"Journey {j.journey_code} missing intent_code")

    def test_each_journey_has_completion_rule(self) -> None:
        for j in self.registry.all_journeys():
            self.assertTrue(
                j.completion_rule,
                f"Journey {j.journey_code} missing completion_rule",
            )

    def test_each_journey_has_next_action(self) -> None:
        for j in self.registry.all_journeys():
            self.assertTrue(
                j.next_action,
                f"Journey {j.journey_code} missing next_action",
            )

    def test_no_duplicate_slot_codes(self) -> None:
        codes = [s.slot_code for s in self.registry.all_slots()]
        self.assertEqual(len(codes), len(set(codes)))

    def test_duplicate_journey_codes_not_allowed(self) -> None:
        dup = QualificationJourneyDefinition(
            intent_code="search_rental",
            journey_code="SEARCH_RENTAL",
            priority_order=["city"],
        )
        with self.assertRaises(ValueError):
            self.registry._register_journey(dup)

    def test_all_slots_have_categories(self) -> None:
        valid = {"ESSENTIAL", "CONDITIONAL", "SECONDARY", "OPTIONAL_USER_REQUIREMENT"}
        for s in self.registry.all_slots():
            self.assertIn(
                s.category, valid,
                f"Slot '{s.slot_code}' has invalid category '{s.category}'",
            )

    def test_all_slots_have_question_key(self) -> None:
        for s in self.registry.all_slots():
            self.assertTrue(
                s.question_key,
                f"Slot '{s.slot_code}' missing question_key",
            )

    def test_all_slots_have_data_type(self) -> None:
        valid_types = {"string", "integer", "boolean", "number"}
        for s in self.registry.all_slots():
            self.assertIn(
                s.data_type, valid_types,
                f"Slot '{s.slot_code}' has invalid data_type '{s.data_type}'",
            )

    def test_all_slots_have_priority(self) -> None:
        for s in self.registry.all_slots():
            self.assertIsInstance(
                s.priority, int,
                f"Slot '{s.slot_code}' priority is not an int",
            )

    def test_priorities_are_unique(self) -> None:
        priorities = [s.priority for s in self.registry.all_slots()]
        self.assertEqual(len(priorities), len(set(priorities)))

    def test_dependencies_are_valid(self) -> None:
        issues = self.registry.validate_dependencies()
        self.assertEqual(
            issues, [],
            f"Dependency validation issues: {issues}",
        )

    def test_priority_order_is_deterministic(self) -> None:
        for j in self.registry.all_journeys():
            order1 = list(j.priority_order)
            order2 = list(j.priority_order)
            self.assertEqual(order1, order2)

    def test_get_journey_by_intent_code(self) -> None:
        j = self.registry.get_journey("search_rental")
        self.assertIsNotNone(j)
        self.assertEqual(j.journey_code, "SEARCH_RENTAL")

    def test_get_journey_by_journey_code(self) -> None:
        j = self.registry.get_journey("SEARCH_PURCHASE")
        self.assertIsNotNone(j)
        self.assertEqual(j.intent_code, "search_purchase")

    def test_get_journey_unknown(self) -> None:
        j = self.registry.get_journey("nonexistent")
        self.assertIsNone(j)

    def test_get_slot(self) -> None:
        s = self.registry.get_slot("city")
        self.assertIsNotNone(s)
        self.assertEqual(s.slot_code, "city")
        self.assertEqual(s.category, "ESSENTIAL")

    def test_get_slot_unknown(self) -> None:
        s = self.registry.get_slot("nonexistent")
        self.assertIsNone(s)

    def test_resolve_priority_returns_first_missing(self) -> None:
        journey = self.registry.get_journey("search_rental")
        known = {}
        first = self.registry.resolve_priority(journey, known)
        self.assertEqual(first, "transaction_type")

    def test_resolve_priority_skips_known(self) -> None:
        journey = self.registry.get_journey("search_rental")
        known = {"transaction_type": "rent"}
        second = self.registry.resolve_priority(journey, known)
        self.assertEqual(second, "property_type")

    def test_resolve_priority_studio_skips_bedrooms(self) -> None:
        journey = self.registry.get_journey("search_rental")
        known = {
            "transaction_type": "rent",
            "property_type": "studio",
            "city": "Douala",
            "district": "Akwa",
            "budget_xaf": 100000,
        }
        next_slot = self.registry.resolve_priority(journey, known)
        self.assertNotEqual(next_slot, "bedrooms")
        self.assertNotEqual(next_slot, "bathrooms")
        self.assertNotEqual(next_slot, "kitchens")

    def test_resolve_priority_apartment_asks_bedrooms(self) -> None:
        journey = self.registry.get_journey("search_rental")
        known = {
            "transaction_type": "rent",
            "property_type": "apartment",
            "city": "Douala",
            "budget_xaf": 100000,
        }
        next_slot = self.registry.resolve_priority(journey, known)
        self.assertEqual(next_slot, "district")

    def test_resolve_priority_returns_none_when_all_filled(self) -> None:
        journey = self.registry.get_journey("search_rental")
        known = {
            "transaction_type": "rent",
            "property_type": "studio",
            "city": "Douala",
            "district": "Akwa",
            "budget_xaf": 100000,
            "furnished": True,
            "move_in_date": "next_month",
            "other_requirements": "none",
        }
        result = self.registry.resolve_priority(journey, known)
        self.assertIsNone(result)

    def test_resolve_all_missing(self) -> None:
        journey = self.registry.get_journey("SEARCH_RENTAL")
        known = {"transaction_type": "rent", "city": "Douala"}
        missing = self.registry.resolve_all_missing(journey, known)
        self.assertIn("property_type", missing)
        self.assertIn("budget_xaf", missing)
        self.assertNotIn("transaction_type", missing)
        self.assertIn("district", missing)

    def test_resolve_all_missing_studio_no_bedrooms(self) -> None:
        journey = self.registry.get_journey("SEARCH_RENTAL")
        known = {
            "transaction_type": "rent",
            "property_type": "studio",
            "city": "Douala",
            "budget_xaf": 100000,
        }
        missing = self.registry.resolve_all_missing(journey, known)
        self.assertNotIn("bedrooms", missing)
        self.assertNotIn("bathrooms", missing)
        self.assertNotIn("kitchens", missing)

    def test_get_journey_via_both_keys(self) -> None:
        j1 = self.registry.get_journey("SEARCH_LAND")
        j2 = self.registry.get_journey("search_land")
        self.assertIsNotNone(j1)
        self.assertIsNotNone(j2)
        self.assertEqual(j1.journey_code, j2.journey_code)

    def test_resolve_priority_with_unmet_dependency(self) -> None:
        journey = self.registry.get_journey("SEARCH_RENTAL")
        known = {"transaction_type": "rent", "property_type": "apartment", "city": "Douala", "budget_xaf": 100000}
        next_slot = self.registry.resolve_priority(journey, known)
        self.assertEqual(next_slot, "district")


class TestSlotQuestionKeys(unittest.TestCase):

    def setUp(self) -> None:
        self.registry = QualificationPriorityRegistry()

    def test_all_slot_questions_exist_in_catalog(self) -> None:
        for slot in self.registry.all_slots():
            self.assertIn(
                slot.question_key,
                QUESTION_CATALOG,
                f"Slot '{slot.slot_code}' question_key '{slot.question_key}' "
                f"not found in QUESTION_CATALOG",
            )

    def test_all_slot_questions_have_fr(self) -> None:
        for slot in self.registry.all_slots():
            self.assertTrue(
                has_language(slot.question_key, "fr"),
                f"Slot '{slot.slot_code}' missing FR question",
            )

    def test_all_slot_questions_have_en(self) -> None:
        for slot in self.registry.all_slots():
            self.assertTrue(
                has_language(slot.question_key, "en"),
                f"Slot '{slot.slot_code}' missing EN question",
            )

    def test_all_slot_questions_have_pcm(self) -> None:
        for slot in self.registry.all_slots():
            self.assertTrue(
                has_language(slot.question_key, "pcm"),
                f"Slot '{slot.slot_code}' missing PCM question",
            )

    def test_clarification_keys_exist(self) -> None:
        for slot in self.registry.all_slots():
            if not slot.clarification_key:
                continue
            self.assertIn(
                slot.clarification_key,
                QUESTION_CATALOG,
                f"Slot '{slot.slot_code}' clarification_key "
                f"'{slot.clarification_key}' not found in QUESTION_CATALOG",
            )


class TestJourneySlotCompleteness(unittest.TestCase):

    def setUp(self) -> None:
        self.registry = QualificationPriorityRegistry()

    def test_search_rental_priority_order(self) -> None:
        journey = self.registry.get_journey("search_rental")
        expected = [
            "transaction_type", "property_type", "city", "district",
            "budget_xaf", "bedrooms", "bathrooms", "kitchens",
            "furnished", "move_in_date", "other_requirements",
        ]
        self.assertEqual(journey.priority_order, expected)

    def test_search_purchase_priority_order(self) -> None:
        journey = self.registry.get_journey("search_purchase")
        expected = [
            "property_type", "city", "district", "budget_xaf",
            "bedrooms", "bathrooms", "kitchens",
            "financing_mode", "title_requirements", "other_requirements",
        ]
        self.assertEqual(journey.priority_order, expected)

    def test_search_land_priority_order(self) -> None:
        journey = self.registry.get_journey("search_land")
        expected = [
            "transaction_type", "city", "district", "intended_use",
            "surface_m2", "budget_xaf", "title_status",
            "accessibility", "utilities", "other_requirements",
        ]
        self.assertEqual(journey.priority_order, expected)

    def test_sell_property_priority_order(self) -> None:
        journey = self.registry.get_journey("sell_property")
        expected = [
            "actor_role", "property_type", "city", "district",
            "ownership_status", "documents_available", "surface_m2",
            "asking_price", "occupancy_status", "inspection_availability",
        ]
        self.assertEqual(journey.priority_order, expected)

    def test_rent_out_property_priority_order(self) -> None:
        journey = self.registry.get_journey("rent_out_property")
        expected = [
            "actor_role", "property_type", "city", "district",
            "ownership_status", "documents_available", "furnished",
            "monthly_rent", "charges", "availability_date",
            "inspection_availability",
        ]
        self.assertEqual(journey.priority_order, expected)

    def test_publish_listing_priority_order(self) -> None:
        journey = self.registry.get_journey("publish_listing")
        expected = [
            "actor_role", "transaction_type", "property_type",
            "location", "price", "description", "documents",
            "media", "availability", "consent",
        ]
        self.assertEqual(journey.priority_order, expected)

    def test_property_visit_priority_order(self) -> None:
        journey = self.registry.get_journey("property_visit")
        expected = [
            "property_reference", "preferred_date",
            "preferred_time_window", "contact_channel",
            "attendee_count", "confirmation",
        ]
        self.assertEqual(journey.priority_order, expected)

    def test_document_assistance_priority_order(self) -> None:
        journey = self.registry.get_journey("document_assistance")
        expected = [
            "document_type", "property_reference", "document_owner",
            "requested_action", "document_availability", "consent",
        ]
        self.assertEqual(journey.priority_order, expected)

    def test_construction_service_priority_order(self) -> None:
        journey = self.registry.get_journey("construction_service")
        expected = [
            "service_type", "project_location", "property_type",
            "project_stage", "scope", "budget_range", "timeline",
            "documents_available", "preferred_contact",
        ]
        self.assertEqual(journey.priority_order, expected)

    def test_professional_service_priority_order(self) -> None:
        journey = self.registry.get_journey("professional_service")
        expected = [
            "service_type", "project_location", "property_type",
            "project_stage", "scope", "timeline",
            "preferred_contact",
        ]
        self.assertEqual(journey.priority_order, expected)

    def test_required_slots_subset_of_priority_order(self) -> None:
        for j in self.registry.all_journeys():
            for slot in j.required_slots:
                self.assertIn(
                    slot, j.priority_order,
                    f"Journey {j.journey_code}: required slot '{slot}' "
                    f"not in priority_order",
                )

    def test_optional_slots_subset_of_priority_order(self) -> None:
        for j in self.registry.all_journeys():
            for slot in j.optional_slots:
                self.assertIn(
                    slot, j.priority_order,
                    f"Journey {j.journey_code}: optional slot '{slot}' "
                    f"not in priority_order",
                )


if __name__ == "__main__":
    unittest.main()
