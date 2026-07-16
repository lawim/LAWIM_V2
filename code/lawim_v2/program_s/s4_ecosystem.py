from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


# ── Tenant ─────────────────────────────────────────────────────────────────


@dataclass
class Tenant:
    tenant_id: str = ""
    code: str = ""
    name: str = ""
    domain: str = ""
    status: str = "ACTIVE"
    created_at: str = ""
    features: dict[str, bool] = field(default_factory=dict)
    branding: dict[str, str] = field(default_factory=dict)

    def can(self, feature: str) -> bool:
        return self.features.get(feature, False)

    def to_dict(self) -> dict[str, Any]:
        return {"tenant_id": self.tenant_id, "code": self.code, "name": self.name,
                "domain": self.domain, "status": self.status}


@dataclass
class TenantMembership:
    membership_id: str = ""
    tenant_id: str = ""
    user_id: int = 0
    role: str = "member"
    joined_at: str = ""


@dataclass
class TenantQuota:
    tenant_id: str = ""
    resource: str = ""
    limit: int = 100
    used: int = 0
    remaining: int = 100


@dataclass
class Partner:
    partner_id: str = ""
    code: str = ""
    name: str = ""
    tier: str = "BRONZE"
    api_key: str = ""
    api_key_prefix: str = ""
    status: str = "ACTIVE"
    quota_daily: int = 1000
    rate_limit: int = 100
    created_at: str = ""


@dataclass
class ApiKey:
    key_id: str = ""
    key_prefix: str = ""
    partner_id: str = ""
    tenant_id: str = ""
    permissions: list[str] = field(default_factory=list)
    active: bool = True
    expires_at: str = ""
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"key_id": self.key_id, "key_prefix": self.key_prefix,
                "active": self.active}


# ── Extension Runtime ─────────────────────────────────────────────────────


@dataclass
class ExtensionInstallation:
    installation_id: str = ""
    extension_code: str = ""
    version: str = "1.0.0"
    tenant_id: str = ""
    status: str = "INSTALLED"
    installed_at: str = ""
    config: dict[str, Any] = field(default_factory=dict)


# ── Connector Runtime ──────────────────────────────────────────────────────


CONNECTOR_TYPES: list[str] = [
    "PAYMENT", "SMS", "EMAIL", "WHATSAPP", "MAPS", "GEOCODING",
    "CALENDAR", "STORAGE", "OCR", "SIGNATURE", "OAUTH", "LDAP",
    "ERP", "CRM", "ACCOUNTING",
]


@dataclass
class ConnectorInstance:
    instance_id: str = ""
    connector_type: str = ""
    provider: str = ""
    tenant_id: str = ""
    config: dict[str, Any] = field(default_factory=dict)
    status: str = "ACTIVE"
    health: str = "UNKNOWN"
    last_check: str = ""


# ── White-label ────────────────────────────────────────────────────────────


@dataclass
class WhiteLabelConfig:
    tenant_id: str = ""
    company_name: str = ""
    logo_url: str = ""
    primary_color: str = "#000000"
    secondary_color: str = "#ffffff"
    custom_domain: str = ""
    support_email: str = ""
    languages: list[str] = field(default_factory=lambda: ["fr", "en"])
    enabled_features: list[str] = field(default_factory=list)
