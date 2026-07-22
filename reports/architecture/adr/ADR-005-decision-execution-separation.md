# ADR-005: Decision-Execution Separation

**Status:** Accepted
**Date:** 2026-07-22

## Context

Deciding what to do and doing it are fundamentally different concerns. When they are mixed, a single bug or LLM error can both decide incorrectly and execute irreversibly. Rollback is impossible because the decision and its effects are interleaved. Replay and audit require reconstructing both the decision rationale and the execution outcome separately.

## Decision

ProjectBrain produces a DecisionResult that specifies what to do. The ActionExecutionEngine reads the DecisionResult and executes it. A DecisionResult has no side effects — it is a pure data structure. Execution is an isolated concern that can be retried, rolled back, or replayed independently.

## Justification

Separation enables idempotent execution (same DecisionResult applied twice produces the same outcome). Rollback becomes possible by reversing the execution without re-litigating the decision. Replay consists of re-executing stored DecisionResults. Audit trail separates decision intent from execution outcome.

## Positive Consequences

- DecisionResults are pure data: storable, comparable, replayable
- Execution is idempotent by design
- Rollback reverses execution without reversing the decision
- Full audit trail: what was decided vs. what actually happened
- Execution can be tested independently of decision logic

## Negative Consequences

- Two-phase flow adds complexity to each business operation
- DecisionResult schema must be designed upfront for each operation
- Some operations are inherently non-reversible (e.g., payment sent)

## Rejected Alternatives

- **Monolithic decision-execution**: Current state; no audit separation, no rollback
- **Event sourcing only**: Captures events but not the decision rationale
- **LLM decides and executes**: Non-deterministic, no rollback possible

## Affected Components

- ProjectBrain
- ActionExecutionEngine
- DecisionResult models
- All domain runtimes
- AuditService

## Compliance Criteria

- Every business operation has a corresponding DecisionResult type
- DecisionResult can be serialized, stored, and replayed
- Executing the same DecisionResult twice produces identical state
- Audit log records both DecisionResult and execution outcome separately
- Rollback procedure exists for each DecisionResult type

## References

- ADR-004: LLM Is Not the Business Decision Maker
- ADR-006: Event-Driven Runtime
- ADR-009: Domain Runtime Boundaries
