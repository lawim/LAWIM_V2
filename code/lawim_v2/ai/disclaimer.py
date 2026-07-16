from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


DEFAULT_DISCLAIMER_TEXT = (
    "LAWIM AI peut commettre des erreurs. "
    "Vérifiez les informations importantes, notamment les informations juridiques, "
    "financières et contractuelles."
)

DEFAULT_DISCLAIMER_TEXT_EN = (
    "LAWIM AI may make mistakes. "
    "Verify important information, especially legal, financial, "
    "and contractual details."
)


@dataclass(frozen=True, slots=True)
class DisclaimerConfig:
    enabled: bool = True
    text: str = DEFAULT_DISCLAIMER_TEXT
    position: str = "after_response"
    style: str = "subtle"
    channels: tuple[str, ...] = ("web", "whatsapp", "telegram", "admin")
    languages: dict[str, str] = field(default_factory=lambda: {"fr": DEFAULT_DISCLAIMER_TEXT, "en": DEFAULT_DISCLAIMER_TEXT_EN})
    agency_overrides: dict[str, bool] = field(default_factory=dict)
    provider_overrides: dict[str, bool] = field(default_factory=dict)
    globally_disabled: bool = False

    def to_dict(self) -> dict[str, object]:
        return {
            "enabled": self.enabled,
            "text": self.text,
            "position": self.position,
            "style": self.style,
            "channels": list(self.channels),
            "languages": dict(self.languages),
            "agency_overrides": dict(self.agency_overrides),
            "provider_overrides": dict(self.provider_overrides),
            "globally_disabled": self.globally_disabled,
        }


@dataclass(frozen=True, slots=True)
class DisclaimerAuditEntry:
    modified_by: int
    field: str
    old_value: str
    new_value: str
    modified_at: str

    def to_dict(self) -> dict[str, object]:
        return {
            "modified_by": self.modified_by,
            "field": self.field,
            "old_value": self.old_value,
            "new_value": self.new_value,
            "modified_at": self.modified_at,
        }


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class DisclaimerManager:
    def __init__(self, repository, config):
        self.repository = repository
        self.config = config
        self._cached_config: DisclaimerConfig | None = None

    def get_config(self) -> DisclaimerConfig:
        if self._cached_config is not None:
            return self._cached_config
        row = self.repository.get_ai_disclaimer_config()
        if row:
            self._cached_config = DisclaimerConfig(
                enabled=bool(row.get("enabled", True)),
                text=str(row.get("text", DEFAULT_DISCLAIMER_TEXT)),
                position=str(row.get("position", "after_response")),
                style=str(row.get("style", "subtle")),
                channels=tuple(row.get("channels", ["web", "whatsapp", "telegram", "admin"])),
                languages=dict(row.get("languages", {"fr": DEFAULT_DISCLAIMER_TEXT, "en": DEFAULT_DISCLAIMER_TEXT_EN})),
                agency_overrides=dict(row.get("agency_overrides", {})),
                provider_overrides=dict(row.get("provider_overrides", {})),
                globally_disabled=bool(row.get("globally_disabled", False)),
            )
        return self._cached_config or DisclaimerConfig()

    def update_config(self, config: DisclaimerConfig, modified_by: int) -> None:
        old = self.get_config()
        self.repository.upsert_ai_disclaimer_config(
            enabled=config.enabled,
            text=config.text,
            position=config.position,
            style=config.style,
            channels=list(config.channels),
            languages=dict(config.languages),
            agency_overrides=dict(config.agency_overrides),
            provider_overrides=dict(config.provider_overrides),
            globally_disabled=config.globally_disabled,
        )
        self._audit_changes(old, config, modified_by)
        self._cached_config = config

    def should_show(self, *, channel: str, provider: str = "", organization_id: int | None = None) -> bool:
        cfg = self.get_config()
        if cfg.globally_disabled or not cfg.enabled:
            return False
        if channel and channel not in cfg.channels:
            return False
        if provider and provider in cfg.provider_overrides:
            return cfg.provider_overrides[provider]
        if organization_id and organization_id in cfg.agency_overrides:
            return cfg.agency_overrides[organization_id]
        return True

    def get_text(self, language: str = "fr") -> str:
        cfg = self.get_config()
        return cfg.languages.get(language, cfg.text)

    def inject_disclaimer(self, content: str, *, channel: str, provider: str, language: str, organization_id: int | None = None) -> str:
        if not self.should_show(channel=channel, provider=provider, organization_id=organization_id):
            return content
        text = self.get_text(language)
        cfg = self.get_config()
        if cfg.position == "before_response":
            return f"{text}\n\n{content}"
        return f"{content}\n\n_{text}_"

    def invalidate_cache(self) -> None:
        self._cached_config = None

    def _audit_changes(self, old: DisclaimerConfig, new: DisclaimerConfig, modified_by: int) -> None:
        now = _utcnow()
        for field in ["enabled", "text", "position", "style", "globally_disabled"]:
            old_val = str(getattr(old, field, ""))
            new_val = str(getattr(new, field, ""))
            if old_val != new_val:
                self.repository.create_ai_disclaimer_audit(
                    modified_by=modified_by,
                    field=field,
                    old_value=old_val,
                    new_value=new_val,
                    modified_at=now,
                )
