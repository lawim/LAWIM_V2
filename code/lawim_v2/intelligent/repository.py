from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from ..errors import NotFoundError, ValidationError
from ..repository_introspection import table_exists
from .constants import GOAL_KEYS, KNOWLEDGE_CATEGORIES, LIFE_EVENT_TYPES
from .engines import (
    DecisionEngine,
    GoalEngine,
    JourneyEngine,
    LifeEventEngine,
    ProjectIntelligenceEngine,
    RecommendationEngine,
    TimelineEngine,
    parse_json_list,
)
from .schema_v7_ddl import V7_TABLE_NAMES


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


class IntelligentRepositoryMixin:
    def apply_intelligent_schema_v7(self) -> None:
        """Applied via schema_migrations.apply_sqlite_legacy_migrations()."""
        return None

    def bootstrap_project_intelligence(self, project_id: int, *, goal_key: str | None = None) -> None:
        project = self.get_project(project_id)
        key = goal_key or str(project.get("primary_goal_key") or project.get("project_type") or "buy")
        if key not in GOAL_KEYS:
            key = "buy" if str(project.get("project_type")) == "buy" else "other"
        now = _utcnow()
        goal_engine = GoalEngine()
        influence = goal_engine.influence(key)
        with self._transaction() as conn:
            conn.execute(
                "UPDATE projects SET primary_goal_key = ?, intelligence_json = ?, updated_at = ? WHERE id = ?",
                (key, _json({"bootstrapped": True, "goal_key": key}), now, project_id),
            )
        self.create_project_goal(
            project_id=project_id,
            goal_key=key,
            title=f"Objectif {key}",
            priority=str(influence["priority_boost"]),
        )
        self.ensure_journey(project_id, journey_key=f"journey-{key}")
        self.create_knowledge_fact(
            project_id=project_id,
            category="checklist",
            fact_key=f"goal-{key}",
            title=f"Parcours {key}",
            content=f"Étapes recommandées: {', '.join(influence['journey_steps'])}",
        )
        self.refresh_project_intelligence(project_id)

    def ensure_journey(self, project_id: int, *, journey_key: str) -> dict[str, object]:
        row = self.one("SELECT * FROM journeys WHERE project_id = ? AND journey_key = ?", (project_id, journey_key))
        if row is not None:
            return row
        now = _utcnow()
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO journeys (project_id, journey_key, status, replan_count, started_at, created_at, updated_at)
                VALUES (?, ?, 'active', 0, ?, ?, ?)
                """,
                (project_id, journey_key, now, now, now),
            )
            journey_id = int(cursor.lastrowid)
        self.record_event("journey_created", {"project_id": project_id, "journey_id": journey_id})
        row = self.one("SELECT * FROM journeys WHERE id = ?", (journey_id,))
        assert row is not None
        return row

    def get_journey(self, project_id: int, journey_id: int | None = None) -> dict[str, object]:
        if journey_id is not None:
            row = self.one("SELECT * FROM journeys WHERE id = ? AND project_id = ?", (journey_id, project_id))
        else:
            row = self.one("SELECT * FROM journeys WHERE project_id = ? ORDER BY id ASC LIMIT 1", (project_id,))
        if row is None:
            raise NotFoundError("journey not found")
        return row

    def list_journeys(self, project_id: int) -> list[dict[str, object]]:
        return self.all("SELECT * FROM journeys WHERE project_id = ? ORDER BY id ASC", (project_id,))

    def journey_engine_state(self, project_id: int) -> dict[str, object]:
        project = self.get_project(project_id)
        journey = self.get_journey(project_id)
        steps = self.list_project_steps(project_id)
        engine = JourneyEngine()
        state = engine.compute_state(project=project, journey=journey, steps=steps)
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                "UPDATE journeys SET status = ?, updated_at = ? WHERE id = ?",
                (state["status"], now, journey["id"]),
            )
        return state

    def replan_journey(self, project_id: int) -> dict[str, object]:
        project = self.get_project(project_id)
        goal_key = str(project.get("primary_goal_key") or project.get("project_type") or "other")
        engine = JourneyEngine()
        plan = engine.replan(goal_key=goal_key)
        journey = self.get_journey(project_id)
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                "UPDATE journeys SET status = 'replanned', replan_count = replan_count + 1, updated_at = ? WHERE id = ?",
                (now, journey["id"]),
            )
        self.record_event("journey_replanned", {"project_id": project_id, "plan": plan})
        return {"project_id": project_id, "goal_key": goal_key, "planned_steps": plan}

    def create_project_goal(self, *, project_id: int, goal_key: str, title: str, priority: str = "normal", status: str = "active", influence: dict[str, object] | None = None) -> dict[str, object]:
        if goal_key not in GOAL_KEYS:
            raise ValidationError(f"unsupported goal_key: {goal_key}")
        now = _utcnow()
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO project_goals (project_id, goal_key, title, priority, status, influence_json, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (project_id, goal_key, title.strip(), priority, status, _json(influence or {}), now, now),
            )
            row_id = int(cursor.lastrowid)
        self.record_event("project_goal_created", {"project_id": project_id, "goal_id": row_id})
        return self._one_table("project_goals", row_id)

    def list_project_goals(self, project_id: int) -> list[dict[str, object]]:
        return self.all("SELECT * FROM project_goals WHERE project_id = ? ORDER BY id ASC", (project_id,))

    def create_project_need(self, *, project_id: int, need_key: str, description: str, priority: str = "normal") -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO project_needs (project_id, need_key, description, priority, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, 'open', ?, ?)
                """,
                (project_id, need_key, description.strip(), priority, now, now),
            )
            row_id = int(cursor.lastrowid)
        return self._one_table("project_needs", row_id)

    def list_project_needs(self, project_id: int) -> list[dict[str, object]]:
        return self.all("SELECT * FROM project_needs WHERE project_id = ? ORDER BY id ASC", (project_id,))

    def create_project_constraint(self, *, project_id: int, constraint_type: str, description: str, severity: str = "medium") -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO project_constraints (project_id, constraint_type, description, severity, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (project_id, constraint_type, description.strip(), severity, now),
            )
            row_id = int(cursor.lastrowid)
        return self._one_table("project_constraints", row_id)

    def list_project_constraints(self, project_id: int) -> list[dict[str, object]]:
        return self.all("SELECT * FROM project_constraints WHERE project_id = ? ORDER BY id ASC", (project_id,))

    def create_project_preference(self, *, project_id: int, preference_key: str, value: dict[str, object], weight: int = 50) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO project_preferences (project_id, preference_key, value_json, weight, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (project_id, preference_key, _json(value), weight, now),
            )
            row_id = int(cursor.lastrowid)
        return self._one_table("project_preferences", row_id)

    def list_project_preferences(self, project_id: int) -> list[dict[str, object]]:
        return self.all("SELECT * FROM project_preferences WHERE project_id = ? ORDER BY id ASC", (project_id,))

    def create_project_funding(self, *, project_id: int, source_type: str, amount: int | None, currency: str = "XAF", status: str = "planned") -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO project_funding (project_id, source_type, amount, currency, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (project_id, source_type, amount, currency, status, now, now),
            )
            row_id = int(cursor.lastrowid)
        return self._one_table("project_funding", row_id)

    def list_project_funding(self, project_id: int) -> list[dict[str, object]]:
        return self.all("SELECT * FROM project_funding WHERE project_id = ? ORDER BY id ASC", (project_id,))

    def create_life_event(self, *, project_id: int, user_id: int, event_type: str, title: str, occurred_at: str | None = None) -> dict[str, object]:
        if event_type not in LIFE_EVENT_TYPES:
            raise ValidationError(f"unsupported event_type: {event_type}")
        engine = LifeEventEngine()
        impact = engine.impact(event_type)
        now = _utcnow()
        occurred = occurred_at or now
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO project_life_events (project_id, user_id, event_type, title, impact_json, occurred_at, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (project_id, user_id, event_type, title.strip(), _json(impact), occurred, now),
            )
            row_id = int(cursor.lastrowid)
        for goal_key in impact.get("suggested_goals", [])[:1]:
            if isinstance(goal_key, str):
                self.create_project_goal(project_id=project_id, goal_key=goal_key, title=f"Objectif suggéré: {goal_key}", priority="high")
        self.refresh_project_intelligence(project_id)
        return self._one_table("project_life_events", row_id)

    def list_life_events(self, project_id: int) -> list[dict[str, object]]:
        return self.all("SELECT * FROM project_life_events WHERE project_id = ? ORDER BY occurred_at DESC", (project_id,))

    def create_project_risk(self, *, project_id: int, risk_key: str, description: str, severity: str = "medium", likelihood: str = "medium") -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO project_risks (project_id, risk_key, description, severity, likelihood, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, 'open', ?, ?)
                """,
                (project_id, risk_key, description.strip(), severity, likelihood, now, now),
            )
            row_id = int(cursor.lastrowid)
        self.refresh_project_intelligence(project_id)
        return self._one_table("project_risks", row_id)

    def list_project_risks(self, project_id: int) -> list[dict[str, object]]:
        return self.all("SELECT * FROM project_risks WHERE project_id = ? ORDER BY id ASC", (project_id,))

    def create_project_opportunity(self, *, project_id: int, opportunity_key: str, description: str, value_score: int = 50) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO project_opportunities (project_id, opportunity_key, description, value_score, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, 'open', ?, ?)
                """,
                (project_id, opportunity_key, description.strip(), value_score, now, now),
            )
            row_id = int(cursor.lastrowid)
        self.refresh_project_intelligence(project_id)
        return self._one_table("project_opportunities", row_id)

    def list_project_opportunities(self, project_id: int) -> list[dict[str, object]]:
        return self.all("SELECT * FROM project_opportunities WHERE project_id = ? ORDER BY value_score DESC", (project_id,))

    def create_decision(self, *, project_id: int, payload: dict[str, object]) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO project_decisions (
                    project_id, decision_key, title, status, reason, confidence,
                    alternatives_json, tradeoffs_json, next_action, created_at, updated_at
                ) VALUES (?, ?, ?, 'proposed', ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    project_id,
                    payload["decision_key"],
                    payload["title"],
                    payload["reason"],
                    payload["confidence"],
                    _json(payload.get("alternatives", [])),
                    _json(payload.get("tradeoffs", [])),
                    payload.get("next_action"),
                    now,
                    now,
                ),
            )
            row_id = int(cursor.lastrowid)
        self.record_event("project_decision_created", {"project_id": project_id, "decision_id": row_id})
        return self._one_table("project_decisions", row_id)

    def list_project_decisions(self, project_id: int) -> list[dict[str, object]]:
        return self.all("SELECT * FROM project_decisions WHERE project_id = ? ORDER BY created_at DESC", (project_id,))

    def create_recommendation_row(self, *, project_id: int, payload: dict[str, object]) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO project_recommendations (
                    project_id, recommendation_key, title, priority, confidence, score, reasons_json, status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, 'active', ?, ?)
                """,
                (
                    project_id,
                    payload["recommendation_key"],
                    payload["title"],
                    payload.get("priority", "normal"),
                    payload.get("confidence", 50),
                    payload.get("score", 50),
                    _json(payload.get("reasons", [])),
                    now,
                    now,
                ),
            )
            row_id = int(cursor.lastrowid)
        return self._one_table("project_recommendations", row_id)

    def list_project_recommendations(self, project_id: int) -> list[dict[str, object]]:
        return self.all(
            "SELECT * FROM project_recommendations WHERE project_id = ? AND status = 'active' ORDER BY score DESC, id DESC",
            (project_id,),
        )

    def create_project_action(self, *, project_id: int, action_key: str, title: str, priority: str = "normal", due_at: str | None = None) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO project_actions (project_id, action_key, title, status, priority, due_at, created_at, updated_at)
                VALUES (?, ?, ?, 'pending', ?, ?, ?, ?)
                """,
                (project_id, action_key, title.strip(), priority, due_at, now, now),
            )
            row_id = int(cursor.lastrowid)
        self.create_timeline_entry(project_id=project_id, entry_type="action", title=title, scheduled_at=due_at)
        return self._one_table("project_actions", row_id)

    def list_project_actions(self, project_id: int) -> list[dict[str, object]]:
        return self.all("SELECT * FROM project_actions WHERE project_id = ? ORDER BY created_at DESC", (project_id,))

    def create_project_task(self, *, project_id: int, title: str, action_id: int | None = None, assignee_user_id: int | None = None, due_at: str | None = None) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO project_tasks (project_id, action_id, title, status, assignee_user_id, due_at, created_at, updated_at)
                VALUES (?, ?, ?, 'todo', ?, ?, ?, ?)
                """,
                (project_id, action_id, title.strip(), assignee_user_id, due_at, now, now),
            )
            row_id = int(cursor.lastrowid)
        return self._one_table("project_tasks", row_id)

    def list_project_tasks(self, project_id: int) -> list[dict[str, object]]:
        return self.all("SELECT * FROM project_tasks WHERE project_id = ? ORDER BY created_at DESC", (project_id,))

    def create_knowledge_fact(self, *, project_id: int | None = None, user_id: int | None = None, category: str, fact_key: str, title: str, content: str, source: str = "system", confidence: int = 70, metadata: dict[str, object] | None = None) -> dict[str, object]:
        if category not in KNOWLEDGE_CATEGORIES:
            raise ValidationError(f"unsupported category: {category}")
        now = _utcnow()
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO knowledge_facts (
                    project_id, user_id, category, fact_key, title, content, source, confidence, metadata_json, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (project_id, user_id, category, fact_key, title.strip(), content.strip(), source, confidence, _json(metadata or {}), now, now),
            )
            row_id = int(cursor.lastrowid)
        return self._one_table("knowledge_facts", row_id)

    def list_knowledge_facts(self, *, project_id: int | None = None, category: str | None = None, limit: int = 50) -> list[dict[str, object]]:
        clauses = ["1=1"]
        params: list[object] = []
        if project_id is not None:
            clauses.append("project_id = ?")
            params.append(project_id)
        if category:
            clauses.append("category = ?")
            params.append(category)
        where = " AND ".join(clauses)
        return self.all(f"SELECT * FROM knowledge_facts WHERE {where} ORDER BY id DESC LIMIT ?", tuple(params + [limit]))

    def upsert_user_context(self, user_id: int, context: dict[str, object]) -> dict[str, object]:
        now = _utcnow()
        existing = self.one("SELECT * FROM user_contexts WHERE user_id = ? ORDER BY id DESC LIMIT 1", (user_id,))
        if existing is None:
            with self._transaction() as conn:
                cursor = conn.execute(
                    "INSERT INTO user_contexts (user_id, context_json, version, created_at, updated_at) VALUES (?, ?, 1, ?, ?)",
                    (user_id, _json(context), now, now),
                )
                row_id = int(cursor.lastrowid)
            return self._one_table("user_contexts", row_id)
        version = int(existing.get("version", 1)) + 1
        with self._transaction() as conn:
            conn.execute(
                "UPDATE user_contexts SET context_json = ?, version = ?, updated_at = ? WHERE id = ?",
                (_json(context), version, now, existing["id"]),
            )
        return self._one_table("user_contexts", int(existing["id"]))

    def get_user_context(self, user_id: int) -> dict[str, object] | None:
        return self.one("SELECT * FROM user_contexts WHERE user_id = ? ORDER BY id DESC LIMIT 1", (user_id,))

    def upsert_project_context(self, project_id: int, context: dict[str, object]) -> dict[str, object]:
        now = _utcnow()
        existing = self.one("SELECT * FROM project_contexts WHERE project_id = ? ORDER BY id DESC LIMIT 1", (project_id,))
        if existing is None:
            with self._transaction() as conn:
                cursor = conn.execute(
                    "INSERT INTO project_contexts (project_id, context_json, version, created_at, updated_at) VALUES (?, ?, 1, ?, ?)",
                    (project_id, _json(context), now, now),
                )
                row_id = int(cursor.lastrowid)
            return self._one_table("project_contexts", row_id)
        version = int(existing.get("version", 1)) + 1
        with self._transaction() as conn:
            conn.execute(
                "UPDATE project_contexts SET context_json = ?, version = ?, updated_at = ? WHERE id = ?",
                (_json(context), version, now, existing["id"]),
            )
        return self._one_table("project_contexts", int(existing["id"]))

    def get_project_context(self, project_id: int) -> dict[str, object] | None:
        return self.one("SELECT * FROM project_contexts WHERE project_id = ? ORDER BY id DESC LIMIT 1", (project_id,))

    def create_timeline_entry(self, *, project_id: int, entry_type: str, title: str, description: str | None = None, scheduled_at: str | None = None, occurred_at: str | None = None, metadata: dict[str, object] | None = None) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO timeline_entries (project_id, entry_type, title, description, status, scheduled_at, occurred_at, metadata_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    project_id,
                    entry_type,
                    title.strip(),
                    description,
                    "done" if occurred_at else "planned",
                    scheduled_at,
                    occurred_at,
                    _json(metadata or {}),
                    now,
                ),
            )
            row_id = int(cursor.lastrowid)
        return self._one_table("timeline_entries", row_id)

    def list_timeline_entries(self, project_id: int) -> list[dict[str, object]]:
        return self.all("SELECT * FROM timeline_entries WHERE project_id = ? ORDER BY COALESCE(occurred_at, scheduled_at, created_at) DESC", (project_id,))

    def capture_progress_snapshot(self, project_id: int, *, metrics: dict[str, object] | None = None) -> dict[str, object]:
        project = self.get_project(project_id)
        now = _utcnow()
        progress = int(project.get("progress_percent") or 0)
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO progress_snapshots (project_id, progress_percent, metrics_json, captured_at, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (project_id, progress, _json(metrics or {}), now, now),
            )
            row_id = int(cursor.lastrowid)
        return self._one_table("progress_snapshots", row_id)

    def list_progress_snapshots(self, project_id: int, *, limit: int = 20) -> list[dict[str, object]]:
        return self.all(
            "SELECT * FROM progress_snapshots WHERE project_id = ? ORDER BY captured_at DESC LIMIT ?",
            (project_id, limit),
        )

    def link_project_resource(self, *, project_id: int, resource_type: str, resource_id: int, role: str = "linked") -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT OR IGNORE INTO project_resources (project_id, resource_type, resource_id, role, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (project_id, resource_type, resource_id, role, now),
            )
            if cursor.lastrowid:
                row_id = int(cursor.lastrowid)
            else:
                row = self.one(
                    "SELECT id FROM project_resources WHERE project_id = ? AND resource_type = ? AND resource_id = ?",
                    (project_id, resource_type, resource_id),
                )
                row_id = int(row["id"]) if row else 0
        row = self.one("SELECT * FROM project_resources WHERE id = ?", (row_id,))
        assert row is not None
        return row

    def list_project_resources(self, project_id: int) -> list[dict[str, object]]:
        return self.all("SELECT * FROM project_resources WHERE project_id = ? ORDER BY id ASC", (project_id,))

    def compute_trust_score(self, *, subject_type: str, subject_id: int, factors: list[dict[str, object]]) -> dict[str, object]:
        base = 50
        score = base + sum(int(f.get("weight", 0)) for f in factors)
        score = max(0, min(100, score))
        now = _utcnow()
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO trust_scores (subject_type, subject_id, score, factors_json, computed_at, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (subject_type, subject_id, score, _json(factors), now, now),
            )
            row_id = int(cursor.lastrowid)
        return self._one_table("trust_scores", row_id)

    def get_trust_score(self, *, subject_type: str, subject_id: int) -> dict[str, object] | None:
        return self.one(
            "SELECT * FROM trust_scores WHERE subject_type = ? AND subject_id = ? ORDER BY computed_at DESC LIMIT 1",
            (subject_type, subject_id),
        )

    def refresh_project_intelligence(self, project_id: int) -> dict[str, object]:
        project = self.get_project(project_id)
        goals = self.list_project_goals(project_id)
        risks = self.list_project_risks(project_id)
        opportunities = self.list_project_opportunities(project_id)
        constraints = self.list_project_constraints(project_id)
        actions = self.list_project_actions(project_id)
        funding = self.list_project_funding(project_id)
        steps = self.list_project_steps(project_id)
        decision_engine = DecisionEngine()
        decision_payload = decision_engine.evaluate(
            project=project,
            goals=goals,
            risks=risks,
            opportunities=opportunities,
            constraints=constraints,
        )
        decision = self.create_decision(project_id=project_id, payload=decision_payload)
        goal_engine = GoalEngine()
        recommendations = RecommendationEngine().generate(
            project=project,
            goals=goals,
            decision=decision_payload,
            goal_engine=goal_engine,
        )
        stored_recommendations = [self.create_recommendation_row(project_id=project_id, payload=row) for row in recommendations]
        influence = goal_engine.influence(str(goals[0]["goal_key"]) if goals else str(project.get("project_type", "other")))
        with self._transaction() as conn:
            conn.execute("UPDATE partner_suggestions SET status='expired' WHERE project_id=? AND status='active'", (project_id,))
            conn.execute("UPDATE service_suggestions SET status='expired' WHERE project_id=? AND status='active'", (project_id,))
        partners = [
            self._create_partner_suggestion(project_id, kind, goal_engine)
            for kind in influence["partner_kinds"][:2]
        ]
        services = [
            self._create_service_suggestion(project_id, key)
            for key in influence["service_keys"][:2]
        ]
        intelligence = ProjectIntelligenceEngine().analyze(
            project=project,
            steps=steps,
            risks=risks,
            opportunities=opportunities,
            actions=actions,
            funding=funding,
        )
        trust = self.compute_trust_score(
            subject_type="project",
            subject_id=project_id,
            factors=[
                {"code": "progress", "label": "Progression", "weight": intelligence["progress_percent"] // 5},
                {"code": "risk_penalty", "label": "Risques", "weight": -intelligence["blockers"]["open_high_risks"] * 5},
            ],
        )
        snapshot = self.capture_progress_snapshot(project_id, metrics=intelligence)
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                "UPDATE projects SET intelligence_json = ?, updated_at = ? WHERE id = ?",
                (_json(intelligence), now, project_id),
            )
        return {
            "decision": decision,
            "recommendations": stored_recommendations,
            "partner_suggestions": partners,
            "service_suggestions": services,
            "intelligence": intelligence,
            "trust_score": trust,
            "progress_snapshot": snapshot,
        }

    def _create_partner_suggestion(self, project_id: int, partner_kind: str, goal_engine: GoalEngine) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO partner_suggestions (project_id, partner_kind, title, rationale, priority, confidence, status, created_at)
                VALUES (?, ?, ?, ?, 'normal', 60, 'active', ?)
                """,
                (project_id, partner_kind, f"Partenaire {partner_kind}", f"Recommandé pour le parcours projet", now),
            )
            row_id = int(cursor.lastrowid)
        return self._one_table("partner_suggestions", row_id)

    def _create_service_suggestion(self, project_id: int, service_key: str) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO service_suggestions (project_id, service_key, title, rationale, priority, confidence, status, created_at)
                VALUES (?, ?, ?, ?, 'normal', 60, 'active', ?)
                """,
                (project_id, service_key, service_key.replace("_", " ").title(), "Service aligné au projet", now),
            )
            row_id = int(cursor.lastrowid)
        return self._one_table("service_suggestions", row_id)

    def list_partner_suggestions(self, project_id: int) -> list[dict[str, object]]:
        return self.all("SELECT * FROM partner_suggestions WHERE project_id = ? AND status = 'active' ORDER BY id DESC", (project_id,))

    def list_service_suggestions(self, project_id: int) -> list[dict[str, object]]:
        return self.all("SELECT * FROM service_suggestions WHERE project_id = ? AND status = 'active' ORDER BY id DESC", (project_id,))

    def get_project_workspace(self, project_id: int) -> dict[str, object]:
        project = self.get_project(project_id)
        journey_state = self.journey_engine_state(project_id)
        timeline_engine = TimelineEngine()
        timeline = timeline_engine.build_timeline(
            history=self.list_project_step_history(project_id),
            entries=self.list_timeline_entries(project_id),
            actions=self.list_project_actions(project_id),
            milestones=self.all("SELECT * FROM project_milestones WHERE project_id = ? ORDER BY id ASC", (project_id,)),
        )
        intelligence_json = project.get("intelligence_json") or "{}"
        try:
            intelligence = json.loads(str(intelligence_json))
        except json.JSONDecodeError:
            intelligence = {}
        return {
            "project": project,
            "journey": self.get_journey(project_id),
            "journey_state": journey_state,
            "goals": self.list_project_goals(project_id),
            "needs": self.list_project_needs(project_id),
            "constraints": self.list_project_constraints(project_id),
            "preferences": self.list_project_preferences(project_id),
            "funding": self.list_project_funding(project_id),
            "life_events": self.list_life_events(project_id),
            "risks": self.list_project_risks(project_id),
            "opportunities": self.list_project_opportunities(project_id),
            "decisions": self.list_project_decisions(project_id),
            "recommendations": self.list_project_recommendations(project_id),
            "actions": self.list_project_actions(project_id),
            "tasks": self.list_project_tasks(project_id),
            "knowledge": self.list_knowledge_facts(project_id=project_id),
            "timeline": timeline,
            "intelligence": intelligence,
            "trust_score": self.get_trust_score(subject_type="project", subject_id=project_id),
            "resources": self.list_project_resources(project_id),
            "partner_suggestions": self.list_partner_suggestions(project_id),
            "service_suggestions": self.list_service_suggestions(project_id),
            "progress_snapshots": self.list_progress_snapshots(project_id),
            "steps": self.list_project_steps(project_id),
            "progress": self.project_progress_payload(project_id),
        }

    def _one_table(self, table: str, row_id: int) -> dict[str, object]:
        if table not in V7_TABLE_NAMES and table not in {"project_goals", "project_needs"}:
            pass
        row = self.one(f"SELECT * FROM {table} WHERE id = ?", (row_id,))
        if row is None:
            raise NotFoundError(f"{table} row not found: {row_id}")
        return row

    def intelligent_tables_present(self) -> bool:
        return table_exists(self, "journeys")
