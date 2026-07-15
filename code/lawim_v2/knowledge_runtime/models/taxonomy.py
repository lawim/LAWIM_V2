"""Data models for property and service taxonomies."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class PropertyType:
    """A node in the property taxonomy tree."""

    canonical_id: str
    canonical_name: str
    aliases: tuple[str, ...] = ()
    parent_id: str | None = None
    family: str | None = None
    subtype: str | None = None
    usage_types: tuple[str, ...] = ()
    applicable_transactions: tuple[str, ...] = ()
    qualification_matrix_ids: tuple[str, ...] = ()
    matching_dimensions: tuple[str, ...] = ()
    verification_requirements: tuple[str, ...] = ()
    status: str = "ACTIVE"
    version: str = "1.0"
    sources: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ServiceType:
    """A node in the service taxonomy tree."""

    canonical_id: str
    canonical_name: str
    aliases: tuple[str, ...] = ()
    parent_id: str | None = None
    service_family: str | None = None
    provider_categories: tuple[str, ...] = ()
    requester_categories: tuple[str, ...] = ()
    pricing_model: str | None = None
    geographic_scope: str | None = None
    SLA_reference: str | None = None
    workflow_id: str | None = None
    consent_requirements: tuple[str, ...] = ()
    matching_requirements: tuple[str, ...] = ()
    status: str = "ACTIVE"
    version: str = "1.0"
    sources: tuple[str, ...] = ()
