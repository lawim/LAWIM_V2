# LAWIM_V2 — Industrialization Mission 001 Report

- **Date:** 2026-06-29
- **Baseline:** `722795f` (productization-001)
- **Tag:** `industrialization-001`
- **Scope:** persistance unifiée, packaging pip, migrations production, reproductibilité v1.0

---

## 1. Architecture de persistance unifiée

### Modèle en couches

```
persistence.py                    ← manifest logique v5 (fingerprint, tables)
        │
        ├── schema_ddl.py         ← DDL SQLite + PostgreSQL (source physique)
        │     ├── SQLITE_INIT_SCRIPT
        │     └── POSTGRESQL_INIT_STATEMENTS
        │
        ├── schema_migrations.py  ← upgrades SQLite legacy + stratégie prod
        │
        ├── db.py                 ← runtime SQLite (init + seed, sans DDL inline)
        ├── postgresql_repository.py
        └── prisma/schema.prisma + migrations/
```

### Alignement vérifié automatiquement

`validate_manifest_table_alignment()` garantit que les 11 tables du manifest sont présentes dans les deux DDL.

### Extraction réalisée

- **~140 lignes** de DDL SQLite retirées de `db.py` → `schema_ddl.SQLITE_INIT_SCRIPT`
- **~150 lignes** de migrations legacy retirées de `db.py` → `schema_migrations.apply_sqlite_legacy_migrations()`
- Alias `SCHEMA = SQLITE_INIT_SCRIPT` conservé pour compatibilité

---

## 2. Packaging

### Métadonnées (`pyproject.toml`)

| Champ | Valeur |
|-------|--------|
| Nom distribution | `lawim-v2` |
| Version | `0.1.0` |
| Python | `>=3.12` |
| Entry point | `lawim-v2` → `lawim_v2.__main__:main` |
| Extras | `[postgresql]`, `[dev]` → pg8000 |
| Package data | `lawim_v2/static/*` |

### Installation

```bash
pip install -e ".[postgresql]"
python -m lawim_v2 --help
```

### Validation packaging

`scripts/validate-packaging.sh` :
1. Crée un venv éphémère
2. `pip install -e ".[postgresql]"`
3. Vérifie entry point + smoke runtime

Intégré dans `validate-install.sh` et CI.

### Publication (sans exécution)

Stratégie documentée dans [docs/PUBLISHING.md](../docs/PUBLISHING.md) : wheel, sdist, image Docker, pipeline registry privé.

---

## 3. Migrations

### Stratégie (documentée dans [docs/MIGRATIONS.md](../docs/MIGRATIONS.md))

| Environnement | Mécanisme |
|---------------|-----------|
| SQLite dev/fallback | `SQLITE_INIT_SCRIPT` + `apply_sqlite_legacy_migrations()` |
| PostgreSQL runtime | `POSTGRESQL_INIT_STATEMENTS` au init (comportement conservé) |
| PostgreSQL production | **Prisma** `migrate deploy` (recommandé) |

### Outils

| Script | Rôle |
|--------|------|
| `scripts/validate_prisma_manifest.py` | Manifest + DDL SQLite/PG + migration SQL |
| `scripts/sync_prisma_migration.py` | Régénère `prisma/migrations/.../migration.sql` depuis `schema_ddl` |

### Compatibilité runtime

- Bases SQLite existantes : migrations legacy idempotentes conservées
- PostgreSQL non obligatoire
- SQLite non supprimé

---

## 4. Installation

### Parcours machine vierge (inchangé, enrichi)

```bash
./scripts/install.sh
./scripts/validate-install.sh
```

Options :

| Variable | Effet |
|----------|--------|
| `LAWIM_INSTALL_PACKAGE=1` | `pip install -e .` |
| `LAWIM_INSTALL_POSTGRES_DRIVER=1` | installe pg8000 |

### Scripts cohérents

- `install.sh` → `infra/install.sh`
- `validate-install.sh` → tests + schema + smoke + compose + **packaging**
- `run-local.sh`, `run-compose-*.sh` — inchangés, PYTHONPATH dépôt toujours supporté

---

## 5. Reproductibilité

### Contrôles finaux exécutés

| Contrôle | Résultat |
|----------|----------|
| `python3 -m compileall code tests scripts` | OK |
| `python3 -m unittest discover -s tests` | **74 OK, 2 skipped** |
| `validate_prisma_manifest.py` | PASS (manifest + DDL + migration) |
| `smoke_runtime.py` | OK |
| Docker Compose (4 paires) | OK |
| `validate-packaging.sh` | OK |
| `validate-install.sh` | **INSTALL VALIDATION OK** |
| `git diff --check` | OK |

### Tests ajoutés (`tests/test_industrialization.py`)

- Alignement manifest ↔ DDL SQLite/PostgreSQL
- Idempotence migrations legacy
- Stratégie Prisma documentée en code
- Métadonnées pyproject + version package

---

## 6. Dette restante avant version 1.0

| Priorité | Item |
|----------|------|
| Haute | CD pipeline (build wheel, image, push registry) |
| Haute | Migrations Prisma incrémentales v6+ (processus formalisé en CI) |
| Moyenne | Génération SQLite DDL depuis manifest (au lieu de script parallèle) |
| Moyenne | `pip install lawim-v2` sans clone git — registry privé |
| Moyenne | Alembic en alternative Prisma (si stack ops l'exige) |
| Basse | Symlinks Compose sur Windows (fallback copy) |
| Basse | Signature wheels / provenance SLSA |

---

## 7. Recommandation de passage en Release Candidate publique

### Critères remplis

- Installation reproductible depuis le dépôt seul
- Paquet pip installable et testé en venv isolé
- Schéma unifié v5 avec validation automatique tri-moteur
- CI active (tests, compose, PostgreSQL)
- Documentation ops (README, OPERATIONS-RC, MIGRATIONS, PUBLISHING)

### Verdict

**LAWIM_V2 peut passer en Release Candidate publique (RC1)** pour early adopters techniques, sous conditions :

1. **Scope RC1** : monolithe Python, SQLite par défaut, PostgreSQL optionnel
2. **Support** : documenter clairement que la Directive v1.0 cible reste aspirational
3. **Avant GA 1.0** : CD pipeline, migrations incrémentales en prod PG, observabilité export

### Prochaine mission suggérée (INDUSTRIALIZATION-002)

- Pipeline CD + registry
- Bump semver `0.1.0-rc1` → `1.0.0-rc.1`
- OpenAPI / contrat API versionné
- Health/readiness K8s

---

## Fichiers créés / modifiés (extrait)

| Fichier | Action |
|---------|--------|
| `code/lawim_v2/schema_ddl.py` | +SQLITE_INIT_SCRIPT, validation tables |
| `code/lawim_v2/schema_migrations.py` | Créé — legacy + stratégie |
| `code/lawim_v2/db.py` | DDL/migrations extraits |
| `pyproject.toml` | Créé — packaging pip |
| `scripts/validate-packaging.sh` | Créé |
| `scripts/sync_prisma_migration.py` | Créé |
| `docs/MIGRATIONS.md`, `docs/PUBLISHING.md` | Créés |
| `tests/test_industrialization.py` | Créé |

---

*Mission Industrialization 001 — distribution, migrations et unification.*
