from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


# ── External Channel Registry ──────────────────────────────────────────────


class ExternalChannelCode(str, Enum):
    FACEBOOK = "FB"
    WHATSAPP = "WA"
    TELEGRAM = "TG"
    INSTAGRAM = "IG"
    TIKTOK = "TK"
    EMAIL = "EM"
    SMS = "SM"
    QR_CODE = "QR"
    PARTNER_SITE = "PS"
    LAWIM_WEB = "LW"
    MOBILE_APP = "MA"
    AGENCY = "AG"
    AGENT = "AT"
    DIRECT = "DR"
    OTHER = "OT"


EXTERNAL_CHANNEL_NAMES: dict[ExternalChannelCode, str] = {
    ExternalChannelCode.FACEBOOK: "Facebook",
    ExternalChannelCode.WHATSAPP: "WhatsApp",
    ExternalChannelCode.TELEGRAM: "Telegram",
    ExternalChannelCode.INSTAGRAM: "Instagram",
    ExternalChannelCode.TIKTOK: "TikTok",
    ExternalChannelCode.EMAIL: "Email",
    ExternalChannelCode.SMS: "SMS",
    ExternalChannelCode.QR_CODE: "QR Code",
    ExternalChannelCode.PARTNER_SITE: "Site partenaire",
    ExternalChannelCode.LAWIM_WEB: "LAWIM Web",
    ExternalChannelCode.MOBILE_APP: "Application mobile",
    ExternalChannelCode.AGENCY: "Agence",
    ExternalChannelCode.AGENT: "Agent",
    ExternalChannelCode.DIRECT: "Direct",
    ExternalChannelCode.OTHER: "Autre",
}

EXTERNAL_CHANNEL_PROVIDERS: dict[ExternalChannelCode, str] = {
    ExternalChannelCode.WHATSAPP: "green_api",
    ExternalChannelCode.TELEGRAM: "telegram",
    ExternalChannelCode.FACEBOOK: "facebook",
}


def channel_code_from_source(channel: str) -> ExternalChannelCode:
    m = {
        "facebook": ExternalChannelCode.FACEBOOK,
        "whatsapp": ExternalChannelCode.WHATSAPP,
        "telegram": ExternalChannelCode.TELEGRAM,
        "instagram": ExternalChannelCode.INSTAGRAM,
        "tiktok": ExternalChannelCode.TIKTOK,
        "email": ExternalChannelCode.EMAIL,
        "sms": ExternalChannelCode.SMS,
        "qr_code": ExternalChannelCode.QR_CODE,
        "partner": ExternalChannelCode.PARTNER_SITE,
        "web": ExternalChannelCode.LAWIM_WEB,
        "mobile": ExternalChannelCode.MOBILE_APP,
        "agency": ExternalChannelCode.AGENCY,
        "agent": ExternalChannelCode.AGENT,
        "direct": ExternalChannelCode.DIRECT,
        "publication": ExternalChannelCode.FACEBOOK,
        "referral": ExternalChannelCode.DIRECT,
    }
    return m.get(channel.lower(), ExternalChannelCode.OTHER)


# ── Campaign Status ────────────────────────────────────────────────────────


class CampaignStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    ARCHIVED = "ARCHIVED"


class PublicationStatus(str, Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    SCHEDULED = "SCHEDULED"
    ARCHIVED = "ARCHIVED"
    FAILED = "FAILED"


# ── External Campaign ──────────────────────────────────────────────────────


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class ExternalCampaign:
    campaign_id: str = ""
    campaign_code: str = ""
    campaign_name: str = ""
    campaign_type: str = ""
    campaign_objective: str = ""
    campaign_owner_actor_id: str = ""
    organization_id: int | None = None
    agency_id: int | None = None
    team_id: int | None = None
    status: CampaignStatus = CampaignStatus.DRAFT
    budget: float | None = None
    currency: str = "XAF"
    start_at: str = ""
    end_at: str = ""
    external_campaign_id: str = ""
    provider: str = ""
    created_at: str = ""
    archived_at: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "campaign_id": self.campaign_id,
            "campaign_code": self.campaign_code,
            "campaign_name": self.campaign_name,
            "campaign_type": self.campaign_type,
            "status": self.status.value,
            "campaign_owner_actor_id": self.campaign_owner_actor_id,
            "organization_id": self.organization_id,
            "start_at": self.start_at,
            "end_at": self.end_at,
        }


# ── External Publication ───────────────────────────────────────────────────


@dataclass
class ExternalPublication:
    publication_id: str = ""
    tracking_code: str = ""
    campaign_id: str = ""
    channel_code: ExternalChannelCode = ExternalChannelCode.OTHER
    provider: str = ""
    external_publication_id: str = ""
    actor_id: str = ""
    actor_role_at_publication: str = ""
    actor_roles_snapshot: list[str] = field(default_factory=list)
    organization_id: int | None = None
    agency_id: int | None = None
    team_id: int | None = None
    title: str = ""
    content_reference: str = ""
    content_hash: str = ""
    language: str = "fr"
    property_id: int | None = None
    service_id: int | None = None
    status: PublicationStatus = PublicationStatus.DRAFT
    published_at: str = ""
    created_at: str = ""
    archived_at: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "publication_id": self.publication_id,
            "tracking_code": self.tracking_code,
            "campaign_id": self.campaign_id,
            "channel_code": self.channel_code.value,
            "actor_id": self.actor_id,
            "actor_role_at_publication": self.actor_role_at_publication,
            "title": self.title,
            "language": self.language,
            "status": self.status.value,
            "published_at": self.published_at,
        }


# ── Tracking Code ──────────────────────────────────────────────────────────


TRACKING_CODE_RE = r"^[A-Z]{2}-LAWIM-\d{6}-\d{4}-\d{2}-\d{3}$"


def parse_tracking_code(code: str) -> dict[str, Any] | None:
    import re
    m = re.match(r"^([A-Z]{2})-LAWIM-(\d{6})-(\d{4})-(\d{2})-(\d{3})$", code)
    if not m:
        return None
    month = int(m.group(4))
    if month < 1 or month > 12:
        return None
    return {
        "channel_code": m.group(1),
        "publication_id": int(m.group(2)),
        "year": int(m.group(3)),
        "month": month,
        "sequence": int(m.group(5)),
    }


def generate_tracking_code(channel_code: str, publication_seq: int, year: int | None = None,
                            month: int | None = None, sequence: int | None = None) -> str:
    now = datetime.now(timezone.utc)
    y = year or now.year
    m = month or now.month
    seq = sequence or 1
    return f"{channel_code}-LAWIM-{publication_seq:06d}-{y:04d}-{m:02d}-{seq:03d}"


# ── Redirect Log ───────────────────────────────────────────────────────────


@dataclass
class RedirectLog:
    redirect_id: str = ""
    tracking_code: str = ""
    occurred_at: str = ""
    session_id: str = ""
    anonymous_subject_id: str = ""
    user_id: int | None = None
    conversation_id: str = ""
    device_category: str = ""
    browser_family: str = ""
    operating_system: str = ""
    country: str = ""
    city: str = ""
    lawim_zone: str = ""
    language: str = ""
    source_url: str = ""
    target_url: str = ""
    target_route: str = ""
    is_bot: bool = False
    is_duplicate: bool = False
    consent_status: str = ""
    correlation_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "redirect_id": self.redirect_id,
            "tracking_code": self.tracking_code,
            "occurred_at": self.occurred_at,
            "session_id": self.session_id,
            "user_id": self.user_id,
            "conversation_id": self.conversation_id,
            "is_bot": self.is_bot,
            "is_duplicate": self.is_duplicate,
            "country": self.country,
        }


# ── Touchpoint ─────────────────────────────────────────────────────────────


class TouchpointType(str, Enum):
    IMPRESSION = "IMPRESSION"
    CLICK = "CLICK"
    QR_SCAN = "QR_SCAN"
    REDIRECT = "REDIRECT"
    CONVERSATION_OPEN = "CONVERSATION_OPEN"
    ACCOUNT_CREATION = "ACCOUNT_CREATION"
    QUALIFICATION = "QUALIFICATION"
    MATCHING = "MATCHING"
    VISIT = "VISIT"
    TRANSACTION = "TRANSACTION"
    PAYMENT = "PAYMENT"
    CONVERSION = "CONVERSION"


@dataclass
class AttributionTouchpoint:
    touchpoint_id: str = ""
    subject_id: str = ""
    user_id: int | None = None
    anonymous_session_id: str = ""
    conversation_id: str = ""
    channel: str = ""
    campaign_id: str = ""
    publication_id: str = ""
    tracking_code: str = ""
    actor_id: str = ""
    actor_role_at_event: str = ""
    touchpoint_type: TouchpointType = TouchpointType.REDIRECT
    touchpoint_value: float = 0.0
    currency: str = "XAF"
    occurred_at: str = ""
    correlation_id: str = ""
    deduplication_key: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "touchpoint_id": self.touchpoint_id,
            "touchpoint_type": self.touchpoint_type.value,
            "channel": self.channel,
            "tracking_code": self.tracking_code,
            "actor_id": self.actor_id,
            "actor_role_at_event": self.actor_role_at_event,
            "occurred_at": self.occurred_at,
        }


# ── Lead Source ────────────────────────────────────────────────────────────


@dataclass
class LeadSource:
    source_id: str = ""
    source_key: str = ""
    reference_code: str = ""
    channel: str = ""
    campaign_id: str = ""
    publication_id: str = ""
    tracking_code: str = ""
    actor_id: str = ""
    first_touch_at: str = ""
    resolution_method: str = ""
    confidence: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "source_key": self.source_key,
            "reference_code": self.reference_code,
            "channel": self.channel,
            "campaign_id": self.campaign_id,
            "tracking_code": self.tracking_code,
            "actor_id": self.actor_id,
            "first_touch_at": self.first_touch_at,
        }


# ── Conversion Event ───────────────────────────────────────────────────────


@dataclass
class ConversionEvent:
    event_id: str = ""
    conversion_type: str = ""
    channel: str = ""
    campaign_id: str = ""
    publication_id: str = ""
    tracking_code: str = ""
    user_id: int | None = None
    actor_id: str = ""
    actor_role_at_conversion: str = ""
    conversation_id: str = ""
    qualification_id: str = ""
    matching_id: str = ""
    visit_id: str = ""
    property_id: int | None = None
    service_id: int | None = None
    transaction_id: str = ""
    payment_id: str = ""
    payment_provider: str = ""
    monetary_value: float = 0.0
    currency: str = "XAF"
    correlation_id: str = ""
    deduplication_key: str = ""
    occurred_at: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "conversion_type": self.conversion_type,
            "channel": self.channel,
            "tracking_code": self.tracking_code,
            "actor_id": self.actor_id,
            "conversation_id": self.conversation_id,
            "transaction_id": self.transaction_id,
            "monetary_value": self.monetary_value,
            "currency": self.currency,
            "occurred_at": self.occurred_at,
        }


# ── Attribution Model ──────────────────────────────────────────────────────


class AttributionModel(str, Enum):
    FIRST_TOUCH = "FIRST_TOUCH"
    LAST_TOUCH = "LAST_TOUCH"
    MULTI_TOUCH = "MULTI_TOUCH"
    LAWIM_ATTRIBUTION = "LAWIM_ATTRIBUTION"


@dataclass
class LeadAttribution:
    attribution_id: str = ""
    lead_id: str = ""
    conversion_event_id: str = ""
    model: AttributionModel = AttributionModel.FIRST_TOUCH
    attribution_window_days: int = 30
    touchpoint_count: int = 0
    weights: dict[str, float] = field(default_factory=dict)
    selected_first_touch: str = ""
    selected_last_touch: str = ""
    calculated_at: str = ""
    calculation_version: str = "1.0"
    deduplication_status: str = ""
    explanation: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "attribution_id": self.attribution_id,
            "model": self.model.value,
            "attribution_window_days": self.attribution_window_days,
            "selected_first_touch": self.selected_first_touch,
            "selected_last_touch": self.selected_last_touch,
            "calculated_at": self.calculated_at,
            "calculation_version": self.calculation_version,
            "explanation": self.explanation,
        }
