# LAWIM_V2 — WEEK 002 Scalability / Performance / Production Report

- **Date:** 2026-06-30
- **Repository:** `/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2`
- **Branch:** `release/1.0.0-beta`
- **Required tag:** `v1.0.0-rc1`
- **Scope:** performance, scalability, production hardening only. No business features added.

---

## 1. Preflight

| Check | Status |
|-------|--------|
| Repository root | PASS |
| Branch `release/1.0.0-beta` | PASS |
| Tag `v1.0.0-rc1` | PASS |
| Clean worktree before changes | PASS |

---

## 2. What changed

| Area | Change |
|------|--------|
| PostgreSQL / SQLite queries | Removed redundant `LOWER(...)` comparisons from indexed filters by normalizing inputs once; replaced correlated count subqueries with CTE/aggregate joins; collapsed summary counts into one query; removed the 100-user notification fan-out cap by querying organization recipients directly. |
| Cache | Added in-memory static asset caching in the HTTP server. |
| API | Switched JSON responses to compact serialization; added structured JSON request logs. |
| Bootstrap path | Eliminated duplicate bootstrap queries by reusing repository payloads and preserving access filtering for users/conversations. |
| UI | Cached the number formatter and batched list rendering with `DocumentFragment` / `replaceChildren()` to reduce DOM churn. |
| Schema / DDL | Removed the redundant session-token index, added targeted read indexes for organizations, users, properties, media, conversations, and events; kept Prisma, runtime DDL, and migration SQL aligned. |
| Repro tooling | Added `scripts/bench_hot_paths.py` for repeatable local benchmarking. |

---

## 3. Validation

| Validation | Result | Notes |
|------------|--------|-------|
| `python3 -m unittest discover -s tests -p 'test_*.py'` | PASS | 82 tests, 3 skipped |
| `python3 scripts/validate_prisma_manifest.py` | PASS | Prisma schema, runtime DDL, and migration SQL aligned |
| `python3 scripts/bench_hot_paths.py --iterations 25` | PASS | Reproducible hot-path benchmark completed |

### Benchmark snapshot

| Hot path | Mean | Median | p95 |
|----------|------|--------|-----|
| `repository.summary` | 0.020 ms | 0.020 ms | 0.061 ms |
| `repository.list_properties` | 0.314 ms | 0.272 ms | 0.843 ms |
| `services.list_conversations` | 0.194 ms | 0.184 ms | 0.276 ms |
| `services.bootstrap` | 1.594 ms | 1.438 ms | 2.431 ms |
| `repository.search_locations` | 0.069 ms | 0.065 ms | 0.084 ms |

Benchmark context: seeded temporary SQLite repository, 25 iterations per path.

---

## 4. Production notes

- The bootstrap path now avoids unnecessary duplicate reads while preserving access control for anonymous, owner/agent, and admin callers.
- Notification fan-out no longer truncates organization recipients at 100 users.
- The runtime remains compatible with PostgreSQL and SQLite, and the manifest validation stayed green after the schema/index changes.
- No push was performed because no remote is configured.

---

## 5. Decision

**PASS:** the repository is prepared for a higher-load production posture without adding business scope.
