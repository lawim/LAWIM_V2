# LAWIM 2.x — PROGRAM 002 Report
## Project Domain & Journey Foundation

**Programme :** LAWIM_2X_PROGRAM_002  
**Date :** 2026-06-29  
**Branche :** `develop/2.0-intelligent-platform`  
**Schema :** v6

---

## 1. Résumé exécutif

PROGRAM 002 livre le **premier domaine métier 2.x** : le **Projet Immobilier Utilisateur**, avec parcours guidé, persistance v6, API `/api/v2/projects`, UI minimale et suite de tests complète.

Aucune IA, marketplace ou partenaires — conformément au périmètre.

**Statut :** prêt pour revue Direction Générale.

---

## 2. Modèle Project

Entité centrale `projects` :

| Champ | Description |
|-------|-------------|
| `user_id` | Propriétaire du projet |
| `organization_id` | Organisation optionnelle |
| `title`, `objective` | Intitulé et objectif |
| `project_type` | buy, rent, sell, invest, build, other |
| `budget_min/max`, `currency` | Budget |
| `location_*` | Ville, région, pays, coordonnées |
| `timeline_horizon` | 1_month … flexible |
| `status` | draft, active, paused, completed, archived |
| `priority` | low, normal, high |
| `progress_percent` | Calculé automatiquement |
| `metadata_json` | Métadonnées extensibles |

Module domaine : `code/lawim_v2/project_domain.py`

---

## 3. Parcours guidé

Tables :

- **project_steps** — étapes par type de projet (templates buy/rent/sell/invest/build/other)
- **project_checklist_items** — checklist par étape
- **project_step_history** — historique des changements de statut

Chaque étape : `step_key`, `title`, `milestone`, `next_action`, `status` (pending → in_progress → completed).

Fonctions : `compute_progress()`, `derive_next_actions()`, `_seed_project_journey()` à la création.

---

## 4. Persistance v6

| Composant | Mise à jour |
|-----------|-------------|
| `persistence.py` | Manifest v6, seed projet demo |
| `schema_ddl.py` | DDL SQLite + PostgreSQL |
| `schema_migrations.py` | Migration legacy v5→v6 idempotente |
| `prisma/schema.prisma` | Modèles Project, ProjectStep, … |
| `prisma/migrations/…/migration.sql` | Aligné POSTGRESQL_INIT_STATEMENTS |

Fingerprint manifest : `8d8330e1…ee2e3`

Seed demo : projet « Achat appartement Douala » pour `agent@lawim.app`.

---

## 5. API v2

| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/api/v2/projects` | Liste paginée (filtres status, type, priority) |
| POST | `/api/v2/projects` | Création + parcours auto |
| GET | `/api/v2/projects/{id}` | Détail (steps, checklist, history, progress, next_actions) |
| PATCH | `/api/v2/projects/{id}` | Mise à jour / archivage |
| DELETE | `/api/v2/projects/{id}` | Archive (soft) |
| GET | `/api/v2/projects/{id}/steps` | Étapes |
| PATCH | `/api/v2/projects/{id}/steps/{step_id}` | Mise à jour étape |
| GET | `/api/v2/projects/{id}/progress` | Progression |
| GET | `/api/v2/projects/{id}/next-actions` | Prochaines actions |

Permissions : owner ou admin ; agents org (lecture org) — via `ProjectService`.

---

## 6. UI

Onglet **Project** dans la console bootstrap :

- Formulaire création projet
- Liste projets (API v2)
- Panneau détail : progression, étapes, next actions

Fichiers : `static/index.html`, `static/app.js`

---

## 7. Tests

Nouveau fichier : `tests/test_lawim_v2_program_002_projects.py` (13 tests)

Couverture :

- Schema v6, migration legacy
- CRUD API, steps, progress, next-actions
- Permissions cross-user
- Audit events `project_created`
- Domain helpers
- Régression v1.0 properties

**Résultat suite globale :** 103 tests OK (2 skipped pg8000 optionnel)

---

## 8. Compatibilité v1.0

- Branches 1.0 non modifiées
- API `/api/*` 1.0 inchangée
- Migrations ** additives ** — legacy v5 databases upgradées via `apply_sqlite_legacy_migrations()`
- SQLite reste défaut ; PostgreSQL optionnel
- Régression properties, auth, conversations : PASS

---

## 9. Risques

| Risque | Mitigation |
|--------|------------|
| Schema bump v5→v6 | Migration legacy testée |
| Permissions trop permissives admin | Tests cross-user |
| Progression simpliste (steps only) | Enrichissement PROGRAM 003+ |
| Pas de lien Property↔Project yet | PROGRAM 003 ou extension 002b |

**blocking_risk :** false

---

## 10. Prochaine mission recommandée

### LAWIM_2X_PROGRAM_003 — Knowledge Engine MVP

Référentiel structuré (quartiers, procédures, FAQ) alimentant les parcours et préparant l’assistant — sans LLM en production.

---

## Validations

| Script | Résultat |
|--------|----------|
| `./scripts/validate-install.sh` | PASS |
| `./scripts/validate-packaging.sh` | PASS |
| `./scripts/run-tests.sh` | PASS (103) |
| `python3 scripts/validate_prisma_manifest.py` | PASS (v6) |
| `python3 scripts/smoke_runtime.py` | PASS |
| `./platform/validate-platform.sh` | PASS |
| `./platform/run-postgres-tests.sh` | PASS (6) |
| `git diff --check` | PASS |

---

## Bloc programme

```yaml
program: LAWIM_2X_PROGRAM_002
status: READY_FOR_DG_REVIEW
project_domain: IMPLEMENTED
journey_foundation: IMPLEMENTED
schema_version: 6
api_v2: IMPLEMENTED
tests: PASS
postgresql: PASS
sqlite: PASS
blocking_risk: false
next_program: LAWIM_2X_PROGRAM_003
decision_required: true
```

---

*Fin du rapport LAWIM_2X_PROGRAM_002.*
