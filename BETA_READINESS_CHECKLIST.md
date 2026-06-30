# Beta Readiness Checklist

## Runtime

- [x] `./scripts/run-local.sh` démarre SQLite local
- [x] `./scripts/run-tests.sh` — 64 tests + Prisma + smoke
- [x] `python3 scripts/smoke_runtime.py` PASS
- [x] Compose dev + postgres overlays valides

## Sécurité

- [x] Health public sans audit/schema complet
- [x] Metrics admin-only
- [x] Users list admin-only sans password_hash/salt
- [x] include_deleted admin-only
- [x] Headers sécurité API/static/media
- [x] Payload JSON limité
- [x] Upload MIME + magic-bytes
- [x] Email/password validation register

## Parcours

- [x] Seller journey E2E
- [x] Buyer journey E2E
- [x] Admin journey E2E
- [x] Guest bootstrap/search
- [x] Erreurs auth/permission/validation/media/geo

## UI

- [x] escapeHtml sur contenus dynamiques
- [x] États vides / loading / erreurs
- [x] Aperçus média image
- [x] Filtres notifications / négociation

## Data

- [x] Schema v5 SQLite
- [x] Migrations idempotentes
- [x] Seed demo contrôlé
- [x] PostgreSQL manifest aligné (fallback SQLite)

## Documentation

- [x] `docs/OPERATIONS-RC.md`
- [x] `RELEASE_NOTES_BETA.md`
- [x] Rapport `reports/program/BETA-CANDIDATE-FINALIZATION-REPORT.md`
