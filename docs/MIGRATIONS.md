# LAWIM_V2 — Stratégie de migrations

## Source de vérité

| Couche | Fichier | Rôle |
|--------|---------|------|
| Manifest logique | `code/lawim_v2/persistence.py` | Tables, version, fingerprint |
| DDL SQLite | `code/lawim_v2/schema_ddl.py` → `SQLITE_INIT_SCRIPT` | Init runtime SQLite |
| DDL PostgreSQL | `code/lawim_v2/schema_ddl.py` → `POSTGRESQL_INIT_STATEMENTS` | Init runtime PG |
| Migrations SQLite legacy | `code/lawim_v2/schema_migrations.py` | Upgrades idempotents v1→v5 |
| Prisma | `prisma/schema.prisma` + `prisma/migrations/` | Production PostgreSQL |

Validation : `python3 scripts/validate_prisma_manifest.py`

Régénération migration Prisma : `python3 scripts/sync_prisma_migration.py`

## SQLite (développement / fallback)

1. `LawimRepository.initialize()` exécute `SQLITE_INIT_SCRIPT`
2. `apply_sqlite_legacy_migrations()` applique les upgrades idempotents pour bases anciennes
3. Aucun outil externe requis

## PostgreSQL (production recommandée)

### Nouvelle installation

- **Option A (runtime)** : le repository Python exécute `POSTGRESQL_INIT_STATEMENTS` au démarrage (comportement actuel)
- **Option B (production)** : `prisma migrate deploy` avec les migrations versionnées

### Mises à jour incrémentales

1. Modifier `persistence.py` manifest + `schema_ddl.py`
2. Générer migration : `python3 scripts/sync_prisma_migration.py`
3. Valider : `python3 scripts/validate_prisma_manifest.py`
4. Déployer : `prisma migrate deploy` (CI/CD ou opérateur)
5. Ajouter des steps legacy SQLite dans `schema_migrations.py` si nécessaire

## Version courante

- **Schema version :** 5
- **Outil production :** Prisma (`schema_migrations.PRODUCTION_MIGRATION_TOOL`)

## Compatibilité

- SQLite reste le moteur par défaut
- PostgreSQL reste optionnel (`LAWIM_DB_DRIVER=postgresql`)
- Le runtime actuel n'est pas modifié : init + legacy migrations conservés
