# LAWIM — Post-Deployment Smoke Test Plan

**Version :** 2.0.0-rc.1
**Date :** 2026-07-21
**Durée estimée :** 10–15 minutes

## Prérequis

- Déploiement OVH terminé (services démarrés)
- Connexion SSH au serveur OVH
- Accès à l'URL publique (api.lawim.app ou localhost)

## 1. Health Check (Liveness)

```bash
# Vérifier que l'API répond
curl -f http://localhost:8000/healthz
# Attendu: HTTP 200

# Vérifier la réponse JSON
curl -s http://localhost:8000/healthz | python3 -m json.tool
# Attendu: {"status": "ok", "version": "2.0.0-rc.1", ...}
```

## 2. Readiness Check

```bash
# Vérifier que tous les services dépendants sont prêts
curl -f http://localhost:8000/readyz
# Attendu: HTTP 200

# Vérifier les dépendances
curl -s http://localhost:8000/readyz | python3 -m json.tool
# Attendu: postgres=ok, redis=ok, db_migrations=ok
```

## 3. API Health

```bash
# Endpoint API principal
curl -f http://localhost:8000/api/health
# Attendu: HTTP 200
```

## 4. Base de données PostgreSQL

```bash
# Vérifier que PostgreSQL est accessible via l'API
curl -s http://localhost:8000/api/health | python3 -c "import sys,json; d=json.load(sys.stdin); print('DB OK' if d.get('database','')=='ok' else 'DB FAIL')"
# Attendu: DB OK

# Vérifier directement (si accès)
docker exec lawim-postgres-prod pg_isready -U lawim -d lawim
# Attendu: accepting connections
```

## 5. Redis

```bash
# Vérifier que Redis est accessible
docker exec lawim-redis-prod redis-cli -a "${REDIS_PASSWORD}" ping
# Attendu: PONG

# Vérifier via l'API
curl -s http://localhost:8000/api/health | python3 -c "import sys,json; d=json.load(sys.stdin); print('Redis OK' if d.get('cache','')=='ok' else 'Redis FAIL')"
# Attendu: Redis OK
```

## 6. Authentification

```bash
# Vérifier que le endpoint d'auth répond
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/v2/auth/login
# Attendu: 405 (Method Not Allowed) ou 400 (Bad Request) — le endpoint existe

# Vérifier que le endpoint n'est pas 404
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/v2/auth/login | grep -v 404
# Attendu: Pas de 404
```

## 7. Conversation — Web QA (sans AI provider)

```bash
# Tester le endpoint conversation avec un message simple (sans auth)
curl -s -X POST http://localhost:8000/api/v2/conversation \
  -H "Content-Type: application/json" \
  -d '{"message": "Bonjour", "channel": "web"}' \
  | python3 -m json.tool
# Attendu: Réponse avec contenu, pas d'erreur 500
```

## 8. Provider Fallback — Moteur Interne

```bash
# Vérifier que le fallback interne est disponible
curl -s http://localhost:8000/api/v2/conversation/health | python3 -m json.tool
# Attendu: internal_fallback=available

# Simuler un cas où le provider AI est indisponible (si endpoint de test existe)
# Sinon, vérifier les logs:
docker compose logs --tail=20 app | grep -i "internal\|fallback"
# Attendu: Pas d'erreur fatale
```

## 9. Moteur Interne (InternalReasoningEngine)

```bash
# Vérifier que le moteur interne répond pour chaque intention
for intent in rental_search sale_search general_inquiry greeting farewell; do
  echo "Testing intent: $intent"
  curl -s -X POST http://localhost:8000/api/v2/conversation/health \
    -H "Content-Type: application/json" \
    -d "{\"intent\": \"$intent\"}" | python3 -m json.tool
done
# Attendu: Chaque intention retourne une réponse
```

## 10. Conteneurs Docker

```bash
# Vérifier l'état de tous les conteneurs
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Vérifier qu'aucun conteneur n'est en état d'erreur
docker ps --filter "status=exited" --filter "status=dead"
# Attendu: Aucun résultat

# Vérifier les redémarrages
docker ps --format "{{.Names}} {{.RestartCount}}" | awk '$2 > 3 {print $1 " a redémarré " $2 " fois"}'
# Attendu: Aucun conteneur avec >3 redémarrages
```

## 11. Logs — Vérification des erreurs

```bash
# Vérifier les dernières lignes de log de l'application
docker compose logs --tail=50 app 2>&1 | grep -i "error\|critical\|exception\|traceback" | head -10
# Attendu: Aucune erreur P0/P1

# Vérifier les logs PostgreSQL
docker compose logs --tail=20 postgres 2>&1 | grep -i "error\|fatal" | head -5
# Attendu: Aucune erreur fatale
```

## 12. Nginx

```bash
# Vérifier que Nginx répond
curl -f http://localhost:80/healthz
# Attendu: HTTP 200 (ou redirection 301 vers HTTPS)

# Vérifier HTTPS si configuré
curl -f https://api.lawim.app/healthz -k 2>/dev/null || echo "HTTPS non testé (certificat peut-être auto-signé)"
```

## Résumé des résultats

| # | Test | Statut | Notes |
|---|------|--------|-------|
| 1 | Health check | ⬜ | |
| 2 | Readiness check | ⬜ | |
| 3 | API health | ⬜ | |
| 4 | PostgreSQL | ⬜ | |
| 5 | Redis | ⬜ | |
| 6 | Authentication | ⬜ | |
| 7 | Conversation Web | ⬜ | |
| 8 | Provider fallback | ⬜ | |
| 9 | Internal engine | ⬜ | |
| 10 | Conteneurs | ⬜ | |
| 11 | Logs | ⬜ | |
| 12 | Nginx | ⬜ | |

## Décision

- [ ] **GO** — Tous les tests passent
- [ ] **ROLLBACK** — Un ou plusieurs tests critiques échouent
