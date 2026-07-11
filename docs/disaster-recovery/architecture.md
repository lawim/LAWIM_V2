# DRF Architecture

The Disaster Recovery Framework is layered on top of the validated backup
platform.

## Layers

1. Backup Orchestrator
   - Produces the operational backup status, destinations, metrics, and restore
     records.
   - Remains the source of truth for backup execution.
2. Recovery Bundle Generator
   - Builds a reproducible bundle from the current repository, backup state,
     system inventory, and runtime artifacts.
   - Writes `manifest.json` plus inventory and reconstruction inputs.
3. Recovery Validation
   - Verifies integrity, checksum drift, runtime compatibility, Git
     synchronization, Docker/PostgreSQL availability, and restore readiness.
4. Recovery Score
   - Aggregates freshness, validation, secret inventory, destination health,
     and isolated recovery test evidence into a 0-100 readiness score.
5. Reconstruction Tooling
   - `deployment/recovery/rebuild-lawim.sh` prepares a blank server and applies
     the recovery bundle.
   - `deployment/recovery/monthly-recovery-test.sh` exercises the rebuild flow
     in an isolated workspace.
6. Cockpit
   - The admin console surfaces bundle status, validation checks, readiness
     signals, and bundle downloads.

## Design rules

- Recovery bundles are reproducible and verifiable.
- Secrets are inventoried, never exported in cleartext.
- The bundle is a reconstruction artifact, not just a data archive.
- The backend exposes DRF state through the existing backup API surface.

## Data flow

1. Backup state is read from the existing backup service.
2. The DRF generator emits the bundle and manifest.
3. Validation evaluates the bundle against the current runtime and repository.
4. Recovery tests verify the rebuild flow in an isolated workspace.
5. The readiness score combines the evidence into a single operational signal.
