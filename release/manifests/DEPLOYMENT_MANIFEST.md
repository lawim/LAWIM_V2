# DEPLOYMENT_MANIFEST

## Objective

Define the exact payload that can be copied to OVH without touching the master repository.

This manifest is deployment-only. It does not launch migrations and it does not change business behavior.

## OVH payload

Include:

- `Dockerfile`
- `sitecustomize.py`
- `pyproject.toml`
- `requirements.txt`
- `requirements-postgresql.txt`
- `code/lawim_v2/` except the exclusions listed below
- `frontend/` except the exclusions listed below
- `prisma/`
- `compose/*.yml`
- `deployment/compose/*.yml`
- `deployment/docker/Dockerfile.*`
- `deployment/nginx/*.conf`
- `deployment/nginx/conf.d/*.conf`
- `deployment/systemd/*.service`
- `deployment/systemd/*.timer`
- `deployment/health/health_checker.py`
- `deployment/scripts/*.sh`
- `deployment/server/scripts/*.sh`
- `deployment/backup/backup.sh`
- `deployment/backup/restore.sh`
- `deployment/backup/rclone.example.conf`
- `deployment/environments/production/.env.production.example`
- `deployment/environments/production/.env.production.template`
- `deployment/environments/production/secrets.example`
- `env/*/.env.example`
- `env/*/.secrets.example`
- `scripts/run-compose-prod.sh`

Keep from `code/lawim_v2/` only runtime code and assets.

Keep from `frontend/` only source, build configuration, and public runtime assets.

Keep from `env/` only `*.env.example` and `*.secrets.example`.

Keep from `deployment/environments/production/` only example values.

## Explicit exclusions

- `release/`
- `docs/`
- `reports/`
- `prompts/`
- `tests/`
- `scripts/validate-packaging.sh`
- `scripts/benchmark_runtime.py`
- `scripts/bench_hot_paths.py`
- `scripts/generate_program_l_tests.py`
- `scripts/smoke_runtime.py`
- `scripts/smoke_postgres.py`
- `scripts/run-compose-dev.sh`
- `scripts/run-compose-staging.sh`
- `scripts/run-compose-postgres.sh`
- `scripts/run-local.sh`
- `code/lawim_v2/migration.py`
- `compose/README.md`
- `deployment/runbook/`
- `deployment/checklists/`
- `deployment/tests/`
- `deployment/validator/`
- `deployment/acceptance/`
- `deployment/orchestrator/`
- `deployment/release-z/`
- `deployment/backup/backup-policy.md`
- `deployment/environments/production/*.md`
- `frontend/docs/`
- `frontend/reports/`
- `frontend/tests/`
- `frontend/node_modules/`
- `frontend/dist/`
- `frontend/**/*.test.ts`
- `frontend/**/*.spec.ts`
- caches, logs, temp files, backups, archives, and secret stores
- hidden local tooling directories

## Notes

- root compose mode uses `Dockerfile` and `compose/`
- the deployment platform also carries `deployment/compose/`, Docker images, Nginx, systemd, health checks, and server scripts
- no real secret is copied into OVH
- no migration is started during packaging
