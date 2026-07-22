# ADR-007: V2->V3 Shadow Migration

**Status:** Accepted
**Date:** 2026-07-22

## Context

V2 is in production with active users. V3 introduces a fundamentally different architecture (LROS, ProjectProfile, event-driven runtime). A cutover migration risks extended downtime, data loss, or regressions that affect real users. V2 cannot be paused while V3 stabilizes.

## Decision

V3 runs in shadow mode by default with all feature flags turned off. V2 adapters observe V2 operations and produce LROS-compatible results without affecting production behavior. Each domain is migrated independently when confidence is sufficient — measured by shadow comparison accuracy exceeding a defined threshold over a monitoring period. Feature flags enable per-domain activation.

## Justification

Shadow mode provides production safety. If V3 produces incorrect results, V2 continues unaffected. Per-domain migration limits blast radius. Shadow comparison data provides objective evidence that V3 matches V2 behavior before any real user impact. Rollback is per-domain by toggling a feature flag.

## Positive Consequences

- Zero production risk during V3 deployment
- Per-domain migration allows granular confidence building
- Shadow comparison generates real evidence of correctness
- Rollback is instant per domain via feature flag
- Users experience no disruption during migration

## Negative Consequences

- Dual execution doubles resource consumption during shadow period
- Shadow adapter development for each V2 domain is significant work
- Monitoring infrastructure required for shadow comparison
- Migration period may last months for complex domains

## Rejected Alternatives

- **Big-bang cutover**: High risk of extended downtime and user-facing regressions
- **Parallel run with dual writes**: Write conflicts, inconsistency risk, complex reconciliation
- **V3 only, no migration**: Ignores existing V2 production commitments

## Affected Components

- Feature flag system
- V2 adapters (read/write observation)
- Shadow comparison service
- All domain runtimes (migrated per domain)
- Deployment pipeline
- Monitoring and alerting

## Compliance Criteria

- All V3 features are behind feature flags, defaulting to off
- Each domain has a feature flag for independent activation
- Shadow mode produces comparison reports without production impact
- Migration threshold is defined per domain (accuracy, monitoring period)
- Rollback is verified for each domain before production activation

## References

- ADR-001: Project-Centric Architecture
- ADR-003: ProjectProfile as Source of Truth
- ADR-008: Evidence-Based Validation
