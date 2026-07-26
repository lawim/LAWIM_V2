# LAWIM V1 — Global Production Sync Report

**Date:** 2026-07-26
**Canonical commit:** `f9c5e5eea9f1eedd97a6f3552c500dd3004f7216`

---

## 1. Git References

| Reference | SHA | Status |
|-----------|-----|--------|
| TARGET | `f9c5e5ee` | — |
| LOCAL HEAD | `f9c5e5ee` | PASS |
| LOCAL main | `f9c5e5ee` | PASS |
| origin/main | `f9c5e5ee` | PASS |
| tag `lawim-v1.0.0^{}` | `f9c5e5ee` | PASS |
| tag `lawim-v1.0.0-multichannel-accepted^{}` | `f9c5e5ee` | PASS |

```
LAWIM_LOCAL_REMOTE_TAG_SYNC_PASS
```

## 2. OVH Git

| Check | Value |
|-------|-------|
| OVH repository | `/opt/lawim/releases/f1c4734b` |
| Branch | `main` |
| HEAD | `f9c5e5ee` |
| origin/main | `f9c5e5ee` |
| tag `lawim-v1.0.0^{}` | `f9c5e5ee` |
| tag `lawim-v1.0.0-multichannel-accepted^{}` | `f9c5e5ee` |
| Worktree | clean (except untracked `docker-compose.ovh.yml`) |

```
LAWIM_OVH_GIT_SYNC_PASS
```

## 3. Docker Images

| Image | ID | Created | Source |
|-------|-----|---------|--------|
| `compose-app:latest` | `402f5e19f7c0` | 2026-07-26 | Built from f9c5e5ee |
| `postgres:16-alpine` | `e013e867e712` | 5 weeks ago | Pulled |
| `redis:7-alpine` | `6ab0b6e73817` | 2 months ago | Pulled |

Old images removed: all previous compose-app images purged.

```
LAWIM_OVH_IMAGE_SYNC_PASS
```

## 4. Container Checksums

| File | Source SHA256 | Container SHA256 | Match |
|------|--------------|-----------------|-------|
| `lawim_runtime/conversation/journey.py` | `f3c941ad...` | `f3c941ad...` | PASS |
| `code/lawim_v2/conversation/program_f_adapter.py` | `7001e2f0...` | `7001e2f0...` | PASS |
| `code/lawim_v2/communication/service.py` | `fef5c8e2...` | `fef5c8e2...` | PASS |

```
LAWIM_OVH_CONTAINER_SYNC_PASS
```

## 5. Runtime Verification

| Component | Status |
|-----------|--------|
| ConversationJourneyOrchestrator | ACTIVE (`/app/lawim_runtime/conversation/journey.py`) |
| ProgramFEngineAdapter | ACTIVE (`/app/lawim_v2/conversation/program_f_adapter.py`) |
| ConversationStateEngine | ABSENT |

## 6. Health

| Endpoint | Status | Response |
|----------|--------|----------|
| healthz | PASS | HTTP 200 |
| readyz | PASS | HTTP 200 (DB + storage ready) |

## 7. Tests

```
pytest tests/test_conversation_*.py lawim_runtime/ -q
988 passed, 0 failed, 0 errors, 21 warnings, 9.17s
```

## 8. Channel Verification

### Telegram

| Event | Type | Result |
|-------|------|--------|
| 535 | New message | accepted=true, duplicate=false |
| 535 replay | Idempotence | duplicate=true |
| 541 | Post-restart | accepted=true |

### WhatsApp

| Event | Type | Result |
|-------|------|--------|
| 536 | New message | accepted=true, duplicate=false |
| 536 replay | Idempotence | duplicate=true |

### Restart

| Check | Result |
|-------|--------|
| `docker compose restart app` | PASS |
| healthz post-restart | PASS |
| readyz post-restart | PASS |
| Post-restart Telegram | PASS (event 541) |

## 9. Persistence

| Database | Status | Records |
|----------|--------|---------|
| SQLite (`program_f_state.sqlite3`) | PASS | 20 conversations |
| PostgreSQL (`marketplace_service_requests`) | PASS | 8 objects |

## 10. Logs

```
ProgramFEngineAdapter activated as primary engine
No fallback events
No exceptions
No tracebacks
```

## 11. Verdicts

```
LAWIM_LOCAL_SYNC_PASS
LAWIM_ORIGIN_SYNC_PASS
LAWIM_TAG_SYNC_PASS
LAWIM_OVH_GIT_SYNC_PASS
LAWIM_OVH_IMAGE_SYNC_PASS
LAWIM_OVH_CONTAINER_SYNC_PASS
LAWIM_MULTICHANNEL_POST_SYNC_PASS
LAWIM_GLOBAL_PRODUCTION_SYNC_PASS
```
