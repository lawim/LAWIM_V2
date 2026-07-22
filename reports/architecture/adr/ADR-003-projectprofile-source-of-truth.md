# ADR-003: ProjectProfile as Source of Truth

**Status:** Accepted
**Date:** 2026-07-22

## Context

Multiple components store overlapping business data, leading to inconsistencies. Conversation state holds extracted criteria. Case records hold business status. User profiles hold preferences. These stores drift apart over time, making it unclear which source is authoritative for any given piece of data.

## Decision

ProjectProfile is the SINGLE source of truth for all project business data. All V2 data stores are adapted to read from and write to ProjectProfile. The ProjectProfile schema is the canonical business schema; all other stores derive from it.

## Justification

Consistency is impossible with multiple authoritative sources. A single source of truth eliminates drift. The V2-to-V3 migration path becomes a data mapping exercise rather than a reconciliation nightmare. A single update point reduces bugs and audit complexity.

## Positive Consequences

- Business data is always consistent across components
- V2 stores can be migrated incrementally via adapters
- Audit trail is centralized on ProjectProfile changes
- Schema changes require one authoritative change point

## Negative Consequences

- ProjectProfile becomes a bottleneck if not optimized
- Adapter layer adds maintenance cost during migration period
- Legacy V2 code must be wrapped rather than rewritten

## Rejected Alternatives

- **Multiple authoritative stores**: Current state; causes the inconsistency problem
- **Eventual consistency with sync jobs**: Complex, failure-prone, no single source of truth
- **Database-level consolidation only**: Ignores in-memory and cache inconsistencies

## Affected Components

- ProjectProfileService
- ConversationStateRepository
- CaseRepository
- All V2 data stores
- Migration adapters

## Compliance Criteria

- Every business data read goes through ProjectProfile or a documented derived view
- Every business data write goes through ProjectProfile
- No V2 store accepts direct writes bypassing ProjectProfile
- An audit query can reconstruct any business state from ProjectProfile history alone

## References

- ADR-001: Project-Centric Architecture
- ADR-007: V2->V3 Shadow Migration
