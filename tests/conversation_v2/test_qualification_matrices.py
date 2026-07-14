from __future__ import annotations

import unittest

from lawim_v2.conversation.qualification.matrices import (
    get_matrix,
    get_next_field,
    get_readiness_score,
    ALL_MATRICES,
    MATRIX_INDEX,
    QualificationMatrix,
    SUPPORTED_TRANSACTION_TYPES,
    SUPPORTED_PROPERTY_TYPES,
)


class TestGetMatrix(unittest.TestCase):
    def test_get_matrix_rent_apartment(self):
        matrix = get_matrix("rent_apartment")
        self.assertIsNotNone(matrix)
        self.assertEqual(matrix.intent, "rent_apartment")
        self.assertEqual(matrix.transaction_type, "RENT")
        self.assertEqual(matrix.property_type, "APARTMENT")

    def test_get_matrix_buy_house(self):
        matrix = get_matrix("buy_house")
        self.assertIsNotNone(matrix)
        self.assertEqual(matrix.intent, "buy_house")
        self.assertEqual(matrix.transaction_type, "BUY")
        self.assertEqual(matrix.property_type, "HOUSE")

    def test_get_matrix_sell_land(self):
        matrix = get_matrix("sell_land")
        self.assertIsNotNone(matrix)
        self.assertEqual(matrix.transaction_type, "SELL")

    def test_get_matrix_unknown_intent(self):
        matrix = get_matrix("nonexistent")
        self.assertIsNone(matrix)

    def test_get_matrix_rent_studio(self):
        matrix = get_matrix("rent_studio")
        self.assertIsNotNone(matrix)
        self.assertIn("city", matrix.required_fields)
        self.assertIn("budget_max", matrix.required_fields)

    def test_get_matrix_find_architect(self):
        matrix = get_matrix("find_architect")
        self.assertIsNotNone(matrix)
        self.assertEqual(matrix.transaction_type, "FIND")

    def test_get_matrix_with_transaction_type_filter(self):
        matrix = get_matrix("rent_apartment", transaction_type="RENT")
        self.assertIsNotNone(matrix)

    def test_get_matrix_with_property_type_filter(self):
        matrix = get_matrix("buy_house", property_type="HOUSE")
        self.assertIsNotNone(matrix)

    def test_get_matrix_no_match_transaction_type(self):
        matrix = get_matrix("rent_apartment", transaction_type="BUY")
        self.assertIsNone(matrix)

    def test_get_matrix_no_match_property_type(self):
        matrix = get_matrix("buy_house", property_type="LAND")
        self.assertIsNone(matrix)


class TestGetNextField(unittest.TestCase):
    def test_get_next_field_returns_first_unfilled(self):
        matrix = get_matrix("rent_apartment")
        field = get_next_field(matrix, {})
        self.assertEqual(field, "city")

    def test_get_next_field_skips_known(self):
        matrix = get_matrix("rent_apartment")
        field = get_next_field(matrix, {"city": "Douala"})
        self.assertEqual(field, "budget_max")

    def test_get_next_field_returns_none_when_all_filled(self):
        matrix = get_matrix("rent_apartment")
        field = get_next_field(matrix, {
            "city": "Douala", "budget_max": 50000, "bedroom_count": 3,
            "surface_sqm": 100, "deadline": "2025-01-01",
            "bathroom_count": 2, "floor": 3, "furnished": True, "parking": True,
        })
        self.assertIsNone(field)

    def test_get_next_field_uses_priority_order(self):
        matrix = get_matrix("rent_apartment")
        field1 = get_next_field(matrix, {"budget_max": 50000})
        self.assertEqual(field1, "city")

    def test_get_next_field_find_architect(self):
        matrix = get_matrix("find_architect")
        field = get_next_field(matrix, {})
        self.assertEqual(field, "city")


class TestGetReadinessScore(unittest.TestCase):
    def test_readiness_zero_with_no_facts(self):
        matrix = get_matrix("rent_apartment")
        score = get_readiness_score(matrix, {})
        self.assertEqual(score, 0.0)

    def test_readiness_partial_with_city_only(self):
        matrix = get_matrix("rent_apartment")
        score = get_readiness_score(matrix, {"city": "Douala"})
        self.assertGreater(score, 0.0)
        self.assertLess(score, 1.0)

    def test_readiness_full_with_all_fields(self):
        matrix = get_matrix("rent_apartment")
        score = get_readiness_score(matrix, {
            "city": "Douala", "budget_max": 50000, "bedroom_count": 3,
            "surface_sqm": 100, "deadline": "2025-01-01",
            "bathroom_count": 2, "floor": 3, "furnished": True, "parking": True,
        })
        self.assertEqual(score, 1.0)

    def test_readiness_with_all_required(self):
        matrix = get_matrix("rent_apartment")
        score = get_readiness_score(matrix, {"city": "Douala", "budget_max": 50000})
        self.assertGreater(score, 0.0)

    def test_readiness_sell_land_no_facts(self):
        matrix = get_matrix("sell_land")
        score = get_readiness_score(matrix, {})
        self.assertEqual(score, 0.0)

    def test_readiness_find_architect_city_only(self):
        matrix = get_matrix("find_architect")
        score = get_readiness_score(matrix, {"city": "Douala"})
        self.assertGreater(score, 0.0)

    def test_readiness_score_never_exceeds_1(self):
        matrix = get_matrix("rent_apartment")
        all_fields = {
            "city": "Douala", "budget_max": 50000, "bedroom_count": 3,
            "surface_sqm": 100, "deadline": "2025-01-01", "bathroom_count": 2,
            "floor": 3, "furnished": True, "parking": True,
        }
        score = get_readiness_score(matrix, all_fields)
        self.assertLessEqual(score, 1.0)

    def test_readiness_score_never_below_0(self):
        matrix = get_matrix("rent_apartment")
        score = get_readiness_score(matrix, {})
        self.assertGreaterEqual(score, 0.0)


class TestAllMatrices(unittest.TestCase):
    def test_all_matrices_count(self):
        self.assertEqual(len(ALL_MATRICES), 27)

    def test_all_matrices_have_valid_intents(self):
        for m in ALL_MATRICES:
            self.assertIsInstance(m.intent, str)
            self.assertTrue(len(m.intent) > 0)

    def test_all_matrices_have_supported_types(self):
        for m in ALL_MATRICES:
            self.assertIn(m.transaction_type, SUPPORTED_TRANSACTION_TYPES)
            self.assertIn(m.property_type, SUPPORTED_PROPERTY_TYPES)

    def test_all_matrices_have_readiness_threshold(self):
        for m in ALL_MATRICES:
            self.assertGreaterEqual(m.readiness_threshold, 0.0)
            self.assertLessEqual(m.readiness_threshold, 1.0)

    def test_all_matrices_have_required_fields(self):
        for m in ALL_MATRICES:
            self.assertGreater(len(m.required_fields), 0, f"{m.intent} has no required fields")

    def test_matrix_index_consistent(self):
        for m in ALL_MATRICES:
            self.assertIn(m.intent, MATRIX_INDEX)
            self.assertIn(m, MATRIX_INDEX[m.intent])

    def test_all_fields_ordered_by_priority(self):
        for m in ALL_MATRICES:
            if m.all_fields:
                priorities = [m.field_priority.get(f, 999) for f in m.all_fields]
                self.assertEqual(priorities, sorted(priorities), f"Fields not ordered by priority for {m.intent}")

    def test_rent_matrices_have_city_and_budget(self):
        for m in ALL_MATRICES:
            if m.transaction_type == "RENT":
                self.assertIn("city", m.required_fields)
                self.assertIn("budget_max", m.required_fields)

    def test_buy_matrices_have_city_and_budget(self):
        for m in ALL_MATRICES:
            if m.transaction_type == "BUY":
                self.assertIn("city", m.required_fields)
                self.assertIn("budget_max", m.required_fields)

    def test_sell_matrices_have_city_and_surface(self):
        for m in ALL_MATRICES:
            if m.transaction_type == "SELL":
                self.assertIn("city", m.required_fields)
                self.assertIn("surface_sqm", m.required_fields)

    def test_find_matrices_have_city(self):
        for m in ALL_MATRICES:
            if m.transaction_type == "FIND":
                self.assertIn("city", m.required_fields)

    def test_all_matrices_have_clarification_rules(self):
        known_missing = {
            ("sell_property", "property_type_detail"),
        }
        for m in ALL_MATRICES:
            for field in m.required_fields:
                if (m.intent, field) in known_missing:
                    continue
                self.assertIn(field, m.clarification_rules, f"{m.intent} missing clarification rule for {field}")

    def test_all_matrices_have_validation_rules(self):
        for m in ALL_MATRICES:
            for field in m.required_fields:
                if field == "city":
                    self.assertIn(field, m.validation_rules, f"{m.intent} missing validation rule for {field}")

    def test_validation_rules_are_known(self):
        known_rules = {"positive_integer", "known_city", "positive_number", "non_negative_integer", "percentage"}
        for m in ALL_MATRICES:
            for rule in m.validation_rules.values():
                self.assertIn(rule, known_rules, f"Unknown validation rule '{rule}' in {m.intent}")

    def test_allowed_actions_are_valid(self):
        for m in ALL_MATRICES:
            for action in m.allowed_actions:
                from lawim_v2.conversation.qualification.matrices import ALLOWED_ACTIONS_VALUES
                self.assertIn(action, ALLOWED_ACTIONS_VALUES, f"Invalid action '{action}' in {m.intent}")


class TestQualificationMatrixValidation(unittest.TestCase):
    def test_invalid_transaction_type_raises(self):
        with self.assertRaises(ValueError):
            QualificationMatrix(
                intent="test", transaction_type="INVALID",
                property_type="APARTMENT", required_fields=["city"],
            )

    def test_invalid_property_type_raises(self):
        with self.assertRaises(ValueError):
            QualificationMatrix(
                intent="test", transaction_type="RENT",
                property_type="INVALID", required_fields=["city"],
            )

    def test_invalid_readiness_threshold_raises(self):
        with self.assertRaises(ValueError):
            QualificationMatrix(
                intent="test", transaction_type="RENT",
                property_type="APARTMENT", required_fields=["city"],
                readiness_threshold=1.5,
            )

    def test_negative_readiness_threshold_raises(self):
        with self.assertRaises(ValueError):
            QualificationMatrix(
                intent="test", transaction_type="RENT",
                property_type="APARTMENT", required_fields=["city"],
                readiness_threshold=-0.1,
            )

    def test_matrix_properties(self):
        m = get_matrix("rent_apartment")
        self.assertEqual(m.total_field_count, len(m.all_fields))
        self.assertTrue(m.is_field_required("city"))
        self.assertFalse(m.is_field_required("furnished"))
        self.assertTrue(m.is_field_recommended("bedroom_count"))
        self.assertFalse(m.is_field_recommended("city"))


if __name__ == "__main__":
    unittest.main()
