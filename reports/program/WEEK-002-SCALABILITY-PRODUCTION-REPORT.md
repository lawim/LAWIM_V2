# WEEK 002 — Scalability & Production Report

- **Date:** 2026-06-29
- **Branch:** `release/1.0.0-beta`
- **Base tag:** `v1.0.0-rc1`
- **Scope:** Production scalability, performance, observability (no new business features)

---

## 1. Optimisations réalisées

| Area | Change |
|------|--------|
| **Conversation detail** | `get_conversation()` uses indexed per-conversation subqueries instead of full-table window CTE |
| **Property listing** | Already used aggregated CTE for media/conversation counts (retained) |
| **Audit log** | `list_events(kind=…)` filter for admin queries (uses new index) |
| **Metrics** | Per-request latency tracking (p50/p95/max) + top routes |
| **Readiness** | `/readyz` now probes media storage writability |
| **UI** | `refresh()` guarded against concurrent in-flight calls |
| **Benchmark** | `scripts/benchmark_runtime.py` — reproducible 20-iteration probe |

---

## 2. Indexes ajoutés

| Index | Tables | Purpose |
|-------|--------|---------|
| `idx_events_kind_created` | events | Audit filter by kind + time |
| `idx_sessions_user_expires` | sessions | Session lookup / expiry sweep |
| `idx_sessions_expires_at` | sessions | Global session cleanup |
| `idx_properties_owner_status` | properties | Seller org listing by status |

Aligned across: `schema_ddl.py` (PG + SQLite), `schema_migrations.py` (legacy SQLite), `persistence.py` manifest, `prisma/schema.prisma`, migration SQL (synced).

**Schema fingerprint updated:** `c2e5c04f…926ac` (manifest v5 unchanged).

---

## 3. Performance

Benchmark local (`scripts/benchmark_runtime.py`, SQLite, 20 iterations):

| Route | p50 (ms) | p95 (ms) |
|-------|----------|----------|
| `/healthz` | ~1.4 | ~2.7 |
| `/readyz` | ~2.4 | ~4.5 |
| `/api/health` | ~1.7 | ~3.1 |
| `/api/properties?limit=10` | (see full JSON output) | — |
| `/api/bootstrap` | (see full JSON output) | — |

PostgreSQL smoke init: **~50 ms** on Podman container (port 5433).

All critical routes remain well under 250 ms p95 on dev hardware.

---

## 4. Sécurité

No regression — RC1 hardening retained:

- CORS allowlist
- Auth rate limiting
- Payload limits
- Optional private media
- Production `AppConfig.validate()` enforced

**New:** `platform/validate-production.sh` — validates production env contract (HTTPS, no PG fallback, no public media, external secrets).

---

## 5. Observabilité

| Capability | Status |
|------------|--------|
| Structured HTTP logs | JSON `http_request` (existing) |
| Request completion debug | `request_complete` with `duration_ms` |
| Metrics snapshot | `latency_ms`, `routes_top` added |
| `/healthz` | Liveness |
| `/readyz` | DB + storage readiness |
| `/api/metrics` | Admin-only (existing) |
| Audit `/api/events?kind=` | Kind filter for operators |

---

## 6. PostgreSQL

- DDL/index alignment verified via `validate_prisma_manifest.py` PASS
- **6/6** integration tests PASS via `./platform/run-postgres-tests.sh`
- `smoke_postgres.py` reports `init_ms` timing
- SQLite fallback unchanged

---

## 7. Tests

| Suite | Result |
|-------|--------|
| Total | **90** run |
| Passed | **88** |
| Skipped | 2 (PG without system pg8000 in `run-tests.sh`) |
| New | `tests/test_week002_production.py` (8 cases) |

---

## 8. Validations finales

| Gate | Result |
|------|--------|
| `./scripts/validate-install.sh` | PASS |
| `./scripts/validate-packaging.sh` | PASS |
| `./scripts/run-tests.sh` | PASS (90 tests) |
| `validate_prisma_manifest.py` | PASS |
| `smoke_runtime.py` | PASS |
| `./platform/validate-platform.sh` | PASS (with postgres started) |
| `./platform/run-postgres-tests.sh` | PASS |
| `git diff --check` | PASS |
| `platform/validate-production.sh` | PASS |

---

## 9. Limites restantes

1. `./scripts/run-tests.sh` skips PG modules without platform venv/DSN.
2. `./platform/validate-platform.sh` requires `./platform/start-postgres.sh` first on this host.
3. Metrics remain in-process (not exported to Prometheus yet).
4. `docker compose up` still fails on Podman-only hosts (use `platform/compose.sh`).
5. No automated browser E2E load testing.

---

## 10. Recommandation GA 1.0.0

**Proceed toward GA** after:

1. Staging deployment with `platform/validate-production.sh` against real env vars
2. Manual QA sign-off (`RC_READINESS_CHECKLIST.md`)
3. PostgreSQL validated on target infra (not only local Podman)
4. Optional: wire metrics export / external APM before high-traffic production

WEEK 002 materially improves production readiness without expanding product scope. RC1 + WEEK 002 provide a solid GA candidate base.

**Tag:** `week-002-scalability-production`
