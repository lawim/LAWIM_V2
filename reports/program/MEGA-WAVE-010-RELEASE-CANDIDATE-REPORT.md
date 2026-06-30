# MEGA WAVE 010 — Release Candidate Readiness

## Résumé exécutif

MEGA WAVE 010 transforme le MVP stabilisé en Release Candidate locale exploitable : commandes de lancement, smoke test runtime, configuration validée, Compose renforcé, contrôle sécurité final et documentation minimale. **55 tests** passent.

## 1. Commandes de lancement

| Commande | Rôle |
|----------|------|
| `./scripts/run-local.sh` | Démarrage Python local (SQLite) |
| `./scripts/run-tests.sh` | Suite unitaire + smoke runtime |
| `./scripts/run-compose-dev.sh` | Compose development |
| `./scripts/run-compose-postgres.sh` | Compose + PostgreSQL optionnel |

## 2. Smoke test runtime (PASS)

`scripts/smoke_runtime.py` :

1. Démarre le serveur sur port libre (thread)
2. `GET /api/health` (+ headers sécurité)
3. `GET /` et `GET /app.js` (UI statique)
4. `GET /api/properties?limit=1` (API publique)
5. `GET /api/me` → 401 + `WWW-Authenticate`
6. Arrêt propre (`shutdown`, `server_close`, fermeture repo)

Intégré dans `tests/test_runtime_smoke.py` et `run-tests.sh`.

## 3. Configuration renforcée

- `AppConfig.validate()` : port, driver DB, TTL session, limites payload, `match_min_score`, `APP_ENV`
- `_float_env()` pour erreurs lisibles sur variables numériques
- Validation au démarrage (`main`) et à `create_server()`
- `env/development/.env.example` enrichi (variables `LAWIM_*`, PostgreSQL commenté)

## 4. Docker / Compose (PASS)

- Healthcheck HTTP sur service `app` (base compose racine + `docker/compose/`)
- Variables runtime documentées dans overlays (`LAWIM_DB_DRIVER`, limites, metrics)
- `compose/README.md` : commandes validate / up / down
- PostgreSQL reste **optionnel** ; `LAWIM_DB_FALLBACK=true` par défaut

## 5. Contrôle sécurité final (PASS)

`tests/test_release_candidate.py` :

- Endpoints privés : `/api/me`, `/api/notifications`, `/api/conversations`, `/api/events` → 401
- Headers : API, static, média (`/media/*`)
- Payload oversized → 413
- Validation configs Compose (4 paires)

## 6. Documentation exploitation

- `docs/OPERATIONS-RC.md` — lancer local, tests, compose, PostgreSQL optionnel
- `scripts/README.md` — index scripts et codes retour

## Fichiers livrés

- `scripts/run-local.sh`, `run-tests.sh`, `run-compose-dev.sh`, `run-compose-postgres.sh`, `smoke_runtime.py`
- `code/lawim_v2/config.py`, `server.py`
- `compose/docker-compose.base.yml`, `docker/compose/docker-compose.base.yml`
- `compose/README.md`, `docs/OPERATIONS-RC.md`, `env/development/.env.example`
- `tests/test_runtime_smoke.py`, `tests/test_release_candidate.py`

## Contrôles obligatoires

- `python3 -m compileall` — OK
- `python3 -m unittest discover -s tests -v` — **55 tests OK**
- `python3 -m lawim_v2 --help` — OK
- `python3 scripts/validate_prisma_manifest.py` — OK
- `git diff --check` — OK
- Docker compose configs (4 variantes) — OK
- `python3 scripts/smoke_runtime.py` — OK

## Limites

- Smoke test en processus local (pas de test Compose up complet en CI).
- PostgreSQL live non exercé automatiquement (fallback SQLite validé).
- Pas de déploiement production dans cette vague.

## Prochaine étape

**RELEASE_FINALIZATION** : tag release, checklist go-live, validation staging.

```yaml
wave: MEGA_WAVE_010
status: READY_FOR_DG_REVIEW
release_candidate: PREPARED
runtime_smoke: PASS
tests: PASS
compose: PASS
security: PASS
blocking_risk: false
next_wave: RELEASE_FINALIZATION
decision_required: true
```
