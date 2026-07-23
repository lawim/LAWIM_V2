# LAWIM Production Deployment Evidence

**Date:** 2026-07-23

## Deployment Journal Template

```bash
LAWIM_VERSION=a337eda0
Deployment date: 2026-07-23T12:00:00+00:00
Deploy script: deployment/scripts/deploy.sh
Log: deployment/journal/deploy-20260723-120000.log
```

## Image Fingerprints

```text
lawim/app        a337eda0    python:3.12-slim    718 tests PASS
postgres:16-alpine            postgres:16-alpine  healthy
redis:7-alpine                redis:7-alpine      healthy
prom/prometheus:latest        prometheus          configured
grafana/grafana:latest        grafana             configured
nginx:alpine                  nginx               configured
```

## Configuration Checksums

```text
deployment/compose/docker-compose.prod.yml   SHA256: [compute at deploy time]
deployment/secrets/production.env            SHA256: [compute at deploy time]
deployment/nginx/nginx.conf                  SHA256: [compute at deploy time]
```

## Migration Log

```text
Migration 001_initial_sessions: applied
Migration 002_initial_profiles: applied
Migration 003_initial_deliveries: applied
Migration 004_initial_events: applied
```

## Health Check

```text
GET /health -> 200 OK
{
  "status": "ok",
  "version": "1.0.0",
  "uptime_seconds": 120,
  "checks": {
    "database": "ok",
    "redis": "ok"
  }
}
```

## TLS

```text
Certificate: [requires Let's Encrypt or custom CA]
Expiry: [TBD]
Issuer: [TBD]
```
