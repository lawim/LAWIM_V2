# Knowledge Execution Architecture — LAWIM

**Mission:** H1 — Knowledge Execution Layer
**Date:** 2026-07-15
**Status:** CANONICAL
**Prerequisite:** Heritage Gold (H0.4) — `docs/lawim_heritage_gold/`

---

## Purpose

The Knowledge Execution Architecture translates LAWIM's certified Heritage Gold knowledge into deterministic, traceable, auditable decisions and actions at runtime. It is the active layer between **what LAWIM knows** (Gold rules, models, facts) and **what LAWIM does** (respond, match, qualify, negotiate, notify, execute).

This directory defines the global execution pipeline, the decision engine, rule resolution model, and the input/output contracts that govern every business decision in LAWIM.

---

## How Heritage Gold Feeds Into Execution

```
Heritage Gold (certified rules + models)
        │
        ▼
Knowledge Registry (indexed, versioned, cacheable)
        │
        ▼
Rule Resolver (condition evaluation, priority resolution, conflict detection)
        │
        ▼
Decision Engine (compose decision, select NBA, build explanation)
        │
        ▼
Domain Engine (execute domain-specific logic: matching, qualification, etc.)
        │
        ▼
Action Executor (perform business action: send message, update state, emit event)
        │
        ▼
Audit and Learning (trace every decision, feed outcomes back)
```

---

## Architecture Overview

| Layer | Responsibility | Key Artifacts |
|-------|---------------|---------------|
| **Heritage Gold** | Certified knowledge repository | `docs/lawim_heritage_gold/` (all models, rule index, evidence) |
| **Knowledge Registry** | Index, load, validate, cache knowledge at startup | Rule Registry, Fact Registry, Model Registry |
| **Rule Resolver** | Evaluate conditions, resolve conflicts, select winning rule | Condition Evaluator, Priority Resolver, Conflict Resolver |
| **Decision Engine** | Compose full decision with explanation, audit, NBA | Decision Composer, NBA Resolver, Explanation Builder |
| **Domain Engine** | Execute domain-specific processing (17 engines) | Workflow, Conversation, Matching, Qualification, etc. |
| **Action Executor** | Perform the decided business action | Message Sender, State Updater, Event Emitter |
| **Audit and Learning** | Record every decision, outcome, and exception | Decision Audit Writer, Feedback Collector, Learning Feed |

---

## File Index

| File | Content |
|------|---------|
| `README.md` | Entry point, purpose, architecture overview, principles |
| `GLOBAL_EXECUTION_ARCHITECTURE.md` | Complete pipeline definition, NBA Engine, 17 engines mapping |
| `DECISION_ENGINE_ARCHITECTURE.md` | Decision Engine component design, algorithms, error states |
| `DECISION_CONTRACT.md` | Formal input/output contracts for every decision |
| `RULE_RESOLUTION_MODEL.md` | Rule structure, loading lifecycle, condition evaluation, conflict resolution |

---

## Key Principles

### Deterministic Execution
Given the same input state + the same set of Gold rules, the execution pipeline MUST always produce the same decision. No randomness, no LLM fallback for business logic, no hidden conditions.

### No Silent Rules
Every rule that matches MUST be recorded. Every rule that is rejected MUST record why. No rule executes without being traced. This enables full explainability and audit.

### Traceability
Every decision produces an immutable audit record containing: input state snapshot, all applicable rules, the selected rule with reason, all rejected rules with rejection reasons, the computed next action, and the execution outcome. Traceability is a first-class output, not an afterthought.

### Contract-First
All cross-component interaction uses explicit, versioned contracts. No component reaches into another's internal state. The `DECISION_CONTRACT.md` is the single source of truth for input/output shapes.

### Fail Closed, Not Silent
If a decision cannot be resolved (no rule matches, conflict cannot be resolved, data is missing), the engine MUST produce a fallback decision — never silently skip, never guess, never hang.

---

## References

- Heritage Gold: `docs/lawim_heritage_gold/` (H0.4 Certified, 2026-07-15)
- Rule Index: `docs/lawim_heritage_gold/RULE_INDEX.md` (99+ certified rules)
- Domain Model: `docs/lawim_heritage_gold/DOMAIN_MODEL.md` (17 engines, 7 property families)
- Canonical Architecture: `docs/canonical/` (domain boundaries, principles)
- ADR: `docs/adr/` (architecture decisions)
