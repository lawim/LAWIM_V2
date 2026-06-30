# Docker Compose (compatibilité)

Ce dossier expose des **alias symlink** vers les fichiers canoniques de `compose/`.

## Source de vérité

Les définitions vivent dans **`compose/`** à la racine. Chaque fichier ici est un lien symbolique :

| Alias (`docker/compose/`) | Cible (`compose/`) |
|---------------------------|---------------------|
| `docker-compose.base.yml` | `docker-compose.base.yml` |
| `docker-compose.development.yml` | `docker-compose.dev.yml` |
| `docker-compose.staging.yml` | `docker-compose.staging.yml` |
| `docker-compose.production.yml` | `docker-compose.prod.yml` |
| `docker-compose.postgres.yml` | `docker-compose.postgres.yml` |

Les chemins relatifs (`context: ..`, volumes) restent valides car Compose résout le chemin réel du fichier cible.

## Validation

```bash
docker compose -f docker/compose/docker-compose.base.yml -f docker/compose/docker-compose.development.yml config
docker compose -f compose/docker-compose.base.yml -f compose/docker-compose.dev.yml config
```

Les scripts opérationnels (`scripts/run-compose-*.sh`) utilisent **`compose/`** directement.

## Régénération des liens

Si un lien est cassé :

```bash
./scripts/sync-compose-aliases.sh
```
