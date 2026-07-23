# LAWIM V3 — Deployment Manual

**Version:** 1.0
**Date:** 2026-07-23

---

## 1. Prérequis infrastructure

| Composant | Version minimale | Usage |
|-----------|------------------|-------|
| Docker | 24+ | Conteneurisation |
| Docker Compose | 2.20+ | Orchestration |
| PostgreSQL | 16 | Base de données |
| Redis | 7 | Cache / sessions |
| Nginx | 1.24+ | Reverse proxy / TLS |
| Python | 3.12 | Runtime (conteneurisé) |

## 2. Architecture déployée

```
[Internet]
    |
  [Nginx:80/443]   → TLS termination, static files
    |
  [LAWIM App:3000]  → LAWIM V3 application
    |       |
  [Postgres:5432] [Redis:6379]
    |
  [Prometheus:9090] [Grafana:3001]
```

## 3. Déploiement rapide

```bash
# 1. Cloner
git clone git@github-lawim:lawim/LAWIM_V2.git
cd LAWIM_V2

# 2. Créer le fichier de secrets (HORS dépôt)
cp deployment/.env.example /home/abel/.config/lawim/.env.production
# Éditer avec vos clés réelles (voir section 5)

# 3. Lancer
docker compose -f deployment/compose/docker-compose.prod.yml up -d

# 4. Vérifier
curl http://localhost:3000/health
# Attendu: {"status":"ok","version":"1.0.0"}
```

## 4. Scripts de déploiement

| Script | Usage |
|--------|-------|
| `deployment/scripts/deploy.sh` | Déploiement complet avec migrations |
| `deployment/scripts/rollback.sh <version>` | Retour à une version précédente |
| `deployment/scripts/backup.sh` | Backup base + config |
| `deployment/scripts/restore.sh <path>` | Restauration complète |

## 5. Variables d'environnement

**Fichier unique :** `/home/abel/.config/lawim/.env.production` (hors dépôt, chargé automatiquement par `docker-compose.prod.yml`)

### Runtime (obligatoires)

```env
APP_ENV=production
LOG_LEVEL=info
PUBLIC_BASE_URL=https://la-vim.com
LAWIM_HOST=0.0.0.0
LAWIM_PORT=3000
LAWIM_DB_DRIVER=postgresql
LAWIM_DATABASE_URL=postgresql://lawim:password@db:5432/lawim_v3
POSTGRES_USER=lawim
POSTGRES_PASSWORD=...
POSTGRES_DB=lawim_v3
```

### Feature flags (tous `false` par défaut)

```env
LROS_AI_INTELLIGENCE_ENABLED=false
LROS_AI_EXTRACTION_ENABLED=false
LROS_AI_RESPONSE_WRITER_ENABLED=false
LROS_AI_SHADOW_MODE=true
LROS_AI_PROVIDER_CALLS_ENABLED=false
LROS_AI_BUDGET_MONTHLY_CENTS=0
LROS_INTERACTION_GATEWAY_ENABLED=false
LROS_WHATSAPP_ADAPTER_ENABLED=false
LROS_TELEGRAM_ADAPTER_ENABLED=false
```

### Providers LLM (optionnels — décommenter dans le fichier .env)

```env
OPENAI_API_KEY=sk-...
DEEPSEEK_API_KEY=...
GEMINI_PRIMARY_API_KEY=...
GEMINI_SECONDARY_API_KEY=...
```

### WhatsApp / Green API (optionnel)

```env
GREEN_API_ID_INSTANCE=...
GREEN_API_TOKEN_INSTANCE=...
GREEN_API_WEBHOOK_SECRET=...
GREEN_API_PHONE=+237...
```

### Telegram (optionnel)

```env
TELEGRAM_BOT_TOKEN=...
TELEGRAM_WEBHOOK_SECRET=...
```

### Campay (optionnel)

```env
LAWIM_CAMPAY_APP_USERNAME=...
LAWIM_CAMPAY_APP_PASSWORD=...
LAWIM_CAMPAY_WEBHOOK_SECRET=...
LAWIM_CAMPAY_WEBHOOK_URL=...
```

## 6. Validation au démarrage

Le container `app` exécute automatiquement `validate_env.py` au démarrage. Celui-ci vérifie la présence des variables requises et signale les manquantes **sans jamais afficher leurs valeurs**.

```bash
# Vérification manuelle
python3 -m lawim_runtime.production.validate_env
```

## 7. Migrations

```bash
# Appliquer
docker compose exec app python3 -m lawim_runtime.production.migrate

# Rollback
docker compose exec app python3 -m lawim_runtime.production.migrate --rollback
```

## 8. Health checks

| Endpoint | Usage |
|----------|-------|
| `GET /health` | Liveness + readiness |
| `GET /health/ready` | Readiness (base de données, Redis) |
| `GET /health/live` | Liveness (application) |

## 9. Sauvegarde

```bash
# Backup complet
bash deployment/scripts/backup.sh

# Restauration
bash deployment/scripts/restore.sh deployment/backup/lawim-backup-20260723-120000
```

## 10. Monitoring

| Service | Port | Accès |
|---------|------|-------|
| Prometheus | 9090 | Interne |
| Grafana | 3001 | admin:/mot de passe défini dans .env |

## 11. Rollback

```bash
bash deployment/scripts/rollback.sh <previous_git_ref>
```

Le rollback exécute :
1. Arrêt des services
2. Checkout de la version précédente
3. Reconstruction des images
4. Redémarrage
5. Rollback des migrations si nécessaire

## 12. Références

| Document | Emplacement |
|----------|-------------|
| Operations Manual | `reports/release/OPERATIONS-MANUAL.md` |
| Known Limitations | `reports/release/KNOWN-LIMITATIONS.md` |
| Env Audit Report | `reports/programs/ENV-AUDIT-REPORT.md` |
| Env Validation | `lawim_runtime/production/validate_env.py` |
| Secrets template | `/home/abel/.config/lawim/.env.production` |
