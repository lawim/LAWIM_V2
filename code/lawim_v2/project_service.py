from __future__ import annotations

from http import HTTPStatus

from .observability import METRICS
from .dto import paginated_payload, project_dto, project_progress_dto, project_step_dto
from .errors import ValidationError
from .project_domain import PROJECT_TYPES, PROJECT_STATUSES, PROJECT_PRIORITIES, TIMELINE_HORIZONS
from .user_roles import resolve_official_user_role


class ProjectPermissionDenied(Exception):
    status = HTTPStatus.FORBIDDEN
    code = "forbidden"

    def __init__(self, message: str = "Forbidden") -> None:
        super().__init__(message)
        self.message = message


class ProjectService:
    def __init__(self, repository, policy) -> None:
        self.repository = repository
        self.policy = policy

    def can_access_project(self, actor: dict[str, object] | None, project_row: dict[str, object]) -> bool:
        if self.policy.is_admin(actor):
            return True
        if actor is None:
            return False
        if project_row.get("user_id") == actor.get("id"):
            return True
        organization_id = actor.get("organization_id")
        if organization_id is not None and project_row.get("organization_id") == organization_id:
            return resolve_official_user_role(actor.get("role")) in {"admin", "manager", "operator", "partner"}
        return False

    def can_manage_project(self, actor: dict[str, object] | None, project_row: dict[str, object]) -> bool:
        if self.policy.is_admin(actor):
            return True
        if actor is None:
            return False
        return project_row.get("user_id") == actor.get("id")

    def _require_access(self, actor: dict[str, object], project_id: int) -> dict[str, object]:
        project = self.repository.get_project(project_id)
        if not self.can_access_project(actor, project):
            raise ProjectPermissionDenied("You cannot access this project")
        return project

    def _require_manage(self, actor: dict[str, object], project_id: int) -> dict[str, object]:
        project = self.repository.get_project(project_id)
        if not self.can_manage_project(actor, project):
            raise ProjectPermissionDenied("You cannot modify this project")
        return project

    def create_project(
        self,
        *,
        actor: dict[str, object],
        title: str,
        project_type: str,
        objective: str,
        budget_min: int | None = None,
        budget_max: int | None = None,
        currency: str = "XAF",
        location_city: str | None = None,
        location_region: str | None = None,
        location_country: str = "Cameroon",
        location_latitude: float | None = None,
        location_longitude: float | None = None,
        timeline_horizon: str | None = None,
        status: str = "draft",
        priority: str = "normal",
        organization_id: int | None = None,
        metadata: dict[str, object] | None = None,
    ) -> dict[str, object]:
        if project_type not in PROJECT_TYPES:
            raise ValidationError(f"unsupported project_type: {project_type}")
        user_id = int(actor["id"])
        org_id = organization_id if organization_id is not None else actor.get("organization_id")
        if org_id is not None:
            org_id = int(org_id)
        row = self.repository.create_project(
            title=title,
            project_type=project_type,
            objective=objective,
            user_id=user_id,
            organization_id=org_id,
            budget_min=budget_min,
            budget_max=budget_max,
            currency=currency,
            location_city=location_city,
            location_region=location_region,
            location_country=location_country,
            location_latitude=location_latitude,
            location_longitude=location_longitude,
            timeline_horizon=timeline_horizon,
            status=status,
            priority=priority,
            metadata=metadata,
        )
        METRICS.increment("projects")
        return project_dto(row)

    def list_projects(
        self,
        *,
        actor: dict[str, object],
        user_id: int | None = None,
        organization_id: int | None = None,
        status: str | None = None,
        project_type: str | None = None,
        priority: str | None = None,
        page: int = 1,
        limit: int = 20,
        sort: str = "created_at",
        order: str = "desc",
    ) -> dict[str, object]:
        if status and status not in PROJECT_STATUSES:
            raise ValidationError(f"unsupported status: {status}")
        if project_type and project_type not in PROJECT_TYPES:
            raise ValidationError(f"unsupported project_type: {project_type}")
        if priority and priority not in PROJECT_PRIORITIES:
            raise ValidationError(f"unsupported priority: {priority}")
        if not self.policy.is_admin(actor):
            user_id = int(actor["id"])
            organization_id = None
        payload = self.repository.list_projects(
            user_id=user_id,
            organization_id=organization_id,
            status=status,
            project_type=project_type,
            priority=priority,
            page=page,
            limit=limit,
            sort=sort,
            order=order,
        )
        items = [project_dto(row) for row in payload["items"]]
        from .dto import PaginationMeta

        pagination = PaginationMeta(**payload["pagination"])
        return paginated_payload(items, key="projects", pagination=pagination)

    def get_project(self, *, actor: dict[str, object], project_id: int) -> dict[str, object]:
        project = self._require_access(actor, project_id)
        return project_dto(project)

    def get_project_detail(self, *, actor: dict[str, object], project_id: int) -> dict[str, object]:
        self._require_access(actor, project_id)
        detail = self.repository.get_project_detail(project_id)
        return {
            "project": project_dto(detail["project"]),
            "steps": [project_step_dto(step) for step in detail["steps"]],
            "checklist": detail["checklist"],
            "history": detail["history"],
            "progress": project_progress_dto(detail["progress"]),
            "next_actions": detail["next_actions"],
        }

    def update_project(
        self,
        *,
        actor: dict[str, object],
        project_id: int,
        **fields: object,
    ) -> dict[str, object]:
        self._require_manage(actor, project_id)
        if fields.get("timeline_horizon") and str(fields["timeline_horizon"]) not in TIMELINE_HORIZONS:
            raise ValidationError(f"unsupported timeline_horizon: {fields['timeline_horizon']}")
        row = self.repository.update_project(project_id, **fields)
        return project_dto(row)

    def archive_project(self, *, actor: dict[str, object], project_id: int) -> dict[str, object]:
        self._require_manage(actor, project_id)
        row = self.repository.archive_project(project_id)
        return project_dto(row)

    def list_project_steps(self, *, actor: dict[str, object], project_id: int) -> list[dict[str, object]]:
        self._require_access(actor, project_id)
        return [project_step_dto(step) for step in self.repository.list_project_steps(project_id)]

    def update_project_step(
        self,
        *,
        actor: dict[str, object],
        project_id: int,
        step_id: int,
        status: str | None = None,
        note: str | None = None,
    ) -> dict[str, object]:
        self._require_manage(actor, project_id)
        row = self.repository.update_project_step(project_id, step_id, status=status, note=note)
        return project_step_dto(row)

    def get_project_progress(self, *, actor: dict[str, object], project_id: int) -> dict[str, object]:
        self._require_access(actor, project_id)
        return project_progress_dto(self.repository.project_progress_payload(project_id))

    def get_project_next_actions(self, *, actor: dict[str, object], project_id: int) -> list[dict[str, object]]:
        self._require_access(actor, project_id)
        return self.repository.project_next_actions(project_id)
