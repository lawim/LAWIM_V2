# LAWIM_V2 — Exploitation Release Candidate

Guide minimal pour lancer et valider LAWIM_V2 en local.

## Prérequis

- Python 3.12+
- `docker compose` (optionnel, pour conteneurs)

## Installation (machine vierge)

```bash
./scripts/install.sh
./scripts/validate-install.sh
```

Voir aussi [README.md](../README.md) à la racine du dépôt.

## Lancer localement (SQLite)

```bash
./scripts/run-local.sh
```

Variables utiles (optionnelles) :

| Variable | Défaut | Description |
|----------|--------|-------------|
| `LAWIM_HOST` | `127.0.0.1` | Interface d'écoute |
| `LAWIM_PORT` | `3000` | Port HTTP |
| `LAWIM_DB_PATH` | `data/runtime/lawim.sqlite3` | Base SQLite |
| `LAWIM_SEED_DEMO_DATA` | `true` | Données de démo au démarrage |
| `LAWIM_MAX_JSON_BODY_BYTES` | `1048576` | Limite corps JSON |
| `LAWIM_MAX_UPLOAD_BYTES` | `5242880` | Limite upload média |

UI : `http://127.0.0.1:3000` · Health : `http://127.0.0.1:3000/api/health`

## Lancer les tests

```bash
./scripts/run-tests.sh
```

Inclut la suite unitaire (`python3 -m unittest discover -s tests -v`) et le smoke test runtime.

Smoke test seul :

```bash
python3 scripts/smoke_runtime.py
```

## Lancer avec Compose (dev)

SQLite par défaut, code monté en volume :

```bash
./scripts/run-compose-dev.sh
```

Arrêt :

```bash
docker compose -f compose/docker-compose.base.yml -f compose/docker-compose.dev.yml down
```

## Activer PostgreSQL (optionnel)

PostgreSQL n'est **pas** obligatoire. SQLite reste le fallback via `LAWIM_DB_FALLBACK=true`.

```bash
./scripts/run-compose-postgres.sh
```

Variables optionnelles :

| Variable | Défaut |
|----------|--------|
| `LAWIM_DB_DRIVER` | `postgresql` |
| `LAWIM_DATABASE_URL` | `postgresql://lawim:lawim@postgres:5432/lawim_v2` |
| `LAWIM_DB_FALLBACK` | `true` |
| `LAWIM_POSTGRES_USER` | `lawim` |
| `LAWIM_POSTGRES_PASSWORD` | `lawim` |

Aucun secret réel ne doit être commité. Adapter les mots de passe via l'environnement local.

## Contrôles release candidate

```bash
python3 -m compileall lawim_v2 code/lawim_v2 tests/test_lawim_v2.py
python3 -m unittest discover -s tests -v
python3 scripts/smoke_runtime.py
python3 scripts/validate_prisma_manifest.py
docker compose -f compose/docker-compose.base.yml -f compose/docker-compose.dev.yml config
```

## Comptes démo

Mot de passe par défaut : `lawim-demo`

- `admin@lawim.local`
- `agent@lawim.local`
- `owner@lawim.local`
