from __future__ import annotations

from ..contact import TELEGRAM_BOT, WHATSAPP_USERNAME

CHANNEL_TYPES: frozenset[str] = frozenset(
    {"email", "sms", "whatsapp", "telegram", "push", "in_app", "webhook"}
)

MESSAGE_DIRECTIONS: frozenset[str] = frozenset({"inbound", "outbound", "internal"})

MESSAGE_PRIORITIES: frozenset[str] = frozenset({"low", "normal", "high", "urgent", "critical"})

MESSAGE_STATUSES: frozenset[str] = frozenset(
    {"draft", "queued", "sending", "sent", "delivered", "failed", "cancelled", "expired", "archived"}
)

THREAD_STATUSES: frozenset[str] = frozenset({"open", "closed", "archived", "spam"})

NOTIFICATION_TYPES: frozenset[str] = frozenset(
    {
        "user",
        "admin",
        "system",
        "ai",
        "workflow",
        "marketplace",
        "crm",
        "rei",
        "security",
        "maintenance",
        "knowledge",
        "api",
        "webhook",
        "internal",
        "external",
        "critical",
        "urgent",
        "deferred",
        "silent",
    }
)

NOTIFICATION_STATUSES: frozenset[str] = frozenset(
    {"pending", "queued", "delivering", "delivered", "failed", "acknowledged", "cancelled"}
)

DELIVERY_STATUSES: frozenset[str] = frozenset(
    {"pending", "processing", "sent", "delivered", "bounced", "failed", "skipped"}
)

CAMPAIGN_STATUSES: frozenset[str] = frozenset(
    {"draft", "scheduled", "running", "paused", "completed", "cancelled", "archived"}
)

CAMPAIGN_TYPES: frozenset[str] = frozenset(
    {"email", "sms", "whatsapp", "push", "multichannel"}
)

QUEUE_JOB_STATUSES: frozenset[str] = frozenset(
    {"pending", "processing", "completed", "failed", "retrying", "dead_letter", "cancelled"}
)

QUEUE_JOB_TYPES: frozenset[str] = frozenset(
    {"send_message", "send_notification", "run_campaign", "process_batch", "retry_delivery"}
)

WORKER_STATUSES: frozenset[str] = frozenset({"idle", "busy", "offline", "draining"})

TEMPLATE_STATUSES: frozenset[str] = frozenset({"draft", "active", "archived", "deprecated"})

CONSENT_TYPES: frozenset[str] = frozenset(
    {"marketing", "transactional", "analytics", "whatsapp", "sms", "email", "push"}
)

CONSENT_STATUSES: frozenset[str] = frozenset({"pending", "granted", "revoked", "expired"})

SMS_PROVIDERS: frozenset[str] = frozenset(
    {"orange", "mtn", "twilio", "messagebird", "aws_sns", "infobip"}
)

EMAIL_PROVIDERS: frozenset[str] = frozenset({"smtp", "sendgrid", "mailgun", "aws_ses"})

WHATSAPP_PROVIDERS: frozenset[str] = frozenset({"meta_cloud", "green_api"})

PUSH_PLATFORMS: frozenset[str] = frozenset({"android", "ios", "web", "desktop"})

EVENT_KINDS: frozenset[str] = frozenset(
    {
        "CustomerCreated",
        "CustomerUpdated",
        "LeadQualified",
        "WorkflowStarted",
        "WorkflowCompleted",
        "MissionAssigned",
        "MissionCompleted",
        "ContractActivated",
        "MarketplaceRequestCreated",
        "MarketplaceQuoteAccepted",
        "SecurityAlertRaised",
        "SecurityIncident",
        "AuditCompleted",
        "KnowledgeIndexed",
        "MaintenanceMessageReceived",
        "HumanHandoverRequested",
        "PropertyPublished",
        "PropertySold",
        "SubscriptionExpired",
        "InvoiceGenerated",
        "PaymentPrepared",
    }
)

OFFICIAL_WHATSAPP_HANDLE: str = WHATSAPP_USERNAME
OFFICIAL_TELEGRAM_BOT: str = TELEGRAM_BOT

DEFAULT_CHANNELS: tuple[tuple[str, str, str, str], ...] = (
    ("channel-email", "email", "Email LAWIM", "smtp"),
    ("channel-sms", "sms", "SMS LAWIM", "orange"),
    ("channel-whatsapp", "whatsapp", "WhatsApp Business LAWIM", "meta_cloud"),
    ("channel-telegram", "telegram", "Telegram Bot LAWIM", "telegram"),
    ("channel-push", "push", "Push Notifications LAWIM", "web"),
    ("channel-inapp", "in_app", "Notifications In-App LAWIM", "internal"),
    ("channel-webhook", "webhook", "Webhooks LAWIM", "internal"),
)

DEFAULT_NOTIFICATION_RULES: tuple[tuple[str, str, str, str], ...] = (
    ("rule-system-default", "Notification système", "system", "in_app"),
    ("rule-security-alert", "Alerte sécurité", "SecurityAlertRaised", "in_app"),
    ("rule-workflow-complete", "Workflow terminé", "WorkflowCompleted", "in_app"),
    ("rule-crm-lead", "Lead qualifié", "LeadQualified", "email"),
    ("rule-marketplace-request", "Demande marketplace", "MarketplaceRequestCreated", "in_app"),
)

DEFAULT_TEMPLATES: tuple[tuple[str, str, str, str, str], ...] = (
    (
        "tpl-welcome-email",
        "email",
        "Bienvenue LAWIM",
        "Bienvenue sur LAWIM",
        "Bonjour {{name}}, bienvenue sur la plateforme LAWIM.",
    ),
    (
        "tpl-welcome-sms",
        "sms",
        "SMS Bienvenue",
        "",
        "Bienvenue {{name}} sur LAWIM.",
    ),
    (
        "tpl-welcome-whatsapp",
        "whatsapp",
        "WhatsApp Bienvenue",
        "",
        "Bonjour {{name}}, LAWIM vous souhaite la bienvenue.",
    ),
    (
        "tpl-notification-inapp",
        "in_app",
        "Notification générique",
        "{{title}}",
        "{{body}}",
    ),
)

DEFAULT_WHATSAPP_ACCOUNT: tuple[str, str, str] = (
    "whatsapp-lawim-official",
    OFFICIAL_WHATSAPP_HANDLE,
    "+237686822667",
)

DEFAULT_TELEGRAM_BOT: tuple[str, str] = (
    "telegram-lawim-assistant",
    OFFICIAL_TELEGRAM_BOT,
)
