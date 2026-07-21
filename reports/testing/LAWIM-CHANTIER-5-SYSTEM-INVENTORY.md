# LAWIM — Système Inventory (Chantier 5)

**Date :** 2026-07-21
**HEAD :** 1258fe19
**Branche :** release/final-acceptance-and-ovh-readiness-20260721

## Services

| Service | Version | Healthcheck | Dépendances |
|---------|---------|-------------|-------------|
| Backend API (FastAPI/Django) | v2.x | /healthz, /readyz | PostgreSQL, Redis, AI providers |
| Frontend (React SPA) | v1.x | / | Backend API |
| WhatsApp worker | v2.x | via API | Green API |
| Telegram bot | v2.x | via API | Telegram Bot API |
| Celery Worker | v2.x | via backend | Redis, PostgreSQL |
| Celery Beat Scheduler | v2.x | via backend | Redis, PostgreSQL |
| Brain service | v2.x | via backend | PostgreSQL, Redis |
| Agents service | v2.x | via backend | PostgreSQL, Redis |
| Knowledge service | v2.x | via backend | PostgreSQL, Redis |
| Communication service | v2.x | via backend | SMTP, WhatsApp, Telegram |
| Campay Payment | v2.x | via backend | Campay API |
| Nginx reverse proxy | latest | port 80/443 | Frontend, Backend |

## Conteneurs

| Container | Image | Port | Healthcheck |
|-----------|-------|------|-------------|
| lawim-frontend-prod | lawim/frontend:prod | 80 | Nginx |
| lawim-backend-prod | lawim/backend:prod | 8000 | /healthz, /readyz |
| lawim-postgres-prod | postgres:15-alpine | 5432 | pg_isready |
| lawim-redis-prod | redis:7-alpine | 6379 | redis-cli ping |
| lawim-worker-prod | lawim/worker:prod | — | via backend |
| lawim-scheduler-prod | lawim/scheduler:prod | — | via backend |
| lawim-brain-prod | lawim/brain:prod | — | via backend |
| lawim-agents-prod | lawim/agents:prod | — | via backend |
| lawim-knowledge-prod | lawim/knowledge:prod | — | via backend |
| lawim-communication-prod | lawim/communication:prod | — | via backend |
| lawim-campay-prod | lawim/campay:prod | — | via backend |
| lawim-nginx-prod | lawim/nginx:prod | 80, 443 | Nginx |

## Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| /healthz | GET | No | Liveness probe |
| /readyz | GET | No | Readiness probe |
| /api/health | GET | No | API health |
| /api/v2/whatsapp/webhook | POST | Secret (webhook) | WhatsApp inbound |
| /api/v2/telegram/webhook | POST | Secret (webhook) | Telegram inbound |
| /api/v2/conversation | POST | JWT | Web conversation |
| /api/v2/conversation/health | GET | No | Conversation engine health |
| /admin/* | GET/POST | JWT + RBAC | Administration interface |
| /api/v2/auth/* | POST | No / JWT | Authentication endpoints |
| /api/v2/properties/* | GET | JWT | Property search/detail |
| /api/v2/cases/* | GET/POST | JWT | Case management |

## Providers IA

| Provider | Model | Endpoint | Circuit breaker |
|----------|-------|----------|-----------------|
| DeepSeek | deepseek-v4-flash | api.deepseek.com | 3 fails → 60s OPEN |
| OpenAI | gpt-4o-mini | api.openai.com | 3 fails → 60s OPEN |
| Gemini Primary | gemini-3.5-flash | generativelanguage.googleapis.com | 3 fails → 60s OPEN |
| Gemini Secondary | gemini-2.5-flash | generativelanguage.googleapis.com | 3 fails → 60s OPEN |
| Internal (rule-based) | N/A | N/A | N/A (fallback final) |

## Canaux

| Channel | Provider | Webhook | Status |
|---------|----------|---------|--------|
| Web | REST API | N/A | IMPLEMENTED |
| WhatsApp | Green API | /api/v2/whatsapp/webhook | TECHNICALLY_REACHABLE |
| Telegram | Bot API | /api/v2/telegram/webhook | TECHNICALLY_REACHABLE |
| Email | SMTP | N/A | IMPLEMENTED |

## Bases de données

| DB | Type | Version | Backup | Persistance |
|----|------|---------|--------|-------------|
| PostgreSQL | Relationnelle | 15 (prod) / 16 (dev) | pg_dump + rclone | Volume Docker |
| Redis | Cache / Queue | 7 | RDB/AOF | Volume Docker |

## Volumes Docker

| Volume | Montage | Usage |
|--------|---------|-------|
| postgres_data_prod | /var/lib/postgresql/data | Données PostgreSQL |
| redis_data_prod | /data | Cache Redis |
| nginx_cache | /var/cache/nginx | Cache Nginx |

## Migrations

- `prisma/migrations/20260714160000_mission_3_conversation_v2/` — tables conversation_v2
- Migration framework: `migration.py` with version tracking
- Rollback: `migration-rollback.sh`
- Schema version: v19 (PostgreSQL, production)
- Toutes les migrations sont additives, aucune destructive

## Réseaux Docker

| Réseau | Type | Usage |
|--------|------|-------|
| lawim_v2_public | bridge | Exposition publique |
| lawim_v2_private | bridge (internal) | Communication interne sécurisée |
| lawim-network | bridge | Réseau de production |

## Dépendances externes

| Service | Dépendance | Statut |
|---------|-----------|--------|
| Green API | WhatsApp | authorized |
| Telegram Bot API | Telegram | ok: true |
| DeepSeek API | LLM | Configuré |
| OpenAI API | LLM fallback | Configuré |
| Gemini API | LLM fallback | Configuré |
| Campay API | Paiements | Configuré (sandbox) |
| SMTP | Email | Configuré |
