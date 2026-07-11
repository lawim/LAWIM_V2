# Validation

Recovery validation is exposed through the existing admin-protected backup API.

## API surface

- `GET /api/v2/backup/recovery`
- `GET /api/v2/backup/recovery/bundles`
- `GET /api/v2/backup/recovery/latest`
- `GET /api/v2/backup/recovery/validation`
- `POST /api/v2/backup/recovery/validate`
- `GET /api/v2/backup/recovery/bundles/{bundle_id}/download`

## Checks

The validator reports explicit pass/fail checks for:

- manifest presence
- bundle integrity
- checksum validity
- LAWIM version compatibility
- Git synchronization
- Docker availability
- PostgreSQL availability
- restore readiness

## Readiness evidence

The readiness score uses:

- bundle freshness
- validation results
- secret inventory coverage
- isolated recovery test evidence
- destination availability
- RPO and RTO metrics

## Monthly test

The monthly isolated recovery test:

- selects the latest bundle or honors an explicit override;
- runs the rebuild flow in dry-run mode inside an isolated workspace;
- writes JSON and Markdown evidence files;
- remains idempotent across repeated runs.
