# Mission 13.0 - Backup & Disaster Recovery Documentation Inventory

Date: 2026-07-11

## Scope

This inventory covers the current documentation and operational procedures that overlap with Mission 13.0:

- backup and restore documentation;
- disaster recovery and incident procedures;
- Google Drive and storage provider documentation;
- retention, monitoring, and systemd scheduling references;
- historical reports that may duplicate operational guidance.

## Method

- Reviewed repository documentation in `README.md`, `docs/`, `OPS/`, `deployment/`, `release/`, and `reports/`.
- Focused on files that already describe backup, restore, Google Drive, retention, or incident handling.
- Classified each item by current state, gap versus Mission 13, and recommended action.
- Did not delete, rewrite, or archive anything in this step.

## Key findings

1. There is no single canonical Mission 13 backup and disaster recovery document yet.
2. The backup story is split between `docs/`, `OPS/OVH/`, `deployment/runbook/`, and `release/`.
3. Backup schedules conflict:
   - `README.md` says 03:00 and 15:00 WAT;
   - `reports/product_reviews/Mission_12_Report.md` says 06:00 and 18:00;
   - `deployment/systemd/lawim-backup.timer` is only `daily`.
4. The runtime backup asset set exists under `deployment/backup/`, but several docs still point to `scripts/ops/` or `/opt/lawim/deployment/backup/`.
5. Google Drive, retention, and backup-center concepts are documented in many small files, but they are still fragmented and partially placeholder-based.
6. Several reports are historical and useful, but they should not be treated as the operational source of truth for Mission 13.

## Inventory matrix

| Document existant | Etat actuel | Ecart | Action | Responsable | Validation |
|---|---|---|---|---|---|
| `README.md`<br>`reports/product_reviews/Mission_12_Report.md` | Executive summary and mission history exist, but the backup posture is outdated and the schedule is not Mission 13 compliant. | No canonical Mission 13 schedule, no provider model, and no backup/restore state model. | Keep as top-level entry points, then update after the canonical Mission 13 docs are in place. | Docs + Ops | Manual review and link check. |
| `deployment/runbook/BackupRunbook.md`<br>`deployment/runbook/RestoreRunbook.md`<br>`release/deployment/BACKUP_RESTORE.md`<br>`OPS/OVH/BACKUP_POLICY.md`<br>`OPS/OVH/RESTORE_PROCEDURE.md` | Several partial descriptions of the same backup/restore flow exist. | No single source of truth, no support-level separation, no lifecycle/state model, no verified restore discipline. | Merge into Mission 13 operational runbooks and archive the older summaries if they become redundant. | Ops + Backend | Dry-run restore review and consistency check. |
| `deployment/runbook/IncidentRunbook.md`<br>`OPS/OVH/INCIDENT_RUNBOOK.md`<br>`deployment/runbook/GoLiveRunbook.md`<br>`deployment/runbook/ProductionRunbook.md`<br>`deployment/runbook/RollbackRunbook.md` | Generic incident and deployment procedures exist. | No backup-specific incident runbooks for Google Drive, local disk, external disk, corruption, or ransomware. | Keep the generic runbooks; add Mission 13 runbooks for backup failure scenarios. | Ops + Security | Incident tabletop exercise. |
| `deployment/systemd/lawim-backup.service`<br>`deployment/systemd/lawim-backup.timer`<br>`deployment/scripts/backup.sh`<br>`deployment/scripts/restore.sh`<br>`deployment/backup/backup-policy.md` | A real runtime backup stack exists, but the timer and scripts are still simplistic. | Timer is `daily`, not 02:00 and 14:30; the schedule and paths do not yet match Mission 13 requirements. | Keep as technical baseline; align with the Mission 13 scheduler and path contract. | Backend + Ops | `systemd-analyze verify`, `systemd-analyze calendar`. |
| `docs/BACKUP_PLATFORM.md`<br>`docs/BACKUP_MANAGER.md`<br>`docs/BACKUP_CENTER.md`<br>`docs/BACKUP_CENTER_CONFIGURATION.md`<br>`docs/BACKUP_SECURITY.md`<br>`docs/EXTERNAL_BACKUP.md`<br>`docs/DATA_RETENTION_POLICY.md`<br>`docs/RESTORE.md`<br>`docs/RESTORATION_ENGINE.md` | Conceptual backup and restore documents exist, mostly placeholder-based. | They do not yet describe the Mission 13 lifecycle, verified backups, or provider contract. | Convert the useful parts into the new canonical documentation tree; archive the rest if they become duplicate summaries. | Architecture + Docs | Review against the Mission 13 architecture contract. |
| `docs/GOOGLE_DRIVE_CONNECTOR.md`<br>`docs/GOOGLE_DRIVE_SETUP.md`<br>`docs/GOOGLE_DRIVE_OAUTH.md`<br>`docs/GOOGLE_DRIVE_ADMIN_CENTER.md`<br>`docs/GOOGLE_DRIVE_DISTRIBUTED_STORAGE.md`<br>`docs/GOOGLE_DRIVE_MONITORING.md`<br>`docs/GOOGLE_DRIVE_QUOTA_POLICY.md`<br>`docs/GOOGLE_DRIVE_FUNCTIONAL_CONFIGURATION.md` | Google Drive is documented across many small files, with a mix of connector, OAuth, monitoring, and admin-center content. | The provider contract is fragmented; some docs are placeholder-only and some overlap heavily. | Consolidate into a single Google Drive provider section and keep only one authoritative policy chain. | Storage + Security + Docs | Provider contract review and secret-safety check. |
| `docs/STORAGE_RESOURCE_REGISTRY.md`<br>`docs/STORAGE_ROUTING_POLICY.md`<br>`docs/STORAGE_ORCHESTRATOR.md` | Strong starting point for provider-agnostic storage routing. | The current model is still centered on the ten Google Drive placeholders, not on a reusable `StorageProvider` contract. | Reuse as the base for the Mission 13 storage abstraction layer. | Storage platform | Interface review and route consistency check. |
| `docs/OVH_DEPLOYMENT_MANIFEST.md`<br>`OPS/OVH/README.md`<br>`OPS/OVH/SERVER_ARCHITECTURE.md`<br>`OPS/OVH/HEALTHCHECKS.md`<br>`OPS/OVH/MONITORING.md`<br>`OPS/OVH/SERVICES.md` | Deployment and host operations are documented in a coherent but separate track. | These docs do not yet expose the full backup state machine, support health model, or restore-test posture. | Keep them as infrastructure references and add links to the new backup subsystem docs. | Ops | Infrastructure path review and service validation. |
| `release/deployment/RUNBOOK.md`<br>`release/deployment/MONITORING.md`<br>`release/deployment/BACKUP_RESTORE.md`<br>`release/manifests/DEPLOYMENT_MANIFEST.md` | Release-oriented operational docs exist. | They are useful for packaging and go-live, but they are not the final operational reference for backup and DR. | Preserve them as release documentation; do not use them as the main backup source of truth. | Release engineering | Manifest consistency check. |
| `docs/DISASTER_RECOVERY_REPORT.md`<br>`reports/program/RELEASE-PROGRAM-AAC-B2-BACKUP-CENTER-COMPLETION.md`<br>`reports/product_reviews/Mission_12_Report.md` | Historical closure reports explain the current posture and completed work. | They are not procedures and they already contain schedule or scope details that may be stale. | Keep them as historical evidence and link to them from the new canonical docs if needed. | PM + Docs | Historical reference review only. |

## Duplicate clusters to collapse later

- Backup and restore runbooks
  - `README.md`
  - `OPS/OVH/BACKUP_POLICY.md`
  - `OPS/OVH/RESTORE_PROCEDURE.md`
  - `deployment/runbook/BackupRunbook.md`
  - `deployment/runbook/RestoreRunbook.md`
  - `release/deployment/BACKUP_RESTORE.md`

- Google Drive and storage provider docs
  - `docs/GOOGLE_DRIVE_CONNECTOR.md`
  - `docs/GOOGLE_DRIVE_SETUP.md`
  - `docs/GOOGLE_DRIVE_OAUTH.md`
  - `docs/GOOGLE_DRIVE_ADMIN_CENTER.md`
  - `docs/GOOGLE_DRIVE_DISTRIBUTED_STORAGE.md`
  - `docs/GOOGLE_DRIVE_MONITORING.md`
  - `docs/GOOGLE_DRIVE_QUOTA_POLICY.md`
  - `docs/STORAGE_RESOURCE_REGISTRY.md`
  - `docs/STORAGE_ROUTING_POLICY.md`
  - `docs/STORAGE_ORCHESTRATOR.md`

- Backup center and retention concepts
  - `docs/BACKUP_PLATFORM.md`
  - `docs/BACKUP_MANAGER.md`
  - `docs/BACKUP_CENTER.md`
  - `docs/BACKUP_CENTER_CONFIGURATION.md`
  - `docs/BACKUP_SECURITY.md`
  - `docs/EXTERNAL_BACKUP.md`
  - `docs/DATA_RETENTION_POLICY.md`
  - `docs/RESTORE.md`
  - `docs/RESTORATION_ENGINE.md`

## Recommended next actions

1. Create the canonical Mission 13 documentation tree under `docs/backup-disaster-recovery/`.
2. Normalize the backup schedule, paths, and runtime service names so the docs, scripts, and timers match.
3. Move obsolete summaries to historical references instead of keeping parallel copies.
4. Keep the existing reports as evidence, but stop treating them as operational procedure sources.
5. After the documentation tree is in place, update the top-level `README.md` and the relevant ops references.

## Decisions de consolidation

| Cluster | Canonical doc | Action performed | Archive | Final status | Commit associe |
|---|---|---|---|---|---|
| Entry points and policy summary | `docs/backup-disaster-recovery/README.md` and `docs/backup-disaster-recovery/schedules.md` | Root README shortened and linked to the canonical tree; schedule policy normalized to the target 02:00/14:30 WAT | No | Active | `38e9719d` |
| Backup and restore runbooks | `docs/backup-disaster-recovery/operations.md`, `restore-database.md`, `restore-media.md`, `restore-complete.md`, `restore-tests.md` | Legacy runbooks converted to archive notes with links to canonical procedures | In place | Historical only | `38e9719d` |
| Backup center documents | `docs/backup-disaster-recovery/cockpit.md`, `operations.md`, `retention.md` | Backup center summaries converted to archive notes | In place | Historical only | `38e9719d` |
| Google Drive documents | `docs/backup-disaster-recovery/google-drive.md`, `storage-providers.md`, `cockpit.md`, `monitoring-alerts.md` | Google Drive connector, OAuth, admin, quota, monitoring, and functional docs consolidated into one canonical provider page | In place | Historical only | `38e9719d` |
| Retention and restore overviews | `docs/backup-disaster-recovery/retention.md`, `restore-database.md`, `restore-media.md`, `restore-complete.md` | General retention and restore overviews archived in place | In place | Historical only | `38e9719d` |
| Mission 12 historical report | `reports/product_reviews/Mission_12_Report.md` | Added an evolution note pointing to the active schedule policy | No | Historical, annotated | `38e9719d` |
| Canonical archive space | `docs/backup-disaster-recovery/archive/README.md` | Added an explicit archive landing page for superseded documents | No | Active archive index | `38e9719d` |
