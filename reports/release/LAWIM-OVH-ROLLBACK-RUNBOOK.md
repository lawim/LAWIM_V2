# LAWIM — Runbook de Rollback OVH

**Version :** 2.0.0-rc.1
**Date :** 2026-07-21

## Déclencheurs de rollback immédiat

- `/healthz` ne répond pas 200 après déploiement (timeout > 30s)
- `/readyz` ne répond pas 200 après déploiement (timeout > 30s)
- Un ou plusieurs conteneurs en état `restarting` ou `exited` après 3 tentatives
- Migration base de données échoue avec perte de données
- Erreur P0 détectée (aucune réponse utilisateur, fuite de secret, données corrompues)
- Aucune réponse WhatsApp/Telegram après déploiement (confirmé par test réel)

## Responsable

Le développeur ou l'opérateur ayant effectué le déploiement. Aucune autorisation supplémentaire nécessaire pour un rollback.

## Durée estimée

10–15 minutes

## Procédure

### 1. Stopper les nouveaux services

```bash
cd /opt/lawim

# Stopper la nouvelle stack
docker compose -f compose/docker-compose.base.yml -f compose/docker-compose.postgres.yml -f compose/docker-compose.prod.yml down

# OU
docker compose -f deployment/compose/docker-compose.prod.yml down
```

### 2. Conserver les logs pour investigation

```bash
docker compose logs --tail=200 app > /opt/lawim/rollback-logs-$(date +%Y%m%d_%H%M%S).log
```

### 3. Restaurer l'image précédente

```bash
# Option A: Revenir à l'image taguée précédente
docker tag lawim_v2/app:previous lawim_v2/app:latest

# Option B: Utiliser le rollback cible identifié dans RELEASE_MANIFEST.json
# rollback_target: 70eb8498
git checkout 70eb8498
docker compose build app
```

### 4. Restaurer la base de données

```bash
# Identifier la dernière sauvegarde pré-déploiement
LATEST_BACKUP=$(ls -t /opt/lawim/backups/pre-deploy-*.sql | head -1)
echo "Restauration de: $LATEST_BACKUP"

# Vérifier le checksum
sha256sum -c "${LATEST_BACKUP}.sha256"

# Restaurer
gunzip -c "$LATEST_BACKUP" | docker exec -i lawim-postgres-prod psql -U lawim lawim
```

### 5. Redémarrer les services précédents

```bash
# Démarrer la version précédente
docker compose -f compose/docker-compose.base.yml -f compose/docker-compose.postgres.yml -f compose/docker-compose.prod.yml up -d
```

### 6. Vérifier le rétablissement

```bash
# Attendre que les services soient prêts (max 30s)
sleep 10

# Vérifier healthz
curl -f http://localhost:8000/healthz || {
    echo "healthz échoué, nouvelle tentative dans 10s..."
    sleep 10
    curl -f http://localhost:8000/healthz
}

# Vérifier readyz
curl -f http://localhost:8000/readyz

# Vérifier l'état des conteneurs
docker ps --format "table {{.Names}}\t{{.Status}}"
```

### 7. Vérifier le trafic

```bash
# Tester un appel API simple
curl -s http://localhost:8000/api/health

# Vérifier les logs pour s'assurer que le trafic est traité
docker compose logs --tail=20 app
```

### 8. Actions post-rollback

- [ ] Documenter la cause du rollback dans `/opt/lawim/rollback-log.txt`
- [ ] Conserver les logs du rollback (inclure dans le rapport d'incident)
- [ ] Conserver les checksums de la base restaurée
- [ ] Analyser la cause racine avant toute nouvelle tentative de déploiement
- [ ] Mettre à jour le runbook si la procédure doit être modifiée

## Check-list de confirmation

- [ ] Services précédents démarrés et healthy
- [ ] Base de données restaurée avec intégrité vérifiée
- [ ] healthz retourne 200
- [ ] readyz retourne 200
- [ ] Trafic utilisateur rétabli
- [ ] Logs sauvés pour analyse
- [ ] Cause racine identifiée et documentée

## Prévention de récurrence

Avant de tenter un nouveau déploiement :
1. Analyser la cause racine du rollback
2. Corriger le défaut
3. Ajouter un test reproduisant le défaut
4. Valider le correctif sur l'environnement local
5. Re-exécuter le runbook de déploiement
