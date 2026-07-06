# Rapport de correction PostgreSQL LAWIM_V2

## Objectif
Corriger les derniers chemins SQL SQLite-spécifiques qui pouvaient casser l'exécution sur PostgreSQL tout en conservant la logique métier et les secrets inchangés.

## Correctifs appliqués
- Adaptation du connecteur PostgreSQL dans [code/lawim_v2/postgresql_repository.py](code/lawim_v2/postgresql_repository.py) pour traduire :
  - `IFNULL(...)` -> `COALESCE(...)`
  - `strftime(...)` -> `to_char(...)`
  - `datetime('now', ...)` -> `CURRENT_TIMESTAMP - INTERVAL ...`
  - `julianday(...)` -> `EXTRACT(EPOCH FROM ...)`
  - `AUTOINCREMENT` -> identité PostgreSQL compatible
- Ajout d'un test de régression dans [tests/test_postgresql_repository_sql.py](tests/test_postgresql_repository_sql.py).

## Vérification
- `./.venv-platform/bin/python -m unittest tests.test_postgresql_repository_sql`
- `./.venv-platform/bin/python -m unittest discover -q tests -p 'test_postgresql*.py'`
- `cd frontend && npm test`

## Résultat
Les tests PostgreSQL ciblés et la suite frontend sont passés. Les validations de déploiement production restent conditionnées par la disponibilité réelle de l'environnement OVH et des secrets associés.
