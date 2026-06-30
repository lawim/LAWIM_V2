# LAWIM_V2 — Release Candidate 1.0.0

**Tag:** `rc-1.0.0-candidate`  
**Base:** Beta 1.0.0 (`v1.0.0-beta`)  
**Branch:** `release/1.0.0-beta`

---

## Summary

This release candidate hardens the Beta 1.0.0 baseline for controlled production rollout. No new business features were added. Focus areas: security, observability, PostgreSQL validation, CI, UI reliability, and packaging.

---

## Security

- **CORS** — `Access-Control-Allow-Origin: *` replaced with an allowlist (`LAWIM_CORS_ORIGINS`, defaulting to `PUBLIC_BASE_URL`).
- **Auth rate limiting** — sliding-window limits on `/api/auth/login` and `/api/auth/register` (`LAWIM_AUTH_RATE_LIMIT_MAX`, `LAWIM_AUTH_RATE_LIMIT_WINDOW_SECONDS`).
- **Media access** — optional authenticated media (`LAWIM_PUBLIC_MEDIA=false`); required in production validation.
- **Production config validation** — rejects HTTP base URL, PostgreSQL with SQLite fallback, and public media when `APP_ENV=production`.

---

## Observability

- **`/readyz`** — readiness probe with database connectivity check (HTTP 503 when DB unavailable).
- **`/healthz`** — unchanged liveness probe (`ok`).
- Smoke tests now cover both probes.

---

## UI / UX

- Demo credentials auto-fill gated by `bootstrap.features.demo_credentials` (only when demo seed is enabled).
- `selectConversation()` handles API errors without breaking the page.
- `apiMultipart()` uses safe JSON parsing consistent with `api()`.

---

## PostgreSQL

- Expanded conditional integration tests (`tests/test_rc_postgresql.py`).
- Optional smoke script: `python3 scripts/smoke_postgres.py` (requires `LAWIM_TEST_POSTGRES_URL`).
- SQLite fallback unchanged and still the default for local development.

---

## CI / Packaging

- CI validate job: packaging validation + runtime smoke.
- CI postgres job: full RC PostgreSQL test module + `smoke_postgres.py`.
- Added `scripts/smoke-runtime.sh` wrapper for `smoke_runtime.py`.

---

## Configuration (new / notable)

| Variable | Default (dev) | Notes |
|----------|---------------|-------|
| `LAWIM_CORS_ORIGINS` | derived from `PUBLIC_BASE_URL` | Comma-separated allowlist |
| `LAWIM_AUTH_RATE_LIMIT_MAX` | 30 | Per client IP per auth route |
| `LAWIM_AUTH_RATE_LIMIT_WINDOW_SECONDS` | 300 | Sliding window |
| `LAWIM_PUBLIC_MEDIA` | `true` (dev/test/staging) | Must be `false` in production |

See `env/production/.env.example` for production-oriented values.

---

## Upgrade from Beta 1.0.0

1. Pull `release/1.0.0-beta` at tag `rc-1.0.0-candidate`.
2. Review production env vars (especially CORS, media, PostgreSQL fallback).
3. Run `./scripts/validate-install.sh` and `./scripts/run-tests.sh`.
4. For PostgreSQL deployments: set `LAWIM_DB_DRIVER=postgresql`, `LAWIM_DB_FALLBACK=false`, and a valid `LAWIM_DATABASE_URL`.

---

## Known limitations (unchanged from Beta)

- In-memory metrics (not persisted).
- Media `<img>` tags cannot send Bearer tokens — use `LAWIM_PUBLIC_MEDIA=true` or CDN/signed URLs for image-heavy UIs until a tokenized media strategy ships.
- PostgreSQL optional locally unless `LAWIM_TEST_POSTGRES_URL` is set.
