from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from typing import Any

from .constants import AGENT_KEYS, DEFAULT_PROMPT_VERSION
from .engines import (
    AgentRouterEngine,
    ConversationMemoryEngine,
    DeterministicAssistantEngine,
    ProjectContextEngine,
    RAGFoundationEngine,
)
from .prompts import get_system_prompt, list_prompt_catalog


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _parse_json(value: str | None) -> Any:
    if not value:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return None


class AssistantRepositoryMixin:
    def assistant_tables_present(self) -> bool:
        row = self.one("SELECT name FROM sqlite_master WHERE type='table' AND name='assistant_sessions'")
        return row is not None

    def seed_assistant_catalog(self) -> None:
        if self.scalar("SELECT COUNT(*) FROM assistant_agents") > 0:
            return
        now = _utcnow()
        agents = (
            ("project_advisor", "Conseiller projet", "Synthèse et pilotage projet", "system.project_advisor"),
            ("decision_coach", "Coach décision", "Décisions et alternatives", "system.decision_coach"),
            ("ecosystem_navigator", "Navigateur écosystème", "Partenaires et services", "system.ecosystem_navigator"),
            ("risk_analyst", "Analyste risques", "Risques et mitigations", "system.risk_analyst"),
            ("journey_guide", "Guide parcours", "Étapes et progression", "system.journey_guide"),
            ("simulation_planner", "Planificateur simulation", "Scénarios what-if", "system.simulation_planner"),
        )
        with self._transaction() as conn:
            for agent_key, title, description, prompt_key in agents:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO assistant_agents (
                        agent_key, title, description, capabilities_json, prompt_key, status, created_at, updated_at
                    ) VALUES (?, ?, ?, '[]', ?, 'active', ?, ?)
                    """,
                    (agent_key, title, description, prompt_key, now, now),
                )
            for row in list_prompt_catalog():
                conn.execute(
                    """
                    INSERT OR IGNORE INTO assistant_prompt_versions (prompt_key, version, content, status, created_at)
                    VALUES (?, ?, ?, 'active', ?)
                    """,
                    (row["prompt_key"], row["version"], row["content"], now),
                )

    def bootstrap_project_assistant(self, project_id: int, user_id: int | None = None) -> None:
        self.seed_assistant_catalog()
        self.refresh_project_rag_index(project_id)
        uid = user_id or int(self.one("SELECT user_id FROM projects WHERE id = ?", (project_id,))["user_id"])
        existing = self.one(
            "SELECT id FROM assistant_sessions WHERE project_id = ? AND user_id = ? AND status = 'active' LIMIT 1",
            (project_id, uid),
        )
        if existing is None:
            self.create_assistant_session(project_id=project_id, user_id=uid, agent_key="project_advisor")

    def create_assistant_session(
        self,
        *,
        project_id: int,
        user_id: int,
        agent_key: str = "project_advisor",
        session_key: str | None = None,
    ) -> dict[str, object]:
        now = _utcnow()
        key = session_key or f"session-{project_id}-{user_id}-{uuid.uuid4().hex[:12]}"
        if agent_key not in AGENT_KEYS:
            agent_key = "project_advisor"
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO assistant_sessions (
                    project_id, user_id, session_key, agent_key, status, metadata_json, created_at, updated_at
                ) VALUES (?, ?, ?, ?, 'active', '{}', ?, ?)
                """,
                (project_id, user_id, key, agent_key, now, now),
            )
            session_id = int(cursor.lastrowid)
            conn.execute(
                """
                INSERT OR IGNORE INTO assistant_agent_assignments (project_id, session_id, agent_key, assigned_at)
                VALUES (?, ?, ?, ?)
                """,
                (project_id, session_id, agent_key, now),
            )
        row = self.one("SELECT * FROM assistant_sessions WHERE id = ?", (session_id,))
        assert row is not None
        return dict(row)

    def list_assistant_sessions(self, project_id: int, user_id: int | None = None) -> list[dict[str, object]]:
        if user_id is not None:
            rows = self.all(
                "SELECT * FROM assistant_sessions WHERE project_id = ? AND user_id = ? ORDER BY id DESC",
                (project_id, user_id),
            )
        else:
            rows = self.all("SELECT * FROM assistant_sessions WHERE project_id = ? ORDER BY id DESC", (project_id,))
        return [dict(row) for row in rows]

    def get_assistant_session(self, project_id: int, session_id: int) -> dict[str, object]:
        row = self.one("SELECT * FROM assistant_sessions WHERE id = ? AND project_id = ?", (session_id, project_id))
        if row is None:
            from ..errors import NotFoundError
            raise NotFoundError("assistant session not found")
        return dict(row)

    def list_assistant_messages(self, session_id: int, project_id: int, *, limit: int = 50) -> list[dict[str, object]]:
        rows = self.all(
            "SELECT * FROM assistant_messages WHERE session_id = ? AND project_id = ? ORDER BY id ASC LIMIT ?",
            (session_id, project_id, limit),
        )
        return [dict(row) for row in rows]

    def list_assistant_agents(self) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM assistant_agents WHERE status = 'active' ORDER BY id ASC")
        return [dict(row) for row in rows]

    def list_assistant_prompts(self) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM assistant_prompt_versions WHERE status = 'active' ORDER BY prompt_key, version")
        return [dict(row) for row in rows]

    def _collect_assistant_context(self, project_id: int) -> dict[str, object]:
        project = self.get_project(project_id)
        goals = self.list_project_goals(project_id)
        journey_state = self.journey_engine_state(project_id)
        partner_matches = self.list_project_matches(project_id, match_type="partner") if hasattr(self, "list_project_matches") else []
        service_matches = self.list_project_matches(project_id, match_type="service") if hasattr(self, "list_project_matches") else []
        decisions = self.list_cognition_decisions(project_id) if hasattr(self, "list_cognition_decisions") else []
        risks = self.list_risk_intelligence(project_id) if hasattr(self, "list_risk_intelligence") else []
        intelligence = self.get_intelligence_workspace(project_id) if hasattr(self, "get_intelligence_workspace") else {}
        nba = self.get_next_best_action(project_id) if hasattr(self, "get_next_best_action") else None
        return ProjectContextEngine().build(
            project=project,
            goals=goals,
            journey_state=journey_state,
            intelligence=intelligence,
            next_action=nba,
            partner_matches=partner_matches,
            service_matches=service_matches,
            decisions=decisions,
            risks=risks,
        )

    def get_assistant_context(self, project_id: int, session_id: int | None = None) -> dict[str, object]:
        context = self._collect_assistant_context(project_id)
        messages: list[dict[str, object]] = []
        if session_id is not None:
            messages = self.list_assistant_messages(session_id, project_id)
        return {
            "project_id": project_id,
            "session_id": session_id,
            "context": context,
            "memory_summary": ConversationMemoryEngine().summarize(messages),
        }

    def refresh_project_rag_index(self, project_id: int) -> dict[str, object]:
        rag = RAGFoundationEngine()
        now = _utcnow()
        docs_indexed = 0
        chunks_indexed = 0
        sources: list[tuple[str, str, str, str]] = []
        project = self.get_project(project_id)
        sources.append(
            (
                f"project-{project_id}",
                "project_metadata",
                str(project.get("title", "Project")),
                f"{project.get('title')} {project.get('objective')} {project.get('location_city')} budget {project.get('budget_min')}-{project.get('budget_max')}",
            )
        )
        if hasattr(self, "list_knowledge_facts"):
            for fact in self.list_knowledge_facts(project_id=project_id):
                sources.append(
                    (
                        f"fact-{fact.get('id')}",
                        "knowledge_fact",
                        str(fact.get("title", "Fact")),
                        f"{fact.get('title')} {fact.get('content')}",
                    )
                )
        if hasattr(self, "get_knowledge_graph"):
            graph = self.get_knowledge_graph(project_id)
            for node in graph.get("nodes", [])[:20]:
                sources.append(
                    (
                        f"node-{node.get('node_key')}",
                        "knowledge_node",
                        str(node.get("title", "Node")),
                        str(node.get("title", "")),
                    )
                )
        with self._transaction() as conn:
            conn.execute("DELETE FROM assistant_rag_chunks WHERE project_id = ?", (project_id,))
            conn.execute("DELETE FROM assistant_rag_documents WHERE project_id = ?", (project_id,))
        for doc_key, source_type, title, content in sources:
            if not content.strip():
                continue
            with self._transaction() as conn:
                cursor = conn.execute(
                    """
                    INSERT INTO assistant_rag_documents (
                        project_id, document_key, source_type, title, content_text, metadata_json, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, '{}', ?, ?)
                    """,
                    (project_id, doc_key, source_type, title, content, now, now),
                )
                doc_id = int(cursor.lastrowid)
            docs_indexed += 1
            for idx, chunk in enumerate(rag.chunk_text(content)):
                chunk_key = f"{doc_key}-chunk-{idx}"
                with self._transaction() as conn:
                    conn.execute(
                        """
                        INSERT INTO assistant_rag_chunks (
                            document_id, project_id, chunk_key, content, token_estimate, metadata_json, created_at
                        ) VALUES (?, ?, ?, ?, ?, '{}', ?)
                        """,
                        (doc_id, project_id, chunk_key, chunk, len(chunk.split()), now),
                    )
                chunks_indexed += 1
        return {"documents": docs_indexed, "chunks": chunks_indexed}

    def retrieve_assistant_rag(self, project_id: int, query: str, *, limit: int = 5) -> list[dict[str, object]]:
        rows = self.all("SELECT chunk_key, content, document_id FROM assistant_rag_chunks WHERE project_id = ?", (project_id,))
        chunks = [{"chunk_key": r["chunk_key"], "content": r["content"], "document_id": r["document_id"]} for r in rows]
        return RAGFoundationEngine().retrieve(query=query, chunks=chunks, limit=limit)

    def chat_assistant(
        self,
        *,
        project_id: int,
        user_id: int,
        message: str,
        session_id: int | None = None,
        agent_key: str | None = None,
        llm_provider=None,
    ) -> dict[str, object]:
        self.seed_assistant_catalog()
        session = (
            self.get_assistant_session(project_id, session_id)
            if session_id is not None
            else None
        )
        if session is None:
            existing = self.one(
                "SELECT * FROM assistant_sessions WHERE project_id = ? AND user_id = ? AND status = 'active' ORDER BY id DESC LIMIT 1",
                (project_id, user_id),
            )
            session = dict(existing) if existing else self.create_assistant_session(project_id=project_id, user_id=user_id)
        session_id = int(session["id"])
        now = _utcnow()
        routing = AgentRouterEngine().route(message=message, project=self.get_project(project_id), default_agent=str(session.get("agent_key", "project_advisor")))
        selected_agent = agent_key or str(routing["agent_key"])
        if selected_agent not in AGENT_KEYS:
            selected_agent = "project_advisor"
        context = self._collect_assistant_context(project_id)
        rag_chunks = self.retrieve_assistant_rag(project_id, message)
        prompt_key = f"system.{selected_agent}" if selected_agent != "project_advisor" else "system.project_advisor"
        system_prompt = get_system_prompt("system.base") + "\n" + get_system_prompt(prompt_key)
        deterministic = DeterministicAssistantEngine().compose(
            agent_key=selected_agent,
            user_message=message,
            context=context,
            rag_chunks=rag_chunks,
            routing=routing,
        )
        if llm_provider is not None:
            response_payload = DeterministicAssistantEngine().maybe_llm_enhance(
                provider=llm_provider,
                system_prompt=system_prompt,
                user_message=message,
                context=context,
                deterministic=deterministic,
            )
        else:
            response_payload = deterministic
        user_key = f"user-{now}"
        with self._transaction() as conn:
            user_cursor = conn.execute(
                """
                INSERT INTO assistant_messages (session_id, project_id, message_key, role, content, metadata_json, created_at)
                VALUES (?, ?, ?, 'user', ?, '{}', ?)
                """,
                (session_id, project_id, user_key, message, now),
            )
            user_message_id = int(user_cursor.lastrowid)
            assistant_key = f"assistant-{now}"
            assistant_cursor = conn.execute(
                """
                INSERT INTO assistant_messages (session_id, project_id, message_key, role, content, metadata_json, created_at)
                VALUES (?, ?, ?, 'assistant', ?, ?, ?)
                """,
                (session_id, project_id, assistant_key, str(response_payload["content"]), _json({"agent_key": selected_agent}), now),
            )
            assistant_message_id = int(assistant_cursor.lastrowid)
            conn.execute(
                """
                INSERT INTO assistant_turns (
                    session_id, project_id, user_message_id, assistant_message_id,
                    agent_key, mode, provider, fallback_used, routing_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    session_id,
                    project_id,
                    user_message_id,
                    assistant_message_id,
                    selected_agent,
                    response_payload["mode"],
                    response_payload["provider"],
                    1 if response_payload.get("fallback_used") else 0,
                    _json(routing),
                    now,
                ),
            )
            conn.execute(
                "UPDATE assistant_sessions SET agent_key = ?, updated_at = ? WHERE id = ?",
                (selected_agent, now, session_id),
            )
        snapshot_key = f"ctx-{now}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO assistant_context_snapshots (project_id, session_id, snapshot_key, context_json, sources_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (project_id, session_id, snapshot_key, _json(context), _json([c.get("chunk_key") for c in rag_chunks]), now),
            )
            conn.execute(
                """
                INSERT INTO assistant_rag_retrievals (session_id, project_id, query_text, chunks_json, score, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (session_id, project_id, message, _json(rag_chunks), rag_chunks[0]["score"] if rag_chunks else 0, now),
            )
        messages = self.list_assistant_messages(session_id, project_id)
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO assistant_memory_summaries (session_id, project_id, summary_text, message_count, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (session_id, project_id, ConversationMemoryEngine().summarize(messages), len(messages), now),
            )
        turn = self.one("SELECT * FROM assistant_turns WHERE session_id = ? ORDER BY id DESC LIMIT 1", (session_id,))
        session = self.get_assistant_session(project_id, session_id)
        self.record_event("assistant_chat_completed", {"project_id": project_id, "session_id": session_id, "agent_key": selected_agent})
        return {
            "session": session,
            "user_message": self.one("SELECT * FROM assistant_messages WHERE id = ?", (user_message_id,)),
            "assistant_message": self.one("SELECT * FROM assistant_messages WHERE id = ?", (assistant_message_id,)),
            "turn": turn,
            "agent_key": selected_agent,
            "mode": response_payload["mode"],
            "provider": response_payload["provider"],
            "fallback_used": response_payload.get("fallback_used"),
            "rag_chunks": rag_chunks,
            "context_snapshot_key": snapshot_key,
        }
