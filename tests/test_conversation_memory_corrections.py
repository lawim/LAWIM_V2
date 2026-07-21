"""Test slot corrections via the Fact model: superseded facts, history preserved."""

from __future__ import annotations

import sqlite3
import unittest
from datetime import datetime

from lawim_v2.conversation.domain.facts import Fact, FactCollection, FactStatus
from lawim_v2.conversation.memory.repository import MemoryRepository
from lawim_v2.conversation.memory.service import MemoryService


class _MemoryWrapper:
    """Wraps a raw sqlite3 connection so that execute() with RETURNING
    returns a dict-like row instead of a cursor."""

    def __init__(self, conn):
        self.conn = conn

    def execute(self, sql: str, params: object = ()) -> dict | None:
        cur = self.conn.execute(sql, params or ())
        if cur.description:
            row = cur.fetchone()
            self.conn.commit()
            return row
        self.conn.commit()
        return None

    def fetch_one(self, sql: str, params: object = ()) -> dict | None:
        cur = self.conn.execute(sql, params or ())
        row = cur.fetchone()
        self.conn.commit()
        return dict(row) if row else None

    def fetch_all(self, sql: str, params: object = ()) -> list[dict]:
        cur = self.conn.execute(sql, params or ())
        rows = [dict(row) for row in cur.fetchall()]
        self.conn.commit()
        return rows


def _make_memory_db():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS conversation_facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            field TEXT NOT NULL,
            raw_value TEXT,
            normalized_value TEXT,
            source_message_id TEXT,
            source_channel TEXT,
            source_type TEXT DEFAULT 'explicit',
            confidence REAL DEFAULT 1.0,
            confirmation_status TEXT DEFAULT 'EXPLICIT',
            project_id INTEGER,
            dossier_id INTEGER,
            conversation_id INTEGER,
            supersedes_fact_id TEXT,
            valid_from TEXT,
            valid_to TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    """)
    conn.commit()
    return _MemoryWrapper(conn)


class TestSlotCorrections(unittest.TestCase):
    def setUp(self):
        self.db = _make_memory_db()
        self.repo = MemoryRepository(self.db)
        self.service = MemoryService(self.repo)

    def tearDown(self):
        pass

    def test_budget_correction(self):
        initial = self.service.add_fact(
            field="budget_max", raw_value="150000",
            normalized_value=150000,
            conversation_id=1,
        )
        corrected = self.service.handle_correction(
            field="budget_max",
            old_fact_id=initial.fact_id,
            new_raw_value="180000",
            new_normalized=180000,
            conversation_id=1,
        )
        self.assertEqual(corrected.raw_value, "180000")
        self.assertEqual(corrected.normalized_value, 180000)
        self.assertEqual(corrected.supersedes_fact_id, initial.fact_id)

    def test_district_correction(self):
        initial = self.service.add_fact(
            field="district", raw_value="Bonamoussadi",
            conversation_id=1,
        )
        corrected = self.service.handle_correction(
            field="district",
            old_fact_id=initial.fact_id,
            new_raw_value="Makepe",
            conversation_id=1,
        )
        self.assertEqual(corrected.raw_value, "Makepe")

    def test_bedrooms_correction(self):
        initial = self.service.add_fact(
            field="bedrooms", raw_value="3",
            normalized_value=3,
            conversation_id=1,
        )
        corrected = self.service.handle_correction(
            field="bedrooms",
            old_fact_id=initial.fact_id,
            new_raw_value="2",
            new_normalized=2,
            conversation_id=1,
        )
        self.assertEqual(corrected.normalized_value, 2)

    def test_furnished_correction(self):
        initial = self.service.add_fact(
            field="furnished", raw_value="yes",
            conversation_id=1,
        )
        corrected = self.service.handle_correction(
            field="furnished",
            old_fact_id=initial.fact_id,
            new_raw_value="no",
            conversation_id=1,
        )
        self.assertEqual(corrected.raw_value, "no")

    def test_intent_change(self):
        initial = self.service.add_fact(
            field="intent", raw_value="rental_search",
            conversation_id=1,
        )
        corrected = self.service.handle_correction(
            field="intent",
            old_fact_id=initial.fact_id,
            new_raw_value="buy_search",
            conversation_id=1,
        )
        self.assertEqual(corrected.raw_value, "buy_search")

    def test_old_value_inactive_after_correction(self):
        initial = self.service.add_fact(
            field="city", raw_value="Douala",
            normalized_value="Douala",
            conversation_id=1,
        )
        self.service.handle_correction(
            field="city",
            old_fact_id=initial.fact_id,
            new_raw_value="Yaoundé",
            new_normalized="Yaoundé",
            conversation_id=1,
        )
        collection = self.service.get_confirmed_facts(conversation_id=1)
        active_cities = collection.get_active("city")
        self.assertEqual(len(active_cities), 1)
        self.assertEqual(active_cities[0].normalized_value, "Yaoundé")

    def test_history_preserved(self):
        self.service.add_fact(
            field="city", raw_value="Douala",
            conversation_id=1, project_id=1,
        )
        f2 = self.service.add_fact(
            field="city", raw_value="Yaoundé",
            conversation_id=1, project_id=1,
        )
        self.service.handle_correction(
            field="city",
            old_fact_id=f2.fact_id,
            new_raw_value="Bafoussam",
            conversation_id=1,
            project_id=1,
        )
        all_facts = self.repo.get_active_facts(
            conversation_id=1, project_id=1,
        )
        city_facts = [f for f in all_facts if f.field == "city"]
        # The correction only supersedes f2, so Douala (f1) + Bafoussam remain
        self.assertEqual(len(city_facts), 2)
        self.assertIn("Bafoussam", [f.raw_value for f in city_facts])

    def test_multiple_corrections_versioned(self):
        f1 = self.service.add_fact(
            field="budget_max", raw_value="100000",
            normalized_value=100000,
            conversation_id=1,
        )
        f2 = self.service.handle_correction(
            field="budget_max",
            old_fact_id=f1.fact_id,
            new_raw_value="150000",
            new_normalized=150000,
            conversation_id=1,
        )
        f3 = self.service.handle_correction(
            field="budget_max",
            old_fact_id=f2.fact_id,
            new_raw_value="200000",
            new_normalized=200000,
            conversation_id=1,
        )
        collection = self.service.get_confirmed_facts(conversation_id=1)
        active = collection.get_active("budget_max")
        self.assertEqual(len(active), 1)
        self.assertEqual(active[0].normalized_value, 200000)

    def test_correction_via_memory_service(self):
        f1 = self.service.add_fact(
            field="district", raw_value="Bonamoussadi",
            conversation_id=1,
        )
        corrected = self.service.handle_correction(
            field="district",
            old_fact_id=f1.fact_id,
            new_raw_value="Makepe",
            conversation_id=1,
        )
        self.assertIsNotNone(corrected.fact_id)
        self.assertNotEqual(corrected.fact_id, f1.fact_id)

        active = self.repo.get_active_facts(conversation_id=1)
        active_districts = [f for f in active if f.field == "district"]
        self.assertEqual(len(active_districts), 1)
        self.assertEqual(active_districts[0].raw_value, "Makepe")


class TestFactModelCorrections(unittest.TestCase):
    def test_fact_supersede_chain(self):
        fc = FactCollection()
        f1 = Fact(
            fact_id="1", field="budget", raw_value="100000",
            normalized_value=100000,
            confirmation_status=FactStatus.CONFIRMED,
            created_at="2025-01-01",
        )
        fc.add_fact(f1)
        f2 = Fact(
            fact_id="2", field="budget", raw_value="150000",
            normalized_value=150000,
            confirmation_status=FactStatus.CONFIRMED,
            supersedes_fact_id="1",
            created_at="2025-06-01",
        )
        fc.add_fact(f2)
        self.assertEqual(f1.confirmation_status, FactStatus.SUPERSEDED)
        self.assertIsNotNone(f1.valid_to)
        latest = fc.get_latest_confirmed("budget")
        self.assertEqual(latest.normalized_value, 150000)


if __name__ == "__main__":
    unittest.main()
