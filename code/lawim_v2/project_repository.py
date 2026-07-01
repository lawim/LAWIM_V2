from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .api_query import pagination_meta
from .errors import NotFoundError, ValidationError
from .project_domain import (
    DEFAULT_CHECKLIST_BY_STEP,
    build_project_input,
    compute_progress,
    journey_templates,
    normalize_metadata,
    normalize_step_status,
    validate_status_transition,
    validate_step_status_transition,
)


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class ProjectRepositoryMixin:
    def create_project(self, **fields: Any) -> dict[str, object]:
        payload = build_project_input(**fields)
        now = _utcnow()
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO projects (
                    user_id, organization_id, title, project_type, objective,
                    budget_min, budget_max, currency,
                    location_city, location_region, location_country,
                    location_latitude, location_longitude,
                    timeline_horizon, status, priority, progress_percent,
                    metadata_json, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?, ?)
                """,
                (
                    payload["user_id"],
                    payload["organization_id"],
                    payload["title"],
                    payload["project_type"],
                    payload["objective"],
                    payload["budget_min"],
                    payload["budget_max"],
                    payload["currency"],
                    payload["location_city"],
                    payload["location_region"],
                    payload["location_country"],
                    payload["location_latitude"],
                    payload["location_longitude"],
                    payload["timeline_horizon"],
                    payload["status"],
                    payload["priority"],
                    payload["metadata_json"],
                    now,
                    now,
                ),
            )
            project_id = int(cursor.lastrowid)
        self._seed_project_journey(project_id, str(payload["project_type"]), now=now)
        project = self.get_project(project_id)
        self.record_event(
            "project_created",
            {"id": project_id, "user_id": payload["user_id"], "project_type": payload["project_type"]},
        )
        if hasattr(self, "bootstrap_project_intelligence"):
            self.bootstrap_project_intelligence(project_id, goal_key=str(payload["project_type"]))
            project = self.get_project(project_id)
        if hasattr(self, "bootstrap_project_ecosystem"):
            self.bootstrap_project_ecosystem(project_id)
            project = self.get_project(project_id)
        if hasattr(self, "bootstrap_project_cognition"):
            self.bootstrap_project_cognition(project_id)
            project = self.get_project(project_id)
        if hasattr(self, "bootstrap_project_assistant"):
            self.bootstrap_project_assistant(project_id, user_id=int(payload["user_id"]))
            project = self.get_project(project_id)
        return project

    def _seed_project_journey(self, project_id: int, project_type: str, *, now: str | None = None) -> None:
        timestamp = now or _utcnow()
        templates = journey_templates(project_type)
        with self._transaction() as conn:
            for index, template in enumerate(templates):
                cursor = conn.execute(
                    """
                    INSERT INTO project_steps (
                        project_id, step_key, title, description, position, status,
                        milestone, next_action, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, 'pending', ?, ?, ?, ?)
                    """,
                    (
                        project_id,
                        template["step_key"],
                        template["title"],
                        template.get("description"),
                        index,
                        template.get("milestone"),
                        template.get("next_action"),
                        timestamp,
                        timestamp,
                    ),
                )
                step_id = int(cursor.lastrowid)
                checklist = DEFAULT_CHECKLIST_BY_STEP.get(template["step_key"], ())
                for check_index, label in enumerate(checklist):
                    conn.execute(
                        """
                        INSERT INTO project_checklist_items (
                            project_id, step_id, label, checked, position, created_at, updated_at
                        ) VALUES (?, ?, ?, 0, ?, ?, ?)
                        """,
                        (project_id, step_id, label, check_index, timestamp, timestamp),
                    )

    def get_project(self, project_id: int) -> dict[str, object]:
        row = self.one("SELECT * FROM projects WHERE id = ?", (project_id,))
        if row is None:
            raise NotFoundError(f"unknown project id: {project_id}")
        return row

    def list_projects(
        self,
        *,
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
        allowed_sort = {"created_at", "updated_at", "title", "status", "priority", "progress_percent"}
        sort_field = sort if sort in allowed_sort else "created_at"
        sort_order = "DESC" if order.lower() != "asc" else "ASC"
        clauses: list[str] = ["1=1"]
        params: list[object] = []
        if user_id is not None:
            clauses.append("user_id = ?")
            params.append(user_id)
        if organization_id is not None:
            clauses.append("organization_id = ?")
            params.append(organization_id)
        if status:
            clauses.append("status = ?")
            params.append(status)
        if project_type:
            clauses.append("project_type = ?")
            params.append(project_type)
        if priority:
            clauses.append("priority = ?")
            params.append(priority)
        where = " AND ".join(clauses)
        total = self.scalar(f"SELECT COUNT(*) FROM projects WHERE {where}", tuple(params))
        offset = max(page - 1, 0) * limit
        rows = self.all(
            f"""
            SELECT * FROM projects
            WHERE {where}
            ORDER BY {sort_field} {sort_order}, id {sort_order}
            LIMIT ? OFFSET ?
            """,
            tuple(params + [limit, offset]),
        )
        return {
            "items": rows,
            "pagination": pagination_meta(page=page, limit=limit, total=int(total), sort=sort_field, order=order.lower()).to_dict(),
        }

    def update_project(self, project_id: int, **fields: Any) -> dict[str, object]:
        current = self.get_project(project_id)
        updates: dict[str, object] = {}
        if "title" in fields and fields["title"] is not None:
            title = str(fields["title"]).strip()
            if not title:
                raise ValidationError("title is required")
            updates["title"] = title
        if "objective" in fields and fields["objective"] is not None:
            objective = str(fields["objective"]).strip()
            if not objective:
                raise ValidationError("objective is required")
            updates["objective"] = objective
        if "project_type" in fields and fields["project_type"] is not None:
            from .project_domain import normalize_project_type

            updates["project_type"] = normalize_project_type(str(fields["project_type"]))
        if "budget_min" in fields:
            updates["budget_min"] = fields["budget_min"]
        if "budget_max" in fields:
            updates["budget_max"] = fields["budget_max"]
        if "currency" in fields and fields["currency"] is not None:
            from .project_domain import normalize_currency

            updates["currency"] = normalize_currency(str(fields["currency"]))
        for key in ("location_city", "location_region", "location_country", "timeline_horizon"):
            if key in fields:
                updates[key] = fields[key]
        for key in ("location_latitude", "location_longitude"):
            if key in fields:
                updates[key] = fields[key]
        if "priority" in fields and fields["priority"] is not None:
            from .project_domain import normalize_priority

            updates["priority"] = normalize_priority(str(fields["priority"]))
        if "status" in fields and fields["status"] is not None:
            from .project_domain import normalize_status

            next_status = normalize_status(str(fields["status"]))
            validate_status_transition(str(current["status"]), next_status)
            updates["status"] = next_status
            if next_status == "archived":
                updates["archived_at"] = _utcnow()
        if "metadata" in fields or "metadata_json" in fields:
            metadata = fields.get("metadata", fields.get("metadata_json"))
            updates["metadata_json"] = normalize_metadata(metadata)
        if "organization_id" in fields:
            updates["organization_id"] = fields["organization_id"]
        if not updates:
            return current
        updates["updated_at"] = _utcnow()
        assignments = ", ".join(f"{column} = ?" for column in updates)
        with self._transaction() as conn:
            conn.execute(
                f"UPDATE projects SET {assignments} WHERE id = ?",
                tuple(updates.values()) + (project_id,),
            )
        updated = self.get_project(project_id)
        self._refresh_project_progress(project_id)
        self.record_event("project_updated", {"id": project_id, "fields": sorted(updates.keys())})
        return self.get_project(project_id)

    def archive_project(self, project_id: int) -> dict[str, object]:
        return self.update_project(project_id, status="archived")

    def list_project_steps(self, project_id: int) -> list[dict[str, object]]:
        self.get_project(project_id)
        return self.all(
            """
            SELECT * FROM project_steps
            WHERE project_id = ?
            ORDER BY position ASC, id ASC
            """,
            (project_id,),
        )

    def list_project_checklist(self, project_id: int, *, step_id: int | None = None) -> list[dict[str, object]]:
        self.get_project(project_id)
        if step_id is not None:
            return self.all(
                """
                SELECT * FROM project_checklist_items
                WHERE project_id = ? AND step_id = ?
                ORDER BY position ASC, id ASC
                """,
                (project_id, step_id),
            )
        return self.all(
            """
            SELECT * FROM project_checklist_items
            WHERE project_id = ?
            ORDER BY step_id ASC, position ASC, id ASC
            """,
            (project_id,),
        )

    def list_project_step_history(self, project_id: int, *, limit: int = 50) -> list[dict[str, object]]:
        self.get_project(project_id)
        return self.all(
            """
            SELECT * FROM project_step_history
            WHERE project_id = ?
            ORDER BY created_at DESC, id DESC
            LIMIT ?
            """,
            (project_id, limit),
        )

    def update_project_step(
        self,
        project_id: int,
        step_id: int,
        *,
        status: str | None = None,
        note: str | None = None,
    ) -> dict[str, object]:
        self.get_project(project_id)
        step = self.one("SELECT * FROM project_steps WHERE id = ? AND project_id = ?", (step_id, project_id))
        if step is None:
            raise NotFoundError(f"unknown step id: {step_id}")
        updates: dict[str, object] = {}
        if status is not None:
            next_status = normalize_step_status(status)
            validate_step_status_transition(str(step["status"]), next_status)
            updates["status"] = next_status
            if next_status == "completed":
                updates["completed_at"] = _utcnow()
        if not updates:
            return step
        now = _utcnow()
        updates["updated_at"] = now
        assignments = ", ".join(f"{column} = ?" for column in updates)
        with self._transaction() as conn:
            conn.execute(
                f"UPDATE project_steps SET {assignments} WHERE id = ?",
                tuple(updates.values()) + (step_id,),
            )
            conn.execute(
                """
                INSERT INTO project_step_history (project_id, step_id, from_status, to_status, note, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (project_id, step_id, step["status"], updates.get("status", step["status"]), note, now),
            )
        self._refresh_project_progress(project_id)
        self.record_event(
            "project_step_updated",
            {"project_id": project_id, "step_id": step_id, "status": updates.get("status")},
        )
        updated = self.one("SELECT * FROM project_steps WHERE id = ?", (step_id,))
        assert updated is not None
        return updated

    def toggle_checklist_item(self, project_id: int, item_id: int, *, checked: bool) -> dict[str, object]:
        self.get_project(project_id)
        row = self.one(
            "SELECT * FROM project_checklist_items WHERE id = ? AND project_id = ?",
            (item_id, project_id),
        )
        if row is None:
            raise NotFoundError(f"unknown checklist item id: {item_id}")
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                "UPDATE project_checklist_items SET checked = ?, updated_at = ? WHERE id = ?",
                (1 if checked else 0, now, item_id),
            )
        updated = self.one("SELECT * FROM project_checklist_items WHERE id = ?", (item_id,))
        assert updated is not None
        self._refresh_project_progress(project_id)
        return updated

    def _refresh_project_progress(self, project_id: int) -> None:
        steps = self.list_project_steps(project_id)
        progress = compute_progress(steps)
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                "UPDATE projects SET progress_percent = ?, updated_at = ? WHERE id = ?",
                (progress, now, project_id),
            )

    def project_progress_payload(self, project_id: int) -> dict[str, object]:
        project = self.get_project(project_id)
        steps = self.list_project_steps(project_id)
        checklist = self.list_project_checklist(project_id)
        checked = sum(1 for item in checklist if int(item.get("checked", 0)) == 1)
        return {
            "project_id": project_id,
            "progress_percent": int(project.get("progress_percent", 0)),
            "steps_total": len(steps),
            "steps_completed": sum(1 for step in steps if str(step.get("status")) in {"completed", "skipped"}),
            "checklist_total": len(checklist),
            "checklist_checked": checked,
            "status": project.get("status"),
        }

    def project_next_actions(self, project_id: int) -> list[dict[str, object]]:
        from .project_domain import derive_next_actions

        project = self.get_project(project_id)
        steps = self.list_project_steps(project_id)
        return derive_next_actions(steps, project_status=str(project.get("status", "draft")))

    def get_project_detail(self, project_id: int) -> dict[str, object]:
        project = self.get_project(project_id)
        steps = self.list_project_steps(project_id)
        checklist = self.list_project_checklist(project_id)
        history = self.list_project_step_history(project_id, limit=20)
        return {
            "project": project,
            "steps": steps,
            "checklist": checklist,
            "history": history,
            "progress": self.project_progress_payload(project_id),
            "next_actions": self.project_next_actions(project_id),
        }
