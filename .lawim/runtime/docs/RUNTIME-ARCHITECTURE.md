# Runtime Architecture

## Goal

Create an internal runtime layer that orchestrates LAWIM commands without changing governance.

## Layer model

1. Entry point: `bin/lawim`
2. Core: `src/core`
3. Command contracts: `src/commands`
4. Service boundaries: `src/services`
5. Policy bindings: `src/policies`
6. Traces: `reports/runtime`

## Execution flow

CLI request -> core validation -> command skeleton -> service orchestration -> policy check -> report seed -> trace output.

## Imported sources

- `.lawim/architecture-backlog/contracts/`
- `.lawim/architecture-backlog/policies/`

## Non goals

- No business logic.
- No direct mutation of governance documents.
- No duplicate copies of contracts or policies.
- No opening of LOT-003 or Sprint 007.

## Implementation status

FOUNDATION_CREATED

## TODO

- Add the real parser and command registry.
- Add read models for `status` and `doctor`.
- Add adapters for review, planning, PCC, report, and Git.
