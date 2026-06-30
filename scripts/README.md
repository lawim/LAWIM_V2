# Scripts opérationnels

Scripts idempotents pour la Release Candidate LAWIM_V2. Aucun secret embarqué.

| Script | Usage |
|--------|-------|
| `run-local.sh` | Démarrage local Python (SQLite par défaut) |
| `run-tests.sh` | Suite unitaire + smoke runtime |
| `run-compose-dev.sh` | Stack Compose development |
| `run-compose-postgres.sh` | Stack dev + PostgreSQL optionnel |
| `smoke_runtime.py` | Smoke test : serveur, health, UI, API, arrêt propre |
| `validate_prisma_manifest.py` | Validation manifeste schéma |

## Codes de retour

- `0` : succès
- `1` : échec (tests, smoke, ou erreur compose)

## Documentation

Voir `docs/OPERATIONS-RC.md` pour le guide d'exploitation minimal.
