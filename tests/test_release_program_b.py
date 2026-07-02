from __future__ import annotations

from http import HTTPStatus

from lawim_v2.ecosystem.constants import PARTNER_TYPES, SERVICE_CATEGORIES, WORKFLOW_TYPES
from lawim_v2.ecosystem.engines import (
    MatchingEngine2,
    NotificationEventEngine,
    ResourceOrchestrationEngine,
    TrustReputationEngine,
    WorkflowEngine,
    normalize_partner_type,
)
from lawim_v2.schema_migrations import apply_sqlite_legacy_migrations

from tests.lawim_harness import LawimTestHarness


class ReleaseProgramBPersistenceTests(LawimTestHarness):
    def test_schema_version_is_v10(self) -> None:
        self.assertEqual(self.repository.schema_version(), 18)

    def test_ecosystem_tables_present(self) -> None:
        self.assertTrue(self.repository.ecosystem_tables_present())

    def test_demo_seed_has_partners_and_services(self) -> None:
        self.assertGreaterEqual(self.repository.scalar("SELECT COUNT(*) FROM partner_profiles"), 1)
        self.assertGreaterEqual(self.repository.scalar("SELECT COUNT(*) FROM service_catalog"), 8)
        self.assertGreaterEqual(self.repository.scalar("SELECT COUNT(*) FROM workflows"), 8)

    def test_v7_to_v8_legacy_migration(self) -> None:
        import sqlite3
        import tempfile
        from pathlib import Path

        from lawim_v2.ecosystem.schema_v8_ddl import V8_TABLE_NAMES
        from lawim_v2.schema_ddl import SQLITE_INIT_SCRIPT

        db_path = Path(tempfile.mkdtemp()) / "v7.sqlite3"
        conn = sqlite3.connect(db_path)
        conn.executescript(SQLITE_INIT_SCRIPT)
        conn.execute("PRAGMA foreign_keys = OFF")
        for table in V8_TABLE_NAMES:
            conn.execute(f"DROP TABLE IF EXISTS {table}")
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("UPDATE schema_meta SET value='7' WHERE key='schema_version'")
        apply_sqlite_legacy_migrations(conn)
        names = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        conn.close()
        self.assertIn("partner_profiles", names)
        self.assertIn("service_catalog", names)


class ReleaseProgramBEngineTests(LawimTestHarness):
    def test_normalize_partner_type_alias(self) -> None:
        self.assertEqual(normalize_partner_type("agent"), "real_estate_agency")

    def test_matching_engine_returns_partners_and_services(self) -> None:
        engine = MatchingEngine2()
        result = engine.match(
            project={"project_type": "buy", "location_city": "Douala", "budget_max": 500000, "status": "active"},
            goals=[{"goal_key": "buy"}],
            constraints=[],
            journey_state={"status": "active", "blocked_steps": 0},
            partners=[
                {
                    "id": 1,
                    "organization_id": 1,
                    "partner_type": "real_estate_agency",
                    "display_name": "Agency",
                    "status": "active",
                    "quality_score": 80,
                    "trust_score": 75,
                    "completion_rate": 0.9,
                    "zones": [{"city": "Douala", "region": "Littoral"}],
                    "availability_status": "available",
                }
            ],
            services=[
                {
                    "id": 1,
                    "service_key": "property_search",
                    "title": "Search",
                    "status": "active",
                    "indicative_price_max": 100000,
                    "estimated_duration_days": 7,
                }
            ],
        )
        self.assertGreaterEqual(len(result["partner_matches"]), 1)
        self.assertGreaterEqual(len(result["service_matches"]), 1)

    def test_trust_reputation_engine(self) -> None:
        metrics = TrustReputationEngine().compute(
            profile={"quality_score": 70, "trust_score": 70, "reliability_score": 75, "response_time_hours": 12, "satisfaction_score": 80},
            orders=[{"status": "completed"}, {"status": "requested"}],
            incidents=0,
        )
        self.assertIn("trust_score", metrics)
        self.assertGreater(metrics["completion_rate"], 0)

    def test_workflow_engine_template_buy(self) -> None:
        steps = WorkflowEngine().template_for("buy")
        self.assertGreaterEqual(len(steps), 3)

    def test_workflow_resolve_type_build(self) -> None:
        wf_type = WorkflowEngine().resolve_workflow_type({"project_type": "build"}, [])
        self.assertEqual(wf_type, "build")

    def test_notification_event_engine_channels(self) -> None:
        notifications = NotificationEventEngine().build_notifications(
            event={"id": 1, "event_type": "match_refreshed", "title": "Match", "project_id": 1, "payload_json": "{}"},
            user_id=1,
            channels=("in_app", "email"),
        )
        self.assertEqual(len(notifications), 2)
        channels = {n["channel"] for n in notifications}
        self.assertIn("email", channels)

    def test_resource_orchestration_assemble(self) -> None:
        view = ResourceOrchestrationEngine().assemble(
            project={"id": 1, "currency": "XAF"},
            partner_matches=[{"partner_profile_id": 1, "confidence": 80}],
            service_matches=[{"service_catalog_id": 1, "confidence": 70}],
            orders=[{"status": "requested", "cost_estimate": 100000}],
            interventions=[{"title": "Visit", "status": "planned", "scheduled_at": "2026-07-01"}],
            resources=[{"resource_type": "property"}],
            workflow_instance={"id": 1, "status": "active", "current_step_key": "search"},
            workflow_steps=[{"status": "pending"}, {"status": "completed"}],
        )
        self.assertIn("cost_summary", view)
        self.assertEqual(view["resources_linked"], 1)


class ReleaseProgramBRepositoryTests(LawimTestHarness):
    def test_list_partner_profiles(self) -> None:
        payload = self.repository.list_partner_profiles(limit=10)
        self.assertGreaterEqual(len(payload["partners"]), 1)

    def test_list_service_catalog(self) -> None:
        payload = self.repository.list_service_catalog(limit=20)
        self.assertGreaterEqual(len(payload["services"]), 8)

    def test_run_project_matching_persists_results(self) -> None:
        project = self.repository.one("SELECT id FROM projects ORDER BY id ASC LIMIT 1")
        project_id = int(project["id"])
        self.repository.run_project_matching(project_id)
        matches = self.repository.list_project_matches(project_id)
        self.assertGreaterEqual(len(matches), 1)

    def test_ensure_project_workflow(self) -> None:
        project = self.repository.one("SELECT id FROM projects ORDER BY id ASC LIMIT 1")
        instance = self.repository.ensure_project_workflow(int(project["id"]))
        self.assertIn("instance_steps", instance)

    def test_compute_partner_reputation(self) -> None:
        partner = self.repository.one("SELECT id FROM partner_profiles LIMIT 1")
        metrics = self.repository.compute_partner_reputation(int(partner["id"]))
        self.assertIn("trust_score", metrics)

    def test_get_project_orchestration(self) -> None:
        project = self.repository.one("SELECT id FROM projects ORDER BY id ASC LIMIT 1")
        view = self.repository.get_project_orchestration(int(project["id"]))
        self.assertIn("cost_summary", view)


class ReleaseProgramBApiTests(LawimTestHarness):
    def _project_id(self, token: str) -> int:
        listing = self.invoke("/api/v2/projects", token=token)
        if listing.body_json()["projects"]:
            return int(listing.body_json()["projects"][0]["id"])
        created = self.invoke(
            "/api/v2/projects",
            method="POST",
            token=token,
            body={"title": "Eco", "project_type": "buy", "objective": "Test", "budget_min": 1, "budget_max": 2},
        )
        return int(created.body_json()["project"]["id"])

    def test_list_partners_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/partners", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertGreaterEqual(len(response.body_json()["partners"]), 1)

    def test_get_partner_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        listing = self.invoke("/api/v2/partners", token=token)
        partner_id = listing.body_json()["partners"][0]["id"]
        detail = self.invoke(f"/api/v2/partners/{partner_id}", token=token)
        self.assertEqual(detail.status, HTTPStatus.OK)

    def test_list_services_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/services", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertGreaterEqual(len(response.body_json()["services"]), 8)

    def test_get_service_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        listing = self.invoke("/api/v2/services", token=token)
        service_id = listing.body_json()["services"][0]["id"]
        detail = self.invoke(f"/api/v2/services/{service_id}", token=token)
        self.assertEqual(detail.status, HTTPStatus.OK)

    def test_list_workflows_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/workflows", token=token)
        self.assertGreaterEqual(len(response.body_json()["workflows"]), 8)

    def test_project_workflow_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._project_id(token)
        response = self.invoke(f"/api/v2/projects/{project_id}/workflows", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("workflow_instance", response.body_json())

    def test_matching_list_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._project_id(token)
        response = self.invoke(f"/api/v2/matching?project_id={project_id}", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_matching_run_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._project_id(token)
        response = self.invoke(f"/api/v2/projects/{project_id}/matching/run", method="POST", token=token, body={})
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("matching", response.body_json())

    def test_reputation_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        partner = self.invoke("/api/v2/partners", token=token).body_json()["partners"][0]
        response = self.invoke(
            f"/api/v2/reputation?subject_type=partner&subject_id={partner['id']}",
            token=token,
        )
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("reputation", response.body_json())

    def test_ecosystem_notifications_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._project_id(token)
        self.invoke(f"/api/v2/projects/{project_id}/matching/run", method="POST", token=token, body={})
        response = self.invoke("/api/v2/notifications/ecosystem", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_resources_ecosystem_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._project_id(token)
        response = self.invoke(f"/api/v2/resources?project_id={project_id}", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("matches", response.body_json())

    def test_orchestration_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._project_id(token)
        response = self.invoke(f"/api/v2/projects/{project_id}/orchestration", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("orchestration", response.body_json())

    def test_create_partner_requires_admin(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke(
            "/api/v2/partners",
            method="POST",
            token=token,
            body={
                "organization_id": 1,
                "partner_type": "notary",
                "display_name": "Denied",
            },
        )
        self.assertEqual(response.status, HTTPStatus.FORBIDDEN)

    def test_create_partner_admin(self) -> None:
        admin = self.login(email="admin@lawim.local")
        response = self.invoke(
            "/api/v2/partners",
            method="POST",
            token=admin,
            body={
                "organization_id": 1,
                "partner_type": "surveyor",
                "display_name": "Admin Surveyor",
                "city": "Douala",
            },
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_matching_forbidden_cross_user(self) -> None:
        agent = self.login(email="agent@lawim.local")
        owner = self.register(email="eco-owner@example.local", full_name="Eco Owner")
        project_id = self._project_id(agent)
        denied = self.invoke(f"/api/v2/projects/{project_id}/matching/run", method="POST", token=owner, body={})
        self.assertEqual(denied.status, HTTPStatus.FORBIDDEN)

    def test_services_filter_category(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/services?category=legal", token=token)
        self.assertTrue(all(s["category"] == "legal" for s in response.body_json()["services"]))

    def test_partners_filter_type(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/partners?partner_type=real_estate_agency", token=token)
        self.assertTrue(all(p["partner_type"] == "real_estate_agency" for p in response.body_json()["partners"]))

    def test_metrics_include_ecosystem_counters(self) -> None:
        admin = self.login(email="admin@lawim.local")
        agent = self.login(email="agent@lawim.local")
        self.invoke("/api/v2/partners", token=agent)
        metrics = self.invoke("/api/metrics", token=admin)
        snapshot = metrics.body_json()["metrics"]
        self.assertIn("ecosystem_partners_total", snapshot)


class ReleaseProgramBConstantsTests(LawimTestHarness):
    def test_partner_types_count(self) -> None:
        self.assertGreaterEqual(len(PARTNER_TYPES), 15)

    def test_service_categories(self) -> None:
        for cat in ("acquisition", "legal", "financing"):
            self.assertIn(cat, SERVICE_CATEGORIES)

    def test_workflow_types(self) -> None:
        for wf in ("buy", "sell", "rent", "build"):
            self.assertIn(wf, WORKFLOW_TYPES)

    def test_all_partner_types_valid(self) -> None:
        for partner_type in (
            "real_estate_agency",
            "notary",
            "bank",
            "architect",
            "construction_company",
        ):
            self.assertIn(partner_type, PARTNER_TYPES)


class ReleaseProgramBMatchingDeepTests(LawimTestHarness):
    def test_matching_scores_ordered(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = ReleaseProgramBApiTests._project_id(self, token)
        self.invoke(f"/api/v2/projects/{project_id}/matching/run", method="POST", token=token, body={})
        matches = self.invoke(f"/api/v2/matching?project_id={project_id}", token=token).body_json()["matches"]
        partner_scores = [m["score"] for m in matches if m["match_type"] == "partner"]
        service_scores = [m["score"] for m in matches if m["match_type"] == "service"]
        if partner_scores:
            self.assertEqual(partner_scores, sorted(partner_scores, reverse=True))
        if service_scores:
            self.assertEqual(service_scores, sorted(service_scores, reverse=True))

    def test_matching_includes_rationale(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = ReleaseProgramBApiTests._project_id(self, token)
        matches = self.invoke(f"/api/v2/matching?project_id={project_id}", token=token).body_json()["matches"]
        self.assertTrue(any(m.get("rationale") for m in matches))

    def test_new_project_bootstraps_ecosystem(self) -> None:
        token = self.login(email="agent@lawim.local")
        created = self.invoke(
            "/api/v2/projects",
            method="POST",
            token=token,
            body={
                "title": "Bootstrap Eco",
                "project_type": "rent",
                "objective": "Location",
                "location_city": "Douala",
                "budget_min": 100000,
                "budget_max": 200000,
            },
        )
        project_id = int(created.body_json()["project"]["id"])
        workflow = self.invoke(f"/api/v2/projects/{project_id}/workflows", token=token)
        self.assertEqual(workflow.status, HTTPStatus.OK)
        matches = self.invoke(f"/api/v2/matching?project_id={project_id}", token=token)
        self.assertGreaterEqual(len(matches.body_json()["matches"]), 1)


class ReleaseProgramBWorkflowTests(LawimTestHarness):
    def test_workflow_instance_has_steps(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = ReleaseProgramBApiTests._project_id(self, token)
        payload = self.invoke(f"/api/v2/projects/{project_id}/workflows", token=token).body_json()
        steps = payload["workflow_instance"]["instance_steps"]
        self.assertGreaterEqual(len(steps), 2)

    def test_workflow_progress_percent(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = ReleaseProgramBApiTests._project_id(self, token)
        payload = self.invoke(f"/api/v2/projects/{project_id}/workflows", token=token).body_json()
        self.assertIn("progress_percent", payload["workflow_instance"])


class ReleaseProgramBUiTests(LawimTestHarness):
    def test_app_js_references_ecosystem_routes(self) -> None:
        js = self.invoke("/app.js")
        text = js.body_text()
        self.assertIn("/api/v2/partners", text)
        self.assertIn("/api/v2/services", text)
        self.assertIn("orchestration", text)

    def test_index_has_ecosystem_section(self) -> None:
        html = self.invoke("/")
        self.assertIn("Ecosystem", html.body_text())


class ReleaseProgramBHealthTests(LawimTestHarness):
    def test_health_schema_v10(self) -> None:
        health = self.invoke("/api/health")
        self.assertEqual(health.body_json()["database"]["schema_version"], 18)

    def test_migration_strategy_v10(self) -> None:
        from lawim_v2.schema_migrations import migration_strategy_profile

        self.assertEqual(migration_strategy_profile()["schema_version"], 18)


class ReleaseProgramBPartnerTypeTests(LawimTestHarness):
    def test_partner_type_real_estate_agency(self) -> None:
        self.assertIn("real_estate_agency", PARTNER_TYPES)

    def test_partner_type_notaire(self) -> None:
        self.assertIn("notary", PARTNER_TYPES)

    def test_partner_type_bank(self) -> None:
        self.assertIn("bank", PARTNER_TYPES)

    def test_partner_type_microfinance(self) -> None:
        self.assertIn("microfinance", PARTNER_TYPES)

    def test_partner_type_surveyor(self) -> None:
        self.assertIn("surveyor", PARTNER_TYPES)

    def test_partner_type_architect(self) -> None:
        self.assertIn("architect", PARTNER_TYPES)

    def test_partner_type_construction(self) -> None:
        self.assertIn("construction_company", PARTNER_TYPES)

    def test_partner_type_mover(self) -> None:
        self.assertIn("mover", PARTNER_TYPES)

    def test_partner_type_insurer(self) -> None:
        self.assertIn("insurer", PARTNER_TYPES)

    def test_partner_type_administration(self) -> None:
        self.assertIn("administration", PARTNER_TYPES)


class ReleaseProgramBServiceCatalogTests(LawimTestHarness):
    def test_service_category_acquisition(self) -> None:
        self.assertIn("acquisition", SERVICE_CATEGORIES)

    def test_service_category_rental(self) -> None:
        self.assertIn("rental", SERVICE_CATEGORIES)

    def test_service_category_construction(self) -> None:
        self.assertIn("construction", SERVICE_CATEGORIES)

    def test_service_category_moving(self) -> None:
        self.assertIn("moving", SERVICE_CATEGORIES)

    def test_catalog_has_property_search(self) -> None:
        row = self.repository.one("SELECT * FROM service_catalog WHERE service_key = 'property_search'")
        self.assertIsNotNone(row)

    def test_catalog_has_financing(self) -> None:
        row = self.repository.one("SELECT * FROM service_catalog WHERE service_key = 'financing_prequalification'")
        self.assertIsNotNone(row)


class ReleaseProgramBWorkflowTypeTests(LawimTestHarness):
    def test_workflow_buy_exists(self) -> None:
        row = self.repository.one("SELECT * FROM workflows WHERE workflow_key = 'workflow-buy'")
        self.assertIsNotNone(row)

    def test_workflow_sell_exists(self) -> None:
        row = self.repository.one("SELECT * FROM workflows WHERE workflow_key = 'workflow-sell'")
        self.assertIsNotNone(row)

    def test_workflow_finance_exists(self) -> None:
        row = self.repository.one("SELECT * FROM workflows WHERE workflow_key = 'workflow-finance'")
        self.assertIsNotNone(row)

    def test_workflow_succession_exists(self) -> None:
        row = self.repository.one("SELECT * FROM workflows WHERE workflow_key = 'workflow-succession'")
        self.assertIsNotNone(row)


class ReleaseProgramBEcosystemIntegrationTests(LawimTestHarness):
    def test_post_matching_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = ReleaseProgramBApiTests._project_id(self, token)
        response = self.invoke("/api/v2/matching", method="POST", token=token, body={"project_id": project_id})
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_project_matching_endpoint(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = ReleaseProgramBApiTests._project_id(self, token)
        response = self.invoke(f"/api/v2/projects/{project_id}/matching", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_ecosystem_events_after_matching(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = ReleaseProgramBApiTests._project_id(self, token)
        self.invoke(f"/api/v2/projects/{project_id}/matching/run", method="POST", token=token, body={})
        events = self.repository.list_ecosystem_events(project_id=project_id, limit=5)
        self.assertGreaterEqual(len(events), 1)

    def test_partner_has_zones(self) -> None:
        partner = self.repository.get_partner_profile(
            int(self.repository.one("SELECT id FROM partner_profiles LIMIT 1")["id"])
        )
        self.assertGreaterEqual(len(partner["zones"]), 1)

    def test_orchestration_includes_workflow(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = ReleaseProgramBApiTests._project_id(self, token)
        orch = self.invoke(f"/api/v2/projects/{project_id}/orchestration", token=token).body_json()["orchestration"]
        self.assertIn("workflow", orch)
