from __future__ import annotations

import unittest

from lawim_v2.conversation.qualification.priority_registry import (
    QualificationPriorityRegistry,
)


class TestProgressiveWizardPriorityOrder(unittest.TestCase):

    def setUp(self) -> None:
        self.registry = QualificationPriorityRegistry()

    def _simulate_questions(self, journey_code: str, answers: list[tuple[str, str]]) -> list[str]:
        journey = self.registry.get_journey(journey_code)
        self.assertIsNotNone(journey, f"Unknown journey: {journey_code}")
        known: dict[str, str] = {}
        questions_asked: list[str] = []
        for slot_code, value in answers:
            next_q = self.registry.resolve_priority(journey, known)
            if next_q is not None:
                questions_asked.append(next_q)
            known[slot_code] = value
        next_q = self.registry.resolve_priority(journey, known)
        if next_q is not None:
            questions_asked.append(next_q)
        return questions_asked

    def test_studio_rental_question_order(self) -> None:
        answers = [
            ("transaction_type", "rent"),
            ("property_type", "studio"),
            ("city", "Douala"),
            ("district", "Akwa"),
            ("budget_xaf", "100000"),
            ("furnished", "true"),
            ("move_in_date", "next_month"),
            ("other_requirements", "none"),
        ]
        asked = self._simulate_questions("SEARCH_RENTAL", answers)
        expected = [
            "transaction_type",
            "property_type",
            "city",
            "district",
            "budget_xaf",
            "furnished",
            "move_in_date",
            "other_requirements",
        ]
        self.assertEqual(asked, expected)

    def test_apartment_rental_question_order(self) -> None:
        answers = [
            ("transaction_type", "rent"),
            ("property_type", "apartment"),
            ("city", "Douala"),
            ("district", "Akwa"),
            ("budget_xaf", "200000"),
            ("bedrooms", "3"),
            ("bathrooms", "2"),
            ("kitchens", "1"),
            ("furnished", "true"),
            ("move_in_date", "next_month"),
            ("other_requirements", "none"),
        ]
        asked = self._simulate_questions("SEARCH_RENTAL", answers)
        expected = [
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
        ]
        self.assertEqual(asked, expected)

    def test_house_purchase_question_order(self) -> None:
        answers = [
            ("property_type", "house"),
            ("city", "Yaounde"),
            ("district", "Nkolbisson"),
            ("budget_xaf", "50000000"),
            ("bedrooms", "4"),
            ("bathrooms", "3"),
            ("kitchens", "1"),
            ("financing_mode", "cash"),
            ("title_requirements", "clean_title"),
            ("other_requirements", "none"),
        ]
        asked = self._simulate_questions("SEARCH_PURCHASE", answers)
        expected = [
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
        ]
        self.assertEqual(asked, expected)

    def test_land_purchase_question_order(self) -> None:
        answers = [
            ("transaction_type", "buy"),
            ("city", "Yaounde"),
            ("district", "Nkolbisson"),
            ("intended_use", "construction"),
            ("surface_m2", "500"),
            ("budget_xaf", "10000000"),
            ("title_status", "available"),
            ("accessibility", "road"),
            ("utilities", "water_electricity"),
            ("other_requirements", "none"),
        ]
        asked = self._simulate_questions("SEARCH_LAND", answers)
        expected = [
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
        ]
        self.assertEqual(asked, expected)

    def test_publish_listing_question_order(self) -> None:
        answers = [
            ("actor_role", "owner"),
            ("transaction_type", "rent"),
            ("property_type", "apartment"),
            ("location", "Douala"),
            ("price", "200000"),
            ("description", "2-bedroom apartment in Akwa"),
            ("documents", "title_deed"),
            ("media", "photos"),
            ("availability", "immediate"),
            ("consent", "true"),
        ]
        asked = self._simulate_questions("PUBLISH_LISTING", answers)
        expected = [
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
        ]
        self.assertEqual(asked, expected)

    def test_property_visit_question_order(self) -> None:
        answers = [
            ("property_reference", "REF123"),
            ("preferred_date", "2026-08-15"),
            ("preferred_time_window", "morning"),
            ("contact_channel", "whatsapp"),
            ("attendee_count", "2"),
            ("confirmation", "true"),
        ]
        asked = self._simulate_questions("PROPERTY_VISIT", answers)
        expected = [
            "property_reference",
            "preferred_date",
            "preferred_time_window",
            "contact_channel",
            "attendee_count",
            "confirmation",
        ]
        self.assertEqual(asked, expected)

    def test_sell_property_question_order(self) -> None:
        answers = [
            ("actor_role", "owner"),
            ("property_type", "house"),
            ("city", "Douala"),
            ("district", "Bonamoussadi"),
            ("ownership_status", "owner"),
            ("documents_available", "title_deed"),
            ("surface_m2", "300"),
            ("asking_price", "75000000"),
            ("occupancy_status", "vacant"),
            ("inspection_availability", "weekdays"),
        ]
        asked = self._simulate_questions("SELL_PROPERTY", answers)
        expected = [
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
        ]
        self.assertEqual(asked, expected)

    def test_rent_out_property_question_order(self) -> None:
        answers = [
            ("actor_role", "owner"),
            ("property_type", "apartment"),
            ("city", "Douala"),
            ("district", "Akwa"),
            ("ownership_status", "owner"),
            ("documents_available", "title_deed"),
            ("furnished", "true"),
            ("monthly_rent", "300000"),
            ("charges", "25000"),
            ("availability_date", "2026-09-01"),
            ("inspection_availability", "weekends"),
        ]
        asked = self._simulate_questions("RENT_OUT_PROPERTY", answers)
        expected = [
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
        ]
        self.assertEqual(asked, expected)

    def test_document_assistance_question_order(self) -> None:
        answers = [
            ("document_type", "title_deed"),
            ("property_reference", "REF456"),
            ("document_owner", "seller"),
            ("requested_action", "verify"),
            ("document_availability", "digital"),
            ("consent", "true"),
        ]
        asked = self._simulate_questions("DOCUMENT_ASSISTANCE", answers)
        expected = [
            "document_type",
            "property_reference",
            "document_owner",
            "requested_action",
            "document_availability",
            "consent",
        ]
        self.assertEqual(asked, expected)

    def test_construction_service_question_order(self) -> None:
        answers = [
            ("service_type", "construction"),
            ("project_location", "Douala"),
            ("property_type", "house"),
            ("project_stage", "planning"),
            ("scope", "full_construction"),
            ("budget_range", "50000000-100000000"),
            ("timeline", "6_months"),
            ("documents_available", "blueprint"),
            ("preferred_contact", "phone"),
        ]
        asked = self._simulate_questions("CONSTRUCTION_SERVICE", answers)
        expected = [
            "service_type",
            "project_location",
            "property_type",
            "project_stage",
            "scope",
            "budget_range",
            "timeline",
            "documents_available",
            "preferred_contact",
        ]
        self.assertEqual(asked, expected)

    def test_professional_service_question_order(self) -> None:
        answers = [
            ("service_type", "architect"),
            ("project_location", "Douala"),
            ("property_type", "house"),
            ("project_stage", "design"),
            ("scope", "full_design"),
            ("timeline", "3_months"),
            ("preferred_contact", "email"),
        ]
        asked = self._simulate_questions("PROFESSIONAL_SERVICE", answers)
        expected = [
            "service_type",
            "project_location",
            "property_type",
            "project_stage",
            "scope",
            "timeline",
            "preferred_contact",
        ]
        self.assertEqual(asked, expected)


if __name__ == "__main__":
    unittest.main()
