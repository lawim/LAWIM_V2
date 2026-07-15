from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProgramRConfig:
    crm_pipeline_enabled: bool = False
    agency_structure_enabled: bool = False
    service_order_enabled: bool = False
    project_dossier_enabled: bool = False
    relationship_consent_enabled: bool = False
    workflow_engine_enabled: bool = False
    events_audit_enabled: bool = False
    sla_fraud_enabled: bool = False
    workflow_migration_enabled: bool = False
    memory_governance_enabled: bool = False
