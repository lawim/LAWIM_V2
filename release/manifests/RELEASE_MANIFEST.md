# RELEASE_MANIFEST

## Snapshot

- Release family: LAWIM Experience 1.0
- Snapshot id: `release-program-j-lawim-experience-1.0-778ab779`
- Source commit: `778ab779bcd69a585a29e0ac42b74f331df7538e`
- Git tag: `release-program-j-lawim-experience-1.0`
- Purpose: reproducible release projection before OVH promotion

## Runtime baseline

- Python: `>=3.12`
- Packaging: `setuptools` from `pyproject.toml`
- Runtime entrypoint: `python -m lawim_v2`
- Deployment families: Docker, Docker Compose, Nginx, systemd, PostgreSQL, Redis

## Included release areas

- `current/` for a full local snapshot
- `ovh/` for the minimized deployment payload
- `manifests/` for packaging rules and security classification
- `checksums/` for materialized SHA256 files
- `deployment/` for operator-facing procedures
- `OPS/` for the certified long-lived local operations memory
- `ops/ovh/` for local-only server pilot notes

## Geo Intelligence closure

- Module: `code/lawim_v2/geo_reference.py`
- Runtime support: `code/lawim_v2/geo_domain.py`, `code/lawim_v2/geocoding_provider.py`, `code/lawim_v2/services.py`, `code/lawim_v2/dto.py`
- Reference data: `code/lawim_v2/data/cameroon_locations.json`
- Runtime capabilities: city and neighborhood alias normalization, offline geocoding, local search merge, deterministic fallback, and distance scoring
- Excluded from OVH: raw LAWIM / LAWIMA trees, reports, prompts, tests, and release analysis artifacts

## Functional consolidation before freeze

- Source intelligence language inference now recognizes pidgin-aware cues in addition to French and English markers, with French fallback preserved.
- CRM lead scoring now consumes richer lead payloads and adds modest bonuses for urgency, location, diaspora, investment, visit, budget, and financing signals.
- These additions are runtime-only and do not change the schema, migrations, or external dependencies.

## Source inputs

- `Dockerfile`
- `sitecustomize.py`
- `pyproject.toml`
- `requirements.txt`
- `requirements-postgresql.txt`
- `code/lawim_v2/`
- `frontend/`
- `prisma/`
- `compose/`
- `deployment/`
- `env/`
- `scripts/run-compose-prod.sh`

## Exclusions

- `docs/`
- `reports/`
- `prompts/`
- `ops/ovh/`
- `OPS/`
- `tests/`
- `frontend/tests/`
- `frontend/docs/`
- `frontend/reports/`
- `frontend/node_modules/`
- `frontend/dist/`
- `frontend/**/*.test.ts`
- `frontend/**/*.test.tsx`
- `frontend/**/*.spec.ts`
- `frontend/**/*.spec.tsx`
- `scripts/benchmark_runtime.py`
- `scripts/bench_hot_paths.py`
- `scripts/generate_program_l_tests.py`
- `scripts/smoke_runtime.py`
- `scripts/smoke_postgres.py`
- `scripts/run-compose-dev.sh`
- `scripts/run-compose-staging.sh`
- `scripts/run-compose-postgres.sh`
- `scripts/run-local.sh`
- `deployment/runbook/`
- `deployment/checklists/`
- `deployment/tests/`
- `deployment/validator/`
- `deployment/acceptance/`
- `deployment/orchestrator/`
- `deployment/release-z/`
- `deployment/backup/backup-policy.md`
- `deployment/environments/production/*.md`
- `compose/README.md`
- `code/lawim_v2/migration.py`
- caches, logs, temp files, backups, archives, and generated build outputs
- local-only migration scaffold files
- real secrets and runtime secret material

## Reproducibility rules

- rebuild from the same Git commit and the same tracked inputs;
- keep secrets external and out of the repository;
- write bundle hashes to `checksums/`;
- compare the manifest and checksum files between releases before promotion.
