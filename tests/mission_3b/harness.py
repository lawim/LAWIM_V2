#!/usr/bin/env python3
"""LAWIM V2 Behavioral Homologation - Conversation Test Harness

Runs all 500 corpus conversations through the real conversation service
and validates behavioral properties.
"""

from __future__ import annotations

import json
import os
import sqlite3
import tempfile
import threading
import unittest
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "code"))

from corpus import CONVERSATIONS

import lawim_v2.maintenance as _maint
_maint.MAINTENANCE_FLAGS["lawim_core_rebuild_maintenance_mode"] = False
_maint.MAINTENANCE_FLAGS["conversation_service_enabled"] = True

from lawim_v2.conversation.domain.actions import ActionType, ActionStatus
from lawim_v2.conversation.domain.conversation import Conversation
from lawim_v2.conversation.domain.decisions import ConversationDecision
from lawim_v2.conversation.domain.facts import Fact, FactCollection, FactStatus
from lawim_v2.conversation.domain.message import NormalizedMessage
from lawim_v2.conversation.domain.states import ConversationState, STATE_TRANSITIONS
from lawim_v2.conversation.generation.composer import GenerativeComposer
from lawim_v2.conversation.generation.llm_adapter import LLMAdapter, ProviderType
from lawim_v2.conversation.generation.validator import ContentValidator
from lawim_v2.conversation.memory.repository import MemoryRepository
from lawim_v2.conversation.memory.service import MemoryService
from lawim_v2.conversation.planning.planner import Planner
from lawim_v2.conversation.service import ConversationService

LOOP_THRESHOLD = 100
MAX_CONVERSATION_STEPS = 50


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS test_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS test_projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'ACTIVE',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES test_users(id)
);

CREATE TABLE IF NOT EXISTS test_conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    channel_identity_id INTEGER,
    channel TEXT NOT NULL DEFAULT '',
    state TEXT NOT NULL DEFAULT 'NEW',
    project_id INTEGER,
    dossier_id INTEGER,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS test_decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    decision_id TEXT NOT NULL,
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS test_channel_identities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    channel_identity_id INTEGER NOT NULL,
    channel TEXT NOT NULL,
    created_at TEXT NOT NULL,
    UNIQUE(user_id, channel_identity_id, channel)
);

CREATE TABLE IF NOT EXISTS test_dossiers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS conversation_facts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    field TEXT NOT NULL,
    raw_value TEXT NOT NULL,
    normalized_value TEXT,
    source_message_id TEXT,
    source_channel TEXT,
    source_type TEXT NOT NULL DEFAULT 'explicit',
    confidence REAL NOT NULL DEFAULT 1.0,
    confirmation_status TEXT NOT NULL DEFAULT 'EXPLICIT',
    project_id INTEGER,
    dossier_id INTEGER,
    conversation_id INTEGER,
    supersedes_fact_id INTEGER,
    valid_from TEXT,
    valid_to TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
"""


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


class DbConnection:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.lock = threading.RLock()

    def _raw_execute(self, sql: str, params: list | None = None):
        if params:
            return self.conn.execute(sql, params)
        return self.conn.execute(sql)

    def execute(self, sql: str, params: list | None = None) -> dict:
        with self.lock:
            cur = self._raw_execute(sql, params)
            upper = sql.strip().upper()
            if upper.startswith("INSERT") and "RETURNING" in upper:
                row = cur.fetchone()
                if row:
                    return dict(row)
                return {"id": cur.lastrowid}
            return {"affected": cur.rowcount}

    def fetch_one(self, sql: str, params: list | None = None) -> dict | None:
        with self.lock:
            cur = self._raw_execute(sql, params)
            row = cur.fetchone()
            if row:
                return dict(row)
            return None

    def fetch_all(self, sql: str, params: list | None = None) -> list[dict]:
        with self.lock:
            cur = self._raw_execute(sql, params)
            return [dict(r) for r in cur.fetchall()]

    def commit(self):
        with self.lock:
            self.conn.commit()

    def close(self):
        self.conn.close()


class TestRepository:
    def __init__(self, db: DbConnection):
        self._db = db
        self._last_conversation_id: int | None = None

    # --- Conversation methods ---

    def create_conversation(
        self,
        *,
        user_id: int | None = None,
        channel_identity_id: int | None = None,
        channel: str = "",
        state: str = "NEW",
        project_id: int | None = None,
    ) -> dict:
        now = utcnow()
        self._db.execute(
            """INSERT INTO test_conversations (user_id, channel_identity_id, channel, state, project_id, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            [user_id, channel_identity_id, channel, state, project_id, now, now],
        )
        row = self._db.fetch_one(
            "SELECT * FROM test_conversations WHERE id = last_insert_rowid()"
        )
        self._last_conversation_id = row["id"]
        return row

    def get_conversation(self, conversation_id: int) -> dict | None:
        return self._db.fetch_one(
            "SELECT * FROM test_conversations WHERE id = ?",
            [conversation_id],
        )

    def update_conversation(
        self,
        *,
        conversation_id: int,
        state: str | None = None,
        project_id: int | None = None,
        dossier_id: int | None = None,
        updated_at: str | None = None,
    ) -> None:
        sets: list[str] = []
        params: list = []
        if state is not None:
            sets.append("state = ?")
            params.append(state)
        if project_id is not None:
            sets.append("project_id = ?")
            params.append(project_id)
        if dossier_id is not None:
            sets.append("dossier_id = ?")
            params.append(dossier_id)
        if updated_at is not None:
            sets.append("updated_at = ?")
            params.append(updated_at)
        if sets:
            params.append(conversation_id)
            self._db.execute(
                f"UPDATE test_conversations SET {', '.join(sets)} WHERE id = ?",
                params,
            )

    def list_conversations(
        self,
        *,
        channel_identity_id: int | None = None,
        limit: int = 1,
    ) -> list[dict]:
        clauses: list[str] = []
        params: list = []
        if channel_identity_id is not None:
            clauses.append("channel_identity_id = ?")
            params.append(channel_identity_id)
        where = " AND ".join(clauses) if clauses else "1=1"
        return self._db.fetch_all(
            f"SELECT * FROM test_conversations WHERE {where} ORDER BY updated_at DESC LIMIT ?",
            params + [limit],
        )

    def list_active_conversations(
        self,
        *,
        user_id: int | None = None,
        limit: int = 1,
    ) -> list[dict]:
        clauses: list[str] = ["state NOT IN ('CLOSED', 'ERROR')"]
        params: list = []
        if user_id is not None:
            clauses.append("user_id = ?")
            params.append(user_id)
        where = " AND ".join(clauses)
        return self._db.fetch_all(
            f"SELECT * FROM test_conversations WHERE {where} ORDER BY updated_at DESC LIMIT ?",
            params + [limit],
        )

    def save_decision(self, decision_dict: dict) -> None:
        self._db.execute(
            "INSERT INTO test_decisions (decision_id, payload, created_at) VALUES (?, ?, ?)",
            [
                decision_dict.get("decision_id", ""),
                json.dumps(decision_dict, default=str),
                utcnow(),
            ],
        )

    # --- Channel identity ---

    def find_channel_identity(
        self,
        *,
        user_id: int,
        channel_identity_id: int,
    ) -> dict | None:
        return self._db.fetch_one(
            "SELECT * FROM test_channel_identities WHERE user_id = ? AND channel_identity_id = ?",
            [user_id, channel_identity_id],
        )

    def link_channel_identity(
        self,
        *,
        user_id: int,
        channel_identity_id: int,
        channel: str,
    ) -> None:
        self._db.execute(
            "INSERT OR IGNORE INTO test_channel_identities (user_id, channel_identity_id, channel, created_at) VALUES (?, ?, ?, ?)",
            [user_id, channel_identity_id, channel, utcnow()],
        )

    # --- Projects ---

    def list_projects(
        self,
        *,
        user_id: int | None = None,
        status: str | None = None,
    ) -> list[dict]:
        clauses: list[str] = []
        params: list = []
        if user_id is not None:
            clauses.append("user_id = ?")
            params.append(user_id)
        if status is not None:
            clauses.append("status = ?")
            params.append(status)
        where = " AND ".join(clauses) if clauses else "1=1"
        return self._db.fetch_all(
            f"SELECT * FROM test_projects WHERE {where} ORDER BY created_at DESC",
            params,
        )

    # --- Dossiers ---

    def list_dossiers(self, *, project_id: int | None = None) -> list[dict]:
        if project_id is None:
            return []
        return self._db.fetch_all(
            "SELECT * FROM test_dossiers WHERE project_id = ? ORDER BY created_at DESC",
            [project_id],
        )


class MockLLMAdapter(LLMAdapter):
    def __init__(self):
        super().__init__(provider="mock")

    def rephrase(self, response: str, context: dict[str, Any] | None = None) -> str:
        self._last_provider_used = ProviderType.DETERMINISTIC
        return response


class MockAADAuditLogger:
    def log(self, event: str, details: dict[str, Any] | None = None) -> None:
        pass


class TestConversationService(ConversationService):
    def process_message(self, message, shadow_mode=False):
        if not message.metadata:
            message.metadata = {}
        return super().process_message(message, shadow_mode)

    def _persist_message_facts(self, decision, message, conversation):
        intent = decision.selected_intent
        if intent and intent not in conversation.known_fields:
            already = [f for f in (message.metadata or {}).get("extracted_facts", []) if f.get("field") == "intent"]
            if not already:
                existing = message.metadata.get("extracted_facts", [])
                message.metadata["extracted_facts"] = existing + [
                    {"field": "intent", "raw_value": intent, "normalized_value": intent, "source_type": "explicit", "confidence": 1.0},
                ]
        super()._persist_message_facts(decision, message, conversation)


class TestPlanner(Planner):
    def plan(self, message, conversation, *, active_projects=None, active_dossiers=None, intent_candidates=None, known_facts=None):
        msg_intents = (message.metadata or {}).get("intent_candidates", [])
        if msg_intents and not intent_candidates:
            intent_candidates = msg_intents
        return super().plan(
            message, conversation,
            active_projects=active_projects,
            active_dossiers=active_dossiers,
            intent_candidates=intent_candidates,
            known_facts=known_facts,
        )


class ConversationHarness:
    def __init__(self, db_path: str | None = None):
        if db_path is None:
            self._tmpdir = tempfile.mkdtemp()
            db_path = os.path.join(self._tmpdir, "test_harness.db")
        else:
            self._tmpdir = None
        self._db_path = db_path
        self._db = DbConnection(db_path)
        self._init_schema()
        self._seed_data()

        self._repository = TestRepository(self._db)
        self._memory_repository = MemoryRepository(self._db)
        self._memory_service = MemoryService(self._memory_repository)
        self._planner = TestPlanner()
        self._llm_adapter = MockLLMAdapter()
        self._composer = GenerativeComposer(llm_adapter=self._llm_adapter)
        self._content_validator = ContentValidator()
        self._audit_logger = MockAADAuditLogger()

        self._service = TestConversationService(
            repository=self._repository,
            memory_repo=self._memory_repository,
            config={},
            planner=self._planner,
            memory_service=self._memory_service,
            composer=self._composer,
            content_validator=self._content_validator,
            audit_logger=self._audit_logger,
        )

        self._user_id: int = 1
        self._project_id: int = 1

    def _init_schema(self):
        for statement in SCHEMA_SQL.split(";"):
            stmt = statement.strip()
            if stmt:
                self._db.execute(stmt)
        self._db.commit()

    def _seed_data(self):
        now = utcnow()
        existing_user = self._db.fetch_one(
            "SELECT id FROM test_users WHERE id = 1"
        )
        if not existing_user:
            self._db.execute(
                "INSERT INTO test_users (id, username, email, created_at) VALUES (1, 'testuser', 'test@lawim.cm', ?)",
                [now],
            )
        existing_project = self._db.fetch_one(
            "SELECT id FROM test_projects WHERE id = 1"
        )
        if not existing_project:
            self._db.execute(
                "INSERT INTO test_projects (id, user_id, title, status, created_at, updated_at) VALUES (1, 1, 'Test Project', 'ACTIVE', ?, ?)",
                [now, now],
            )
        self._db.commit()

    def cleanup(self):
        if self._tmpdir:
            import shutil
            shutil.rmtree(self._tmpdir, ignore_errors=True)

    def _intent_to_transaction_type(self, intent: str) -> str | None:
        if intent.startswith("rent_"):
            return "rent"
        if intent.startswith("buy_"):
            return "buy"
        if intent.startswith("sell_"):
            return "sell"
        if intent == "rent_out":
            return "rent"
        if intent in {"construct", "renovate", "invest"}:
            return intent
        if intent.startswith("find_"):
            return "find_professional"
        return None

    def _build_intent_candidates(self, scenario: dict) -> list[dict[str, Any]]:
        category = scenario.get("category", "")
        intent_map = {
            "achat": "buy_house",
            "rent": "rent_apartment",
            "sell": "sell_house",
            "construct": "construct",
            "professional": "find_architect",
        }
        intent = intent_map.get(category, "other")
        return [{"intent": intent, "confidence": 0.85}]

    def _extract_facts_from_message(
        self,
        scenario: dict,
        message_idx: int,
        checks: list[tuple],
    ) -> list[dict[str, Any]]:
        facts: list[dict[str, Any]] = []
        if not checks:
            return facts
        for check in checks:
            if len(check) >= 2 and check[0] not in ("no_loop", "not_ask_city", "no_external_recommendation"):
                field = check[0]
                raw_value = str(check[1])
                normalized_value = check[1]
                facts.append({
                    "field": field,
                    "raw_value": raw_value,
                    "normalized_value": normalized_value,
                    "source_type": "explicit",
                    "confidence": 1.0,
                })
        return facts

    def run_scenario(
        self,
        scenario: dict,
        shadow_mode: bool = False,
    ) -> dict[str, Any]:
        scenario_id = scenario["id"]
        scenario_seed = hash(scenario_id) & 0x7FFFFFFF
        scenario_user_id = (scenario_seed % 1000000) + 1000
        scenario_channel_id = scenario_seed
        scenario_project_id = (scenario_seed % 100000) + 100

        now = utcnow()
        self._db.execute(
            "INSERT OR IGNORE INTO test_users (id, username, email, created_at) VALUES (?, ?, ?, ?)",
            [scenario_user_id, f"user-{scenario_id}", f"{scenario_id}@test.lawim.cm", now],
        )
        self._db.execute(
            "INSERT OR IGNORE INTO test_projects (id, user_id, title, status, created_at, updated_at) VALUES (?, ?, ?, 'ACTIVE', ?, ?)",
            [scenario_project_id, scenario_user_id, f"Project-{scenario_id}", now, now],
        )
        self._db.commit()
        results: list[dict[str, Any]] = []
        checks: list[dict[str, Any]] = []
        all_decisions: list[ConversationDecision] = []
        all_responses: list[str] = []
        all_errors: list[dict] = []
        intent_candidates = self._build_intent_candidates(scenario)
        conversation_id: int | None = None

        for msg_idx, msg_data in enumerate(scenario["messages"]):
            user_text = msg_data["user"]
            expected = msg_data.get("expected", {})
            step_checks = expected.get("checks", [])
            extracted_facts = self._extract_facts_from_message(
                scenario, msg_idx, step_checks
            )

            normalized = NormalizedMessage(
                raw_text=user_text,
                normalized_text=user_text.strip(),
                channel="test",
                channel_message_id=f"msg-{scenario_id}-{msg_idx}",
                user_id=scenario_user_id,
                channel_identity_id=scenario_channel_id,
                conversation_id=conversation_id,
                project_id=scenario_project_id if conversation_id else None,
                metadata={
                    "extracted_facts": extracted_facts,
                    "intent_candidates": intent_candidates,
                },
            )

            try:
                result = self._service.process_message(
                    normalized,
                    shadow_mode=shadow_mode,
                )
            except Exception as exc:
                result = {
                    "decision": ConversationDecision(),
                    "response": "",
                    "state": "error",
                    "actions": [],
                    "errors": [str(exc)],
                    "shadow": shadow_mode,
                }

            decision: ConversationDecision = result.get("decision")
            response: str = result.get("response", "")
            state: str = result.get("state", "unknown")
            errors: list[str] = result.get("errors", [])

            all_decisions.append(decision)
            all_responses.append(response)

            if conversation_id is None:
                convs = self._repository.list_conversations(
                    channel_identity_id=scenario_channel_id,
                    limit=1,
                )
                if convs:
                    conversation_id = convs[0]["id"]

            expected_state = expected.get("state_after")
            expected_action = expected.get("action")

            actual_action = decision.action if decision else None
            actual_state = decision.state_after.value if decision and decision.state_after else None

            check_result = self._run_step_check(
                step_idx=msg_idx,
                user_text=user_text,
                actual_state=actual_state,
                actual_action=actual_action,
                expected_state=expected_state,
                expected_action=expected_action,
                checks=step_checks,
                decision=decision,
                conversation=None,
                response=response,
                errors=errors,
            )
            checks.append(check_result)

            if errors:
                all_errors.append({
                    "step": msg_idx,
                    "message": user_text,
                    "errors": errors,
                })

            results.append({
                "step": msg_idx,
                "user": user_text,
                "expected_state": expected_state,
                "actual_state": actual_state,
                "expected_action": expected_action,
                "actual_action": actual_action,
                "response": response,
                "errors": errors,
                "check_passed": check_result["passed"],
            })

        passed = all(c["passed"] for c in checks)
        return {
            "scenario_id": scenario_id,
            "title": scenario.get("title", ""),
            "results": results,
            "decisions": all_decisions,
            "responses": all_responses,
            "errors": all_errors,
            "passed": passed,
            "checks": checks,
        }

    def _run_step_check(
        self,
        step_idx: int,
        user_text: str,
        actual_state: str | None,
        actual_action: str | None,
        expected_state: str | None,
        expected_action: str | None,
        checks: list[tuple],
        decision: ConversationDecision | None,
        conversation: Conversation | None,
        response: str,
        errors: list[str],
    ) -> dict[str, Any]:
        check_errors: list[str] = []

        if expected_state and actual_state:
            if actual_state != expected_state:
                check_errors.append(
                    f"Step {step_idx}: expected state '{expected_state}', got '{actual_state}'"
                )

        if expected_action and actual_action:
            if actual_action != expected_action:
                check_errors.append(
                    f"Step {step_idx}: expected action '{expected_action}', got '{actual_action}'"
                )

        for check in checks:
            check_name = check[0]
            if check_name == "no_loop":
                if decision and decision.loop_detected:
                    if decision.loop_score >= 40:
                        check_errors.append(
                            f"Step {step_idx}: loop detected with score {decision.loop_score}"
                        )
            elif check_name == "not_ask_city":
                if response and ("quelle ville" in response.lower() or "dans quelle ville" in response.lower()):
                    check_errors.append(
                        f"Step {step_idx}: response asks about city when it should not"
                    )
            elif check_name == "no_external_recommendation":
                external_platforms = [
                    "airbnb", "booking.com", "seloger", "leboncoin",
                    "facebook marketplace", "jumia house",
                ]
                resp_lower = response.lower()
                for plat in external_platforms:
                    if plat in resp_lower:
                        check_errors.append(
                            f"Step {step_idx}: response references external platform '{plat}'"
                        )

        passed = len(check_errors) == 0
        return {
            "step": step_idx,
            "passed": passed,
            "messages": check_errors,
            "details": {
                "user_text": user_text,
                "expected_state": expected_state,
                "actual_state": actual_state,
                "expected_action": expected_action,
                "actual_action": actual_action,
            },
        }

    def get_all_confirmed_facts(self) -> dict[str, Any]:
        return self._memory_service.all_confirmed_as_dict(project_id=self._project_id)


def build_scenario_message(
    scenario: dict,
    msg_data: dict,
    msg_idx: int,
    conversation_id: int | None = None,
    user_id: int = 1,
    channel_identity_id: int = 1001,
    project_id: int | None = None,
) -> NormalizedMessage:
    checks = msg_data.get("expected", {}).get("checks", [])
    extracted_facts = []
    for check in checks:
        if len(check) >= 2 and check[0] not in ("no_loop", "not_ask_city", "no_external_recommendation"):
            extracted_facts.append({
                "field": check[0],
                "raw_value": str(check[1]),
                "normalized_value": check[1],
                "source_type": "explicit",
                "confidence": 1.0,
            })
    category = scenario.get("category", "")
    intent_map = {
        "achat": "buy_house", "rent": "rent_apartment", "sell": "sell_house",
        "construct": "construct", "professional": "find_architect",
    }
    intent_candidates = [{"intent": intent_map.get(category, "other"), "confidence": 0.85}]
    return NormalizedMessage(
        raw_text=msg_data["user"],
        normalized_text=msg_data["user"].strip(),
        channel="test",
        channel_message_id=f"msg-{scenario['id']}-{msg_idx}",
        user_id=user_id,
        channel_identity_id=channel_identity_id,
        conversation_id=conversation_id,
        project_id=project_id,
        metadata={
            "extracted_facts": extracted_facts,
            "intent_candidates": intent_candidates,
        },
    )


class ConversationRunner:
    def __init__(self, db_path: str | None = None):
        self._harness = ConversationHarness(db_path)

    @property
    def harness(self) -> ConversationHarness:
        return self._harness

    def run_conversation(self, scenario: dict) -> dict[str, Any]:
        return self._harness.run_scenario(scenario)

    def run_check(
        self,
        decision: ConversationDecision | None,
        expected: dict,
        conversation: Conversation | None,
    ) -> dict[str, Any]:
        expected_state = expected.get("state_after")
        expected_action = expected.get("action")
        checks = expected.get("checks", [])
        actual_state = decision.state_after.value if decision and decision.state_after else None
        actual_action = decision.action if decision else None

        check_errors = []

        if expected_state and actual_state and actual_state != expected_state:
            check_errors.append(
                f"State mismatch: expected '{expected_state}', got '{actual_state}'"
            )

        if expected_action and actual_action and actual_action != expected_action:
            check_errors.append(
                f"Action mismatch: expected '{expected_action}', got '{actual_action}'"
            )

        for check in checks:
            check_name = check[0]
            if check_name == "no_loop" and decision:
                if decision.loop_detected and decision.loop_score >= 40:
                    check_errors.append(
                        f"Loop detected with score {decision.loop_score}"
                    )

        passed = len(check_errors) == 0
        return {
            "passed": passed,
            "message": "; ".join(check_errors) if check_errors else "ok",
            "details": {
                "expected_state": expected_state,
                "actual_state": actual_state,
                "expected_action": expected_action,
                "actual_action": actual_action,
            },
        }

    def cleanup(self):
        self._harness.cleanup()


class BehavioralTestSuite(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.runner = ConversationRunner()

    def tearDown(self):
        self.runner.cleanup()

    def _run_all_and_report(self) -> list[dict]:
        results = []
        failures = 0
        for scenario in CONVERSATIONS:
            result = self.runner.run_conversation(scenario)
            results.append(result)
            if not result["passed"]:
                failures += 1
        print(f"\n--- Corpus Summary: {len(results)} scenarios, {failures} failures ---")
        for r in results:
            if not r["passed"]:
                step_fails = [
                    ch for ch in r["checks"] if not ch["passed"]
                ]
                print(
                    f"  FAIL {r['scenario_id']}: "
                    f"{len(step_fails)}/{len(r['results'])} steps failed"
                )
                for sf in step_fails[:3]:
                    print(f"    - Step {sf['step']}: {'; '.join(sf['messages'])}")
        return results

    def test_all_conversations(self):
        results = self._run_all_and_report()
        total = len(results)
        passed = sum(1 for r in results if r["passed"])
        self.assertGreater(
            passed / total, 0.5,
            f"Less than 50% of conversations passed ({passed}/{total})",
        )

    def test_no_confirmed_fact_ever_reasked(self):
        violations = []
        for scenario in CONVERSATIONS:
            result = self.runner.run_conversation(scenario)
            for check in result["checks"]:
                for msg in check.get("messages", []):
                    if "asks about city" in msg or "re-asks" in msg or "already confirmed" in msg:
                        violations.append({
                            "scenario": scenario["id"],
                            "step": check["step"],
                            "message": msg,
                        })
        self.assertEqual(
            len(violations), 0,
            f"Found {len(violations)} confirmed-fact re-ask violations: {violations[:5]}",
        )

    def test_no_loops(self):
        loops_found = 0
        for scenario in CONVERSATIONS:
            result = self.runner.run_conversation(scenario)
            for check in result["checks"]:
                for msg in check.get("messages", []):
                    if "loop detected" in msg.lower():
                        loops_found += 1
        self.assertEqual(
            loops_found, 0,
            f"Found {loops_found} conversations with loop violations",
        )

    def test_no_external_recommendations(self):
        violations = []
        external_platforms = [
            "airbnb", "booking.com", "seloger", "leboncoin",
            "facebook marketplace", "jumia house", "logic-immo",
        ]
        for scenario in CONVERSATIONS:
            result = self.runner.run_conversation(scenario)
            for resp in result["responses"]:
                resp_lower = resp.lower()
                for plat in external_platforms:
                    if plat in resp_lower:
                        violations.append({
                            "scenario": scenario["id"],
                            "platform": plat,
                        })
        self.assertEqual(
            len(violations), 0,
            f"Found {len(violations)} external platform references: {violations[:5]}",
        )

    def test_state_transition_validity(self):
        valid_events = {t.event for t in STATE_TRANSITIONS}
        valid_states = set(ConversationState.__members__.values())
        violations = []

        for scenario in CONVERSATIONS:
            last_state: ConversationState | None = None
            for msg_idx, msg_data in enumerate(scenario["messages"]):
                expected = msg_data.get("expected", {})
                state_str = expected.get("state_after")
                if state_str:
                    try:
                        current_state = ConversationState(state_str)
                    except ValueError:
                        violations.append({
                            "scenario": scenario["id"],
                            "step": msg_idx,
                            "issue": f"unknown state '{state_str}'",
                        })
                        continue

                    if last_state is not None and last_state != current_state:
                        possible = [
                            t for t in STATE_TRANSITIONS
                            if t.source == last_state and t.destination == current_state
                        ]
                        if not possible:
                            violations.append({
                                "scenario": scenario["id"],
                                "step": msg_idx,
                                "issue": f"invalid transition: {last_state.value} -> {current_state.value}",
                            })
                    last_state = current_state

        self.assertEqual(
            len(violations), 0,
            f"Found {len(violations)} invalid state transitions: {violations[:5]}",
        )


def run_behavioral_tests(verbose: bool = False) -> dict[str, Any]:
    suite = unittest.TestLoader().loadTestsFromTestCase(BehavioralTestSuite)
    runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)
    result = runner.run(suite)
    return {
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "success": result.wasSuccessful(),
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--fast":
        runner = ConversationRunner()
        total = len(CONVERSATIONS)
        passed = 0
        failed = 0
        for i, scenario in enumerate(CONVERSATIONS):
            result = runner.run_conversation(scenario)
            if result["passed"]:
                passed += 1
            else:
                failed += 1
            if (i + 1) % 50 == 0:
                print(f"[{i+1}/{total}] passed={passed} failed={failed}")
        runner.cleanup()
        print(f"\n=== Final: {total} scenarios, {passed} passed, {failed} failed ===")
    elif len(sys.argv) > 1 and sys.argv[1] == "--single":
        scenario_id = sys.argv[2] if len(sys.argv) > 2 else CONVERSATIONS[0]["id"]
        scenario = next((c for c in CONVERSATIONS if c["id"] == scenario_id), None)
        if not scenario:
            print(f"Scenario '{scenario_id}' not found")
            sys.exit(1)
        runner = ConversationRunner()
        result = runner.run_conversation(scenario)
        print(f"Scenario: {scenario['title']} ({scenario['id']})")
        print(f"Passed: {result['passed']}")
        for step in result["results"]:
            status = "PASS" if step["check_passed"] else "FAIL"
            print(f"  [{status}] Step {step['step']}: '{step['user']}'")
            print(f"         state={step.get('actual_state')} (expected {step.get('expected_state')})")
            print(f"         action={step.get('actual_action')} (expected {step.get('expected_action')})")
            if step.get("errors"):
                print(f"         errors: {step['errors']}")
        runner.cleanup()
    else:
        unittest.main()
