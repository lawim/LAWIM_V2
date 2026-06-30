# Changelog — LAWIM_V2 Beta 1.0.0

**Date de release :** 2026-06-29  
**Tag :** `v1.0.0-beta`  
**Branche :** `release/1.0.0-beta`  
**Validation :** `v1.0.0-beta-validated`

Format basé sur les livraisons depuis la baseline executable jusqu'à la Beta industrialisée.

---

## [1.0.0-beta] — 2026-06-29

### Added

- Monolithe Python 3.12 executable : API REST, matching, conversations, notifications
- Console web statique (login, bootstrap, properties, matching, conversations)
- Persistance SQLite par défaut ; PostgreSQL optionnel (`LAWIM_DB_DRIVER=postgresql`)
- Schéma v5 unifié (`persistence.py`, `schema_ddl.py`, `schema_migrations.py`)
- Packaging pip (`pyproject.toml`, entry point `lawim-v2`)
- Scripts d'installation et validation reproductible (`install.sh`, `validate-install.sh`, `validate-packaging.sh`)
- Stacks Docker Compose (dev, staging, prod, postgres)
- CI GitHub Actions (tests, compose, PostgreSQL service container)
- **74 tests** unittest + smoke runtime + validation manifest Prisma
- Comptes et données démo seedées (3 orgs, 3 users, 3 properties)

### Security

- Health public minimal ; audit/metrics réservés admin authentifié
- Endpoints privés protégés (Bearer) ; RBAC admin / agent / owner
- Redaction credentials dans les réponses API
- Validation email/mot de passe à l'inscription
- Validation magic-bytes upload média
- Headers sécurité (CSP, X-Frame-Options, etc.)
- `AppConfig.validate()` : seed demo interdit en `APP_ENV=production`

### Changed

- Organisations et users exposés via DTOs stables
- Parsing query properties centralisé (`api_query.build_property_query`)
- Compose : source unique `compose/` + alias symlinks `docker/compose/`

### API breaking (vs early baseline)

| Endpoint | Beta 1.0.0 |
|----------|------------|
| `GET /api/health` | Minimal public ; détail si admin |
| `GET /api/metrics` | Admin requis |
| `GET /api/users` | Admin requis ; DTO sans hash |
| `GET /api/properties?include_deleted=true` | Admin requis |
| Upload média | Magic-bytes obligatoires |

### Known limitations

- Pas de rate limiting
- Médias `/media/*` servis sans authentification
- UI sans pipeline de build ni tests E2E navigateur
- Pas de publication PyPI/Docker Hub public
- Directive v1.0 complète non entièrement implémentée (scope Beta = runtime RC)

### Tags & reports

| Artefact | Référence |
|----------|-----------|
| Beta tag | `v1.0.0-beta` |
| Validation | `v1.0.0-beta-validated` |
| Distribution kit | `v1.0.0-beta-distribution-kit` |
| Validation report | `reports/program/BETA-1.0.0-RELEASE-VALIDATION-REPORT.md` |

---

## Historique pré-Beta (résumé)

| Tag / phase | Contenu clé |
|-------------|-------------|
| `mega-wave-009-mvp-stabilization` | Stabilisation MVP, parcours E2E |
| `mega-wave-010-release-candidate` | Durcissement RC, sécurité |
| `beta-candidate-ready` | Critères beta, health scoping |
| `full-engineering-review` | Revue engineering, DTOs, tests |
| `productization-001` | Installabilité, Compose, CI PG |
| `industrialization-001` | DDL unifié, packaging pip |

---

## Upgrade notes

### Nouvelle installation

```bash
git checkout v1.0.0-beta-validated
./scripts/install.sh
./scripts/validate-install.sh
./scripts/run-local.sh
```

### Depuis une checkout develop antérieure

1. Sauvegarder `data/runtime/` si données locales à conserver
2. Checkout tag Beta
3. `./scripts/validate-install.sh`
4. Relancer le serveur ; le schéma v5 est appliqué au init

---

*Beta 1.0.0 — diffusion contrôlée. Voir [BETA_DISTRIBUTION_GUIDE.md](BETA_DISTRIBUTION_GUIDE.md).*
