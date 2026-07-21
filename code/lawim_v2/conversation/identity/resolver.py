from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from .models import (
    CrossChannelConsent,
    IdentityBinding,
    IdentityConfidence,
    IdentitySource,
    ResolvedIdentity,
)
from .events import (
    IDENTITY_CONFLICT,
    IDENTITY_CONSENT_REQUIRED,
    IDENTITY_RESOLVED,
    IDENTITY_RESUMED,
)


class _ConnectionWrapper:
    def __init__(self, conn) -> None:
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


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_id() -> str:
    return uuid.uuid4().hex[:16]


class IdentityBindingRepository:
    def __init__(self, db) -> None:
        if not hasattr(db, "fetch_one"):
            db = _ConnectionWrapper(db)
        self.db = db
        self._ensure_table()

    def _ensure_table(self) -> None:
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS identity_bindings (
                binding_id TEXT PRIMARY KEY,
                actor_id TEXT NOT NULL,
                channel TEXT NOT NULL,
                channel_identifier TEXT NOT NULL,
                source TEXT NOT NULL DEFAULT 'UNVERIFIED',
                confidence TEXT NOT NULL DEFAULT 'UNVERIFIED',
                created_at TEXT NOT NULL,
                verified_at TEXT,
                UNIQUE(channel, channel_identifier)
            )
        """)

    def save_binding(self, binding: IdentityBinding) -> IdentityBinding:
        self.db.execute(
            """INSERT INTO identity_bindings (
                binding_id, actor_id, channel, channel_identifier,
                source, confidence, created_at, verified_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(channel, channel_identifier) DO UPDATE SET
                actor_id=excluded.actor_id,
                source=excluded.source,
                confidence=excluded.confidence,
                verified_at=excluded.verified_at""",
            [
                binding.binding_id,
                binding.actor_id,
                binding.channel,
                binding.channel_identifier,
                binding.source.value,
                binding.confidence.value,
                binding.created_at,
                binding.verified_at,
            ],
        )
        return binding

    def load_binding(
        self, channel: str, channel_identifier: str
    ) -> IdentityBinding | None:
        row = self.db.fetch_one(
            "SELECT * FROM identity_bindings WHERE channel = ? AND channel_identifier = ?",
            [channel, channel_identifier],
        )
        if not row:
            return None
        return self._row_to_binding(row)

    def load_bindings_by_actor(self, actor_id: str) -> list[IdentityBinding]:
        rows = self.db.fetch_all(
            "SELECT * FROM identity_bindings WHERE actor_id = ? ORDER BY created_at ASC",
            [actor_id],
        )
        return [self._row_to_binding(r) for r in rows]

    def load_bindings_by_channel(self, channel: str) -> list[IdentityBinding]:
        rows = self.db.fetch_all(
            "SELECT * FROM identity_bindings WHERE channel = ? ORDER BY created_at ASC",
            [channel],
        )
        return [self._row_to_binding(r) for r in rows]

    def delete_binding(self, binding_id: str) -> None:
        self.db.execute(
            "DELETE FROM identity_bindings WHERE binding_id = ?",
            [binding_id],
        )

    def _row_to_binding(self, row: dict[str, Any]) -> IdentityBinding:
        return IdentityBinding(
            binding_id=row["binding_id"],
            actor_id=row["actor_id"],
            channel=row["channel"],
            channel_identifier=row["channel_identifier"],
            source=IdentitySource(row["source"]),
            confidence=IdentityConfidence(row["confidence"]),
            created_at=row["created_at"],
            verified_at=row.get("verified_at"),
        )


class CrossChannelConsentRepository:
    def __init__(self, db) -> None:
        if not hasattr(db, "fetch_one"):
            db = _ConnectionWrapper(db)
        self.db = db
        self._ensure_table()

    def _ensure_table(self) -> None:
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS cross_channel_consents (
                consent_id TEXT PRIMARY KEY,
                consent_type TEXT NOT NULL DEFAULT 'cross_channel_continuity',
                actor_id TEXT NOT NULL,
                source_channel TEXT NOT NULL,
                target_channel TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'PENDING',
                granted_at TEXT,
                expires_at TEXT,
                revoked_at TEXT,
                evidence TEXT DEFAULT '',
                created_at TEXT NOT NULL
            )
        """)

    def save_consent(self, consent: CrossChannelConsent) -> CrossChannelConsent:
        self.db.execute(
            """INSERT INTO cross_channel_consents (
                consent_id, consent_type, actor_id, source_channel, target_channel,
                status, granted_at, expires_at, revoked_at, evidence, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(consent_id) DO UPDATE SET
                status=excluded.status,
                granted_at=excluded.granted_at,
                expires_at=excluded.expires_at,
                revoked_at=excluded.revoked_at,
                evidence=excluded.evidence""",
            [
                consent.consent_id,
                consent.consent_type,
                consent.actor_id,
                consent.source_channel,
                consent.target_channel,
                consent.status,
                consent.granted_at,
                consent.expires_at,
                consent.revoked_at,
                consent.evidence,
                consent.created_at,
            ],
        )
        return consent

    def load_consent(self, consent_id: str) -> CrossChannelConsent | None:
        row = self.db.fetch_one(
            "SELECT * FROM cross_channel_consents WHERE consent_id = ?",
            [consent_id],
        )
        if not row:
            return None
        return self._row_to_consent(row)

    def load_active_consent(
        self,
        actor_id: str,
        source_channel: str,
        target_channel: str,
    ) -> CrossChannelConsent | None:
        row = self.db.fetch_one(
            """SELECT * FROM cross_channel_consents
             WHERE actor_id = ? AND source_channel = ? AND target_channel = ?
             AND status = 'GRANTED'
             ORDER BY created_at DESC LIMIT 1""",
            [actor_id, source_channel, target_channel],
        )
        if not row:
            return None
        return self._row_to_consent(row)

    def load_consents_by_actor(self, actor_id: str) -> list[CrossChannelConsent]:
        rows = self.db.fetch_all(
            "SELECT * FROM cross_channel_consents WHERE actor_id = ? ORDER BY created_at DESC",
            [actor_id],
        )
        return [self._row_to_consent(r) for r in rows]

    def revoke_consent(self, consent_id: str) -> None:
        now = _utcnow()
        self.db.execute(
            "UPDATE cross_channel_consents SET status = ?, revoked_at = ? WHERE consent_id = ?",
            ["REVOKED", now, consent_id],
        )

    def _row_to_consent(self, row: dict[str, Any]) -> CrossChannelConsent:
        return CrossChannelConsent(
            consent_id=row["consent_id"],
            consent_type=row["consent_type"],
            actor_id=row["actor_id"],
            source_channel=row["source_channel"],
            target_channel=row["target_channel"],
            status=row["status"],
            granted_at=row.get("granted_at"),
            expires_at=row.get("expires_at"),
            revoked_at=row.get("revoked_at"),
            evidence=row.get("evidence", ""),
            created_at=row["created_at"],
        )


class CrossChannelIdentityResolver:
    def __init__(
        self,
        repository: IdentityBindingRepository,
        consent_repository: CrossChannelConsentRepository,
    ) -> None:
        self.repository = repository
        self.consent_repository = consent_repository

    def resolve(
        self, channel: str, channel_identifier: str
    ) -> ResolvedIdentity:
        now = _utcnow()
        binding = self.repository.load_binding(channel, channel_identifier)

        if binding is None:
            return ResolvedIdentity(
                actor_id="",
                confidence=IdentityConfidence.UNVERIFIED,
                sources=[],
                channels=[channel],
                resolved_at=now,
            )

        resolved = ResolvedIdentity(
            actor_id=binding.actor_id,
            confidence=binding.confidence,
            sources=[binding.source.value],
            channels=[binding.channel],
            resolved_at=now,
        )

        if binding.confidence == IdentityConfidence.VERIFIED:
            bindings = self.repository.load_bindings_by_actor(binding.actor_id)
            seen_sources: dict[str, str] = {}
            for b in bindings:
                resolved.channels.append(b.channel)
                if b.source.value not in seen_sources:
                    resolved.sources.append(b.source.value)
                    seen_sources[b.source.value] = b.binding_id
                if b.binding_id != binding.binding_id and b.source == IdentitySource.PHONE_VERIFIED:
                    resolved.confidence = IdentityConfidence.CONFLICT
                    break

            return resolved

        return resolved

    def resolve_with_consent(
        self, channel: str, channel_identifier: str, target_channel: str
    ) -> tuple[ResolvedIdentity, bool]:
        resolved = self.resolve(channel, channel_identifier)

        if resolved.confidence == IdentityConfidence.UNVERIFIED:
            return resolved, False

        if not resolved.can_auto_merge():
            return resolved, False

        consent = self.consent_repository.load_active_consent(
            resolved.actor_id, channel, target_channel,
        )

        has_consent = consent is not None and consent.is_active()
        return resolved, has_consent

    def bind_identity(
        self,
        actor_id: str,
        channel: str,
        channel_identifier: str,
        source: IdentitySource,
    ) -> IdentityBinding:
        now = _utcnow()
        existing = self.repository.load_binding(channel, channel_identifier)

        if existing:
            existing.actor_id = actor_id
            existing.source = source
            if source in (
                IdentitySource.PHONE_VERIFIED,
                IdentitySource.EMAIL_VERIFIED,
                IdentitySource.AUTHENTICATED_ACCOUNT,
            ):
                existing.confidence = IdentityConfidence.VERIFIED
                existing.verified_at = now
            elif source == IdentitySource.USER_ID:
                existing.confidence = IdentityConfidence.HIGH_CONFIDENCE
            else:
                existing.confidence = IdentityConfidence.UNVERIFIED
            return self.repository.save_binding(existing)

        confidence = IdentityConfidence.UNVERIFIED
        verified_at = None
        if source in (
            IdentitySource.PHONE_VERIFIED,
            IdentitySource.EMAIL_VERIFIED,
            IdentitySource.AUTHENTICATED_ACCOUNT,
        ):
            confidence = IdentityConfidence.VERIFIED
            verified_at = now
        elif source == IdentitySource.USER_ID:
            confidence = IdentityConfidence.HIGH_CONFIDENCE

        binding = IdentityBinding(
            binding_id=_new_id(),
            actor_id=actor_id,
            channel=channel,
            channel_identifier=channel_identifier,
            source=source,
            confidence=confidence,
            created_at=now,
            verified_at=verified_at,
        )
        return self.repository.save_binding(binding)

    def request_consent(
        self, actor_id: str, source_channel: str, target_channel: str
    ) -> CrossChannelConsent:
        now = _utcnow()
        consent = CrossChannelConsent(
            consent_id=_new_id(),
            consent_type="cross_channel_continuity",
            actor_id=actor_id,
            source_channel=source_channel,
            target_channel=target_channel,
            status="PENDING",
            created_at=now,
        )
        return self.consent_repository.save_consent(consent)

    def grant_consent(self, consent_id: str) -> CrossChannelConsent:
        consent = self.consent_repository.load_consent(consent_id)
        if consent is None:
            raise ValueError(f"Consent not found: {consent_id}")

        now = _utcnow()
        consent.status = "GRANTED"
        consent.granted_at = now
        return self.consent_repository.save_consent(consent)

    def revoke_consent(self, consent_id: str) -> None:
        consent = self.consent_repository.load_consent(consent_id)
        if consent is None:
            raise ValueError(f"Consent not found: {consent_id}")
        self.consent_repository.revoke_consent(consent_id)

    def get_known_channels(self, actor_id: str) -> list[dict[str, str]]:
        bindings = self.repository.load_bindings_by_actor(actor_id)
        seen: set[str] = set()
        result: list[dict[str, str]] = []
        for b in bindings:
            key = f"{b.channel}:{b.channel_identifier}"
            if key not in seen:
                seen.add(key)
                result.append({
                    "channel": b.channel,
                    "channel_identifier": b.channel_identifier,
                    "confidence": b.confidence.value,
                    "source": b.source.value,
                })
        return result
