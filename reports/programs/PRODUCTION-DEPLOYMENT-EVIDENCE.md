# LAWIM Production Deployment Evidence

**Date:** 2026-07-23
**Status:** TEMPLATE — Aucune exécution réelle

Ce document est un gabarit. Les champs marqués `[TBD]` ou `[compute at deploy time]` doivent être renseignés lors d'un déploiement réel sur infrastructure cible.

## Prérequis non satisfaits

Pour compléter ce document, les éléments suivants sont requis :

- Infrastructure cible (VM, Kubernetes, ou serveur bare-metal)
- Nom de domaine et certificat TLS
- Credentials Green API (WhatsApp)
- Token Telegram Bot
- Credentials Campay Sandbox
- Credentials fournisseur LLM (OpenAI / Anthropic / DeepSeek / Gemini)
- Accès PostgreSQL et Redis

## Journal de déploiement

```bash
# À exécuter sur l'infrastructure cible
LAWIM_VERSION=a337eda0
bash deployment/scripts/deploy.sh
# Log généré dans deployment/journal/deploy-YYYYMMDD-HHMMSS.log
```

## Empreintes des images

```text
lawim/app        [TAG]    python:3.12-slim    [BUILD DATE]
postgres:16-alpine        postgres:16-alpine  [PULL DATE]
redis:7-alpine            redis:7-alpine      [PULL DATE]
prom/prometheus:latest    prometheus          [PULL DATE]
grafana/grafana:latest    grafana             [PULL DATE]
nginx:alpine              nginx               [PULL DATE]
```

## Checksums de configuration

```text
deployment/compose/docker-compose.prod.yml   SHA256: [compute at deploy time]
deployment/secrets/production.env            SHA256: [compute at deploy time]
deployment/nginx/nginx.conf                  SHA256: [compute at deploy time]
```

## Journal des migrations

```text
# À exécuter
python3 -m lawim_runtime.production.migrate
# Attendu :
# Migration 001_initial_sessions: applied
# Migration 002_initial_profiles: applied
# Migration 003_initial_deliveries: applied
# Migration 004_initial_events: applied
```

## Health Check

```text
GET /health
Attendu : 200 OK
{
  "status": "ok",
  "version": "1.0.0",
  "uptime_seconds": [VALUE],
  "checks": {
    "database": "ok",
    "redis": "ok"
  }
}
```

## TLS

```text
Certificate: [TBD — Let's Encrypt ou CA existant]
Expiry: [TBD]
Issuer: [TBD]
Subject: [TBD]
```

## Tests réels

Aucun test réel n'a été exécuté. Voir PROGRAM-G5-REPORT.md pour la matrice complète IMPLEMENTED / TESTED L4 / VALIDATED L6 / CERTIFIED.
