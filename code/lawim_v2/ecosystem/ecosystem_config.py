from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EcosystemConfig:
    extension_platform_enabled: bool = False
    connector_framework_enabled: bool = False
    marketplace_enabled: bool = False
    public_api_enabled: bool = False
    partner_ecosystem_enabled: bool = False
