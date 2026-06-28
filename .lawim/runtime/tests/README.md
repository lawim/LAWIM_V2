# Runtime Tests

## Scope

This directory starts with structure validation only.
It does not test business behaviour.

## Current test

- `runtime-foundation-smoke.sh` checks that the runtime foundation files exist.
- `runtime-minimal-smoke.sh` checks `lawim --help`, `lawim status`, and `lawim doctor`.
- `git-service-smoke.sh` checks the safe `lawim git-sync` surface in an isolated repository.

## Status

SKELETON_CREATED

## TODO

- Add command contract tests.
- Add service boundary tests.
- Add report snapshot tests.
