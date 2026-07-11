# Mission 13.2 - Lot 3 - Reconstruction Scripts

## Objective

Add an idempotent recovery entry point that can rebuild LAWIM from a Recovery
Bundle on a fresh host without relying on undocumented operator knowledge.

## Delivered Files

- `deployment/recovery/rebuild-lawim.sh`
- `tests/test_recovery_script.py`

## Implemented Behavior

The rebuild script now:

- accepts an explicit bundle path with `--bundle`;
- discovers the latest `LAWIM-DRF-*` bundle from the recovery bundle root;
- restores the repository into a release directory and repoints `/opt/lawim/current`;
- restores secrets and system configuration without writing secret values into bundles;
- restores PostgreSQL either through `DATABASE_URL`/`LAWIM_DATABASE_URL` or through
  the Compose `postgres` service;
- restores media into the configured shared storage path;
- launches LAWIM through the production Compose file;
- verifies the rebuilt instance through the configured health endpoint;
- supports `--dry-run` for non-invasive validation.

## Validation

Executed:

- `bash -n deployment/recovery/rebuild-lawim.sh`
- `python3 -m unittest tests.test_recovery_script tests.test_disaster_recovery_bundle tests.test_backup_api tests.test_backup_module`

Result:

- all targeted tests passed
- the script is executable
- dry-run execution is idempotent and bundle-aware
- the backup orchestrator behavior remains intact

## Notes

- The script reuses the existing release-based deployment pattern instead of
  inventing a parallel restore layout.
- PostgreSQL restore has a containerized fallback, which keeps the script usable
  even when no external `DATABASE_URL` is provided.
- This lot is additive and does not modify the validated Backup Orchestrator.
