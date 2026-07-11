# Restore Complete

STATUT : CIBLE DOCUMENTAIRE ACTIVE

## Goal

Reconstruct a full LAWIM instance from backups without depending on the original production server.

## Canonical steps

1. provision a new server
2. install the required dependencies
3. retrieve the code at the validated commit
4. restore secrets from the approved secret source
5. restore PostgreSQL
6. restore media
7. restore permissions
8. run migrations if required by the chosen release
9. start the stack
10. run health checks and smoke tests
11. switch traffic only after validation

## Safety rules

- This flow is isolated by default.
- Production overwrite requires explicit, separate authorization.

