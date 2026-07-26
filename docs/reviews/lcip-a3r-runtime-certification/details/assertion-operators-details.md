# Assertion Operators Details — A.3R

## Opérateurs implémentés

| Opérateur | Fonction | Tests |
|-----------|----------|-------|
| equals | == | + |
| not_equals | != | + |
| contains | item in container | + |
| not_contains | not in container | + |
| subset | dict/list subset | + |
| superset | dict/list superset | + |
| exists | is not None | + |
| not_exists | is None | + |
| count_equals | len() == | + |
| greater_than | > | + |
| less_than | < | + |
| unchanged | == (before/after) | + |
| changed | != (before/after) | + |

## Tests

12 tests unitaires dans `TestAssertionOperators` : 12/12 PASS

## Contrôle

OP-0001 : PASS
