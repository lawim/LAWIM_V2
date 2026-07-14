from __future__ import annotations

import unittest
from datetime import datetime
from uuid import uuid4

from lawim_v2.conversation.domain.facts import Fact, FactStatus, FactCollection, CONFIRMED_STATUSES, ACTIVE_STATUSES


class TestFactCreation(unittest.TestCase):
    def test_create_explicit_fact(self):
        f = Fact(field="city", raw_value="Douala", normalized_value="Douala", source_type="explicit")
        self.assertEqual(f.field, "city")
        self.assertEqual(f.normalized_value, "Douala")
        self.assertEqual(f.confirmation_status, FactStatus.EXPLICIT)
        self.assertEqual(f.source_type, "explicit")
        self.assertEqual(f.confidence, 1.0)

    def test_create_inferred_fact(self):
        f = Fact(field="city", raw_value="makepe", normalized_value="Makepe", source_type="inferred", confidence=0.9)
        self.assertEqual(f.confirmation_status, FactStatus.EXPLICIT)
        self.assertEqual(f.confidence, 0.9)

    def test_is_confirmed_returns_true_for_explicit(self):
        f = Fact(field="city", raw_value="Yaoundé", confirmation_status=FactStatus.EXPLICIT)
        self.assertTrue(f.is_confirmed())

    def test_is_confirmed_returns_true_for_confirmed(self):
        f = Fact(field="budget", raw_value="50000", confirmation_status=FactStatus.CONFIRMED)
        self.assertTrue(f.is_confirmed())

    def test_is_confirmed_returns_false_for_inferred(self):
        f = Fact(field="city", raw_value="makepe", confirmation_status=FactStatus.INFERRED)
        self.assertFalse(f.is_confirmed())

    def test_is_confirmed_returns_false_for_ambiguous(self):
        f = Fact(field="budget", raw_value="109 mil", confirmation_status=FactStatus.AMBIGUOUS)
        self.assertFalse(f.is_confirmed())

    def test_is_active_returns_true_for_unexpired_explicit(self):
        f = Fact(field="city", raw_value="Douala", confirmation_status=FactStatus.EXPLICIT, valid_to=None)
        self.assertTrue(f.is_active())

    def test_is_active_returns_false_when_valid_to_set(self):
        f = Fact(field="city", raw_value="Douala", confirmation_status=FactStatus.CONFIRMED, valid_to="2025-01-01")
        self.assertFalse(f.is_active())

    def test_is_active_returns_false_when_superseded(self):
        f = Fact(field="city", raw_value="Douala", confirmation_status=FactStatus.SUPERSEDED, valid_to=None)
        self.assertFalse(f.is_active())

    def test_supersede_creates_copy_with_superseded_status(self):
        original = Fact(
            fact_id="f1", field="city", raw_value="Douala",
            normalized_value="Douala", project_id=1,
        )
        superseded = original.supersede()
        self.assertEqual(superseded.confirmation_status, FactStatus.SUPERSEDED)
        self.assertEqual(superseded.field, "city")
        self.assertEqual(superseded.raw_value, "Douala")
        self.assertEqual(superseded.supersedes_fact_id, "f1")
        self.assertEqual(superseded.project_id, 1)
        self.assertIsNotNone(superseded.valid_to)

    def test_supersede_does_not_mutate_original(self):
        original = Fact(fact_id="f1", field="city", raw_value="Douala")
        original.supersede()
        self.assertIsNone(original.valid_to)
        self.assertEqual(original.confirmation_status, FactStatus.EXPLICIT)


class TestFactCollection(unittest.TestCase):
    def test_empty_collection(self):
        fc = FactCollection()
        self.assertEqual(fc.get_active(), [])
        self.assertEqual(fc.get_confirmed(), [])
        self.assertIsNone(fc.get_latest_confirmed("city"))

    def test_get_active_returns_all_active_facts(self):
        fc = FactCollection()
        fc.add_fact(Fact(field="city", raw_value="Douala", confirmation_status=FactStatus.CONFIRMED, fact_id="1"))
        fc.add_fact(Fact(field="budget", raw_value="50000", confirmation_status=FactStatus.INFERRED, fact_id="2"))
        active = fc.get_active()
        self.assertEqual(len(active), 2)

    def test_get_active_filters_by_field(self):
        fc = FactCollection()
        fc.add_fact(Fact(field="city", raw_value="Douala", confirmation_status=FactStatus.CONFIRMED, fact_id="1"))
        fc.add_fact(Fact(field="budget", raw_value="50000", confirmation_status=FactStatus.EXPLICIT, fact_id="2"))
        active_city = fc.get_active("city")
        self.assertEqual(len(active_city), 1)
        self.assertEqual(active_city[0].field, "city")

    def test_get_confirmed_returns_only_confirmed(self):
        fc = FactCollection()
        fc.add_fact(Fact(field="city", raw_value="Douala", confirmation_status=FactStatus.CONFIRMED, fact_id="1"))
        fc.add_fact(Fact(field="budget", raw_value="50000", confirmation_status=FactStatus.INFERRED, fact_id="2"))
        confirmed = fc.get_confirmed()
        self.assertEqual(len(confirmed), 1)
        self.assertEqual(confirmed[0].field, "city")

    def test_get_confirmed_filters_by_field(self):
        fc = FactCollection()
        fc.add_fact(Fact(field="city", raw_value="Douala", confirmation_status=FactStatus.CONFIRMED, fact_id="1"))
        fc.add_fact(Fact(field="budget", raw_value="50000", confirmation_status=FactStatus.EXPLICIT, fact_id="2"))
        city_confirmed = fc.get_confirmed("city")
        self.assertEqual(len(city_confirmed), 1)
        budget_confirmed = fc.get_confirmed("budget")
        self.assertEqual(len(budget_confirmed), 1)

    def test_get_latest_confirmed_returns_most_recent(self):
        fc = FactCollection()
        f1 = Fact(field="city", raw_value="Douala", normalized_value="Douala", confirmation_status=FactStatus.CONFIRMED, fact_id="1", created_at="2024-01-01")
        f2 = Fact(field="city", raw_value="Yaoundé", normalized_value="Yaoundé", confirmation_status=FactStatus.CONFIRMED, fact_id="2", created_at="2024-06-01")
        fc.add_fact(f1)
        fc.add_fact(f2)
        latest = fc.get_latest_confirmed("city")
        self.assertEqual(latest.normalized_value, "Yaoundé")

    def test_get_latest_confirmed_returns_none_for_missing_field(self):
        fc = FactCollection()
        fc.add_fact(Fact(field="city", raw_value="Douala", confirmation_status=FactStatus.CONFIRMED, fact_id="1"))
        self.assertIsNone(fc.get_latest_confirmed("budget"))

    def test_get_ambiguous_returns_only_ambiguous_facts(self):
        fc = FactCollection()
        fc.add_fact(Fact(field="budget", raw_value="109 mil", confirmation_status=FactStatus.AMBIGUOUS, fact_id="1"))
        fc.add_fact(Fact(field="city", raw_value="Douala", confirmation_status=FactStatus.CONFIRMED, fact_id="2"))
        ambiguous = fc.get_ambiguous()
        self.assertEqual(len(ambiguous), 1)
        self.assertEqual(ambiguous[0].field, "budget")

    def test_add_fact_with_supersession(self):
        fc = FactCollection()
        old = Fact(field="city", raw_value="Yaoundé", normalized_value="Yaoundé", confirmation_status=FactStatus.CONFIRMED, fact_id="f1")
        fc.add_fact(old)
        new = Fact(field="city", raw_value="Douala", normalized_value="Douala", confirmation_status=FactStatus.CONFIRMED, fact_id="f2", supersedes_fact_id="f1", created_at="2025-01-01")
        fc.add_fact(new)
        confirmed = fc.get_confirmed("city")
        self.assertEqual(len(confirmed), 1)
        self.assertEqual(confirmed[0].normalized_value, "Douala")
        self.assertEqual(confirmed[0].fact_id, "f2")
        self.assertEqual(old.confirmation_status, FactStatus.SUPERSEDED)
        self.assertIsNotNone(old.valid_to)

    def test_has_field_returns_true_when_confirmed(self):
        fc = FactCollection()
        fc.add_fact(Fact(field="city", raw_value="Douala", confirmation_status=FactStatus.CONFIRMED, fact_id="1"))
        self.assertTrue(fc.has_field("city"))
        self.assertFalse(fc.has_field("budget"))

    def test_has_field_returns_false_for_non_confirmed(self):
        fc = FactCollection()
        fc.add_fact(Fact(field="city", raw_value="makepe", confirmation_status=FactStatus.INFERRED, fact_id="1"))
        self.assertFalse(fc.has_field("city"))

    def test_all_confirmed_fields_returns_dict(self):
        fc = FactCollection()
        fc.add_fact(Fact(field="city", raw_value="Douala", normalized_value="Douala", confirmation_status=FactStatus.CONFIRMED, fact_id="1"))
        fc.add_fact(Fact(field="budget_max", raw_value="50000", normalized_value=50000, confirmation_status=FactStatus.EXPLICIT, fact_id="2"))
        fc.add_fact(Fact(field="bedroom_count", raw_value="3", confirmation_status=FactStatus.INFERRED, fact_id="3"))
        result = fc.all_confirmed_fields()
        self.assertEqual(result.get("city"), "Douala")
        self.assertEqual(result.get("budget_max"), 50000)
        self.assertNotIn("bedroom_count", result)

    def test_all_confirmed_fields_uses_normalized_value(self):
        fc = FactCollection()
        fc.add_fact(Fact(field="city", raw_value="douala", normalized_value="Douala", confirmation_status=FactStatus.CONFIRMED, fact_id="1"))
        result = fc.all_confirmed_fields()
        self.assertEqual(result["city"], "Douala")

    def test_all_confirmed_fields_falls_back_to_raw(self):
        fc = FactCollection()
        fc.add_fact(Fact(field="city", raw_value="Douala", normalized_value=None, confirmation_status=FactStatus.CONFIRMED, fact_id="1"))
        result = fc.all_confirmed_fields()
        self.assertEqual(result["city"], "Douala")

    def test_to_dict_returns_expected_structure(self):
        fc = FactCollection()
        fc.add_fact(Fact(field="city", raw_value="Douala", normalized_value="Douala", confirmation_status=FactStatus.CONFIRMED, source_type="explicit", fact_id="1"))
        fc.add_fact(Fact(field="budget", raw_value="109 mil", confirmation_status=FactStatus.AMBIGUOUS, fact_id="2"))
        fc.add_fact(Fact(field="bedroom_count", raw_value="3", confirmation_status=FactStatus.INFERRED, fact_id="3"))
        d = fc.to_dict()
        self.assertIn("confirmed", d)
        self.assertIn("ambiguous", d)
        self.assertIn("pending", d)
        self.assertEqual(len(d["confirmed"]), 1)
        self.assertEqual(len(d["ambiguous"]), 1)
        self.assertEqual(len(d["pending"]), 1)

    def test_fact_field_properties(self):
        now = datetime.utcnow().isoformat()
        f = Fact(
            fact_id="test-1",
            field="budget_max",
            raw_value="50 000",
            normalized_value=50000,
            source_message_id="msg-1",
            source_channel="telegram",
            source_type="explicit",
            confidence=1.0,
            project_id=1,
            dossier_id=2,
            conversation_id=3,
            valid_from=now,
            valid_to=None,
            supersedes_fact_id="prev-1",
            created_at=now,
            updated_at=now,
        )
        self.assertEqual(f.fact_id, "test-1")
        self.assertEqual(f.normalized_value, 50000)
        self.assertEqual(f.project_id, 1)
        self.assertEqual(f.dossier_id, 2)
        self.assertEqual(f.conversation_id, 3)
        self.assertEqual(f.supersedes_fact_id, "prev-1")
        self.assertTrue(f.is_confirmed())
        self.assertTrue(f.is_active())

    def test_superseded_fact_not_active(self):
        f = Fact(field="city", raw_value="Douala", confirmation_status=FactStatus.SUPERSEDED)
        self.assertFalse(f.is_active())

    def test_revoked_fact_not_confirmed(self):
        f = Fact(field="city", raw_value="Douala", confirmation_status=FactStatus.REVOKED)
        self.assertFalse(f.is_confirmed())

    def test_conflicting_fact_not_confirmed(self):
        f = Fact(field="city", raw_value="Douala", confirmation_status=FactStatus.CONFLICTING)
        self.assertFalse(f.is_confirmed())

    def test_fact_defaults(self):
        f = Fact()
        self.assertEqual(f.field, "")
        self.assertEqual(f.raw_value, "")
        self.assertIsNone(f.normalized_value)
        self.assertEqual(f.confirmation_status, FactStatus.EXPLICIT)
        self.assertEqual(f.confidence, 1.0)
        self.assertIsNone(f.fact_id)
        self.assertIsNone(f.project_id)

    def test_add_fact_appends_to_list(self):
        fc = FactCollection()
        self.assertEqual(len(fc.facts), 0)
        fc.add_fact(Fact(field="test", raw_value="val", confirmation_status=FactStatus.EXPLICIT, fact_id="1"))
        self.assertEqual(len(fc.facts), 1)


if __name__ == "__main__":
    unittest.main()
