from __future__ import annotations

from http import HTTPStatus

from lawim_v2.intelligent.constants import GOAL_KEYS, LIFE_EVENT_TYPES
from lawim_v2.intelligent.engines import DecisionEngine, GoalEngine, JourneyEngine, LifeEventEngine, RecommendationEngine
from lawim_v2.schema_migrations import apply_sqlite_legacy_migrations

from tests.lawim_harness import LawimTestHarness


class ReleaseProgramAEngineTests(LawimTestHarness):
    def test_goal_engine_influence_buy(self) -> None:
        influence = GoalEngine().influence("buy")
        self.assertIn("search", influence["journey_steps"])
        self.assertIn("agent", influence["partner_kinds"])

    def test_decision_engine_produces_confidence(self) -> None:
        decision = DecisionEngine().evaluate(
            project={"project_type": "buy", "budget_min": None, "budget_max": None},
            goals=[{"goal_key": "buy"}],
            risks=[{"severity": "high", "status": "open"}],
            opportunities=[],
            constraints=[],
        )
        self.assertIn("confidence", decision)
        self.assertTrue(decision["alternatives"])

    def test_life_event_engine_suggests_goals(self) -> None:
        impact = LifeEventEngine().impact("marriage")
        self.assertIn("house_family", impact["suggested_goals"])

    def test_journey_engine_blocked_status(self) -> None:
        state = JourneyEngine().compute_state(
            project={"status": "active"},
            journey={"id": 1, "status": "active"},
            steps=[{"status": "blocked", "position": 0, "step_key": "a", "title": "A", "next_action": "x"}],
        )
        self.assertEqual(state["status"], "blocked")

    def test_recommendation_engine_generates_items(self) -> None:
        recs = RecommendationEngine().generate(
            project={"project_type": "buy"},
            goals=[{"goal_key": "buy"}],
            decision={"decision_key": "d1", "next_action": "Act", "reason": "R", "confidence": 70},
            goal_engine=GoalEngine(),
        )
        self.assertGreaterEqual(len(recs), 2)


class ReleaseProgramAPersistenceTests(LawimTestHarness):
    def test_schema_version_is_v7(self) -> None:
        self.assertEqual(self.repository.schema_version(), 7)

    def test_intelligent_tables_exist(self) -> None:
        self.assertTrue(self.repository.intelligent_tables_present())

    def test_v6_to_v7_legacy_migration(self) -> None:
        import sqlite3
        import tempfile
        from pathlib import Path

        from lawim_v2.schema_ddl import SQLITE_INIT_SCRIPT

        db_path = Path(tempfile.mkdtemp()) / "v6.sqlite3"
        conn = sqlite3.connect(db_path)
        conn.executescript(SQLITE_INIT_SCRIPT)
        conn.execute("PRAGMA foreign_keys = OFF")
        for table in (
            "trust_scores",
            "service_suggestions",
            "partner_suggestions",
            "progress_snapshots",
            "timeline_entries",
            "project_resources",
            "project_milestones",
            "project_tasks",
            "project_actions",
            "project_recommendations",
            "project_decisions",
            "project_opportunities",
            "project_risks",
            "project_life_events",
            "project_funding",
            "project_preferences",
            "project_constraints",
            "project_needs",
            "project_goals",
            "project_contexts",
            "user_contexts",
            "knowledge_facts",
            "journeys",
        ):
            conn.execute(f"DROP TABLE IF EXISTS {table}")
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("UPDATE schema_meta SET value='6' WHERE key='schema_version'")
        apply_sqlite_legacy_migrations(conn)
        names = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        conn.close()
        self.assertIn("journeys", names)
        self.assertIn("project_decisions", names)


class ReleaseProgramAApiTests(LawimTestHarness):
    def _create_project(self, token: str) -> int:
        response = self.invoke(
            "/api/v2/projects",
            method="POST",
            token=token,
            body={"title": "Core Platform Project", "project_type": "buy", "objective": "Acheter", "budget_min": 100000, "budget_max": 300000},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)
        return int(response.body_json()["project"]["id"])

    def test_workspace_endpoint(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._create_project(token)
        response = self.invoke(f"/api/v2/projects/{project_id}/workspace", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        workspace = response.body_json()["workspace"]
        self.assertIn("goals", workspace)
        self.assertIn("intelligence", workspace)
        self.assertIn("recommendations", workspace)
        self.assertIn("timeline", workspace)

    def test_goals_list_and_create(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._create_project(token)
        listing = self.invoke(f"/api/v2/projects/{project_id}/goals", token=token)
        self.assertGreaterEqual(len(listing.body_json()["goals"]), 1)
        created = self.invoke(
            f"/api/v2/projects/{project_id}/goals",
            method="POST",
            token=token,
            body={"goal_key": "secure_patrimony", "title": "Sécuriser patrimoine"},
        )
        self.assertEqual(created.status, HTTPStatus.CREATED)

    def test_knowledge_crud(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._create_project(token)
        created = self.invoke(
            f"/api/v2/projects/{project_id}/knowledge",
            method="POST",
            token=token,
            body={"category": "market", "fact_key": "douala-prices", "title": "Prix Douala", "content": "Fourchette indicative"},
        )
        self.assertEqual(created.status, HTTPStatus.CREATED)
        listing = self.invoke(f"/api/v2/projects/{project_id}/knowledge", token=token)
        self.assertGreaterEqual(len(listing.body_json()["knowledge"]), 2)

    def test_recommendations_and_decisions(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._create_project(token)
        recs = self.invoke(f"/api/v2/projects/{project_id}/recommendations", token=token)
        self.assertGreaterEqual(len(recs.body_json()["recommendations"]), 1)
        decisions = self.invoke(f"/api/v2/projects/{project_id}/decisions", token=token)
        self.assertGreaterEqual(len(decisions.body_json()["decisions"]), 1)

    def test_actions_and_tasks(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._create_project(token)
        action = self.invoke(
            f"/api/v2/projects/{project_id}/actions",
            method="POST",
            token=token,
            body={"action_key": "visit-plan", "title": "Planifier visite"},
        )
        action_id = action.body_json()["action"]["id"]
        task = self.invoke(
            f"/api/v2/projects/{project_id}/tasks",
            method="POST",
            token=token,
            body={"title": "Appeler agent", "action_id": action_id},
        )
        self.assertEqual(task.status, HTTPStatus.CREATED)

    def test_life_event_updates_project(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._create_project(token)
        response = self.invoke(
            f"/api/v2/projects/{project_id}/life-events",
            method="POST",
            token=token,
            body={"event_type": "relocation", "title": "Mutation professionnelle"},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)
        events = self.invoke(f"/api/v2/projects/{project_id}/life-events", token=token)
        self.assertEqual(len(events.body_json()["life_events"]), 1)

    def test_timeline_endpoint(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._create_project(token)
        timeline = self.invoke(f"/api/v2/projects/{project_id}/timeline", token=token)
        self.assertIn("history", timeline.body_json()["timeline"])

    def test_journey_state_and_replan(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._create_project(token)
        state = self.invoke(f"/api/v2/projects/{project_id}/journey/state", token=token)
        self.assertIn("progress_percent", state.body_json()["journey_state"])
        replan = self.invoke(f"/api/v2/projects/{project_id}/journey/replan", method="POST", token=token, body={})
        self.assertIn("planned_steps", replan.body_json()["replan"])

    def test_intelligence_refresh(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._create_project(token)
        refreshed = self.invoke(f"/api/v2/projects/{project_id}/intelligence/refresh", method="POST", token=token, body={})
        self.assertIn("intelligence", refreshed.body_json()["intelligence"])
        self.assertIn("trust_score", refreshed.body_json()["intelligence"])

    def test_link_property_resource(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._create_project(token)
        props = self.invoke("/api/properties?limit=1", token=token)
        property_id = props.body_json()["properties"][0]["id"]
        linked = self.invoke(
            f"/api/v2/projects/{project_id}/resources",
            method="POST",
            token=token,
            body={"property_id": property_id},
        )
        self.assertEqual(linked.status, HTTPStatus.CREATED)
        resources = self.invoke(f"/api/v2/projects/{project_id}/resources", token=token)
        self.assertEqual(len(resources.body_json()["resources"]), 1)

    def test_workspace_forbidden_cross_user(self) -> None:
        owner = self.register(email="owner-core@example.local", full_name="Owner Core")
        agent = self.login(email="agent@lawim.local")
        project_id = self._create_project(agent)
        denied = self.invoke(f"/api/v2/projects/{project_id}/workspace", token=owner)
        self.assertEqual(denied.status, HTTPStatus.FORBIDDEN)

    def test_demo_seed_has_intelligence(self) -> None:
        token = self.login(email="agent@lawim.local")
        listing = self.invoke("/api/v2/projects", token=token)
        self.assertGreaterEqual(listing.body_json()["pagination"]["total"], 1)
        project_id = listing.body_json()["projects"][0]["id"]
        workspace = self.invoke(f"/api/v2/projects/{project_id}/workspace", token=token)
        self.assertIn("trust_score", workspace.body_json()["workspace"])


class ReleaseProgramAConstantsTests(LawimTestHarness):
    def test_all_goal_keys_valid(self) -> None:
        for key in ("buy", "rent", "invest", "secure_patrimony", "house_family"):
            self.assertIn(key, GOAL_KEYS)

    def test_life_event_types(self) -> None:
        for event in ("marriage", "retirement", "business_creation"):
            self.assertIn(event, LIFE_EVENT_TYPES)


class ReleaseProgramAEngineDeepTests(LawimTestHarness):
    def test_decision_engine_budget_gap_lowers_confidence(self) -> None:
        from lawim_v2.intelligent.engines import DecisionEngine

        with_budget = DecisionEngine().evaluate(
            project={"project_type": "buy", "budget_min": 100000, "budget_max": 200000},
            goals=[{"goal_key": "buy"}],
            risks=[],
            opportunities=[],
            constraints=[],
        )
        without_budget = DecisionEngine().evaluate(
            project={"project_type": "buy", "budget_min": None, "budget_max": None},
            goals=[{"goal_key": "buy"}],
            risks=[],
            opportunities=[],
            constraints=[],
        )
        self.assertGreater(with_budget["confidence"], without_budget["confidence"])

    def test_decision_engine_high_risk_alternatives(self) -> None:
        from lawim_v2.intelligent.engines import DecisionEngine

        decision = DecisionEngine().evaluate(
            project={"project_type": "buy", "budget_min": 1, "budget_max": 2},
            goals=[{"goal_key": "buy"}],
            risks=[{"severity": "high", "status": "open"}],
            opportunities=[],
            constraints=[],
        )
        self.assertTrue(any("risque" in alt.lower() for alt in decision["alternatives"]))

    def test_journey_engine_completed_at_100_percent(self) -> None:
        from lawim_v2.intelligent.engines import JourneyEngine

        state = JourneyEngine().compute_state(
            project={"status": "active"},
            journey={"id": 1, "status": "active"},
            steps=[{"status": "completed", "position": 0, "step_key": "a", "title": "A", "next_action": ""}],
        )
        self.assertEqual(state["status"], "completed")
        self.assertEqual(state["progress_percent"], 100)

    def test_goal_engine_influence_rent(self) -> None:
        influence = GoalEngine().influence("rent")
        self.assertIn("property_search", influence["service_keys"])

    def test_goal_engine_invalid_goal_raises(self) -> None:
        with self.assertRaises(ValueError):
            GoalEngine().normalize_goal("unknown_goal")

    def test_life_event_birth_suggests_family_goal(self) -> None:
        impact = LifeEventEngine().impact("birth")
        self.assertIn("house_family", impact["suggested_goals"])

    def test_life_event_invalid_raises(self) -> None:
        with self.assertRaises(ValueError):
            LifeEventEngine().impact("invalid_event")

    def test_timeline_engine_groups_future_actions(self) -> None:
        from lawim_v2.intelligent.engines import TimelineEngine

        timeline = TimelineEngine().build_timeline(
            history=[{"to_status": "in_progress"}],
            entries=[{"title": "Future visit", "scheduled_at": "2026-12-01", "occurred_at": None}],
            actions=[{"title": "Call agent", "status": "pending"}],
            milestones=[{"title": "Offer accepted"}],
        )
        self.assertIn("history", timeline)
        self.assertEqual(len(timeline["planned_actions"]), 1)
        self.assertEqual(len(timeline["milestones"]), 1)

    def test_project_intelligence_prioritizes_budget(self) -> None:
        from lawim_v2.intelligent.engines import ProjectIntelligenceEngine

        intel = ProjectIntelligenceEngine().analyze(
            project={"status": "active", "budget_max": None},
            steps=[{"status": "pending"}],
            risks=[],
            opportunities=[],
            actions=[],
            funding=[],
        )
        self.assertIn("Qualifier le budget", intel["priorities"])

    def test_project_intelligence_budget_variance(self) -> None:
        from lawim_v2.intelligent.engines import ProjectIntelligenceEngine

        intel = ProjectIntelligenceEngine().analyze(
            project={"status": "active", "budget_max": 100000},
            steps=[],
            risks=[],
            opportunities=[],
            actions=[],
            funding=[{"amount": 120000, "status": "planned"}],
        )
        self.assertEqual(intel["budget"]["variance"], 20000)

    def test_recommendation_includes_services(self) -> None:
        recs = RecommendationEngine().generate(
            project={"project_type": "build"},
            goals=[{"goal_key": "build"}],
            decision=None,
            goal_engine=GoalEngine(),
        )
        keys = {row["recommendation_key"] for row in recs}
        self.assertTrue(any(key.startswith("service-") for key in keys))


class ReleaseProgramARepositoryTests(LawimTestHarness):
    def test_bootstrap_creates_journey_and_goals(self) -> None:
        project = self.repository.create_project(
            title="Repo bootstrap",
            project_type="buy",
            objective="Test",
            user_id=1,
        )
        project_id = int(project["id"])
        goals = self.repository.list_project_goals(project_id)
        journey = self.repository.get_journey(project_id)
        self.assertGreaterEqual(len(goals), 1)
        self.assertIsNotNone(journey)

    def test_refresh_intelligence_updates_decisions(self) -> None:
        project = self.repository.create_project(title="Intel", project_type="rent", objective="Test", user_id=1)
        project_id = int(project["id"])
        before = len(self.repository.list_project_decisions(project_id))
        self.repository.refresh_project_intelligence(project_id)
        after = len(self.repository.list_project_decisions(project_id))
        self.assertGreaterEqual(after, before)

    def test_create_knowledge_fact(self) -> None:
        project = self.repository.create_project(title="Knowledge", project_type="buy", objective="Test", user_id=1)
        fact = self.repository.create_knowledge_fact(
            project_id=int(project["id"]),
            category="legal",
            fact_key="test-fact",
            title="Test fact",
            content="Content",
        )
        self.assertEqual(fact["fact_key"], "test-fact")

    def test_link_project_resource(self) -> None:
        project = self.repository.create_project(title="Resource", project_type="buy", objective="Test", user_id=1)
        props = self.repository.list_properties(limit=1)
        items = props.get("properties") or props.get("items") or []
        self.assertTrue(items)
        resource = self.repository.link_project_resource(
            project_id=int(project["id"]),
            resource_type="property",
            resource_id=int(items[0]["id"]),
            role="candidate",
        )
        self.assertEqual(resource["resource_type"], "property")


class ReleaseProgramAApiExtendedTests(LawimTestHarness):
    def test_projects_pagination(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/projects?page=1&limit=2", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        body = response.body_json()
        self.assertIn("pagination", body)
        self.assertLessEqual(len(body["projects"]), 2)

    def test_projects_filter_by_type(self) -> None:
        token = self.login(email="agent@lawim.local")
        self.invoke(
            "/api/v2/projects",
            method="POST",
            token=token,
            body={"title": "Filter test", "project_type": "invest", "objective": "Yield"},
        )
        filtered = self.invoke("/api/v2/projects?project_type=invest", token=token)
        self.assertTrue(all(row["project_type"] == "invest" for row in filtered.body_json()["projects"]))

    def test_invalid_project_type_rejected(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke(
            "/api/v2/projects",
            method="POST",
            token=token,
            body={"title": "Bad", "project_type": "invalid", "objective": "x"},
        )
        self.assertEqual(response.status, HTTPStatus.BAD_REQUEST)

    def test_global_knowledge_requires_admin(self) -> None:
        token = self.login(email="agent@lawim.local")
        denied = self.invoke("/api/v2/knowledge", token=token)
        self.assertEqual(denied.status, HTTPStatus.FORBIDDEN)

    def test_global_knowledge_admin(self) -> None:
        admin = self.login(email="admin@lawim.local")
        response = self.invoke("/api/v2/knowledge", token=admin)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_list_actions_and_tasks(self) -> None:
        token = self.login(email="agent@lawim.local")
        created = self.invoke(
            "/api/v2/projects",
            method="POST",
            token=token,
            body={"title": "Actions", "project_type": "buy", "objective": "Test"},
        )
        project_id = int(created.body_json()["project"]["id"])
        actions = self.invoke(f"/api/v2/projects/{project_id}/actions", token=token)
        tasks = self.invoke(f"/api/v2/projects/{project_id}/tasks", token=token)
        self.assertEqual(actions.status, HTTPStatus.OK)
        self.assertEqual(tasks.status, HTTPStatus.OK)

    def test_metrics_include_project_counters(self) -> None:
        token = self.login(email="admin@lawim.local")
        agent = self.login(email="agent@lawim.local")
        created = self.invoke(
            "/api/v2/projects",
            method="POST",
            token=agent,
            body={"title": "Metrics", "project_type": "buy", "objective": "Test", "budget_min": 1, "budget_max": 2},
        )
        project_id = int(created.body_json()["project"]["id"])
        self.invoke(f"/api/v2/projects/{project_id}/workspace", token=agent)
        metrics = self.invoke("/api/metrics", token=token)
        snapshot = metrics.body_json()["metrics"]
        self.assertGreaterEqual(snapshot.get("projects_total", 0), 1)
        self.assertGreaterEqual(snapshot.get("intelligent_workspace_total", 0), 1)

    def test_app_js_references_workspace(self) -> None:
        js = self.invoke("/app.js")
        self.assertIn("/workspace", js.body_text())

    def test_migration_strategy_profile_v7(self) -> None:
        from lawim_v2.schema_migrations import migration_strategy_profile

        profile = migration_strategy_profile()
        self.assertEqual(profile["schema_version"], 7)


class ReleaseProgramAHealthTests(LawimTestHarness):
    def test_health_reports_schema_v7(self) -> None:
        health = self.invoke("/api/health")
        self.assertEqual(health.body_json()["database"]["schema_version"], 7)

    def test_summary_includes_projects(self) -> None:
        summary = self.repository.summary()
        self.assertIn("projects", summary)
        self.assertGreaterEqual(summary["projects"], 1)
