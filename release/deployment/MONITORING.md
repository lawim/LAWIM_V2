# MONITORING

## Health sources

- backend service checks in `deployment/health/health_checker.py`
- HTTP readiness checks from the application runtime
- Docker health checks defined in the Dockerfiles
- compose-level health checks in the production and staging manifests

## What to watch

- service availability
- database connectivity
- Redis connectivity
- release checksum drift
- backup freshness
- log growth and error spikes

## Operational rule

Monitoring must never require real secrets in the repository and must never mutate the database during validation.

