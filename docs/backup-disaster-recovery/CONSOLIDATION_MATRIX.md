# Consolidation Matrix

STATUT : CIBLE DOCUMENTAIRE ACTIVE

This matrix records the first consolidation decisions for Mission 13.0 before any archival move or deletion.

| Document existant | Document canonique | Action | Archive | Statut final | Note |
|---|---|---|---|---|---|
| `README.md` | `docs/backup-disaster-recovery/README.md` | Update entry point | No | Active summary only | Root README keeps a short pointer. |
| `deployment/runbook/BackupRunbook.md` | `docs/backup-disaster-recovery/operations.md` | Convert to archive note | No | Historical | Legacy runbook is redundant. |
| `deployment/runbook/RestoreRunbook.md` | `docs/backup-disaster-recovery/restore-complete.md` | Convert to archive note | No | Historical | Legacy restore summary is redundant. |
| `release/deployment/BACKUP_RESTORE.md` | `docs/backup-disaster-recovery/operations.md` | Convert to archive note | No | Historical | Release-level summary only. |
| `OPS/OVH/BACKUP_POLICY.md` | `docs/backup-disaster-recovery/retention.md` | Convert to archive note | No | Historical | Policy fragments moved into canonical retention doc. |
| `OPS/OVH/RESTORE_PROCEDURE.md` | `docs/backup-disaster-recovery/restore-complete.md` | Convert to archive note | No | Historical | Procedure fragments moved into canonical restore docs. |
| `docs/BACKUP_PLATFORM.md` | `docs/backup-disaster-recovery/architecture.md` | Convert to archive note | No | Historical | Overlaps with canonical architecture. |
| `docs/BACKUP_MANAGER.md` | `docs/backup-disaster-recovery/operations.md` | Convert to archive note | No | Historical | Manager summary is superseded. |
| `docs/BACKUP_CENTER.md` | `docs/backup-disaster-recovery/cockpit.md` | Convert to archive note | No | Historical | Superseded by cockpit view. |
| `docs/BACKUP_CENTER_CONFIGURATION.md` | `docs/backup-disaster-recovery/cockpit.md` | Convert to archive note | No | Historical | Configuration details are now in canonical docs. |
| `docs/BACKUP_SECURITY.md` | `docs/backup-disaster-recovery/encryption.md` | Convert to archive note | No | Historical | Security rules moved into canonical docs. |
| `docs/EXTERNAL_BACKUP.md` | `docs/backup-disaster-recovery/external-disk.md` | Convert to archive note | No | Historical | External disk policy now canonical. |
| `docs/DATA_RETENTION_POLICY.md` | `docs/backup-disaster-recovery/retention.md` | Convert to archive note | No | Historical | Retention lives in one canonical policy. |
| `docs/RESTORE.md` | `docs/backup-disaster-recovery/restore-complete.md` | Convert to archive note | No | Historical | Restore overview is superseded. |
| `docs/RESTORATION_ENGINE.md` | `docs/backup-disaster-recovery/restore-tests.md` | Convert to archive note | No | Historical | Restore planner overview is superseded. |
| `docs/GOOGLE_DRIVE_CONNECTOR.md` | `docs/backup-disaster-recovery/google-drive.md` | Convert to archive note | No | Historical | Canonical Google Drive provider replaces fragments. |
| `docs/GOOGLE_DRIVE_SETUP.md` | `docs/backup-disaster-recovery/google-drive.md` | Convert to archive note | No | Historical | Setup flow consolidated. |
| `docs/GOOGLE_DRIVE_OAUTH.md` | `docs/backup-disaster-recovery/google-drive.md` | Convert to archive note | No | Historical | OAuth contract consolidated. |
| `docs/GOOGLE_DRIVE_ADMIN_CENTER.md` | `docs/backup-disaster-recovery/cockpit.md` | Convert to archive note | No | Historical | Admin center content consolidated. |
| `docs/GOOGLE_DRIVE_DISTRIBUTED_STORAGE.md` | `docs/backup-disaster-recovery/storage-providers.md` | Convert to archive note | No | Historical | Distributed storage mapping is now provider-oriented. |
| `docs/GOOGLE_DRIVE_MONITORING.md` | `docs/backup-disaster-recovery/monitoring-alerts.md` | Convert to archive note | No | Historical | Monitoring is now canonical elsewhere. |
| `docs/GOOGLE_DRIVE_QUOTA_POLICY.md` | `docs/backup-disaster-recovery/google-drive.md` | Convert to archive note | No | Historical | Quota policy is consolidated. |
| `docs/GOOGLE_DRIVE_FUNCTIONAL_CONFIGURATION.md` | `docs/backup-disaster-recovery/google-drive.md` | Convert to archive note | No | Historical | Functional configuration is consolidated. |

## Decisions

- The canonical active policy is documented only in `docs/backup-disaster-recovery/`.
- Legacy docs are preserved as historical records only when traceability matters.
- Operational paths in the repository are described separately from deployed server paths.
- Mission 12 and earlier reports remain historical and are not treated as current procedures.

