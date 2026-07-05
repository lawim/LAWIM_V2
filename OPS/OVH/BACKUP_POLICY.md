# Backup Policy

## Baseline

- a pre-start backup is mandatory before deployment or other risky operations;
- the running stack has a dedicated backup service and timer;
- backup artifacts stay under `/opt/lawim/backups/`;
- cold archives and database dumps can be exported to external storage after validation.

## Rotation policy

- daily backups should be kept for the current operational window;
- weekly and monthly copies should be rolled into external archives;
- expired copies should be pruned only after a verified restore exists.

## Retention policy

- keep the last known-good backup on the server;
- keep restore-capable copies off-server for disaster recovery;
- never delete the only validated restore point.

## Restore testing

- restore tests must be performed on a disposable path or disposable database;
- validate the backup before trusting it for rollback;
- record the restore result in `DEPLOYMENT_HISTORY.md`.
