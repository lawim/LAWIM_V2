# DRF Implementation Plan

Mission 13.2 - Disaster Recovery Framework (DRF)

## Scope

This plan breaks the DRF mission into isolated lots that can be implemented,
tested, documented, validated, and committed independently.

Constraints:

- Do not break the validated Backup Orchestrator from Mission 13.1.
- Reuse the existing backup architecture and service boundaries.
- Never store secrets in recovery bundles.
- Keep bundles reproducible and verifiable.
- Finish one lot completely before starting the next.
- Produce a distinct Git commit for each lot.

## Lot 1 - Recovery Bundle Generator

- Objective: generate a canonical Recovery Bundle structure with manifest,
  bundle metadata, file inventory, and bundle packaging entry points.
- Components concerned:
  - `code/lawim_v2/backup/`
  - `code/lawim_v2/services.py`
  - `code/lawim_v2/server.py`
  - `deployment/backup/`
- Dependencies:
  - existing Backup Orchestrator state snapshot
  - repository root discovery
  - current LAWIM runtime version and Git SHA
- Risks:
  - accidental coupling with backup runtime behavior
  - inconsistent bundle layout across environments
  - non-deterministic file ordering or timestamps
- Tests to run:
  - unit tests for manifest generation and bundle path layout
  - API tests for bundle listing and bundle detail payloads
  - regression tests ensuring backup routes still work
- Acceptance criteria:
  - bundle manifest is generated deterministically
  - bundle structure is stable and documented
  - no secret values are written into the bundle
  - existing backup endpoints remain unchanged
- Complexity estimate: High

## Lot 2 - Inventories

- Objective: generate software, hardware, Docker, Git, and secret inventories
  with redaction guarantees.
- Components concerned:
  - `code/lawim_v2/backup/`
  - `code/lawim_v2/security/`
  - `deployment/backup/`
  - `env/`
  - `deployment/environments/production/`
- Dependencies:
  - bundle generator from Lot 1
  - access to local runtime commands when available
  - secret source declarations already present in the repo
- Risks:
  - leaking sensitive values in inventory output
  - command unavailability in minimal environments
  - partial inventories on hosts without Docker or PostgreSQL tools
- Tests to run:
  - inventory unit tests with tool availability mocks
  - secret redaction tests
  - compatibility tests for missing Docker/PostgreSQL binaries
- Acceptance criteria:
  - each inventory file is generated with the expected schema
  - secrets are represented only as metadata
  - absent tools degrade gracefully and are clearly reported
- Complexity estimate: High

## Lot 3 - Reconstruction Scripts

- Objective: add idempotent recovery and rebuild scripts under
  `deployment/recovery/` to prepare a blank server and restore LAWIM.
- Components concerned:
  - `deployment/recovery/`
  - `deployment/scripts/`
  - `deployment/backup/`
  - `deployment/systemd/`
- Dependencies:
  - bundle structure and inventory outputs from Lots 1 and 2
  - canonical restore flow from existing documentation
- Risks:
  - scripts assuming a specific host image
  - non-idempotent package or service operations
  - accidental modification of live production hosts
- Tests to run:
  - shell script lint or syntax checks
  - idempotency checks in a disposable workspace
  - dry-run rebuild path tests
- Acceptance criteria:
  - `rebuild-lawim.sh` is present and executable
  - repeated execution does not corrupt state
  - scripts only rely on documented bundle inputs
- Complexity estimate: High

## Lot 4 - Automated Recovery Validation

- Objective: validate bundle integrity, checksums, compatibility, and restore
  readiness in a machine-readable way.
- Components concerned:
  - `code/lawim_v2/backup/`
  - `code/lawim_v2/server.py`
  - `tests/`
- Dependencies:
  - completed bundle generator
  - completed inventories
  - recovery scripts
- Risks:
  - validation that passes even when bundle contents are incomplete
  - checksum mismatch handling not surfaced clearly enough
  - false positives when host tools are missing
- Tests to run:
  - validation unit tests
  - checksum mismatch tests
  - compatibility failure tests
- Acceptance criteria:
  - validation report returns explicit pass/fail per check
  - validation detects missing files and checksum drift
  - validation can run without mutating state
- Complexity estimate: Medium-High

## Lot 5 - Isolated Reconstruction Tests

- Objective: add automated isolated rebuild tests that exercise the recovery
  flow end to end without touching production state.
- Components concerned:
  - `tests/`
  - `deployment/recovery/`
  - `code/lawim_v2/backup/`
  - `code/lawim_v2/server.py`
- Dependencies:
  - reconstruction scripts from Lot 3
  - validation from Lot 4
- Risks:
  - test environment drift
  - long-running tests without deterministic timeout bounds
  - accidental dependence on local operator knowledge
- Tests to run:
  - isolated rebuild smoke test
  - bundle restore simulation
  - report generation test
- Acceptance criteria:
  - a disposable environment can be reconstructed from a valid bundle
  - the test records duration and outcome
  - the test produces a reusable report artifact
- Complexity estimate: High

## Lot 6 - Cockpit Disaster Recovery Tab

- Objective: expose the DRF status, bundles, validation history, and restore
  controls in the admin Cockpit.
- Components concerned:
  - `frontend/apps/admin/`
  - `frontend/packages/api-sdk/`
  - `code/lawim_v2/server.py`
  - `code/lawim_v2/services.py`
- Dependencies:
  - DRF backend endpoints from Lots 1 to 5
  - recovery score data model from Lot 7
- Risks:
  - UI exposing sensitive details
  - stale state if refresh behavior is weak
  - confusion between backup status and DRF status
- Tests to run:
  - API SDK contract tests
  - frontend rendering tests
  - route and navigation tests
- Acceptance criteria:
  - a dedicated "Disaster Recovery" tab exists
  - the Cockpit shows bundles, validation state, restore evidence, and score
  - no secrets are displayed
- Complexity estimate: Medium-High

## Lot 7 - Recovery Readiness Score

- Objective: compute a 0 to 100 percent readiness score from bundle freshness,
  Git synchronization, restore test success, secret availability, bundle
  integrity, and destination health.
- Components concerned:
  - `code/lawim_v2/backup/`
  - `frontend/apps/admin/`
  - `frontend/packages/api-sdk/`
- Dependencies:
  - validation data from Lot 4
  - isolated test results from Lot 5
  - Cockpit view from Lot 6
- Risks:
  - opaque scoring that is not explainable
  - score inflation from missing evidence
  - mismatch between backend score and UI score
- Tests to run:
  - score formula unit tests
  - edge case tests for missing Git, stale bundles, and absent secrets
  - API/UI snapshot tests for score display
- Acceptance criteria:
  - score is deterministic and explainable
  - score decreases for the documented failure modes
  - Cockpit displays score and contributing signals
- Complexity estimate: Medium

## Lot 8 - Final Documentation

- Objective: consolidate DRF documentation under `docs/disaster-recovery/`
  and remove or mark duplicate legacy explanations.
- Components concerned:
  - `docs/disaster-recovery/`
  - `docs/backup-disaster-recovery/`
  - `prompts/disaster_recovery_framework.md`
  - `README.md` and related indexes if needed
- Dependencies:
  - completed implementation details from Lots 1 to 7
- Risks:
  - duplicate guidance across old and new doc trees
  - references that drift away from the implemented code
- Tests to run:
  - documentation link checks
  - repository search for stale DRF references
- Acceptance criteria:
  - new DRF docs tree is complete and canonical
  - legacy duplication is removed or explicitly marked obsolete
  - documentation matches the shipped implementation
- Complexity estimate: Medium

## Lot 9 - Full Validation and Final Report

- Objective: run end-to-end validation, confirm rebuildability on a clean
  server model, and produce the final mission report.
- Components concerned:
  - `reports/`
  - `tests/`
  - `code/lawim_v2/backup/`
  - `frontend/apps/admin/`
  - `deployment/recovery/`
- Dependencies:
  - all previous lots completed and committed
  - stable Git state
  - reproducible bundle artifacts
- Risks:
  - final evidence not matching the validated code path
  - missing SHA or Git state reporting
  - residual uncommitted changes at handoff
- Tests to run:
  - full backend test suite for backup and DRF paths
  - frontend test suite for Cockpit DRF views
  - rebuild verification in an isolated environment
- Acceptance criteria:
  - an instance of LAWIM can be reconstructed from Git, restored secrets,
    and a valid Recovery Bundle
  - local SHA, remote SHA, and `main...origin/main = 0 0` are reported
  - worktree is clean at handoff
- Complexity estimate: High

## Recommended Execution Order

1. Recovery Bundle Generator
2. Inventories
3. Reconstruction Scripts
4. Automated Recovery Validation
5. Isolated Reconstruction Tests
6. Cockpit Disaster Recovery Tab
7. Recovery Readiness Score
8. Final Documentation
9. Full Validation and Final Report

## Delivery Rule

Each lot must finish with:

- code
- tests
- documentation
- Git commit
- delivery report

