# LAWIM_V2 — Operations Guide

**Document ID:** LAWIM-OPS-GUIDE-V1
**Status:** OPERATIONAL
**Date:** 2026-07-15

---

## 1. Deployment

### Prerequisites

- Python 3.12+
- PostgreSQL 15+ (or SQLite for development)
- pip dependencies from `requirements.txt` or `pyproject.toml`

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | — | PostgreSQL connection string |
| `APP_ENV` | Yes | `development` | `development`, `staging`, `production` |
| `SECRET_KEY` | Yes | — | Session signing key (min 32 chars) |
| `GREEN_API_TOKEN` | No | — | WhatsApp API token |
| `TELEGRAM_BOT_TOKEN` | No | — | Telegram bot token |
| `CAMPAY_USERNAME` | No | — | Campay API username |
| `CAMPAY_PASSWORD` | No | — | Campay API password |
| `SMTP_*` | No | — | Email configuration |

### Startup

```bash
python3 -m lawim_v2.server
```
Server starts on port 8080 by default.

## 2. Monitoring

### Health Check

```
GET /api/health
```

Returns database status, schema version, and service status.

### Metrics

```
GET /api/metrics
```

Returns application metrics including counters for CRM, communication, and API requests.

### Alerts

Critical alert conditions:
- **Service down**: Health check fails 3 consecutive times
- **Database unavailable**: Connection refused or timeout
- **High error rate**: >5% 5xx responses over 5 minutes
- **Webhook failures**: WhatsApp or Telegram delivery failures
- **Payment failures**: Campay callback missing or error status
- **Backup failure**: Scheduled backup did not complete
- **Disk space**: <10% free on data volume

## 3. Backup and Restore

### Backup

```bash
pg_dump -Fc lawim_v2 > /backups/lawim_v2_$(date +%Y%m%d).dump
```

### Restore

```bash
pg_restore -d lawim_v2 /backups/lawim_v2_YYYYMMDD.dump
```

## 4. Rollback

### Code Rollback

```bash
git checkout <previous_tag>
python3 -m lawim_v2.server
```

### Database Rollback

Migrations are additive. Rollback by reverting the code to the previous version that matches the database schema.

### Feature Flag Rollback

Set any feature flag to `false` to immediately disable the associated functionality.

## 5. Incident Response

1. **Detect**: Monitoring alert or user report
2. **Assess**: Determine impact and severity
3. **Contain**: Disable feature flags, rollback code, or block traffic
4. **Resolve**: Apply fix or restore from backup
5. **Verify**: Confirm service恢复正常
6. **Document**: Record incident timeline and root cause

## 6. Maintenance Windows

Standard maintenance: Monthly, Sunday 02:00-04:00 WAT
Emergency maintenance: As needed, with notification
