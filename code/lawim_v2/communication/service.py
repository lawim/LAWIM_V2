from __future__ import annotations

import re

from ..observability import METRICS
from ..maintenance import MAINTENANCE_FLAGS, MAINTENANCE_RESPONSE, MaintenanceService, MaintenanceSubmission
from ..project_service import ProjectPermissionDenied, ProjectService
from ..financial.engines import normalize_mobile_money_number
from . import dto as cdto
from .delivery import mask_delivery_recipient
from .green_api import (
    GREEN_API_MESSAGE_WEBHOOKS,
    GREEN_API_SUPPORTED_WEBHOOKS,
    build_event_key,
    build_message_key,
    map_message_status,
    normalize_webhook_payload,
    redact_headers,
    summarize_for_log,
)
from .telegram_webhook import (
    TELEGRAM_MESSAGE_UPDATE_TYPES,
    TELEGRAM_SUPPORTED_UPDATE_TYPES,
    build_event_key as build_telegram_event_key,
    build_message_key as build_telegram_message_key,
    normalize_webhook_payload as normalize_telegram_webhook_payload,
    redact_headers as redact_telegram_headers,
    summarize_for_log as summarize_telegram_for_log,
)
from .analytics import AnalyticsModule
from .campaigns import CampaignsModule
from .email import EmailModule
from .engines import CommunicationPlatformEngine
from .integrations import IntegrationsModule
from .notifications import NotificationsModule
from .preferences import PreferencesModule
from .push import PushModule
from .queue import QueueModule
from .sms import SmsModule
from .telegram import TelegramModule
from .templates import TemplatesModule
from .whatsapp import WhatsappModule


class NotificationService:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.module = NotificationsModule(repository)

    def create(self, **kwargs: object) -> dict[str, object]:
        return self.module.create(**kwargs)

    def list_events(self, **kwargs: object) -> list[dict[str, object]]:
        return self.module.list_events(**kwargs)

    def deliver(self, notification_id: int) -> dict[str, object]:
        return self.module.deliver(notification_id)

    def acknowledge(self, **kwargs: object) -> dict[str, object]:
        return self.module.acknowledge(**kwargs)


class EmailService:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.module = EmailModule(repository)

    def send(self, **kwargs: object) -> dict[str, object]:
        return self.module.send(**kwargs)

    def list_messages(self, **kwargs: object) -> list[dict[str, object]]:
        return self.module.list_messages(**kwargs)


class SmsService:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.module = SmsModule(repository)

    def send(self, **kwargs: object) -> dict[str, object]:
        return self.module.send(**kwargs)

    def list_messages(self, **kwargs: object) -> list[dict[str, object]]:
        return self.module.list_messages(**kwargs)


class WhatsappService:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.module = WhatsappModule(repository)

    def send(self, **kwargs: object) -> dict[str, object]:
        return self.module.send(**kwargs)

    def list_messages(self, **kwargs: object) -> list[dict[str, object]]:
        return self.module.list_messages(**kwargs)


class TelegramService:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.module = TelegramModule(repository)

    def send(self, **kwargs: object) -> dict[str, object]:
        return self.module.send(**kwargs)

    def list_messages(self, **kwargs: object) -> list[dict[str, object]]:
        return self.module.list_messages(**kwargs)


class PushService:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.module = PushModule(repository)

    def send(self, **kwargs: object) -> dict[str, object]:
        return self.module.send(**kwargs)

    def list_notifications(self, **kwargs: object) -> list[dict[str, object]]:
        return self.module.list_notifications(**kwargs)

    def register_device(self, **kwargs: object) -> dict[str, object]:
        return self.module.register_device(**kwargs)


class CampaignService:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.module = CampaignsModule(repository)

    def create(self, **kwargs: object) -> dict[str, object]:
        return self.module.create(**kwargs)

    def list_campaigns(self, **kwargs: object) -> list[dict[str, object]]:
        return self.module.list_campaigns(**kwargs)

    def execute(self, campaign_id: int) -> dict[str, object]:
        return self.module.execute(campaign_id)

    def pause(self, campaign_id: int) -> dict[str, object]:
        return self.module.pause(campaign_id)

    def resume(self, campaign_id: int) -> dict[str, object]:
        return self.module.resume(campaign_id)


class TemplateService:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.module = TemplatesModule(repository)

    def create(self, **kwargs: object) -> dict[str, object]:
        return self.module.create(**kwargs)

    def list_templates(self, **kwargs: object) -> list[dict[str, object]]:
        return self.module.list_templates(**kwargs)

    def render(self, **kwargs: object) -> dict[str, object]:
        return self.module.render(**kwargs)


class PreferenceService:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.module = PreferencesModule(repository)

    def get(self, **kwargs: object) -> dict[str, object] | None:
        return self.module.get(**kwargs)

    def upsert(self, **kwargs: object) -> dict[str, object]:
        return self.module.upsert(**kwargs)

    def list_consents(self, **kwargs: object) -> list[dict[str, object]]:
        return self.module.list_consents(**kwargs)

    def record_consent(self, **kwargs: object) -> dict[str, object]:
        return self.module.record_consent(**kwargs)


class QueueService:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.module = QueueModule(repository)

    def enqueue(self, **kwargs: object) -> dict[str, object]:
        return self.module.enqueue(**kwargs)

    def list_jobs(self, **kwargs: object) -> list[dict[str, object]]:
        return self.module.list_jobs(**kwargs)

    def retry(self, job_id: int) -> dict[str, object]:
        return self.module.retry(job_id)

    def process_next(self) -> dict[str, object] | None:
        return self.module.process_next()


class ConversationService:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.engine = CommunicationPlatformEngine().conversation

    def create_thread(self, **kwargs: object) -> dict[str, object]:
        return self.repository.create_communication_thread(**kwargs)

    def list_threads(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_communication_threads(**kwargs)


class AnalyticsService:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.module = AnalyticsModule(repository)

    def stats(self) -> dict[str, object]:
        return self.module.stats()

    def dashboard(self) -> dict[str, object]:
        return self.module.dashboard()

    def analytics(self) -> dict[str, object]:
        return self.module.analytics()

    def snapshot(self) -> dict[str, object]:
        return self.module.snapshot()

    def ai_recommendations(self, **kwargs: object) -> list[dict[str, object]]:
        return self.module.ai_recommendations(**kwargs)


class IntegrationService:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.module = IntegrationsModule(repository)

    def sources(self) -> dict[str, object]:
        return self.module.sources()

    def process_event(self, **kwargs: object) -> dict[str, object]:
        return self.module.process_event(**kwargs)


class CommunicationService:
    def __init__(
        self,
        repository,
        project_service: ProjectService,
        policy,
        config=None,
        maintenance: MaintenanceService | None = None,
        ai_orchestrator=None,
        disclaimer_manager=None,
    ) -> None:
        self.repository = repository
        self.projects = project_service
        self.policy = policy
        self.config = config
        self.maintenance = maintenance or MaintenanceService(repository)
        self.ai = ai_orchestrator
        self.disclaimer = disclaimer_manager
        self.engine = CommunicationPlatformEngine()
        self.notifications = NotificationService(repository)
        self.email = EmailService(repository)
        self.sms = SmsService(repository)
        self.whatsapp = WhatsappService(repository)
        self.telegram = TelegramService(repository)
        self.push = PushService(repository)
        self.campaigns = CampaignService(repository)
        self.templates = TemplateService(repository)
        self.preferences = PreferenceService(repository)
        self.queue = QueueService(repository)
        self.conversations = ConversationService(repository)
        self.analytics_service = AnalyticsService(repository)
        self.integrations = IntegrationService(repository)

    def _require_auth(self, actor: dict[str, object] | None) -> None:
        if actor is None:
            raise ProjectPermissionDenied("Authentication required")

    def _require_admin(self, actor: dict[str, object]) -> None:
        if not self.policy.is_admin(actor):
            raise ProjectPermissionDenied("Admin required")

    # --- Messages ---

    def list_messages(
        self,
        *,
        actor: dict[str, object],
        channel_type: str | None = None,
        status: str | None = None,
        limit: int = 50,
    ) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("communication_message_list")
        rows = self.repository.list_communication_messages(channel_type=channel_type, status=status, limit=limit)
        return {"messages": [cdto.message_dto(r) for r in rows]}

    def create_message(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        sender_id = int(actor["id"]) if actor.get("id") is not None else None
        message = self.repository.create_communication_message(
            channel_type=str(body.get("channel_type") or "email"),
            body=str(body["body"]),
            subject=str(body.get("subject") or ""),
            priority=str(body.get("priority") or "normal"),
            sender_user_id=sender_id,
            recipient_user_id=int(body["recipient_user_id"]) if body.get("recipient_user_id") is not None else None,
            contact_id=int(body["contact_id"]) if body.get("contact_id") is not None else None,
            organization_id=int(body["organization_id"]) if body.get("organization_id") is not None else None,
            scheduled_at=str(body["scheduled_at"]) if body.get("scheduled_at") else None,
            payload=dict(body.get("payload") or {}),
        )
        METRICS.increment("communication_messages_total")
        return {"message": cdto.message_dto(message)}

    def send_message(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        channel_type = str(body.get("channel_type") or "email")
        result: dict[str, object]
        if channel_type == "email":
            result = self.email.send(
                to_email=str(body["to_email"]),
                subject=str(body.get("subject") or ""),
                body=str(body["body"]),
            )
            METRICS.increment("email_messages_total")
        elif channel_type == "sms":
            result = self.sms.send(to_number=str(body["to_number"]), body=str(body["body"]))
            METRICS.increment("sms_messages_total")
        elif channel_type == "whatsapp":
            result = self.whatsapp.send(to_number=str(body["to_number"]), body=str(body["body"]))
            METRICS.increment("whatsapp_messages_total")
        elif channel_type == "telegram":
            result = self.telegram.send(chat_id=str(body["chat_id"]), body=str(body["body"]))
            METRICS.increment("telegram_messages_total")
        elif channel_type == "push":
            result = self.push.send(title=str(body.get("title") or ""), body=str(body["body"]))
            METRICS.increment("push_notifications_total")
        else:
            message = self.repository.create_communication_message(
                channel_type=channel_type,
                body=str(body["body"]),
                subject=str(body.get("subject") or ""),
                status="queued",
            )
            self.queue.enqueue(channel_type=channel_type, payload={"message_id": message.get("id")})
            result = message
        METRICS.increment("communication_messages_total")
        return {"delivery": result, "channel_type": channel_type}

    # --- Channels ---

    def list_channels(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("communication_channel_list")
        return {"channels": [cdto.channel_dto(r) for r in self.repository.list_communication_channels()]}

    # --- Notifications ---

    def list_notifications(self, *, actor: dict[str, object], user_id: int | None = None) -> dict[str, object]:
        self._require_auth(actor)
        uid = user_id if user_id is not None else (int(actor["id"]) if actor.get("id") is not None else None)
        METRICS.increment("communication_notifications_total")
        METRICS.increment("notification_list")
        rows = self.notifications.list_events(user_id=uid)
        return {"notifications": [cdto.notification_event_dto(r) for r in rows]}

    def create_notification(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        notification = self.notifications.create(
            notification_type=str(body.get("notification_type") or "user"),
            title=str(body["title"]),
            body=str(body.get("body") or ""),
            user_id=int(body["user_id"]) if body.get("user_id") is not None else None,
            contact_id=int(body["contact_id"]) if body.get("contact_id") is not None else None,
            priority=str(body.get("priority") or "normal"),
            payload=dict(body.get("payload") or {}),
        )
        METRICS.increment("communication_notifications_total")
        METRICS.increment("notification_created")
        return {"notification": cdto.notification_event_dto(notification)}

    # --- Templates ---

    def list_templates(self, *, actor: dict[str, object], channel_type: str | None = None) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("template_list")
        rows = self.templates.list_templates(channel_type=channel_type)
        return {"templates": [cdto.template_dto(r) for r in rows]}

    def create_template(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        template = self.templates.create(
            name=str(body["name"]),
            channel_type=str(body.get("channel_type") or "in_app"),
            subject=str(body.get("subject") or ""),
            body=str(body.get("body") or ""),
        )
        METRICS.increment("template_usage_total")
        METRICS.increment("template_created")
        return {"template": cdto.template_dto(template)}

    def render_template(self, *, actor: dict[str, object], template_id: int, body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        rendered = self.templates.render(template_id=template_id, variables=dict(body.get("variables") or {}))
        METRICS.increment("template_usage_total")
        return {"rendered": rendered}

    # --- Campaigns ---

    def list_campaigns(self, *, actor: dict[str, object], status: str | None = None) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("communication_campaigns_total")
        METRICS.increment("campaign_list")
        rows = self.campaigns.list_campaigns(status=status)
        return {"campaigns": [cdto.campaign_dto(r) for r in rows]}

    def create_campaign(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        campaign = self.campaigns.create(
            name=str(body["name"]),
            campaign_type=str(body.get("campaign_type") or "multichannel"),
            organization_id=int(body["organization_id"]) if body.get("organization_id") is not None else None,
            scheduled_at=str(body["scheduled_at"]) if body.get("scheduled_at") else None,
        )
        METRICS.increment("communication_campaigns_total")
        METRICS.increment("campaign_created")
        return {"campaign": cdto.campaign_dto(campaign)}

    def execute_campaign(self, *, actor: dict[str, object], campaign_id: int) -> dict[str, object]:
        self._require_admin(actor)
        execution = self.campaigns.execute(campaign_id)
        METRICS.increment("campaign_success_total")
        return {"execution": execution}

    # --- Queue ---

    def list_queue_jobs(self, *, actor: dict[str, object], job_status: str | None = None) -> dict[str, object]:
        self._require_admin(actor)
        METRICS.increment("communication_queue_jobs_total")
        METRICS.increment("queue_job_list")
        rows = self.queue.list_jobs(job_status=job_status)
        return {"jobs": [cdto.queue_job_dto(r) for r in rows]}

    def enqueue_job(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        job = self.queue.enqueue(
            job_type=str(body.get("job_type") or "send_message"),
            channel_type=str(body.get("channel_type") or "email"),
            priority=str(body.get("priority") or "normal"),
            payload=dict(body.get("payload") or {}),
            scheduled_at=str(body["scheduled_at"]) if body.get("scheduled_at") else None,
        )
        METRICS.increment("communication_queue_jobs_total")
        METRICS.increment("queue_job_enqueued")
        return {"job": cdto.queue_job_dto(job)}

    def retry_queue_job(self, *, actor: dict[str, object], job_id: int) -> dict[str, object]:
        self._require_admin(actor)
        job = self.queue.retry(job_id)
        METRICS.increment("communication_retry_total")
        METRICS.increment("queue_job_retried")
        return {"job": cdto.queue_job_dto(job)}

    # --- Preferences ---

    def get_preferences(
        self,
        *,
        actor: dict[str, object],
        channel_type: str = "email",
    ) -> dict[str, object]:
        self._require_auth(actor)
        user_id = int(actor["id"]) if actor.get("id") is not None else None
        pref = self.preferences.get(user_id=user_id, channel_type=channel_type)
        METRICS.increment("communication_preference_get")
        return {"preference": cdto.preference_dto(pref) if pref else None}

    def update_preferences(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        user_id = int(actor["id"]) if actor.get("id") is not None else None
        pref = self.preferences.upsert(
            user_id=user_id,
            channel_type=str(body.get("channel_type") or "email"),
            enabled=bool(body.get("enabled", True)),
            settings=dict(body.get("settings") or {}),
        )
        METRICS.increment("communication_preference_updated")
        return {"preference": cdto.preference_dto(pref)}

    # --- Conversations ---

    def list_conversations(self, *, actor: dict[str, object], limit: int = 50) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("communication_conversation_list")
        rows = self.conversations.list_threads(limit=limit)
        return {"threads": [cdto.thread_dto(r) for r in rows]}

    def create_conversation(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        thread = self.conversations.create_thread(
            subject=str(body.get("subject") or ""),
            channel_id=int(body["channel_id"]) if body.get("channel_id") is not None else None,
            organization_id=int(body["organization_id"]) if body.get("organization_id") is not None else None,
        )
        METRICS.increment("communication_conversation_created")
        return {"thread": cdto.thread_dto(thread)}

    # --- Analytics ---

    def analytics(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("communication_analytics")
        return cdto.analytics_dto(self.analytics_service.analytics())

    def dashboard(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("communication_dashboard")
        return cdto.dashboard_dto(self.analytics_service.dashboard())

    def stats(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("communication_stats")
        return cdto.stats_dto(self.analytics_service.stats())

    def ai_recommendations(
        self,
        *,
        actor: dict[str, object],
        contact_id: int | None = None,
    ) -> dict[str, object]:
        self._require_auth(actor)
        user_id = int(actor["id"]) if actor.get("id") is not None else None
        rows = self.analytics_service.ai_recommendations(user_id=user_id, contact_id=contact_id)
        METRICS.increment("communication_ai_recommendations_total")
        return {"recommendations": [cdto.ai_recommendation_dto(r) for r in rows]}

    # --- Integrations ---

    def integration_sources(self, *, actor: dict[str, object] | None = None) -> dict[str, object]:
        if actor is not None:
            self._require_auth(actor)
        return {
            "sources": self.engine.integration_sources(),
            "integrations": self.integrations.sources(),
        }

    def process_event(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        result = self.integrations.process_event(
            event_kind=str(body["event_kind"]),
            source_program=str(body.get("source_program") or "platform"),
            payload=dict(body.get("payload") or {}),
        )
        METRICS.increment("communication_event_processed")
        return {"result": result}

    def _normalize_whatsapp_number(self, value: str) -> str:
        raw = re.sub(r"[^0-9+]", "", value or "")
        if not raw:
            return ""
        try:
            return normalize_mobile_money_number(raw)
        except Exception:
            digits = re.sub(r"\D", "", raw)
            if len(digits) == 12 and digits.startswith("237"):
                return f"+{digits}"
            if len(digits) == 9 and digits.startswith("6"):
                return f"+237{digits}"
            if digits:
                return f"+{digits}"
            return ""

    def _generate_ai_reply(self, raw_text: str, channel: str, conversation_key: str) -> str:
        if not raw_text.strip():
            return ""
        if self.ai is None:
            self.repository.create_communication_log(
                level="warning",
                message="AI orchestrator not available for channel reply",
                payload={"channel": channel},
            )
            return "Merci pour votre message. L'équipe LAWIM vous répondra prochainement."
        try:
            request = self.ai.build_request(
                channel=channel,
                text=raw_text,
                conversation_key=conversation_key,
                language="fr",
            )
            outcome = self.ai.generate(request)
            response_text = outcome.response.content.strip() if outcome.response and outcome.response.content else ""
            if not response_text:
                return "Merci pour votre message. L'équipe LAWIM vous répondra prochainement."
            if outcome.response.provider == "internal":
                response_text += "\n\n_Réponse préparée par le moteire interne LAWIM._"
            disclaimer_text = ""
            if self.disclaimer:
                disclaimer_text = self.disclaimer.get_text(language="fr")
            if disclaimer_text:
                response_text += f"\n\n{disclaimer_text}"
            self.repository.create_communication_log(
                level="info",
                message="AI reply generated for channel",
                payload={"channel": channel, "provider": outcome.response.provider, "language": "fr"},
            )
            return response_text
        except Exception as exc:
            self.repository.create_communication_log(
                level="error",
                message="AI reply generation failed",
                payload={"channel": channel, "error": str(exc)},
            )
            return "Merci pour votre message. L'équipe LAWIM vous répondra prochainement."

    def _dispatch_maintenance_reply(
        self,
        *,
        channel: str,
        normalized: dict[str, object],
        message_row: dict[str, object],
    ) -> dict[str, object] | None:
        raw_message = str(message_row.get("body") or normalized.get("message_body") or "")
        handover_requested = any(
            marker in raw_message.lower()
            for marker in ("parler à une personne", "parler a une personne", "humain", "conseiller", "équipe", "equipe")
        )
        maintenance = self.maintenance.submit_message(
            MaintenanceSubmission(
                channel=channel,
                raw_message=raw_message,
                delivery_metadata={
                    "source_message_id": message_row.get("id"),
                    "message_key": message_row.get("message_key"),
                    "external_chat_id": normalized.get("chat_id") or normalized.get("sender"),
                    "external_user_id": normalized.get("user_id"),
                },
                handover_requested=handover_requested,
            )
        )
        response_text = MAINTENANCE_RESPONSE
        chat_id_value = normalized.get("chat_id_raw")
        recipient_masked = mask_delivery_recipient(
            str(normalized.get("chat_id") or normalized.get("sender") or normalized.get("user_id") or "")
        )
        self.repository.create_communication_log(
            level="info",
            message=f"Maintenance reply delivery started on {channel}",
            payload={
                "channel": channel,
                "maintenance_message_id": maintenance["message"]["id"],
                "message_id": int(message_row["id"]),
                "recipient": recipient_masked,
                "telegram_chat_id": normalized.get("chat_id_raw") if channel == "telegram" else None,
                "telegram_username": normalized.get("username") if channel == "telegram" else None,
                "response_length": len(response_text),
            },
        )
        if channel == "whatsapp":
            normalized_number = self._normalize_whatsapp_number(str(normalized.get("chat_id") or normalized.get("sender") or ""))
            if not normalized_number:
                return {"status": "skipped", "reason": "missing_recipient"}
            try:
                delivery = self.repository.send_whatsapp(
                    to_number=normalized_number,
                    body=response_text,
                    thread_id=None,
                    contact_id=None,
                    external_chat_id=str(normalized.get("chat_id") or normalized.get("sender") or ""),
                    external_user_id=str(normalized.get("user_id") or ""),
                    provider_message_id=None,
                    metadata={
                        "maintenance_mode": True,
                        "maintenance_message_id": maintenance["message"]["id"],
                    },
                )
            except Exception as exc:
                self.repository.create_communication_log(
                    level="error",
                    message=f"Maintenance reply delivery raised on {channel}",
                    payload={
                        "channel": channel,
                        "message_id": int(message_row["id"]),
                        "recipient": recipient_masked,
                        "response_length": len(response_text),
                        "error_type": exc.__class__.__name__,
                        "error_message": str(exc),
                    },
                )
                return {"status": "failed", "maintenance": maintenance, "error_type": exc.__class__.__name__}
        else:
            chat_id_value = normalized.get("chat_id_raw")
            chat_id = str(chat_id_value or normalized.get("chat_id") or "")
            if not chat_id:
                return {"status": "skipped", "reason": "missing_chat_id"}
            try:
                delivery = self.repository.send_telegram(
                    chat_id=chat_id_value if chat_id_value is not None else chat_id,
                    body=response_text,
                    thread_id=None,
                    contact_id=None,
                    external_chat_id=chat_id,
                    external_user_id=str(normalized.get("user_id") or ""),
                    provider_message_id=None,
                    metadata={
                        "maintenance_mode": True,
                        "maintenance_message_id": maintenance["message"]["id"],
                    },
                )
            except Exception as exc:
                self.repository.create_communication_log(
                    level="error",
                    message=f"Maintenance reply delivery raised on {channel}",
                    payload={
                        "channel": channel,
                        "message_id": int(message_row["id"]),
                        "recipient": recipient_masked,
                        "telegram_chat_id": chat_id_value,
                        "telegram_username": normalized.get("username"),
                        "response_length": len(response_text),
                        "error_type": exc.__class__.__name__,
                        "error_message": str(exc),
                    },
                )
                return {"status": "failed", "maintenance": maintenance, "error_type": exc.__class__.__name__}
        delivery_status = str(delivery.get("delivery_status") or (delivery.get("delivery") or {}).get("delivery_status") or "failed")
        delivery_payload = delivery.get("delivery") if isinstance(delivery, dict) else {}
        self.repository.create_communication_log(
            level="info" if delivery_status == "sent" else "warning",
            message=f"Maintenance reply delivery finished on {channel}",
            payload={
                "channel": channel,
                "maintenance_message_id": maintenance["message"]["id"],
                "message_id": int(message_row["id"]),
                "recipient": recipient_masked,
                "telegram_chat_id": chat_id_value if channel == "telegram" else None,
                "telegram_username": normalized.get("username") if channel == "telegram" else None,
                "response_length": len(response_text),
                "delivery_status": delivery_status,
                "http_status": delivery_payload.get("http_status") if isinstance(delivery_payload, dict) else None,
                "provider_message_id": delivery_payload.get("provider_message_id") if isinstance(delivery_payload, dict) else None,
                "resolved_ipv4": delivery_payload.get("resolved_ipv4") if isinstance(delivery_payload, dict) else None,
                "sanitized_url": delivery_payload.get("sanitized_url") if isinstance(delivery_payload, dict) else None,
                "error_type": delivery_payload.get("error_type") if isinstance(delivery_payload, dict) else None,
                "response_text": delivery_payload.get("response_text") if isinstance(delivery_payload, dict) else None,
                "ok": delivery_payload.get("ok") if isinstance(delivery_payload, dict) else None,
                "description": (
                    (delivery_payload.get("response_json") or {}).get("description")
                    if isinstance(delivery_payload, dict)
                    else None
                ),
            },
        )
        self.repository.create_communication_log(
            level="info" if delivery_status == "sent" else "warning",
            message=f"Maintenance reply {delivery_status} on {channel}",
            payload={
                "channel": channel,
                "maintenance_message_id": maintenance["message"]["id"],
                "delivery_id": delivery.get("id") if isinstance(delivery, dict) else None,
            },
        )
        return {
            "status": delivery_status,
            "maintenance": maintenance,
            "delivery_status": delivery_status,
            "provider_message_id": delivery_payload.get("provider_message_id") if isinstance(delivery_payload, dict) else None,
        }

    def process_green_api_webhook(
        self,
        *,
        payload: dict[str, object],
        headers: dict[str, str],
    ) -> dict[str, object]:
        normalized = normalize_webhook_payload(payload)
        type_webhook = str(normalized.get("type_webhook") or "unknown")
        event_key = build_event_key(normalized)
        message_key = build_message_key(normalized) if type_webhook in GREEN_API_MESSAGE_WEBHOOKS else None
        duplicate = self.repository.one("SELECT 1 FROM communication_events WHERE event_key = ?", (event_key,)) is not None
        safe_headers = redact_headers(headers)

        if type_webhook not in GREEN_API_SUPPORTED_WEBHOOKS:
            self.repository.create_communication_log(
                level="warning",
                message=f"Ignored unsupported Green API webhook: {type_webhook}",
                payload={
                    "webhook": summarize_for_log(normalized, duplicate=False, event_key=event_key, message_key=message_key),
                    "headers": safe_headers,
                },
            )
            METRICS.increment("communication_green_api_webhook_ignored_total")
            return {"status": "ignored", "accepted": True, "typeWebhook": type_webhook, "duplicate": False}

        message_row: dict[str, object] | None = None
        desired_status = ""
        if type_webhook == "incomingMessageReceived":
            desired_status = "delivered"
            message_row = self._upsert_green_api_message(
                normalized=normalized,
                message_key=message_key,
                direction="inbound",
                desired_status=desired_status,
            )
        elif type_webhook == "outgoingAPIMessageReceived":
            desired_status = "sent"
            message_row = self._upsert_green_api_message(
                normalized=normalized,
                message_key=message_key,
                direction="outbound",
                desired_status=desired_status,
            )
        elif type_webhook == "outgoingMessageStatus":
            desired_status = map_message_status(str(normalized.get("status") or ""))
            message_row = self._upsert_green_api_message(
                normalized=normalized,
                message_key=message_key,
                direction="outbound",
                desired_status=desired_status,
                allow_empty_body=True,
            )
        event_row = self.repository.create_communication_event(
            event_kind=type_webhook,
            source_program="green_api",
            payload=dict(normalized.get("raw_payload") or {}),
            event_key=event_key,
            message_id=int(message_row["id"]) if message_row else None,
            metadata={
                "webhook": summarize_for_log(normalized, duplicate=duplicate, event_key=event_key, message_key=message_key),
                "headers": safe_headers,
            },
        )
        log_message = (
            f"Green API webhook processed: {type_webhook}"
            if not duplicate
            else f"Green API webhook duplicate ignored: {type_webhook}"
        )
        self.repository.create_communication_log(
            level="info" if not duplicate else "debug",
            message=log_message,
            payload={
                "webhook": summarize_for_log(normalized, duplicate=duplicate, event_key=event_key, message_key=message_key),
                "event_id": int(event_row["id"]),
                "message_id": int(message_row["id"]) if message_row else None,
            },
        )
        METRICS.increment(
            "communication_green_api_webhook_duplicate_total" if duplicate else "communication_green_api_webhook_received_total"
        )
        maintenance_reply = None
        if not duplicate and type_webhook == "incomingMessageReceived" and message_row is not None:
            if MAINTENANCE_FLAGS.get("lawim_core_rebuild_maintenance_mode", False):
                maintenance_reply = self._dispatch_maintenance_reply(channel="whatsapp", normalized=normalized, message_row=message_row)
            else:
                reply_text = self._generate_ai_reply(
                    raw_text=str(normalized.get("message_body") or normalized.get("text") or ""),
                    channel="whatsapp",
                    conversation_key=str(message_row.get("id") or ""),
                )
                sender_chat_id = str(normalized.get("chat_id") or normalized.get("sender") or "")
                normalized_number = self._normalize_whatsapp_number(sender_chat_id)
                if normalized_number and reply_text:
                    try:
                        delivery = self.repository.send_whatsapp(
                            to_number=normalized_number,
                            body=reply_text,
                        )
                        self.repository.create_communication_log(
                            level="info",
                            message="WhatsApp contextual reply sent",
                            payload={"event_id": int(event_row["id"]), "message_id": int(message_row["id"]), "to": mask_delivery_recipient(normalized_number)},
                        )
                    except Exception as exc:
                        self.repository.create_communication_log(
                            level="error",
                            message="WhatsApp contextual reply failed",
                            payload={"event_id": int(event_row["id"]), "message_id": int(message_row["id"]), "error": str(exc)},
                        )
                elif not normalized_number:
                    self.repository.create_communication_log(
                        level="debug",
                        message="WhatsApp inbound message received (maintenance mode inactive, no reply sent - missing recipient)",
                        payload={"event_id": int(event_row["id"]), "message_id": int(message_row["id"])},
                    )
        return {
            "status": "ok",
            "accepted": True,
            "duplicate": duplicate,
            "typeWebhook": type_webhook,
            "event_id": int(event_row["id"]),
            "message_id": int(message_row["id"]) if message_row else None,
            "maintenance_reply": maintenance_reply,
        }

    def process_telegram_webhook(
        self,
        *,
        payload: dict[str, object],
        headers: dict[str, str],
    ) -> dict[str, object]:
        normalized = normalize_telegram_webhook_payload(payload)
        update_type = str(normalized.get("update_type") or "unknown")
        update_key = build_telegram_event_key(normalized)
        message_key = build_telegram_message_key(normalized) if update_type in TELEGRAM_MESSAGE_UPDATE_TYPES else None
        duplicate = self.repository.one("SELECT 1 FROM telegram_updates WHERE update_key = ?", (update_key,)) is not None
        safe_headers = redact_telegram_headers(headers)

        if update_type not in TELEGRAM_SUPPORTED_UPDATE_TYPES:
            self.repository.create_communication_log(
                level="warning",
                message=f"Ignored unsupported Telegram update: {update_type}",
                payload={
                    "webhook": summarize_telegram_for_log(
                        normalized,
                        duplicate=False,
                        event_key=update_key,
                        message_key=message_key,
                    ),
                    "headers": safe_headers,
                },
            )
            METRICS.increment("communication_telegram_webhook_ignored_total")
            return {"status": "ignored", "accepted": True, "update_type": update_type, "duplicate": False}

        self.repository.create_telegram_update(
            update_key=update_key,
            update_type=update_type,
            payload=dict(normalized.get("raw_payload") or {}),
            metadata={
                "webhook": summarize_telegram_for_log(
                    normalized,
                    duplicate=duplicate,
                    event_key=update_key,
                    message_key=message_key,
                ),
                "headers": safe_headers,
            },
        )

        message_row: dict[str, object] | None = None
        if update_type in TELEGRAM_MESSAGE_UPDATE_TYPES:
            message_row = self._upsert_telegram_message(
                normalized=normalized,
                message_key=message_key,
                desired_status="delivered",
            )
        elif update_type in {"my_chat_member", "chat_member"}:
            self.repository.create_communication_log(
                level="info",
                message=f"Telegram state update received: {update_type}",
                payload={
                    "webhook": summarize_telegram_for_log(
                        normalized,
                        duplicate=duplicate,
                        event_key=update_key,
                        message_key=message_key,
                    ),
                    "headers": safe_headers,
                },
            )

        event_kind = {
            "callback_query": "TelegramCallbackQuery",
            "my_chat_member": "TelegramStateChanged",
            "chat_member": "TelegramStateChanged",
        }.get(update_type, "TelegramMessageReceived")
        event_row = self.repository.create_communication_event(
            event_kind=event_kind,
            source_program="telegram",
            payload=dict(normalized.get("raw_payload") or {}),
            event_key=update_key,
            message_id=int(message_row["id"]) if message_row else None,
            metadata={
                "webhook": summarize_telegram_for_log(
                    normalized,
                    duplicate=duplicate,
                    event_key=update_key,
                    message_key=message_key,
                ),
                "headers": safe_headers,
            },
        )
        log_message = (
            f"Telegram webhook processed: {update_type}"
            if not duplicate
            else f"Telegram webhook duplicate ignored: {update_type}"
        )
        self.repository.create_communication_log(
            level="info" if not duplicate else "debug",
            message=log_message,
            payload={
                "webhook": summarize_telegram_for_log(
                    normalized,
                    duplicate=duplicate,
                    event_key=update_key,
                    message_key=message_key,
                ),
                "event_id": int(event_row["id"]),
                "update_id": normalized.get("update_id"),
                "message_id": int(message_row["id"]) if message_row else None,
            },
        )
        METRICS.increment(
            "communication_telegram_webhook_duplicate_total"
            if duplicate
            else "communication_telegram_webhook_received_total"
        )
        maintenance_reply = None
        if not duplicate and update_type in {"message", "business_message", "guest_message"} and message_row is not None:
            if MAINTENANCE_FLAGS.get("lawim_core_rebuild_maintenance_mode", False):
                maintenance_reply = self._dispatch_maintenance_reply(channel="telegram", normalized=normalized, message_row=message_row)
            else:
                reply_text = self._generate_ai_reply(
                    raw_text=str(normalized.get("text") or normalized.get("message_body") or ""),
                    channel="telegram",
                    conversation_key=str(message_row.get("id") or ""),
                )
                chat_id = normalized.get("chat_id_raw")
                if chat_id is not None and reply_text:
                    try:
                        delivery = self.repository.send_telegram(
                            chat_id=chat_id,
                            body=reply_text,
                        )
                        self.repository.create_communication_log(
                            level="info",
                            message="Telegram contextual reply sent",
                            payload={"event_id": int(event_row["id"]), "message_id": int(message_row["id"]), "chat_id_present": True},
                        )
                    except Exception as exc:
                        self.repository.create_communication_log(
                            level="error",
                            message="Telegram contextual reply failed",
                            payload={"event_id": int(event_row["id"]), "message_id": int(message_row["id"]), "error": str(exc)},
                        )
                else:
                    self.repository.create_communication_log(
                        level="debug",
                        message="Telegram inbound message received (maintenance mode inactive, no reply sent - missing chat_id or empty response)",
                        payload={"event_id": int(event_row["id"]), "message_id": int(message_row["id"])},
                    )
        return {
            "status": "ok",
            "accepted": True,
            "duplicate": duplicate,
            "update_type": update_type,
            "event_id": int(event_row["id"]),
            "update_id": normalized.get("update_id"),
            "message_id": int(message_row["id"]) if message_row else None,
            "maintenance_reply": maintenance_reply,
        }

    def _upsert_green_api_message(
        self,
        *,
        normalized: dict[str, object],
        message_key: str | None,
        direction: str,
        desired_status: str,
        allow_empty_body: bool = False,
    ) -> dict[str, object]:
        body = str(normalized.get("message_body") or "")
        subject = str(normalized.get("sender_name") or normalized.get("chat_id") or "Green API WhatsApp")
        payload = dict(normalized.get("raw_payload") or {})
        message = self.repository.create_communication_message(
            channel_type="whatsapp",
            body=body,
            subject=subject,
            direction=direction,
            status=desired_status,
            message_key=message_key,
            payload=payload,
        )
        current_status = str(message.get("status") or "")
        current_body = str(message.get("body") or "")
        updates: dict[str, object] = {}
        if body and body != current_body:
            updates["body"] = body
            updates["payload"] = payload
        if not allow_empty_body and not body and current_body:
            updates["body"] = current_body
        if desired_status and current_status != desired_status:
            if self._can_promote_green_api_status(current_status, desired_status):
                updates["status"] = desired_status
        if updates:
            message = self.repository.update_communication_message(int(message["id"]), **updates)
        return message

    def _upsert_telegram_message(
        self,
        *,
        normalized: dict[str, object],
        message_key: str | None,
        desired_status: str,
        allow_empty_body: bool = False,
    ) -> dict[str, object]:
        body = str(normalized.get("message_body") or "")
        if not body:
            body = str(normalized.get("callback_data") or "")
        subject = str(normalized.get("full_name") or normalized.get("username") or normalized.get("chat_id") or "Telegram Update")
        payload = dict(normalized.get("raw_payload") or {})
        message = self.repository.create_communication_message(
            channel_type="telegram",
            body=body,
            subject=subject,
            direction="inbound",
            status=desired_status,
            message_key=message_key,
            payload=payload,
        )
        current_status = str(message.get("status") or "")
        current_body = str(message.get("body") or "")
        updates: dict[str, object] = {}
        if body and body != current_body:
            updates["body"] = body
            updates["payload"] = payload
        if not allow_empty_body and not body and current_body:
            updates["body"] = current_body
        if desired_status and current_status != desired_status:
            if self._can_promote_green_api_status(current_status, desired_status):
                updates["status"] = desired_status
        if updates:
            message = self.repository.update_communication_message(int(message["id"]), **updates)
        return message

    @staticmethod
    def _can_promote_green_api_status(current_status: str, desired_status: str) -> bool:
        order = {
            "draft": 0,
            "queued": 1,
            "sending": 2,
            "sent": 3,
            "delivered": 4,
            "failed": 5,
            "cancelled": 5,
            "expired": 5,
            "archived": 6,
        }
        return order.get(desired_status, 0) >= order.get(current_status, 0)

    def seed_catalog(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        self.repository.seed_communication_catalog()
        METRICS.increment("communication_catalog_seeded")
        return {"seeded": True}

    # --- Channel-specific list endpoints ---

    def list_email_messages(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("email_message_list")
        return {"messages": [cdto.email_message_dto(r) for r in self.email.list_messages()]}

    def list_sms_messages(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("sms_message_list")
        return {"messages": [cdto.sms_message_dto(r) for r in self.sms.list_messages()]}

    def list_whatsapp_messages(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("whatsapp_message_list")
        return {"messages": [cdto.whatsapp_message_dto(r) for r in self.whatsapp.list_messages()]}

    def list_telegram_messages(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("telegram_message_list")
        return {"messages": [cdto.telegram_message_dto(r) for r in self.telegram.list_messages()]}

    def list_push_notifications(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("push_notification_list")
        return {"notifications": [cdto.push_notification_dto(r) for r in self.push.list_notifications()]}

    def health(self, *, actor: dict[str, object] | None = None) -> dict[str, object]:
        if actor is not None:
            self._require_auth(actor)
        tables_ok = self.repository.communication_tables_present()
        pending = 0
        if tables_ok:
            pending = self.repository.scalar("SELECT COUNT(*) FROM queue_jobs WHERE job_status = 'pending'")
        return {
            "status": "ok" if tables_ok else "degraded",
            "tables_present": tables_ok,
            "queue_pending": pending,
        }

    def list_events(self, *, actor: dict[str, object], limit: int = 50) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("communication_event_list")
        rows = self.repository.list_communication_events(limit=limit)
        return {"events": [cdto.event_dto(r) for r in rows]}

    def list_history(self, *, actor: dict[str, object], limit: int = 50) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("communication_history_list")
        rows = self.repository.list_communication_history(limit=limit)
        return {"history": [cdto.history_dto(r) for r in rows]}

    def search(self, *, actor: dict[str, object], query: str, limit: int = 50) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("communication_search")
        rows = self.repository.search_communication_messages(query=query, limit=limit)
        return {"results": [cdto.message_dto(r) for r in rows]}

    def list_groups(self, *, actor: dict[str, object], limit: int = 50) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("communication_group_list")
        rows = self.repository.list_communication_groups(limit=limit)
        return {"groups": [cdto.group_dto(r) for r in rows]}

    def list_inapp(self, *, actor: dict[str, object], user_id: int | None = None) -> dict[str, object]:
        self._require_auth(actor)
        uid = user_id or (int(actor["id"]) if actor.get("id") is not None else None)
        METRICS.increment("inapp_notification_list")
        rows = self.repository.list_inapp_notifications(user_id=uid)
        return {"notifications": [cdto.inapp_notification_dto(r) for r in rows]}

    def export_data(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        METRICS.increment("communication_export")
        return {"export": self.repository.export_communication_snapshot()}

    def import_data(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        METRICS.increment("communication_import")
        return self.repository.import_communication_payload(dict(body.get("payload") or body))

    def reports(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("communication_reports")
        stats = self.analytics_service.stats()
        return {"report": stats, "generated_at": stats.get("generated_at")}
