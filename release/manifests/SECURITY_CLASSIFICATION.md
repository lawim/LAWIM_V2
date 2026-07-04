# SECURITY_CLASSIFICATION

## Local only

- docs, reports, prompts, tests, notes, roadmaps, and governance files
- caches, logs, temp directories, generated build outputs, and archives
- local tooling such as benchmarks, smoke helpers, and validation harnesses
- local-only migration scaffold files
- hidden tooling folders such as `.agents`, `.cursor`, `.lawim`

## Distributed servers

- runtime code under `code/lawim_v2/`
- frontend source and runtime assets under `frontend/`
- database contracts under `prisma/`
- compose and deployment manifests under `compose/` and `deployment/`
- example environment files under `env/` and `deployment/environments/production/`
- launch and operations scripts that do not contain secrets

## OVH

- the minimized payload defined in `DEPLOYMENT_MANIFEST.md`
- runtime code, runtime assets, Docker and compose definitions, Nginx, systemd, health checks, and example configuration
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

