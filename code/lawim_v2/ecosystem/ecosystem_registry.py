from __future__ import annotations

from typing import Any

from .ecosystem_models import (
    ConnectorDefinition,
    ConnectorStatus,
    ExtensionDefinition,
    ExtensionStatus,
    MarketplaceListing,
    MarketplaceStatus,
    PartnerDefinition,
    PartnerStatus,
    PluginDefinition,
    PluginStatus,
    SdkDefinition,
    SdkStatus,
)


class PluginRegistry:
    def __init__(self) -> None:
        self._plugins: dict[str, PluginDefinition] = {}

    def register(self, p: PluginDefinition) -> PluginDefinition:
        self._plugins[p.plugin_code] = p
        return p

    def get(self, code: str) -> PluginDefinition | None:
        return self._plugins.get(code)

    def list(self, status: PluginStatus | None = None) -> list[PluginDefinition]:
        if status is None:
            return list(self._plugins.values())
        return [p for p in self._plugins.values() if p.status == status]

    def count(self) -> int:
        return len(self._plugins)


class ExtensionRegistry:
    def __init__(self) -> None:
        self._extensions: dict[str, ExtensionDefinition] = {}

    def register(self, e: ExtensionDefinition) -> ExtensionDefinition:
        self._extensions[e.extension_code] = e
        return e

    def get(self, code: str) -> ExtensionDefinition | None:
        return self._extensions.get(code)

    def list(self, status: ExtensionStatus | None = None) -> list[ExtensionDefinition]:
        if status is None:
            return list(self._extensions.values())
        return [e for e in self._extensions.values() if e.status == status]

    def count(self) -> int:
        return len(self._extensions)


class ConnectorRegistry:
    def __init__(self) -> None:
        self._connectors: dict[str, ConnectorDefinition] = {}

    def register(self, c: ConnectorDefinition) -> ConnectorDefinition:
        self._connectors[c.connector_code] = c
        return c

    def get(self, code: str) -> ConnectorDefinition | None:
        return self._connectors.get(code)

    def list(self, ctype: Any = None) -> list[ConnectorDefinition]:
        if ctype is None:
            return list(self._connectors.values())
        return [c for c in self._connectors.values() if c.connector_type == ctype]

    def count(self) -> int:
        return len(self._connectors)


class MarketplaceRegistry:
    def __init__(self) -> None:
        self._listings: dict[str, MarketplaceListing] = {}

    def register(self, m: MarketplaceListing) -> MarketplaceListing:
        self._listings[m.listing_id] = m
        return m

    def list(self, status: MarketplaceStatus | None = None) -> list[MarketplaceListing]:
        if status is None:
            return list(self._listings.values())
        return [m for m in self._listings.values() if m.status == status]

    def count(self) -> int:
        return len(self._listings)


class SdkRegistry:
    def __init__(self) -> None:
        self._sdks: dict[str, SdkDefinition] = {}

    def register(self, s: SdkDefinition) -> SdkDefinition:
        self._sdks[f"{s.language.value}_{s.version}"] = s
        return s

    def list(self) -> list[SdkDefinition]:
        return list(self._sdks.values())

    def count(self) -> int:
        return len(self._sdks)


class PartnerRegistry:
    def __init__(self) -> None:
        self._partners: dict[str, PartnerDefinition] = {}

    def register(self, p: PartnerDefinition) -> PartnerDefinition:
        self._partners[p.partner_code] = p
        return p

    def get(self, code: str) -> PartnerDefinition | None:
        return self._partners.get(code)

    def list(self, status: PartnerStatus | None = None) -> list[PartnerDefinition]:
        if status is None:
            return list(self._partners.values())
        return [p for p in self._partners.values() if p.status == status]

    def count(self) -> int:
        return len(self._partners)
