from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from ..errors import NotFoundError, ValidationError
from .constants import DEFAULT_SERVICE_CATALOG, WORKFLOW_STEP_TEMPLATES, WORKFLOW_TYPES
from .engines import (
    MatchingEngine2,
    NotificationEventEngine,
    ResourceOrchestrationEngine,
    TrustReputationEngine,
    WorkflowEngine,
    normalize_partner_type,
    parse_json_list,
)
from .schema_v8_ddl import V8_TABLE_NAMES


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


class EcosystemRepositoryMixin:
    def ecosystem_tables_present(self) -> bool:
        row = self.one("SELECT name FROM sqlite_master WHERE type='table' AND name='partner_profiles'")
        return row is not None

    def seed_ecosystem_catalog(self) -> None:
        if self.one("SELECT id FROM service_catalog LIMIT 1") is not None:
            return
        now = _utcnow()
        for item in DEFAULT_SERVICE_CATALOG:
            with self._transaction() as conn:
                conn.execute(
                    """
                    INSERT INTO service_catalog (
                        service_key, category, title, description, conditions,
                        indicative_price_min, indicative_price_max, currency,
                        estimated_duration_days, documents_json, prerequisites_json,
                        deliverables_json, status, metadata_json, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, 'XAF', ?, '[]', '[]', '[]', 'active', '{}', ?, ?)
                    """,
                    (
                        item["service_key"],
                        item["category"],
                        item["title"],
                        item["description"],
                        "Conditions standard LAWIM",
                        item.get("indicative_price_min"),
                        item.get("indicative_price_max"),
                        item.get("estimated_duration_days", 7),
                        now,
                        now,
                    ),
                )
        for workflow_type in WORKFLOW_TYPES:
            workflow_key = f"workflow-{workflow_type}"
            if self.one("SELECT id FROM workflows WHERE workflow_key = ?", (workflow_key,)) is not None:
                continue
            template = WORKFLOW_STEP_TEMPLATES.get(workflow_type, [])
            now = _utcnow()
            with self._transaction() as conn:
                cursor = conn.execute(
                    """
                    INSERT INTO workflows (workflow_key, workflow_type, title, description, status, created_at, updated_at)
                    VALUES (?, ?, ?, ?, 'active', ?, ?)
                    """,
                    (workflow_key, workflow_type, f"Parcours {workflow_type}", f"Workflow standard {workflow_type}", now, now),
                )
                workflow_id = int(cursor.lastrowid)
                for position, step in enumerate(template):
                    conn.execute(
                        """
                        INSERT INTO workflow_steps (
                            workflow_id, step_key, title, position, partner_type, service_key,
                            depends_on_json, validation_rules_json, created_at
                        ) VALUES (?, ?, ?, ?, ?, ?, '[]', '[]', ?)
                        """,
                        (
                            workflow_id,
                            step["step_key"],
                            step["title"],
                            position,
                            step.get("partner_type"),
                            step.get("service_key"),
                            now,
                        ),
                    )

    def seed_demo_partners(self) -> None:
        if self.one("SELECT id FROM partner_profiles LIMIT 1") is not None:
            return
        org = self.one("SELECT * FROM organizations WHERE slug = 'lawim-partner-group'")
        agency = self.one("SELECT * FROM organizations WHERE slug = 'lawim-demo-agency'")
        if org is None:
            return
        now = _utcnow()
        profiles = [
            (int(org["id"]), "real_estate_agency", "LAWIM Partner Agency", "Agence partenaire démo"),
            (int(agency["id"]) if agency else int(org["id"]), "notary", "LAWIM Notaire Associé", "Notaire partenaire"),
            (int(org["id"]), "bank", "LAWIM Finance Desk", "Banque partenaire"),
        ]
        for organization_id, partner_type, display_name, description in profiles:
            if self.one(
                "SELECT id FROM partner_profiles WHERE organization_id = ? AND partner_type = ?",
                (organization_id, partner_type),
            ):
                continue
            with self._transaction() as conn:
                cursor = conn.execute(
                    """
                    INSERT INTO partner_profiles (
                        organization_id, partner_type, display_name, description, status,
                        quality_score, trust_score, completion_rate, reliability_score,
                        response_time_hours, satisfaction_score, incident_count,
                        specialties_json, metadata_json, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, 'active', 82, 78, 0.9, 80, 12, 85, 0, '[]', '{}', ?, ?)
                    """,
                    (organization_id, partner_type, display_name, description, now, now),
                )
                profile_id = int(cursor.lastrowid)
                conn.execute(
                    "INSERT INTO partner_zones (partner_profile_id, city, region, country, created_at) VALUES (?, 'Douala', 'Littoral', 'Cameroon', ?)",
                    (profile_id, now),
                )
                conn.execute(
                    "INSERT INTO partner_zones (partner_profile_id, city, region, country, created_at) VALUES (?, 'Yaounde', 'Centre', 'Cameroon', ?)",
                    (profile_id, now),
                )
                conn.execute(
                    "INSERT INTO partner_availability (partner_profile_id, status, schedule_json, updated_at) VALUES (?, 'available', '{}', ?)",
                    (profile_id, now),
                )
                conn.execute(
                    "INSERT INTO partner_sla (partner_profile_id, response_hours, completion_days, uptime_percent, created_at) VALUES (?, 24, 14, 95, ?)",
                    (profile_id, now),
                )
        self._link_catalog_to_partners()

    def _link_catalog_to_partners(self) -> None:
        now = _utcnow()
        partners = self.all("SELECT * FROM partner_profiles WHERE status = 'active'")
        services = self.all("SELECT * FROM service_catalog WHERE status = 'active'")
        for service in services:
            for partner in partners[:2]:
                exists = self.one(
                    "SELECT id FROM service_catalog_partners WHERE service_catalog_id = ? AND partner_profile_id = ?",
                    (service["id"], partner["id"]),
                )
                if exists:
                    continue
                with self._transaction() as conn:
                    conn.execute(
                        "INSERT INTO service_catalog_partners (service_catalog_id, partner_profile_id, priority, created_at) VALUES (?, ?, 50, ?)",
                        (service["id"], partner["id"], now),
                    )

    def list_partner_profiles(
        self,
        *,
        partner_type: str | None = None,
        city: str | None = None,
        status: str | None = "active",
        limit: int = 50,
        page: int = 1,
    ) -> dict[str, object]:
        clauses = ["1=1"]
        params: list[object] = []
        if partner_type:
            clauses.append("partner_type = ?")
            params.append(normalize_partner_type(partner_type))
        if status:
            clauses.append("status = ?")
            params.append(status)
        if city:
            clauses.append(
                "id IN (SELECT partner_profile_id FROM partner_zones WHERE lower(city) = lower(?))"
            )
            params.append(city)
        where = " AND ".join(clauses)
        offset = max(0, (page - 1) * limit)
        total = int(self.one(f"SELECT COUNT(*) AS c FROM partner_profiles WHERE {where}", tuple(params))["c"])
        rows = self.all(
            f"SELECT * FROM partner_profiles WHERE {where} ORDER BY trust_score DESC, id ASC LIMIT ? OFFSET ?",
            tuple(params) + (limit, offset),
        )
        enriched = [self._enrich_partner(row) for row in rows]
        return {"partners": enriched, "pagination": {"page": page, "limit": limit, "total": total}}

    def get_partner_profile(self, profile_id: int) -> dict[str, object]:
        row = self.one("SELECT * FROM partner_profiles WHERE id = ?", (profile_id,))
        if row is None:
            raise NotFoundError("partner profile not found")
        return self._enrich_partner(row)

    def _enrich_partner(self, row: dict[str, object]) -> dict[str, object]:
        profile_id = int(row["id"])
        zones = self.all("SELECT * FROM partner_zones WHERE partner_profile_id = ?", (profile_id,))
        skills = self.all("SELECT * FROM partner_skills WHERE partner_profile_id = ?", (profile_id,))
        certs = self.all("SELECT * FROM partner_certifications WHERE partner_profile_id = ?", (profile_id,))
        availability = self.one("SELECT * FROM partner_availability WHERE partner_profile_id = ?", (profile_id,))
        sla = self.one("SELECT * FROM partner_sla WHERE partner_profile_id = ?", (profile_id,))
        services = self.all(
            """
            SELECT sc.* FROM service_catalog sc
            JOIN service_catalog_partners scp ON scp.service_catalog_id = sc.id
            WHERE scp.partner_profile_id = ?
            ORDER BY scp.priority DESC
            """,
            (profile_id,),
        )
        payload = dict(row)
        payload["zones"] = zones
        payload["skills"] = skills
        payload["certifications"] = certs
        payload["availability_status"] = availability.get("status") if availability else "unknown"
        payload["sla"] = sla
        payload["services"] = services
        payload["specialties"] = parse_json_list(str(row.get("specialties_json")))
        return payload

    def create_partner_profile(
        self,
        *,
        organization_id: int,
        partner_type: str,
        display_name: str,
        description: str | None = None,
        city: str | None = None,
        region: str | None = None,
    ) -> dict[str, object]:
        normalized = normalize_partner_type(partner_type)
        self.get_organization_by_id(organization_id)
        now = _utcnow()
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO partner_profiles (
                    organization_id, partner_type, display_name, description, status,
                    quality_score, trust_score, completion_rate, reliability_score,
                    response_time_hours, satisfaction_score, incident_count,
                    specialties_json, metadata_json, created_at, updated_at
                ) VALUES (?, ?, ?, ?, 'active', 70, 70, 0.85, 75, 24, 80, 0, '[]', '{}', ?, ?)
                """,
                (organization_id, normalized, display_name, description, now, now),
            )
            profile_id = int(cursor.lastrowid)
            conn.execute(
                "INSERT INTO partner_availability (partner_profile_id, status, schedule_json, updated_at) VALUES (?, 'available', '{}', ?)",
                (profile_id, now),
            )
            conn.execute(
                "INSERT INTO partner_sla (partner_profile_id, response_hours, completion_days, uptime_percent, created_at) VALUES (?, 24, 14, 95, ?)",
                (profile_id, now),
            )
            if city or region:
                conn.execute(
                    "INSERT INTO partner_zones (partner_profile_id, city, region, country, created_at) VALUES (?, ?, ?, 'Cameroon', ?)",
                    (profile_id, city, region, now),
                )
        self.record_event("partner_profile_created", {"partner_profile_id": profile_id})
        return self.get_partner_profile(profile_id)

    def list_service_catalog(
        self,
        *,
        category: str | None = None,
        status: str | None = "active",
        limit: int = 50,
        page: int = 1,
    ) -> dict[str, object]:
        clauses = ["1=1"]
        params: list[object] = []
        if category:
            clauses.append("category = ?")
            params.append(category)
        if status:
            clauses.append("status = ?")
            params.append(status)
        where = " AND ".join(clauses)
        offset = max(0, (page - 1) * limit)
        total = int(self.one(f"SELECT COUNT(*) AS c FROM service_catalog WHERE {where}", tuple(params))["c"])
        rows = self.all(
            f"SELECT * FROM service_catalog WHERE {where} ORDER BY category ASC, title ASC LIMIT ? OFFSET ?",
            tuple(params) + (limit, offset),
        )
        return {"services": [self._service_dto(row) for row in rows], "pagination": {"page": page, "limit": limit, "total": total}}

    def get_service_catalog_item(self, service_id: int) -> dict[str, object]:
        row = self.one("SELECT * FROM service_catalog WHERE id = ?", (service_id,))
        if row is None:
            raise NotFoundError("service not found")
        return self._service_dto(row, include_partners=True)

    def _service_dto(self, row: dict[str, object], *, include_partners: bool = False) -> dict[str, object]:
        payload = dict(row)
        payload["documents"] = parse_json_list(str(row.get("documents_json")))
        payload["prerequisites"] = parse_json_list(str(row.get("prerequisites_json")))
        payload["deliverables"] = parse_json_list(str(row.get("deliverables_json")))
        if include_partners:
            payload["partners"] = self.all(
                """
                SELECT pp.* FROM partner_profiles pp
                JOIN service_catalog_partners scp ON scp.partner_profile_id = pp.id
                WHERE scp.service_catalog_id = ?
                ORDER BY scp.priority DESC
                """,
                (row["id"],),
            )
        return payload

    def list_workflows(self) -> list[dict[str, object]]:
        return self.all("SELECT * FROM workflows WHERE status = 'active' ORDER BY workflow_type ASC")

    def get_workflow(self, workflow_id: int) -> dict[str, object]:
        row = self.one("SELECT * FROM workflows WHERE id = ?", (workflow_id,))
        if row is None:
            raise NotFoundError("workflow not found")
        steps = self.all("SELECT * FROM workflow_steps WHERE workflow_id = ? ORDER BY position ASC", (workflow_id,))
        payload = dict(row)
        payload["steps"] = steps
        return payload

    def ensure_project_workflow(self, project_id: int) -> dict[str, object]:
        project = self.get_project(project_id)
        goals = self.list_project_goals(project_id)
        engine = WorkflowEngine()
        workflow_type = engine.resolve_workflow_type(project, goals)
        workflow_key = f"workflow-{workflow_type}"
        workflow = self.one("SELECT * FROM workflows WHERE workflow_key = ?", (workflow_key,))
        if workflow is None:
            self.seed_ecosystem_catalog()
            workflow = self.one("SELECT * FROM workflows WHERE workflow_key = ?", (workflow_key,))
        if workflow is None:
            raise NotFoundError("workflow template not found")
        existing = self.one(
            "SELECT * FROM workflow_instances WHERE project_id = ? AND workflow_id = ?",
            (project_id, workflow["id"]),
        )
        if existing:
            return self.get_workflow_instance(int(existing["id"]))
        now = _utcnow()
        steps = self.all("SELECT * FROM workflow_steps WHERE workflow_id = ? ORDER BY position ASC", (workflow["id"],))
        first_step = steps[0]["step_key"] if steps else None
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO workflow_instances (
                    project_id, workflow_id, status, current_step_key, started_at, created_at, updated_at
                ) VALUES (?, ?, 'active', ?, ?, ?, ?)
                """,
                (project_id, workflow["id"], first_step, now, now, now),
            )
            instance_id = int(cursor.lastrowid)
            for step in steps:
                conn.execute(
                    """
                    INSERT INTO workflow_instance_steps (
                        workflow_instance_id, step_key, title, status, created_at, updated_at
                    ) VALUES (?, ?, ?, 'pending', ?, ?)
                    """,
                    (instance_id, step["step_key"], step["title"], now, now),
                )
        self.record_event("workflow_instance_created", {"project_id": project_id, "workflow_instance_id": instance_id})
        return self.get_workflow_instance(instance_id)

    def get_workflow_instance(self, instance_id: int) -> dict[str, object]:
        row = self.one("SELECT * FROM workflow_instances WHERE id = ?", (instance_id,))
        if row is None:
            raise NotFoundError("workflow instance not found")
        steps = self.all(
            "SELECT * FROM workflow_instance_steps WHERE workflow_instance_id = ? ORDER BY id ASC",
            (instance_id,),
        )
        workflow = self.get_workflow(int(row["workflow_id"]))
        payload = dict(row)
        payload["workflow"] = workflow
        payload["instance_steps"] = steps
        payload["progress_percent"] = WorkflowEngine().progress_percent(steps)
        return payload

    def get_project_workflow_instance(self, project_id: int) -> dict[str, object] | None:
        row = self.one("SELECT * FROM workflow_instances WHERE project_id = ? ORDER BY id DESC LIMIT 1", (project_id,))
        if row is None:
            return None
        return self.get_workflow_instance(int(row["id"]))

    def run_project_matching(self, project_id: int) -> dict[str, object]:
        project = self.get_project(project_id)
        goals = self.list_project_goals(project_id)
        constraints = self.list_project_constraints(project_id)
        journey_state = self.journey_engine_state(project_id)
        partners_payload = self.list_partner_profiles(limit=100, page=1)
        partners = partners_payload["partners"]
        services_payload = self.list_service_catalog(limit=100, page=1)
        services = services_payload["services"]
        engine = MatchingEngine2()
        result = engine.match(
            project=project,
            goals=goals,
            constraints=constraints,
            journey_state=journey_state,
            partners=partners,
            services=services,
        )
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                "UPDATE project_match_results SET status = 'expired', updated_at = ? WHERE project_id = ? AND status = 'active'",
                (now, project_id),
            )
        for match in result["partner_matches"]:
            self._store_match(project_id, match, now)
        for match in result["service_matches"]:
            self._store_match(project_id, match, now)
        self._update_ecosystem_state(project_id, result, now)
        event = self.create_ecosystem_event(
            project_id=project_id,
            user_id=int(project["user_id"]),
            event_type="match_refreshed",
            title="Matching ecosystem recalculé",
            payload={"partner_count": len(result["partner_matches"]), "service_count": len(result["service_matches"])},
        )
        self._deliver_ecosystem_notifications(event, int(project["user_id"]))
        self.record_event("project_matching_run", {"project_id": project_id})
        return result

    def _store_match(self, project_id: int, match: dict[str, object], now: str) -> None:
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO project_match_results (
                    project_id, match_type, partner_profile_id, service_catalog_id,
                    score, confidence, priority, rationale_json, status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'active', ?, ?)
                """,
                (
                    project_id,
                    match["match_type"],
                    match.get("partner_profile_id"),
                    match.get("service_catalog_id"),
                    match.get("score"),
                    match.get("confidence"),
                    match.get("priority"),
                    _json(match.get("rationale") or []),
                    now,
                    now,
                ),
            )

    def _update_ecosystem_state(self, project_id: int, result: dict[str, object], now: str) -> None:
        payload = {"last_match": result, "updated_at": now}
        existing = self.one("SELECT id FROM project_ecosystem_state WHERE project_id = ?", (project_id,))
        if existing:
            with self._transaction() as conn:
                conn.execute(
                    "UPDATE project_ecosystem_state SET orchestration_json = ?, last_matched_at = ?, updated_at = ? WHERE project_id = ?",
                    (_json(payload), now, now, project_id),
                )
        else:
            with self._transaction() as conn:
                conn.execute(
                    "INSERT INTO project_ecosystem_state (project_id, orchestration_json, last_matched_at, updated_at) VALUES (?, ?, ?, ?)",
                    (project_id, _json(payload), now, now),
                )

    def list_project_matches(self, project_id: int, *, match_type: str | None = None) -> list[dict[str, object]]:
        if match_type:
            rows = self.all(
                "SELECT * FROM project_match_results WHERE project_id = ? AND match_type = ? AND status = 'active' ORDER BY priority DESC, score DESC",
                (project_id, match_type),
            )
        else:
            rows = self.all(
                "SELECT * FROM project_match_results WHERE project_id = ? AND status = 'active' ORDER BY priority DESC, score DESC",
                (project_id,),
            )
        return [self._match_dto(row) for row in rows]

    def _match_dto(self, row: dict[str, object]) -> dict[str, object]:
        payload = dict(row)
        payload["rationale"] = parse_json_list(str(row.get("rationale_json")))
        if row.get("partner_profile_id"):
            try:
                payload["partner"] = self.get_partner_profile(int(row["partner_profile_id"]))
            except NotFoundError:
                payload["partner"] = None
        if row.get("service_catalog_id"):
            try:
                payload["service"] = self.get_service_catalog_item(int(row["service_catalog_id"]))
            except NotFoundError:
                payload["service"] = None
        return payload

    def compute_partner_reputation(self, profile_id: int) -> dict[str, object]:
        profile = self.get_partner_profile(profile_id)
        orders = self.all("SELECT * FROM service_orders WHERE partner_profile_id = ?", (profile_id,))
        metrics = TrustReputationEngine().compute(profile=profile, orders=orders, incidents=int(profile.get("incident_count") or 0))
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO reputation_metrics (
                    subject_type, subject_id, trust_score, quality_score, completion_rate,
                    reliability, avg_response_hours, satisfaction, incident_count, history_json, computed_at
                ) VALUES ('partner', ?, ?, ?, ?, ?, ?, ?, ?, '[]', ?)
                """,
                (
                    profile_id,
                    metrics["trust_score"],
                    metrics["quality_score"],
                    metrics["completion_rate"],
                    metrics["reliability"],
                    metrics["avg_response_hours"],
                    metrics["satisfaction"],
                    metrics["incident_count"],
                    now,
                ),
            )
            conn.execute(
                """
                UPDATE partner_profiles SET trust_score = ?, quality_score = ?, completion_rate = ?, updated_at = ?
                WHERE id = ?
                """,
                (metrics["trust_score"], metrics["quality_score"], metrics["completion_rate"], now, profile_id),
            )
        metrics["computed_at"] = now
        metrics["subject_type"] = "partner"
        metrics["subject_id"] = profile_id
        return metrics

    def get_reputation(self, *, subject_type: str, subject_id: int) -> dict[str, object] | None:
        row = self.one(
            "SELECT * FROM reputation_metrics WHERE subject_type = ? AND subject_id = ? ORDER BY computed_at DESC LIMIT 1",
            (subject_type, subject_id),
        )
        return dict(row) if row else None

    def create_service_order(
        self,
        *,
        project_id: int,
        service_catalog_id: int,
        partner_profile_id: int | None = None,
        cost_estimate: int | None = None,
        scheduled_at: str | None = None,
    ) -> dict[str, object]:
        self.get_project(project_id)
        service = self.get_service_catalog_item(service_catalog_id)
        now = _utcnow()
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO service_orders (
                    project_id, service_catalog_id, partner_profile_id, status,
                    cost_estimate, currency, scheduled_at, created_at, updated_at
                ) VALUES (?, ?, ?, 'requested', ?, ?, ?, ?, ?)
                """,
                (project_id, service_catalog_id, partner_profile_id, cost_estimate, service.get("currency", "XAF"), scheduled_at, now, now),
            )
            order_id = int(cursor.lastrowid)
        event = self.create_ecosystem_event(
            project_id=project_id,
            user_id=None,
            event_type="service_order_created",
            title=f"Commande {service.get('title')}",
            payload={"service_order_id": order_id},
        )
        project = self.get_project(project_id)
        self._deliver_ecosystem_notifications(event, int(project["user_id"]))
        return self.get_service_order(order_id)

    def get_service_order(self, order_id: int) -> dict[str, object]:
        row = self.one("SELECT * FROM service_orders WHERE id = ?", (order_id,))
        if row is None:
            raise NotFoundError("service order not found")
        return dict(row)

    def list_service_orders(self, project_id: int) -> list[dict[str, object]]:
        return self.all("SELECT * FROM service_orders WHERE project_id = ? ORDER BY created_at DESC", (project_id,))

    def create_intervention(
        self,
        *,
        project_id: int,
        title: str,
        partner_profile_id: int | None = None,
        service_order_id: int | None = None,
        scheduled_at: str | None = None,
    ) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO project_interventions (
                    project_id, partner_profile_id, service_order_id, intervention_type,
                    title, status, scheduled_at, currency, created_at, updated_at
                ) VALUES (?, ?, ?, 'service', ?, 'planned', ?, 'XAF', ?, ?)
                """,
                (project_id, partner_profile_id, service_order_id, title, scheduled_at, now, now),
            )
            intervention_id = int(cursor.lastrowid)
        return self.one("SELECT * FROM project_interventions WHERE id = ?", (intervention_id,))  # type: ignore[return-value]

    def list_interventions(self, project_id: int) -> list[dict[str, object]]:
        return self.all("SELECT * FROM project_interventions WHERE project_id = ? ORDER BY scheduled_at ASC, id ASC", (project_id,))

    def create_ecosystem_event(
        self,
        *,
        project_id: int | None,
        user_id: int | None,
        event_type: str,
        title: str,
        payload: dict[str, object] | None = None,
    ) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO ecosystem_events (project_id, user_id, event_type, title, payload_json, occurred_at, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (project_id, user_id, event_type, title, _json(payload or {}), now, now),
            )
            event_id = int(cursor.lastrowid)
        row = self.one("SELECT * FROM ecosystem_events WHERE id = ?", (event_id,))
        assert row is not None
        return row

    def _deliver_ecosystem_notifications(self, event: dict[str, object], user_id: int) -> None:
        engine = NotificationEventEngine()
        notifications = engine.build_notifications(event=event, user_id=user_id, channels=("in_app",))
        now = _utcnow()
        for item in notifications:
            with self._transaction() as conn:
                conn.execute(
                    """
                    INSERT INTO ecosystem_notifications (
                        user_id, project_id, event_id, kind, title, body, channel, status,
                        scheduled_at, delivered_at, payload_json, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, NULL, ?, ?, ?)
                    """,
                    (
                        item["user_id"],
                        item.get("project_id"),
                        item.get("event_id"),
                        item["kind"],
                        item["title"],
                        item["body"],
                        item["channel"],
                        item["status"],
                        now if item["status"] == "delivered" else None,
                        item.get("payload_json") or "{}",
                        now,
                    ),
                )

    def list_ecosystem_notifications(self, user_id: int, *, limit: int = 50) -> list[dict[str, object]]:
        return self.all(
            "SELECT * FROM ecosystem_notifications WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
            (user_id, limit),
        )

    def list_ecosystem_events(self, project_id: int | None = None, *, limit: int = 50) -> list[dict[str, object]]:
        if project_id is not None:
            return self.all(
                "SELECT * FROM ecosystem_events WHERE project_id = ? ORDER BY occurred_at DESC LIMIT ?",
                (project_id, limit),
            )
        return self.all("SELECT * FROM ecosystem_events ORDER BY occurred_at DESC LIMIT ?", (limit,))

    def get_project_orchestration(self, project_id: int) -> dict[str, object]:
        project = self.get_project(project_id)
        partner_matches = self.list_project_matches(project_id, match_type="partner")
        service_matches = self.list_project_matches(project_id, match_type="service")
        orders = self.list_service_orders(project_id)
        interventions = self.list_interventions(project_id)
        resources = self.list_project_resources(project_id)
        workflow_instance = self.get_project_workflow_instance(project_id)
        workflow_steps = workflow_instance.get("instance_steps", []) if workflow_instance else []
        orchestration = ResourceOrchestrationEngine().assemble(
            project=project,
            partner_matches=partner_matches,
            service_matches=service_matches,
            orders=orders,
            interventions=interventions,
            resources=resources,
            workflow_instance=workflow_instance,
            workflow_steps=workflow_steps,
        )
        return orchestration

    def bootstrap_project_ecosystem(self, project_id: int) -> None:
        self.seed_ecosystem_catalog()
        self.seed_demo_partners()
        self.ensure_project_workflow(project_id)
        self.run_project_matching(project_id)
