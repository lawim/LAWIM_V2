# Commands

This document summarizes the prepared LAWIM runtime commands.
The per-command skeletons live in `.lawim/runtime/src/commands/`.

## Minimal executable surface

- `lawim --help` is available.
- `lawim status` is implemented.
- `lawim doctor` is implemented.
- `lawim git-sync --status`, `lawim git-sync --commit "<message>"`, `lawim git-sync --tag "<tag>"`, and `lawim git-sync --push` are implemented.
- `lawim run`, `lawim batch-run`, `lawim review`, and `lawim close-sprint` remain stubs.

| Command | Objective | Inputs | Outputs | Critical errors | Status | TODO |
| --- | --- | --- | --- | --- | --- | --- |
| `status` | Read current runtime readiness and trace links. | Runtime root, PCC summary, latest report pointers. | Readiness snapshot. | Missing runtime root; unreadable report trail; missing PCC reference. | IMPLEMENTED | Bind to a read-only status model. |
| `doctor` | Check runtime health and contract coverage. | Filesystem, command registry, imported contracts, imported policies. | Diagnostic result with PASS/WARN/FAIL. | Missing file, contract drift, unreadable policy source. | IMPLEMENTED | Add structural and policy validators. |
| `run` | Execute one prepared work item through the runtime. | Ticket context, planning data, policy gates, execution context. | Execution trace and report seed. | Missing ticket, invalid state, unresolved policy gate. | SKELETON_CREATED | Bind to the execution service. |
| `batch-run` | Execute a controlled batch of work items. | Batch manifest, ordered ticket list, dependency map, policy gates. | Batch execution trace and aggregate report seed. | Invalid order, unresolved dependency, missing batch manifest. | SKELETON_CREATED | Add batch planning and aggregation. |
| `review` | Orchestrate a formal review gate. | Deliverable, checklist, evidence, findings inputs. | Review decision, findings, and trace. | Missing evidence, incomplete checklist, unresolved review gate. | SKELETON_CREATED | Bind review outcomes to reports. |
| `close-sprint` | Prepare and close a sprint in a traceable way. | Sprint state, open-ticket list, validations, closure evidence. | Sprint closure report and decision bundle. | Open ticket, missing validation, absent closure evidence. | SKELETON_CREATED | Add closure sequencing and checks. |
| `git-sync` | Prepare a controlled repository sync. | Diff summary, branch state, tag intent, remote availability. | Git status, commit, tag, or push result with traceable output. | Empty commit message, clean tree, empty tag, existing tag, missing remote, forbidden mutation. | IMPLEMENTED | Extend safety checks if upstream rules evolve. |

## Notes

- The runtime does not duplicate contract text from the architecture backlog.
- The command layer is executable for `status`, `doctor`, `--help`, and the safe `git-sync` surface at this stage.
