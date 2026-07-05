# SECURITY_CLASSIFICATION

## Local only

- docs, reports, prompts, tests, notes, roadmaps, and governance files
- the local operating memory under `OPS/`
- the local operating notes under `ops/ovh/`
- raw LAWIM and LAWIMA source snapshots used for analysis
- internal comparison reports under `reports/comparison/` and the storage prompt `prompts/Storage_organisation_lawim.md`
- the local migration scaffold `code/lawim_v2/migration.py` and its validation harness `tests/test_migration_framework.py`
- caches, logs, temp directories, generated build outputs, and archives
- local tooling such as benchmarks, smoke helpers, and validation harnesses
- hidden tooling folders such as `.agents`, `.cursor`, `.lawim`

## Distributed servers

- runtime code under `code/lawim_v2/`, including the curated geo stack and `code/lawim_v2/data/`
- frontend source and runtime assets under `frontend/`
- database contracts under `prisma/`
- compose and deployment manifests under `compose/` and `deployment/`
- example environment files under `env/` and `deployment/environments/production/`
- launch and operations scripts that do not contain secrets

## OVH

- the minimized payload defined in `DEPLOYMENT_MANIFEST.md`
- runtime code, runtime assets, the curated geo reference bundle, Docker and compose definitions, Nginx, systemd, health checks, and example configuration
- deployment backup placeholders under `deployment/backup/` such as `postgres-init.sql` and `postgresql.conf` when mounted by compose
- no real secret, no test, and no internal document

## External backup

- database dumps
- cold archives
- release tarballs and checksum archives
- rotated logs
- media exports and restore snapshots
- secret material stored in a vault or other external secret provider

## Rule

No real secret lives in Git. Only placeholder example files are allowed in the repository.
