# Server Inventory

## Identity

- Hostname: `vps-6da158cc`
- Provider: OVH VPS
- Public IPv4: `164.132.44.192`
- Public IPv6: `2001:41d0:305:2100::1:2af1`
- OS: Ubuntu 26.04 LTS
- Initial login user: `ubuntu`
- Application user: `lawim`

## Storage layout

- root production: `/opt/lawim`
- runtime app: `/opt/lawim/app`
- compose files: `/opt/lawim/compose`
- config: `/opt/lawim/config`
- data: `/opt/lawim/data`
- backups: `/opt/lawim/backups`
- logs: `/opt/lawim/logs`
- secrets: `/opt/lawim/secrets`
- scripts: `/opt/lawim/scripts`
- releases: `/opt/lawim/releases`
- shared runtime files: `/opt/lawim/shared`
- current release symlink: `/opt/lawim/current`

## Persistent data

- PostgreSQL data: `/opt/lawim/data/postgres`
- Redis data: `/opt/lawim/data/redis`
- media: `/opt/lawim/data/media`
- thumbnails: `/opt/lawim/data/thumbnails`
- registry and cache: `/opt/lawim/data/registry`
- shared media/export/import/tmp/cache: `/opt/lawim/shared/*`

## Service model

- application: Docker container
- PostgreSQL: Docker container
- Redis: Docker container
- Nginx: host package on Ubuntu
- TLS: later via domain and Certbot

## Access policy

- use SSH key authentication only
- rotate or replace any provisional password before public exposure
- keep secrets outside Git and outside the payload bundle

