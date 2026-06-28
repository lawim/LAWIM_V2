# Command: git-sync

## Objective

Prepare a controlled repository sync.

## Inputs

- Diff summary.
- Branch state.
- Trace notes.
- Policy gates.
- Remote availability.

## Outputs

- Git action plan.
- Commit or tag request when allowed.
- Trace record.

## Critical errors

- Dirty tree with unknown ownership.
- Missing trace.
- Forbidden policy transition.
- Remote absent when push is required.

## Implementation status

SKELETON_CREATED

## TODO

- Bind to the Git Service and Policy Service.
- Define the local-only fallback when no remote exists.
