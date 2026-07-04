# RELEASE_MANIFEST

## Snapshot

- Release family: LAWIM_V2 Gate 1
- Snapshot id: `release-program-aae-bootstrap-2-g749648a1-dirty`
- Source commit: `749648a1`
- Purpose: reproducible release projection before Gate 2 migration

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
- `tests/`
- caches, logs, temp files, backups, archives, and generated build outputs
- local-only migration scaffold files
- real secrets and runtime secret material

## Reproducibility rules

- rebuild from the same Git commit and the same tracked inputs;
- keep secrets external and out of the repository;
- write bundle hashes to `checksums/`;
- compare the manifest and checksum files between releases before promotion.

