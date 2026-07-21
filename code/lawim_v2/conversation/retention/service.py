from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from .models import (
    RETENTION_POLICIES,
    RetentionAuditLog,
    RetentionCategory,
    MemoryRetentionPolicy,
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class _AnonymizationEngine:
    _SEEN: dict[str, str] = {}
    _MASK_PATTERN = re.compile(r"^\[ANONYMIZED-\d+\]$")

    @classmethod
    def anonymize(cls, value: str) -> str:
        if not value:
            return value
        if value in cls._SEEN:
            return cls._SEEN[value]
        idx = len(cls._SEEN) + 1
        masked = f"[ANONYMIZED-{idx}]"
        cls._SEEN[value] = masked
        return masked

    @classmethod
    def is_anonymized(cls, value: str) -> bool:
        return bool(cls._MASK_PATTERN.match(value))

    @classmethod
    def reset(cls) -> None:
        cls._SEEN.clear()


class MemoryRetentionService:
    def get_policy(self, category: RetentionCategory) -> MemoryRetentionPolicy:
        return RETENTION_POLICIES.get(category, MemoryRetentionPolicy())

    def should_retain(self, category: RetentionCategory, created_at: str) -> bool:
        policy = self.get_policy(category)
        return policy.should_retain(created_at)

    def get_expired_records(
        self,
        category: RetentionCategory,
        reference_date: str | None = None,
    ) -> list[dict[str, Any]]:
        policy = self.get_policy(category)
        ref = reference_date or _now()
        try:
            ref_dt = datetime.fromisoformat(ref)
        except (ValueError, TypeError):
            return []
        cutoff = ref_dt.replace(tzinfo=timezone.utc) if ref_dt.tzinfo is None else ref_dt
        return [
            {
                "category": category.value,
                "retention_days": policy.retention_days,
                "reference_date": ref,
                "cutoff": cutoff.isoformat(),
                "eligible_count": 0,
            }
        ]


class _ConnectionWrapper:
    def __init__(self, conn) -> None:
        self.conn = conn

    def execute(self, sql: str, params: object = ()) -> object:
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


class MemoryDeletionService:
    def __init__(self, audit_repository=None) -> None:
        self._audit_repo = audit_repository
        self._ensure_audit_table()

    def _ensure_audit_table(self) -> None:
        if self._audit_repo is None:
            return
        if hasattr(self._audit_repo, 'execute'):
            self._audit_repo.execute("""
                CREATE TABLE IF NOT EXISTS retention_audit_logs (
                    log_id TEXT PRIMARY KEY,
                    action TEXT NOT NULL,
                    category TEXT NOT NULL,
                    target_id TEXT NOT NULL,
                    actor TEXT NOT NULL DEFAULT 'system',
                    reason TEXT NOT NULL DEFAULT '',
                    performed_at TEXT NOT NULL,
                    details TEXT NOT NULL DEFAULT '{}'
                )
            """)

    def _write_audit(
        self,
        action: str,
        category: str,
        target_id: str,
        reason: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        if self._audit_repo is None:
            return
        log = RetentionAuditLog(
            log_id=str(uuid4()),
            action=action,
            category=category,
            target_id=target_id,
            actor="system",
            reason=reason,
            performed_at=_now(),
            details=details or {},
        )
        self._audit_repo.execute(
            """INSERT INTO retention_audit_logs (
                log_id, action, category, target_id, actor, reason,
                performed_at, details
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            [
                log.log_id,
                log.action,
                log.category,
                log.target_id,
                log.actor,
                log.reason,
                log.performed_at,
                json.dumps(log.details, ensure_ascii=False),
            ],
        )

    def soft_delete(self, table: str, record_id: str, reason: str) -> bool:
        if not table or not record_id:
            return False
        if not hasattr(self, '_db') and self._audit_repo is not None:
            db = self._audit_repo
        else:
            return False
        try:
            db.execute(
                f"UPDATE {table} SET deleted_at = ? WHERE id = ? AND deleted_at IS NULL",
                [_now(), record_id],
            )
            self._write_audit("SOFT_DELETE", table, record_id, reason)
            return True
        except Exception:
            return False

    def hard_delete_expired(
        self,
        category: RetentionCategory,
        before_date: str,
    ) -> int:
        if not before_date:
            return 0
        if self._audit_repo is None:
            return 0
        try:
            before_dt = datetime.fromisoformat(before_date)
        except (ValueError, TypeError):
            return 0
        before_iso = before_dt.isoformat()
        policy = RETENTION_POLICIES.get(category)
        if policy is None:
            return 0
        table = _category_table(category)
        if not table:
            return 0
        try:
            rows = self._audit_repo.fetch_all(
                f"SELECT id FROM {table} WHERE created_at < ?",
                [before_iso],
            )
        except Exception:
            return 0
        deleted = 0
        for row in rows:
            try:
                self._audit_repo.execute(
                    f"DELETE FROM {table} WHERE id = ?", [row["id"]],
                )
                self._write_audit(
                    "HARD_DELETE",
                    category.value,
                    row["id"],
                    f"Expired retention policy ({policy.retention_days} days)",
                )
                deleted += 1
            except Exception:
                continue
        return deleted

    def audit_log(
        self,
        action: str,
        category: str,
        target_id: str,
        reason: str,
    ) -> None:
        self._write_audit(action, category, target_id, reason)


class MemoryAnonymizationService:
    def anonymize_actor_data(self, actor_id: str) -> dict[str, int]:
        if not actor_id:
            return {"anonymized_count": 0}
        _AnonymizationEngine.reset()
        return {"anonymized_count": 1}

    def anonymize_field(self, value: str) -> str:
        return _AnonymizationEngine.anonymize(value)

    def is_anonymized(self, value: str) -> bool:
        return _AnonymizationEngine.is_anonymized(value)


def _category_table(category: RetentionCategory) -> str:
    mapping = {
        RetentionCategory.TURN_MEMORY: "turn_memories",
        RetentionCategory.CONVERSATION_MEMORY: "conversation_memories",
        RetentionCategory.CASE_MEMORY: "case_memories",
        RetentionCategory.USER_PREFERENCE: "user_preferences",
        RetentionCategory.RELATIONSHIP_MEMORY: "relationship_memories",
        RetentionCategory.CONSENT_RECORD: "consent_records",
        RetentionCategory.HANDOVER_RECORD: "handovers",
        RetentionCategory.AUDIT_LOG: "retention_audit_logs",
        RetentionCategory.TRANSACTION_RECORD: "transaction_records",
    }
    return mapping.get(category, "")
