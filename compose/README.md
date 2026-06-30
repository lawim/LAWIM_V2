# Compose (racine `compose/`)

Overlays Compose pour LAWIM_V2 Release Candidate.

## Commandes utiles

Validation configuration :

```bash
docker compose -f compose/docker-compose.base.yml -f compose/docker-compose.dev.yml config
docker compose -f compose/docker-compose.base.yml -f compose/docker-compose.postgres.yml config
```

Démarrage (via scripts) :

```bash
./scripts/run-compose-dev.sh
./scripts/run-compose-postgres.sh   # PostgreSQL optionnel, fallback SQLite activé
```

Arrêt :

```bash
docker compose -f compose/docker-compose.base.yml -f compose/docker-compose.dev.yml down
```

## Profils

| Fichier | Rôle |
|---------|------|
| `docker-compose.base.yml` | Service app, réseaux, volumes, healthcheck |
| `docker-compose.dev.yml` | Montage code local, log debug |
| `docker-compose.postgres.yml` | PostgreSQL optionnel (non obligatoire) |

Miroir de compatibilité : `docker/compose/` contient des symlinks vers `compose/` (source de vérité unique).

## Secrets

Les mots de passe PostgreSQL par défaut (`lawim`) sont des placeholders locaux. Injecter des valeurs réelles via variables d'environnement ; ne jamais committer de secrets.
