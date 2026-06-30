from __future__ import annotations

import json
from typing import Any

from ..project_domain import compute_progress, derive_next_actions
from .constants import GOAL_JOURNEY_INFLUENCE, GOAL_KEYS, LIFE_EVENT_GOAL_SHIFT, LIFE_EVENT_TYPES


class JourneyEngine:
    def compute_state(self, *, project: dict[str, object], journey: dict[str, object], steps: list[dict[str, object]]) -> dict[str, object]:
        progress = compute_progress(steps)
        blocked = [step for step in steps if str(step.get("status")) == "blocked"]
        active = [step for step in steps if str(step.get("status")) == "in_progress"]
        pending = [step for step in steps if str(step.get("status")) == "pending"]
        status = str(journey.get("status", "draft"))
        if blocked:
            status = "blocked"
        elif progress >= 100:
            status = "completed"
        elif active or pending:
            status = "active"
        return {
            "journey_id": journey.get("id"),
            "status": status,
            "progress_percent": progress,
            "blocked_steps": len(blocked),
            "active_steps": len(active),
            "next_actions": derive_next_actions(steps, project_status=str(project.get("status", "draft"))),
        }

    def can_advance(self, step: dict[str, object]) -> bool:
        return str(step.get("status")) in {"pending", "in_progress", "blocked"}

    def replan(self, *, goal_key: str) -> list[str]:
        return list(GOAL_JOURNEY_INFLUENCE.get(goal_key, GOAL_JOURNEY_INFLUENCE["other"]))


class GoalEngine:
    def normalize_goal(self, goal_key: str) -> str:
        normalized = goal_key.strip().lower()
        if normalized not in GOAL_KEYS:
            raise ValueError(f"unsupported goal: {normalized}")
        return normalized

    def influence(self, goal_key: str) -> dict[str, object]:
        key = self.normalize_goal(goal_key)
        steps = GOAL_JOURNEY_INFLUENCE.get(key, GOAL_JOURNEY_INFLUENCE["other"])
        return {
            "goal_key": key,
            "journey_steps": steps,
            "priority_boost": "high" if key in {"buy", "house_family", "diaspora"} else "normal",
            "partner_kinds": self._partner_kinds(key),
            "service_keys": self._service_keys(key),
        }

    def _partner_kinds(self, goal_key: str) -> list[str]:
        mapping = {
            "buy": ["agent", "notary", "bank"],
            "rent": ["agent", "owner"],
            "sell": ["agent", "notary"],
            "build": ["architect", "contractor", "surveyor"],
            "invest": ["advisor", "bank"],
            "secure_patrimony": ["notary", "advisor"],
            "prepare_retirement": ["advisor", "bank"],
            "house_family": ["agent", "bank"],
            "diaspora": ["agent", "notary", "remote_manager"],
        }
        return mapping.get(goal_key, ["agent"])

    def _service_keys(self, goal_key: str) -> list[str]:
        mapping = {
            "buy": ["property_search", "visit_support", "document_check"],
            "rent": ["property_search", "lease_review"],
            "sell": ["listing_support", "valuation"],
            "build": ["land_search", "permit_guidance"],
            "invest": ["market_analysis", "yield_review"],
            "diaspora": ["remote_visit", "trust_verification"],
        }
        return mapping.get(goal_key, ["project_guidance"])


class DecisionEngine:
    def evaluate(
        self,
        *,
        project: dict[str, object],
        goals: list[dict[str, object]],
        risks: list[dict[str, object]],
        opportunities: list[dict[str, object]],
        constraints: list[dict[str, object]],
    ) -> dict[str, object]:
        goal_key = str(goals[0]["goal_key"]) if goals else str(project.get("project_type", "other"))
        high_risks = [risk for risk in risks if str(risk.get("severity")) in {"high", "critical"}]
        open_opportunities = [item for item in opportunities if str(item.get("status")) == "open"]
        budget_gap = self._budget_gap(project)
        confidence = max(20, 90 - len(high_risks) * 15 - (10 if budget_gap else 0))
        alternatives: list[str] = []
        tradeoffs: list[str] = []
        if high_risks:
            alternatives.append("Reporter la décision et réduire les risques identifiés")
            tradeoffs.append("Retard possible sur le planning")
        if open_opportunities:
            alternatives.append("Prioriser l'opportunité à plus fort score")
        if budget_gap:
            alternatives.append("Ajuster le budget ou le périmètre de recherche")
            tradeoffs.append("Compromis sur localisation ou surface")
        if not alternatives:
            alternatives.append("Poursuivre le parcours actuel")
        next_action = self._next_best_action(project, goal_key, high_risks, constraints)
        return {
            "decision_key": f"next-step-{goal_key}",
            "title": f"Décision recommandée pour {goal_key}",
            "reason": self._reason(goal_key, high_risks, budget_gap, open_opportunities),
            "confidence": confidence,
            "alternatives": alternatives,
            "tradeoffs": tradeoffs,
            "next_action": next_action,
        }

    def _budget_gap(self, project: dict[str, object]) -> bool:
        budget_min = project.get("budget_min")
        budget_max = project.get("budget_max")
        return budget_min is None or budget_max is None or int(budget_min) <= 0

    def _reason(self, goal_key: str, high_risks: list, budget_gap: bool, opportunities: list) -> str:
        parts = [f"Objectif principal: {goal_key}."]
        if high_risks:
            parts.append(f"{len(high_risks)} risque(s) élevé(s) détecté(s).")
        if budget_gap:
            parts.append("Budget incomplet — qualification nécessaire.")
        if opportunities:
            parts.append(f"{len(opportunities)} opportunité(s) ouverte(s).")
        return " ".join(parts)

    def _next_best_action(self, project: dict[str, object], goal_key: str, high_risks: list, constraints: list) -> str:
        if high_risks:
            return "Traiter le risque prioritaire avant d'avancer"
        if self._budget_gap(project):
            return "Compléter le budget et les contraintes financières"
        if constraints:
            return "Valider les contraintes bloquantes du projet"
        mapping = {
            "buy": "Affiner la recherche de biens alignée au projet",
            "rent": "Consolider les critères de location",
            "sell": "Préparer la mise en marché du bien",
            "invest": "Analyser le rendement des options",
            "build": "Valider le terrain et le budget travaux",
        }
        return mapping.get(goal_key, "Passer à l'étape suivante du parcours")


class LifeEventEngine:
    def normalize_event(self, event_type: str) -> str:
        normalized = event_type.strip().lower()
        if normalized not in LIFE_EVENT_TYPES:
            raise ValueError(f"unsupported life event: {normalized}")
        return normalized

    def impact(self, event_type: str) -> dict[str, object]:
        key = self.normalize_event(event_type)
        suggested_goals = list(LIFE_EVENT_GOAL_SHIFT.get(key, ("other",)))
        return {
            "event_type": key,
            "suggested_goals": suggested_goals,
            "priority_shift": "high" if key in {"birth", "relocation", "retirement"} else "normal",
            "recommendation_boost": key in {"investment", "succession", "business_creation"},
        }


class TimelineEngine:
    def build_timeline(
        self,
        *,
        history: list[dict[str, object]],
        entries: list[dict[str, object]],
        actions: list[dict[str, object]],
        milestones: list[dict[str, object]],
    ) -> dict[str, object]:
        past = sorted(
            [entry for entry in entries if entry.get("occurred_at")],
            key=lambda row: str(row.get("occurred_at")),
            reverse=True,
        )
        future = sorted(
            [entry for entry in entries if entry.get("scheduled_at") and not entry.get("occurred_at")],
            key=lambda row: str(row.get("scheduled_at")),
        )
        planned_actions = [action for action in actions if str(action.get("status")) in {"pending", "in_progress"}]
        return {
            "history": history[:20],
            "past_events": past[:20],
            "projections": future[:20],
            "planned_actions": planned_actions[:10],
            "milestones": milestones[:20],
        }


class RecommendationEngine:
    def generate(
        self,
        *,
        project: dict[str, object],
        goals: list[dict[str, object]],
        decision: dict[str, object] | None,
        goal_engine: GoalEngine,
    ) -> list[dict[str, object]]:
        goal_key = str(goals[0]["goal_key"]) if goals else str(project.get("project_type", "other"))
        influence = goal_engine.influence(goal_key)
        recommendations: list[dict[str, object]] = []
        recommendations.append(
            {
                "recommendation_key": f"goal-{goal_key}",
                "title": f"Prioriser l'objectif {goal_key}",
                "priority": influence["priority_boost"],
                "confidence": 75,
                "score": 80,
                "reasons": [{"code": "primary_goal", "label": "Objectif principal du projet"}],
            }
        )
        if decision:
            recommendations.append(
                {
                    "recommendation_key": decision["decision_key"],
                    "title": decision["next_action"],
                    "priority": "high",
                    "confidence": decision["confidence"],
                    "score": min(100, int(decision["confidence"]) + 10),
                    "reasons": [{"code": "decision_engine", "label": decision["reason"]}],
                }
            )
        for service_key in influence["service_keys"][:2]:
            recommendations.append(
                {
                    "recommendation_key": f"service-{service_key}",
                    "title": f"Envisager le service {service_key.replace('_', ' ')}",
                    "priority": "normal",
                    "confidence": 60,
                    "score": 65,
                    "reasons": [{"code": "goal_service", "label": f"Aligné avec l'objectif {goal_key}"}],
                }
            )
        return recommendations


class ProjectIntelligenceEngine:
    def analyze(
        self,
        *,
        project: dict[str, object],
        steps: list[dict[str, object]],
        risks: list[dict[str, object]],
        opportunities: list[dict[str, object]],
        actions: list[dict[str, object]],
        funding: list[dict[str, object]],
    ) -> dict[str, object]:
        progress = compute_progress(steps)
        open_risks = [risk for risk in risks if str(risk.get("status")) == "open"]
        blocked_actions = [action for action in actions if str(action.get("status")) == "blocked"]
        funding_total = sum(int(row.get("amount") or 0) for row in funding if str(row.get("status")) != "cancelled")
        budget_max = int(project.get("budget_max") or 0)
        budget_variance = None
        if budget_max > 0 and funding_total > 0:
            budget_variance = funding_total - budget_max
        return {
            "progress_percent": progress,
            "blockers": {
                "blocked_steps": len([s for s in steps if str(s.get("status")) == "blocked"]),
                "blocked_actions": len(blocked_actions),
                "open_high_risks": len([r for r in open_risks if str(r.get("severity")) in {"high", "critical"}]),
            },
            "risks": {"open": len(open_risks), "items": open_risks[:5]},
            "opportunities": {"open": len([o for o in opportunities if str(o.get("status")) == "open"])},
            "budget": {
                "planned_funding": funding_total,
                "budget_max": budget_max or None,
                "variance": budget_variance,
            },
            "priorities": self._priorities(project, open_risks, blocked_actions),
        }

    def _priorities(self, project: dict[str, object], risks: list, blocked_actions: list) -> list[str]:
        items: list[str] = []
        if str(project.get("status")) == "draft":
            items.append("Activer le projet")
        if risks:
            items.append("Traiter les risques ouverts")
        if blocked_actions:
            items.append("Débloquer les actions en attente")
        if not project.get("budget_max"):
            items.append("Qualifier le budget")
        if not items:
            items.append("Poursuivre le parcours")
        return items


def parse_json_list(value: str | None) -> list[Any]:
    if not value:
        return []
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return []
    return parsed if isinstance(parsed, list) else []
