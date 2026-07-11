# Mission 13.0 - Backup & Disaster Recovery Documentation Inventory

Date: 2026-07-11

## Scope

This inventory records the final state of the BDR documentation after consolidation and deletion of superseded duplicates.

## Method

- Reviewed repository documentation in `README.md`, `docs/`, `OPS/`, `deployment/`, `release/`, and `reports/`.
- Kept mission reports only when explicitly required.
- Deleted superseded duplicate documents with `git rm`.
- Did not create any extra consolidation directory.

## Canonical sources of truth

| Subject | Canonical document | Notes |
|---|---|---|
| Overview | `docs/backup-disaster-recovery/README.md` | Single entry point for the BDR tree. |
| Architecture | `docs/backup-disaster-recovery/architecture.md` | Runtime contract, sources of truth, and path model. |
| Operations | `docs/backup-disaster-recovery/operations.md` | Reading order, responsibilities, and OVH deployment path. |
| Schedules | `docs/backup-disaster-recovery/schedules.md` | Target policy, deployed state, and validation notes. |
| Storage providers | `docs/backup-disaster-recovery/storage-providers.md` | Provider contract. |
| Google Drive | `docs/backup-disaster-recovery/google-drive.md` | Off-site provider policy and checks. |
| Local disk | `docs/backup-disaster-recovery/local-disk.md` | Local replication target. |
| External disk | `docs/backup-disaster-recovery/external-disk.md` | Offline weekly copy target. |
| Encryption | `docs/backup-disaster-recovery/encryption.md` | Encryption and secret handling rules. |
| Retention | `docs/backup-disaster-recovery/retention.md` | Retention policy and safeguards. |
| Monitoring and alerts | `docs/backup-disaster-recovery/monitoring-alerts.md` | Health, alerting, and metrics. |
| Cockpit | `docs/backup-disaster-recovery/cockpit.md` | Operator-facing control surface. |
| Restore database | `docs/backup-disaster-recovery/restore-database.md` | PostgreSQL restore path. |
| Restore media | `docs/backup-disaster-recovery/restore-media.md` | Media restore path. |
| Restore complete | `docs/backup-disaster-recovery/restore-complete.md` | Full system restore path. |
| Disaster recovery plan | `docs/backup-disaster-recovery/disaster-recovery-plan.md` | Scenario matrix and response rules. |
| Incident response | `docs/backup-disaster-recovery/incident-response.md` | Incident handling and communications. |
| Restore tests | `docs/backup-disaster-recovery/restore-tests.md` | Daily, weekly, monthly, and quarterly checks. |
| Maintenance | `docs/backup-disaster-recovery/maintenance.md` | Maintenance and change procedure. |
| Troubleshooting | `docs/backup-disaster-recovery/troubleshooting.md` | Known failure modes and operator guidance. |
| Audit checklist | `docs/backup-disaster-recovery/audit-checklist.md` | Final compliance checklist. |

## Consolidation matrix

| File(s) | Reason | Canonical replacement | References found | Action | Commit associé |
|---|---|---|---|---|---|
| `docs/backup-disaster-recovery/archive/README.md`<br>`docs/backup-disaster-recovery/CONSOLIDATION_MATRIX.md` | Temporary consolidation artifacts with no operational value. | `docs/backup-disaster-recovery/README.md` and this inventory. | `docs/backup-disaster-recovery/README.md`, `docs/backup-disaster-recovery/google-drive.md`, `docs/backup-disaster-recovery/operations.md`. | SUPPRIMÉ | this step |
| `docs/BACKUP_PLATFORM.md`<br>`docs/BACKUP_MANAGER.md`<br>`docs/BACKUP_CENTER.md`<br>`docs/BACKUP_CENTER_CONFIGURATION.md`<br>`docs/BACKUP_SECURITY.md`<br>`docs/EXTERNAL_BACKUP.md`<br>`docs/DATA_RETENTION_POLICY.md`<br>`docs/RESTORE.md`<br>`docs/RESTORATION_ENGINE.md` | Duplicate backup and restore summaries superseded by the canonical BDR tree. | `docs/backup-disaster-recovery/architecture.md`, `operations.md`, `retention.md`, `restore-*`. | Old doc references and report text only. | SUPPRIMÉ | this step |
| `docs/GOOGLE_DRIVE_CONNECTOR.md`<br>`docs/GOOGLE_DRIVE_SETUP.md`<br>`docs/GOOGLE_DRIVE_OAUTH.md`<br>`docs/GOOGLE_DRIVE_ADMIN_CENTER.md`<br>`docs/GOOGLE_DRIVE_DISTRIBUTED_STORAGE.md`<br>`docs/GOOGLE_DRIVE_MONITORING.md`<br>`docs/GOOGLE_DRIVE_QUOTA_POLICY.md`<br>`docs/GOOGLE_DRIVE_FUNCTIONAL_CONFIGURATION.md` | Duplicate Google Drive provider documents superseded by the canonical provider page. | `docs/backup-disaster-recovery/google-drive.md` and `storage-providers.md`. | Old doc references and report text only. | SUPPRIMÉ | this step |
| `deployment/runbook/BackupRunbook.md`<br>`deployment/runbook/RestoreRunbook.md`<br>`release/deployment/BACKUP_RESTORE.md`<br>`OPS/OVH/BACKUP_POLICY.md`<br>`OPS/OVH/RESTORE_PROCEDURE.md` | Duplicate operational summaries superseded by canonical BDR procedures. | `docs/backup-disaster-recovery/operations.md`, `restore-database.md`, `restore-media.md`, `restore-complete.md`, `retention.md`. | Old doc references and report text only. | SUPPRIMÉ | this step |

## Kept report

| File | Reason | Status |
|---|---|---|
| `reports/product_reviews/Mission_12_Report.md` | Mission report kept by explicit rule. It remains useful for mission traceability. | KEPT |

## Decisions de consolidation

- Superseded documents are deleted permanently.
- Git history is the only historical record for the project.
- The root README points only to the canonical BDR tree.
- Mission 12 report remains in place because mission reports are explicitly preserved.
