from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── Plugin / Extension Framework ──────────────────────────────────────────


class PluginStatus(str, Enum):
    DRAFT = "DRAFT"
    VALIDATED = "VALIDATED"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DISABLED = "DISABLED"
    DEPRECATED = "DEPRECATED"
    UNINSTALLED = "UNINSTALLED"


@dataclass
class PluginDefinition:
    plugin_id: str = ""
    plugin_code: str = ""
    name: str = ""
    description: str = ""
    version: str = "1.0.0"
    min_core_version: str = "2.0.0"
    entry_point: str = ""
    dependencies: list[str] = field(default_factory=list)
    permissions: list[str] = field(default_factory=list)
    status: PluginStatus = PluginStatus.DRAFT
    feature_flag: str = ""
    created_at: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {"plugin_id": self.plugin_id, "plugin_code": self.plugin_code,
                "name": self.name, "version": self.version, "status": self.status.value,
                "feature_flag": self.feature_flag}


class ExtensionStatus(str, Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    VALIDATED = "VALIDATED"
    PUBLISHED = "PUBLISHED"
    DISABLED = "DISABLED"
    DEPRECATED = "DEPRECATED"


class LicenseType(str, Enum):
    MIT = "MIT"
    APACHE_2 = "APACHE_2"
    GPL_3 = "GPL_3"
    PROPRIETARY = "PROPRIETARY"
    FREE = "FREE"


@dataclass
class ExtensionManifest:
    manifest_version: str = "1.0"
    min_core_version: str = "2.0.0"
    max_core_version: str = ""
    compatible_plugins: list[str] = field(default_factory=list)
    checksum: str = ""
    signature: str = ""


@dataclass
class ExtensionDefinition:
    extension_id: str = ""
    extension_code: str = ""
    name: str = ""
    description: str = ""
    version: str = "1.0.0"
    author: str = ""
    license: LicenseType = LicenseType.MIT
    manifest: ExtensionManifest = field(default_factory=ExtensionManifest)
    status: ExtensionStatus = ExtensionStatus.DRAFT
    feature_flag: str = ""
    created_at: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {"extension_id": self.extension_id, "extension_code": self.extension_code,
                "name": self.name, "version": self.version, "status": self.status.value}


# ── Connectors ─────────────────────────────────────────────────────────────


class ConnectorType(str, Enum):
    PAYMENT = "PAYMENT"
    SMS = "SMS"
    EMAIL = "EMAIL"
    WHATSAPP = "WHATSAPP"
    MAPS = "MAPS"
    GEOCODING = "GEOCODING"
    CALENDAR = "CALENDAR"
    STORAGE = "STORAGE"
    OCR = "OCR"
    SIGNATURE = "SIGNATURE"
    OAUTH = "OAUTH"
    LDAP = "LDAP"
    ERP = "ERP"
    CRM = "CRM"
    ACCOUNTING = "ACCOUNTING"


class ConnectorStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    ERROR = "ERROR"
    DEPRECATED = "DEPRECATED"


@dataclass
class ConnectorDefinition:
    connector_id: str = ""
    connector_code: str = ""
    connector_type: ConnectorType = ConnectorType.PAYMENT
    name: str = ""
    provider: str = ""
    version: str = "1.0.0"
    status: ConnectorStatus = ConnectorStatus.DRAFT
    config_schema: dict[str, Any] = field(default_factory=dict)
    feature_flag: str = ""
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"connector_id": self.connector_id, "connector_code": self.connector_code,
                "connector_type": self.connector_type.value, "name": self.name,
                "provider": self.provider, "status": self.status.value}


# ── Marketplace ────────────────────────────────────────────────────────────


class MarketplaceStatus(str, Enum):
    DRAFT = "DRAFT"
    PENDING_REVIEW = "PENDING_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    PUBLISHED = "PUBLISHED"
    UNPUBLISHED = "UNPUBLISHED"
    DEPRECATED = "DEPRECATED"


@dataclass
class MarketplaceListing:
    listing_id: str = ""
    extension_id: str = ""
    name: str = ""
    description: str = ""
    version: str = "1.0.0"
    author: str = ""
    license: LicenseType = LicenseType.MIT
    price: float = 0.0
    currency: str = "XAF"
    categories: list[str] = field(default_factory=list)
    compatibility: list[str] = field(default_factory=list)
    downloads: int = 0
    rating: float = 0.0
    status: MarketplaceStatus = MarketplaceStatus.DRAFT
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"listing_id": self.listing_id, "name": self.name,
                "version": self.version, "status": self.status.value,
                "downloads": self.downloads, "rating": self.rating}


# ── SDK ────────────────────────────────────────────────────────────────────


class SdkLanguage(str, Enum):
    PYTHON = "PYTHON"
    JAVASCRIPT = "JAVASCRIPT"
    PHP = "PHP"
    TYPESCRIPT = "TYPESCRIPT"
    RUBY = "RUBY"
    GO = "GO"
    JAVA = "JAVA"
    DOTNET = "DOTNET"


class SdkStatus(str, Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    DEPRECATED = "DEPRECATED"


@dataclass
class SdkDefinition:
    sdk_id: str = ""
    language: SdkLanguage = SdkLanguage.PYTHON
    version: str = "1.0.0"
    package_name: str = ""
    repository: str = ""
    documentation: str = ""
    status: SdkStatus = SdkStatus.DRAFT
    openapi_spec: str = ""
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"sdk_id": self.sdk_id, "language": self.language.value,
                "version": self.version, "status": self.status.value}


# ── Partner Ecosystem ──────────────────────────────────────────────────────


class PartnerStatus(str, Enum):
    PROSPECT = "PROSPECT"
    ONBOARDING = "ONBOARDING"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    TERMINATED = "TERMINATED"


class PartnerTier(str, Enum):
    BRONZE = "BRONZE"
    SILVER = "SILVER"
    GOLD = "GOLD"
    PLATINUM = "PLATINUM"


@dataclass
class PartnerDefinition:
    partner_id: str = ""
    partner_code: str = ""
    name: str = ""
    partner_type: str = ""
    tier: PartnerTier = PartnerTier.BRONZE
    status: PartnerStatus = PartnerStatus.PROSPECT
    organization_id: int | None = None
    api_key: str = ""
    api_quota: int = 1000
    rate_limit: int = 100
    white_label_enabled: bool = False
    domain: str = ""
    branding: dict[str, Any] = field(default_factory=dict)
    feature_flags: list[str] = field(default_factory=list)
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"partner_id": self.partner_id, "partner_code": self.partner_code,
                "name": self.name, "tier": self.tier.value, "status": self.status.value}
