from __future__ import annotations

from ..intelligent.engines import DecisionEngine
from .constants import LIKELIHOOD_WEIGHTS, REASONING_RULES, SEVERITY_WEIGHTS, SIMULATION_SCENARIOS


class KnowledgeGraphEngine:
    def build_graph(
        self,
        *,
        project: dict[str, object],
        goals: list[dict[str, object]],
        needs: list[dict[str, object]],
        constraints: list[dict[str, object]],
        life_events: list[dict[str, object]],
        decisions: list[dict[str, object]],
        recommendations: list[dict[str, object]],
        tasks: list[dict[str, object]],
        actions: list[dict[str, object]],
        risks: list[dict[str, object]],
        opportunities: list[dict[str, object]],
        knowledge_facts: list[dict[str, object]],
        resources: list[dict[str, object]],
        partner_matches: list[dict[str, object]],
        service_matches: list[dict[str, object]],
    ) -> dict[str, object]:
        nodes: list[dict[str, object]] = []
        edges: list[dict[str, object]] = []
        relations: list[dict[str, object]] = []
        project_node = self._node("project", "project", int(project["id"]), str(project.get("title", "Project")), project)
        nodes.append(project_node)
        for entity_type, rows, key_field, edge_type in (
            ("goal", goals, "goal_key", "has_goal"),
            ("need", needs, "need_key", "has_need"),
            ("constraint", constraints, "constraint_type", "has_constraint"),
            ("life_event", life_events, "event_type", "triggered_by"),
            ("decision", decisions, "decision_key", "informs"),
            ("recommendation", recommendations, "recommendation_key", "recommends"),
            ("task", tasks, "title", "requires"),
            ("action", actions, "action_key", "requires"),
            ("risk", risks, "risk_key", "blocks"),
            ("opportunity", opportunities, "opportunity_key", "enables"),
            ("knowledge_fact", knowledge_facts, "fact_key", "informs"),
            ("resource", resources, "resource_type", "linked_to"),
        ):
            for row in rows:
                eid = int(row["id"]) if row.get("id") else None
                key = str(row.get(key_field) or eid)
                node = self._node(entity_type, entity_type, eid, key, row)
                nodes.append(node)
                edges.append(self._edge(project_node["node_key"], node["node_key"], edge_type, 70))
        for match in partner_matches:
            eid = match.get("partner_profile_id")
            node = self._node("partner", "partner", int(eid) if eid else None, str(match.get("partner_type", "partner")), match)
            nodes.append(node)
            edges.append(self._edge(project_node["node_key"], node["node_key"], "assigned_to", int(match.get("score") or 50)))
        for match in service_matches:
            eid = match.get("service_catalog_id")
            node = self._node("service", "service", int(eid) if eid else None, str(match.get("service_key", "service")), match)
            nodes.append(node)
            edges.append(self._edge(project_node["node_key"], node["node_key"], "requires", int(match.get("score") or 50)))
        goal_nodes = [n for n in nodes if n["entity_type"] == "goal"]
        constraint_nodes = [n for n in nodes if n["entity_type"] == "constraint"]
        if goal_nodes and constraint_nodes:
            relations.append(
                {
                    "relation_key": f"rel-{goal_nodes[0]['node_key']}-{constraint_nodes[0]['node_key']}",
                    "subject_node_key": goal_nodes[0]["node_key"],
                    "object_node_key": constraint_nodes[0]["node_key"],
                    "relation_type": "conflict",
                    "confidence": 60,
                }
            )
        return {"nodes": nodes, "edges": edges, "relations": relations}

    def _node(self, node_type: str, entity_type: str, entity_id: int | None, title: str, content: dict[str, object]) -> dict[str, object]:
        return {
            "node_key": f"{entity_type}-{entity_id or title}",
            "node_type": node_type,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "title": title,
            "content": content,
        }

    def _edge(self, source: str, target: str, edge_type: str, weight: int) -> dict[str, object]:
        return {"source_node_key": source, "target_node_key": target, "edge_type": edge_type, "weight": weight}


class ReasoningEngine:
    def run(
        self,
        *,
        project: dict[str, object],
        goals: list[dict[str, object]],
        risks: list[dict[str, object]],
        opportunities: list[dict[str, object]],
        constraints: list[dict[str, object]],
        journey_state: dict[str, object],
        partner_matches: list[dict[str, object]],
        workflow_instance: dict[str, object] | None,
    ) -> dict[str, object]:
        context = {
            "missing_budget": project.get("budget_min") is None or project.get("budget_max") is None,
            "high_risk": any(str(r.get("severity")) in {"high", "critical"} and str(r.get("status")) == "open" for r in risks),
            "journey_blocked": int(journey_state.get("blocked_steps") or 0) > 0,
            "open_opportunity": any(str(o.get("status")) == "open" for o in opportunities),
            "workflow_step_pending": bool(
                workflow_instance and any(str(s.get("status")) == "pending" for s in (workflow_instance.get("instance_steps") or []))
            ),
            "missing_partner_match": len(partner_matches) == 0,
            "has_goals": bool(goals),
            "has_constraints": bool(constraints),
        }
        fired: list[dict[str, object]] = []
        conclusions: list[str] = []
        inferences: list[dict[str, object]] = []
        for rule in REASONING_RULES:
            if context.get(rule["condition"]):
                fired.append({"rule_key": rule["key"], "condition": rule["condition"]})
                conclusions.append(rule["conclusion"])
                inferences.append(
                    {
                        "inference_key": rule["key"],
                        "premise": [rule["condition"]],
                        "conclusion": rule["conclusion"],
                        "confidence": 75,
                        "rule_key": rule["key"],
                    }
                )
        merged = list(conclusions)
        if context.get("high_risk"):
            merged.insert(0, "Traiter les risques élevés en priorité")
        if context.get("missing_budget"):
            merged.insert(0, "Qualifier le budget avant d'avancer")
        return {"rules_fired": fired, "conclusions": conclusions, "inferences": inferences, "merged_priority": merged[:8], "context": context}


class DecisionPlatformEngine:
    def evaluate(
        self,
        *,
        project: dict[str, object],
        goals: list[dict[str, object]],
        risks: list[dict[str, object]],
        opportunities: list[dict[str, object]],
        constraints: list[dict[str, object]],
        reasoning: dict[str, object],
        evidences: list[dict[str, object]],
    ) -> dict[str, object]:
        base = DecisionEngine().evaluate(
            project=project, goals=goals, risks=risks, opportunities=opportunities, constraints=constraints
        )
        return {
            **base,
            "priority": "high" if reasoning.get("context", {}).get("high_risk") else "normal",
            "explainability": {
                "rules_fired": [r["rule_key"] for r in reasoning.get("rules_fired", [])],
                "evidence_count": len(evidences),
                "factors": reasoning.get("merged_priority", [])[:5],
                "method": "deterministic_rule_engine_v1",
            },
            "evidences": evidences,
        }


class SimulationEngine:
    def run(self, *, scenario_key: str, project: dict[str, object], goals: list[dict[str, object]], parameters: dict[str, object] | None = None) -> dict[str, object]:
        if scenario_key not in SIMULATION_SCENARIOS:
            raise ValueError(f"unsupported scenario: {scenario_key}")
        spec = SIMULATION_SCENARIOS[scenario_key]
        params = dict(parameters or {})
        param_key = str(spec["parameter"])
        if param_key not in params:
            params[param_key] = spec["default_value"]
        budget_max = int(project.get("budget_max") or 0)
        impacts: list[dict[str, object]] = []
        recommendations: list[str] = []
        actions: list[str] = []
        priorities: list[str] = []
        if scenario_key == "budget_increase":
            delta = int(params.get("budget_delta_percent", 15))
            impacts.append({"type": "budget", "before": budget_max, "after": int(budget_max * (1 + delta / 100)) if budget_max else 0})
            recommendations.append("Élargir le périmètre de recherche")
            actions.append("Mettre à jour le budget projet")
        elif scenario_key == "budget_decrease":
            delta = int(params.get("budget_delta_percent", -10))
            impacts.append({"type": "budget", "before": budget_max, "after": int(budget_max * (1 + delta / 100)) if budget_max else 0})
            recommendations.append("Réduire les critères de surface")
            priorities.append("Optimiser le coût")
        elif scenario_key == "new_loan":
            impacts.append({"type": "funding", "loan_amount": int(params.get("loan_amount", 0))})
            recommendations.append("Contacter un partenaire bancaire")
            actions.append("Lancer préqualification financement")
        elif scenario_key == "relocation":
            city = str(params.get("new_city", "Douala"))
            impacts.append({"type": "location", "city": city})
            recommendations.append(f"Recentrer la recherche sur {city}")
        elif scenario_key == "birth":
            impacts.append({"type": "need", "space_increase": params.get("space_need_increase", 1)})
            recommendations.append("Prioriser logement familial")
        elif scenario_key == "construction_delay":
            impacts.append({"type": "timeline", "delay_days": int(params.get("delay_days", 30))})
            recommendations.append("Renégocier le planning chantier")
        elif scenario_key == "interest_rate_change":
            impacts.append({"type": "finance", "rate_delta": float(params.get("rate_delta_percent", 2))})
            recommendations.append("Recalculer la capacité d'emprunt")
        elif scenario_key == "new_partner":
            impacts.append({"type": "partner", "partner_type": str(params.get("partner_type", "real_estate_agency"))})
            actions.append("Mobiliser un partenaire")
        elif scenario_key == "prior_sale":
            impacts.append({"type": "funding", "sale_proceeds": int(params.get("sale_proceeds", 0))})
            recommendations.append("Planifier la vente préalable")
        return {
            "scenario_key": scenario_key,
            "title": str(spec["title"]),
            "input": params,
            "output": {"goal_key": str(goals[0]["goal_key"]) if goals else str(project.get("project_type", "other")), "parameters": params},
            "impacts": impacts,
            "recommendations": recommendations,
            "actions": actions,
            "priorities": priorities,
        }


class NextBestActionEngine:
    def compute(
        self,
        *,
        project: dict[str, object],
        decision: dict[str, object],
        reasoning: dict[str, object],
        risks: list[dict[str, object]],
        workflow_instance: dict[str, object] | None,
        partner_matches: list[dict[str, object]],
        cost_summary: dict[str, object] | None,
    ) -> dict[str, object]:
        factors: list[dict[str, object]] = []
        score = 50
        title = str(decision.get("next_action") or "Poursuivre le parcours")
        if reasoning.get("merged_priority"):
            title = str(reasoning["merged_priority"][0])
            factors.append({"code": "reasoning", "label": "Raisonnement métier", "weight": 20})
            score += 15
        if any(str(r.get("severity")) in {"high", "critical"} for r in risks):
            title = "Traiter le risque prioritaire"
            factors.append({"code": "risk", "label": "Risque élevé", "weight": 25})
            score += 20
        if workflow_instance and workflow_instance.get("current_step_key"):
            factors.append({"code": "workflow", "label": str(workflow_instance["current_step_key"]), "weight": 10})
            score += 10
        if partner_matches:
            factors.append({"code": "partner", "label": "Partenaire disponible", "weight": 10})
            score += 5
        if cost_summary and int(cost_summary.get("estimated") or 0) > int(project.get("budget_max") or 0) > 0:
            score -= 10
        return {
            "action_key": f"nba-{decision.get('decision_key', 'next')}",
            "title": title,
            "score": min(100, max(10, score)),
            "confidence": min(95, max(40, int(decision.get("confidence") or 50) + len(factors) * 3)),
            "justification": str(decision.get("reason") or "Analyse projet"),
            "explanation": {"summary": f"{len(factors)} facteur(s)", "method": "weighted_deterministic_scoring"},
            "factors": factors,
        }


class RiskIntelligenceEngine:
    def analyze(self, *, project: dict[str, object], risks: list[dict[str, object]], journey_state: dict[str, object], workflow_instance: dict[str, object] | None) -> list[dict[str, object]]:
        results: list[dict[str, object]] = []
        for risk in risks:
            if str(risk.get("status")) != "open":
                continue
            severity = str(risk.get("severity", "medium"))
            likelihood = str(risk.get("likelihood", "medium"))
            score = min(100, SEVERITY_WEIGHTS.get(severity, 25) + LIKELIHOOD_WEIGHTS.get(likelihood, 15))
            mitigation = [{"action": "Suivre et documenter", "priority": "normal"}]
            if severity in {"high", "critical"}:
                mitigation.insert(0, {"action": "Plan de mitigation immédiat", "priority": "high"})
            results.append({"risk_key": str(risk.get("risk_key")), "severity": severity, "likelihood": likelihood, "score": score, "mitigation": mitigation, "description": str(risk.get("description", ""))})
        if int(journey_state.get("blocked_steps") or 0) > 0:
            results.append({"risk_key": "journey-blocked", "severity": "high", "likelihood": "certain", "score": 85, "mitigation": [{"action": "Débloquer le parcours", "priority": "high"}], "description": "Parcours bloqué"})
        if project.get("budget_max") is None:
            results.append({"risk_key": "budget-unknown", "severity": "medium", "likelihood": "high", "score": 55, "mitigation": [{"action": "Qualifier le budget", "priority": "high"}], "description": "Budget non qualifié"})
        return sorted(results, key=lambda r: -int(r["score"]))


class OpportunityIntelligenceEngine:
    def analyze(self, *, project: dict[str, object], opportunities: list[dict[str, object]], partner_matches: list[dict[str, object]], service_matches: list[dict[str, object]]) -> list[dict[str, object]]:
        results: list[dict[str, object]] = []
        for opp in opportunities:
            if str(opp.get("status")) != "open":
                continue
            value = int(opp.get("value_score") or 50)
            results.append({"opportunity_key": str(opp.get("opportunity_key")), "value_score": value, "opportunity_score": min(100, value + 10), "description": str(opp.get("description", "")), "kind": "project_opportunity"})
        if partner_matches:
            top = max(partner_matches, key=lambda m: int(m.get("score") or 0))
            results.append({"opportunity_key": "partner-match", "value_score": int(top.get("score") or 50), "opportunity_score": int(top.get("confidence") or 50), "description": "Meilleur partenaire identifié", "kind": "partner"})
        if service_matches:
            top = max(service_matches, key=lambda m: int(m.get("score") or 0))
            results.append({"opportunity_key": "service-optimization", "value_score": int(top.get("score") or 50), "opportunity_score": 65, "description": "Service recommandé", "kind": "service"})
        if int(project.get("budget_max") or 0) > 0:
            results.append({"opportunity_key": "subsidy-check", "value_score": 40, "opportunity_score": 55, "description": "Vérifier aides/subventions", "kind": "subsidy"})
        return sorted(results, key=lambda r: -int(r["opportunity_score"]))
