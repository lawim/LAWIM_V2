from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from lawim_runtime.domains.base.context import DomainRuntimeContext
from lawim_runtime.domains.base.errors import DomainValidationError
from lawim_runtime.domains.base.request import DomainRuntimeRequest
from lawim_runtime.domains.base.result import DomainRuntimeResult, DomainRuntimeStatus
from lawim_runtime.domains.base.runtime import DomainRuntime

from .events import CRMEvent, CRMEventType
from .metrics import CRMMetrics
from .models import CRMStatus, HandoverData, LeadData, OpportunityData
from .repository import CRMRepository, InMemoryCRMRepository


class CRMRuntime(DomainRuntime):
    runtime_name: str = "crm"
    supported_actions: list[str] = [
        "CREATE_OR_UPDATE_LEAD",
        "CREATE_OR_UPDATE_OPPORTUNITY",
        "ESCALATE_TO_HUMAN",
        "SYNC_PROJECT_TIMELINE",
        "CLOSE_CRM_CASE",
    ]

    def __init__(self, repository: CRMRepository | None = None) -> None:
        self._repository = repository or InMemoryCRMRepository()
        self._opportunities_by_project: dict[str, OpportunityData] = {}
        self._metrics = CRMMetrics()

    @property
    def metrics(self) -> CRMMetrics:
        return self._metrics

    def execute_op(self, request: DomainRuntimeRequest, context: DomainRuntimeContext) -> dict[str, Any]:
        action = request.action_code
        params = request.parameters

        if action == "CREATE_OR_UPDATE_LEAD":
            return self._execute_create_or_update_lead(params)
        elif action == "CREATE_OR_UPDATE_OPPORTUNITY":
            return self._execute_create_or_update_opportunity(params)
        elif action == "ESCALATE_TO_HUMAN":
            return self._execute_escalate_to_human(params)
        elif action == "SYNC_PROJECT_TIMELINE":
            return self._execute_sync_project_timeline(params)
        elif action == "CLOSE_CRM_CASE":
            return self._execute_close_crm_case(params)
        else:
            raise DomainValidationError(f"unsupported action: {action}")

    def _execute_create_or_update_lead(self, params: dict[str, Any]) -> dict[str, Any]:
        project_id = params.get("project_id", "")
        if not project_id:
            return {
                "status": CRMStatus.FAILED.value,
                "error": "project_id is required",
            }

        existing = self._repository.get_lead_by_project(project_id)
        if existing:
            existing.contact_name = params.get("contact_name", existing.contact_name)
            existing.contact_phone = params.get("contact_phone", existing.contact_phone)
            existing.contact_email = params.get("contact_email", existing.contact_email)
            existing.source = params.get("source", existing.source)
            existing.status = params.get("status", existing.status)
            self._repository.save_lead(existing)
            self._metrics.leads_updated += 1
            return {
                "status": CRMStatus.LEAD_UPDATED.value,
                "lead_id": existing.lead_id,
                "project_id": existing.project_id,
                "is_new": False,
            }

        lead = LeadData(
            lead_id=uuid4().hex[:16],
            project_id=project_id,
            contact_name=params.get("contact_name", ""),
            contact_phone=params.get("contact_phone", ""),
            contact_email=params.get("contact_email", ""),
            source=params.get("source", ""),
            status=params.get("status", "new"),
        )
        self._repository.save_lead(lead)
        self._metrics.leads_created += 1
        return {
            "status": CRMStatus.LEAD_CREATED.value,
            "lead_id": lead.lead_id,
            "project_id": lead.project_id,
            "is_new": True,
        }

    def _execute_create_or_update_opportunity(self, params: dict[str, Any]) -> dict[str, Any]:
        project_id = params.get("project_id", "")
        if not project_id:
            return {
                "status": CRMStatus.FAILED.value,
                "error": "project_id is required",
            }

        existing = self._opportunities_by_project.get(project_id)
        if existing:
            existing.stage = params.get("stage", existing.stage)
            existing.value = params.get("value", existing.value)
            existing.probability = params.get("probability", existing.probability)
            existing.expected_close_date = params.get("expected_close_date", existing.expected_close_date)
            self._repository.save_opportunity(existing)
            self._metrics.opportunities_created += 1
            return {
                "status": CRMStatus.OPPORTUNITY_UPDATED.value,
                "opportunity_id": existing.opportunity_id,
                "project_id": existing.project_id,
                "is_new": False,
            }

        lead = self._repository.get_lead_by_project(project_id)
        opportunity = OpportunityData(
            opportunity_id=uuid4().hex[:16],
            project_id=project_id,
            lead_id=lead.lead_id if lead else "",
            stage=params.get("stage", "qualification"),
            value=params.get("value", 0.0),
            probability=params.get("probability", 0.0),
            expected_close_date=params.get("expected_close_date", ""),
        )
        self._opportunities_by_project[project_id] = opportunity
        self._repository.save_opportunity(opportunity)
        self._metrics.opportunities_created += 1
        return {
            "status": CRMStatus.OPPORTUNITY_CREATED.value,
            "opportunity_id": opportunity.opportunity_id,
            "project_id": opportunity.project_id,
            "is_new": True,
        }

    def _execute_escalate_to_human(self, params: dict[str, Any]) -> dict[str, Any]:
        project_id = params.get("project_id", "")
        if not project_id:
            return {
                "status": CRMStatus.FAILED.value,
                "error": "project_id is required",
            }

        handover = HandoverData(
            handover_id=uuid4().hex[:16],
            project_id=project_id,
            reason=params.get("reason", ""),
            target_team=params.get("target_team", "support"),
            status="open",
        )
        self._repository.save_handover(handover)
        self._metrics.handovers_created += 1
        return {
            "status": CRMStatus.HANDOVER_CREATED.value,
            "handover_id": handover.handover_id,
            "project_id": handover.project_id,
        }

    def _execute_sync_project_timeline(self, params: dict[str, Any]) -> dict[str, Any]:
        project_id = params.get("project_id", "")
        if not project_id:
            return {
                "status": CRMStatus.FAILED.value,
                "error": "project_id is required",
            }
        return {
            "status": CRMStatus.SIMULATED.value,
            "project_id": project_id,
            "message": "timeline sync simulated",
        }

    def _execute_close_crm_case(self, params: dict[str, Any]) -> dict[str, Any]:
        project_id = params.get("project_id", "")
        if not project_id:
            return {
                "status": CRMStatus.FAILED.value,
                "error": "project_id is required",
            }

        lead = self._repository.get_lead_by_project(project_id)
        if lead:
            lead.status = "closed"
            self._repository.save_lead(lead)

        handovers = self._repository.list_handovers()
        for h in handovers:
            if h.project_id == project_id and h.status == "open":
                h.status = "resolved"
                h.resolved_at = datetime.now(timezone.utc).isoformat()
                self._repository.save_handover(h)
                self._metrics.handovers_resolved += 1

        return {
            "status": CRMStatus.HANDOVER_RESOLVED.value,
            "project_id": project_id,
        }

    def validate(self, request: DomainRuntimeRequest) -> list[str]:
        errors = super().validate(request)
        params = request.parameters
        action = request.action_code
        if action in ("CREATE_OR_UPDATE_LEAD", "CREATE_OR_UPDATE_OPPORTUNITY", "ESCALATE_TO_HUMAN", "SYNC_PROJECT_TIMELINE", "CLOSE_CRM_CASE"):
            if not params.get("project_id"):
                errors.append("project_id is required")
        return errors

    def verify(self, request: DomainRuntimeRequest, output: dict[str, Any]) -> bool:
        if not isinstance(output, dict):
            return False
        status = output.get("status")
        if status == CRMStatus.FAILED.value:
            return "error" in output
        if status in (
            CRMStatus.LEAD_CREATED.value,
            CRMStatus.LEAD_UPDATED.value,
            CRMStatus.OPPORTUNITY_CREATED.value,
            CRMStatus.OPPORTUNITY_UPDATED.value,
            CRMStatus.HANDOVER_CREATED.value,
            CRMStatus.HANDOVER_RESOLVED.value,
            CRMStatus.SIMULATED.value,
        ):
            return "project_id" in output
        return False
