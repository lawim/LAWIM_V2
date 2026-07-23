# LAWIM — Environment Variable Audit Report

**Date:** 2026-07-23
**Status:** COMPLETE

---

## Méthode

Audit réalisé par traçage des variables d'environnement dans :

- `code/lawim_v2/config.py` — `AppConfig.from_env()` (source de vérité applicative)
- `deployment/compose/docker-compose.prod.yml` — fichier compose production (unique)
- `deployment/compose/docker-compose.staging.yml` — staging
- `deployment/compose/docker-compose.dev.yml` — développement
- `compose/` — anciens fichiers compose legacy
- `deployment/.env.*`, `env/*/.env.*` — templates .env dispersés
- `deployment/secrets/` — anciens fichiers de secrets

## Source de vérité unique

**Fichier :** `/home/abel/.config/lawim/.env.production`
**Référencé par :** `deployment/compose/docker-compose.prod.yml` (via `env_file`)
**Hors dépôt :** OUI

## Variables conservées

Toutes les variables lues par `AppConfig.from_env()` dans `code/lawim_v2/config.py` sont conservées. La liste complète figure dans `lawim_runtime/production/validate_env.py`.

Les principales catégories :

| Catégorie | Variables clés |
|-----------|---------------|
| Base de données | `LAWIM_DB_DRIVER`, `LAWIM_DATABASE_URL`, `POSTGRES_*` |
| Runtime | `LAWIM_HOST`, `LAWIM_PORT`, `APP_ENV`, `LOG_LEVEL`, `PUBLIC_BASE_URL` |
| IA/LLM | `OPENAI_API_KEY`, `DEEPSEEK_API_KEY`, `GEMINI_PRIMARY_API_KEY`, `GEMINI_SECONDARY_API_KEY` |
| WhatsApp | `GREEN_API_ID_INSTANCE`, `GREEN_API_TOKEN_INSTANCE`, `GREEN_API_WEBHOOK_SECRET` |
| Telegram | `TELEGRAM_BOT_TOKEN`, `TELEGRAM_WEBHOOK_SECRET` |
| Campay | `LAWIM_CAMPAY_APP_USERNAME`, `LAWIM_CAMPAY_APP_PASSWORD`, `LAWIM_CAMPAY_WEBHOOK_SECRET` |
| Feature flags | `LROS_AI_*`, `LROS_INTERACTION_*`, `LROS_WHATSAPP_*`, `LROS_TELEGRAM_*` |
| Monitoring | `LAWIM_METRICS_ENABLED` |

## Variables supprimées (obsolètes ou renommées)

| Variable | Fichier(s) source(s) | Raison |
|----------|---------------------|--------|
| `CAMPAY_API_KEY` | `deployment/compose/docker-compose.staging.yml`, `code/lawim_v2/backup/recovery.py` | L'API Campay utilise désormais `LAWIM_CAMPAY_APP_USERNAME` + `LAWIM_CAMPAY_APP_PASSWORD` |
| `CAMPAY_API_SECRET` | `deployment/.env.production` | Même raison, nomenclature obsolète |
| `DB_PASSWORD` | `deployment/compose/docker-compose.staging.yml` | Remplacé par `POSTGRES_PASSWORD` |
| `JWT_SECRET` | `deployment/compose/docker-compose.staging.yml`, `deployment/compose/docker-compose.dev.yml`, `code/lawim_v2/backup/recovery.py` | LAWIM V2 utilisait JWT, V3 n'utilise plus cette variable (le warning `LAWIM_VAULT_KEY not set` est un placeholder) |
| `REDIS_PASSWORD` | `deployment/compose/docker-compose.staging.yml` | Remplacé par la configuration Redis interne |
| `GOOGLE_API_KEY` | `deployment/.env.production` | Non utilisé par le runtime V3 |
| `SMTP_*` | `deployment/.env.production`, `code/lawim_v2/backup/recovery.py` | Service email non activé dans V3 |

## Fichiers conservés (justification)

| Fichier | Justification |
|---------|---------------|
| `deployment/compose/docker-compose.staging.yml` | Environnement staging distinct, utilise sa propre nomenclature |
| `deployment/compose/docker-compose.dev.yml` | Développement local |
| `deployment/secrets/production.env` | Template de référence (de 81 octets) |
| `deployment/secrets/staging.env` | Template de référence |
| `.env.local` | Configuration développement local |
| `deployment/.env.example` | Template exhaustif pour nouveaux déploiements |

## Fichiers supprimés

Aucun fichier supprimé. Les anciens templates `.env` dispersés sont conservés comme documentation historique. La source de vérité unique est `/home/abel/.config/lawim/.env.production`.

## Procédure pour ajouter une nouvelle variable

1. Ajouter la variable à `AppConfig.from_env()` dans `code/lawim_v2/config.py`
2. Ajouter le nom à `ALL_VARS` dans `lawim_runtime/production/validate_env.py`
3. Ajouter au template dans `/home/abel/.config/lawim/.env.production`
4. Documenter dans le manuel de déploiement
