# ADR-008: Evidence-Based Validation

**Status:** Accepted
**Date:** 2026-07-22

## Context

Stakeholders frequently mistake code presence, passing tests, or successful deployment for real business functionality. A component can be fully implemented, tested, and deployed but still fail on a real user message. This creates false confidence and delays detection of production issues.

## Decision

Validation levels L0 through L8 are mandatory. Every component declares its achieved validation level in a canonical inventory. Forbidden equivalence mappings (e.g., "tests pass" != "feature works") are documented and enforced. No component can claim validation level L6 or higher without real channel proof (a genuine message traversing the full production pipeline).

## Justification

Accurate reporting prevents false confidence. Stakeholders see exactly what has been proven at each level. Forbidden equivalences eliminate the most common reporting errors. The L6 gate ensures that no component is declared production-ready without proven end-to-end behavior on a real channel.

## Positive Consequences

- Stakeholder reports reflect actual runtime evidence, not code artifacts
- Forbidden equivalences prevent common reporting mistakes
- L6+ requires real channel proof, eliminating simulation gaps
- Objective criteria for release readiness decisions
- Teams have a clear definition of done per validation level

## Negative Consequences

- Validation level tracking adds process overhead
- L6 evidence collection requires production access and coordination
- Some components may remain at L5 for extended periods
- Reporting tooling must be built or adapted

## Rejected Alternatives

- **Self-certification by developers**: No objective evidence, conflicts of interest
- **No validation levels**: Current state; leads to false confidence
- **Only L0 (code present)**: Meaningless for stakeholders

## Affected Components

- System inventory
- Release manifest
- CI/CD pipeline
- All components (must declare their level)
- Stakeholder reporting

## Compliance Criteria

- Every component in the system inventory has a declared validation level
- Forbidden equivalences are documented in the validation policy
- No L6+ claim without real channel evidence in the evidence log
- Validation level is checked as a release gate
- Evidence log is reviewed before major releases

## References

- ADR-007: V2->V3 Shadow Migration
- Production Evidence Policy (docs/ai-context/LAWIM_PRODUCTION_EVIDENCE_POLICY.md)
