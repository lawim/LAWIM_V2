# LAWIM_V2 — Productization Mission 001 Report

- **Date:** 2026-06-29
- **Baseline:** `85fe307` (full-engineering-review)
- **Tag:** `productization-001`
- **Scope:** installabilité, reproductibilité, unification schéma/Compose, CI PostgreSQL

---

## 1. Cartographie de l'installation

### 1.1 Chemin d'installation (machine vierge)

```
git clone → cd LAWIM_V2
    │
    ├─ ./scripts/install.sh
    │     ├─ infra/check-env.sh      (Python 3.12+, dirs, docker/node optionnels)
    │     ├─ mkdir data/runtime/media
    │     └─ cp env/development/.env.example → .env.local (si absent)
    │
    ├─ ./scripts/validate-install.sh  (gate reproductibilité)
    │     ├─ compileall
    │     ├─ unittest (67 tests, 1 skip PG local)
    │     ├─ validate_prisma_manifest.py
    │     ├─ smoke_runtime.py
    │     └─ docker compose config (4 paires)
    │
    └─ ./scripts/run-local.sh | run-compose-dev.sh | run-compose-postgres.sh
```

### 1.2 Dépendances runtime

| Composant | Obligatoire | Fichier / source |
|-----------|-------------|------------------|
| Python 3.12+ | Oui | stdlib uniquement (core) |
| pg8000 | Non (PG only) | `requirements-postgresql.txt` |
| Docker Compose | Non | `compose/` |
| Node.js | Non | check syntaxe `app.js` |
| Prisma CLI | Non | manifest Python + SQL statique |

### 1.3 Artefacts de persistance (source de vérité)

```
persistence.py (manifest logique v5, fingerprint)
       │
       ├── schema_ddl.py (DDL PostgreSQL runtime — NOUVEAU)
       │        ├── postgresql_repository.py
       │        └── prisma/migrations/.../migration.sql (v5 aligné)
       ├── db.py (SQLite DDL + migrations inline)
       └── prisma/schema.prisma (ancre ORM, header v5)
```

### 1.4 Compose (source de vérité unique)

```
compose/                          ← canonique (scripts, docs, CI)
  docker-compose.base.yml
  docker-compose.dev.yml
  docker-compose.staging.yml
  docker-compose.prod.yml
  docker-compose.postgres.yml

docker/compose/                   ← alias symlinks (compat historique)
  docker-compose.development.yml → compose/docker-compose.dev.yml
  docker-compose.production.yml  → compose/docker-compose.prod.yml
  …
```

Régénération : `./scripts/sync-compose-aliases.sh`

### 1.5 Contrat repository (branché)

`repository_contract.py` → `LawimRepositoryContract` utilisé comme type de retour de `persistence_adapter.create_repository()` ; vérifié par `isinstance` dans les tests.

---

## 2. Problèmes structurels corrigés

| ID | Problème | Correction |
|----|----------|------------|
| P-01 | DDL PostgreSQL dupliqué / Prisma migration v4 obsolète | `schema_ddl.py` + migration SQL v5 régénérée |
| P-02 | `validate_prisma_manifest.py` superficiel | Comparaison statement-by-statement migration ↔ runtime DDL |
| P-03 | Double arbre Compose (contenu dupliqué, dérive paths) | `compose/` canonique ; `docker/compose/` = symlinks |
| P-04 | `repository_contract.py` mort | Typage + test runtime `isinstance` |
| P-05 | `infra/install.sh` / `check-env.sh` no-op | Implémentation idempotente |
| P-06 | Pas de README racine | `README.md` avec parcours install/run |
| P-07 | CI inactive (`.example` only) | `.github/workflows/ci.yml` actif |
| P-08 | Pas de test PostgreSQL | `PostgreSQLIntegrationTest` + job CI service container |
| P-09 | Pas de gate install reproductible | `scripts/validate-install.sh` |
| P-10 | Scripts staging/prod absents | `run-compose-staging.sh`, `run-compose-prod.sh` |

---

## 3. Simplifications réalisées

1. **Une seule définition Compose** — fin de la maintenance parallèle de 10 fichiers YAML quasi-identiques.
2. **DDL PostgreSQL centralisé** — `schema_ddl.py` alimente runtime et migration Prisma.
3. **Factory install** — `install.sh` → `infra/install.sh` ; un point d'entrée documenté.
4. **requirements.txt** — déclare explicitement stdlib + extra PostgreSQL via `-r`.
5. **Tests productization** — contrat repository, symlinks compose, fingerprint DDL stable.

---

## 4. Reproductibilité de l'installation

### Procédure validée localement

```bash
./scripts/install.sh
./scripts/validate-install.sh
```

### Résultats des contrôles finaux

| Contrôle | Résultat |
|----------|----------|
| `python3 -m compileall code tests scripts` | OK |
| `python3 -m unittest discover -s tests` | **67 OK, 1 skipped** (PG local sans DSN) |
| `scripts/validate_prisma_manifest.py` | PASS v5 + DDL aligné |
| `scripts/smoke_runtime.py` | Smoke OK |
| Docker Compose (4 paires base+overlay) | OK |
| `node --check app.js` | OK |
| `git diff --check` | OK |
| `./scripts/validate-install.sh` | **INSTALL VALIDATION OK** |

### CI GitHub Actions (`.github/workflows/ci.yml`)

- Job **validate** : `validate-install.sh` complet
- Job **compose** : 4 stacks
- Job **postgres** : service `postgres:16-alpine` + `PostgreSQLIntegrationTest`

---

## 5. État réel de préparation à une version 1.0

| Dimension | Avant | Après P-001 | Commentaire |
|-----------|-------|-------------|-------------|
| Installabilité | 2/5 | **4/5** | Scripts fonctionnels, README, gate validate |
| Reproductibilité | 2/5 | **4/5** | validate-install + CI |
| Schéma unifié | 3/5 | **4/5** | DDL central ; SQLite DDL inline reste |
| Compose | 2/5 | **4.5/5** | Source unique + alias |
| CI/CD | 1/5 | **3.5/5** | CI actif ; CD encore absent |
| Doc exploitation | 3/5 | **4/5** | README + OPERATIONS-RC enrichi |

**Verdict :** LAWIM_V2 peut être **installé et opéré par une organisation tierce** en mode RC (SQLite ou PostgreSQL optionnel). Pas encore une v1.0 « enterprise » (pas de CD, pas de migrations incrémentales, pas de packaging OS).

---

## 6. Dette restante

| Priorité | Item |
|----------|------|
| Haute | SQLite DDL encore inline dans `db.py` — générer depuis manifest ou schema_ddl |
| Haute | CD / release pipeline (images signées, semver) |
| Moyenne | Prisma CLI workflow (`migrate deploy`) documenté vs runtime init |
| Moyenne | `infra/check-env.sh` — codes de sortie structurés / JSON report |
| Moyenne | Windows : symlinks `docker/compose/` (script copy fallback) |
| Basse | Directive `23-INSTALLATION-GUIDE.md` vs RC — section « écart cible » |
| Basse | Rate limiting, metrics export, E2E browser |

---

## 7. Recommandations pour PRODUCTIZATION-002

1. **Génération SQLite DDL** depuis `persistence.APPLICATION_SCHEMA` — éliminer la dernière triplication.
2. **Packaging** — wheel/sdist `lawim_v2`, entry point `pip install .`, data dirs via config.
3. **CD pipeline** — build/push image, tag semver, changelog automatisé.
4. **Migrations incrémentales** — Alembic ou Prisma migrate comme seul chemin PG prod.
5. **Installers OS** — systemd unit, healthcheck externe, log rotation.
6. **Documentation tierce** — guide « deploy on OVH/K8s », matrice env vars/secrets.
7. **Observabilité production** — `/metrics` Prometheus, structured JSON logs.

---

## Fichiers créés / modifiés (extrait)

| Fichier | Action |
|---------|--------|
| `code/lawim_v2/schema_ddl.py` | Créé — DDL PostgreSQL source |
| `code/lawim_v2/persistence_adapter.py` | Contrat repository branché |
| `docker/compose/*.yml` | Symlinks → `compose/` |
| `scripts/install.sh`, `validate-install.sh`, `sync-compose-aliases.sh` | Créés |
| `infra/install.sh`, `check-env.sh` | Implémentés |
| `.github/workflows/ci.yml` | CI actif |
| `README.md`, `requirements.txt` | Créés |
| `prisma/migrations/.../migration.sql` | Mis à jour v5 |
| `tests/test_productization.py` | Créé |

---

*Mission Productization 001 — production readiness & installability.*
