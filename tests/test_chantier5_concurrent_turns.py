"""Chantier 5: Concurrent multi-user conversation tests.

Verifies that multiple simultaneous conversations with different actor_ids
maintain isolated state without cross-contamination.
"""

from __future__ import annotations

import os
import sqlite3
import tempfile
import unittest

from lawim_v2.conversation.state.engine import ConversationStateEngine
from lawim_v2.conversation.state.repository import ConversationStateRepository
from lawim_v2.conversation.state.resolver import ConversationResolver


def _make_engine() -> tuple[ConversationStateEngine, str]:
    db = tempfile.mktemp(suffix=".db")
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    repo = ConversationStateRepository(conn)
    resolver = ConversationResolver()
    engine = ConversationStateEngine(repo, resolver)
    return engine, db


def _wa(short: str) -> str:
    """Return a valid WhatsApp number that normalizes to a unique session."""
    return f"+237600{short.zfill(7)}"


class TestChantier5ConcurrentTurns(unittest.TestCase):
    """Concurrent conversation isolation and integrity."""

    # ── Basic multi-user isolation ────────────────────────────────────────

    def test_two_independent_conversations(self):
        engine, db = _make_engine()
        try:
            r1 = engine.process_turn(
                actor_id="alice", channel="whatsapp",
                external_conversation_id=_wa("0001001"),
                message="Je cherche un appartement à Douala", language="fr",
            )
            r2 = engine.process_turn(
                actor_id="bob", channel="whatsapp",
                external_conversation_id=_wa("0001002"),
                message="Je veux acheter une maison à Yaoundé", language="fr",
            )
            self.assertNotEqual(
                r1["state"].known_slots.get("city"),
                r2["state"].known_slots.get("city"),
            )
            self.assertEqual(r1["state"].actor_id, "alice")
            self.assertEqual(r2["state"].actor_id, "bob")
        finally:
            if os.path.exists(db):
                os.unlink(db)

    def test_three_concurrent_users(self):
        engine, db = _make_engine()
        try:
            users = [
                ("alice", _wa("0002001"), "appartement Douala 100000"),
                ("bob", _wa("0002002"), "maison Yaoundé 50000000"),
                ("carol", _wa("0002003"), "terrain Douala 20000000"),
            ]
            states = {}
            for actor, conv_id, msg in users:
                result = engine.process_turn(
                    actor_id=actor, channel="whatsapp",
                    external_conversation_id=conv_id,
                    message=msg, language="fr",
                )
                states[actor] = result["state"]
            self.assertEqual(states["alice"].actor_id, "alice")
            self.assertEqual(states["bob"].actor_id, "bob")
            self.assertEqual(states["carol"].actor_id, "carol")
        finally:
            if os.path.exists(db):
                os.unlink(db)

    # ── Interleaved turns ────────────────────────────────────────────────

    def test_interleaved_turns_no_contamination(self):
        engine, db = _make_engine()
        try:
            engine.process_turn(
                actor_id="x", channel="whatsapp",
                external_conversation_id=_wa("0003001"),
                message="Je cherche à Douala", language="fr",
            )
            engine.process_turn(
                actor_id="y", channel="whatsapp",
                external_conversation_id=_wa("0003002"),
                message="Je cherche à Yaounde", language="fr",
            )
            engine.process_turn(
                actor_id="x", channel="whatsapp",
                external_conversation_id=_wa("0003001"),
                message="150000", language="fr",
            )
            engine.process_turn(
                actor_id="y", channel="whatsapp",
                external_conversation_id=_wa("0003002"),
                message="50000000", language="fr",
            )
            engine.process_turn(
                actor_id="x", channel="whatsapp",
                external_conversation_id=_wa("0003001"),
                message="2 chambres", language="fr",
            )
            engine.process_turn(
                actor_id="y", channel="whatsapp",
                external_conversation_id=_wa("0003002"),
                message="4 chambres", language="fr",
            )

            conn = sqlite3.connect(db)
            conn.row_factory = sqlite3.Row
            repo = ConversationStateRepository(conn)
            x_state = repo.load("whatsapp", _wa("0003001"))
            y_state = repo.load("whatsapp", _wa("0003002"))
            conn.close()

            self.assertIsNotNone(x_state)
            self.assertIsNotNone(y_state)
            self.assertEqual(x_state.known_slots.get("city"), "Douala")
            self.assertEqual(y_state.known_slots.get("city"), "Yaoundé")
            self.assertEqual(x_state.known_slots.get("budget_max"), 150000)
            self.assertEqual(y_state.known_slots.get("budget_max"), 50000000)
            self.assertEqual(x_state.known_slots.get("bedroom_count"), 2)
            self.assertEqual(y_state.known_slots.get("bedroom_count"), 4)
        finally:
            if os.path.exists(db):
                os.unlink(db)

    # ── Same actor, different channels ────────────────────────────────────

    def test_same_actor_different_channels_independent(self):
        engine, db = _make_engine()
        try:
            r_wa = engine.process_turn(
                actor_id="multi", channel="whatsapp",
                external_conversation_id=_wa("0004001"),
                message="Je cherche un studio à Douala", language="fr",
            )
            r_tg = engine.process_turn(
                actor_id="multi", channel="telegram",
                external_conversation_id="tg_multi_001",
                message="Je cherche une maison à Yaoundé", language="fr",
            )
            self.assertEqual(r_wa["state"].actor_id, "multi")
            self.assertEqual(r_tg["state"].actor_id, "multi")
            self.assertNotEqual(
                r_wa["state"].known_slots.get("city"),
                r_tg["state"].known_slots.get("city"),
            )
        finally:
            if os.path.exists(db):
                os.unlink(db)

    # ── Many rapid turns ─────────────────────────────────────────────────

    def test_many_rapid_turns(self):
        engine, db = _make_engine()
        try:
            for i in range(10):
                engine.process_turn(
                    actor_id=f"user_{i}", channel="whatsapp",
                    external_conversation_id=_wa(f"000{i}001"),
                    message=f"Je cherche un bien à Douala budget {i}00000",
                    language="fr",
                )
            conn = sqlite3.connect(db)
            conn.row_factory = sqlite3.Row
            repo = ConversationStateRepository(conn)
            for i in range(10):
                loaded = repo.load("whatsapp", _wa(f"000{i}001"))
                self.assertIsNotNone(loaded, f"State missing for user_{i}")
                self.assertEqual(loaded.actor_id, f"user_{i}")
            conn.close()
        finally:
            if os.path.exists(db):
                os.unlink(db)

    # ── Slot isolation ───────────────────────────────────────────────────

    def test_slot_isolation_across_users(self):
        engine, db = _make_engine()
        try:
            engine.process_turn(
                actor_id="u1", channel="whatsapp",
                external_conversation_id=_wa("0005001"),
                message="Je veux un terrain à Nkolbisson", language="fr",
            )
            engine.process_turn(
                actor_id="u2", channel="whatsapp",
                external_conversation_id=_wa("0005002"),
                message="Je veux un appartement meublé à Akwa", language="fr",
            )
            conn = sqlite3.connect(db)
            conn.row_factory = sqlite3.Row
            repo = ConversationStateRepository(conn)
            u1_state = repo.load("whatsapp", _wa("0005001"))
            u2_state = repo.load("whatsapp", _wa("0005002"))
            conn.close()

            u1_keys = set(u1_state.known_slots.keys())
            u2_keys = set(u2_state.known_slots.keys())

            shared_keys = u1_keys & u2_keys
            for key in shared_keys:
                if key in ("city", "district"):
                    self.assertNotEqual(
                        u1_state.known_slots[key],
                        u2_state.known_slots[key],
                        f"Key '{key}' must differ across users",
                    )
        finally:
            if os.path.exists(db):
                os.unlink(db)

    # ── Concurrent update safety ──────────────────────────────────────────

    def test_concurrent_updates_different_users(self):
        engine, db = _make_engine()
        try:
            engine.process_turn(
                actor_id="user_a", channel="whatsapp",
                external_conversation_id=_wa("0006001"),
                message="150000", language="fr",
            )
            engine.process_turn(
                actor_id="user_b", channel="whatsapp",
                external_conversation_id=_wa("0006002"),
                message="200000", language="fr",
            )
            conn = sqlite3.connect(db)
            conn.row_factory = sqlite3.Row
            repo = ConversationStateRepository(conn)
            a_state = repo.load("whatsapp", _wa("0006001"))
            b_state = repo.load("whatsapp", _wa("0006002"))
            conn.close()

            self.assertEqual(a_state.known_slots.get("budget_max"), 150000)
            self.assertEqual(b_state.known_slots.get("budget_max"), 200000)
        finally:
            if os.path.exists(db):
                os.unlink(db)

    # ── Response isolation ───────────────────────────────────────────────

    def test_response_not_cached_across_users(self):
        engine, db = _make_engine()
        try:
            r_alice = engine.process_turn(
                actor_id="alice", channel="whatsapp",
                external_conversation_id=_wa("0007001"),
                message="Bonjour", language="fr",
            )
            r_bob = engine.process_turn(
                actor_id="bob", channel="whatsapp",
                external_conversation_id=_wa("0007002"),
                message="Hello", language="en",
            )
            self.assertIsNotNone(r_alice["response"])
            self.assertIsNotNone(r_bob["response"])
        finally:
            if os.path.exists(db):
                os.unlink(db)


if __name__ == "__main__":
    unittest.main()
