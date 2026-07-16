# LAWIM — OPERATIONAL HANDOVER

**Version:** 2.0.0  
**Status:** FROZEN — MAINTENANCE MODE

---

## Architecture Overview

```
Frontend (Static HTML/JS) → HTTP Server (Python) → PostgreSQL
    ↕                        ↕
WhatsApp ← Green API    Telegram Bot API    Campay
```

## Services

| Service | Entry Point | Port | Health Check |
|---------|-------------|------|-------------|
| HTTP Server | `python3 -m lawim_v2.server` | 8080 | `GET /api/health` |

## Deployment

```bash
git checkout main
python3 -m lawim_v2.server
```

## Rollback

```bash
git checkout <previous-tag>
# Feature flags: set to false to disable any capability
```

## Backup

```bash
pg_dump -Fc lawim_v2 > /backups/lawim_v2_$(date +%Y%m%d).dump
```

## Restore

```bash
pg_restore -d lawim_v2 /backups/lawim_v2_YYYYMMDD.dump
```

## Incidents

| Scenario | Action |
|----------|--------|
| WhatsApp down | Check Green API token, verify webhook URL |
| Telegram down | Check bot token, verify webhook via `getWebhook` |
| Campay failure | Check credentials, verify callback endpoint |
| Agent loop | Disable agent via feature flag |
| High error rate | Check logs, rollback code, disable flags |
| Database failure | Restore from latest backup |

## Feature Flags Emergency

Set any of the 71 flags to `false` to immediately disable the associated functionality. No restart required for program J/K/L/Q/R/S flags.

## Maintenance

Monthly: Sunday 02:00-04:00 WAT. Emergency: as needed.
