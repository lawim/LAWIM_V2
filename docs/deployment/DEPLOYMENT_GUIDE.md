# LAWIM_V2 — Deployment Guide

**Document ID:** LAWIM-DEPLOY-GUIDE-V1
**Status:** CANONICAL
**Date:** 2026-07-15

---

## Quick Start

```bash
# Prerequisites
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configure
export DATABASE_URL="postgresql://user:pass@localhost:5432/lawim_v2"
export SECRET_KEY="your-secret-key-min-32-chars"

# Initialize database
python3 -c "from lawim_v2.schema_migrations import apply_all; apply_all()"

# Start server
python3 -m lawim_v2.server
# → http://localhost:8080
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | — | PostgreSQL connection string |
| `SECRET_KEY` | Yes | — | Session signing key (≥32 chars) |
| `APP_ENV` | Yes | `development` | `development`, `staging`, `production` |
| `GREEN_API_TOKEN` | No | — | WhatsApp API token |
| `TELEGRAM_BOT_TOKEN` | No | — | Telegram bot token |
| `CAMPAY_USERNAME` | No | — | Campay username |
| `CAMPAY_PASSWORD` | No | — | Campay password |
| `SMTP_*` | No | — | Email configuration |
| `GOOGLE_MAPS_KEY` | No | — | Maps API key |

## Docker Deployment

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["python3", "-m", "lawim_v2.server"]
```

## Database Migrations

```bash
# Apply all pending migrations
python3 -c "from lawim_v2.schema_migrations import apply_all; apply_all()"

# Check current schema version
python3 -c "from lawim_v2.persistence import APPLICATION_SCHEMA_VERSION; print(APPLICATION_SCHEMA_VERSION)"
```

## Feature Flags

```bash
# Activate via environment
export KNOWLEDGE_RUNTIME_ENABLED=true

# Or via config
python3 -c "
from lawim_v2.knowledge_runtime.config import KnowledgeConfig
cfg = KnowledgeConfig(runtime_enabled=True)
print('Runtime enabled:', cfg.runtime_enabled)
"
```

## Verification

```bash
# Health check
curl https://your-domain.com/api/health

# Smoke test
curl https://your-domain.com/
curl https://your-domain.com/api/v2/crm/official-contact
```
