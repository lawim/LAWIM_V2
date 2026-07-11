# Runbook - Local Disk Failure

STATUT : A COMPLETER

## Trigger

- disk absent
- disk read-only
- mount lost
- free space below threshold

## First actions

1. Preserve other destinations.
2. Verify cable, mount, UUID, label, and permissions.
3. Alert the operator.
4. Resume replication only after the disk is healthy again.

## Recovery source

- Google Drive
- external disk

