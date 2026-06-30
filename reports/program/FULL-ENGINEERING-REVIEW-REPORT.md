# LAWIM_V2 — Full Engineering Review Report

- **Date:** 2026-06-29
- **Baseline:** `d50567d` (beta-candidate-ready)
- **Tag:** `full-engineering-review`
- **Scope:** revue Principal Engineer avant ouverture publique — cartographie, dette, corrections sans toucher Bootstrap / Constitution / Gouvernance / règles métier

---

## 1. Cartographie complète du produit

### 1.1 Vue d'ensemble

LAWIM_V2 est un **monolithe Python 3.12** orienté immobilier (listings, matching, conversations, notifications). Le runtime est un serveur HTTP (`ThreadingHTTPServer`) sans framework web externe.

```
┌─────────────────────────────────────────────────────────────┐
│  CLI: python -m lawim_v2  (code/lawim_v2/__main__.py)       │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│  server.py — routage HTTP, auth Bearer, multipart, static   │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│  services.py — RBAC, orchestration, DTOs, domaine métier    │
└────────────┬─────────────────────────────┬──────────────────┘
             │                             │
┌────────────▼────────────┐   ┌────────────▼────────────────────┐
│  db.py (SQLite)         │   │  postgresql_repository.py       │
│  persistence.py v5      │   │  (sous-classe, optionnel)       │
└────────────┬────────────┘   └─────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────────────────┐
│  Fichiers média locaux (config.media_storage_path)          │
└─────────────────────────────────────────────────────────────┘
```

**Pont d'import :** le paquet racine `lawim_v2/` et `sitecustomize.py` rendent `code/` importable ; `PYTHONPATH=code` en dev/test.

### 1.2 Couches applicatives (`code/lawim_v2/` — 27 modules)

| Module | Rôle |
|--------|------|
| `server.py` | Handler HTTP, routes REST, erreurs API, assets statiques |
| `services.py` | Couche service, politique d'accès, agrégation DTO |
| `db.py` | Repository SQLite, seed demo, CRUD, matching, events |
| `postgresql_repository.py` | Adapter PostgreSQL (DDL + requêtes héritées) |
| `persistence.py` / `persistence_adapter.py` | Schéma v5, résolution driver |
| `dto.py` | Contrats JSON (property, media, user, org, pagination…) |
| `api_query.py` | Parsing query string typé (ListQuery, build_*_query) |
| `matching.py` | Moteur de scoring déterministe |
| `*_domain.py` | Règles métier par domaine (property, media, geo, conversation, notification) |
| `security.py` | Hash mot de passe, validation email/password |
| `config.py` | `AppConfig` frozen, env vars, validation |
| `observability.py` | Compteurs METRICS in-process |
| `repository_contract.py` | Protocols documentaires (non branchés runtime) |
| `static/` | UI vanilla (index.html, app.js, styles.css) |

### 1.3 Persistance

- **SQLite** (défaut) : fichier `data/runtime/lawim.sqlite3`, schéma version 5.
- **PostgreSQL** : via `LAWIM_DB_DRIVER=postgresql`, fallback SQLite configurable.
- **Prisma** (`prisma/`) : ancre d'alignement schéma + migration ; **pas d'ORM runtime**. Validé par `scripts/validate_prisma_manifest.py` (fingerprint v5).

Tables principales : `organizations`, `users`, `sessions`, `properties`, `media`, `conversations`, `messages`, `notifications`, `events`.

### 1.4 API (extrait)

| Zone | Endpoints clés |
|------|----------------|
| Public | `GET /api/health`, `GET /api/bootstrap`, `GET /api/properties`, `GET /api/matches` |
| Auth | `POST /api/auth/login|register|logout`, `GET /api/me` |
| Admin | orgs/users/events CRUD, metrics détaillés, `include_deleted` |
| Métier | properties/media/conversations/notifications (GET/POST/PUT/PATCH/DELETE) |
| Static | `/`, `/assets/*`, `/media/*` |

Erreurs normalisées : `{"error": {"code", "message"}}` via `error_dto`.

### 1.5 Frontend

Console statique sans build pipeline : login, bootstrap, recherche matching, CRUD property, conversations. Sécurité côté client : `escapeHtml` pour l'injection XSS.

### 1.6 Ops & tooling

| Artefact | Usage |
|----------|-------|
| `scripts/run-local.sh` | Lancement dev |
| `scripts/run-tests.sh` | unittest + Prisma + smoke + check JS |
| `scripts/smoke_runtime.py` | Serveur éphémère, probes HTTP |
| `compose/` | Stacks utilisées par les scripts (`dev`, `postgres`, `staging`, `prod`) |
| `docker/compose/` | Miroir avec contextes build différents |
| `Dockerfile` racine | Image runtime `python -m lawim_v2` |
| `tests/` | 8 fichiers, **64 tests**, harness partagé `lawim_harness.py` |

### 1.7 Configuration runtime

Variables clés : `LAWIM_HOST`, `LAWIM_PORT`, `LAWIM_DB_PATH`, `LAWIM_DB_DRIVER`, `LAWIM_DATABASE_URL`, `LAWIM_SEED_DEMO_DATA`, `APP_ENV`, `LAWIM_MAX_JSON_BODY_BYTES`, etc. Validation stricte en production (pas de seed demo).

---

## 2. Faiblesses détectées

### P0 — Correctness

| ID | Problème | Impact |
|----|----------|--------|
| F-01 | **`app.js` : accolade manquante** dans `setLoading()` — tout le fichier JS était imbriqué par erreur | UI cassée en navigateur ; tests ne vérifiaient que des chaînes grep |

### P1 — DRY / duplication

| ID | Problème |
|----|----------|
| F-02 | Harness dupliqué dans `test_lawim_v2.py` (~100 lignes) vs `lawim_harness.py` |
| F-03 | Blocs `AppConfig(...)` répétés dans harness, smoke, tests |
| F-04 | Parsing query properties dupliqué entre `server.py` et `api_query.py` |
| F-05 | Quatre extracteurs d'ID quasi-identiques dans `server.py` |
| F-06 | Arbres Compose dupliqués `compose/` vs `docker/compose/` |
| F-07 | DDL tripliqué SQLite / PostgreSQL init / Prisma migration |

### P2 — Cohérence API / DTO

| ID | Problème |
|----|----------|
| F-08 | Organisations renvoyées en lignes SQL brutes (pas de `organization_dto`) |
| F-09 | `public_user()` inline dans `db.py` au lieu de `user_dto()` |
| F-10 | `error_dto` importé mais non utilisé ; imports DTO morts dans `server.py` |

### P3 — Code mort / misc

| ID | Problème |
|----|----------|
| F-11 | `repository_contract.py` — Protocols jamais injectés |
| F-12 | `MAX_JSON_BODY_BYTES` module constant dupliquant `config.max_json_body_bytes` |

### P4 — Documentation & tests

| ID | Problème |
|----|----------|
| F-13 | `tests/README.md` placeholder obsolète |
| F-14 | Pas de vérification syntaxe JS dans la CI locale |
| F-15 | Pas de test d'intégration PostgreSQL automatisé |
| F-16 | Pas de détection de dérive entre miroirs Compose |

### P5 — Sécurité / observabilité (dette acceptée beta)

- Pas de rate limiting HTTP
- Metrics in-memory non exportées Prometheus
- Workflows GitHub `.example` non actifs
- Géocodage Nominatim sans cache distribué

---

## 3. Corrections réalisées

| ID | Action | Fichiers |
|----|--------|----------|
| F-01 | Ajout `}` fermant `setLoading()` | `static/app.js` |
| F-02 | `LawimV2ExecutableBaselineTest` hérite de `LawimTestHarness` | `tests/test_lawim_v2.py` |
| F-03 | Factory `AppConfig.for_test(**overrides)` | `config.py`, harness, smoke |
| F-04 | Route `GET /api/properties` délègue à `build_property_query` | `server.py` |
| F-08 | `organization_dto` + `services.list_organizations()` | `dto.py`, `services.py`, `server.py` |
| F-09 | `user_dto()` centralisé ; `db._public_user` délègue | `dto.py`, `db.py` |
| F-10 | `_send_json_error` utilise `error_dto` ; imports nettoyés | `server.py` |
| F-13 | `tests/README.md` documenté | `tests/README.md` |
| F-14 | `node --check app.js` dans `run-tests.sh` | `scripts/run-tests.sh` |
| — | Suppression fichier junk `data/Untitled` | — |
| — | Test MVP aligné sur code `validation_error` pour price range | `test_mvp_stabilization.py` |

---

## 4. Refactorings effectués

### 4.1 Consolidation extracteurs d'ID (`server.py`)

`_extract_path_id(marker, suffix, resource)` remplace `_extract_resource_id` et unifie property / conversation / notification / media / user / organization. Réduction ~45 lignes, comportement identique.

### 4.2 Couche DTO organisations

- `organization_dto(row)` : `id`, `name`, `slug`, `kind`, `city`, `created_at`, `user_count`
- Bootstrap, list, create, update passent par la couche service avec DTO stable.

### 4.3 Configuration test unifiée

`AppConfig.for_test(db_path=..., media_storage_path=..., **overrides)` avec `dataclasses.replace` pour les cas spéciaux (smoke port/host).

### 4.4 Non modifié (hors scope / risque)

- Bootstrap, Constitution, Gouvernance, règles métier domaine
- Fusion des arbres Compose (documentée en dette)
- Suppression `repository_contract.py` (documentation utile)
- Refonte DDL tripliqué (Prisma reste ancre)

---

## 5. Dette restante

| Priorité | Item | Recommandation |
|----------|------|----------------|
| Haute | Miroirs Compose `compose/` vs `docker/compose/` | Unifier ou script de sync + test dérive |
| Haute | DDL tripliqué | Générer SQLite/PG depuis Prisma ou manifest unique |
| Moyenne | `repository_contract.py` non câblé | Brancher via `persistence_adapter` ou retirer |
| Moyenne | Pas de test PG CI | Job matrix sqlite+postgres avec service container |
| Moyenne | `MAX_JSON_BODY_BYTES` export module | Dériver uniquement de config (breaking tests mineur) |
| Basse | Frontend sans bundler/tests E2E | Playwright ou Cypress sur smoke paths |
| Basse | Rate limiting, export metrics | Middleware + endpoint `/metrics` Prometheus |
| Basse | Workflows CI `.example` → actifs | Activer lint/test sur PR |

---

## 6. Recommandations long terme

1. **Contrat API versionné** — OpenAPI généré depuis routes + DTOs ; breaking changes semver.
2. **Migration framework** — Alembic ou Prisma migrate comme source unique ; SQLite dev, PG prod.
3. **Observabilité production** — structured logging JSON, trace IDs, health/readiness K8s distincts.
4. **Sécurité publique** — rate limit auth, CSP renforcée, audit secrets, rotation sessions.
5. **Frontend** — build minimal (esbuild) + tests unitaires JS ; conserver vanilla ou migrer progressivement.
6. **CI/CD** — pipeline unique : compileall, 64+ tests, compose pairs, smoke, scan deps.
7. **Documentation produit** — README racine à jour (API table, env vars, parcours demo).

---

## 7. Évaluation globale de la qualité logicielle

| Dimension | Note (1–5) | Commentaire |
|-----------|------------|-------------|
| Architecture | 4 | Monolithe clair, séparation server/services/db/domain ; PG optionnel propre |
| Maintenabilité | 4 | DTOs centralisés, api_query, harness partagé ; dette Compose/DDL |
| Testabilité | 4 | 64 tests, smoke runtime, harness riche ; manque PG E2E et JS tests |
| Sécurité | 3.5 | RBAC, validation input, CSP, redaction ; pas de rate limit |
| Performance | 3.5 | SQLite OK MVP ; pas de cache/query tuning documenté |
| Observabilité | 3 | Metrics in-process ; pas d'export standard |
| Documentation | 3.5 | Rapports program riches ; README racine absent/minimal |
| Évolutivité | 4 | Domain modules, adapter PG ; frontend limite scaling UX |

**Verdict :** LAWIM_V2 est **prêt pour une beta publique contrôlée** après cette revue. La baseline executable est saine, les régressions sont couvertes, et le bug UI critique est corrigé. La dette structurelle (Compose, DDL, CI) est connue et planifiable sans bloquer un lancement limité.

---

## Contrôles finaux exécutés

| Contrôle | Résultat |
|----------|----------|
| `python3 -m compileall code tests scripts` | OK |
| `python3 -m unittest discover -s tests` | **64/64 OK** |
| `scripts/validate_prisma_manifest.py` | PASS (manifest v5) |
| `scripts/smoke_runtime.py` | Smoke OK |
| `docker compose config` (4 paires base+overlay) | OK |
| `node --check code/lawim_v2/static/app.js` | OK |
| `git diff --check` | OK |

---

*Rapport généré dans le cadre de la mission Principal Engineer — LAWIM_V2 full engineering review.*
