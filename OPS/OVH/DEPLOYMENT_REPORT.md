# Deployment Report

## Summary

LAWIM_V2 was deployed on the OVH VPS using the approved runtime bundle and the `/opt/lawim` server layout.

## Operations performed

- created the server directory tree under `/opt/lawim`;
- installed or verified Docker, Docker Compose v2, Nginx, Certbot and firewall tooling;
- created Docker networks for public, private and data traffic;
- transferred the approved release bundle only;
- extracted the release into `/opt/lawim/releases/bc46a686`;
- pointed `/opt/lawim/current` to the deployed release;
- created server-side environment and secret files under `/opt/lawim/secrets/`;
- created a pre-start backup under `/opt/lawim/backups/pre-start/`;
- started the application, PostgreSQL and Redis containers;
- configured host Nginx;
- validated health endpoints and geolocation search.

## Notable commands

- `docker compose up -d`
- `curl -k https://164.132.44.192/healthz`
- `curl -k https://164.132.44.192/readyz`
- `curl -k https://164.132.44.192/api/health`
- `curl -k "https://164.132.44.192/api/geo/search?q=Douala"`

## Errors and corrections

- The first login validation failed because the PostgreSQL adapter added `RETURNING id` to `sessions`.
- The adapter was corrected so only tables with a real auto-generated `id` use that path.

## Result

- runtime is active;
- backups exist;
- TLS proxying works for validation;
- login validation is expected to recover after the adapter fix and redeployment.

## Duration

- same-session deployment and validation; the full sequence ran in a single maintenance window on `2026-07-05`.
