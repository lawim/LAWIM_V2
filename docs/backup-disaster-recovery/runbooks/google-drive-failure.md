# Runbook - Google Drive Failure

STATUT : A COMPLETER

## Trigger

- upload failure
- OAuth invalid
- quota exceeded
- remote unavailable

## First actions

1. Keep local copies intact.
2. Verify network, rclone, OAuth, quota, and logs.
3. Continue backup creation locally if possible.
4. Escalate if the remote destination remains unavailable.

## Recovery source

- local disk
- external disk

