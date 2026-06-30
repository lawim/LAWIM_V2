# LAWIM_V2 RC 1.0.0 — Readiness Checklist

Use this checklist before promoting `rc-1.0.0-candidate` to a final 1.0.0 release.

---

## Repository gates (automated)

- [ ] `./scripts/validate-install.sh` — PASS
- [ ] `./scripts/validate-packaging.sh` — PASS
- [ ] `./scripts/run-tests.sh` — PASS (82 tests; PostgreSQL tests skip locally without DSN)
- [ ] `python3 scripts/validate_prisma_manifest.py` — PASS
- [ ] `python3 scripts/smoke_runtime.py` — PASS
- [ ] `git diff --check` — PASS
- [ ] Docker Compose config (×4 stacks) — PASS

---

## Security (production)

- [ ] `APP_ENV=production`
- [ ] `PUBLIC_BASE_URL` uses HTTPS
- [ ] `LAWIM_CORS_ORIGINS` lists only trusted frontends
- [ ] `LAWIM_PUBLIC_MEDIA=false` (or CDN with signed URLs documented)
- [ ] `LAWIM_DB_FALLBACK=false` when using PostgreSQL
- [ ] Demo seed disabled: `LAWIM_SEED_DEMO_DATA=false`
- [ ] Secrets injected externally (`SECRET_PROVIDER=external`)

---

## Runtime probes

- [ ] `GET /healthz` → `200 ok` (liveness)
- [ ] `GET /readyz` → `200` with `"status":"ready"` when DB is up
- [ ] `GET /api/health` → minimal payload for guests; detailed for admin

---

## PostgreSQL (if used)

- [ ] `pip install -r requirements-postgresql.txt`
- [ ] `LAWIM_TEST_POSTGRES_URL` set for integration tests
- [ ] `python3 scripts/smoke_postgres.py` — PASS
- [ ] Prisma migration applied in target environment

---

## CI (GitHub Actions)

- [ ] `validate` job green
- [ ] `compose` job green
- [ ] `postgres` job green (with service container)

**CI variables:** `LAWIM_TEST_POSTGRES_URL` (set in workflow for postgres job; optional locally).

---

## Manual smoke (recommended)

- [ ] Login as admin, seller, buyer demo accounts (when seed enabled)
- [ ] Property search, match, conversation, message flow
- [ ] Media upload (multipart)
- [ ] Admin: users list, metrics, audit events
- [ ] UI: journey tabs, empty states, error notices

---

## Documentation

- [ ] `RELEASE_NOTES_RC_1.0.0.md` reviewed
- [ ] `BETA_DISTRIBUTION_GUIDE.md` still accurate for rollout process
- [ ] Production `.env` filled from `env/production/.env.example`

---

## Sign-off

| Role | Name | Date | OK |
|------|------|------|-----|
| Engineering | | | |
| QA | | | |
| Security | | | |
| Product | | | |

**Decision:** ☐ Promote to GA 1.0.0  ☐ Hold RC  ☐ Revert to Beta
