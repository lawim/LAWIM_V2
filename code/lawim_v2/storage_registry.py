from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence
import re
import unicodedata

from .credential_vault import CredentialReference, CredentialStatus, CredentialVault, build_default_credential_vault
from .google_drive_connector import GoogleDriveConnector, build_default_google_drive_connectors


def _normalize_key(value: str) -> str:
    ascii_value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    ascii_value = ascii_value.lower().replace("&", " and ")
    normalized = re.sub(r"[^a-z0-9]+", " ", ascii_value).strip()
    return re.sub(r"\s+", " ", normalized)


def _gb(value: float) -> float:
    return round(max(value, 0.0), 2)


@dataclass(frozen=True, slots=True)
class StorageUsageThresholds:
    normal_max_percent: int = 70
    attention_max_percent: int = 85
    slowdown_max_percent: int = 92

    def band_for(self, usage_percent: float) -> str:
        if usage_percent > self.slowdown_max_percent:
            return "blocked"
        if usage_percent >= self.attention_max_percent:
            return "slowdown"
        if usage_percent >= self.normal_max_percent:
            return "attention"
        return "normal"

    def as_dict(self) -> dict[str, int]:
        return {
            "normal_max_percent": self.normal_max_percent,
            "attention_max_percent": self.attention_max_percent,
            "slowdown_max_percent": self.slowdown_max_percent,
        }


@dataclass(slots=True)
class StorageResource:
    drive_id: str
    logical_name: str
    role: str
    priority: int
    category: str
    credential_id: str = ""
    resource_type: str = "google-drive-resource"
    quota_gb: float = 13.0
    used_gb: float = 0.0
    provider_type: str = "google-drive"
    status: str = "normal"
    health: str = "healthy"
    last_test: str = "2026-07-05T10:00:00Z"
    last_control: str = "2026-07-05T10:00:00Z"
    last_access: str = "2026-07-05T10:00:00Z"
    last_connection_test: str = "2026-07-05T10:00:00Z"
    last_upload_test: str = "2026-07-05T10:00:00Z"
    last_download_test: str = "2026-07-05T10:00:00Z"
    last_healthcheck: str = "2026-07-05T10:00:00Z"
    api_version: str = "v3"
    routing_strategy: str = "official-priority-route"
    backup_policy: str = "backup-center-activation"
    restore_policy: str = "restore-center-activation"
    credential_status: str = CredentialStatus.PLACEHOLDER_CONFIGURED
    oauth_status: str = CredentialStatus.PLACEHOLDER_CONFIGURED
    test_status: str = "activation-passed"

    @property
    def state(self) -> str:
        return self.status

    @property
    def available_gb(self) -> float:
        return _gb(self.quota_gb - self.used_gb)

    @property
    def usage_percent(self) -> float:
        if self.quota_gb <= 0:
            return 0.0
        return round((self.used_gb / self.quota_gb) * 100, 1)

    def threshold_band(self, thresholds: StorageUsageThresholds | None = None) -> str:
        return (thresholds or StorageUsageThresholds()).band_for(self.usage_percent)

    def is_blocked(self, thresholds: StorageUsageThresholds | None = None) -> bool:
        return self.threshold_band(thresholds) == "blocked"

    def can_store(self, *, size_gb: float = 0.0, thresholds: StorageUsageThresholds | None = None) -> bool:
        return not self.is_blocked(thresholds) and size_gb <= self.available_gb

    def as_dict(self, thresholds: StorageUsageThresholds | None = None) -> dict[str, Any]:
        band = self.threshold_band(thresholds)
        return {
            "drive_id": self.drive_id,
            "logical_name": self.logical_name,
            "role": self.role,
            "priority": self.priority,
            "category": self.category,
            "credential_id": self.credential_id,
            "resource_type": self.resource_type,
            "quota_gb": self.quota_gb,
            "used_gb": self.used_gb,
            "available_gb": self.available_gb,
            "usage_percent": self.usage_percent,
            "provider_type": self.provider_type,
            "status": self.status or band,
            "state": self.state,
            "health": self.health,
            "last_test": self.last_test,
            "last_control": self.last_control,
            "last_access": self.last_access,
            "last_connection_test": self.last_connection_test,
            "last_upload_test": self.last_upload_test,
            "last_download_test": self.last_download_test,
            "last_healthcheck": self.last_healthcheck,
            "api_version": self.api_version,
            "routing_strategy": self.routing_strategy,
            "backup_policy": self.backup_policy,
            "restore_policy": self.restore_policy,
            "credential_status": self.credential_status,
            "oauth_status": self.oauth_status,
            "test_status": self.test_status,
            "threshold_band": band,
        }


@dataclass(slots=True)
class GoogleDriveConfigurationModel:
    drive_id: str
    logical_name: str
    email_placeholder: str
    provider: str = "google-drive"
    category: str = "general"
    credential_id: str = ""
    quota_gb: float = 13.0
    used_gb: float = 0.0
    credential_status: str = CredentialStatus.PLACEHOLDER_CONFIGURED
    oauth_status: str = CredentialStatus.PLACEHOLDER_CONFIGURED
    last_connection_test: str = "2026-07-05T10:00:00Z"
    last_upload_test: str = "2026-07-05T10:00:00Z"
    last_download_test: str = "2026-07-05T10:00:00Z"
    last_healthcheck: str = "2026-07-05T10:00:00Z"
    test_status: str = "activation-passed"

    @property
    def available_gb(self) -> float:
        return _gb(self.quota_gb - self.used_gb)

    def as_dict(self) -> dict[str, Any]:
        return {
            "drive_id": self.drive_id,
            "logical_name": self.logical_name,
            "email_placeholder": self.email_placeholder,
            "provider": self.provider,
            "category": self.category,
            "credential_id": self.credential_id,
            "quota_gb": self.quota_gb,
            "used_gb": self.used_gb,
            "available_gb": self.available_gb,
            "credential_status": self.credential_status,
            "oauth_status": self.oauth_status,
            "last_connection_test": self.last_connection_test,
            "last_upload_test": self.last_upload_test,
            "last_download_test": self.last_download_test,
            "last_healthcheck": self.last_healthcheck,
            "test_status": self.test_status,
        }


def _default_route_map() -> dict[str, tuple[str, ...]]:
    return {
        "video": ("drive-1", "drive-2", "drive-8"),
        "photo": ("drive-3", "drive-8"),
        "audio": ("drive-3", "drive-8"),
        "document": ("drive-4", "drive-8"),
        "conversation archive": ("drive-5", "drive-8"),
        "export rapport": ("drive-6", "drive-8"),
        "backup applicatif": ("drive-7", "drive-10"),
        "replication critique": ("drive-8", "drive-10"),
        "reserve": ("drive-9",),
        "maintenance migration": ("drive-10",),
    }


def _default_aliases() -> dict[str, str]:
    return {
        "image": "photo",
        "images": "photo",
        "photos": "photo",
        "video": "video",
        "videos": "video",
        "audio": "audio",
        "audios": "audio",
        "document": "document",
        "documents": "document",
        "floorplan": "document",
        "thumbnail": "document",
        "conversation": "conversation archive",
        "conversations": "conversation archive",
        "conversation archive": "conversation archive",
        "conversation archives": "conversation archive",
        "archive conversation": "conversation archive",
        "archive conversations": "conversation archive",
        "export": "export rapport",
        "exports": "export rapport",
        "rapport": "export rapport",
        "rapports": "export rapport",
        "report": "export rapport",
        "reports": "export rapport",
        "statistic": "export rapport",
        "statistics": "export rapport",
        "backup": "backup applicatif",
        "backups": "backup applicatif",
        "application backup": "backup applicatif",
        "app backup": "backup applicatif",
        "app backups": "backup applicatif",
        "replication": "replication critique",
        "critical replication": "replication critique",
        "reserve strategy": "reserve",
        "strategic reserve": "reserve",
        "maintenance": "maintenance migration",
        "migration": "maintenance migration",
    }


@dataclass(slots=True)
class StorageRoutingPolicy:
    route_map: dict[str, tuple[str, ...]] = field(default_factory=_default_route_map)
    aliases: dict[str, str] = field(default_factory=_default_aliases)

    def canonicalize(self, category: str) -> str:
        normalized = _normalize_key(category)
        return self.aliases.get(normalized, normalized)

    def route_for(self, category: str) -> tuple[str, ...]:
        canonical = self.canonicalize(category)
        route = self.route_map.get(canonical)
        if route is None:
            raise KeyError(f"unknown storage routing category: {category}")
        return route

    def describe_routes(self) -> list[dict[str, Any]]:
        return [{"category": category, "route": list(route)} for category, route in self.route_map.items()]


_RESOURCE_SPECS: tuple[dict[str, Any], ...] = (
    {
        "drive_id": "drive-1",
        "logical_name": "videos-a",
        "role": "Videos A",
        "priority": 1,
        "category": "video",
        "used_gb": 3.2,
    },
    {
        "drive_id": "drive-2",
        "logical_name": "videos-b",
        "role": "Videos B",
        "priority": 2,
        "category": "video",
        "used_gb": 4.1,
    },
    {
        "drive_id": "drive-3",
        "logical_name": "photos-audio",
        "role": "Photos + Audio",
        "priority": 3,
        "category": "photo/audio",
        "used_gb": 5.8,
    },
    {
        "drive_id": "drive-4",
        "logical_name": "documents",
        "role": "Documents",
        "priority": 4,
        "category": "document",
        "used_gb": 6.4,
    },
    {
        "drive_id": "drive-5",
        "logical_name": "conversation-registry",
        "role": "Conversation Registry",
        "priority": 5,
        "category": "conversation archive",
        "used_gb": 9.4,
    },
    {
        "drive_id": "drive-6",
        "logical_name": "exports-reports-stats",
        "role": "Exports / reports / statistics",
        "priority": 6,
        "category": "export rapport",
        "used_gb": 10.5,
    },
    {
        "drive_id": "drive-7",
        "logical_name": "application-backups",
        "role": "Application backups",
        "priority": 7,
        "category": "backup applicatif",
        "used_gb": 11.9,
    },
    {
        "drive_id": "drive-8",
        "logical_name": "replication-overflow",
        "role": "Replication / overflow",
        "priority": 8,
        "category": "replication critique",
        "used_gb": 12.4,
    },
    {
        "drive_id": "drive-9",
        "logical_name": "strategic-reserve",
        "role": "Strategic reserve",
        "priority": 9,
        "category": "reserve",
        "used_gb": 1.3,
    },
    {
        "drive_id": "drive-10",
        "logical_name": "maintenance-migration",
        "role": "Maintenance / migration",
        "priority": 10,
        "category": "maintenance migration",
        "used_gb": 3.9,
    },
)


def _resource_status_for_band(band: str) -> tuple[str, str]:
    mapping = {
        "normal": ("ready", "healthy"),
        "attention": ("watch", "watch"),
        "slowdown": ("degraded", "degraded"),
        "blocked": ("blocked", "blocked"),
    }
    return mapping[band]


def build_default_storage_resources() -> list[StorageResource]:
    thresholds = StorageUsageThresholds()
    resources: list[StorageResource] = []
    for spec in _RESOURCE_SPECS:
        used_gb = float(spec["used_gb"])
        quota_gb = 13.0
        usage_percent = round((used_gb / quota_gb) * 100, 1)
        band = thresholds.band_for(usage_percent)
        status, health = _resource_status_for_band(band)
        last_check = "2026-07-05T10:00:00Z"
        resources.append(
            StorageResource(
                drive_id=str(spec["drive_id"]),
                logical_name=str(spec["logical_name"]),
                role=str(spec["role"]),
                priority=int(spec["priority"]),
                category=str(spec["category"]),
                credential_id=f"cred-{spec['drive_id']}",
                resource_type="google-drive-resource",
                quota_gb=quota_gb,
                used_gb=used_gb,
                status=status,
                health=health,
                last_test=last_check,
                last_control=last_check,
                last_access=last_check,
                last_connection_test=last_check,
                last_upload_test=last_check,
                last_download_test=last_check,
                last_healthcheck=last_check,
                api_version="v3",
                routing_strategy="official-priority-route",
                backup_policy="backup-center-activation",
                restore_policy="restore-center-activation",
                credential_status="placeholder-configured",
                oauth_status="placeholder-configured",
                test_status="activation-passed" if band != "blocked" else "activation-review",
            )
        )
    return resources


def build_default_google_drive_configurations(
    resources: Sequence[StorageResource] | None = None,
) -> list[GoogleDriveConfigurationModel]:
    resources = list(resources or build_default_storage_resources())
    configurations: list[GoogleDriveConfigurationModel] = []
    for resource in resources:
        configurations.append(
            GoogleDriveConfigurationModel(
                drive_id=resource.drive_id,
                logical_name=resource.logical_name,
                email_placeholder=f"{resource.drive_id}@placeholder.lawim.invalid",
                provider=resource.provider_type,
                category=resource.category,
                credential_id=resource.credential_id,
                quota_gb=resource.quota_gb,
                used_gb=resource.used_gb,
                credential_status=resource.credential_status,
                oauth_status=resource.oauth_status,
                last_connection_test=resource.last_connection_test,
                last_upload_test=resource.last_upload_test,
                last_download_test=resource.last_download_test,
                last_healthcheck=resource.last_healthcheck,
                test_status=resource.test_status,
            )
        )
    return configurations


@dataclass(slots=True)
class StorageResourceRegistry:
    resources: list[StorageResource] = field(default_factory=build_default_storage_resources)
    routing_policy: StorageRoutingPolicy = field(default_factory=StorageRoutingPolicy)
    thresholds: StorageUsageThresholds = field(default_factory=StorageUsageThresholds)
    credential_vault: CredentialVault = field(default_factory=lambda: build_default_credential_vault(_RESOURCE_SPECS))

    def __post_init__(self) -> None:
        resource_ids = {resource.credential_id for resource in self.resources if resource.credential_id}
        vault_ids = {record.credential_id for record in self.credential_vault.list_records()}
        if not resource_ids or resource_ids != vault_ids:
            self.credential_vault = build_default_credential_vault(self.resources)

    @classmethod
    def default(cls) -> "StorageResourceRegistry":
        return cls()

    def get(self, drive_id: str) -> StorageResource:
        for resource in self.resources:
            if resource.drive_id == drive_id:
                return resource
        raise KeyError(f"unknown drive resource: {drive_id}")

    def canonical_category(self, category: str) -> str:
        return self.routing_policy.canonicalize(category)

    def route_for(self, category: str) -> tuple[str, ...]:
        return self.routing_policy.route_for(category)

    def select(
        self,
        *,
        category: str,
        size_gb: float = 0.0,
        routing_policy: StorageRoutingPolicy | None = None,
    ) -> StorageResource:
        policy = routing_policy or self.routing_policy
        route = policy.route_for(category)
        for drive_id in route:
            resource = self.get(drive_id)
            if resource.can_store(size_gb=size_gb, thresholds=self.thresholds):
                return resource
        return self.get(route[-1])

    def list_resources(self) -> list[StorageResource]:
        return list(self.resources)

    def available_resources(self) -> list[StorageResource]:
        return [resource for resource in self.resources if not resource.is_blocked(self.thresholds)]

    def blocked_resources(self) -> list[StorageResource]:
        return [resource for resource in self.resources if resource.is_blocked(self.thresholds)]

    def google_drive_configurations(self) -> list[GoogleDriveConfigurationModel]:
        return build_default_google_drive_configurations(self.resources)

    def google_drive_connectors(self) -> list[GoogleDriveConnector]:
        return build_default_google_drive_connectors(self.resources, vault=self.credential_vault)

    def credential_reference_for(self, drive_id: str) -> CredentialReference:
        resource = self.get(drive_id)
        return self.credential_vault.reference_for(resource.credential_id)

    def credential_vault_snapshot(self) -> dict[str, Any]:
        return self.credential_vault.snapshot()

    def drive_configuration_for(self, drive_id: str) -> GoogleDriveConfigurationModel:
        for configuration in self.google_drive_configurations():
            if configuration.drive_id == drive_id:
                return configuration
        raise KeyError(f"unknown drive configuration: {drive_id}")

    def connector_for(self, drive_id: str) -> GoogleDriveConnector:
        for connector in self.google_drive_connectors():
            if connector.drive_id == drive_id:
                return connector
        raise KeyError(f"unknown google drive connector: {drive_id}")

    def alerts(self) -> list[str]:
        alerts: list[str] = []
        for resource in self.resources:
            band = resource.threshold_band(self.thresholds)
            if band != "normal":
                alerts.append(f"{resource.drive_id} {band} at {resource.usage_percent:.1f}%")
        return alerts

    def summary(self) -> dict[str, Any]:
        total_quota = round(sum(resource.quota_gb for resource in self.resources), 2)
        total_used = round(sum(resource.used_gb for resource in self.resources), 2)
        last_control = max(resource.last_control for resource in self.resources)
        last_access = max(resource.last_access for resource in self.resources)
        return {
            "resource_count": len(self.resources),
            "available_count": len(self.available_resources()),
            "blocked_count": len(self.blocked_resources()),
            "alert_count": len(self.alerts()),
            "total_quota_gb": total_quota,
            "total_used_gb": total_used,
            "remaining_gb": _gb(total_quota - total_used),
            "usage_percent": round((total_used / total_quota) * 100, 1) if total_quota else 0.0,
            "last_test": max(resource.last_test for resource in self.resources),
            "last_control": last_control,
            "last_access": last_access,
        }

    def dashboard_snapshot(self) -> dict[str, Any]:
        return {
            "summary": self.summary(),
            "thresholds": self.thresholds.as_dict(),
            "resources": [resource.as_dict(self.thresholds) for resource in self.resources],
            "available_resources": [resource.drive_id for resource in self.available_resources()],
            "blocked_resources": [resource.drive_id for resource in self.blocked_resources()],
            "alerts": self.alerts(),
            "routes": self.routing_policy.describe_routes(),
        }

    def google_drive_registry_snapshot(self) -> dict[str, Any]:
        configurations = self.google_drive_configurations()
        connectors = self.google_drive_connectors()
        return {
            "summary": self.summary(),
            "drives": [configuration.as_dict() for configuration in configurations],
            "connectors": [connector.activation_snapshot() for connector in connectors],
            "credential_vault": self.credential_vault_snapshot(),
            "available_drives": [configuration.drive_id for configuration in configurations if configuration.available_gb > 0],
            "required_folders": list(GoogleDriveConnector.required_folders()),
        }

    def google_drive_admin_snapshot(self) -> dict[str, Any]:
        connectors = self.google_drive_connectors()
        return {
            "summary": self.summary(),
            "drives": [connector.activation_snapshot() for connector in connectors],
            "available_drives": [connector.drive_id for connector in connectors if connector.threshold_band != "blocked"],
            "blocked_drives": [connector.drive_id for connector in connectors if connector.threshold_band == "blocked"],
            "oauth_ready": [connector.drive_id for connector in connectors if connector.oauth.status == CredentialStatus.PLACEHOLDER_CONFIGURED],
            "credential_vault": self.credential_vault_snapshot(),
            "required_folders": list(GoogleDriveConnector.required_folders()),
            "alerts": self.alerts(),
            "routes": self.routing_policy.describe_routes(),
            "monitoring": self.monitoring_snapshot(),
        }

    def monitoring_snapshot(self) -> dict[str, Any]:
        connectors = self.google_drive_connectors()
        total_quota = round(sum(connector.quota_gb for connector in connectors), 2)
        total_used = round(sum(connector.used_gb for connector in connectors), 2)
        usage_percent = round((total_used / total_quota) * 100, 1) if total_quota else 0.0
        latency_ms = 28 if not self.blocked_resources() else 64
        throughput_mbps = 180 if not self.blocked_resources() else 92
        api_monitor = {
            "apiVersion": "v3",
            "oauthStatus": "placeholder-configured",
            "status": "healthy" if not self.blocked_resources() else "watch",
        }
        return {
            "quota_monitor": {
                "total_quota_gb": total_quota,
                "total_used_gb": total_used,
                "remaining_gb": _gb(total_quota - total_used),
                "usage_percent": usage_percent,
                "band": self.thresholds.band_for(usage_percent),
            },
            "latency_ms": latency_ms,
            "throughput_mbps": throughput_mbps,
            "apiMonitor": {**api_monitor, "connectorCount": len(connectors)},
            "api_monitor": {**api_monitor, "connector_count": len(connectors)},
            "credentialMonitor": self.credential_vault.monitoring_snapshot(),
            "credential_monitor": self.credential_vault.monitoring_snapshot(),
            "alerts": self.alerts(),
            "occupation": {
                "available_resources": len(self.available_resources()),
                "blocked_resources": len(self.blocked_resources()),
            },
            "rotation": {
                "video": list(self.routing_policy.route_for("video")),
                "photo": list(self.routing_policy.route_for("photo")),
                "audio": list(self.routing_policy.route_for("audio")),
                "document": list(self.routing_policy.route_for("document")),
                "conversation": list(self.routing_policy.route_for("conversation archive")),
                "backup": list(self.routing_policy.route_for("backup applicatif")),
                "exports": list(self.routing_policy.route_for("export rapport")),
                "maintenance": list(self.routing_policy.route_for("maintenance migration")),
            },
        }

    def ovh_optimization_profile(self) -> dict[str, Any]:
        return {
            "thumbnail_policy": "keep thumbnails on OVH",
            "original_policy": "cold originals move to Google Drive",
            "conversation_cold_target": "drive-5",
            "backup_applicative_target": "drive-7",
            "overflow_target": "drive-8",
            "reserve_target": "drive-9",
            "maintenance_target": "drive-10",
            "no_google_drive_urls": True,
        }

    def backup_center_configuration(self) -> dict[str, Any]:
        return {
            "backup_center": "activation-ready",
            "local_backup": "enabled",
            "external_disk_backup": "enabled",
            "retention_policy": "placeholder",
            "storage_resource_registry": "connected",
            "storage_orchestrator": "connected",
            "conversation_registry": "connected",
            "media_registry": "connected",
            "restore_center": "connected",
            "credential_vault": "connected",
            "monitoring": self.monitoring_snapshot(),
            "quota_policy": self.thresholds.as_dict(),
        }


@dataclass(slots=True)
class StorageSetupWizard:
    steps: tuple[str, ...] = (
        "Register the credential vault",
        "Declare the 10 Google Drive resources",
        "Bind credential references",
        "Validate OAuth connection",
        "Validate permissions",
        "Create the automatic folders",
        "Run the read test",
        "Run the write test",
        "Run the upload test",
        "Run the download test",
        "Run the final validation",
    )
    required_folders: tuple[str, ...] = GoogleDriveConnector.required_folders()

    def build_activation_plan(self, registry: StorageResourceRegistry | None = None) -> dict[str, Any]:
        registry = registry or StorageResourceRegistry.default()
        return {
            "steps": [{"step": step, "status": "prepared"} for step in self.steps],
            "required_folders": list(self.required_folders),
            "connectors": [connector.activation_snapshot() for connector in registry.google_drive_connectors()],
            "credential_vault": registry.credential_vault_snapshot(),
            "sample_routes": {
                "video": list(registry.routing_policy.route_for("video")),
                "photo": list(registry.routing_policy.route_for("photo")),
                "conversation archive": list(registry.routing_policy.route_for("conversation archive")),
                "backup applicatif": list(registry.routing_policy.route_for("backup applicatif")),
                "maintenance migration": list(registry.routing_policy.route_for("maintenance migration")),
            },
            "no_real_secrets": True,
            "activation_ready": True,
        }

    def run_mock(self, registry: StorageResourceRegistry | None = None) -> dict[str, Any]:
        return self.build_activation_plan(registry)


__all__ = [
    "GoogleDriveConfigurationModel",
    "GoogleDriveConnector",
    "StorageResource",
    "StorageResourceRegistry",
    "StorageRoutingPolicy",
    "StorageSetupWizard",
    "StorageUsageThresholds",
    "build_default_google_drive_configurations",
    "build_default_google_drive_connectors",
    "build_default_storage_resources",
]
