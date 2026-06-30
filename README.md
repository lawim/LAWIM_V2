# LAWIM_V2

Monolithe Python 3.12 pour la gestion immobilière : listings, matching, conversations et notifications.

## Prérequis

- Python **3.12+**
- `docker compose` (optionnel)
- Node.js (optionnel — vérification syntaxe `app.js`)

## Installation (machine vierge)

```bash
git clone <repo-url> lawim_v2 && cd lawim_v2
./scripts/install.sh
./scripts/validate-install.sh
```

Variables utiles à l'installation :

| Variable | Effet |
|----------|--------|
| `LAWIM_INSTALL_POSTGRES_DRIVER=1` | installe `pg8000` via pip |

Un fichier `.env.local` est créé depuis `env/development/.env.example` s'il n'existe pas.

## Démarrage rapide

```bash
./scripts/run-local.sh          # SQLite, http://127.0.0.1:3000
./scripts/run-tests.sh          # tests + validate_prisma + smoke
./scripts/run-compose-dev.sh    # Docker (SQLite)
./scripts/run-compose-postgres.sh  # Docker + PostgreSQL optionnel
```

Comptes démo (mot de passe `lawim-demo`) : `admin@lawim.local`, `agent@lawim.local`, `owner@lawim.local`.

## Documentation

| Document | Contenu |
|----------|---------|
| [docs/OPERATIONS-RC.md](docs/OPERATIONS-RC.md) | Guide d'exploitation release candidate |
| [compose/README.md](compose/README.md) | Stacks Docker Compose (source de vérité) |
| [tests/README.md](tests/README.md) | Suite de tests |
| [reports/program/FULL-ENGINEERING-REVIEW-REPORT.md](reports/program/FULL-ENGINEERING-REVIEW-REPORT.md) | Revue engineering |

## Schéma & persistance

- Source de vérité logique : `code/lawim_v2/persistence.py` (manifest v5)
- DDL PostgreSQL runtime : `code/lawim_v2/schema_ddl.py`
- Prisma : ancre d'alignement (`prisma/schema.prisma` + migration SQL)
- Validation : `python3 scripts/validate_prisma_manifest.py`

## Structure

```
code/lawim_v2/   # application runtime
compose/         # Docker Compose canonique
docker/compose/  # alias include → compose/
scripts/         # install, tests, smoke, compose
tests/           # unittest harness
prisma/          # schéma Prisma aligné
```

## CI

Workflow GitHub Actions : `.github/workflows/ci.yml` (tests, schema, smoke, compose).

Test PostgreSQL optionnel en CI via service container ; localement :

```bash
export LAWIM_TEST_POSTGRES_URL=postgresql://lawim:lawim@localhost:5432/lawim_v2
pip install -r requirements-postgresql.txt
python3 -m unittest tests.test_productization.PostgreSQLIntegrationTest -v
```

## Licence & gouvernance

Bootstrap, Constitution et Gouvernance du programme LAWIM ne sont pas modifiés par les missions produit.
