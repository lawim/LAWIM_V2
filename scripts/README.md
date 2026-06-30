# Scripts opérationnels

Scripts idempotents pour la Release Candidate LAWIM_V2. Aucun secret embarqué.

| Script | Usage |
|--------|-------|
| `install.sh` | Bootstrap machine vierge (dirs, `.env.local`, checks) |
| `validate-install.sh` | Gate reproductibilité : compile, tests, schema, smoke, compose |
| `run-local.sh` | Démarrage local Python (SQLite par défaut) |
| `run-tests.sh` | Suite unitaire + validate_prisma + smoke |
| `run-compose-dev.sh` | Stack Compose development |
| `run-compose-postgres.sh` | Stack dev + PostgreSQL optionnel |
| `run-compose-staging.sh` | Stack staging |
| `run-compose-prod.sh` | Stack production (seed demo off par défaut) |
| `smoke_runtime.py` | Smoke test : serveur, health, UI, API, arrêt propre |
| `validate_prisma_manifest.py` | Validation manifeste schéma + migration SQL |

## Codes de retour

- `0` : succès
- `1` : échec (tests, smoke, ou erreur compose)

## Documentation

Voir `docs/OPERATIONS-RC.md` pour le guide d'exploitation minimal.
