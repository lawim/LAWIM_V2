from __future__ import annotations

from http import HTTPStatus

from lawim_v2.assistant.constants import AGENT_KEYS, ASSISTANT_MODES, INTENT_KEYWORDS, PROMPT_KEYS, RAG_SOURCE_TYPES
from lawim_v2.assistant.engines import (
    AgentRouterEngine,
    ConversationMemoryEngine,
    DeterministicAssistantEngine,
    ProjectContextEngine,
    RAGFoundationEngine,
)
from lawim_v2.assistant.prompts import get_system_prompt, list_prompt_catalog
from lawim_v2.assistant.providers import DeterministicLLMProvider, OptionalLLMProvider, resolve_llm_provider
from lawim_v2.assistant.schema_v10_ddl import V10_TABLE_NAMES
from lawim_v2.schema_migrations import apply_sqlite_legacy_migrations

from tests.lawim_harness import LawimTestHarness


class ReleaseProgramDPersistenceTests(LawimTestHarness):
    def test_schema_version_is_v10(self) -> None:
        self.assertEqual(self.repository.schema_version(), 12)

    def test_assistant_tables_present(self) -> None:
        self.assertTrue(self.repository.assistant_tables_present())

    def test_all_v10_tables_exist(self) -> None:
        names = {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V10_TABLE_NAMES:
            self.assertIn(table, names)

    def test_assistant_catalog_seeded(self) -> None:
        self.repository.seed_assistant_catalog()
        self.assertGreaterEqual(self.repository.scalar("SELECT COUNT(*) FROM assistant_agents"), 6)

    def test_v9_to_v10_legacy_migration(self) -> None:
        import sqlite3
        import tempfile
        from pathlib import Path

        from lawim_v2.cognition.schema_v9_ddl import V9_TABLE_NAMES
        from lawim_v2.schema_ddl import SQLITE_INIT_SCRIPT

        db_path = Path(tempfile.mkdtemp()) / "v9.sqlite3"
        conn = sqlite3.connect(db_path)
        conn.executescript(SQLITE_INIT_SCRIPT)
        conn.execute("PRAGMA foreign_keys = OFF")
        from lawim_v2.assistant.schema_v10_ddl import V10_TABLE_NAMES as V10

        for table in V10:
            conn.execute(f"DROP TABLE IF EXISTS {table}")
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("UPDATE schema_meta SET value='9' WHERE key='schema_version'")
        apply_sqlite_legacy_migrations(conn)
        names = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        conn.close()
        self.assertIn("assistant_sessions", names)
        for table in V9_TABLE_NAMES:
            self.assertIn(table, names)


class ReleaseProgramDConstantsTests(LawimTestHarness):
    def test_agent_keys_include_advisor(self) -> None:
        self.assertIn("project_advisor", AGENT_KEYS)

    def test_agent_keys_include_decision_coach(self) -> None:
        self.assertIn("decision_coach", AGENT_KEYS)

    def test_prompt_keys_include_base(self) -> None:
        self.assertIn("system.base", PROMPT_KEYS)

    def test_rag_source_knowledge_fact(self) -> None:
        self.assertIn("knowledge_fact", RAG_SOURCE_TYPES)

    def test_assistant_modes(self) -> None:
        self.assertIn("deterministic", ASSISTANT_MODES)

    def test_intent_keywords_decision(self) -> None:
        self.assertIn("decision_coach", INTENT_KEYWORDS)


class ReleaseProgramDEngineTests(LawimTestHarness):
    def test_agent_router_decision_intent(self) -> None:
        route = AgentRouterEngine().route(message="Quelle décision prendre ?", project={"id": 1})
        self.assertEqual(route["agent_key"], "decision_coach")

    def test_agent_router_default(self) -> None:
        route = AgentRouterEngine().route(message="Bonjour", project={"id": 1})
        self.assertIn(route["agent_key"], AGENT_KEYS)

    def test_project_context_engine(self) -> None:
        ctx = ProjectContextEngine().build(
            project={"id": 1, "title": "Test"},
            goals=[{"goal_key": "buy", "title": "Buy"}],
            journey_state={},
            intelligence={},
            next_action={"title": "Act"},
            partner_matches=[],
            service_matches=[],
            decisions=[],
            risks=[],
        )
        self.assertEqual(ctx["project"]["title"], "Test")

    def test_rag_chunk_and_retrieve(self) -> None:
        engine = RAGFoundationEngine()
        chunks = engine.chunk_text("budget achat immobilier Douala financement prêt")
        self.assertGreaterEqual(len(chunks), 1)
        retrieved = engine.retrieve(
            query="budget Douala",
            chunks=[{"content": "budget achat immobilier Douala", "chunk_key": "c1"}],
        )
        self.assertGreaterEqual(len(retrieved), 1)

    def test_deterministic_assistant_compose(self) -> None:
        payload = DeterministicAssistantEngine().compose(
            agent_key="project_advisor",
            user_message="Comment avancer ?",
            context={"project": {"title": "Projet A"}, "next_best_action": {"title": "Valider budget"}},
            rag_chunks=[],
            routing={"agent_key": "project_advisor"},
        )
        self.assertIn("content", payload)
        self.assertEqual(payload["mode"], "deterministic")

    def test_conversation_memory_summary(self) -> None:
        summary = ConversationMemoryEngine().summarize(
            [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi"}]
        )
        self.assertIn("user", summary)

    def test_get_system_prompt(self) -> None:
        text = get_system_prompt("system.base")
        self.assertIn("LAWIM", text)

    def test_prompt_catalog(self) -> None:
        self.assertGreaterEqual(len(list_prompt_catalog()), 7)


class ReleaseProgramDProviderTests(LawimTestHarness):
    def test_deterministic_provider_available(self) -> None:
        provider = DeterministicLLMProvider()
        self.assertTrue(provider.is_available())
        self.assertIsNone(provider.complete(system_prompt="x", user_message="y", context={}))

    def test_optional_llm_disabled(self) -> None:
        provider = resolve_llm_provider(enabled=False)
        self.assertEqual(provider.name, "deterministic")

    def test_optional_llm_enabled_not_used_without_impl(self) -> None:
        provider = OptionalLLMProvider(enabled=True)
        self.assertIsNone(provider.complete(system_prompt="x", user_message="y", context={}))


class ReleaseProgramDRepositoryTests(LawimTestHarness):
    def _project_id(self) -> int:
        return int(self.repository.one("SELECT id FROM projects ORDER BY id ASC LIMIT 1")["id"])

    def test_bootstrap_project_assistant(self) -> None:
        project_id = self._project_id()
        user_id = int(self.repository.one("SELECT user_id FROM projects WHERE id = ?", (project_id,))["user_id"])
        self.repository.bootstrap_project_assistant(project_id, user_id=user_id)
        sessions = self.repository.list_assistant_sessions(project_id, user_id)
        self.assertGreaterEqual(len(sessions), 1)

    def test_refresh_rag_index(self) -> None:
        project_id = self._project_id()
        payload = self.repository.refresh_project_rag_index(project_id)
        self.assertGreaterEqual(payload["documents"], 1)

    def test_chat_assistant_persists_messages(self) -> None:
        project_id = self._project_id()
        user_id = int(self.repository.one("SELECT user_id FROM projects WHERE id = ?", (project_id,))["user_id"])
        result = self.repository.chat_assistant(
            project_id=project_id,
            user_id=user_id,
            message="Quels sont les risques du projet ?",
        )
        self.assertIn("assistant_message", result)
        self.assertEqual(result["mode"], "deterministic")

    def test_list_assistant_agents(self) -> None:
        self.repository.seed_assistant_catalog()
        agents = self.repository.list_assistant_agents()
        self.assertGreaterEqual(len(agents), 6)

    def test_get_assistant_context(self) -> None:
        project_id = self._project_id()
        ctx = self.repository.get_assistant_context(project_id)
        self.assertEqual(ctx["project_id"], project_id)


class ReleaseProgramDApiTests(LawimTestHarness):
    def _project_id(self, token: str) -> int:
        return int(self.invoke("/api/v2/projects?limit=1", token=token).body_json()["projects"][0]["id"])

    def test_assistant_agents_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/assistant/agents", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertGreaterEqual(len(response.body_json()["agents"]), 6)

    def test_assistant_prompts_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/assistant/prompts", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertGreaterEqual(len(response.body_json()["prompts"]), 7)

    def test_assistant_sessions_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._project_id(token)
        response = self.invoke(f"/api/v2/assistant/sessions?project_id={project_id}", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("sessions", response.body_json())

    def test_assistant_create_session_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._project_id(token)
        response = self.invoke(
            "/api/v2/assistant/sessions",
            method="POST",
            token=token,
            body={"project_id": project_id, "agent_key": "risk_analyst"},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_assistant_context_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._project_id(token)
        response = self.invoke(f"/api/v2/assistant/context?project_id={project_id}", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("context", response.body_json())

    def test_assistant_rag_retrieve_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._project_id(token)
        response = self.invoke(f"/api/v2/assistant/rag?project_id={project_id}&query=budget", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_assistant_rag_refresh_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._project_id(token)
        response = self.invoke(
            "/api/v2/assistant/rag/refresh",
            method="POST",
            token=token,
            body={"project_id": project_id},
        )
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_assistant_chat_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._project_id(token)
        response = self.invoke(
            "/api/v2/assistant/chat",
            method="POST",
            token=token,
            body={"project_id": project_id, "message": "Quelle est la prochaine action ?"},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)
        chat = response.body_json()["chat"]
        self.assertIn("assistant_message", chat)
        self.assertTrue(chat.get("fallback_used"))

    def test_assistant_root_chat_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._project_id(token)
        response = self.invoke(
            "/api/v2/assistant",
            method="POST",
            token=token,
            body={"project_id": project_id, "message": "Bonjour assistant"},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)


class ReleaseProgramDUiTests(LawimTestHarness):
    def test_app_js_references_assistant(self) -> None:
        js = self.invoke("/app.js")
        self.assertIn("/api/v2/assistant/chat", js.body_text())

    def test_index_has_assistant_section(self) -> None:
        html = self.invoke("/")
        self.assertIn("AI Assistant", html.body_text())


class ReleaseProgramDHealthTests(LawimTestHarness):
    def test_health_schema_v10(self) -> None:
        health = self.invoke("/api/health")
        self.assertEqual(health.body_json()["database"]["schema_version"], 12)

    def test_migration_strategy_v10(self) -> None:
        from lawim_v2.schema_migrations import migration_strategy_profile

        self.assertEqual(migration_strategy_profile()["schema_version"], 12)

    def test_metrics_include_assistant_counters(self) -> None:
        token = self.login(email="admin@lawim.local")
        agent = self.login(email="agent@lawim.local")
        project_id = int(self.invoke("/api/v2/projects?limit=1", token=agent).body_json()["projects"][0]["id"])
        self.invoke(
            "/api/v2/assistant/chat",
            method="POST",
            token=agent,
            body={"project_id": project_id, "message": "Test metrics"},
        )
        metrics = self.invoke("/api/metrics", token=token)
        snapshot = metrics.body_json()["metrics"]
        self.assertGreaterEqual(snapshot.get("assistant_chat_total", 0), 1)


class ReleaseProgramDAgentKeyTests(LawimTestHarness):
    def test_agent_ecosystem_navigator(self) -> None:
        self.assertIn("ecosystem_navigator", AGENT_KEYS)

    def test_agent_risk_analyst(self) -> None:
        self.assertIn("risk_analyst", AGENT_KEYS)

    def test_agent_journey_guide(self) -> None:
        self.assertIn("journey_guide", AGENT_KEYS)

    def test_agent_simulation_planner(self) -> None:
        self.assertIn("simulation_planner", AGENT_KEYS)


class ReleaseProgramDIntegrationTests(LawimTestHarness):
    def test_new_project_bootstraps_assistant(self) -> None:
        token = self.login(email="agent@lawim.local")
        created = self.invoke(
            "/api/v2/projects",
            method="POST",
            token=token,
            body={"title": "Assistant bootstrap", "project_type": "buy", "objective": "Test", "budget_min": 1, "budget_max": 2},
        )
        project_id = int(created.body_json()["project"]["id"])
        count = self.repository.scalar("SELECT COUNT(*) FROM assistant_sessions WHERE project_id = ?", (project_id,))
        self.assertGreaterEqual(count, 1)

    def test_assistant_event_recorded(self) -> None:
        project_id = int(self.repository.one("SELECT id FROM projects ORDER BY id ASC LIMIT 1")["id"])
        user_id = int(self.repository.one("SELECT user_id FROM projects WHERE id = ?", (project_id,))["user_id"])
        self.repository.chat_assistant(project_id=project_id, user_id=user_id, message="Test event")
        events = self.repository.list_events(limit=10)
        self.assertIn("assistant_chat_completed", [e["kind"] for e in events])

    def test_assistant_messages_list_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = int(self.invoke("/api/v2/projects?limit=1", token=token).body_json()["projects"][0]["id"])
        self.invoke(
            "/api/v2/assistant/chat",
            method="POST",
            token=token,
            body={"project_id": project_id, "message": "Liste messages"},
        )
        sessions = self.invoke(f"/api/v2/assistant/sessions?project_id={project_id}", token=token).body_json()["sessions"]
        session_id = sessions[0]["id"]
        response = self.invoke(
            f"/api/v2/assistant/messages?project_id={project_id}&session_id={session_id}",
            token=token,
        )
        self.assertGreaterEqual(len(response.body_json()["messages"]), 2)


class ReleaseProgramDRagSourceTests(LawimTestHarness):
    def test_rag_source_knowledge_node(self) -> None:
        self.assertIn("knowledge_node", RAG_SOURCE_TYPES)

    def test_rag_source_cognition_decision(self) -> None:
        self.assertIn("cognition_decision", RAG_SOURCE_TYPES)

    def test_rag_source_ecosystem_match(self) -> None:
        self.assertIn("ecosystem_match", RAG_SOURCE_TYPES)

    def test_rag_source_journey_step(self) -> None:
        self.assertIn("journey_step", RAG_SOURCE_TYPES)

    def test_rag_source_project_metadata(self) -> None:
        self.assertIn("project_metadata", RAG_SOURCE_TYPES)


class ReleaseProgramDPromptTests(LawimTestHarness):
    def test_prompt_decision_coach(self) -> None:
        self.assertIn("décision", get_system_prompt("system.decision_coach").lower())

    def test_prompt_ecosystem(self) -> None:
        self.assertIn("partenaire", get_system_prompt("system.ecosystem_navigator").lower())

    def test_prompt_risk(self) -> None:
        self.assertIn("risque", get_system_prompt("system.risk_analyst").lower())

    def test_prompt_journey(self) -> None:
        self.assertIn("parcours", get_system_prompt("system.journey_guide").lower())

    def test_prompt_simulation(self) -> None:
        self.assertIn("simulation", get_system_prompt("system.simulation_planner").lower())


class ReleaseProgramDExtraCoverageTests(LawimTestHarness):
    def test_router_ecosystem_intent(self) -> None:
        route = AgentRouterEngine().route(message="Quel partenaire recommandez-vous ?", project={"id": 1})
        self.assertEqual(route["agent_key"], "ecosystem_navigator")

    def test_router_risk_intent(self) -> None:
        route = AgentRouterEngine().route(message="Quels risques ouvrir ?", project={"id": 1})
        self.assertEqual(route["agent_key"], "risk_analyst")

    def test_router_journey_intent(self) -> None:
        route = AgentRouterEngine().route(message="Où en est mon parcours ?", project={"id": 1})
        self.assertEqual(route["agent_key"], "journey_guide")

    def test_router_simulation_intent(self) -> None:
        route = AgentRouterEngine().route(message="Simuler un prêt bancaire", project={"id": 1})
        self.assertEqual(route["agent_key"], "simulation_planner")

    def test_rag_empty_query_score(self) -> None:
        self.assertEqual(RAGFoundationEngine().score_query("", "budget achat"), 0)

    def test_rag_chunk_empty(self) -> None:
        self.assertEqual(RAGFoundationEngine().chunk_text(""), [])

    def test_deterministic_ecosystem_template(self) -> None:
        payload = DeterministicAssistantEngine().compose(
            agent_key="ecosystem_navigator",
            user_message="Services",
            context={"project": {"title": "P"}},
            rag_chunks=[],
            routing={},
        )
        self.assertIn("Écosystème", payload["content"])

    def test_list_assistant_prompts_repo(self) -> None:
        self.repository.seed_assistant_catalog()
        self.assertGreaterEqual(len(self.repository.list_assistant_prompts()), 7)

    def test_retrieve_assistant_rag(self) -> None:
        project_id = int(self.repository.one("SELECT id FROM projects ORDER BY id ASC LIMIT 1")["id"])
        self.repository.refresh_project_rag_index(project_id)
        chunks = self.repository.retrieve_assistant_rag(project_id, "budget")
        self.assertIsInstance(chunks, list)

    def test_assistant_session_get_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = int(self.invoke("/api/v2/projects?limit=1", token=token).body_json()["projects"][0]["id"])
        session_id = self.invoke(f"/api/v2/assistant/sessions?project_id={project_id}", token=token).body_json()["sessions"][0]["id"]
        response = self.invoke(f"/api/v2/assistant/sessions/{session_id}?project_id={project_id}", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_chat_routes_to_decision_coach(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = int(self.invoke("/api/v2/projects?limit=1", token=token).body_json()["projects"][0]["id"])
        response = self.invoke(
            "/api/v2/assistant/chat",
            method="POST",
            token=token,
            body={"project_id": project_id, "message": "Quelle décision prendre maintenant ?"},
        )
        self.assertEqual(response.body_json()["chat"]["agent_key"], "decision_coach")

    def test_assistant_mode_deterministic(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = int(self.invoke("/api/v2/projects?limit=1", token=token).body_json()["projects"][0]["id"])
        response = self.invoke(
            "/api/v2/assistant/chat",
            method="POST",
            token=token,
            body={"project_id": project_id, "message": "Bonjour"},
        )
        self.assertEqual(response.body_json()["chat"]["mode"], "deterministic")

    def test_v10_table_assistant_messages(self) -> None:
        names = {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn("assistant_messages", names)

    def test_v10_table_assistant_turns(self) -> None:
        names = {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn("assistant_turns", names)

    def test_v10_table_assistant_rag_chunks(self) -> None:
        names = {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn("assistant_rag_chunks", names)

    def test_v10_table_assistant_memory_summaries(self) -> None:
        names = {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn("assistant_memory_summaries", names)

    def test_v10_table_assistant_prompt_versions(self) -> None:
        names = {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn("assistant_prompt_versions", names)

    def test_v10_table_assistant_context_snapshots(self) -> None:
        names = {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn("assistant_context_snapshots", names)

    def test_v10_table_assistant_rag_retrievals(self) -> None:
        names = {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn("assistant_rag_retrievals", names)

    def test_v10_table_assistant_agent_assignments(self) -> None:
        names = {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn("assistant_agent_assignments", names)
