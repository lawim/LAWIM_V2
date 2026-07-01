from __future__ import annotations


def knowledge_node_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "node_key": row.get("node_key"),
        "node_type": row.get("node_type"),
        "entity_type": row.get("entity_type"),
        "entity_id": row.get("entity_id"),
        "title": row.get("title"),
        "status": row.get("status"),
    }


def knowledge_graph_dto(payload: dict[str, object]) -> dict[str, object]:
    return {
        "nodes": [knowledge_node_dto(n) for n in payload.get("nodes", [])],
        "edges": payload.get("edges", []),
        "relations": payload.get("relations", []),
    }


def decision_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "project_id": row.get("project_id"),
        "decision_key": row.get("decision_key"),
        "title": row.get("title"),
        "status": row.get("status"),
        "reason": row.get("reason"),
        "confidence": row.get("confidence"),
        "priority": row.get("priority"),
        "alternatives": row.get("alternatives", []),
        "tradeoffs": row.get("tradeoffs", []),
        "explainability": row.get("explainability", {}),
        "next_action": row.get("next_action"),
        "evidences": row.get("evidences", []),
        "histories": row.get("histories", []),
    }


def simulation_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "scenario_key": row.get("scenario_key"),
        "title": row.get("title"),
        "input": row.get("input", row.get("input_json")),
        "output": row.get("output", row.get("output_json")),
        "impacts": row.get("impacts", row.get("impacts_json")),
        "recommendations": row.get("recommendations", []),
        "actions": row.get("actions", []),
        "priorities": row.get("priorities", []),
        "status": row.get("status"),
        "created_at": row.get("created_at"),
    }


def reasoning_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "trace_key": row.get("trace_key"),
        "rules_fired": row.get("rules_fired", []),
        "conclusions": row.get("conclusions", []),
        "merged_priority": row.get("merged_priority", []),
        "created_at": row.get("created_at"),
    }


def next_best_action_dto(row: dict[str, object] | None) -> dict[str, object] | None:
    if row is None:
        return None
    return {
        "action_key": row.get("action_key"),
        "title": row.get("title"),
        "score": row.get("score"),
        "confidence": row.get("confidence"),
        "justification": row.get("justification"),
        "explanation": row.get("explanation", {}),
        "factors": row.get("factors", []),
    }


def risk_intelligence_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "risk_key": row.get("risk_key"),
        "severity": row.get("severity"),
        "likelihood": row.get("likelihood"),
        "score": row.get("score"),
        "mitigation": row.get("mitigation", []),
        "description": row.get("description"),
        "computed_at": row.get("computed_at"),
    }


def opportunity_intelligence_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "opportunity_key": row.get("opportunity_key"),
        "value_score": row.get("value_score"),
        "opportunity_score": row.get("opportunity_score"),
        "description": row.get("description"),
        "kind": row.get("kind"),
        "computed_at": row.get("computed_at"),
    }


def intelligence_workspace_dto(payload: dict[str, object]) -> dict[str, object]:
    return {
        "project_id": payload.get("project_id"),
        "snapshot": payload.get("snapshot", {}),
        "graph_summary": payload.get("graph_summary"),
        "next_best_action": next_best_action_dto(payload.get("next_best_action")),
        "decisions": [decision_dto(d) for d in payload.get("decisions", [])],
        "risks": [risk_intelligence_dto(r) for r in payload.get("risks", [])],
        "opportunities": [opportunity_intelligence_dto(o) for o in payload.get("opportunities", [])],
        "reasoning": [reasoning_dto(r) for r in payload.get("reasoning", [])],
    }
