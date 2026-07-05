# Server Inventory

## Identity

- Provider: OVH VPS
- Hostname: `vps-6da158cc.vps.ovh.net`
- Public IPv4: `164.132.44.192`
- Public IPv6: `2001:41d0:305:2100::1:2af1`
- OS: Ubuntu 26.04
- Initial user: `ubuntu`
- Application user: `lawim`
- Deployment date: `2026-07-05`

## Runtime layout

- production root: `/opt/lawim`
- application: `/opt/lawim/current`
- releases: `/opt/lawim/releases`
- shared runtime: `/opt/lawim/shared`
- persistent data: `/opt/lawim/data`
- backups: `/opt/lawim/backups`
- logs: `/opt/lawim/logs`
- secrets: `/opt/lawim/secrets`
- compose files: `/opt/lawim/compose`
- scripts: `/opt/lawim/scripts`

## Persistent paths

- PostgreSQL: `/opt/lawim/data/postgres`
- Redis: `/opt/lawim/data/redis`
- media: `/opt/lawim/data/media`
- thumbnails: `/opt/lawim/data/thumbnails`
- registry: `/opt/lawim/data/registry`
- shared exports/imports/tmp/cache: `/opt/lawim/shared/*`

## Container and proxy model

- application container: `lawim-app`
- PostgreSQL container: `lawim-postgres`
- Redis container: `lawim-redis`
- host reverse proxy: native Nginx on Ubuntu
- Docker networks: `lawim-public`, `lawim-private`, `lawim-data`

## Release data

- deployed bundle: `lawim_v2_ovh_bc46a686.tar`
- source commit: `bc46a68664f166d7f079f8dcd48f4e954581fcea`
- local release tag: `pre-ovh-final`
- SHA256: `7644e58bfa80414309b54c38d724cc75b7ced93d8748b6f5b18e95e45cf8b7f2`

## Notes

- No real secret is stored here.
- No schema change is described here.
- No migration instruction is authorized here.
