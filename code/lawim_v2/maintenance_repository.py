from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any


def utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class MaintenanceRepositoryMixin:
    def create_maintenance_message(
        self,
        *,
        user_id: int | None,
        channel_identity_id: int | None,
        channel: str,
        raw_message: str,
        delivery_metadata: dict[str, object],
        handover_requested: bool = False,
    ) -> dict[str, object]:
        now = utcnow()
        message_key = f"maintenance-{channel}-{now}-{abs(hash((channel, raw_message, now))) % 1_000_000_000}"
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO maintenance_messages (
                    message_key, user_id, channel_identity_id, channel, raw_message,
                    received_at, delivery_metadata_json, maintenance_status, handover_requested
                ) VALUES (?, ?, ?, ?, ?, ?, ?, 'received', ?)
                """,
                (
                    message_key,
                    user_id,
                    channel_identity_id,
                    channel,
                    raw_message,
                    now,
                    json.dumps(delivery_metadata, ensure_ascii=False, sort_keys=True),
                    1 if handover_requested else 0,
                ),
            )
            return dict(conn.execute("SELECT * FROM maintenance_messages WHERE id = ?", (cursor.lastrowid,)).fetchone())

    def list_maintenance_messages(
        self,
        *,
        channel: str | None = None,
        handover_requested: bool | None = None,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        conditions: list[str] = []
        params: list[object] = []
        if channel:
            conditions.append("channel = ?")
            params.append(channel)
        if handover_requested is not None:
            conditions.append("handover_requested = ?")
            params.append(1 if handover_requested else 0)
        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        params.append(limit)
        rows = self.all(
            f"SELECT * FROM maintenance_messages {where} ORDER BY id DESC LIMIT ?",
            tuple(params),
        )
        return [dict(row) for row in rows]
