# OVH Production Deployment Completion

## Release Record

- Date: 2026-07-09
- Time: 00:16:20 WAT
- Deployed SHA: `88c1e67b36480619f0cb0275df69ef0532ac1eb2`
- Short release: `88c1e67b`
- New release directory: `/opt/lawim/releases/88c1e67b`
- Active symlink: `/opt/lawim/current -> /opt/lawim/releases/88c1e67b`
- Previous release: `/opt/lawim/releases/29eb91c1`
- Rollback state: preserved; the previous release directory remains available for immediate rollback

## Production State

- Docker: `lawim-app` healthy, `lawim-postgres` healthy, `lawim-redis` healthy
- PostgreSQL: healthy and serving the production database
- Redis: healthy and serving the production cache
- Nginx: active, configuration validated with `nginx -t`
- HTTPS: valid on all required public domains
- `/api/health`: `status=ok`
- `admin@lawim.app`: `201`, role `admin`
- `agent@lawim.app`: `201`, role `agent`
- `owner@lawim.app`: `201`, role `owner`

## Tests Executed

- `curl` checks against:
  - `http://127.0.0.1:3000/api/health`
  - `http://127.0.0.1:3000/api/auth/login`
- `docker ps`
- `docker logs --tail 20 lawim-app`

## Anomalies Corrected

- The initial deployment attempt hit a fixed-name collision on `lawim-redis`.
- Legacy containers `lawim-redis`, `compose-app-1` and `compose-postgres-1` were removed before the final promotion so the new stack could bind its canonical names.
- The release was then promoted successfully from `/opt/lawim/releases/88c1e67b`.

## Release Record

- Date: 2026-07-05
- Time: 15:08:51 WAT
- Deployed SHA: `4c078fd8139f98d6cc34c6e6ff452165bee10bdd`
- Short release: `4c078fd8`
- New release directory: `/opt/lawim/releases/4c078fd8`
- Active symlink: `/opt/lawim/current`
- Previous release: `/opt/lawim/releases/bc46a686`
- Rollback state: preserved; one initial promotion attempt rolled back automatically, then the final promotion succeeded

## Production State

- Docker: `lawim-app` healthy, `lawim-postgres` healthy, `lawim-redis` healthy
- PostgreSQL: healthy and serving the production database
- Redis: healthy and serving the production cache
- Nginx: active, configuration validated with `nginx -t`
- HTTPS: valid on all required public domains
- `lawim.app`: HTTP 200
- Media Registry: present in the deployed snapshot and covered by the validation suite
- Conversation Registry: present in the deployed snapshot and covered by the validation suite
- Storage Orchestrator: present in the deployed snapshot and covered by the validation suite
- Backup Center: present in the deployed snapshot and covered by the validation suite
- Restore Center: present in the deployed snapshot and covered by the validation suite
- Archive Center: present in the deployed snapshot and covered by the validation suite
- Google Drive Registry: prepared as runtime infrastructure only; no credentials were requested

## Tests Executed

- `./scripts/run-tests.sh`
- `./scripts/validate-packaging.sh`
- `curl` checks against:
  - `https://lawim.app`
  - `https://www.lawim.app`
  - `https://app.lawim.app`
  - `https://api.lawim.app`
  - `https://admin.lawim.app`
  - `https://docs.lawim.app`
  - `https://status.lawim.app`
  - `https://api.lawim.app/healthz`
  - `https://api.lawim.app/api/health`
- `nginx -t`
- `docker ps`
- `docker logs --tail 20 lawim-app`

## Migrations

- Prisma schema validation: passed
- Runtime schema and manifest validation: passed
- SQLite migration: no runtime migration executed during this deployment
- PostgreSQL migration: no runtime migration executed during this deployment
- Prisma migration: no runtime migration executed during this deployment

## Anomalies Corrected

- The first remote extraction of the new release was incomplete and left the `deployment/`, `platform/`, and `templates/` trees missing
- The remote release directory was resynchronized to `4c078fd8` before promotion
- The initial compose rebuild ran without the production env file and was rolled back
- The promotion was repeated with `--env-file /opt/lawim/secrets/.env`

## Remaining Actions

- Google Drive account wiring for drives 1 through 10
- Local backup scheduling
- External disk backup scheduling
- Retention policy wiring
- Monitoring, quota, alert, rotation, sync, and restore configuration
- WhatsApp Business configuration
- Facebook integration configuration
- Distributed storage configuration
