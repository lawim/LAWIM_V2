from __future__ import annotations

import json
import logging
import os
import uuid
from datetime import datetime, timezone
from typing import Any

from ..repository_introspection import table_exists
from .constants import (
    CAMPAIGN_STATUSES,
    CHANNEL_TYPES,
    DEFAULT_CHANNELS,
    DEFAULT_NOTIFICATION_RULES,
    DEFAULT_TELEGRAM_BOT,
    DEFAULT_TEMPLATES,
    DEFAULT_WHATSAPP_ACCOUNT,
    EVENT_KINDS,
    MESSAGE_PRIORITIES,
    MESSAGE_STATUSES,
    NOTIFICATION_TYPES,
)
from .delivery import (
    dry_run_delivery,
    failed_delivery,
    green_api_chat_id,
    mask_delivery_recipient,
    sanitize_delivery_record,
    send_green_api_message,
    send_telegram_message,
    should_use_real_delivery,
)
from .engines import CommunicationPlatformEngine

LOGGER = logging.getLogger(__name__)


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _parse_json(value: str | None) -> Any:
    if not value:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return None


def _normalize_message_key(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


def _normalize_event_key(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


class CommunicationRepositoryMixin:
    def communication_tables_present(self) -> bool:
        return table_exists(self, "communication_channels")

    def seed_communication_catalog(self) -> None:
        if self.scalar("SELECT COUNT(*) FROM communication_channels") > 0:
            return
        engine = CommunicationPlatformEngine()
        now = _utcnow()
        with self._transaction() as conn:
            for channel_key, channel_type, name, provider in DEFAULT_CHANNELS:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO communication_channels (
                        channel_key, channel_type, name, provider, status, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, 'active', ?, ?)
                    """,
                    (channel_key, channel_type, name, provider, now, now),
                )
            for rule_key, name, event_kind, channel_type in DEFAULT_NOTIFICATION_RULES:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO notification_rules (
                        rule_key, name, event_kind, channel_type, status, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, 'active', ?, ?)
                    """,
                    (rule_key, name, event_kind, channel_type, now, now),
                )
            for tpl_key, channel_type, name, subject, body in DEFAULT_TEMPLATES:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO notification_templates (
                        template_key, name, channel_type, subject, body, status, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, 'active', ?, ?)
                    """,
                    (tpl_key, name, channel_type, subject, body, now, now),
                )
            wa_key, wa_handle, wa_phone = DEFAULT_WHATSAPP_ACCOUNT
            conn.execute(
                """
                INSERT OR IGNORE INTO whatsapp_accounts (
                    account_key, handle, phone_e164, provider, status, created_at, updated_at
                ) VALUES (?, ?, ?, 'meta_cloud', 'active', ?, ?)
                """,
                (wa_key, wa_handle, wa_phone, now, now),
            )
            tg_key, tg_handle = DEFAULT_TELEGRAM_BOT
            conn.execute(
                """
                INSERT OR IGNORE INTO telegram_bots (
                    bot_key, bot_handle, status, created_at, updated_at
                ) VALUES (?, ?, 'active', ?, ?)
                """,
                (tg_key, tg_handle, now, now),
            )
            conn.execute(
                """
                INSERT OR IGNORE INTO sms_providers (
                    provider_key, name, provider_type, status, created_at, updated_at
                ) VALUES ('sms-orange', 'Orange Cameroon', 'orange', 'active', ?, ?)
                """,
                (now, now),
            )
        self.record_event(
            "communication_catalog_seeded",
            {"channels": len(DEFAULT_CHANNELS), "templates": len(DEFAULT_TEMPLATES)},
        )
        self.snapshot_communication_dashboard()

    def integration_sources(self) -> dict[str, object]:
        engine = CommunicationPlatformEngine()
        payload: dict[str, object] = {"sources": engine.integration_sources()}
        checks = {
            "intelligent_core": hasattr(self, "get_intelligent_decision"),
            "ecosystem": hasattr(self, "get_service_catalog_item"),
            "cognition": hasattr(self, "cognition_query"),
            "maintenance": hasattr(self, "create_maintenance_message"),
            "knowledge_platform": hasattr(self, "expert_rag_query"),
            "workflow_automation": hasattr(self, "start_automation_instance"),
            "real_estate_intelligence": hasattr(self, "get_rei_property_bundle"),
            "crm": hasattr(self, "get_crm_contact"),
            "marketplace": hasattr(self, "get_marketplace_provider"),
            "security": hasattr(self, "record_audit_trail"),
        }
        payload["programs"] = {key: bool(value) for key, value in checks.items()}
        return payload

    # --- Messages ---

    def create_communication_message(
        self,
        *,
        channel_type: str = "email",
        body: str,
        subject: str = "",
        direction: str = "outbound",
        priority: str = "normal",
        status: str = "draft",
        message_key: str | None = None,
        sender_user_id: int | None = None,
        recipient_user_id: int | None = None,
        contact_id: int | None = None,
        organization_id: int | None = None,
        thread_id: int | None = None,
        scheduled_at: str | None = None,
        payload: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, object]:
        engine = CommunicationPlatformEngine()
        channel_type = engine.communication.validate_channel(channel_type)
        if priority not in MESSAGE_PRIORITIES:
            priority = "normal"
        if status not in MESSAGE_STATUSES:
            status = "draft"
        now = _utcnow()
        key = _normalize_message_key(message_key) or f"msg-{uuid.uuid4().hex[:12]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO communication_messages (
                    message_key, thread_id, channel_type, direction, priority, status,
                    sender_user_id, recipient_user_id, contact_id, organization_id,
                    subject, body, payload_json, scheduled_at, metadata_json, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    key,
                    thread_id,
                    channel_type,
                    direction,
                    priority,
                    status,
                    sender_user_id,
                    recipient_user_id,
                    contact_id,
                    organization_id,
                    subject,
                    body,
                    _json(payload or {}),
                    scheduled_at,
                    _json(metadata or {}),
                    now,
                    now,
                ),
            )
        return dict(self.one("SELECT * FROM communication_messages WHERE message_key = ?", (key,)))

    def create_communication_event(
        self,
        *,
        event_kind: str,
        source_program: str = "platform",
        payload: dict[str, Any] | None = None,
        event_key: str | None = None,
        message_id: int | None = None,
        metadata: dict[str, Any] | None = None,
        status: str = "active",
    ) -> dict[str, object]:
        now = _utcnow()
        key = _normalize_event_key(event_key) or f"evt-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO communication_events (
                    event_key, status, metadata_json, created_at, event_kind, source_program, payload_json, message_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    key,
                    status,
                    _json(metadata or {}),
                    now,
                    event_kind,
                    source_program,
                    _json(payload or {}),
                    message_id,
                ),
            )
        return dict(self.one("SELECT * FROM communication_events WHERE event_key = ?", (key,)))

    def create_communication_log(
        self,
        *,
        level: str = "info",
        message: str,
        payload: dict[str, Any] | None = None,
        message_id: int | None = None,
    ) -> dict[str, object]:
        now = _utcnow()
        key = f"log-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO communication_logs (
                    log_key, status, metadata_json, created_at, message_id, level, message, payload_json
                ) VALUES (?, 'active', ?, ?, ?, ?, ?, ?)
                """,
                (
                    key,
                    _json({"level": level}),
                    now,
                    message_id,
                    level,
                    message,
                    _json(payload or {}),
                ),
        )
        return dict(self.one("SELECT * FROM communication_logs WHERE log_key = ?", (key,)))

    def create_telegram_update(
        self,
        *,
        update_key: str,
        update_type: str,
        payload: dict[str, Any] | None = None,
        bot_id: int | None = None,
        metadata: dict[str, Any] | None = None,
        received_at: str | None = None,
    ) -> dict[str, object]:
        now = received_at or _utcnow()
        key = _normalize_event_key(update_key) or f"tgupd-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO telegram_updates (
                    update_key, status, metadata_json, created_at, bot_id, update_type, payload_json, received_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    key,
                    "active",
                    _json(metadata or {}),
                    now,
                    bot_id,
                    update_type,
                    _json(payload or {}),
                    now,
                ),
            )
        return dict(self.one("SELECT * FROM telegram_updates WHERE update_key = ?", (key,)))

    def get_communication_message(self, message_id: int) -> dict[str, object]:
        row = self.one("SELECT * FROM communication_messages WHERE id = ?", (message_id,))
        if row is None:
            from ..errors import NotFoundError

            raise NotFoundError("message not found")
        return dict(row)

    def list_communication_messages(
        self,
        *,
        channel_type: str | None = None,
        status: str | None = None,
        limit: int = 50,
    ) -> list[dict[str, object]]:
        query = "SELECT * FROM communication_messages WHERE 1=1"
        params: list[object] = []
        if channel_type:
            query += " AND channel_type = ?"
            params.append(channel_type)
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY id DESC LIMIT ?"
        params.append(limit)
        return [dict(r) for r in self.all(query, tuple(params))]

    def update_communication_message(self, message_id: int, **fields: object) -> dict[str, object]:
        allowed = {
            "status",
            "priority",
            "body",
            "subject",
            "scheduled_at",
            "sent_at",
            "metadata_json",
            "payload_json",
            "thread_id",
            "contact_id",
            "organization_id",
            "sender_user_id",
            "recipient_user_id",
        }
        updates = {k: v for k, v in fields.items() if k in allowed and v is not None}
        if "metadata" in fields and fields["metadata"] is not None:
            updates["metadata_json"] = _json(fields["metadata"])
        if "payload" in fields and fields["payload"] is not None:
            updates["payload_json"] = _json(fields["payload"])
        if not updates:
            return self.get_communication_message(message_id)
        updates["updated_at"] = _utcnow()
        cols = ", ".join(f"{k} = ?" for k in updates)
        with self._transaction() as conn:
            conn.execute(f"UPDATE communication_messages SET {cols} WHERE id = ?", (*updates.values(), message_id))
        return self.get_communication_message(message_id)

    # --- Channels ---

    def list_communication_channels(self, *, status: str | None = None, limit: int = 50) -> list[dict[str, object]]:
        if status:
            rows = self.all(
                "SELECT * FROM communication_channels WHERE status = ? ORDER BY id ASC LIMIT ?",
                (status, limit),
            )
        else:
            rows = self.all("SELECT * FROM communication_channels ORDER BY id ASC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    def get_communication_channel(self, channel_id: int) -> dict[str, object]:
        row = self.one("SELECT * FROM communication_channels WHERE id = ?", (channel_id,))
        if row is None:
            from ..errors import NotFoundError

            raise NotFoundError("channel not found")
        return dict(row)

    # --- Threads / Conversations ---

    def create_communication_thread(
        self,
        *,
        subject: str = "",
        channel_id: int | None = None,
        organization_id: int | None = None,
        thread_key: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, object]:
        now = _utcnow()
        key = _normalize_message_key(thread_key) or f"thread-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO communication_threads (
                    thread_key, channel_id, subject, status, organization_id, metadata_json, created_at, updated_at
                ) VALUES (?, ?, ?, 'open', ?, ?, ?, ?)
                """,
                (key, channel_id, subject, organization_id, _json(metadata or {}), now, now),
            )
        return dict(self.one("SELECT * FROM communication_threads WHERE thread_key = ?", (key,)))

    def list_communication_threads(self, *, limit: int = 50) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM communication_threads ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    # --- Notifications ---

    def create_notification_event(
        self,
        *,
        notification_type: str = "system",
        title: str,
        body: str = "",
        user_id: int | None = None,
        contact_id: int | None = None,
        priority: str = "normal",
        payload: dict[str, Any] | None = None,
    ) -> dict[str, object]:
        engine = CommunicationPlatformEngine()
        notification_type = engine.notification.validate_type(notification_type)
        if priority not in MESSAGE_PRIORITIES:
            priority = "normal"
        now = _utcnow()
        key = f"notif-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO notification_events (
                    event_key, notification_type, user_id, contact_id, title, body,
                    payload_json, priority, status, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending', ?)
                """,
                (key, notification_type, user_id, contact_id, title, body, _json(payload or {}), priority, now),
            )
        return dict(self.one("SELECT * FROM notification_events WHERE event_key = ?", (key,)))

    def list_notification_events(
        self,
        *,
        user_id: int | None = None,
        status: str | None = None,
        limit: int = 50,
    ) -> list[dict[str, object]]:
        query = "SELECT * FROM notification_events WHERE 1=1"
        params: list[object] = []
        if user_id is not None:
            query += " AND user_id = ?"
            params.append(user_id)
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY id DESC LIMIT ?"
        params.append(limit)
        return [dict(r) for r in self.all(query, tuple(params))]

    def get_notification_template(self, template_id: int) -> dict[str, object]:
        row = self.one("SELECT * FROM notification_templates WHERE id = ?", (template_id,))
        if row is None:
            from ..errors import NotFoundError

            raise NotFoundError("template not found")
        return dict(row)

    def create_notification_template(
        self,
        *,
        name: str,
        channel_type: str = "in_app",
        subject: str = "",
        body: str = "",
    ) -> dict[str, object]:
        now = _utcnow()
        key = f"tpl-{uuid.uuid4().hex[:10]}"
        if channel_type not in CHANNEL_TYPES:
            channel_type = "in_app"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO notification_templates (
                    template_key, name, channel_type, subject, body, status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, 'active', ?, ?)
                """,
                (key, name, channel_type, subject, body, now, now),
            )
        return dict(self.one("SELECT * FROM notification_templates WHERE template_key = ?", (key,)))

    def list_notification_templates(
        self,
        *,
        channel_type: str | None = None,
        limit: int = 50,
    ) -> list[dict[str, object]]:
        if channel_type:
            rows = self.all(
                "SELECT * FROM notification_templates WHERE channel_type = ? ORDER BY id ASC LIMIT ?",
                (channel_type, limit),
            )
        else:
            rows = self.all("SELECT * FROM notification_templates ORDER BY id ASC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    def deliver_notification(self, notification_id: int) -> dict[str, object]:
        engine = CommunicationPlatformEngine()
        row = self.one("SELECT * FROM notification_events WHERE id = ?", (notification_id,))
        if row is None:
            from ..errors import NotFoundError

            raise NotFoundError("notification not found")
        now = _utcnow()
        key = f"del-{uuid.uuid4().hex[:10]}"
        channel_type = "in_app"
        with self._transaction() as conn:
            conn.execute(
                "UPDATE notification_events SET status = 'delivered' WHERE id = ?",
                (notification_id,),
            )
            conn.execute(
                """
                INSERT INTO notification_deliveries (
                    delivery_key, notification_event_id, channel_type, delivery_status,
                    delivered_at, status, created_at
                ) VALUES (?, ?, ?, 'delivered', ?, 'active', ?)
                """,
                (key, notification_id, channel_type, now, now),
            )
        delivery = dict(self.one("SELECT * FROM notification_deliveries WHERE delivery_key = ?", (key,)))
        delivery["stub"] = engine.notification.should_deliver(
            notification_type=str(row["notification_type"]),
            channel_type=channel_type,
            preferences=None,
        )
        return delivery

    def acknowledge_notification(self, *, notification_id: int, user_id: int) -> dict[str, object]:
        now = _utcnow()
        key = f"ack-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO notification_acknowledgements (
                    ack_key, notification_event_id, user_id, acknowledged_at, status, created_at
                ) VALUES (?, ?, ?, ?, 'active', ?)
                """,
                (key, notification_id, user_id, now, now),
            )
            conn.execute(
                "UPDATE notification_events SET status = 'acknowledged' WHERE id = ?",
                (notification_id,),
            )
        return dict(self.one("SELECT * FROM notification_acknowledgements WHERE ack_key = ?", (key,)))

    def record_delivery(
        self,
        *,
        channel_type: str,
        resource_type: str,
        resource_id: int,
        delivery_status: str = "delivered",
        provider_response: str = "",
    ) -> dict[str, object]:
        now = _utcnow()
        table_map = {
            "email": ("email_delivery_logs", "log_key", "email_message_id", "delivery_status", "provider_response", "logged_at"),
            "sms": ("sms_delivery_logs", "log_key", "sms_message_id", "delivery_status", "provider_response", "logged_at"),
            "whatsapp": ("whatsapp_delivery_logs", "log_key", "whatsapp_message_id", "delivery_status", "provider_response", "logged_at"),
            "push": ("push_delivery_logs", "log_key", "push_notification_id", "delivery_status", "provider_response", "logged_at"),
        }
        mapping = table_map.get(channel_type)
        if mapping is None:
            return {"recorded": False, "channel_type": channel_type}
        table, key_col, fk_col, status_col, response_col, time_col = mapping
        key = f"log-{uuid.uuid4().hex[:8]}"
        with self._transaction() as conn:
            conn.execute(
                f"""
                INSERT INTO {table} (
                    {key_col}, {fk_col}, {status_col}, {response_col}, {time_col}, status, created_at
                ) VALUES (?, ?, ?, ?, ?, 'active', ?)
                """,
                (key, resource_id, delivery_status, provider_response, now, now),
            )
        return {"recorded": True, "channel_type": channel_type, "resource_type": resource_type, "log_key": key}

    # --- Channel send stubs ---

    def send_email(
        self,
        *,
        to_email: str,
        subject: str,
        body: str,
        account_id: int | None = None,
    ) -> dict[str, object]:
        engine = CommunicationPlatformEngine()
        payload = engine.email.build_payload(to_email=to_email, subject=subject, body=body)
        result = engine.email.stub_send(payload)
        now = _utcnow()
        msg = self.create_communication_message(
            channel_type="email",
            subject=subject,
            body=body,
            status="sent",
        )
        key = f"email-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO email_messages (
                    message_key, account_id, message_id, to_email, from_email, subject, body,
                    email_status, sent_at, status, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, 'sent', ?, 'active', ?)
                """,
                (
                    key,
                    account_id,
                    msg["id"],
                    to_email,
                    str(payload.get("from_email") or ""),
                    subject,
                    body,
                    now,
                    now,
                ),
            )
        row = dict(self.one("SELECT * FROM email_messages WHERE message_key = ?", (key,)))
        row["delivery"] = result
        return row

    def list_email_messages(self, *, limit: int = 50) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM email_messages ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    def send_sms(
        self,
        *,
        to_number: str,
        body: str,
        provider_id: int | None = None,
    ) -> dict[str, object]:
        engine = CommunicationPlatformEngine()
        payload = engine.sms.build_payload(to_number=to_number, body=body)
        result = engine.sms.stub_send(payload)
        now = _utcnow()
        msg = self.create_communication_message(channel_type="sms", body=body, status="sent")
        key = f"sms-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO sms_messages (
                    message_key, provider_id, message_id, to_number, from_number, body,
                    sms_status, sent_at, status, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, 'sent', ?, 'active', ?)
                """,
                (
                    key,
                    provider_id,
                    msg["id"],
                    to_number,
                    str(payload.get("from_number") or ""),
                    body,
                    now,
                    now,
                ),
            )
        row = dict(self.one("SELECT * FROM sms_messages WHERE message_key = ?", (key,)))
        row["delivery"] = result
        return row

    def list_sms_messages(self, *, limit: int = 50) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM sms_messages ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    def send_whatsapp(
        self,
        *,
        to_number: str,
        body: str,
        account_id: int | None = None,
        thread_id: int | None = None,
        contact_id: int | None = None,
        external_chat_id: str | None = None,
        external_user_id: str | None = None,
        provider_message_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, object]:
        engine = CommunicationPlatformEngine()
        payload = engine.whatsapp.build_payload(to_number=to_number, body=body)
        payload.update(
            {
                "external_chat_id": external_chat_id or "",
                "external_user_id": external_user_id or "",
                "provider_message_id": provider_message_id or "",
            }
        )
        now = _utcnow()
        request_row = self.create_communication_message(
            channel_type="whatsapp",
            body=body,
            status="sending",
            thread_id=thread_id,
            contact_id=contact_id,
            payload=payload,
            metadata=metadata or {
                "external_chat_id": external_chat_id or "",
                "external_user_id": external_user_id or "",
                "provider_message_id": provider_message_id or "",
                "delivery_stage": "request_created",
            },
        )
        recipient = str(to_number or "").strip()
        request_summary = {
            "channel": "whatsapp",
            "message_id": int(request_row["id"]),
            "recipient": mask_delivery_recipient(recipient),
            "response_length": len(body.strip()),
            "provider": "green_api",
            "selected_provider": "green_api",
            "stage": "delivery_start",
        }
        self.create_communication_log(
            level="info",
            message="WhatsApp outbound delivery started",
            payload=request_summary,
            message_id=int(request_row["id"]),
        )
        LOGGER.info("%s", json.dumps(request_summary, ensure_ascii=False, sort_keys=True))
        if should_use_real_delivery():
            api_url = (os.getenv("GREEN_API_API_URL") or "").strip()
            id_instance = (os.getenv("GREEN_API_ID_INSTANCE") or "").strip()
            token_instance = (os.getenv("GREEN_API_TOKEN_INSTANCE") or "").strip()
            chat_id = green_api_chat_id(recipient)
            if api_url and id_instance and token_instance and chat_id:
                delivery = send_green_api_message(
                    api_url=api_url,
                    id_instance=id_instance,
                    token_instance=token_instance,
                    chat_id=chat_id,
                    message=body,
                )
            else:
                missing = [
                    name
                    for name, value in (
                        ("GREEN_API_API_URL", api_url),
                        ("GREEN_API_ID_INSTANCE", id_instance),
                        ("GREEN_API_TOKEN_INSTANCE", token_instance),
                        ("GREEN_API_CHAT_ID", chat_id),
                    )
                    if not value
                ]
                delivery = failed_delivery(
                    provider="green_api",
                    method="POST",
                    url=f"{api_url.rstrip('/') if api_url else 'https://api.greenapi.com'}/waInstance{id_instance or 'unknown'}/sendMessage/[redacted]",
                    payload={"chatId": chat_id or recipient, "message": body},
                    recipient=recipient,
                    error_type="unconfigured",
                    error_message=f"Missing Green API delivery configuration: {', '.join(missing)}",
                )
        else:
            delivery = dry_run_delivery(
                provider="green_api",
                method="POST",
                url=f"{os.getenv('GREEN_API_API_URL', 'https://api.greenapi.com').rstrip('/')}/waInstance{os.getenv('GREEN_API_ID_INSTANCE', 'unknown')}/sendMessage/[redacted]",
                payload={"chatId": green_api_chat_id(recipient) or recipient, "message": body},
                recipient=recipient,
            )
        delivery_record = sanitize_delivery_record(delivery, recipient=recipient)
        outbound_status = "sent" if delivery.ok else "failed"
        request_metadata = {
            "external_chat_id": external_chat_id or "",
            "external_user_id": external_user_id or "",
            "provider_message_id": delivery.provider_message_id,
            "provider_response": delivery_record,
            "provider_status": delivery.delivery_status,
            "delivery_status": outbound_status,
            "resolved_ipv4": delivery.resolved_ipv4,
            "sanitized_url": delivery.sanitized_url,
        }
        self.update_communication_message(
            int(request_row["id"]),
            status=outbound_status,
            sent_at=now,
            metadata=request_metadata,
            payload={**payload, "provider_response": delivery_record},
        )
        account_row = self.one("SELECT id FROM whatsapp_accounts ORDER BY id LIMIT 1")
        account_id = int(account_row["id"]) if account_row and account_row.get("id") is not None else None
        key = f"wa-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO whatsapp_messages (
                    message_key, status, metadata_json, created_at, account_id, message_id, to_number, body,
                    whatsapp_status, sent_at
                ) VALUES (?, 'active', ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    key,
                    json.dumps(request_metadata, ensure_ascii=False, sort_keys=True),
                    now,
                    account_id,
                    request_row["id"],
                    to_number,
                    body,
                    outbound_status,
                    now,
                ),
            )
        row = dict(self.one("SELECT * FROM whatsapp_messages WHERE message_key = ?", (key,)))
        self.record_delivery(
            channel_type="whatsapp",
            resource_type="whatsapp_message",
            resource_id=int(row["id"]),
            delivery_status=outbound_status,
            provider_response=json.dumps(delivery_record, ensure_ascii=False, sort_keys=True),
        )
        self.create_communication_log(
            level="info" if delivery.ok else "warning",
            message="WhatsApp outbound delivery completed" if delivery.ok else "WhatsApp outbound delivery failed",
            payload={
                "channel": "whatsapp",
                "message_id": int(request_row["id"]),
                "whatsapp_message_id": int(row["id"]),
                "recipient": mask_delivery_recipient(recipient),
                "response_length": len(body.strip()),
                "provider": delivery.provider,
                "selected_provider": "green_api",
                "delivery_status": outbound_status,
                "http_status": delivery.http_status,
                "provider_message_id": delivery.provider_message_id,
                "resolved_ipv4": delivery.resolved_ipv4,
                "sanitized_url": delivery.sanitized_url,
                "error_type": delivery.error_type,
            },
            message_id=int(request_row["id"]),
        )
        LOGGER.info(
            "%s",
            json.dumps(
                {
                    "channel": "whatsapp",
                    "message_id": int(request_row["id"]),
                    "whatsapp_message_id": int(row["id"]),
                    "recipient": mask_delivery_recipient(recipient),
                    "response_length": len(body.strip()),
                    "provider": delivery.provider,
                    "selected_provider": "green_api",
                    "delivery_status": outbound_status,
                    "http_status": delivery.http_status,
                    "provider_message_id": delivery.provider_message_id,
                    "resolved_ipv4": delivery.resolved_ipv4,
                    "sanitized_url": delivery.sanitized_url,
                    "error_type": delivery.error_type,
                },
                ensure_ascii=False,
                sort_keys=True,
            ),
        )
        row["delivery"] = delivery_record
        row["communication_message_id"] = int(request_row["id"])
        row["delivery_status"] = outbound_status
        row["provider_message_id"] = delivery.provider_message_id
        return row

    def list_whatsapp_messages(self, *, limit: int = 50) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM whatsapp_messages ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    def send_telegram(
        self,
        *,
        chat_id: str | int,
        body: str,
        bot_id: int | None = None,
        thread_id: int | None = None,
        contact_id: int | None = None,
        external_chat_id: str | None = None,
        external_user_id: str | None = None,
        provider_message_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, object]:
        engine = CommunicationPlatformEngine()
        payload = engine.telegram.build_payload(chat_id=chat_id, body=body)
        recipient_text = str(chat_id or "").strip()
        recipient_value: str | int = chat_id if isinstance(chat_id, int) else recipient_text
        payload.update(
            {
                "external_chat_id": external_chat_id or recipient_text,
                "external_user_id": external_user_id or "",
                "provider_message_id": provider_message_id or "",
            }
        )
        now = _utcnow()
        request_row = self.create_communication_message(
            channel_type="telegram",
            body=body,
            status="sending",
            thread_id=thread_id,
            contact_id=contact_id,
            payload=payload,
            metadata=metadata or {
                "external_chat_id": external_chat_id or recipient_text,
                "external_user_id": external_user_id or "",
                "provider_message_id": provider_message_id or "",
                "delivery_stage": "request_created",
            },
        )
        request_summary = {
            "channel": "telegram",
            "message_id": int(request_row["id"]),
            "recipient": mask_delivery_recipient(recipient_text),
            "response_length": len(body.strip()),
            "provider": "telegram",
            "selected_provider": "telegram",
            "stage": "delivery_start",
        }
        self.create_communication_log(
            level="info",
            message="Telegram outbound delivery started",
            payload=request_summary,
            message_id=int(request_row["id"]),
        )
        LOGGER.info("%s", json.dumps(request_summary, ensure_ascii=False, sort_keys=True))
        if should_use_real_delivery():
            bot_row = self.one("SELECT id FROM telegram_bots ORDER BY id LIMIT 1")
            bot_id = int(bot_row["id"]) if bot_row and bot_row.get("id") is not None else None
            bot_token = (os.getenv("TELEGRAM_BOT_TOKEN") or "").strip()
            if bot_token and recipient_text:
                delivery = send_telegram_message(
                    bot_token=bot_token,
                    chat_id=recipient_value,
                    message=body,
                )
            else:
                missing = [
                    name
                    for name, value in (
                        ("TELEGRAM_BOT_TOKEN", bot_token),
                        ("TELEGRAM_CHAT_ID", recipient_text),
                    )
                    if not value
                ]
                delivery = failed_delivery(
                    provider="telegram",
                    method="POST",
                    url=f"https://api.telegram.org/bot[redacted]/sendMessage",
                    payload={"chat_id": recipient_value, "text": body},
                    recipient=recipient_text,
                    error_type="unconfigured",
                    error_message=f"Missing Telegram delivery configuration: {', '.join(missing)}",
                )
        else:
            bot_row = self.one("SELECT id FROM telegram_bots ORDER BY id LIMIT 1")
            bot_id = int(bot_row["id"]) if bot_row and bot_row.get("id") is not None else None
            delivery = dry_run_delivery(
                provider="telegram",
                method="POST",
                url="https://api.telegram.org/bot[redacted]/sendMessage",
                payload={"chat_id": recipient_value, "text": body},
                recipient=recipient_text,
            )
        delivery_record = sanitize_delivery_record(delivery, recipient=recipient_text)
        outbound_status = "sent" if delivery.ok else "failed"
        request_metadata = {
            "external_chat_id": external_chat_id or recipient_text,
            "external_user_id": external_user_id or "",
            "provider_message_id": delivery.provider_message_id,
            "provider_response": delivery_record,
            "provider_status": delivery.delivery_status,
            "delivery_status": outbound_status,
            "resolved_ipv4": delivery.resolved_ipv4,
            "sanitized_url": delivery.sanitized_url,
        }
        self.update_communication_message(
            int(request_row["id"]),
            status=outbound_status,
            sent_at=now,
            metadata=request_metadata,
            payload={**payload, "provider_response": delivery_record},
        )
        key = f"tg-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO telegram_messages (
                    message_key, status, metadata_json, created_at, bot_id, message_id, chat_id, body,
                    telegram_status, sent_at
                ) VALUES (?, 'active', ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    key,
                    json.dumps(request_metadata, ensure_ascii=False, sort_keys=True),
                    now,
                    bot_id,
                    request_row["id"],
                    chat_id,
                    body,
                    outbound_status,
                    now,
                ),
            )
        row = dict(self.one("SELECT * FROM telegram_messages WHERE message_key = ?", (key,)))
        self.create_communication_log(
            level="info" if delivery.ok else "warning",
            message="Telegram outbound delivery completed" if delivery.ok else "Telegram outbound delivery failed",
            payload={
                "channel": "telegram",
                "message_id": int(request_row["id"]),
                "telegram_message_id": int(row["id"]),
                "recipient": mask_delivery_recipient(recipient_text),
                "response_length": len(body.strip()),
                "provider": delivery.provider,
                "selected_provider": "telegram",
                "delivery_status": outbound_status,
                "http_status": delivery.http_status,
                "provider_message_id": delivery.provider_message_id,
                "resolved_ipv4": delivery.resolved_ipv4,
                "sanitized_url": delivery.sanitized_url,
                "error_type": delivery.error_type,
            },
            message_id=int(request_row["id"]),
        )
        LOGGER.info(
            "%s",
            json.dumps(
                {
                    "channel": "telegram",
                    "message_id": int(request_row["id"]),
                    "telegram_message_id": int(row["id"]),
                    "recipient": mask_delivery_recipient(recipient_text),
                    "response_length": len(body.strip()),
                    "provider": delivery.provider,
                    "selected_provider": "telegram",
                    "delivery_status": outbound_status,
                    "http_status": delivery.http_status,
                    "provider_message_id": delivery.provider_message_id,
                    "resolved_ipv4": delivery.resolved_ipv4,
                    "sanitized_url": delivery.sanitized_url,
                    "error_type": delivery.error_type,
                },
                ensure_ascii=False,
                sort_keys=True,
            ),
        )
        row["delivery"] = delivery_record
        row["communication_message_id"] = int(request_row["id"])
        row["delivery_status"] = outbound_status
        row["provider_message_id"] = delivery.provider_message_id
        return row

    def list_telegram_messages(self, *, limit: int = 50) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM telegram_messages ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    def send_push(
        self,
        *,
        title: str,
        body: str,
        device_id: int | None = None,
    ) -> dict[str, object]:
        engine = CommunicationPlatformEngine()
        payload = engine.push.build_payload(title=title, body=body)
        result = engine.push.stub_send(payload)
        now = _utcnow()
        msg = self.create_communication_message(channel_type="push", subject=title, body=body, status="sent")
        key = f"push-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO push_notifications (
                    notification_key, device_id, message_id, title, body,
                    push_status, sent_at, status, created_at
                ) VALUES (?, ?, ?, ?, ?, 'sent', ?, 'active', ?)
                """,
                (key, device_id, msg["id"], title, body, now, now),
            )
        row = dict(self.one("SELECT * FROM push_notifications WHERE notification_key = ?", (key,)))
        row["delivery"] = result
        return row

    def list_push_notifications(self, *, limit: int = 50) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM push_notifications ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    def register_push_device(
        self,
        *,
        user_id: int,
        platform: str = "web",
        device_token: str = "",
    ) -> dict[str, object]:
        now = _utcnow()
        key = f"device-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO push_devices (
                    device_key, user_id, platform, device_token, status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, 'active', ?, ?)
                """,
                (key, user_id, platform, device_token, now, now),
            )
        return dict(self.one("SELECT * FROM push_devices WHERE device_key = ?", (key,)))

    # --- Campaigns ---

    def create_campaign(
        self,
        *,
        name: str,
        campaign_type: str = "multichannel",
        organization_id: int | None = None,
        scheduled_at: str | None = None,
    ) -> dict[str, object]:
        now = _utcnow()
        key = f"camp-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO campaigns (
                    campaign_key, name, campaign_type, organization_id, campaign_status,
                    scheduled_at, status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, 'draft', ?, 'active', ?, ?)
                """,
                (key, name, campaign_type, organization_id, scheduled_at, now, now),
            )
        return dict(self.one("SELECT * FROM campaigns WHERE campaign_key = ?", (key,)))

    def list_campaigns(self, *, status: str | None = None, limit: int = 50) -> list[dict[str, object]]:
        if status:
            rows = self.all(
                "SELECT * FROM campaigns WHERE campaign_status = ? ORDER BY id DESC LIMIT ?",
                (status, limit),
            )
        else:
            rows = self.all("SELECT * FROM campaigns ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    def update_campaign(self, campaign_id: int, **fields: object) -> dict[str, object]:
        allowed = {"name", "campaign_status", "campaign_type", "scheduled_at", "started_at", "completed_at"}
        updates = {k: v for k, v in fields.items() if k in allowed and v is not None}
        if not updates:
            row = self.one("SELECT * FROM campaigns WHERE id = ?", (campaign_id,))
            if row is None:
                from ..errors import NotFoundError

                raise NotFoundError("campaign not found")
            return dict(row)
        updates["updated_at"] = _utcnow()
        cols = ", ".join(f"{k} = ?" for k in updates)
        with self._transaction() as conn:
            conn.execute(f"UPDATE campaigns SET {cols} WHERE id = ?", (*updates.values(), campaign_id))
        row = self.one("SELECT * FROM campaigns WHERE id = ?", (campaign_id,))
        return dict(row)

    def execute_campaign(self, campaign_id: int) -> dict[str, object]:
        engine = CommunicationPlatformEngine()
        campaign = self.one("SELECT * FROM campaigns WHERE id = ?", (campaign_id,))
        if campaign is None:
            from ..errors import NotFoundError

            raise NotFoundError("campaign not found")
        now = _utcnow()
        key = f"exec-{uuid.uuid4().hex[:10]}"
        channels_rows = self.all(
            "SELECT channel_type FROM campaign_channels WHERE campaign_id = ?",
            (campaign_id,),
        )
        channels = [str(r["channel_type"]) for r in channels_rows] or ["email"]
        plan = engine.campaign.plan_execution(campaign=dict(campaign), channels=channels)
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO campaign_executions (
                    execution_key, campaign_id, execution_status, started_at, status, created_at
                ) VALUES (?, ?, 'running', ?, 'active', ?)
                """,
                (key, campaign_id, now, now),
            )
            conn.execute(
                "UPDATE campaigns SET campaign_status = 'running', started_at = ?, updated_at = ? WHERE id = ?",
                (now, now, campaign_id),
            )
        execution = dict(self.one("SELECT * FROM campaign_executions WHERE execution_key = ?", (key,)))
        execution["plan"] = plan
        return execution

    # --- Queue ---

    def enqueue_message(
        self,
        *,
        job_type: str = "send_message",
        channel_type: str = "email",
        priority: str = "normal",
        payload: dict[str, Any] | None = None,
        scheduled_at: str | None = None,
    ) -> dict[str, object]:
        engine = CommunicationPlatformEngine()
        if channel_type not in CHANNEL_TYPES:
            channel_type = "email"
        if priority not in MESSAGE_PRIORITIES:
            priority = "normal"
        now = _utcnow()
        key = f"job-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO queue_jobs (
                    job_key, job_type, channel_type, priority, job_status, payload_json,
                    scheduled_at, status, created_at
                ) VALUES (?, ?, ?, ?, 'pending', ?, ?, 'active', ?)
                """,
                (key, job_type, channel_type, priority, _json(payload or {}), scheduled_at, now),
            )
        return dict(self.one("SELECT * FROM queue_jobs WHERE job_key = ?", (key,)))

    def list_queue_jobs(
        self,
        *,
        job_status: str | None = None,
        limit: int = 50,
    ) -> list[dict[str, object]]:
        if job_status:
            rows = self.all(
                "SELECT * FROM queue_jobs WHERE job_status = ? ORDER BY id DESC LIMIT ?",
                (job_status, limit),
            )
        else:
            rows = self.all("SELECT * FROM queue_jobs ORDER BY id DESC LIMIT ?", (limit,))
        engine = CommunicationPlatformEngine()
        return engine.priority.sort_jobs([dict(r) for r in rows])

    def retry_job(self, job_id: int) -> dict[str, object]:
        engine = CommunicationPlatformEngine()
        row = self.one("SELECT * FROM queue_jobs WHERE id = ?", (job_id,))
        if row is None:
            from ..errors import NotFoundError

            raise NotFoundError("job not found")
        attempt = int(row["attempt_count"] or 0) + 1
        max_attempts = int(row["max_attempts"] or 3)
        plan = engine.retry.plan_retry(attempt_count=attempt, max_attempts=max_attempts)
        now = _utcnow()
        retry_key = f"retry-{uuid.uuid4().hex[:8]}"
        new_status = "retrying" if plan["retry"] else "dead_letter"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO queue_retry_history (
                    retry_key, job_id, attempt_number, retry_at, result, status, created_at
                ) VALUES (?, ?, ?, ?, ?, 'active', ?)
                """,
                (retry_key, job_id, attempt, now, _json(plan), now),
            )
            conn.execute(
                """
                UPDATE queue_jobs
                SET attempt_count = ?, job_status = ?
                WHERE id = ?
                """,
                (attempt, new_status, job_id),
            )
            if not plan["retry"]:
                conn.execute(
                    """
                    INSERT INTO queue_failures (
                        failure_key, job_id, error_code, error_message, failed_at, status, created_at
                    ) VALUES (?, ?, 'max_attempts', 'Retry limit reached', ?, 'active', ?)
                    """,
                    (f"fail-{uuid.uuid4().hex[:8]}", job_id, now, now),
                )
        return dict(self.one("SELECT * FROM queue_jobs WHERE id = ?", (job_id,)))

    def process_next_queue_job(self) -> dict[str, object] | None:
        engine = CommunicationPlatformEngine()
        row = self.one(
            """
            SELECT * FROM queue_jobs
            WHERE job_status = 'pending'
            ORDER BY id ASC LIMIT 1
            """
        )
        if row is None:
            return None
        job = dict(row)
        if not engine.scheduler.is_due(scheduled_at=str(job.get("scheduled_at") or "")):
            return None
        now = _utcnow()
        job_id = int(job["id"])
        with self._transaction() as conn:
            conn.execute(
                "UPDATE queue_jobs SET job_status = 'completed', completed_at = ? WHERE id = ?",
                (now, job_id),
            )
        return dict(self.one("SELECT * FROM queue_jobs WHERE id = ?", (job_id,)))

    # --- Preferences ---

    def get_communication_preference(
        self,
        *,
        user_id: int | None = None,
        contact_id: int | None = None,
        channel_type: str = "email",
    ) -> dict[str, object] | None:
        if user_id is not None:
            row = self.one(
                """
                SELECT * FROM communication_preferences
                WHERE user_id = ? AND channel_type = ?
                ORDER BY id DESC LIMIT 1
                """,
                (user_id, channel_type),
            )
        elif contact_id is not None:
            row = self.one(
                """
                SELECT * FROM communication_preferences
                WHERE contact_id = ? AND channel_type = ?
                ORDER BY id DESC LIMIT 1
                """,
                (contact_id, channel_type),
            )
        else:
            return None
        return dict(row) if row else None

    def upsert_communication_preference(
        self,
        *,
        user_id: int | None = None,
        contact_id: int | None = None,
        channel_type: str = "email",
        enabled: bool = True,
        settings: dict[str, Any] | None = None,
    ) -> dict[str, object]:
        existing = self.get_communication_preference(
            user_id=user_id, contact_id=contact_id, channel_type=channel_type
        )
        now = _utcnow()
        if existing:
            pref_id = int(existing["id"])
            with self._transaction() as conn:
                conn.execute(
                    """
                    UPDATE communication_preferences
                    SET enabled = ?, settings_json = ?, updated_at = ?
                    WHERE id = ?
                    """,
                    (1 if enabled else 0, _json(settings or {}), now, pref_id),
                )
            return dict(self.one("SELECT * FROM communication_preferences WHERE id = ?", (pref_id,)))
        key = f"pref-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO communication_preferences (
                    preference_key, user_id, contact_id, channel_type, enabled,
                    settings_json, status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, 'active', ?, ?)
                """,
                (key, user_id, contact_id, channel_type, 1 if enabled else 0, _json(settings or {}), now, now),
            )
        return dict(self.one("SELECT * FROM communication_preferences WHERE preference_key = ?", (key,)))

    def list_communication_consents(self, *, user_id: int | None = None, limit: int = 50) -> list[dict[str, object]]:
        if user_id is not None:
            rows = self.all(
                "SELECT * FROM communication_consent_history WHERE user_id = ? ORDER BY id DESC LIMIT ?",
                (user_id, limit),
            )
        else:
            rows = self.all("SELECT * FROM communication_consent_history ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    def record_communication_consent(
        self,
        *,
        user_id: int | None = None,
        contact_id: int | None = None,
        consent_type: str = "marketing",
        consent_status: str = "granted",
    ) -> dict[str, object]:
        now = _utcnow()
        key = f"consent-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO communication_consent_history (
                    consent_key, user_id, contact_id, consent_type, consent_status,
                    recorded_at, status, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, 'active', ?)
                """,
                (key, user_id, contact_id, consent_type, consent_status, now, now),
            )
        return dict(self.one("SELECT * FROM communication_consent_history WHERE consent_key = ?", (key,)))

    def get_quiet_hours(self, *, user_id: int) -> dict[str, object] | None:
        row = self.one(
            "SELECT * FROM communication_quiet_hours WHERE user_id = ? ORDER BY id DESC LIMIT 1",
            (user_id,),
        )
        return dict(row) if row else None

    # --- Event bus ---

    def process_communication_event(
        self,
        *,
        event_kind: str,
        source_program: str = "platform",
        payload: dict[str, Any] | None = None,
    ) -> dict[str, object]:
        engine = CommunicationPlatformEngine()
        mapping = engine.integration.map_event_kind(event_kind)
        now = _utcnow()
        key = f"evt-{uuid.uuid4().hex[:10]}"
        channel_type = str(mapping.get("default_channel") or "in_app")
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO communication_events (
                    event_key, event_kind, source_program, payload_json, status, created_at
                ) VALUES (?, ?, ?, ?, 'active', ?)
                """,
                (key, event_kind, source_program, _json(payload or {}), now),
            )
        event_row = dict(self.one("SELECT * FROM communication_events WHERE event_key = ?", (key,)))
        notification = None
        if mapping.get("valid") and event_kind in EVENT_KINDS:
            title = f"Événement {event_kind}"
            notification = self.create_notification_event(
                notification_type="system",
                title=title,
                body=str((payload or {}).get("message") or event_kind),
                priority="high" if event_kind.startswith("Security") else "normal",
                payload={"event_kind": event_kind, "source_program": source_program},
            )
            self.enqueue_message(
                job_type="send_notification",
                channel_type=channel_type,
                payload={"notification_id": notification.get("id"), "event_kind": event_kind},
            )
        return {
            "event": event_row,
            "mapping": mapping,
            "notification": notification,
        }

    # --- Analytics ---

    def snapshot_communication_dashboard(self) -> dict[str, object]:
        metrics = {
            "messages": self.scalar("SELECT COUNT(*) FROM communication_messages"),
            "notifications": self.scalar("SELECT COUNT(*) FROM notification_events"),
            "campaigns": self.scalar("SELECT COUNT(*) FROM campaigns"),
            "queue_pending": self.scalar("SELECT COUNT(*) FROM queue_jobs WHERE job_status = 'pending'"),
            "email_sent": self.scalar("SELECT COUNT(*) FROM email_messages WHERE email_status = 'sent'"),
            "sms_sent": self.scalar("SELECT COUNT(*) FROM sms_messages WHERE sms_status = 'sent'"),
            "whatsapp_sent": self.scalar("SELECT COUNT(*) FROM whatsapp_messages WHERE whatsapp_status = 'sent'"),
            "telegram_sent": self.scalar("SELECT COUNT(*) FROM telegram_messages WHERE telegram_status = 'sent'"),
            "push_sent": self.scalar("SELECT COUNT(*) FROM push_notifications WHERE push_status = 'sent'"),
            "failures": self.scalar("SELECT COUNT(*) FROM queue_failures"),
        }
        now = _utcnow()
        key = f"snap-{uuid.uuid4().hex[:8]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO communication_dashboard_snapshots (
                    snapshot_key, scope, metrics_json, snapshot_at, status, created_at
                ) VALUES (?, 'global', ?, ?, 'active', ?)
                """,
                (key, _json(metrics), now, now),
            )
        return metrics

    def communication_analytics(self) -> dict[str, object]:
        latest = self.one("SELECT * FROM communication_dashboard_snapshots ORDER BY id DESC LIMIT 1")
        if latest is None:
            metrics = self.snapshot_communication_dashboard()
            return {"metrics": metrics, "snapshot": None}
        return {"metrics": _parse_json(str(latest.get("metrics_json"))) or {}, "snapshot": dict(latest)}

    def communication_dashboard(self) -> dict[str, object]:
        analytics = self.communication_analytics()
        return {
            "summary": analytics.get("metrics") or {},
            "recent_messages": self.list_communication_messages(limit=5),
            "recent_notifications": self.list_notification_events(limit=5),
            "active_campaigns": self.list_campaigns(status="running", limit=5),
            "queue_pending": self.scalar("SELECT COUNT(*) FROM queue_jobs WHERE job_status = 'pending'"),
            "integrations": self.integration_sources(),
        }

    def communication_stats(self) -> dict[str, object]:
        return {
            "messages_total": self.scalar("SELECT COUNT(*) FROM communication_messages"),
            "messages_sent": self.scalar("SELECT COUNT(*) FROM communication_messages WHERE status = 'sent'"),
            "messages_failed": self.scalar("SELECT COUNT(*) FROM communication_messages WHERE status = 'failed'"),
            "notifications_total": self.scalar("SELECT COUNT(*) FROM notification_events"),
            "campaigns_active": self.scalar(
                "SELECT COUNT(*) FROM campaigns WHERE campaign_status IN ('running', 'scheduled')"
            ),
            "queue_pending": self.scalar("SELECT COUNT(*) FROM queue_jobs WHERE job_status = 'pending'"),
            "queue_failed": self.scalar("SELECT COUNT(*) FROM queue_jobs WHERE job_status = 'failed'"),
            "templates_active": self.scalar("SELECT COUNT(*) FROM notification_templates WHERE status = 'active'"),
        }

    def list_ai_recommendations(
        self,
        *,
        user_id: int | None = None,
        contact_id: int | None = None,
        limit: int = 20,
    ) -> list[dict[str, object]]:
        engine = CommunicationPlatformEngine()
        stored: list[dict[str, object]] = []
        if contact_id is not None:
            rows = self.all(
                "SELECT * FROM communication_ai_recommendations WHERE contact_id = ? ORDER BY id DESC LIMIT ?",
                (contact_id, limit),
            )
            stored = [dict(r) for r in rows]
        if stored:
            return stored
        rec = engine.ai_recommendation.recommend_followup(contact_id=contact_id, last_channel="whatsapp")
        now = _utcnow()
        key = f"airec-{uuid.uuid4().hex[:8]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO communication_ai_recommendations (
                    recommendation_key, user_id, contact_id, recommendation_type,
                    recommendation_json, score, generated_at, status, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, 'active', ?)
                """,
                (
                    key,
                    user_id,
                    contact_id,
                    rec["recommendation_type"],
                    _json(rec),
                    rec["score"],
                    now,
                    now,
                ),
            )
        row = self.one("SELECT * FROM communication_ai_recommendations WHERE recommendation_key = ?", (key,))
        return [dict(row)] if row else []

    def list_communication_events(self, *, limit: int = 50) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM communication_events ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    def list_communication_history(self, *, limit: int = 50) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM communication_history ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    def search_communication_messages(self, *, query: str, limit: int = 50) -> list[dict[str, object]]:
        pattern = f"%{query.strip()}%"
        rows = self.all(
            """
            SELECT * FROM communication_messages
            WHERE body LIKE ? OR subject LIKE ?
            ORDER BY id DESC LIMIT ?
            """,
            (pattern, pattern, limit),
        )
        return [dict(r) for r in rows]

    def list_communication_groups(self, *, limit: int = 50) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM communication_groups ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    def list_inapp_notifications(self, *, user_id: int | None = None, limit: int = 50) -> list[dict[str, object]]:
        if user_id is not None:
            rows = self.all(
                "SELECT * FROM inapp_notifications WHERE user_id = ? ORDER BY id DESC LIMIT ?",
                (user_id, limit),
            )
        else:
            rows = self.all("SELECT * FROM inapp_notifications ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    def export_communication_snapshot(self) -> dict[str, object]:
        return {
            "stats": self.communication_stats(),
            "messages": self.list_communication_messages(limit=100),
            "templates": self.list_notification_templates(limit=100),
        }

    def import_communication_payload(self, payload: dict[str, object]) -> dict[str, object]:
        imported = 0
        for item in list(payload.get("templates") or []):
            if isinstance(item, dict) and item.get("name"):
                self.create_notification_template(
                    name=str(item["name"]),
                    channel_type=str(item.get("channel_type") or "email"),
                    subject=str(item.get("subject") or ""),
                    body=str(item.get("body") or ""),
                )
                imported += 1
        return {"imported": imported}
