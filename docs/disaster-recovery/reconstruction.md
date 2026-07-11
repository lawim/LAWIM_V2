# Reconstruction

The canonical rebuild path is implemented by
`deployment/recovery/rebuild-lawim.sh`.

## Rebuild sequence

1. Create the target server.
2. Install Docker and the required system packages.
3. Restore or clone the LAWIM Git repository.
4. Restore the approved secrets.
5. Restore PostgreSQL from the Recovery Bundle.
6. Restore the media tree and generated documents.
7. Restore deployment, Nginx, systemd, and backup configuration files.
8. Launch LAWIM.
9. Run validation and confirm service availability.

## Operational model

- The script is idempotent.
- The script supports explicit bundle selection and latest-bundle discovery.
- Dry-run mode is used by the isolated recovery test harness.
- The rebuild flow does not rely on hidden operator knowledge.

## Isolated recovery test

`deployment/recovery/monthly-recovery-test.sh` executes the rebuild flow in an
isolated workspace and emits:

- `latest-report.json`
- `latest-report.md`

This report is the monthly evidence that the rebuild path remains executable.

## Expected inputs

- Git repository
- Restored secrets
- A valid Recovery Bundle
- The documented rebuild procedure
