# Runbook - PostgreSQL Failure

STATUT : A COMPLETER

## Trigger

- database unavailable
- corruption
- restore needed

## First actions

1. Stop write activity.
2. Select a validated backup.
3. Restore into an isolated database.
4. Verify schema and key queries.

## Recovery source

- latest validated PostgreSQL backup

