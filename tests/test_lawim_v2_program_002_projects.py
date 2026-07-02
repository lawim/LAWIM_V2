from __future__ import annotations

from http import HTTPStatus

from lawim_v2.project_domain import compute_progress, derive_next_actions, journey_templates
from lawim_v2.schema_migrations import apply_sqlite_legacy_migrations

from tests.lawim_harness import LawimTestHarness


class Program002ProjectTests(LawimTestHarness):
    def test_schema_version_is_v6(self) -> None:
        self.assertEqual(self.repository.schema_version(), 18)

    def test_legacy_migration_adds_project_tables(self) -> None:
        import sqlite3
        import tempfile
        from pathlib import Path

        from lawim_v2.ecosystem.schema_v8_ddl import V8_TABLE_NAMES
        from lawim_v2.schema_ddl import SQLITE_INIT_SCRIPT

        db_path = Path(tempfile.mkdtemp()) / "legacy.sqlite3"
        conn = sqlite3.connect(db_path)
        conn.executescript(SQLITE_INIT_SCRIPT)
        conn.execute("PRAGMA foreign_keys = OFF")
        for table in (
            *V8_TABLE_NAMES,
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
            "project_step_history",
            "project_checklist_items",
            "project_steps",
            "projects",
        ):
            conn.execute(f"DROP TABLE IF EXISTS {table}")
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("INSERT OR REPLACE INTO schema_meta (key, value) VALUES ('schema_version', '5')")
        apply_sqlite_legacy_migrations(conn)
        tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        conn.close()
        self.assertIn("projects", tables)
        self.assertIn("project_steps", tables)

    def test_demo_seed_includes_project(self) -> None:
        summary = self.repository.summary()
        self.assertGreaterEqual(summary["projects"], 1)

    def test_create_project_via_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke(
            "/api/v2/projects",
            method="POST",
            token=token,
            body={
                "title": "Location studio Yaoundé",
                "project_type": "rent",
                "objective": "Trouver un studio meublé proche du centre",
                "budget_min": 120000,
                "budget_max": 180000,
                "location_city": "Yaounde",
                "timeline_horizon": "3_months",
            },
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)
        project = response.body_json()["project"]
        self.assertEqual(project["project_type"], "rent")
        self.assertEqual(project["status"], "draft")
        self.assertIn("budget", project)
        self.assertIn("location", project)

    def test_list_and_get_project(self) -> None:
        token = self.login(email="agent@lawim.local")
        created = self.invoke(
            "/api/v2/projects",
            method="POST",
            token=token,
            body={
                "title": "Investissement Kribi",
                "project_type": "invest",
                "objective": "Acquérir une villa locative",
                "status": "active",
            },
        )
        project_id = created.body_json()["project"]["id"]
        listing = self.invoke("/api/v2/projects", token=token)
        self.assertEqual(listing.status, HTTPStatus.OK)
        self.assertGreaterEqual(len(listing.body_json()["projects"]), 1)

        detail = self.invoke(f"/api/v2/projects/{project_id}", token=token)
        self.assertEqual(detail.status, HTTPStatus.OK)
        payload = detail.body_json()
        self.assertIn("steps", payload)
        self.assertGreaterEqual(len(payload["steps"]), 4)
        self.assertIn("progress", payload)
        self.assertIn("next_actions", payload)

    def test_project_steps_and_progress_endpoints(self) -> None:
        token = self.login(email="agent@lawim.local")
        created = self.invoke(
            "/api/v2/projects",
            method="POST",
            token=token,
            body={
                "title": "Achat test",
                "project_type": "buy",
                "objective": "Test parcours",
            },
        )
        project_id = created.body_json()["project"]["id"]
        steps = self.invoke(f"/api/v2/projects/{project_id}/steps", token=token)
        self.assertEqual(steps.status, HTTPStatus.OK)
        self.assertGreaterEqual(len(steps.body_json()["steps"]), 5)

        progress = self.invoke(f"/api/v2/projects/{project_id}/progress", token=token)
        self.assertEqual(progress.status, HTTPStatus.OK)
        self.assertIn("progress_percent", progress.body_json()["progress"])

        actions = self.invoke(f"/api/v2/projects/{project_id}/next-actions", token=token)
        self.assertEqual(actions.status, HTTPStatus.OK)
        self.assertIsInstance(actions.body_json()["next_actions"], list)

    def test_update_step_advances_progress(self) -> None:
        token = self.login(email="agent@lawim.local")
        created = self.invoke(
            "/api/v2/projects",
            method="POST",
            token=token,
            body={"title": "Parcours", "project_type": "buy", "objective": "Progression"},
        )
        project_id = created.body_json()["project"]["id"]
        steps = self.invoke(f"/api/v2/projects/{project_id}/steps", token=token).body_json()["steps"]
        first_step_id = steps[0]["id"]
        updated = self.invoke(
            f"/api/v2/projects/{project_id}/steps/{first_step_id}",
            method="PATCH",
            token=token,
            body={"status": "completed", "note": "Test completion"},
        )
        self.assertEqual(updated.status, HTTPStatus.OK)
        self.assertEqual(updated.body_json()["step"]["status"], "completed")
        progress = self.invoke(f"/api/v2/projects/{project_id}/progress", token=token).body_json()["progress"]
        self.assertGreater(progress["progress_percent"], 0)

    def test_permissions_other_user_forbidden(self) -> None:
        owner_token = self.register(email="buyer2@example.local", full_name="Buyer Two")
        agent_token = self.login(email="agent@lawim.local")
        created = self.invoke(
            "/api/v2/projects",
            method="POST",
            token=agent_token,
            body={"title": "Privé", "project_type": "buy", "objective": "Secret"},
        )
        project_id = created.body_json()["project"]["id"]
        denied = self.invoke(f"/api/v2/projects/{project_id}", token=owner_token)
        self.assertEqual(denied.status, HTTPStatus.FORBIDDEN)

    def test_admin_can_list_all_projects(self) -> None:
        admin_token = self.login(email="admin@lawim.local")
        response = self.invoke("/api/v2/projects", token=admin_token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertGreaterEqual(response.body_json()["pagination"]["total"], 1)

    def test_archive_project(self) -> None:
        token = self.login(email="agent@lawim.local")
        created = self.invoke(
            "/api/v2/projects",
            method="POST",
            token=token,
            body={"title": "Archive me", "project_type": "other", "objective": "Test archive"},
        )
        project_id = created.body_json()["project"]["id"]
        archived = self.invoke(
            f"/api/v2/projects/{project_id}",
            method="PATCH",
            token=token,
            body={"status": "archived"},
        )
        self.assertEqual(archived.status, HTTPStatus.OK)
        self.assertEqual(archived.body_json()["project"]["status"], "archived")

    def test_project_created_audit_event(self) -> None:
        token = self.login(email="admin@lawim.local")
        self.invoke(
            "/api/v2/projects",
            method="POST",
            token=token,
            body={"title": "Audit", "project_type": "sell", "objective": "Audit trail"},
        )
        events = self.repository.list_events(kind="project_created", limit=5)
        self.assertTrue(any("project_type" in str(event.get("payload", "")) for event in events))

    def test_domain_progress_helpers(self) -> None:
        steps = [
            {"status": "completed", "position": 0},
            {"status": "in_progress", "position": 1},
            {"status": "pending", "position": 2},
        ]
        self.assertEqual(compute_progress(steps), 33)
        actions = derive_next_actions(
            [{"id": 2, "step_key": "search", "title": "Search", "status": "in_progress", "next_action": "Go", "position": 1}],
            project_status="active",
        )
        self.assertEqual(len(actions), 1)
        self.assertEqual(len(journey_templates("buy")), 5)

    def test_v1_regression_properties_still_work(self) -> None:
        response = self.invoke("/api/properties?status=published")
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertGreaterEqual(len(response.body_json()["properties"]), 1)
