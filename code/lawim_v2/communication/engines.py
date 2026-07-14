from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Any

from ..contact import official_signature_block, to_public_dict
from .constants import (
    CAMPAIGN_STATUSES,
    CHANNEL_TYPES,
    DELIVERY_STATUSES,
    EVENT_KINDS,
    MESSAGE_PRIORITIES,
    MESSAGE_STATUSES,
    NOTIFICATION_TYPES,
    QUEUE_JOB_STATUSES,
    SMS_PROVIDERS,
)


class CommunicationEngine:
    def validate_channel(self, channel_type: str) -> str:
        return channel_type if channel_type in CHANNEL_TYPES else "email"

    def validate_status(self, status: str) -> str:
        return status if status in MESSAGE_STATUSES else "draft"

    def build_message_payload(
        self,
        *,
        channel_type: str,
        body: str,
        subject: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, object]:
        return {
            "channel_type": self.validate_channel(channel_type),
            "subject": subject,
            "body": body.strip(),
            "metadata": metadata or {},
            "sender": to_public_dict(),
        }

    def format_outbound_body(self, body: str, *, include_signature: bool = True) -> str:
        text = body.strip()
        if include_signature:
            text = f"{text}\n\n{official_signature_block()}"
        return text


class NotificationEngine:
    def validate_type(self, notification_type: str) -> str:
        return notification_type if notification_type in NOTIFICATION_TYPES else "system"

    def should_deliver(
        self,
        *,
        notification_type: str,
        channel_type: str,
        preferences: dict[str, object] | None,
        quiet_hours_active: bool = False,
    ) -> dict[str, object]:
        if quiet_hours_active and notification_type not in {"critical", "urgent", "security"}:
            return {"deliver": False, "reason": "quiet_hours"}
        if preferences is None:
            return {"deliver": True, "reason": "default"}
        enabled = preferences.get("enabled")
        if enabled is not None and not bool(enabled):
            return {"deliver": False, "reason": "preference_disabled"}
        settings_raw = preferences.get("settings_json") or "{}"
        try:
            settings = json.loads(str(settings_raw)) if isinstance(settings_raw, str) else dict(settings_raw)
        except (json.JSONDecodeError, TypeError):
            settings = {}
        blocked = settings.get("blocked_channels") or []
        if channel_type in blocked:
            return {"deliver": False, "reason": "channel_blocked"}
        return {"deliver": True, "reason": "allowed"}


class EmailEngine:
    def build_payload(
        self,
        *,
        to_email: str,
        subject: str,
        body: str,
        html: bool = False,
        cc: list[str] | None = None,
        bcc: list[str] | None = None,
    ) -> dict[str, object]:
        sender = to_public_dict()
        return {
            "from_email": sender["support_email"],
            "to_email": to_email,
            "subject": subject,
            "body": body,
            "html": html,
            "cc": cc or [],
            "bcc": bcc or [],
            "channel": "email",
            "lawim_sender_json": sender,
        }

    def stub_send(self, payload: dict[str, object]) -> dict[str, object]:
        return {"sent": True, "provider": "architecture_only", "payload": payload}


class SmsEngine:
    MAX_LENGTH = 160

    def normalize_provider(self, provider: str) -> str:
        return provider if provider in SMS_PROVIDERS else "twilio"

    def build_payload(self, *, to_number: str, body: str, provider: str = "orange") -> dict[str, object]:
        sender = to_public_dict()
        return {
            "from_number": sender["phone_e164"],
            "to_number": to_number,
            "body": body[: self.MAX_LENGTH],
            "provider": self.normalize_provider(provider),
            "channel": "sms",
            "lawim_sender_json": sender,
        }

    def stub_send(self, payload: dict[str, object]) -> dict[str, object]:
        return {"sent": True, "provider": str(payload.get("provider")), "architecture_only": True}


class WhatsappEngine:
    def build_payload(self, *, to_number: str, body: str, template_name: str | None = None) -> dict[str, object]:
        sender = to_public_dict()
        return {
            "from_handle": sender["whatsapp_username"],
            "to_number": to_number,
            "body": body,
            "template_name": template_name,
            "channel": "whatsapp",
            "lawim_sender_json": sender,
        }

    def stub_send(self, payload: dict[str, object]) -> dict[str, object]:
        return {"sent": True, "provider": "meta_cloud", "architecture_only": True}


class TelegramEngine:
    def build_payload(self, *, chat_id: str, body: str) -> dict[str, object]:
        sender = to_public_dict()
        return {
            "from_handle": sender["telegram_bot"],
            "chat_id": chat_id,
            "body": body,
            "channel": "telegram",
            "lawim_sender_json": sender,
        }

    def stub_send(self, payload: dict[str, object]) -> dict[str, object]:
        return {"sent": True, "provider": "telegram", "architecture_only": True}


class PushEngine:
    def build_payload(self, *, title: str, body: str, platform: str = "web") -> dict[str, object]:
        return {
            "title": title,
            "body": body,
            "platform": platform,
            "channel": "push",
        }

    def stub_send(self, payload: dict[str, object]) -> dict[str, object]:
        return {"sent": True, "provider": "architecture_only", "payload": payload}


class CampaignEngine:
    def validate_status(self, status: str) -> str:
        return status if status in CAMPAIGN_STATUSES else "draft"

    def can_transition(self, *, current: str, target: str) -> bool:
        allowed: dict[str, set[str]] = {
            "draft": {"scheduled", "running", "cancelled"},
            "scheduled": {"running", "paused", "cancelled"},
            "running": {"paused", "completed", "cancelled"},
            "paused": {"running", "cancelled", "archived"},
            "completed": {"archived"},
            "cancelled": {"archived"},
        }
        return target in allowed.get(current, set())

    def plan_execution(self, *, campaign: dict[str, object], channels: list[str]) -> dict[str, object]:
        return {
            "campaign_id": campaign.get("id"),
            "channels": channels,
            "status": "planned",
            "steps": [{"channel": ch, "action": "send"} for ch in channels],
        }


class QueueEngine:
    def validate_job_status(self, status: str) -> str:
        return status if status in QUEUE_JOB_STATUSES else "pending"

    def should_retry(self, *, attempt_count: int, max_attempts: int = 3) -> bool:
        return attempt_count < max_attempts

    def next_retry_delay(self, attempt_count: int) -> int:
        return min(3600, 2 ** max(0, attempt_count) * 30)


class TemplateEngine:
    _VAR_PATTERN = re.compile(r"\{\{\s*(\w+)\s*\}\}")

    def extract_variables(self, content: str) -> list[str]:
        return sorted(set(self._VAR_PATTERN.findall(content)))

    def render(self, *, template: str, variables: dict[str, Any]) -> str:
        def repl(match: re.Match[str]) -> str:
            key = match.group(1)
            return str(variables.get(key, match.group(0)))

        return self._VAR_PATTERN.sub(repl, template)

    def validate(self, *, subject: str, body: str, required: list[str] | None = None) -> dict[str, object]:
        found = set(self.extract_variables(subject) + self.extract_variables(body))
        missing = [v for v in (required or []) if v not in found]
        return {"valid": len(missing) == 0, "variables": sorted(found), "missing": missing}


class PreferenceEngine:
    def merge_preferences(
        self,
        *,
        user_prefs: list[dict[str, object]],
        channel_type: str,
    ) -> dict[str, object] | None:
        for pref in user_prefs:
            if str(pref.get("channel_type") or "") == channel_type:
                return pref
        return None

    def is_quiet_hours(
        self,
        *,
        quiet_hours: dict[str, object] | None,
        now: datetime | None = None,
    ) -> bool:
        if quiet_hours is None:
            return False
        ref = now or datetime.now(timezone.utc)
        start = str(quiet_hours.get("start_time") or "22:00")
        end = str(quiet_hours.get("end_time") or "07:00")
        try:
            sh, sm = map(int, start.split(":"))
            eh, em = map(int, end.split(":"))
        except ValueError:
            return False
        current_minutes = ref.hour * 60 + ref.minute
        start_minutes = sh * 60 + sm
        end_minutes = eh * 60 + em
        if start_minutes <= end_minutes:
            return start_minutes <= current_minutes < end_minutes
        return current_minutes >= start_minutes or current_minutes < end_minutes


class AnalyticsEngine:
    def aggregate_metrics(self, *, counters: dict[str, int]) -> dict[str, object]:
        total = sum(counters.values())
        return {
            "total": total,
            "counters": counters,
            "channels": {k: v for k, v in counters.items() if k.startswith("channel_")},
        }

    def dashboard_summary(self, *, metrics: dict[str, object]) -> dict[str, object]:
        return {
            "messages_sent": metrics.get("messages_sent", 0),
            "messages_failed": metrics.get("messages_failed", 0),
            "avg_delivery_ms": metrics.get("avg_delivery_ms", 0),
            "campaigns_active": metrics.get("campaigns_active", 0),
            "queue_pending": metrics.get("queue_pending", 0),
        }


class CommunicationStatisticsEngine:
    def compute_rates(self, *, sent: int, delivered: int, failed: int) -> dict[str, object]:
        total = max(1, sent)
        return {
            "sent": sent,
            "delivered": delivered,
            "failed": failed,
            "delivery_rate": round(delivered / total, 4),
            "failure_rate": round(failed / total, 4),
        }


class AiCommunicationRecommendationEngine:
    def recommend_followup(
        self,
        *,
        contact_id: int | None,
        last_channel: str | None,
        days_since_contact: int = 0,
    ) -> dict[str, object]:
        channel = last_channel or "whatsapp"
        if channel not in CHANNEL_TYPES:
            channel = "email"
        urgency = "high" if days_since_contact >= 7 else "normal"
        return {
            "contact_id": contact_id,
            "recommended_channel": channel,
            "recommendation_type": "followup",
            "urgency": urgency,
            "score": min(100, 50 + days_since_contact * 5),
            "message_hint": "Relance client recommandée",
        }


class DeliveryScheduler:
    def is_due(self, *, scheduled_at: str | None, now: datetime | None = None) -> bool:
        if not scheduled_at:
            return True
        try:
            due = datetime.fromisoformat(str(scheduled_at).replace("Z", "+00:00"))
            if due.tzinfo is None:
                due = due.replace(tzinfo=timezone.utc)
        except ValueError:
            return True
        ref = now or datetime.now(timezone.utc)
        return ref >= due


class RetryEngine:
    def plan_retry(self, *, attempt_count: int, max_attempts: int = 3, error_code: str = "") -> dict[str, object]:
        retry = attempt_count < max_attempts
        delay = min(3600, 2 ** max(0, attempt_count) * 30)
        return {
            "retry": retry,
            "attempt_count": attempt_count,
            "max_attempts": max_attempts,
            "delay_seconds": delay if retry else 0,
            "dead_letter": not retry,
            "error_code": error_code,
        }


class PriorityEngine:
    WEIGHTS = {"low": 1, "normal": 5, "high": 10, "urgent": 20, "critical": 50}

    def weight(self, priority: str) -> int:
        return self.WEIGHTS.get(priority if priority in MESSAGE_PRIORITIES else "normal", 5)

    def sort_jobs(self, jobs: list[dict[str, object]]) -> list[dict[str, object]]:
        return sorted(
            jobs,
            key=lambda j: (
                -self.weight(str(j.get("priority") or "normal")),
                str(j.get("scheduled_at") or ""),
                int(j.get("id") or 0),
            ),
        )


class RoutingEngine:
    def route(self, *, channel_type: str, event_kind: str | None = None) -> dict[str, object]:
        channel = channel_type if channel_type in CHANNEL_TYPES else "in_app"
        if event_kind and event_kind in EVENT_KINDS:
            if event_kind.startswith("Security"):
                channel = "in_app"
            elif event_kind in {"LeadQualified", "CustomerCreated", "CustomerUpdated"}:
                channel = "email"
        return {"channel_type": channel, "event_kind": event_kind, "routed": True}


class ConversationEngine:
    def thread_key_for_participants(self, *, user_id: int | None, contact_id: int | None) -> str:
        parts = [f"u{user_id or 0}", f"c{contact_id or 0}"]
        return "thread-" + "-".join(parts)

    def append_to_thread(
        self,
        *,
        thread: dict[str, object],
        message: dict[str, object],
    ) -> dict[str, object]:
        return {
            "thread_id": thread.get("id"),
            "message_id": message.get("id"),
            "subject": thread.get("subject") or message.get("subject"),
            "last_message_at": message.get("created_at"),
        }


class IntegrationBridge:
    PROGRAM_SOURCES: tuple[str, ...] = (
        "intelligent_core",
        "ecosystem",
        "cognition",
        "maintenance",
        "knowledge_platform",
        "workflow_automation",
        "real_estate_intelligence",
        "crm",
        "marketplace",
        "security",
        "source_intelligence",
    )

    def sources(self) -> list[str]:
        return list(self.PROGRAM_SOURCES)

    def map_event_kind(self, event_kind: str) -> dict[str, object]:
        if event_kind not in EVENT_KINDS:
            return {"valid": False, "event_kind": event_kind}
        channel = "in_app"
        if event_kind in {"LeadQualified", "CustomerCreated", "InvoiceGenerated"}:
            channel = "email"
        elif event_kind in {"SecurityAlertRaised", "SecurityIncident"}:
            channel = "in_app"
        return {"valid": True, "event_kind": event_kind, "default_channel": channel}


class CommunicationPlatformEngine:
    def __init__(self) -> None:
        self.communication = CommunicationEngine()
        self.notification = NotificationEngine()
        self.email = EmailEngine()
        self.sms = SmsEngine()
        self.whatsapp = WhatsappEngine()
        self.telegram = TelegramEngine()
        self.push = PushEngine()
        self.campaign = CampaignEngine()
        self.queue = QueueEngine()
        self.template = TemplateEngine()
        self.preference = PreferenceEngine()
        self.analytics = AnalyticsEngine()
        self.statistics = CommunicationStatisticsEngine()
        self.ai_recommendation = AiCommunicationRecommendationEngine()
        self.scheduler = DeliveryScheduler()
        self.retry = RetryEngine()
        self.priority = PriorityEngine()
        self.routing = RoutingEngine()
        self.conversation = ConversationEngine()
        self.integration = IntegrationBridge()

    def integration_sources(self) -> list[str]:
        return self.integration.sources()
