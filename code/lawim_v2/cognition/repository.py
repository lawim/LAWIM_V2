from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from ..repository_introspection import table_exists
from .constants import SIMULATION_SCENARIOS
from .engines import (
    DecisionPlatformEngine,
    KnowledgeGraphEngine,
    NextBestActionEngine,
    OpportunityIntelligenceEngine,
    ReasoningEngine,
    RiskIntelligenceEngine,
    SimulationEngine,
)


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


class CognitionRepositoryMixin:
    def cognition_tables_present(self) -> bool:
        return table_exists(self, "knowledge_nodes")

    def bootstrap_project_cognition(self, project_id: int) -> None:
        self.refresh_project_cognition(project_id)

    def refresh_project_cognition(self, project_id: int) -> dict[str, object]:
        ctx = self._collect_cognition_context(project_id)
        graph_engine = KnowledgeGraphEngine()
        graph = graph_engine.build_graph(**ctx["graph_inputs"])
        node_map = self._persist_knowledge_graph(project_id, graph)
        reasoning = ReasoningEngine().run(
            project=ctx["project"],
            goals=ctx["goals"],
            risks=ctx["risks"],
            opportunities=ctx["opportunities"],
            constraints=ctx["constraints"],
            journey_state=ctx["journey_state"],
            partner_matches=ctx["partner_matches"],
            workflow_instance=ctx["workflow_instance"],
        )
        self._persist_reasoning(project_id, reasoning)
        evidences = self._build_evidences(ctx)
        decision_payload = DecisionPlatformEngine().evaluate(
            project=ctx["project"],
            goals=ctx["goals"],
            risks=ctx["risks"],
            opportunities=ctx["opportunities"],
            constraints=ctx["constraints"],
            reasoning=reasoning,
            evidences=evidences,
        )
        decision = self._persist_cognition_decision(project_id, decision_payload)
        risk_scores = RiskIntelligenceEngine().analyze(
            project=ctx["project"],
            risks=ctx["risks"],
            journey_state=ctx["journey_state"],
            workflow_instance=ctx["workflow_instance"],
        )
        opp_scores = OpportunityIntelligenceEngine().analyze(
            project=ctx["project"],
            opportunities=ctx["opportunities"],
            partner_matches=ctx["partner_matches"],
            service_matches=ctx["service_matches"],
        )
        self._persist_risk_scores(project_id, risk_scores)
        self._persist_opportunity_scores(project_id, opp_scores)
        nba = NextBestActionEngine().compute(
            project=ctx["project"],
            decision=decision_payload,
            reasoning=reasoning,
            risks=ctx["risks"],
            workflow_instance=ctx["workflow_instance"],
            partner_matches=ctx["partner_matches"],
            cost_summary=ctx.get("cost_summary"),
        )
        self._persist_next_best_action(project_id, nba)
        snapshot_payload = {
            "graph": {"nodes": len(graph["nodes"]), "edges": len(graph["edges"])},
            "reasoning": reasoning,
            "decision": decision_payload,
            "next_best_action": nba,
            "risks": risk_scores[:5],
            "opportunities": opp_scores[:5],
        }
        self._persist_intelligence_snapshot(project_id, snapshot_payload)
        self._persist_knowledge_snapshot(project_id, graph, node_map)
        self.record_event("project_cognition_refreshed", {"project_id": project_id})
        return snapshot_payload

    def _collect_cognition_context(self, project_id: int) -> dict[str, object]:
        project = self.get_project(project_id)
        goals = self.list_project_goals(project_id)
        needs = self.list_project_needs(project_id)
        constraints = self.list_project_constraints(project_id)
        life_events = self.list_life_events(project_id)
        decisions = self.list_project_decisions(project_id)
        recommendations = self.list_project_recommendations(project_id)
        tasks = self.list_project_tasks(project_id)
        actions = self.list_project_actions(project_id)
        risks = self.list_project_risks(project_id)
        opportunities = self.list_project_opportunities(project_id)
        knowledge_facts = self.list_knowledge_facts(project_id=project_id)
        resources = self.list_project_resources(project_id)
        journey_state = self.journey_engine_state(project_id)
        partner_matches = self.list_project_matches(project_id, match_type="partner") if hasattr(self, "list_project_matches") else []
        service_matches = self.list_project_matches(project_id, match_type="service") if hasattr(self, "list_project_matches") else []
        workflow_instance = self.get_project_workflow_instance(project_id) if hasattr(self, "get_project_workflow_instance") else None
        cost_summary = None
        if hasattr(self, "get_project_orchestration"):
            orch = self.get_project_orchestration(project_id)
            cost_summary = orch.get("cost_summary")
        return {
            "project": project,
            "goals": goals,
            "needs": needs,
            "constraints": constraints,
            "life_events": life_events,
            "decisions": decisions,
            "recommendations": recommendations,
            "tasks": tasks,
            "actions": actions,
            "risks": risks,
            "opportunities": opportunities,
            "knowledge_facts": knowledge_facts,
            "resources": resources,
            "journey_state": journey_state,
            "partner_matches": partner_matches,
            "service_matches": service_matches,
            "workflow_instance": workflow_instance,
            "cost_summary": cost_summary,
            "graph_inputs": {
                "project": project,
                "goals": goals,
                "needs": needs,
                "constraints": constraints,
                "life_events": life_events,
                "decisions": decisions,
                "recommendations": recommendations,
                "tasks": tasks,
                "actions": actions,
                "risks": risks,
                "opportunities": opportunities,
                "knowledge_facts": knowledge_facts,
                "resources": resources,
                "partner_matches": partner_matches,
                "service_matches": service_matches,
            },
        }

    def _persist_knowledge_graph(self, project_id: int, graph: dict[str, object]) -> dict[str, int]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute("DELETE FROM knowledge_edges WHERE project_id = ?", (project_id,))
            conn.execute("DELETE FROM knowledge_relations WHERE project_id = ?", (project_id,))
            conn.execute("DELETE FROM knowledge_nodes WHERE project_id = ?", (project_id,))
        node_map: dict[str, int] = {}
        for node in graph["nodes"]:
            now = _utcnow()
            with self._transaction() as conn:
                cursor = conn.execute(
                    """
                    INSERT INTO knowledge_nodes (
                        project_id, node_key, node_type, entity_type, entity_id, title,
                        content_json, status, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, 'active', ?, ?)
                    """,
                    (
                        project_id,
                        node["node_key"],
                        node["node_type"],
                        node["entity_type"],
                        node.get("entity_id"),
                        node["title"],
                        _json(node.get("content") or {}),
                        now,
                        now,
                    ),
                )
                node_map[str(node["node_key"])] = int(cursor.lastrowid)
            self._record_history(project_id, node_map[str(node["node_key"])], "created", {}, node)
        for edge in graph["edges"]:
            src = node_map.get(str(edge["source_node_key"]))
            tgt = node_map.get(str(edge["target_node_key"]))
            if src and tgt:
                with self._transaction() as conn:
                    conn.execute(
                        """
                        INSERT INTO knowledge_edges (
                            project_id, source_node_id, target_node_id, edge_type, weight, metadata_json, created_at
                        ) VALUES (?, ?, ?, ?, ?, '{}', ?)
                        """,
                        (project_id, src, tgt, edge["edge_type"], edge["weight"], _utcnow()),
                    )
        for rel in graph.get("relations", []):
            subj = node_map.get(str(rel["subject_node_key"]))
            obj = node_map.get(str(rel["object_node_key"]))
            if subj and obj:
                with self._transaction() as conn:
                    conn.execute(
                        """
                        INSERT INTO knowledge_relations (
                            project_id, relation_key, subject_node_id, object_node_id,
                            relation_type, confidence, metadata_json, created_at
                        ) VALUES (?, ?, ?, ?, ?, ?, '{}', ?)
                        """,
                        (project_id, rel["relation_key"], subj, obj, rel["relation_type"], rel["confidence"], _utcnow()),
                    )
        return node_map

    def _record_history(self, project_id: int, node_id: int, change_type: str, before: dict, after: dict) -> None:
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO knowledge_history (project_id, node_id, change_type, before_json, after_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (project_id, node_id, change_type, _json(before), _json(after), _utcnow()),
            )

    def _persist_reasoning(self, project_id: int, reasoning: dict[str, object]) -> None:
        now = _utcnow()
        trace_key = f"trace-{now}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO reasoning_traces (
                    project_id, trace_key, rules_fired_json, conclusions_json, merged_priority_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    project_id,
                    trace_key,
                    _json(reasoning.get("rules_fired", [])),
                    _json(reasoning.get("conclusions", [])),
                    _json(reasoning.get("merged_priority", [])),
                    now,
                ),
            )
        for inf in reasoning.get("inferences", []):
            with self._transaction() as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO knowledge_inferences (
                        project_id, inference_key, premise_json, conclusion, confidence, rule_key, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        project_id,
                        inf["inference_key"],
                        _json(inf.get("premise", [])),
                        inf["conclusion"],
                        inf["confidence"],
                        inf["rule_key"],
                        now,
                    ),
                )

    def _build_evidences(self, ctx: dict[str, object]) -> list[dict[str, object]]:
        evidences: list[dict[str, object]] = []
        for idx, risk in enumerate(ctx["risks"][:3]):  # type: ignore[index]
            evidences.append({"evidence_key": f"risk-{idx}", "label": str(risk.get("description", "Risque")), "source_type": "risk", "source_id": risk.get("id"), "weight": 60})
        for idx, goal in enumerate(ctx["goals"][:2]):  # type: ignore[index]
            evidences.append({"evidence_key": f"goal-{idx}", "label": str(goal.get("title", "Goal")), "source_type": "goal", "source_id": goal.get("id"), "weight": 50})
        return evidences

    def _persist_cognition_decision(self, project_id: int, payload: dict[str, object]) -> dict[str, object]:
        now = _utcnow()
        existing = self.one("SELECT id, status FROM cognition_decisions WHERE project_id = ? AND decision_key = ?", (project_id, payload["decision_key"]))
        if existing:
            with self._transaction() as conn:
                conn.execute(
                    """
                    UPDATE cognition_decisions SET title=?, reason=?, confidence=?, priority=?, alternatives_json=?,
                    tradeoffs_json=?, explainability_json=?, next_action=?, updated_at=? WHERE id=?
                    """,
                    (
                        payload["title"],
                        payload["reason"],
                        payload["confidence"],
                        payload["priority"],
                        _json(payload.get("alternatives", [])),
                        _json(payload.get("tradeoffs", [])),
                        _json(payload.get("explainability", {})),
                        payload.get("next_action"),
                        now,
                        existing["id"],
                    ),
                )
                conn.execute(
                    "INSERT INTO decision_histories (decision_id, project_id, from_status, to_status, note, created_at) VALUES (?, ?, ?, 'proposed', 'refresh', ?)",
                    (existing["id"], project_id, existing.get("status"), now),
                )
            decision_id = int(existing["id"])
        else:
            with self._transaction() as conn:
                cursor = conn.execute(
                    """
                    INSERT INTO cognition_decisions (
                        project_id, decision_key, title, status, reason, confidence, priority,
                        alternatives_json, tradeoffs_json, explainability_json, next_action, created_at, updated_at
                    ) VALUES (?, ?, ?, 'proposed', ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        project_id,
                        payload["decision_key"],
                        payload["title"],
                        payload["reason"],
                        payload["confidence"],
                        payload["priority"],
                        _json(payload.get("alternatives", [])),
                        _json(payload.get("tradeoffs", [])),
                        _json(payload.get("explainability", {})),
                        payload.get("next_action"),
                        now,
                        now,
                    ),
                )
                decision_id = int(cursor.lastrowid)
        with self._transaction() as conn:
            conn.execute("DELETE FROM decision_evidences WHERE decision_id = ?", (decision_id,))
        for ev in payload.get("evidences", []):
            with self._transaction() as conn:
                conn.execute(
                    """
                    INSERT INTO decision_evidences (
                        decision_id, project_id, evidence_key, label, source_type, source_id, weight, content_json, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, '{}', ?)
                    """,
                    (decision_id, project_id, ev["evidence_key"], ev["label"], ev["source_type"], ev.get("source_id"), ev.get("weight", 50), now),
                )
        row = self.one("SELECT * FROM cognition_decisions WHERE id = ?", (decision_id,))
        assert row is not None
        return dict(row)

    def _persist_risk_scores(self, project_id: int, scores: list[dict[str, object]]) -> None:
        now = _utcnow()
        for item in scores:
            with self._transaction() as conn:
                conn.execute(
                    """
                    INSERT INTO risk_intelligence_scores (
                        project_id, risk_key, severity, likelihood, score, mitigation_json, computed_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (project_id, item["risk_key"], item["severity"], item["likelihood"], item["score"], _json(item.get("mitigation", [])), now),
                )

    def _persist_opportunity_scores(self, project_id: int, scores: list[dict[str, object]]) -> None:
        now = _utcnow()
        for item in scores:
            with self._transaction() as conn:
                conn.execute(
                    """
                    INSERT INTO opportunity_intelligence_scores (
                        project_id, opportunity_key, value_score, opportunity_score, description, computed_at
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (project_id, item["opportunity_key"], item["value_score"], item["opportunity_score"], item["description"], now),
                )

    def _persist_next_best_action(self, project_id: int, nba: dict[str, object]) -> None:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO next_best_actions (
                    project_id, action_key, title, score, confidence, justification,
                    explanation_json, factors_json, status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'active', ?, ?)
                """,
                (
                    project_id,
                    nba["action_key"],
                    nba["title"],
                    nba["score"],
                    nba["confidence"],
                    nba["justification"],
                    _json(nba.get("explanation", {})),
                    _json(nba.get("factors", [])),
                    now,
                    now,
                ),
            )

    def _persist_intelligence_snapshot(self, project_id: int, payload: dict[str, object]) -> None:
        now = _utcnow()
        key = f"intel-{now}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO intelligence_snapshots (project_id, snapshot_key, payload_json, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (project_id, key, _json(payload), now),
            )

    def _persist_knowledge_snapshot(self, project_id: int, graph: dict[str, object], node_map: dict[str, int]) -> None:
        now = _utcnow()
        key = f"graph-{now}"
        graph_json = {"node_keys": list(node_map.keys()), "edge_count": len(graph.get("edges", [])), "relation_count": len(graph.get("relations", []))}
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO knowledge_snapshots (
                    project_id, snapshot_key, graph_json, node_count, edge_count, relation_count, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (project_id, key, _json(graph_json), len(node_map), len(graph.get("edges", [])), len(graph.get("relations", [])), now),
            )

    def get_knowledge_graph(self, project_id: int) -> dict[str, object]:
        nodes = self.all("SELECT * FROM knowledge_nodes WHERE project_id = ? ORDER BY id ASC", (project_id,))
        edges_raw = self.all(
            """
            SELECT e.*, sn.node_key AS source_key, tn.node_key AS target_key
            FROM knowledge_edges e
            JOIN knowledge_nodes sn ON sn.id = e.source_node_id
            JOIN knowledge_nodes tn ON tn.id = e.target_node_id
            WHERE e.project_id = ?
            """,
            (project_id,),
        )
        relations = self.all("SELECT * FROM knowledge_relations WHERE project_id = ? ORDER BY id ASC", (project_id,))
        return {"nodes": nodes, "edges": edges_raw, "relations": relations}

    def get_knowledge_context(self, project_id: int) -> dict[str, object]:
        ctx = self._collect_cognition_context(project_id)
        latest = self.one("SELECT * FROM intelligence_snapshots WHERE project_id = ? ORDER BY id DESC LIMIT 1", (project_id,))
        trace = self.one("SELECT * FROM reasoning_traces WHERE project_id = ? ORDER BY id DESC LIMIT 1", (project_id,))
        return {
            "project_id": project_id,
            "goals_count": len(ctx["goals"]),  # type: ignore[arg-type]
            "risks_count": len(ctx["risks"]),  # type: ignore[arg-type]
            "constraints_count": len(ctx["constraints"]),  # type: ignore[arg-type]
            "latest_intelligence": _parse_json(str(latest["payload_json"])) if latest else None,
            "latest_reasoning": {
                "conclusions": _parse_json(str(trace["conclusions_json"])) if trace else [],
                "merged_priority": _parse_json(str(trace["merged_priority_json"])) if trace else [],
            },
        }

    def list_cognition_decisions(self, project_id: int) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM cognition_decisions WHERE project_id = ? ORDER BY id DESC", (project_id,))
        return [self._decision_dto(row) for row in rows]

    def get_cognition_decision(self, project_id: int, decision_id: int) -> dict[str, object]:
        row = self.one("SELECT * FROM cognition_decisions WHERE id = ? AND project_id = ?", (decision_id, project_id))
        if row is None:
            from ..errors import NotFoundError
            raise NotFoundError("decision not found")
        return self._decision_dto(row)

    def _decision_dto(self, row: dict[str, object]) -> dict[str, object]:
        evidences = self.all("SELECT * FROM decision_evidences WHERE decision_id = ? ORDER BY id ASC", (row["id"],))
        histories = self.all("SELECT * FROM decision_histories WHERE decision_id = ? ORDER BY id ASC", (row["id"],))
        return {
            **dict(row),
            "alternatives": _parse_json(str(row.get("alternatives_json"))) or [],
            "tradeoffs": _parse_json(str(row.get("tradeoffs_json"))) or [],
            "explainability": _parse_json(str(row.get("explainability_json"))) or {},
            "evidences": evidences,
            "histories": histories,
        }

    def list_reasoning_traces(self, project_id: int) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM reasoning_traces WHERE project_id = ? ORDER BY id DESC LIMIT 10", (project_id,))
        return [
            {
                **dict(row),
                "rules_fired": _parse_json(str(row.get("rules_fired_json"))) or [],
                "conclusions": _parse_json(str(row.get("conclusions_json"))) or [],
                "merged_priority": _parse_json(str(row.get("merged_priority_json"))) or [],
            }
            for row in rows
        ]

    def run_simulation(self, project_id: int, scenario_key: str, parameters: dict[str, object] | None = None) -> dict[str, object]:
        ctx = self._collect_cognition_context(project_id)
        result = SimulationEngine().run(
            scenario_key=scenario_key,
            project=ctx["project"],  # type: ignore[arg-type]
            goals=ctx["goals"],  # type: ignore[arg-type]
            parameters=parameters,
        )
        now = _utcnow()
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO simulation_runs (
                    project_id, scenario_key, title, input_json, output_json, impacts_json, status, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, 'completed', ?)
                """,
                (project_id, scenario_key, result["title"], _json(result["input"]), _json(result["output"]), _json(result["impacts"]), now),
            )
            result["id"] = int(cursor.lastrowid)
        return result

    def list_simulation_runs(self, project_id: int) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM simulation_runs WHERE project_id = ? ORDER BY id DESC LIMIT 20", (project_id,))
        return [
            {
                **dict(row),
                "input": _parse_json(str(row.get("input_json"))),
                "output": _parse_json(str(row.get("output_json"))),
                "impacts": _parse_json(str(row.get("impacts_json"))),
            }
            for row in rows
        ]

    def list_simulation_scenarios(self) -> list[dict[str, object]]:
        return [{"scenario_key": k, **v} for k, v in SIMULATION_SCENARIOS.items()]

    def get_next_best_action(self, project_id: int) -> dict[str, object] | None:
        row = self.one("SELECT * FROM next_best_actions WHERE project_id = ? AND status = 'active' ORDER BY score DESC LIMIT 1", (project_id,))
        if row is None:
            return None
        return {
            **dict(row),
            "explanation": _parse_json(str(row.get("explanation_json"))) or {},
            "factors": _parse_json(str(row.get("factors_json"))) or [],
        }

    def list_risk_intelligence(self, project_id: int) -> list[dict[str, object]]:
        rows = self.all(
            "SELECT * FROM risk_intelligence_scores WHERE project_id = ? ORDER BY computed_at DESC, score DESC LIMIT 20",
            (project_id,),
        )
        return [{**dict(row), "mitigation": _parse_json(str(row.get("mitigation_json"))) or []} for row in rows]

    def list_opportunity_intelligence(self, project_id: int) -> list[dict[str, object]]:
        return self.all(
            "SELECT * FROM opportunity_intelligence_scores WHERE project_id = ? ORDER BY computed_at DESC, opportunity_score DESC LIMIT 20",
            (project_id,),
        )

    def get_intelligence_workspace(self, project_id: int) -> dict[str, object]:
        snapshot = self.one("SELECT * FROM intelligence_snapshots WHERE project_id = ? ORDER BY id DESC LIMIT 1", (project_id,))
        return {
            "project_id": project_id,
            "snapshot": _parse_json(str(snapshot["payload_json"])) if snapshot else {},
            "graph_summary": self.one("SELECT * FROM knowledge_snapshots WHERE project_id = ? ORDER BY id DESC LIMIT 1", (project_id,)),
            "next_best_action": self.get_next_best_action(project_id),
            "decisions": self.list_cognition_decisions(project_id)[:3],
            "risks": self.list_risk_intelligence(project_id)[:5],
            "opportunities": self.list_opportunity_intelligence(project_id)[:5],
            "reasoning": self.list_reasoning_traces(project_id)[:1],
        }

    def list_knowledge_history(self, project_id: int, limit: int = 50) -> list[dict[str, object]]:
        return self.all("SELECT * FROM knowledge_history WHERE project_id = ? ORDER BY id DESC LIMIT ?", (project_id, limit))

    def list_knowledge_inferences(self, project_id: int) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM knowledge_inferences WHERE project_id = ? ORDER BY id DESC", (project_id,))
        return [{**dict(row), "premise": _parse_json(str(row.get("premise_json"))) or []} for row in rows]
