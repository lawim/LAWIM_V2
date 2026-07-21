from __future__ import annotations

import unittest

from lawim_v2.conversation.qualification.priority_registry import (
    QualificationPriorityRegistry,
)


class Turn:
    def __init__(self, text: str, slot: str, value: str) -> None:
        self.text = text
        self.slot = slot
        self.value = value


class TestMultiTurnStudioRental(unittest.TestCase):

    def setUp(self) -> None:
        self.registry = QualificationPriorityRegistry()

    def _run_dialogue(self, journey_code: str, expected_order: list[str]) -> None:
        journey = self.registry.get_journey(journey_code)
        self.assertIsNotNone(journey)
        known: dict[str, str] = {}
        questions_asked: list[str] = []
        for expected_slot in expected_order:
            next_q = self.registry.resolve_priority(journey, known)
            self.assertIsNotNone(
                next_q,
                f"Expected to ask '{expected_slot}' but got None. "
                f"Known: {known}",
            )
            questions_asked.append(next_q)
            known[expected_slot] = f"value_{expected_slot}"
        final = self.registry.resolve_priority(journey, known)
        self.assertIsNone(final, f"Expected None but got '{final}'")
        self.assertEqual(questions_asked, expected_order)

    def test_studio_rental_full_dialogue(self) -> None:
        journey = self.registry.get_journey("SEARCH_RENTAL")
        known: dict[str, str] = {
            "transaction_type": "rent",
            "property_type": "studio",
        }
        expected_order = [
            "city",
            "district",
            "budget_xaf",
            "furnished",
            "move_in_date",
            "other_requirements",
        ]
        questions_asked: list[str] = []
        for expected_slot in expected_order:
            next_q = self.registry.resolve_priority(journey, known)
            self.assertIsNotNone(
                next_q,
                f"Expected to ask '{expected_slot}' but got None. "
                f"Known: {known}",
            )
            questions_asked.append(next_q)
            known[expected_slot] = f"value_{expected_slot}"
        final = self.registry.resolve_priority(journey, known)
        self.assertIsNone(final, f"Expected None but got '{final}'")
        self.assertEqual(questions_asked, expected_order)

    def test_apartment_rental_full_dialogue(self) -> None:
        self._run_dialogue(
            "SEARCH_RENTAL",
            [
                "transaction_type",
                "property_type",
                "city",
                "district",
                "budget_xaf",
                "bedrooms",
                "bathrooms",
                "kitchens",
                "furnished",
                "move_in_date",
                "other_requirements",
            ],
        )

    def test_house_purchase_full_dialogue(self) -> None:
        self._run_dialogue(
            "SEARCH_PURCHASE",
            [
                "property_type",
                "city",
                "district",
                "budget_xaf",
                "bedrooms",
                "bathrooms",
                "kitchens",
                "financing_mode",
                "title_requirements",
                "other_requirements",
            ],
        )

    def test_land_purchase_full_dialogue(self) -> None:
        self._run_dialogue(
            "SEARCH_LAND",
            [
                "transaction_type",
                "city",
                "district",
                "intended_use",
                "surface_m2",
                "budget_xaf",
                "title_status",
                "accessibility",
                "utilities",
                "other_requirements",
            ],
        )

    def test_sell_property_full_dialogue(self) -> None:
        self._run_dialogue(
            "SELL_PROPERTY",
            [
                "actor_role",
                "property_type",
                "city",
                "district",
                "ownership_status",
                "documents_available",
                "surface_m2",
                "asking_price",
                "occupancy_status",
                "inspection_availability",
            ],
        )

    def test_rent_out_property_full_dialogue(self) -> None:
        self._run_dialogue(
            "RENT_OUT_PROPERTY",
            [
                "actor_role",
                "property_type",
                "city",
                "district",
                "ownership_status",
                "documents_available",
                "furnished",
                "monthly_rent",
                "charges",
                "availability_date",
                "inspection_availability",
            ],
        )

    def test_publish_listing_full_dialogue(self) -> None:
        self._run_dialogue(
            "PUBLISH_LISTING",
            [
                "actor_role",
                "transaction_type",
                "property_type",
                "location",
                "price",
                "description",
                "documents",
                "media",
                "availability",
                "consent",
            ],
        )

    def test_property_visit_full_dialogue(self) -> None:
        self._run_dialogue(
            "PROPERTY_VISIT",
            [
                "property_reference",
                "preferred_date",
                "preferred_time_window",
                "contact_channel",
                "attendee_count",
                "confirmation",
            ],
        )

    def test_document_assistance_full_dialogue(self) -> None:
        self._run_dialogue(
            "DOCUMENT_ASSISTANCE",
            [
                "document_type",
                "property_reference",
                "document_owner",
                "requested_action",
                "document_availability",
                "consent",
            ],
        )

    def test_construction_service_full_dialogue(self) -> None:
        self._run_dialogue(
            "CONSTRUCTION_SERVICE",
            [
                "service_type",
                "project_location",
                "property_type",
                "project_stage",
                "scope",
                "budget_range",
                "timeline",
                "documents_available",
                "preferred_contact",
            ],
        )

    def test_professional_service_full_dialogue(self) -> None:
        self._run_dialogue(
            "PROFESSIONAL_SERVICE",
            [
                "service_type",
                "project_location",
                "property_type",
                "project_stage",
                "scope",
                "timeline",
                "preferred_contact",
            ],
        )

    def test_studio_rental_bonjour_scenario(self) -> None:
        """Simulate: Bonjour -> Je cherche un studio -> Je veux louer -> Douala -> Akwa"""
        journey = self.registry.get_journey("SEARCH_RENTAL")
        known: dict[str, str] = {}
        questions: list[str] = []

        next_q = self.registry.resolve_priority(journey, known)
        questions.append(next_q)
        self.assertEqual(next_q, "transaction_type")

        known["transaction_type"] = "rent"
        next_q = self.registry.resolve_priority(journey, known)
        questions.append(next_q)
        self.assertEqual(next_q, "property_type")

        known["property_type"] = "studio"
        next_q = self.registry.resolve_priority(journey, known)
        questions.append(next_q)
        self.assertEqual(next_q, "city")

        known["city"] = "Douala"
        next_q = self.registry.resolve_priority(journey, known)
        questions.append(next_q)
        self.assertEqual(next_q, "district")

        known["district"] = "Akwa"
        next_q = self.registry.resolve_priority(journey, known)
        questions.append(next_q)
        self.assertEqual(next_q, "budget_xaf")

        known["budget_xaf"] = "100000"
        next_q = self.registry.resolve_priority(journey, known)
        self.assertEqual(next_q, "furnished")

        known["furnished"] = "true"
        next_q = self.registry.resolve_priority(journey, known)
        self.assertEqual(next_q, "move_in_date")

    def test_apartment_douala_bonamoussadi_scenario(self) -> None:
        """Apartment rental: 3 bedrooms, 2 bathrooms, kitchen"""
        journey = self.registry.get_journey("SEARCH_RENTAL")
        known: dict[str, str] = {}

        steps = [
            ("transaction_type", "rent"),
            ("property_type", "apartment"),
            ("city", "Douala"),
            ("district", "Bonamoussadi"),
            ("budget_xaf", "250000"),
            ("bedrooms", "3"),
            ("bathrooms", "2"),
            ("kitchens", "1"),
        ]
        for slot, val in steps:
            next_q = self.registry.resolve_priority(journey, known)
            self.assertEqual(next_q, slot)
            known[slot] = val

    def test_land_yaounde_nkolbisson_scenario(self) -> None:
        """Land purchase: Yaounde, Nkolbisson"""
        journey = self.registry.get_journey("SEARCH_LAND")
        known: dict[str, str] = {}

        steps = [
            ("transaction_type", "buy"),
            ("city", "Yaounde"),
            ("district", "Nkolbisson"),
            ("intended_use", "construction"),
            ("surface_m2", "500"),
            ("budget_xaf", "15000000"),
        ]
        for slot, val in steps:
            next_q = self.registry.resolve_priority(journey, known)
            self.assertEqual(next_q, slot)
            known[slot] = val

    def test_bonjour_sequence(self) -> None:
        """Bonjour -> Je cherche un appartement -> Je veux louer -> Douala -> Budget"""
        journey = self.registry.get_journey("SEARCH_RENTAL")
        known: dict[str, str] = {}

        next_q = self.registry.resolve_priority(journey, known)
        self.assertEqual(next_q, "transaction_type")

        known["transaction_type"] = "rent"
        next_q = self.registry.resolve_priority(journey, known)
        self.assertEqual(next_q, "property_type")

        known["property_type"] = "apartment"
        next_q = self.registry.resolve_priority(journey, known)
        self.assertEqual(next_q, "city")

        known["city"] = "Douala"
        next_q = self.registry.resolve_priority(journey, known)
        self.assertEqual(next_q, "district")

    def test_studio_skip_bedrooms_in_multiturn(self) -> None:
        """Verify bedrooms/bathrooms/kitchens are never asked for studio."""
        journey = self.registry.get_journey("SEARCH_RENTAL")
        known: dict[str, str] = {
            "transaction_type": "rent",
            "property_type": "studio",
        }
        while True:
            next_q = self.registry.resolve_priority(journey, known)
            if next_q is None:
                break
            self.assertNotIn(next_q, ("bedrooms", "bathrooms", "kitchens"))
            known[next_q] = f"val_{next_q}"

    def test_each_journey_completes(self) -> None:
        """Every journey can be completed by filling all priority slots."""
        for j in self.registry.all_journeys():
            known: dict[str, str] = {}
            for slot in j.priority_order:
                known[slot] = f"val_{slot}"
            result = self.registry.resolve_priority(j, known)
            self.assertIsNone(
                result,
                f"Journey {j.journey_code} should return None "
                f"when all slots are filled, got '{result}'",
            )


if __name__ == "__main__":
    unittest.main()
