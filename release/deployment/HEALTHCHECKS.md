# HEALTHCHECKS

## Application runtime

- `/healthz` returns plain text `ok` with HTTP 200
- `/readyz` returns readiness JSON and can return HTTP 503 when not ready
- `/api/health` returns the API health payload

## Container services

- backend: `http://localhost:8000/health`
- brain: `http://localhost:8001/health`
- agents: `http://localhost:8002/health`
- knowledge: `http://localhost:8003/health`
- communication: `http://localhost:8004/health`
- frontend: `http://localhost:3000/health`

## Validation rule

Health checks are validation only. They must not seed data, modify schemas, or alter runtime state.

