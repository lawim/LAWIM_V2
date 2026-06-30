# WEEK 001 — Beta to Release Candidate Report

- **Date:** 2026-06-29
- **Repository:** `/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2`
- **Branch:** `release/1.0.0-beta`
- **Target tag:** `rc-1.0.0-candidate`
- **Scope:** Harden Beta 1.0.0 into Release Candidate (no new business features)

---

## 1. Executive summary

WEEK 001 executed a full engineering cycle across security, observability, PostgreSQL validation, CI, UI maturity, tests, and packaging. The Beta baseline was structurally sound (74 passing tests, validated install/packaging, Prisma alignment); the main gaps were production-unsafe defaults (open CORS, unauthenticated media option, no auth rate limits), missing readiness probes, thin PostgreSQL coverage, and minor UI fragility.

**Outcome:** Substantive hardening landed. All mandatory validation gates pass locally. Test count increased to **82** (2 skipped without local PostgreSQL DSN). RC artifacts (`RELEASE_NOTES_RC_1.0.0.md`, `RC_READINESS_CHECKLIST.md`) are published.

**Proposed decision:** Accept `rc-1.0.0-candidate` for staged rollout with production checklist enforced; hold GA until PostgreSQL is exercised in a target environment and manual journey QA is signed off.

---

## 2. Work performed

| Phase | Actions |
|-------|---------|
| A — Audit | Full codebase cartography; gaps documented in prior audit |
| B — PostgreSQL | `tests/test_rc_postgresql.py`, `scripts/smoke_postgres.py`, CI postgres job expanded |
| C — CI/CD | Validate job: packaging + smoke; postgres job: RC tests + smoke |
| D — Security | CORS allowlist, auth rate limiting, optional private media, production config validation |
| E — Observability | `/readyz` with DB check; smoke extended for `/healthz` + `/readyz` |
| F — UI/UX | Demo credential gating, conversation error handling, multipart JSON safety |
| G — Packaging | `scripts/smoke-runtime.sh` wrapper; production env example updated |
| H — Tests | `tests/test_rc_hardening.py` (8 cases), harness rate-limiter wiring fix |
| I — RC | Release notes, checklist, this report |

**Files touched (high level):** `config.py`, `server.py`, `services.py`, `rate_limit.py`, `app.js`, CI workflow, smoke scripts, env example, tests.

---

## 3. PostgreSQL

| Item | Status |
|------|--------|
| `requirements-postgresql.txt` / pg8000 | Verified; optional locally |
| Compose postgres stack | Config valid (×4 compose pairs) |
| Conditional tests | `test_rc_postgresql.py` (5 tests), existing `PostgreSQLIntegrationTest` |
| `smoke_postgres.py` | Added; skips gracefully without DSN |
| Prisma / DDL alignment | Unchanged; `validate_prisma_manifest.py` PASS |
| SQLite fallback | Preserved; default for dev |

**Local note:** `LAWIM_TEST_POSTGRES_URL` not set — PostgreSQL tests skipped locally; CI postgres job covers integration when service container is available.

---

## 4. CI/CD

Workflow `.github/workflows/ci.yml`:

- **validate:** install, packaging, smoke (unchanged test discovery via install script)
- **compose:** four stack configs
- **postgres:** productization + RC PostgreSQL tests + `smoke_postgres.py`

**CI variables documented:** `LAWIM_TEST_POSTGRES_URL=postgresql://lawim:lawim@localhost:5432/lawim_v2` (postgres job).

---

## 5. Security

| Risk (Beta) | RC mitigation |
|-------------|---------------|
| CORS `*` | Allowlist via `LAWIM_CORS_ORIGINS` |
| No auth rate limit | `AuthRateLimiter` on login/register |
| Public `/media/*` | `LAWIM_PUBLIC_MEDIA` (required false in production validate) |
| Weak production config | `AppConfig.validate()` enforces HTTPS URL, no PG fallback, no public media |
| Security headers | Unchanged (already present); verified by tests |

**Residual:** Bearer-authenticated media incompatible with `<img src>` without signed URLs or public media flag — documented in release notes.

---

## 6. Performance

No architectural performance changes (RC scope). Existing pagination on list endpoints retained. Payload limits unchanged (`LAWIM_MAX_JSON_BODY_BYTES`, upload caps). N+1 patterns not introduced.

---

## 7. Observability

| Endpoint | Role |
|----------|------|
| `/healthz` | Liveness — always `ok` |
| `/readyz` | Readiness — DB `SELECT 1`; 503 when not ready |
| `/api/health` | Application health; admin gets audit/metrics |
| `/api/metrics` | Admin-only in-memory metrics |

Audit log via `/api/events` (admin) unchanged.

---

## 8. UI/UX

- Demo credentials only when `seed_demo_data` enabled; demo button hidden otherwise.
- Conversation selection errors surfaced via notice + empty state.
- Multipart upload errors use consistent API error formatting.

Seller/Buyer/Admin journeys unchanged functionally; regression suite passes.

---

## 9. Packaging

| Gate | Result |
|------|--------|
| `validate-install.sh` | PASS |
| `validate-packaging.sh` | PASS |
| `pyproject.toml` / editable install | PASS |
| `python3 -m build` | Not run — `build` module absent locally; packaging validated via pip editable install |

---

## 10. Tests

| Suite | Count |
|-------|-------|
| Total | 82 run |
| Passed | 80 |
| Skipped | 2 (PostgreSQL without DSN) |
| New | `test_rc_hardening.py`, `test_rc_postgresql.py` |

Coverage additions: CORS, rate limit, readyz, private media, production config, bootstrap feature flag, PostgreSQL auth/list/schema.

---

## 11. Remaining debt

1. Signed URL or cookie-based media for strict production without `LAWIM_PUBLIC_MEDIA`.
2. Persistent metrics / external APM integration.
3. Full E2E browser automation (current E2E is HTTP harness + UI asset checks).
4. `python3 -m build` wheel validation in CI (optional `pip install build`).
5. Readiness probe could include geocoder/media storage checks (not required for RC).

---

## 12. Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Production UI breaks if `LAWIM_PUBLIC_MEDIA=false` without CDN | Medium | Document; default public in non-production |
| Rate limit blocks legitimate burst logins | Low | Configurable limits; 30/5min default |
| PostgreSQL untested on operator infra | Medium | Run checklist + smoke_postgres before GA |
| No remote configured | Low | Tag local only; no push |

---

## 13. Proposed decision

**Accept Release Candidate `rc-1.0.0-candidate`** on branch `release/1.0.0-beta` for:

- Internal/staging deployment with production env checklist
- Beta tester cohort already on distribution kit
- CI green on next push (when remote available)

**Hold general availability (GA 1.0.0)** until:

- Manual QA sign-off on RC checklist
- PostgreSQL validated in at least one staging environment
- Production env review (CORS, media, secrets)

---

## Validation log (final run)

```
./scripts/validate-install.sh     PASS
./scripts/validate-packaging.sh   PASS
./scripts/run-tests.sh            PASS (82 tests, 2 skipped)
python3 scripts/validate_prisma_manifest.py  PASS
python3 scripts/smoke_runtime.py    PASS
git diff --check                  PASS
docker compose (×4)               PASS
```

Commit: `feat(release): harden beta into release candidate`  
Tag: `rc-1.0.0-candidate`
