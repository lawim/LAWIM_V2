from __future__ import annotations

import sqlite3
import tempfile
import os
from datetime import datetime, timezone

import pytest

from lawim_v2.conversation.state.state import ConversationState, ConversationStateUpdate
from lawim_v2.conversation.state.repository import ConversationStateRepository
from lawim_v2.conversation.state.errors import StateConflictError


def _make_repo() -> tuple[ConversationStateRepository, str]:
    db = tempfile.mktemp(suffix=".db")
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    repo = ConversationStateRepository(conn)
    return repo, db


def _make_state(**overrides) -> ConversationState:
    now = datetime.now(timezone.utc).isoformat()
    kwargs = dict(
        actor_id="test",
        channel="whatsapp",
        channel_session_id="+237600000000",
        language="fr",
        created_at=now,
        updated_at=now,
    )
    kwargs.update(overrides)
    return ConversationState(**kwargs)


class TestNewFields:

    def test_case_id_default_none(self):
        state = _make_state()
        assert state.case_id is None

    def test_journey_code_default_empty(self):
        state = _make_state()
        assert state.journey_code == ""

    def test_state_version_default_1(self):
        state = _make_state()
        assert state.state_version == 1

    def test_updated_by_default_system(self):
        state = _make_state()
        assert state.updated_by == "system"

    def test_change_source_default_empty(self):
        state = _make_state()
        assert state.change_source == ""

    def test_increment_version(self):
        state = _make_state()
        state.increment_version()
        assert state.state_version == 2
        state.increment_version()
        assert state.state_version == 3

    def test_expected_version_default_none(self):
        state = _make_state()
        assert state.expected_version is None

    def test_case_id_in_update(self):
        update = ConversationStateUpdate(case_id="case-123")
        assert update.case_id == "case-123"


class TestOptimisticLocking:

    def test_insert_sets_state_version_1(self):
        repo, db_path = _make_repo()
        try:
            state = _make_state()
            saved = repo.save(state)
            assert saved.state_version == 1
            loaded = repo.load("whatsapp", "+237600000000")
            assert loaded is not None
            assert loaded.state_version == 1
        finally:
            os.unlink(db_path)

    def test_update_increments_state_version(self):
        repo, db_path = _make_repo()
        try:
            state = _make_state()
            repo.save(state)

            state.known_slots["city"] = "Douala"
            saved = repo.save(state)
            assert saved.state_version == 2
            loaded = repo.load("whatsapp", "+237600000000")
            assert loaded is not None
            assert loaded.state_version == 2
        finally:
            os.unlink(db_path)

    def test_consecutive_updates_increment_sequentially(self):
        repo, db_path = _make_repo()
        try:
            state = _make_state()
            repo.save(state)
            for i in range(1, 6):
                state.known_slots[f"key_{i}"] = i
                saved = repo.save(state)
                assert saved.state_version == i + 1
        finally:
            os.unlink(db_path)

    def test_expected_version_match_succeeds(self):
        repo, db_path = _make_repo()
        try:
            state = _make_state()
            repo.save(state)
            state.expected_version = 1
            state.known_slots["city"] = "Douala"
            saved = repo.save(state)
            assert saved.state_version == 2
        finally:
            os.unlink(db_path)

    def test_expected_version_mismatch_raises(self):
        repo, db_path = _make_repo()
        try:
            state = _make_state()
            repo.save(state)
            state.expected_version = 99
            state.known_slots["city"] = "Douala"
            with pytest.raises(StateConflictError) as exc:
                repo.save(state)
            assert exc.value.expected_version == 99
            assert exc.value.actual_version == 1
        finally:
            os.unlink(db_path)

    def test_conflict_error_message_contains_channel_info(self):
        repo, db_path = _make_repo()
        try:
            state = _make_state()
            repo.save(state)
            state.expected_version = 99
            with pytest.raises(StateConflictError) as exc:
                repo.save(state)
            assert "whatsapp" in str(exc.value)
            assert "+237600000000" in str(exc.value)
        finally:
            os.unlink(db_path)

    def test_concurrent_save_detects_stale_version(self):
        repo, db_path = _make_repo()
        try:
            state_a = _make_state()
            saved_a = repo.save(state_a)

            state_b = repo.load("whatsapp", "+237600000000")
            assert state_b is not None

            saved_a.known_slots["city"] = "Douala"
            repo.save(saved_a)

            state_b.known_slots["budget_max"] = 200000
            with pytest.raises(StateConflictError):
                repo.save(state_b)
        finally:
            os.unlink(db_path)

    def test_update_without_expected_version_uses_db_version(self):
        repo, db_path = _make_repo()
        try:
            state = _make_state()
            repo.save(state)

            state.expected_version = None
            state.known_slots["city"] = "Douala"
            saved = repo.save(state)
            assert saved.state_version == 2
        finally:
            os.unlink(db_path)

    def test_reload_returns_latest_state(self):
        repo, db_path = _make_repo()
        try:
            state = _make_state()
            repo.save(state)
            state.known_slots["city"] = "Douala"
            repo.save(state)
            reloaded = repo.reload("whatsapp", "+237600000000")
            assert reloaded is not None
            assert reloaded.state_version == 2
            assert reloaded.known_slots.get("city") == "Douala"
        finally:
            os.unlink(db_path)


class TestNewColumnsPersistence:

    def test_case_id_persisted(self):
        repo, db_path = _make_repo()
        try:
            state = _make_state(case_id="case-42")
            repo.save(state)
            loaded = repo.load("whatsapp", "+237600000000")
            assert loaded is not None
            assert loaded.case_id == "case-42"
        finally:
            os.unlink(db_path)

    def test_journey_code_persisted(self):
        repo, db_path = _make_repo()
        try:
            state = _make_state(journey_code="rent_apartment")
            repo.save(state)
            loaded = repo.load("whatsapp", "+237600000000")
            assert loaded is not None
            assert loaded.journey_code == "rent_apartment"
        finally:
            os.unlink(db_path)

    def test_updated_by_persisted(self):
        repo, db_path = _make_repo()
        try:
            state = _make_state(updated_by="ai_orchestrator")
            repo.save(state)
            loaded = repo.load("whatsapp", "+237600000000")
            assert loaded is not None
            assert loaded.updated_by == "ai_orchestrator"
        finally:
            os.unlink(db_path)

    def test_change_source_persisted(self):
        repo, db_path = _make_repo()
        try:
            state = _make_state(change_source="wizard_step_3")
            repo.save(state)
            loaded = repo.load("whatsapp", "+237600000000")
            assert loaded is not None
            assert loaded.change_source == "wizard_step_3"
        finally:
            os.unlink(db_path)

    def test_all_new_fields_roundtrip(self):
        repo, db_path = _make_repo()
        try:
            state = _make_state(
                case_id="case-99",
                journey_code="buy_house",
                state_version=1,
                updated_by="human_agent",
                change_source="manual_override",
            )
            repo.save(state)
            loaded = repo.load("whatsapp", "+237600000000")
            assert loaded is not None
            assert loaded.case_id == "case-99"
            assert loaded.journey_code == "buy_house"
            assert loaded.state_version == 1
            assert loaded.updated_by == "human_agent"
            assert loaded.change_source == "manual_override"
        finally:
            os.unlink(db_path)


class TestBackwardCompatibility:

    def test_old_state_still_works(self):
        repo, db_path = _make_repo()
        try:
            now = datetime.now(timezone.utc).isoformat()
            state = ConversationState(
                actor_id="test",
                channel="whatsapp",
                channel_session_id="+237600000001",
                language="fr",
                created_at=now,
                updated_at=now,
            )
            saved = repo.save(state)
            assert saved.state_version == 1
            loaded = repo.load("whatsapp", "+237600000001")
            assert loaded is not None
            assert loaded.state_version == 1
        finally:
            os.unlink(db_path)

    def test_existing_code_update_works(self):
        repo, db_path = _make_repo()
        try:
            state = _make_state()
            repo.save(state)
            state.known_slots["city"] = "Douala"
            result = repo.update(state)
            assert result.state_version == 2
        finally:
            os.unlink(db_path)

    def test_to_dict_includes_new_fields(self):
        state = _make_state(case_id="case-1", journey_code="rent")
        d = state.to_dict()
        assert d["case_id"] == "case-1"
        assert d["journey_code"] == "rent"
        assert d["state_version"] == 1
        assert d["updated_by"] == "system"
        assert d["change_source"] == ""
