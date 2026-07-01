from __future__ import annotations

from http import HTTPStatus

from lawim_v2.cognition.constants import (
    EDGE_TYPES,
    LIKELIHOOD_WEIGHTS,
    NODE_TYPES,
    REASONING_RULES,
    RELATION_TYPES,
    SEVERITY_WEIGHTS,
    SIMULATION_SCENARIOS,
)
from lawim_v2.cognition.engines import (
    DecisionPlatformEngine,
    KnowledgeGraphEngine,
    NextBestActionEngine,
    OpportunityIntelligenceEngine,
    ReasoningEngine,
    RiskIntelligenceEngine,
    SimulationEngine,
)
from lawim_v2.cognition.schema_v9_ddl import V9_TABLE_NAMES
from lawim_v2.schema_migrations import apply_sqlite_legacy_migrations

from tests.lawim_harness import LawimTestHarness


class ReleaseProgramCPersistenceTests(LawimTestHarness):
    def test_schema_version_is_v10(self) -> None:
        self.assertEqual(self.repository.schema_version(), 12)

    def test_cognition_tables_present(self) -> None:
        self.assertTrue(self.repository.cognition_tables_present())

    def test_all_v9_tables_exist(self) -> None:
        names = {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V9_TABLE_NAMES:
            self.assertIn(table, names)

    def test_demo_project_has_knowledge_nodes(self) -> None:
        project_id = int(self.repository.one("SELECT id FROM projects ORDER BY id ASC LIMIT 1")["id"])
        count = self.repository.scalar("SELECT COUNT(*) FROM knowledge_nodes WHERE project_id = ?", (project_id,))
        self.assertGreaterEqual(count, 1)

    def test_v8_to_v9_legacy_migration(self) -> None:
        import sqlite3
        import tempfile
        from pathlib import Path

        from lawim_v2.ecosystem.schema_v8_ddl import V8_TABLE_NAMES
        from lawim_v2.schema_ddl import SQLITE_INIT_SCRIPT

        db_path = Path(tempfile.mkdtemp()) / "v8.sqlite3"
        conn = sqlite3.connect(db_path)
        conn.executescript(SQLITE_INIT_SCRIPT)
        conn.execute("PRAGMA foreign_keys = OFF")
        from lawim_v2.cognition.schema_v9_ddl import V9_TABLE_NAMES

        for table in V9_TABLE_NAMES:
            conn.execute(f"DROP TABLE IF EXISTS {table}")
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("UPDATE schema_meta SET value='8' WHERE key='schema_version'")
        apply_sqlite_legacy_migrations(conn)
        names = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        conn.close()
        self.assertIn("knowledge_nodes", names)
        self.assertIn("cognition_decisions", names)
        for table in V8_TABLE_NAMES:
            self.assertIn(table, names)


class ReleaseProgramCConstantsTests(LawimTestHarness):
    def test_node_types_include_project(self) -> None:
        self.assertIn("project", NODE_TYPES)

    def test_node_types_include_knowledge_fact(self) -> None:
        self.assertIn("knowledge_fact", NODE_TYPES)

    def test_edge_types_include_has_goal(self) -> None:
        self.assertIn("has_goal", EDGE_TYPES)

    def test_relation_types_include_influence(self) -> None:
        self.assertIn("influence", RELATION_TYPES)

    def test_simulation_scenario_budget_increase(self) -> None:
        self.assertIn("budget_increase", SIMULATION_SCENARIOS)

    def test_simulation_scenario_count(self) -> None:
        self.assertGreaterEqual(len(SIMULATION_SCENARIOS), 8)

    def test_reasoning_rules_count(self) -> None:
        self.assertGreaterEqual(len(REASONING_RULES), 5)

    def test_severity_weights_high(self) -> None:
        self.assertEqual(SEVERITY_WEIGHTS["high"], 50)

    def test_likelihood_weights_certain(self) -> None:
        self.assertEqual(LIKELIHOOD_WEIGHTS["certain"], 45)


class ReleaseProgramCEngineTests(LawimTestHarness):
    def test_knowledge_graph_builds_nodes(self) -> None:
        graph = KnowledgeGraphEngine().build_graph(
            project={"id": 1, "title": "Test"},
            goals=[{"id": 1, "goal_key": "buy", "title": "Buy"}],
            needs=[],
            constraints=[],
            life_events=[],
            decisions=[],
            recommendations=[],
            tasks=[],
            actions=[],
            risks=[],
            opportunities=[],
            knowledge_facts=[],
            resources=[],
            partner_matches=[],
            service_matches=[],
        )
        self.assertGreaterEqual(len(graph["nodes"]), 2)
        self.assertTrue(any(node["node_type"] == "project" for node in graph["nodes"]))

    def test_reasoning_engine_budget_rule(self) -> None:
        result = ReasoningEngine().run(
            project={"budget_min": None, "budget_max": None},
            goals=[],
            risks=[],
            opportunities=[],
            constraints=[],
            journey_state={"blocked_steps": 0},
            partner_matches=[],
            workflow_instance=None,
        )
        conclusions = result["conclusions"]
        self.assertTrue(any("budget" in c.lower() for c in conclusions))

    def test_decision_platform_engine(self) -> None:
        decision = DecisionPlatformEngine().evaluate(
            project={"project_type": "buy", "budget_min": 100, "budget_max": 200},
            goals=[{"goal_key": "buy"}],
            risks=[],
            opportunities=[],
            constraints=[],
            reasoning={"conclusions": [], "merged_priority": []},
            evidences=[{"evidence_key": "g1", "label": "Goal", "weight": 50}],
        )
        self.assertIn("decision_key", decision)
        self.assertGreater(decision["confidence"], 0)

    def test_simulation_engine_budget_increase(self) -> None:
        result = SimulationEngine().run(
            scenario_key="budget_increase",
            project={"budget_max": 100000},
            goals=[],
            parameters={"budget_delta_percent": 10},
        )
        self.assertEqual(result["scenario_key"], "budget_increase")
        self.assertIn("impacts", result)

    def test_risk_intelligence_engine(self) -> None:
        scores = RiskIntelligenceEngine().analyze(
            project={"id": 1},
            risks=[{"risk_key": "budget", "severity": "high", "likelihood": "medium", "description": "Gap"}],
            journey_state={"blocked_steps": 1},
            workflow_instance={"status": "active"},
        )
        self.assertGreaterEqual(len(scores), 1)
        self.assertGreater(scores[0]["score"], 0)

    def test_opportunity_intelligence_engine(self) -> None:
        scores = OpportunityIntelligenceEngine().analyze(
            project={"id": 1},
            opportunities=[{"opportunity_key": "yield", "description": "Yield", "value_score": 70}],
            partner_matches=[{"score": 80}],
            service_matches=[{"score": 75}],
        )
        self.assertGreaterEqual(len(scores), 1)

    def test_next_best_action_engine(self) -> None:
        nba = NextBestActionEngine().compute(
            project={"project_type": "buy"},
            decision={"next_action": "Validate budget", "confidence": 70},
            reasoning={"merged_priority": ["Validate budget"]},
            risks=[],
            workflow_instance={"current_step_key": "search"},
            partner_matches=[],
            cost_summary=None,
        )
        self.assertIn("action_key", nba)
        self.assertGreater(nba["score"], 0)


class ReleaseProgramCRepositoryTests(LawimTestHarness):
    def _project_id(self) -> int:
        return int(self.repository.one("SELECT id FROM projects ORDER BY id ASC LIMIT 1")["id"])

    def test_refresh_project_cognition(self) -> None:
        project_id = self._project_id()
        payload = self.repository.refresh_project_cognition(project_id)
        self.assertIn("graph", payload)
        self.assertIn("decision", payload)

    def test_get_knowledge_graph(self) -> None:
        project_id = self._project_id()
        graph = self.repository.get_knowledge_graph(project_id)
        self.assertIn("nodes", graph)
        self.assertIn("edges", graph)

    def test_get_knowledge_context(self) -> None:
        project_id = self._project_id()
        ctx = self.repository.get_knowledge_context(project_id)
        self.assertEqual(ctx["project_id"], project_id)

    def test_list_cognition_decisions(self) -> None:
        project_id = self._project_id()
        decisions = self.repository.list_cognition_decisions(project_id)
        self.assertGreaterEqual(len(decisions), 1)

    def test_list_reasoning_traces(self) -> None:
        project_id = self._project_id()
        traces = self.repository.list_reasoning_traces(project_id)
        self.assertGreaterEqual(len(traces), 1)

    def test_run_simulation_persisted(self) -> None:
        project_id = self._project_id()
        result = self.repository.run_simulation(project_id, "budget_increase", {"budget_delta_percent": 5})
        self.assertIn("id", result)
        runs = self.repository.list_simulation_runs(project_id)
        self.assertGreaterEqual(len(runs), 1)

    def test_get_next_best_action(self) -> None:
        project_id = self._project_id()
        nba = self.repository.get_next_best_action(project_id)
        self.assertIsNotNone(nba)
        self.assertIn("title", nba)

    def test_list_risk_intelligence(self) -> None:
        project_id = self._project_id()
        risks = self.repository.list_risk_intelligence(project_id)
        self.assertIsInstance(risks, list)

    def test_get_intelligence_workspace(self) -> None:
        project_id = self._project_id()
        workspace = self.repository.get_intelligence_workspace(project_id)
        self.assertEqual(workspace["project_id"], project_id)


class ReleaseProgramCApiTests(LawimTestHarness):
    def _project_id(self, token: str) -> int:
        response = self.invoke("/api/v2/projects?limit=1", token=token)
        projects = response.body_json()["projects"]
        self.assertGreaterEqual(len(projects), 1)
        return int(projects[0]["id"])

    def test_knowledge_graph_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._project_id(token)
        response = self.invoke(f"/api/v2/knowledge/graph?project_id={project_id}", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("graph", response.body_json())

    def test_knowledge_context_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._project_id(token)
        response = self.invoke(f"/api/v2/knowledge/context?project_id={project_id}", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("context", response.body_json())

    def test_decisions_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._project_id(token)
        response = self.invoke(f"/api/v2/decisions?project_id={project_id}", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertGreaterEqual(len(response.body_json()["decisions"]), 1)

    def test_reasoning_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._project_id(token)
        response = self.invoke(f"/api/v2/reasoning?project_id={project_id}", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("reasoning", response.body_json())

    def test_simulations_list_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._project_id(token)
        response = self.invoke(f"/api/v2/simulations?project_id={project_id}", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        body = response.body_json()
        self.assertIn("scenarios", body)
        self.assertIn("runs", body)

    def test_simulation_run_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._project_id(token)
        response = self.invoke(
            "/api/v2/simulations",
            method="POST",
            token=token,
            body={"project_id": project_id, "scenario_key": "relocation", "parameters": {"new_city": "Yaoundé"}},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)
        self.assertIn("simulation", response.body_json())

    def test_intelligence_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._project_id(token)
        response = self.invoke(f"/api/v2/intelligence?project_id={project_id}", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("intelligence", response.body_json())

    def test_next_actions_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._project_id(token)
        response = self.invoke(f"/api/v2/next-actions?project_id={project_id}", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("next_action", response.body_json())

    def test_risks_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._project_id(token)
        response = self.invoke(f"/api/v2/risks?project_id={project_id}", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("risks", response.body_json())

    def test_opportunities_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._project_id(token)
        response = self.invoke(f"/api/v2/opportunities?project_id={project_id}", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("opportunities", response.body_json())

    def test_knowledge_refresh_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._project_id(token)
        response = self.invoke(
            "/api/v2/knowledge/refresh",
            method="POST",
            token=token,
            body={"project_id": project_id},
        )
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("intelligence", response.body_json())

    def test_global_knowledge_still_admin_only(self) -> None:
        token = self.login(email="agent@lawim.local")
        denied = self.invoke("/api/v2/knowledge", token=token)
        self.assertEqual(denied.status, HTTPStatus.FORBIDDEN)


class ReleaseProgramCUiTests(LawimTestHarness):
    def test_app_js_references_knowledge_graph(self) -> None:
        js = self.invoke("/app.js")
        self.assertIn("/api/v2/knowledge/graph", js.body_text())

    def test_app_js_references_intelligence(self) -> None:
        js = self.invoke("/app.js")
        self.assertIn("/api/v2/intelligence", js.body_text())

    def test_index_has_cognition_section(self) -> None:
        html = self.invoke("/")
        self.assertIn("Knowledge &amp; decisions", html.body_text())


class ReleaseProgramCHealthTests(LawimTestHarness):
    def test_health_schema_v10(self) -> None:
        health = self.invoke("/api/health")
        self.assertEqual(health.body_json()["database"]["schema_version"], 12)

    def test_migration_strategy_v10(self) -> None:
        from lawim_v2.schema_migrations import migration_strategy_profile

        self.assertEqual(migration_strategy_profile()["schema_version"], 12)

    def test_metrics_include_cognition_counters(self) -> None:
        token = self.login(email="admin@lawim.local")
        agent = self.login(email="agent@lawim.local")
        project_id = int(self.invoke("/api/v2/projects?limit=1", token=agent).body_json()["projects"][0]["id"])
        self.invoke(f"/api/v2/knowledge/graph?project_id={project_id}", token=agent)
        metrics = self.invoke("/api/metrics", token=token)
        snapshot = metrics.body_json()["metrics"]
        self.assertGreaterEqual(snapshot.get("cognition_graph_total", 0), 1)


class ReleaseProgramCSimulationScenarioTests(LawimTestHarness):
    def test_scenario_budget_decrease(self) -> None:
        self.assertIn("budget_decrease", SIMULATION_SCENARIOS)

    def test_scenario_new_loan(self) -> None:
        self.assertIn("new_loan", SIMULATION_SCENARIOS)

    def test_scenario_prior_sale(self) -> None:
        self.assertIn("prior_sale", SIMULATION_SCENARIOS)

    def test_scenario_relocation(self) -> None:
        self.assertIn("relocation", SIMULATION_SCENARIOS)

    def test_scenario_birth(self) -> None:
        self.assertIn("birth", SIMULATION_SCENARIOS)

    def test_scenario_construction_delay(self) -> None:
        self.assertIn("construction_delay", SIMULATION_SCENARIOS)

    def test_scenario_interest_rate_change(self) -> None:
        self.assertIn("interest_rate_change", SIMULATION_SCENARIOS)

    def test_scenario_new_partner(self) -> None:
        self.assertIn("new_partner", SIMULATION_SCENARIOS)


class ReleaseProgramCNodeTypeTests(LawimTestHarness):
    def test_node_goal(self) -> None:
        self.assertIn("goal", NODE_TYPES)

    def test_node_need(self) -> None:
        self.assertIn("need", NODE_TYPES)

    def test_node_constraint(self) -> None:
        self.assertIn("constraint", NODE_TYPES)

    def test_node_partner(self) -> None:
        self.assertIn("partner", NODE_TYPES)

    def test_node_service(self) -> None:
        self.assertIn("service", NODE_TYPES)

    def test_node_workflow(self) -> None:
        self.assertIn("workflow", NODE_TYPES)

    def test_node_risk(self) -> None:
        self.assertIn("risk", NODE_TYPES)

    def test_node_opportunity(self) -> None:
        self.assertIn("opportunity", NODE_TYPES)


class ReleaseProgramCEdgeTypeTests(LawimTestHarness):
    def test_edge_recommends(self) -> None:
        self.assertIn("recommends", EDGE_TYPES)

    def test_edge_blocks(self) -> None:
        self.assertIn("blocks", EDGE_TYPES)

    def test_edge_enables(self) -> None:
        self.assertIn("enables", EDGE_TYPES)

    def test_edge_mitigates(self) -> None:
        self.assertIn("mitigates", EDGE_TYPES)

    def test_edge_exploits(self) -> None:
        self.assertIn("exploits", EDGE_TYPES)


class ReleaseProgramCIntegrationTests(LawimTestHarness):
    def test_new_project_bootstraps_cognition(self) -> None:
        token = self.login(email="agent@lawim.local")
        created = self.invoke(
            "/api/v2/projects",
            method="POST",
            token=token,
            body={"title": "Cognition bootstrap", "project_type": "buy", "objective": "Test cognition", "budget_min": 1, "budget_max": 2},
        )
        project_id = int(created.body_json()["project"]["id"])
        count = self.repository.scalar("SELECT COUNT(*) FROM knowledge_nodes WHERE project_id = ?", (project_id,))
        self.assertGreaterEqual(count, 1)

    def test_cognition_event_recorded(self) -> None:
        project_id = int(self.repository.one("SELECT id FROM projects ORDER BY id ASC LIMIT 1")["id"])
        self.repository.refresh_project_cognition(project_id)
        events = self.repository.list_events(limit=10)
        kinds = [event["kind"] for event in events]
        self.assertIn("project_cognition_refreshed", kinds)

    def test_decision_detail_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = int(self.invoke("/api/v2/projects?limit=1", token=token).body_json()["projects"][0]["id"])
        decision_id = int(self.invoke(f"/api/v2/decisions?project_id={project_id}", token=token).body_json()["decisions"][0]["id"])
        response = self.invoke(f"/api/v2/decisions/{decision_id}?project_id={project_id}", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("decision", response.body_json())


class ReleaseProgramCExtraCoverageTests(LawimTestHarness):
    def test_list_knowledge_inferences(self) -> None:
        project_id = int(self.repository.one("SELECT id FROM projects ORDER BY id ASC LIMIT 1")["id"])
        rows = self.repository.list_knowledge_inferences(project_id)
        self.assertIsInstance(rows, list)

    def test_list_knowledge_history(self) -> None:
        project_id = int(self.repository.one("SELECT id FROM projects ORDER BY id ASC LIMIT 1")["id"])
        rows = self.repository.list_knowledge_history(project_id)
        self.assertIsInstance(rows, list)

    def test_list_simulation_scenarios(self) -> None:
        scenarios = self.repository.list_simulation_scenarios()
        self.assertGreaterEqual(len(scenarios), 8)

    def test_simulation_engine_interest_rate(self) -> None:
        result = SimulationEngine().run(
            scenario_key="interest_rate_change",
            project={"budget_max": 100000},
            goals=[],
            parameters={"rate_delta_percent": 1},
        )
        self.assertIn("impacts", result)

    def test_relation_types_include_support(self) -> None:
        self.assertIn("support", RELATION_TYPES)

    def test_node_milestone(self) -> None:
        self.assertIn("milestone", NODE_TYPES)
