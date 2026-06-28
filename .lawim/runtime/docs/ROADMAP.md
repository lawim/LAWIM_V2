# Roadmap

## Phase 0

Foundation created.

- Runtime directories exist.
- Command skeletons exist.
- Service skeletons exist.
- Policy bindings are mapped to imported sources.
- Smoke test scaffold exists.

## Phase 1

Implement the core runtime kernel.

- Add a real parser.
- Add command registration.
- Add shared runtime context objects.

## Phase 2

Add read-only command behavior.

- `status` is implemented.
- `doctor` is implemented.
- `--help` is available.
- Remaining commands stay stubbed.

## Phase 3

Add orchestration services.

- Bind Workflow, Policy, Execution, Review, Git, PCC, Planning, and Report services.
- Keep imports aligned with the existing backlog contracts and policies.

## Phase 4

Add controlled write paths.

- Connect report generation.
- Connect git synchronization safeguards.
- Keep every mutation traceable.

## Phase 5

Add tests and smoke automation.

- Add command contract tests.
- Add service boundary tests.
- Expand the runtime smoke test into a real verification suite.

## Constraints

- Do not modify governance.
- Do not open LOT-003.
- Do not open Sprint 007.
- Do not duplicate backlog contracts or policies.
