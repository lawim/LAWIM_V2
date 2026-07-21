# LAWIM — Runbook de Déploiement OVH

**Version :** 2.0.0-rc.1
**Commit cible :** 1258fe19
**Date :** 2026-07-21
**Responsable :** Développeur ou opérateur désigné

## Prérequis

- [ ] Accès SSH au serveur OVH (vps-6da158cc.vps.ovh.net)
- [ ] Docker et Docker Compose installés sur le serveur
- [ ] Fichier `/opt/lawim/secrets/.env` présent avec tous les secrets (min 20 entrées)
- [ ] Espace disque > 10 Go libre
- [ ] Backup récent de la base existante disponible
- [ ] Git tag `lawim-v2-final-acceptance-candidate-local` créé
- [ ] Checksum SHA256 du manifeste calculé
- [ ] Accès à Git (origin) configuré

## Étapes

### 1. Vérifier les accès et l'environnement

```bash
ssh ubuntu@vps-6da158cc.vps.ovh.net

# Vérifier Docker
docker --version
docker compose version

# Vérifier l'OS
cat /etc/os-release
```

### 2. Vérifier les secrets

```bash
cat /opt/lawim/secrets/.env | grep -v '^#' | grep -v '^$' | wc -l
# Devrait afficher > 20 entrées

# Vérifier que les secrets critiques sont présents
grep -c 'DEEPSEEK_API_KEY' /opt/lawim/secrets/.env
grep -c 'OPENAI_API_KEY' /opt/lawim/secrets/.env
grep -c 'GREEN_API_TOKEN_INSTANCE' /opt/lawim/secrets/.env
grep -c 'TELEGRAM_BOT_TOKEN' /opt/lawim/secrets/.env
grep -c 'DB_PASSWORD' /opt/lawim/secrets/.env
grep -c 'JWT_SECRET' /opt/lawim/secrets/.env
grep -c 'LAWIM_VAULT_KEY' /opt/lawim/secrets/.env
```

### 3. Vérifier l'espace disque

```bash
df -h /
# Doit montrer > 10 Go disponibles
```

### 4. Sauvegarder la base existante

```bash
BACKUP_FILE="/opt/lawim/backups/pre-deploy-$(date +%Y%m%d_%H%M%S).sql"

docker exec lawim-postgres-prod pg_dump -U lawim lawim > "$BACKUP_FILE"

# Vérifier que le fichier n'est pas vide
ls -lh "$BACKUP_FILE"

# Calculer le checksum
sha256sum "$BACKUP_FILE" > "${BACKUP_FILE}.sha256"
```

### 5. Transférer le code source

```bash
cd /opt/lawim

# S'assurer que le répertoire est propre
git status

# Récupérer la dernière version de la branche
git fetch origin

# Basculer sur le commit cible
git checkout 1258fe19

# Vérifier le worktree propre
git status
```

### 6. Configurer les variables d'environnement

```bash
# Copier le fichier .env de production
cp /opt/lawim/secrets/.env /opt/lawim/.env

# Vérifier que APP_ENV=production
grep APP_ENV /opt/lawim/.env
```

### 7. Construire les images Docker

```bash
cd /opt/lawim

# Option A: Déploiement avec compose/ (nouvelle stack)
docker compose -f compose/docker-compose.base.yml -f compose/docker-compose.postgres.yml -f compose/docker-compose.prod.yml build

# Option B: Déploiement avec deployment/compose/ (stack production complète)
docker compose -f deployment/compose/docker-compose.prod.yml build
```

### 8. Appliquer les migrations

```bash
# Avec compose/
docker compose -f compose/docker-compose.base.yml -f compose/docker-compose.postgres.yml run --rm app python scripts/migrate.py

# Avec deployment/compose/
docker compose -f deployment/compose/docker-compose.prod.yml run --rm backend python scripts/migrate.py
```

### 9. Démarrer les services

```bash
# Option A
docker compose -f compose/docker-compose.base.yml -f compose/docker-compose.postgres.yml -f compose/docker-compose.prod.yml up -d

# Option B
docker compose -f deployment/compose/docker-compose.prod.yml up -d
```

### 10. Vérifier l'état des conteneurs

```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Vérifier qu'aucun conteneur n'est en état restart/crash
docker ps --filter "status=exited" --filter "status=dead"
```

### 11. Vérifier healthz

```bash
curl -f http://localhost:8000/healthz
# Doit retourner 200 OK
```

### 12. Vérifier readyz

```bash
curl -f http://localhost:8000/readyz
# Doit retourner 200 OK
```

### 13. Exécuter les smoke tests

```bash
# Vérifier le endpoint API
curl -f http://localhost:8000/api/health

# Vérifier le endpoint conversation
curl -f http://localhost:8000/api/v2/conversation/health

# Vérifier que le moteur interne répond
curl -s http://localhost:8000/api/v2/conversation/health | python3 -m json.tool
```

### 14. Vérifier les logs

```bash
# Vérifier qu'il n'y a pas d'erreur critique
docker compose logs --tail=50 app
```

### 15. Décider maintien ou rollback

| Critère | Vérification | Action si échec |
|---------|-------------|-----------------|
| healthz | `curl -f http://localhost:8000/healthz` | Rollback immédiat |
| readyz | `curl -f http://localhost:8000/readyz` | Rollback immédiat |
| Conteneurs | Tous les conteneurs "healthy" | Rollback |
| Smoke tests | API répond, conversation répond | Rollback si échec |
| Logs | Aucune erreur P0/P1 | Investigation |

### 16. Action finale

**Si tout est OK :**
```bash
echo "DÉPLOIEMENT REUSSI — $(date)" >> /opt/lawim/deployment-log.txt
git tag -a lawim-v2-ovh-deployed-$(date +%Y%m%d) -m "Deployed 1258fe19 to OVH production"
```

**Si rollback nécessaire :**
```bash
# Exécuter immédiatement le runbook de rollback
# Voir LAWIM-OVH-ROLLBACK-RUNBOOK.md
```

## Post-déploiement

- [ ] Exécuter le plan de smoke tests complet (LAWIM-POST-DEPLOYMENT-SMOKE-TEST-PLAN.md)
- [ ] Vérifier les métriques d'observabilité
- [ ] Confirmer la réception des webhooks WhatsApp/Telegram
- [ ] Mettre à jour le statut dans LAWIM_CURRENT_STATE.md
- [ ] Notifier l'équipe
