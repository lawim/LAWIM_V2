#!/usr/bin/env python3
"""LAWIM V2 - Mission 3B.1 Behavioral Homologation Corpus Runner.

Processes all conversations from the corpus through the real ConversationService.
Each conversation's messages are processed sequentially through the real
ConversationService.process_message() with an in-memory SQLite backend.

Usage:
    PYTHONPATH="code:tests" python3 -m tests.mission_3b.run_corpus
"""

from __future__ import annotations

import json
import os
import sqlite3
import sys
import time
import uuid
from datetime import datetime, timezone
from typing import Any

# ---- Disable maintenance mode BEFORE importing any service code ----
import lawim_v2.maintenance as _maint

_maint.MAINTENANCE_FLAGS["lawim_core_rebuild_maintenance_mode"] = False

from lawim_v2.conversation.domain.facts import Fact, FactStatus
from lawim_v2.conversation.domain.message import NormalizedMessage
from lawim_v2.conversation.domain.states import ConversationState
from lawim_v2.conversation.service import ConversationService
from lawim_v2.conversation.planning.planner import Planner
from lawim_v2.conversation.generation.composer import GenerativeComposer
from lawim_v2.conversation.memory.service import MemoryService
from lawim_v2.conversation.qualification.evaluator import QualificationEvaluator
from lawim_v2.conversation.generation.validator import ContentValidator
from lawim_v2.security.audit import AADAuditLogger

from tests.mission_3b.corpus import CONVERSATIONS


# ---------------------------------------------------------------------------
# In-memory SQLite database wrapper
# ---------------------------------------------------------------------------

class _Database:
    def __init__(self) -> None:
        self._conn = sqlite3.connect(":memory:")
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._create_tables()

    def _create_tables(self) -> None:
        self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                channel_identity_id INTEGER,
                channel TEXT NOT NULL DEFAULT '',
                state TEXT NOT NULL DEFAULT 'NEW',
                project_id INTEGER,
                dossier_id INTEGER,
                expected_input TEXT,
                last_question_field TEXT,
                question_repeat_count INTEGER DEFAULT 0,
                loop_score INTEGER DEFAULT 0,
                human_handover_requested INTEGER DEFAULT 0,
                created_at TEXT,
                updated_at TEXT
            );

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
                supersedes_fact_id INTEGER,
                valid_from TEXT,
                valid_to TEXT,
                created_at TEXT,
                updated_at TEXT
            );

            CREATE TABLE IF NOT EXISTS conversation_decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                decision_id TEXT,
                conversation_id INTEGER,
                user_id INTEGER,
                channel TEXT,
                project_id INTEGER,
                dossier_id INTEGER,
                raw_message TEXT,
                normalized_message TEXT,
                state_before TEXT,
                state_after TEXT,
                selected_intent TEXT,
                intent_confidence REAL DEFAULT 0.0,
                transaction_type TEXT,
                property_type TEXT,
                action TEXT,
                action_status TEXT,
                requires_clarification INTEGER DEFAULT 0,
                requires_human INTEGER DEFAULT 0,
                loop_detected INTEGER DEFAULT 0,
                decision_json TEXT,
                created_at TEXT
            );

            CREATE TABLE IF NOT EXISTS channel_identity_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                channel_identity_id INTEGER,
                channel TEXT,
                created_at TEXT
            );

            CREATE INDEX IF NOT EXISTS idx_conv_user ON conversations(user_id);
            CREATE INDEX IF NOT EXISTS idx_conv_ci ON conversations(channel_identity_id);
            CREATE INDEX IF NOT EXISTS idx_facts_project ON conversation_facts(project_id);
            CREATE INDEX IF NOT EXISTS idx_facts_conv ON conversation_facts(conversation_id);
            CREATE INDEX IF NOT EXISTS idx_decisions_conv ON conversation_decisions(conversation_id);
            CREATE INDEX IF NOT EXISTS idx_ci_links ON channel_identity_links(user_id, channel_identity_id);
        """)
        self._conn.commit()

    def execute(self, sql: str, params: tuple = ()) -> sqlite3.Cursor:
        return self._conn.execute(sql, params)

    def executemany(self, sql: str, seq: list[tuple]) -> sqlite3.Cursor:
        return self._conn.executemany(sql, seq)

    def one(self, sql: str, params: tuple = ()) -> dict[str, Any] | None:
        row = self._conn.execute(sql, params).fetchone()
        if row is None:
            return None
        return dict(row)

    def all(self, sql: str, params: tuple = ()) -> list[dict[str, Any]]:
        return [dict(r) for r in self._conn.execute(sql, params)]

    def scalar(self, sql: str, params: tuple = ()) -> Any:
        row = self._conn.execute(sql, params).fetchone()
        if row is None:
            return None
        return row[0]

    def commit(self) -> None:
        self._conn.commit()


# ---------------------------------------------------------------------------
# Repository implementing the interface expected by ConversationService
# ---------------------------------------------------------------------------

class _Repository:
    def __init__(self, db: _Database) -> None:
        self._db = db

    # -- Conversation lifecycle --

    def get_conversation(self, conversation_id: int) -> dict[str, Any] | None:
        return self._db.one(
            "SELECT * FROM conversations WHERE id = ?", (conversation_id,)
        )

    def list_conversations(
        self, channel_identity_id: int, limit: int = 1
    ) -> list[dict[str, Any]]:
        return self._db.all(
            "SELECT * FROM conversations WHERE channel_identity_id = ? ORDER BY updated_at DESC LIMIT ?",
            (channel_identity_id, limit),
        )

    def list_active_conversations(
        self, user_id: int, limit: int = 1
    ) -> list[dict[str, Any]]:
        return self._db.all(
            "SELECT * FROM conversations WHERE user_id = ? AND state NOT IN ('CLOSED', 'HUMAN_HANDOVER', 'ERROR') ORDER BY updated_at DESC LIMIT ?",
            (user_id, limit),
        )

    def create_conversation(
        self,
        user_id: int | None = None,
        channel_identity_id: int | None = None,
        channel: str | None = None,
        state: str = "NEW",
        project_id: int | None = None,
    ) -> dict[str, Any]:
        now = datetime.now(timezone.utc).isoformat()
        cursor = self._db.execute(
            """INSERT INTO conversations (user_id, channel_identity_id, channel, state, project_id, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (user_id, channel_identity_id, channel, state, project_id, now, now),
        )
        self._db.commit()
        return self._db.one("SELECT * FROM conversations WHERE id = ?", (cursor.lastrowid,)) or {}

    def update_conversation(
        self,
        conversation_id: int,
        state: str | None = None,
        project_id: int | None = None,
        dossier_id: int | None = None,
        updated_at: str | None = None,
        **kwargs: Any,
    ) -> None:
        now = updated_at or datetime.now(timezone.utc).isoformat()
        fields: dict[str, Any] = {"updated_at": now}
        if state is not None:
            fields["state"] = state
        if project_id is not None:
            fields["project_id"] = project_id
        if dossier_id is not None:
            fields["dossier_id"] = dossier_id
        if "expected_input" in kwargs:
            fields["expected_input"] = kwargs["expected_input"]
        if "last_question_field" in kwargs:
            fields["last_question_field"] = kwargs["last_question_field"]
        if "question_repeat_count" in kwargs:
            fields["question_repeat_count"] = kwargs["question_repeat_count"]
        if "loop_score" in kwargs:
            fields["loop_score"] = kwargs["loop_score"]
        if "human_handover_requested" in kwargs:
            fields["human_handover_requested"] = 1 if kwargs["human_handover_requested"] else 0
        assignments = ", ".join(f"{k} = ?" for k in fields)
        params = tuple(fields.values()) + (conversation_id,)
        self._db.execute(f"UPDATE conversations SET {assignments} WHERE id = ?", params)
        self._db.commit()

    # -- Decisions --

    def save_decision(self, decision_dict: dict[str, Any]) -> None:
        now = datetime.now(timezone.utc).isoformat()
        self._db.execute(
            """INSERT INTO conversation_decisions (
                decision_id, conversation_id, user_id, channel, project_id, dossier_id,
                raw_message, normalized_message, state_before, state_after,
                selected_intent, intent_confidence, transaction_type, property_type,
                action, action_status, requires_clarification, requires_human,
                loop_detected, decision_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                decision_dict.get("decision_id"),
                decision_dict.get("conversation_id"),
                decision_dict.get("user_id"),
                decision_dict.get("channel"),
                decision_dict.get("project_id"),
                decision_dict.get("dossier_id"),
                decision_dict.get("raw_message"),
                decision_dict.get("normalized_message"),
                decision_dict.get("state_before"),
                decision_dict.get("state_after"),
                decision_dict.get("selected_intent"),
                decision_dict.get("intent_confidence", 0.0),
                decision_dict.get("transaction_type"),
                decision_dict.get("property_type"),
                decision_dict.get("action"),
                decision_dict.get("action_status"),
                1 if decision_dict.get("requires_clarification") else 0,
                1 if decision_dict.get("requires_human") else 0,
                1 if decision_dict.get("loop_detected") else 0,
                json.dumps(decision_dict, ensure_ascii=False, default=str),
                now,
            ),
        )
        self._db.commit()

    # -- Projects / Dossiers (stubs) --

    def list_projects(self, user_id: int, status: str = "ACTIVE") -> list[dict[str, Any]]:
        return []

    def list_dossiers(self, project_id: int) -> list[dict[str, Any]]:
        return []

    # -- Channel identity linking --

    def find_channel_identity(
        self, user_id: int, channel_identity_id: int
    ) -> dict[str, Any] | None:
        return self._db.one(
            "SELECT * FROM channel_identity_links WHERE user_id = ? AND channel_identity_id = ?",
            (user_id, channel_identity_id),
        )

    def link_channel_identity(
        self, user_id: int, channel_identity_id: int, channel: str
    ) -> None:
        existing = self.find_channel_identity(user_id, channel_identity_id)
        if existing:
            return
        now = datetime.now(timezone.utc).isoformat()
        self._db.execute(
            "INSERT INTO channel_identity_links (user_id, channel_identity_id, channel, created_at) VALUES (?, ?, ?, ?)",
            (user_id, channel_identity_id, channel, now),
        )
        self._db.commit()


# ---------------------------------------------------------------------------
# Memory repository implementing the interface expected by MemoryService
# ---------------------------------------------------------------------------

class _MemoryRepository:
    def __init__(self, db: _Database) -> None:
        self._db = db

    def _row_to_fact(self, row: dict[str, Any]) -> Fact:
        return Fact(
            fact_id=str(row["id"]),
            field=row["field"],
            raw_value=row["raw_value"] or "",
            normalized_value=row["normalized_value"] or row["raw_value"],
            source_message_id=row["source_message_id"],
            source_channel=row["source_channel"],
            source_type=row["source_type"] or "explicit",
            confidence=row["confidence"] or 1.0,
            confirmation_status=FactStatus(row["confirmation_status"]) if row.get("confirmation_status") else FactStatus.EXPLICIT,
            project_id=row["project_id"],
            dossier_id=row["dossier_id"],
            conversation_id=row["conversation_id"],
            supersedes_fact_id=str(row["supersedes_fact_id"]) if row.get("supersedes_fact_id") else None,
            valid_from=row["valid_from"],
            valid_to=row["valid_to"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def save_fact(self, fact: Fact) -> Fact:
        now = datetime.now(timezone.utc).isoformat()
        cursor = self._db.execute(
            """INSERT INTO conversation_facts (
                field, raw_value, normalized_value, source_message_id, source_channel,
                source_type, confidence, confirmation_status, project_id, dossier_id,
                conversation_id, supersedes_fact_id, valid_from, valid_to, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                fact.field,
                fact.raw_value,
                str(fact.normalized_value) if fact.normalized_value is not None else None,
                fact.source_message_id,
                fact.source_channel,
                fact.source_type or "explicit",
                fact.confidence,
                fact.confirmation_status.value if isinstance(fact.confirmation_status, FactStatus) else (fact.confirmation_status or "EXPLICIT"),
                fact.project_id,
                fact.dossier_id,
                fact.conversation_id,
                int(fact.supersedes_fact_id) if fact.supersedes_fact_id else None,
                fact.valid_from or now,
                fact.valid_to,
                now,
                now,
            ),
        )
        self._db.commit()
        row = self._db.one("SELECT * FROM conversation_facts WHERE id = ?", (cursor.lastrowid,))
        if row is None:
            return fact
        return self._row_to_fact(row)

    def supersede_fact(self, fact_id: str, timestamp: str) -> None:
        now = datetime.now(timezone.utc).isoformat()
        self._db.execute(
            "UPDATE conversation_facts SET confirmation_status = ?, valid_to = ?, updated_at = ? WHERE id = ?",
            ("SUPERSEDED", timestamp, now, int(fact_id)),
        )
        self._db.commit()

    def get_active_facts(
        self,
        project_id: int | None = None,
        dossier_id: int | None = None,
        conversation_id: int | None = None,
    ) -> list[Fact]:
        conditions = ["valid_to IS NULL"]
        params: list[Any] = []
        if project_id is not None:
            conditions.append("project_id = ?")
            params.append(project_id)
        if dossier_id is not None:
            conditions.append("dossier_id = ?")
            params.append(dossier_id)
        if conversation_id is not None:
            conditions.append("conversation_id = ?")
            params.append(conversation_id)
        where = " AND ".join(conditions)
        rows = self._db.all(
            f"SELECT * FROM conversation_facts WHERE {where} ORDER BY created_at DESC",
            tuple(params),
        )
        return [self._row_to_fact(r) for r in rows]

    def get_latest_confirmed_fact(
        self, field: str, project_id: int | None = None
    ) -> Fact | None:
        conditions = ["field = ?", "valid_to IS NULL",
                       "confirmation_status IN ('CONFIRMED', 'EXPLICIT')"]
        params: list[Any] = [field]
        if project_id is not None:
            conditions.append("project_id = ?")
            params.append(project_id)
        where = " AND ".join(conditions)
        row = self._db.one(
            f"SELECT * FROM conversation_facts WHERE {where} ORDER BY created_at DESC LIMIT 1",
            tuple(params),
        )
        if row is None:
            return None
        return self._row_to_fact(row)

    def update_fact_status(self, fact_id: str, status: FactStatus) -> None:
        now = datetime.now(timezone.utc).isoformat()
        status_val = status.value if isinstance(status, FactStatus) else status
        self._db.execute(
            "UPDATE conversation_facts SET confirmation_status = ?, updated_at = ? WHERE id = ?",
            (status_val, now, int(fact_id)),
        )
        self._db.commit()

    def get_facts_by_status(
        self, status: FactStatus, project_id: int | None = None
    ) -> list[Fact]:
        status_val = status.value if isinstance(status, FactStatus) else status
        conditions = ["confirmation_status = ?", "valid_to IS NULL"]
        params: list[Any] = [status_val]
        if project_id is not None:
            conditions.append("project_id = ?")
            params.append(project_id)
        where = " AND ".join(conditions)
        rows = self._db.all(
            f"SELECT * FROM conversation_facts WHERE {where} ORDER BY created_at DESC",
            tuple(params),
        )
        return [self._row_to_fact(r) for r in rows]


# ---------------------------------------------------------------------------
# Simple config object
# ---------------------------------------------------------------------------

class _Config:
    pass


# ---------------------------------------------------------------------------
# Corpus runner
# ---------------------------------------------------------------------------

_CONVERSATION_ID_MAP: dict[str, int] = {}  # corpus_id -> db_id (set after create)


def _make_message(
    text: str,
    corpus_conv_id: str,
    idx: int,
    db_conv_id: int | None,
) -> NormalizedMessage:
    return NormalizedMessage(
        raw_text=text,
        normalized_text=text,
        channel="whatsapp",
        channel_message_id=f"{corpus_conv_id}-msg-{idx}",
        user_id=hash(corpus_conv_id) % (10**9) + 1000,
        channel_identity_id=hash(corpus_conv_id) % (10**9) + 1000,
        conversation_id=db_conv_id,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


def _run_corpus() -> dict[str, Any]:
    db = _Database()
    repository = _Repository(db)
    memory_repo = _MemoryRepository(db)
    config = _Config()

    planner = Planner()
    composer = GenerativeComposer()
    content_validator = ContentValidator()
    audit_logger = AADAuditLogger()
    qualification_evaluator = QualificationEvaluator()
    memory_service = MemoryService(memory_repo)

    service = ConversationService(
        repository=repository,
        memory_repo=memory_repo,
        config=config,
        planner=planner,
        memory_service=memory_service,
        qualification_evaluator=qualification_evaluator,
        composer=composer,
        content_validator=content_validator,
        audit_logger=audit_logger,
    )

    total_convs = len(CONVERSATIONS)
    total_msgs = sum(len(c.get("messages", [])) for c in CONVERSATIONS)

    results: dict[str, Any] = {
        "summary": {
            "total_conversations": total_convs,
            "total_messages": total_msgs,
            "total_errors": 0,
            "total_decisions": 0,
            "total_loops": 0,
            "total_handovers": 0,
            "total_clarifications": 0,
            "total_state_transitions": 0,
        },
        "conversations": [],
        "errors": [],
        "duration_seconds": 0.0,
    }

    start_ts = time.time()

    for conv_idx, conv in enumerate(CONVERSATIONS):
        corpus_id: str = conv.get("id", f"corpus-{conv_idx}")
        title: str = conv.get("title", "")
        category: str = conv.get("category", "")
        messages: list[dict[str, Any]] = conv.get("messages", [])

        conv_result: dict[str, Any] = {
            "corpus_id": corpus_id,
            "title": title,
            "category": category,
            "message_count": len(messages),
            "messages": [],
            "total_errors": 0,
            "final_state": None,
            "actions": [],
            "intents": [],
            "loop_count": 0,
            "error": None,
        }

        db_conv_id: int | None = None

        for msg_idx, msg_data in enumerate(messages):
            text: str = msg_data.get("user", "")
            expected: dict[str, Any] | None = msg_data.get("expected")

            message = _make_message(text, corpus_id, msg_idx, db_conv_id)

            try:
                result = service.process_message(message)
            except Exception as exc:
                conv_result["total_errors"] += 1
                results["summary"]["total_errors"] += 1
                err_entry = {
                    "corpus_id": corpus_id,
                    "message_index": msg_idx,
                    "text": text,
                    "error": str(exc),
                }
                conv_result["messages"].append({
                    "index": msg_idx,
                    "user": text,
                    "expected": expected,
                    "error": str(exc),
                })
                results["errors"].append(err_entry)
                continue

            decision = result.get("decision")
            response = result.get("response", "")
            state = result.get("state", "unknown")
            actions = result.get("actions", [])
            errs = result.get("errors", [])

            # Track db conversation_id after first message creates it
            if decision and hasattr(decision, "conversation_id") and decision.conversation_id is not None:
                db_conv_id = decision.conversation_id

            msg_entry: dict[str, Any] = {
                "index": msg_idx,
                "user": text,
                "expected": expected,
                "state": state,
                "response": response,
                "action": decision.action if decision else None,
                "intent": decision.selected_intent if decision else None,
                "requires_clarification": decision.requires_clarification if decision else False,
                "requires_human": decision.requires_human if decision else False,
                "loop_detected": decision.loop_detected if decision else False,
                "errors": errs,
            }
            conv_result["messages"].append(msg_entry)

            if errs:
                conv_result["total_errors"] += len(errs)
                results["summary"]["total_errors"] += len(errs)

            if decision and decision.action:
                conv_result["actions"].append(decision.action)

            if decision and decision.selected_intent:
                conv_result["intents"].append(decision.selected_intent)

            if decision and decision.loop_detected:
                conv_result["loop_count"] += 1
                results["summary"]["total_loops"] += 1

            if decision and decision.requires_human:
                results["summary"]["total_handovers"] += 1

            if decision and decision.requires_clarification:
                results["summary"]["total_clarifications"] += 1

            if decision and decision.state_before != decision.state_after:
                results["summary"]["total_state_transitions"] += 1

        results["summary"]["total_decisions"] += len(conv_result["messages"])

        last_msg = conv_result["messages"][-1] if conv_result["messages"] else {}
        conv_result["final_state"] = last_msg.get("state")

        results["conversations"].append(conv_result)

        if (conv_idx + 1) % 100 == 0 or conv_idx == total_convs - 1:
            elapsed = time.time() - start_ts
            rate = (conv_idx + 1) / elapsed if elapsed > 0 else 0
            print(
                f"[{conv_idx + 1:4d}/{total_convs}] "
                f"msgs={len(messages):2d} "
                f"errs={conv_result['total_errors']} "
                f"state={conv_result['final_state'] or '?'} "
                f"elapsed={elapsed:.1f}s "
                f"rate={rate:.1f} conv/s",
                flush=True,
            )

    elapsed = time.time() - start_ts
    results["duration_seconds"] = elapsed

    # Final summary
    s = results["summary"]
    print()
    print("=" * 60)
    print(f"  LAWIM V2 - Mission 3B.1 Corpus Runner Results")
    print("=" * 60)
    print(f"  Total conversations:  {s['total_conversations']}")
    print(f"  Total messages:       {s['total_messages']}")
    print(f"  Total decisions:      {s['total_decisions']}")
    print(f"  Total errors:         {s['total_errors']}")
    print(f"  Total loops:          {s['total_loops']}")
    print(f"  Total handovers:      {s['total_handovers']}")
    print(f"  Total clarifications: {s['total_clarifications']}")
    print(f"  State transitions:    {s['total_state_transitions']}")
    print(f"  Duration:             {elapsed:.2f}s")
    print(f"  Throughput:           {s['total_conversations'] / elapsed:.1f} conv/s")
    print(f"                        {s['total_messages'] / elapsed:.1f} msg/s")
    print("=" * 60)

    return results


def main() -> None:
    results = _run_corpus()

    output_path = "/tmp/mission-3b1-runner-results.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    print(f"\nDetailed results saved to {output_path}")


if __name__ == "__main__":
    main()
