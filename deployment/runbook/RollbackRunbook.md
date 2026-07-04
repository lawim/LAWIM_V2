# Rollback Runbook

## Purpose

Document rollback actions for a controlled migration attempt without executing them automatically.

## Procedure

1. Stop services and preserve logs.
2. Restore the previous release or backup snapshot.
3. Re-verify readiness and health.
4. Re-open incident channels if needed.
