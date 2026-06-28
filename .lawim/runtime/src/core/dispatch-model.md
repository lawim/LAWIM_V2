# Dispatch Model

## Objective

Map the prepared commands to the services that will eventually execute them.

| Command | Primary services | Notes |
| --- | --- | --- |
| `status` | Report Service, PCC Service | Read-only snapshot. |
| `doctor` | Policy Service, Workflow Service, Git Service | Read-only diagnostics. |
| `run` | Execution Service, Workflow Service, PCC Service | Single-ticket execution. |
| `batch-run` | Planning Service, Execution Service, Report Service | Multi-ticket orchestration. |
| `review` | Review Service, Policy Service, Report Service | Formal review gate. |
| `close-sprint` | Planning Service, PCC Service, Report Service | Sprint closure flow. |
| `git-sync` | Git Service, Policy Service, Report Service | Controlled repository sync. |

## Critical errors

- Unknown command-to-service mapping.
- Contract drift with imported backlog files.
- More than one primary owner for a single dispatch path.

## Implementation status

SKELETON_CREATED

## TODO

- Convert the table into executable routing rules.
- Add policy gates before dispatch.
