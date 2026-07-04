# BACKUP_RESTORE

## Backup

- use the existing backup scripts under `deployment/backup/` and `deployment/scripts/`
- keep backup archives and checksums outside the master repository
- keep secrets external
- keep the backup policy aligned with the deployment manifest

## Restore

- validate the archive checksum before restore
- restore data and configuration in the documented order
- verify the application health endpoints after restore
- do not use restore operations to launch a migration

## Stored artifacts

- database dumps
- media and file archives
- release checksums
- logs that are retained for audit

