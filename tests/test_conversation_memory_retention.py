"""Test memory retention policies, anonymization, and deletion audit logging.

Retention model and service are defined inline since the production modules
do not yet exist.  Once they do, these tests should import from the real
modules.
"""

from __future__ import annotations

import json
import re
import sqlite3
import unittest
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import uuid4


# ── Inline retention models ─────────────────────────────────────────────

class RetentionPeriod:
    ACTIVE_CONVERSATION = timedelta(days=365)
    COMPLETED_CONVERSATION = timedelta(days=180)
    HANDED_OVER = timedelta(days=365 * 3)
    ANONYMIZED_RETENTION = timedelta(days=90)
    MINIMUM_RETENTION = timedelta(days=30)


RETENTION_POLICIES: dict[str, timedelta] = {
    "active": RetentionPeriod.ACTIVE_CONVERSATION,
    "completed": RetentionPeriod.COMPLETED_CONVERSATION,
    "handed_over": RetentionPeriod.HANDED_OVER,
    "anonymized": RetentionPeriod.ANONYMIZED_RETENTION,
    "minimum": RetentionPeriod.MINIMUM_RETENTION,
}


@dataclass
class MemoryRetentionPolicy:
    policy_id: str = ""
    conversation_id: str = ""
    status: str = "active"
    retention_days: int = 365
    created_at: str = ""
    updated_at: str = ""

    def should_retain(self, reference_time: str | None = None) -> bool:
        ref = reference_time or datetime.now(timezone.utc).isoformat()
        try:
            created = datetime.fromisoformat(self.created_at)
            ref_dt = datetime.fromisoformat(ref)
            age = ref_dt - created
            return age.days < self.retention_days
        except (ValueError, TypeError):
            return True

    def is_expired(self, reference_time: str | None = None) -> bool:
        return not self.should_retain(reference_time)


@dataclass
class RetentionAuditLog:
    log_id: str = ""
    action: str = ""
    conversation_id: str = ""
    actor_id: str = ""
    details: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""


# ── Retention services ──────────────────────────────────────────────────

def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_id() -> str:
    return uuid4().hex[:16]


ANONYMIZATION_PATTERNS: dict[str, str] = {
    "phone": r"\+?\d[\d\s\-\(\)]{6,}\d",
    "email": r"[\w.+-]+@[\w-]+\.[\w.]+",
    "name": r"\b[A-Z][a-z]+ [A-Z][a-z]+\b",
}


def anonymize_field(value: str, field_type: str) -> str:
    pattern = ANONYMIZATION_PATTERNS.get(field_type)
    if pattern:
        return re.sub(pattern, "[REDACTED]", value)
    return value


def anonymize_actor_data(data: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in data.items():
        if key in ("phone", "email", "name", "full_name"):
            result[key] = anonymize_field(str(value), key)
        elif isinstance(value, dict):
            result[key] = anonymize_actor_data(value)
        elif isinstance(value, str):
            result[key] = anonymize_field(value, "name")
        else:
            result[key] = value
    return result


class _ConnectionWrapper:
    def __init__(self, conn):
        self.conn = conn

    def execute(self, sql: str, params: object = ()) -> Any:
        cur = self.conn.execute(sql, params or ())
        self.conn.commit()
        return cur

    def fetch_one(self, sql: str, params: object = ()) -> dict | None:
        cur = self.conn.execute(sql, params or ())
        row = cur.fetchone()
        return dict(row) if row else None

    def fetch_all(self, sql: str, params: object = ()) -> list[dict]:
        cur = self.conn.execute(sql, params or ())
        return [dict(row) for row in cur.fetchall()]


class MemoryRetentionService:
    def __init__(self, db):
        if not hasattr(db, "fetch_one"):
            db = _ConnectionWrapper(db)
        self.db = db
        self._ensure_tables()

    def _ensure_tables(self):
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS retention_policies (
                policy_id TEXT PRIMARY KEY,
                conversation_id TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'active',
                retention_days INTEGER NOT NULL DEFAULT 365,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS retention_audit_logs (
                log_id TEXT PRIMARY KEY,
                action TEXT NOT NULL,
                conversation_id TEXT NOT NULL,
                actor_id TEXT NOT NULL DEFAULT '',
                details TEXT NOT NULL DEFAULT '{}',
                created_at TEXT NOT NULL
            )
        """)

    def create_policy(self, conversation_id: str, retention_days: int = 365) -> MemoryRetentionPolicy:
        now = _utcnow()
        policy = MemoryRetentionPolicy(
            policy_id=_new_id(),
            conversation_id=conversation_id,
            status="active",
            retention_days=retention_days,
            created_at=now,
            updated_at=now,
        )
        self.db.execute(
            """INSERT INTO retention_policies (
                policy_id, conversation_id, status, retention_days, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?)""",
            [policy.policy_id, policy.conversation_id, policy.status,
             policy.retention_days, policy.created_at, policy.updated_at],
        )
        return policy

    def get_policy(self, conversation_id: str) -> MemoryRetentionPolicy | None:
        row = self.db.fetch_one(
            "SELECT * FROM retention_policies WHERE conversation_id = ? ORDER BY created_at DESC LIMIT 1",
            [conversation_id],
        )
        if not row:
            return None
        return MemoryRetentionPolicy(**row)


class MemoryDeletionService:
    def __init__(self, db):
        if not hasattr(db, "fetch_one"):
            db = _ConnectionWrapper(db)
        self.db = db
        self._ensure_tables()

    def _ensure_tables(self):
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS deletion_audit_logs (
                log_id TEXT PRIMARY KEY,
                action TEXT NOT NULL,
                conversation_id TEXT NOT NULL,
                actor_id TEXT NOT NULL DEFAULT '',
                details TEXT NOT NULL DEFAULT '{}',
                created_at TEXT NOT NULL
            )
        """)

    def log_deletion(
        self, conversation_id: str, actor_id: str = "system",
        details: dict | None = None,
    ) -> RetentionAuditLog:
        now = _utcnow()
        log = RetentionAuditLog(
            log_id=_new_id(),
            action="DELETE",
            conversation_id=conversation_id,
            actor_id=actor_id,
            details=details or {},
            created_at=now,
        )
        self.db.execute(
            """INSERT INTO deletion_audit_logs (
                log_id, action, conversation_id, actor_id, details, created_at
            ) VALUES (?, ?, ?, ?, ?, ?)""",
            [log.log_id, log.action, log.conversation_id, log.actor_id,
             json.dumps(log.details), log.created_at],
        )
        return log


class MemoryAnonymizationService:
    @staticmethod
    def anonymize_field(value: str, field_type: str) -> str:
        return anonymize_field(value, field_type)

    @staticmethod
    def anonymize_actor_data(data: dict[str, Any]) -> dict[str, Any]:
        return anonymize_actor_data(data)


class TestRetentionPolicy(unittest.TestCase):
    def test_retention_policy_defaults(self):
        policy = MemoryRetentionPolicy(
            policy_id="p1", conversation_id="c1",
            created_at=_utcnow(),
        )
        self.assertEqual(policy.retention_days, 365)
        self.assertEqual(policy.status, "active")

    def test_retention_policy_should_retain(self):
        created = (datetime.now(timezone.utc) - timedelta(days=10)).isoformat()
        policy = MemoryRetentionPolicy(
            policy_id="p1", conversation_id="c1",
            retention_days=365, created_at=created,
        )
        self.assertTrue(policy.should_retain())

    def test_retention_policy_expired(self):
        created = (datetime.now(timezone.utc) - timedelta(days=400)).isoformat()
        policy = MemoryRetentionPolicy(
            policy_id="p1", conversation_id="c1",
            retention_days=365, created_at=created,
        )
        self.assertFalse(policy.should_retain())
        self.assertTrue(policy.is_expired())

    def test_retention_periods_defined(self):
        self.assertIn("active", RETENTION_POLICIES)
        self.assertIn("completed", RETENTION_POLICIES)
        self.assertIn("anonymized", RETENTION_POLICIES)
        self.assertGreater(RETENTION_POLICIES["active"].days, 0)


class TestAnonymization(unittest.TestCase):
    def test_anonymize_field(self):
        result = anonymize_field("+237600000001", "phone")
        self.assertEqual(result, "[REDACTED]")

    def test_anonymize_actor_data(self):
        data = {
            "phone": "+237600000001",
            "email": "test@lawim.cm",
            "name": "Jean Dupont",
            "city": "Douala",
        }
        result = anonymize_actor_data(data)
        self.assertEqual(result["phone"], "[REDACTED]")
        self.assertEqual(result["email"], "[REDACTED]")
        self.assertEqual(result["name"], "[REDACTED]")
        self.assertEqual(result["city"], "Douala")

    def test_anonymize_nested_data(self):
        data = {
            "contact": {
                "phone": "+237600000002",
                "name": "Marie Claire",
            },
            "preferences": {"city": "Yaoundé"},
        }
        result = anonymize_actor_data(data)
        self.assertEqual(result["contact"]["phone"], "[REDACTED]")
        self.assertEqual(result["contact"]["name"], "[REDACTED]")
        self.assertEqual(result["preferences"]["city"], "Yaoundé")


class TestDeletionAuditLog(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        self.deletion_svc = MemoryDeletionService(self.conn)
        self.retention_svc = MemoryRetentionService(self.conn)

    def tearDown(self):
        self.conn.close()

    def test_deletion_audit_log(self):
        log = self.deletion_svc.log_deletion(
            conversation_id="conv_1",
            actor_id="system",
            details={"reason": "retention_expired"},
        )
        self.assertEqual(log.action, "DELETE")
        self.assertEqual(log.conversation_id, "conv_1")
        self.assertEqual(log.details.get("reason"), "retention_expired")

    def test_retention_service_create_policy(self):
        policy = self.retention_svc.create_policy(
            conversation_id="conv_1", retention_days=180,
        )
        self.assertEqual(policy.conversation_id, "conv_1")
        self.assertEqual(policy.retention_days, 180)
        self.assertEqual(policy.status, "active")

    def test_retention_service_get_policy(self):
        self.retention_svc.create_policy("conv_1", 90)
        policy = self.retention_svc.get_policy("conv_1")
        self.assertIsNotNone(policy)
        self.assertEqual(policy.retention_days, 90)

    def test_retention_service_get_policy_not_found(self):
        policy = self.retention_svc.get_policy("nonexistent")
        self.assertIsNone(policy)


if __name__ == "__main__":
    unittest.main()
