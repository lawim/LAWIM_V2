from __future__ import annotations

import unittest

from lawim_v2.conversation.qualification.priority_registry import (
    QualificationPriorityRegistry,
)

_NEVER_ASK_SPONTANEOUSLY = {
    "parking", "pool", "piscine", "balcony", "balcon",
    "ac", "climatisation", "garden", "jardin", "generator",
    "groupe electrogene", "terrace", "terrasse", "elevator",
    "ascenseur", "internet", "security", "securite",
}


class TestNoOptionalSuggestion(unittest.TestCase):

    def setUp(self) -> None:
        self.registry = QualificationPriorityRegistry()

    def test_parking_not_in_any_priority_order(self) -> None:
        for j in self.registry.all_journeys():
            for forbidden in _NEVER_ASK_SPONTANEOUSLY:
                self.assertNotIn(
                    forbidden, j.priority_order,
                    f"Journey {j.journey_code} should NOT contain "
                    f"'{forbidden}' in priority_order",
                )

    def test_pool_not_in_any_priority_order(self) -> None:
        for j in self.registry.all_journeys():
            for forbidden in ("pool", "piscine"):
                self.assertNotIn(
                    forbidden, j.priority_order,
                    f"Journey {j.journey_code} should NOT contain "
                    f"'{forbidden}' in priority_order",
                )

    def test_balcony_not_in_any_priority_order(self) -> None:
        for j in self.registry.all_journeys():
            for forbidden in ("balcony", "balcon"):
                self.assertNotIn(
                    forbidden, j.priority_order,
                    f"Journey {j.journey_code} should NOT contain "
                    f"'{forbidden}' in priority_order",
                )

    def test_ac_not_in_any_priority_order(self) -> None:
        for j in self.registry.all_journeys():
            for forbidden in ("ac", "climatisation"):
                self.assertNotIn(
                    forbidden, j.priority_order,
                    f"Journey {j.journey_code} should NOT contain "
                    f"'{forbidden}' in priority_order",
                )

    def test_garden_not_in_any_priority_order(self) -> None:
        for j in self.registry.all_journeys():
            for forbidden in ("garden", "jardin"):
                self.assertNotIn(
                    forbidden, j.priority_order,
                    f"Journey {j.journey_code} should NOT contain "
                    f"'{forbidden}' in priority_order",
                )

    def test_generator_not_in_any_priority_order(self) -> None:
        for j in self.registry.all_journeys():
            for forbidden in ("generator", "groupe electrogene"):
                self.assertNotIn(
                    forbidden, j.priority_order,
                    f"Journey {j.journey_code} should NOT contain "
                    f"'{forbidden}' in priority_order",
                )

    def test_no_luxury_features_in_required_slots(self) -> None:
        for j in self.registry.all_journeys():
            for slot in j.required_slots:
                self.assertNotIn(
                    slot, _NEVER_ASK_SPONTANEOUSLY,
                    f"Journey {j.journey_code} has forbidden luxury "
                    f"feature '{slot}' in required_slots",
                )

    def test_no_luxury_features_in_conditional_slots(self) -> None:
        for j in self.registry.all_journeys():
            for cond in j.conditional_slots:
                slot = cond["slot"] if isinstance(cond, dict) else cond
                self.assertNotIn(
                    slot, _NEVER_ASK_SPONTANEOUSLY,
                    f"Journey {j.journey_code} has forbidden luxury "
                    f"feature '{slot}' in conditional_slots",
                )

    def test_resolve_priority_never_returns_luxury(self) -> None:
        for j in self.registry.all_journeys():
            known: dict = {}
            for slot_code in j.priority_order:
                if slot_code in _NEVER_ASK_SPONTANEOUSLY:
                    next_q = self.registry.resolve_priority(j, known)
                    self.assertNotEqual(
                        next_q, slot_code,
                        f"Journey {j.journey_code} should NEVER ask "
                        f"'{slot_code}' spontaneously",
                    )
                known[slot_code] = "test_value"

    def test_no_luxury_slots_defined_in_registry(self) -> None:
        slot_codes = {s.slot_code for s in self.registry.all_slots()}
        for forbidden in _NEVER_ASK_SPONTANEOUSLY:
            self.assertNotIn(
                forbidden, slot_codes,
                f"Luxury feature '{forbidden}' should not be a registered slot",
            )


if __name__ == "__main__":
    unittest.main()
