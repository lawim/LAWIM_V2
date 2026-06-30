# RELEASE PROGRAM A — Intelligent Core Platform

**Programme :** RELEASE PROGRAM A  
**Date :** 2026-06-29  
**Branche :** `develop/2.0-intelligent-platform`  
**Tag :** `release-program-a`  
**Schema :** v7

---

## 1. Résumé exécutif

RELEASE PROGRAM A transforme LAWIM 2.x en **plateforme centrée sur le projet immobilier**. Le bien devient une **ressource** rattachée au projet ; le projet est l’**agrégat racine** du domaine intelligent.

Livré :

- **Knowledge Domain** — 23 entités métier (goals, needs, constraints, decisions, recommendations, life events, etc.)
- **Moteurs rule-based** — Journey, Goal, Decision, Life Event, Timeline, Recommendation, Project Intelligence (sans IA)
- **API v2 complète** — workspace, goals, knowledge, recommendations, decisions, actions, tasks, life-events, timeline, journey, intelligence, resources
- **Schema v7** — SQLite + PostgreSQL (Prisma), migration legacy v5→v7
- **UI Journey** — panneau projet enrichi (goals, timeline, intelligence, recommendations, actions, tasks, life events, knowledge)
- **151 tests** — unitaires, API, repositories, engines, migration, permissions
- **Observabilité** — compteurs `projects_total`, `intelligent_workspace_total`

**Compatibilité v1.0 :** API `/api/*` inchangée ; annonces et conversations préservées.

---

## 2. Architecture

```
Project (aggregate root)
├── Journey + JourneySteps (project_steps)
├── Goals / Needs / Constraints / Preferences / Funding
├── LifeEvents → GoalEngine impact
├── Risks / Opportunities
├── DecisionEngine → Decisions
├── RecommendationEngine → Recommendations
├── Actions / Tasks / Milestones
├── KnowledgeFacts / Contexts
├── ProjectResources (property = resource)
├── TimelineEngine → timeline_entries
├── ProjectIntelligenceEngine → intelligence_json + trust_scores
└── ProgressSnapshots
```

Package : `code/lawim_v2/intelligent/`

| Module | Rôle |
|--------|------|
| `constants.py` | Goal keys, life events, influence maps |
| `schema_v7_ddl.py` | DDL v7 (23 tables intelligentes) |
| `engines.py` | 7 moteurs métier déterministes |
| `repository.py` | CRUD, bootstrap, refresh intelligence, workspace |
| `dto.py` | DTOs API |
| `service.py` | Permissions + orchestration |

Intégration : `LawimRepository(IntelligentRepositoryMixin, ProjectRepositoryMixin)`.

---

## 3. Knowledge Domain

Chaque entité dispose de :

- Tables SQLite/PostgreSQL alignées (`persistence.py` manifest v7)
- Repository mixin (`intelligent/repository.py`)
- DTO (`intelligent/dto.py`)
- Service avec permissions (`intelligent/service.py`)
- Bootstrap automatique à la création de projet
- Audit via `events` existant + `timeline_entries`

Entités principales : `Project`, `Goal`, `Need`, `Constraint`, `Preference`, `Budget` (champs projet), `Funding`, `Timeline`, `LifeEvent`, `Risk`, `Opportunity`, `Decision`, `Recommendation`, `Action`, `Task`, `Milestone`, `Journey`, `JourneyStep`, `ProgressSnapshot`, `KnowledgeFact`, `UserContext`, `ProjectContext`, `PartnerSuggestion`, `ServiceSuggestion`, `TrustScore`.

---

## 4. Moteurs

### Journey Engine
Calcule statut (active/blocked/completed), progression, next actions, replanification par objectif.

### Goal Engine
Normalise 10 objectifs (buy, rent, sell, build, invest, secure_patrimony, prepare_retirement, house_family, diaspora, other). Influence parcours, partenaires, services.

### Decision Engine
Produit `Decision`, `Reason`, `Confidence`, `Alternatives`, `Tradeoffs`, `Next Best Action` — règles budget/risques/contraintes.

### Life Event Engine
10 types (marriage, birth, relocation, retirement, investment, succession, business_creation, divorce, inheritance, other). Modifie priorités et objectifs suggérés.

### Timeline Engine
Historique, projections, actions planifiées, milestones.

### Recommendation Engine
`Recommendation`, `RecommendationReason`, `RecommendationScore`, `Priority`, `Confidence` — sans ML.

### Project Intelligence Engine
Avancement, blocages, risques, opportunités, budget/variance, priorités.

---

## 5. API v2

| Route | Méthodes | Description |
|-------|----------|-------------|
| `/api/v2/projects` | GET, POST | Liste paginée / création |
| `/api/v2/projects/{id}` | GET, PATCH | Détail / mise à jour |
| `/api/v2/projects/{id}/workspace` | GET | Workspace intelligent complet |
| `/api/v2/projects/{id}/goals` | GET, POST | Objectifs |
| `/api/v2/projects/{id}/knowledge` | GET, POST | Faits métier |
| `/api/v2/projects/{id}/recommendations` | GET | Recommandations |
| `/api/v2/projects/{id}/decisions` | GET | Décisions |
| `/api/v2/projects/{id}/actions` | GET, POST | Actions |
| `/api/v2/projects/{id}/tasks` | GET, POST | Tâches |
| `/api/v2/projects/{id}/life-events` | GET, POST | Événements de vie |
| `/api/v2/projects/{id}/timeline` | GET | Timeline |
| `/api/v2/projects/{id}/journey/state` | GET | État parcours |
| `/api/v2/projects/{id}/journey/replan` | POST | Replanification |
| `/api/v2/projects/{id}/intelligence/refresh` | POST | Recalcul intelligence |
| `/api/v2/projects/{id}/resources` | GET, POST | Ressources (biens) |
| `/api/v2/knowledge` | GET | Recherche globale (admin) |

Pagination, filtrage, erreurs JSON standardisées, permissions propriétaire/admin.

---

## 6. Persistance v7

- `APPLICATION_SCHEMA_VERSION = 7`
- Migration legacy SQLite : `apply_sqlite_legacy_migrations()` (v5→v6 projects + v7 intelligent)
- Prisma : `prisma/migrations/20260629120000_init/migration.sql` régénéré
- Dual SQLite/PostgreSQL via manifest `persistence.py`

---

## 7. UI

Onglet **Project** (`static/index.html`, `static/app.js`) :

- Liste projets + formulaire création
- Détail workspace : goals, recommendations, intelligence, timeline, actions, tasks, life events, knowledge, journey steps
- Chargement via `GET /api/v2/projects/{id}/workspace`

Pas de réécriture front — extension progressive du console existant.

---

## 8. Tests & qualité

| Suite | Tests |
|-------|-------|
| `test_release_program_a.py` | 48 (engines, API, repository, migration, metrics) |
| `test_lawim_v2_program_002_projects.py` | 13 |
| Autres suites existantes | 90 |
| **Total** | **151** (2 skipped) |

Validations exécutées :

- `./scripts/run-tests.sh` ✓
- `./scripts/validate-install.sh` ✓
- `./scripts/validate-packaging.sh` ✓
- `python3 scripts/validate_prisma_manifest.py` ✓
- `python3 scripts/smoke_runtime.py` ✓
- `./platform/validate-platform.sh` ✓
- `./platform/run-postgres-tests.sh` ✓

---

## 9. Observabilité

`observability.py` étendu :

- `projects_total` — incrémenté à la création de projet
- `intelligent_workspace_total` — incrémenté à chaque chargement workspace
- Exposé via `/api/metrics` (admin)

---

## 10. Migration depuis v1 / v6

1. Bases v1/v5 : migration legacy idempotente au démarrage SQLite
2. Bases v6 (PROGRAM 002) : ajout tables v7 via même chemin legacy
3. Fresh install : `SQLITE_INIT_SCRIPT` v7 complet
4. PostgreSQL prod : `prisma migrate deploy`

Aucune rupture API v1.

---

## 11. Prochaines étapes (hors périmètre A)

- Marketplace partenaires avancée
- IA / scoring prédictif
- Notifications projet intelligentes
- Prisma models typés pour toutes les tables v7

---

## 12. Statut

**RELEASE PROGRAM A — TERMINÉ**

LAWIM n’est plus centré sur les annonces. LAWIM est centré sur le **projet immobilier**.
