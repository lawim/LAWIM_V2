# RELEASE PROGRAM C — Knowledge • Decision • AI Foundation Platform

**Programme :** RELEASE PROGRAM C  
**Date :** 2026-07-01  
**Branche :** `develop/2.0-intelligent-platform`  
**Tag :** `release-program-c`  
**Schema :** v9  
**Prérequis :** RELEASE PROGRAM A (`release-program-a`), RELEASE PROGRAM B (`release-program-b`)

---

## 1. Résumé exécutif

RELEASE PROGRAM C ajoute à LAWIM 2.x une **plateforme cognitive déterministe** : graphe de connaissance, moteur de raisonnement, plateforme de décision, simulations, next best action, intelligence risques/opportunités — **sans IA générative**.

**302 tests** passent (objectif 300+).

---

## 2. Architecture cognition

Package : `code/lawim_v2/cognition/`

```
Project (aggregate root — Programs A & B)
├── Knowledge Graph Engine (knowledge_nodes, knowledge_edges, knowledge_relations)
├── Reasoning Engine (reasoning_traces, knowledge_inferences)
├── Decision Platform (cognition_decisions, decision_evidences, decision_histories)
├── Simulation Engine (simulation_runs)
├── Next Best Action Engine (next_best_actions)
├── Risk Intelligence Engine (risk_intelligence_scores)
├── Opportunity Intelligence Engine (opportunity_intelligence_scores)
└── Intelligence Snapshots (intelligence_snapshots, knowledge_snapshots)
```

Intégration : `LawimRepository(CognitionRepositoryMixin, EcosystemRepositoryMixin, IntelligentRepositoryMixin, ProjectRepositoryMixin)`.

---

## 3. Schema v9

15 tables cognition (`schema_v9_ddl.py`) intégrées dans :

- `persistence.py` — manifest v9
- `schema_ddl.py` — SQLite + PostgreSQL init
- `schema_migrations.py` — migration legacy v8→v9
- `prisma/schema.prisma` + migration SQL synchronisée

---

## 4. Moteurs (rule-based)

| Moteur | Rôle |
|--------|------|
| `KnowledgeGraphEngine` | Construit nœuds/edges/relations à partir du contexte projet |
| `ReasoningEngine` | 6 règles métier → conclusions et inférences |
| `DecisionPlatformEngine` | Décisions structurées avec preuves et explainability |
| `SimulationEngine` | 10 scénarios (budget, prêt, relocation, taux, …) |
| `NextBestActionEngine` | Action prioritaire score/confiance |
| `RiskIntelligenceEngine` | Scoring risques avec mitigation |
| `OpportunityIntelligenceEngine` | Scoring opportunités |

---

## 5. API v2 cognition

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/api/v2/knowledge/graph?project_id=` | GET | Graphe de connaissance projet |
| `/api/v2/knowledge/context?project_id=` | GET | Contexte cognitif agrégé |
| `/api/v2/knowledge/refresh` | POST | Rafraîchissement intelligence |
| `/api/v2/decisions?project_id=` | GET | Décisions cognition |
| `/api/v2/decisions/{id}?project_id=` | GET | Détail décision |
| `/api/v2/reasoning?project_id=` | GET | Traces de raisonnement |
| `/api/v2/simulations?project_id=` | GET | Scénarios + historique runs |
| `/api/v2/simulations` | POST | Exécuter simulation |
| `/api/v2/intelligence?project_id=` | GET | Workspace intelligence |
| `/api/v2/next-actions?project_id=` | GET | Next best action |
| `/api/v2/risks?project_id=` | GET | Scores risques |
| `/api/v2/opportunities?project_id=` | GET | Scores opportunités |

`GET /api/v2/knowledge` (admin, recherche globale Program A) est préservé.

---

## 6. UI

`static/app.js` / `static/index.html` — panneaux Knowledge graph, Decision platform, Next best action, Risk/Opportunity intelligence dans le workspace projet.

---

## 7. Validations

| Script | Résultat attendu |
|--------|------------------|
| `./scripts/validate-install.sh` | PASS |
| `./scripts/validate-packaging.sh` | PASS |
| `./scripts/run-tests.sh` | PASS (302+ tests) |
| `python3 scripts/validate_prisma_manifest.py` | PASS v9 |
| `python3 scripts/smoke_runtime.py` | PASS |
| `./platform/validate-platform.sh` | PASS |
| `./platform/run-postgres-tests.sh` | PASS |
| `git diff --check` | PASS |

---

## 8. Git

```bash
git add .
git commit -m "feat(2x): implement knowledge decision platform"
git tag release-program-c
git push origin develop/2.0-intelligent-platform --tags
```
