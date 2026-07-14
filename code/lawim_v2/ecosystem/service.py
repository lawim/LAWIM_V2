from __future__ import annotations

from http import HTTPStatus

from ..observability import METRICS
from ..project_service import ProjectPermissionDenied, ProjectService
from . import dto as edto
from .constants import PARTNER_TYPES, SERVICE_CATEGORIES


class EcosystemService:
    def __init__(self, repository, project_service: ProjectService, policy) -> None:
        self.repository = repository
        self.projects = project_service
        self.policy = policy

    def list_partners(
        self,
        *,
        actor: dict[str, object],
        partner_type: str | None = None,
        city: str | None = None,
        page: int = 1,
        limit: int = 20,
    ) -> dict[str, object]:
        self._require_authenticated(actor)
        payload = self.repository.list_partner_profiles(partner_type=partner_type, city=city, page=page, limit=limit)
        return {
            "partners": [edto.partner_profile_dto(row) for row in payload["partners"]],
            "pagination": payload["pagination"],
        }

    def get_partner(self, *, actor: dict[str, object], partner_id: int) -> dict[str, object]:
        self._require_authenticated(actor)
        METRICS.increment("ecosystem_partners")
        return {"partner": edto.partner_profile_dto(self.repository.get_partner_profile(partner_id))}

    def create_partner(
        self,
        *,
        actor: dict[str, object],
        organization_id: int,
        partner_type: str,
        display_name: str,
        description: str | None = None,
        city: str | None = None,
        region: str | None = None,
    ) -> dict[str, object]:
        if not self.policy.is_admin(actor):
            raise ProjectPermissionDenied("Partner creation requires admin")
        if partner_type not in PARTNER_TYPES:
            raise ProjectPermissionDenied(f"unsupported partner_type: {partner_type}")
        row = self.repository.create_partner_profile(
            organization_id=organization_id,
            partner_type=partner_type,
            display_name=display_name,
            description=description,
            city=city,
            region=region,
        )
        METRICS.increment("ecosystem_partners")
        return {"partner": edto.partner_profile_dto(row)}

    def list_services(
        self,
        *,
        actor: dict[str, object],
        category: str | None = None,
        page: int = 1,
        limit: int = 20,
    ) -> dict[str, object]:
        self._require_authenticated(actor)
        payload = self.repository.list_service_catalog(category=category, page=page, limit=limit)
        return {
            "services": [edto.service_catalog_dto(row) for row in payload["services"]],
            "pagination": payload["pagination"],
        }

    def get_service(self, *, actor: dict[str, object], service_id: int) -> dict[str, object]:
        self._require_authenticated(actor)
        METRICS.increment("ecosystem_services")
        return {"service": edto.service_catalog_dto(self.repository.get_service_catalog_item(service_id))}

    def list_workflows(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_authenticated(actor)
        return {"workflows": [edto.workflow_dto(row) for row in self.repository.list_workflows()]}

    def get_project_workflow(self, *, actor: dict[str, object], project_id: int) -> dict[str, object]:
        self.projects._require_access(actor, project_id)
        instance = self.repository.ensure_project_workflow(project_id)
        METRICS.increment("ecosystem_workflows")
        return {"workflow_instance": edto.workflow_instance_dto(instance)}

    def get_reputation(self, *, actor: dict[str, object], subject_type: str, subject_id: int) -> dict[str, object]:
        self._require_authenticated(actor)
        if subject_type == "partner":
            row = self.repository.compute_partner_reputation(subject_id)
        else:
            row = self.repository.get_reputation(subject_type=subject_type, subject_id=subject_id)
            if row is None:
                row = {"subject_type": subject_type, "subject_id": subject_id, "trust_score": 70, "quality_score": 70}
        METRICS.increment("ecosystem_reputation")
        return {"reputation": edto.reputation_dto(row)}

    def list_ecosystem_notifications(self, *, actor: dict[str, object], limit: int = 50) -> dict[str, object]:
        rows = self.repository.list_ecosystem_notifications(int(actor["id"]), limit=limit)
        METRICS.increment("ecosystem_notifications")
        return {"notifications": [edto.ecosystem_notification_dto(row) for row in rows]}

    def list_ecosystem_events(self, *, actor: dict[str, object], project_id: int | None = None, limit: int = 50) -> dict[str, object]:
        if project_id is not None:
            self.projects._require_access(actor, project_id)
        rows = self.repository.list_ecosystem_events(project_id=project_id, limit=limit)
        return {"events": [edto.ecosystem_event_dto(row) for row in rows]}

    def get_orchestration(self, *, actor: dict[str, object], project_id: int) -> dict[str, object]:
        self.projects._require_access(actor, project_id)
        METRICS.increment("ecosystem_orchestration")
        return {"orchestration": self.repository.get_project_orchestration(project_id)}

    def create_service_order(
        self,
        *,
        actor: dict[str, object],
        project_id: int,
        service_catalog_id: int,
        partner_profile_id: int | None = None,
        cost_estimate: int | None = None,
        scheduled_at: str | None = None,
    ) -> dict[str, object]:
        self.projects._require_manage(actor, project_id)
        row = self.repository.create_service_order(
            project_id=project_id,
            service_catalog_id=service_catalog_id,
            partner_profile_id=partner_profile_id,
            cost_estimate=cost_estimate,
            scheduled_at=scheduled_at,
        )
        return {"service_order": edto.service_order_dto(row)}

    def list_project_resources_ecosystem(self, *, actor: dict[str, object], project_id: int) -> dict[str, object]:
        self.projects._require_access(actor, project_id)
        resources = self.repository.list_project_resources(project_id)
        orders = self.repository.list_service_orders(project_id)
        interventions = self.repository.list_interventions(project_id)
        matches = self.repository.list_project_matches(project_id)
        return {
            "resources": resources,
            "service_orders": [edto.service_order_dto(row) for row in orders],
            "interventions": [edto.intervention_dto(row) for row in interventions],
            "matches": [edto.match_result_dto(row) for row in matches],
        }

    def _require_authenticated(self, actor: dict[str, object]) -> None:
        if actor is None:
            raise ProjectPermissionDenied("Authentication required")
