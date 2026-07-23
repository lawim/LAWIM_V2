# LAWIM V3 — Operations Manual

**Version:** 1.0
**Date:** 2026-07-23

---

## 1. Architecture du système

```
┌─────────────────────────────────────────────────┐
│                    LAWIM V3                      │
├─────────────────────────────────────────────────┤
│ Interaction Platform  │     AI Intelligence      │
│ (Programme E)         │     (Programme F)        │
├───────────────────────┼─────────────────────────┤
│ Domain Runtime        │     Production           │
│ (Programme D)         │     (Programme G)        │
├───────────────────────┴─────────────────────────┤
│ LROS Kernel (Programmes A, B, C, C.5)           │
└─────────────────────────────────────────────────┘
```

## 2. Flux de traitement d'un message

```
Message entrant
  → Channel Adapter (WhatsApp / Telegram / Web)
  → InteractionEnvelope
  → Interaction Gateway (validation, déduplication)
  → Identity Resolution
  → Session Management
  → Project Resolution
  → Extraction (déterministe ou IA)
  → CandidateUpdate → ProfilePatch
  → ProjectProfile
  → Qualification
  → ProjectBrain / Decision
  → ActionExecutionEngine
  → Domain Runtime (matching, visite, CRM, etc.)
  → Response Plan
  → Response Writer (déterministe ou IA)
  → Delivery Manager
  → Channel Adapter (réponse)
```

## 3. Supervision quotidienne

### Matin

```bash
# 1. Vérifier l'état des services
docker compose ps
curl http://localhost:3000/health

# 2. Vérifier les logs d'erreur
docker compose logs --tail=50 app | grep -i "error\|exception\|traceback"

# 3. Vérifier les métriques Prometheus
curl http://localhost:9090/api/v1/query?query=up

# 4. Vérifier les backups récents
ls -la deployment/backup/
```

### Hebdomadaire

```bash
# 1. Test de backup
bash deployment/scripts/backup.sh

# 2. Vérifier l'espace disque
df -h

# 3. Vérifier les logs de latence
docker compose logs --tail=200 app | grep "latency_ms"
```

## 4. Gestion des incidents

### Incident : application lente

1. Vérifier `GET /health` — statut ?
2. Vérifier CPU/RAM : `docker stats`
3. Vérifier PostgreSQL : `docker exec lawim-db psql -c "SELECT count(*) FROM pg_stat_activity;"`
4. Vérifier Redis : `docker exec lawim-redis redis-cli ping`
5. Vérifier les logs de latence

### Incident : provider IA indisponible

Le système tombe automatiquement en mode déterministe :

- Circuit breaker s'ouvre après 5 échecs consécutifs
- `DeterministicResponseWriter` prend le relais
- Les métriques `ai_fallback_total` s'incrémentent
- Vérifier : `docker compose logs app | grep "circuit breaker"`

### Incident : base de données inaccessible

1. Vérifier PostgreSQL : `docker compose logs db`
2. Si PostgreSQL est down :
   ```bash
   docker compose restart db
   # Vérifier la récupération
   docker compose logs db | tail -20
   ```
3. Si persistant, restaurer depuis le dernier backup :
   ```bash
   bash deployment/scripts/restore.sh deployment/backup/backup-le-plus-recent
   ```

### Incident : perte d'un webhook

Le système utilise la déduplication par `external_message_id`. Si un webhook est perdu :

1. Vérifier les logs Green API / Telegram
2. Vérifier les logs LAWIM pour le `correlation_id`
3. Le webhook peut être renvoyé manuellement depuis le tableau de bord du fournisseur

## 5. Maintenance planifiée

### Mise à jour

```bash
git pull
docker compose -f deployment/compose/docker-compose.prod.yml build
docker compose -f deployment/compose/docker-compose.prod.yml up -d
python3 -m lawim_runtime.production.migrate
```

### Rotation des secrets

Les secrets sont dans `.env` (hors dépôt). Rotation recommandée :

- Clés API LLM : tous les 90 jours
- Tokens WhatsApp/Telegram : tous les 180 jours
- Mot de passe PostgreSQL : tous les 90 jours
- Mot de passe Grafana : tous les 30 jours

## 6. Sauvegarde et restauration

### Backup automatique (cron)

```cron
# Tous les jours à 2h du matin
0 2 * * * cd /opt/lawim && bash deployment/scripts/backup.sh

# Toutes les semaines, copie vers un stockage distant
0 3 * * 0 rsync -avz deployment/backup/ user@backup-server:/backups/lawim/
```

### Vérification d'intégrité

```bash
cd deployment/backup/backup-le-plus-recent
sha256sum -c MANIFEST.txt
```

## 7. Coûts opérationnels estimés

| Poste | Estimation mensuelle |
|-------|---------------------|
| Serveur (4 vCPU, 8 GB RAM) | ~40-80 € |
| PostgreSQL (géré ou auto-hébergé) | ~10-30 € |
| Redis (géré ou conteneurisé) | ~5-10 € |
| Domaine + TLS | ~5-15 € |
| OpenAI API (usage modéré) | ~20-100 € |
| Green API WhatsApp | ~10-30 € |
| Total | ~90-265 € |

## 8. Contacts et escalade

| Rôle | Responsabilité |
|------|---------------|
| Administrateur système | Déploiement, infrastructure, backups |
| Opérateur LAWIM | Supervision quotidienne, incidents courants |
| Développeur | Corrections, évolutions, programmes F+ |
| Support utilisateur | Première ligne utilisateur |

## 9. Références

| Document | Emplacement |
|----------|-------------|
| Deployment Manual | `reports/release/DEPLOYMENT-MANUAL.md` |
| Known Limitations | `reports/release/KNOWN-LIMITATIONS.md` |
| Changelog | `reports/release/CHANGELOG-1.0.md` |
| Programmes status | `lawim_program_status.yaml` |
| Architecture | `reports/architecture/` |
