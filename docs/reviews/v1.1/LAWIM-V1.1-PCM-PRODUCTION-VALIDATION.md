# LAWIM V1.1 — PCM Production Validation

**Date:** 2026-07-26
**Canonical HEAD:** `4d65582ad956c88f6c132b348616da2e85105e5d`
**Tag:** `lawim-v1.1.0`

---

## 1. Git Alignment

| Reference | SHA | Status |
|-----------|-----|--------|
| LOCAL HEAD | `4d65582a` | PASS |
| origin/main | `4d65582a` | PASS |
| tag `lawim-v1.1.0^{}` | `4d65582a` | PASS |
| tag `lawim-v1.0.0^{}` | `28a9a6da` | PRESERVED |
| OVH Git HEAD | `4d65582a` | PASS |

Evidence: `docs/reviews/evidence/lawim-v1.1-production/raw/git/`

## 2. Docker

| Image | Tag | Status |
|-------|-----|--------|
| `compose-app` | latest (built from 4d65582a) | ACTIVE |
| `postgres` | 16-alpine | ACTIVE |
| `redis` | 7-alpine | ACTIVE |

Containers: lawim-app (healthy), lawim-postgres (healthy), lawim-redis (healthy)

Evidence: `docs/reviews/evidence/lawim-v1.1-production/raw/docker/`

## 3. Tests

| Suite | Collected | Passed | Failed | Skipped |
|-------|----------:|------:|------:|--------:|
| PCM Gold | 35 | 28 | 0 | 7 |
| V1 Canonical | 988 | 988 | 0 | 0 |
| Full collection | 5,087 | — | — | — |

Evidence: `docs/reviews/evidence/lawim-v1.1-production/raw/tests/`

## 4. Channel Verification

### Telegram
| Event | Type | Result |
|-------|------|--------|
| 542 | PCM initial | accepted=true, duplicate=false |
| 545 | Language switch (PCM→FR) | accepted=true |
| 547 | PCM post-restart | accepted=true, restart=true |
| 548 | PCM production | accepted=true |
| 553 | PCM post-restart (2nd) | accepted=true, restart=true |

### WhatsApp
| Event | Type | Result |
|-------|------|--------|
| 543 | PCM initial | accepted=true |
| 550 | PCM production | accepted=true |

Evidence: `docs/reviews/evidence/lawim-v1.1-production/normalized/channel-events.jsonl`

## 5. Language Switch

Sequence tested on Telegram:
```
I wan rent house → PCM (detected)
Continue en français → FR (explicit switch)
Mon budget est de 180000 → FR (stable)
Speak English → EN (explicit switch)
Two bedrooms → EN (stable)
Abeg talk for Pidgin → PCM (explicit switch)
September → PCM (short message stable)
```

Verdict: PASS — PCM → FR → EN → PCM without fact loss

## 6. Persistence

| Database | Status | Details |
|----------|--------|---------|
| SQLite | PASS | Conversations preserved across restart |
| PostgreSQL | PASS | Objects preserved across restart |

## 7. Rollback

| Mechanism | Value |
|-----------|-------|
| V1 baseline tag | `lawim-v1.0.0` @ `28a9a6da` |
| Production release | `/opt/lawim/releases/f1c4734b` |
| Rollback command | `sudo ln -sfn /opt/lawim/releases/f1c4734b /opt/lawim/current && docker compose build --no-cache app && docker compose up -d --force-recreate app` |

## 8. Runtime Components

| Component | Status |
|-----------|--------|
| ConversationJourneyOrchestrator | ACTIVE |
| ProgramFEngineAdapter | ACTIVE |
| ConversationStateEngine | ABSENT |

## 9. Health

| Endpoint | Status |
|----------|--------|
| healthz | HTTP 200 |
| readyz | HTTP 200 |

## 10. Verdict

```
LAWIM_V1_1_PRODUCTION_VALIDATION_PASS
LAWIM_V1_1_RELEASE_AUTHORIZED
```
