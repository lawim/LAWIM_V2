# Mission 13.2 - Lot 4 - Automated Recovery Validation

## Objective

Expose a machine-readable DRF validation procedure that verifies bundle
integrity, checksums, compatibility, Git state, Docker availability, PostgreSQL
availability, and restore readiness.

## Delivered Files

- `code/lawim_v2/backup/recovery.py`
- `code/lawim_v2/server.py`
- `tests/test_disaster_recovery_validation.py`

## Implemented Behavior

The validation flow now returns explicit checks for:

- manifest presence;
- bundle integrity;
- checksum validity;
- LAWIM version compatibility;
- Git synchronization;
- Docker availability;
- PostgreSQL availability;
- restore readiness.

The backup API now exposes DRF read/validate endpoints:

- `GET /api/v2/backup/recovery`
- `GET /api/v2/backup/recovery/bundles`
- `GET /api/v2/backup/recovery/latest`
- `GET /api/v2/backup/recovery/validation`
- `POST /api/v2/backup/recovery/validate`

## Validation

Executed:

- `python3 -m unittest tests.test_disaster_recovery_validation tests.test_disaster_recovery_bundle tests.test_recovery_script tests.test_backup_api tests.test_backup_module`

Result:

- all targeted tests passed
- checksum drift is detected
- missing files are detected
- validation remains machine-readable and deterministic

## Notes

- `restore_ready` remains focused on bundle integrity and compatibility, while
  the new check list makes Docker and PostgreSQL availability explicit.
- The new API surface stays under the existing admin-protected backup routes.
