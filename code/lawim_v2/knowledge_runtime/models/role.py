"""Role model for the Knowledge Runtime."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Role:
    """A role definition with a dimension classifier."""

    id: str
    name: str
    dimension: str  # e.g. "system_role", "business_role"
    aliases: tuple[str, ...] = ()
    permissions: tuple[str, ...] = ()
    parent_id: str | None = None
    status: str = "ACTIVE"
    sources: tuple[str, ...] = ()
