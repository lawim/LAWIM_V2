# Global Execution Architecture

**Component of:** Knowledge Execution Architecture (H1)
**Date:** 2026-07-15
**Status:** CANONICAL

---

## 1. Complete Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      HERITAGE GOLD (H0.4 Certified)                        │
│  docs/lawim_heritage_gold/ — 99+ rules, 12 domains, 17 engines, all models │
└────────────────────┬────────────────────────────────────────────────────────┘
                     │ load, validate, index
                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         KNOWLEDGE REGISTRY                                 │
│  • Rule Registry     • Fact Registry     • Model Registry                  │
│  • Versioned cache   • Dependency graph   • Effective date index           │
└────────────────────┬────────────────────────────────────────────────────────┘
                     │ get_applicable_rules(context)
                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           RULE RESOLVER                                    │
│  • Load rules for domain      • Evaluate conditions                        │
│  • Filter by context          • Resolve priorities                         │
│  • Detect conflicts           • Select winner                              │
└────────────────────┬────────────────────────────────────────────────────────┘
                     │ resolved_rule + all_candidates + conflicts
                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DECISION ENGINE                                  │
│  • Compose decision        • Compute confidence                            │
│  • Resolve NBA             • Build explanation                             │
│  • Detect gaps             • Write audit events                            │
└────────────────────┬────────────────────────────────────────────────────────┘
                     │ decision with NBA
                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DOMAIN ENGINE                                    │
│  • Workflow Engine    • Conversation Engine    • Qualification Engine      │
│  • Matching Engine    • Rematching Engine      • Geo Engine                │
│  • Notification Engine• Dashboard Engine       • Role Engine               │
│  • Reporting Engine   • Security Engine        • LAWIM AI                  │
│  • Continuous Learning• Campay Payment Engine  • Storage Lifecycle Mgr     │
│  • API Gateway        • Administration Engine                              │
└────────────────────┬────────────────────────────────────────────────────────┘
                     │ business_action + response_strategy
                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ACTION EXECUTOR                                   │
│  • Send message (channel)   • Update state   • Emit event                  │
│  • Create resource          • Trigger workflow transition                  │
│  • Log action result                                                       │
└────────────────────┬────────────────────────────────────────────────────────┘
                     │ outcome + metrics
                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        AUDIT AND LEARNING                                  │
│  • Decision Audit Writer   • Feedback Collector                            │
│  • Outcome Tracker         • Learning Feed → Heritage Gold update          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Layer Specifications

### 2.1 Heritage Gold

| Aspect | Detail |
|--------|--------|
| **Input** | Raw source files (Directive, JSON, Python, SQL), validated Gold documents |
| **Processing** | Cross-validation, confidence rating, source tracing, contradiction resolution |
| **Output** | Certified rule index (`RULE_INDEX.md`), domain models, knowledge glossary |
| **Contract** | `docs/lawim_heritage_gold/` — read-only reference, versioned by H-tag |
| **Owner** | Knowledge Recovery mission (H0 series) |

### 2.2 Knowledge Registry

| Aspect | Detail |
|--------|--------|
| **Input** | Heritage Gold documents, runtime schema definitions, entity metadata |
| **Processing** | Parse rules into structured objects → validate schema → build dependency graph → index by domain/entity/trigger → cache |
| **Output** | `RuleRegistry`, `FactRegistry`, `ModelRegistry` — queryable, cacheable registries |
| **Contract** | `getRules(domain, trigger) → Rule[]`, `getFacts(entityId) → Fact[]`, `getModel(modelName) → Model` |
| **Error states** | Registry unloaded → return empty set; version mismatch → reject and log; circular dependency → fail with graph report |

### 2.3 Rule Resolver

| Aspect | Detail |
|--------|--------|
| **Input** | Current context (actor, intent, project, dossier, facts, state, channel, history), applicable rules from Registry |
| **Processing** | Load rules for matching domains → filter by trigger + state → evaluate condition expressions → compute priority scores → detect conflicts (overlap, contradiction, circular) → resolve conflicts (priority/specificity/recency) → select winning rule |
| **Output** | `ResolvedRule { selectedRule, candidates[], conflicts[], rejections[] }` |
| **Contract** | `resolve(context, domain) → ResolvedRule` |
| **Error states** | No rules match → return explicit `no_match` fallback; unresolvable conflict → return `conflict_escalation` with details; condition evaluation error → reject rule with `evaluation_error` reason |

### 2.4 Decision Engine

| Aspect | Detail |
|--------|--------|
| **Input** | `ResolvedRule` from Rule Resolver + full context |
| **Processing** | Compose decision record → compute confidence → resolve NBA (Next Best Action) from all domain outputs → build human-readable explanation → identify required data gaps → determine state transition → select response strategy → define business action → generate audit events |
| **Output** | `Decision { decision_id, selected_rule, rejected_rules, reason, next_action, required_data, state_transition, response_strategy, business_action, audit_events, confidence, fallback_policy }` |
| **Contract** | `decide(context, resolvedRule) → Decision` |
| **Error states** | Confidence below threshold → enforce fallback; gap in required data → set `required_data` and return `awaiting_data` NBA; NBA resolution conflict → escalate |

### 2.5 Domain Engine

| Aspect | Detail |
|--------|--------|
| **Input** | `Decision` with `business_action` + `response_strategy` |
| **Processing** | Route to target engine → execute engine-specific logic (e.g., Matching Engine runs score/rank, Conversation Engine builds message, Workflow Engine applies state transition) → return engine result |
| **Output** | `EngineResult { success, output_data, events[], metrics }` |
| **Contract** | `execute(businessAction, decision) → EngineResult` |
| **Error states** | Engine unavailable → return `execution_failure` with fallback; engine timeout → return `timeout`; validation error → return `validation_failure` |

### 2.6 Action Executor

| Aspect | Detail |
|--------|--------|
| **Input** | `EngineResult` with concrete action payload |
| **Processing** | Format for target channel → validate permissions → execute action (send message, update DB, emit event) → record result |
| **Output** | `ActionResult { success, channel_response, error?, timestamp }` |
| **Contract** | `executeAction(actionPayload, channel) → ActionResult` |
| **Error states** | Channel unreachable → retry with backoff (max 3); permission denied → return `authorization_failure`; payload invalid → return `validation_failure` |

### 2.7 Audit and Learning

| Aspect | Detail |
|--------|--------|
| **Input** | Full `Decision` + `EngineResult` + `ActionResult` |
| **Processing** | Write immutable audit event → track outcome against predicted confidence → detect pattern deviations → feed outcome back to Heritage Gold confidence recalibration |
| **Output** | `AuditEvent` (persisted), learning signal to Knowledge Registry |
| **Contract** | `audit(decision, result) → AuditEvent` |
| **Error states** | Audit store unavailable → buffer and retry (never fail the main flow for audit) |

---

## 3. Data Flow Between Components

```
                                Context (actor, intent, state, facts, ...)
                                        │
                                        ▼
[Knowledge Registry] ◄──── [Heritage Gold]
        │
        │ rules
        ▼
[Rule Resolver] ───► candidates, conflicts, selected
        │
        ▼
[Decision Engine] ──► decision_id, reason, NBA, confidence
        │
        ▼
[Domain Engine] ───► engine-specific output
        │
        ▼
[Action Executor] ──► action result
        │
        ▼
[Audit & Learning] ──► audit event, learning signal ──► [Knowledge Registry]
```

### Data flow invariants

1. **Context is immutable** during a single decision cycle. No component modifies the context.
2. **Each layer enriches** the flow with structured output; no layer skips.
3. **Failures are explicit** — every layer produces a valid structured output even on error.
4. **Audit events cover the full chain** — one `decision_id` traces through all layers.

---

## 4. Event Propagation Model

| Event Type | Emitter | Consumers | Delivery |
|-----------|---------|-----------|----------|
| `decision.made` | Decision Engine | Domain Engine, Audit | Synchronous |
| `rule.matched` | Rule Resolver | Decision Engine, Audit | Synchronous |
| `rule.conflict` | Rule Resolver | Decision Engine, Audit, Admin alert | Synchronous + async notification |
| `domain.action.required` | Domain Engine | Action Executor | Synchronous |
| `action.executed` | Action Executor | Audit, Learning | Synchronous |
| `action.failed` | Action Executor | Audit, Learning, Fallback handler | Synchronous |
| `audit.recorded` | Audit | Learning, Admin dashboard | Async |
| `learning.signal` | Learning | Knowledge Registry (confidence update) | Async, scheduled batch |

### Event schema

```json
{
  "event_id": "evt_<uuid>",
  "type": "decision.made",
  "decision_id": "dec_<uuid>",
  "source": "decision_engine",
  "timestamp": "2026-07-15T12:00:00Z",
  "payload": { /* type-specific data */ },
  "parent_id": null
}
```

---

## 5. Error Handling Philosophy

| Principle | Rule |
|-----------|------|
| **Fail closed** | Never silently skip. If resolution fails, return explicit fallback. |
| **No silent swallows** | Every error produces a structured error event in the audit trail. |
| **Fallback chain** | Primary path → degraded path → safe fallback → escalate. |
| **Retry with backoff** | Transient failures (network, channel) retry 3x with exponential backoff. |
| **Circuit breaker** | After 5 consecutive failures in any layer, open circuit and escalate. |
| **Audit survives** | Audit writes are buffered; audit failure never blocks the main flow. |

### Fallback hierarchy

```
1. Primary rule match → execute selected rule
2. Partial match → execute best-effort with reduced confidence
3. No match → execute domain default rule (if exists)
4. No default → execute global fallback policy
5. Global fallback fails → escalate to human (admin dashboard alert)
```

---

## 6. NBA (Next Best Action) Engine

### Purpose

The NBA Engine consumes all domain rule outputs to determine the single next best action for any entity at any state. It answers: **given where the entity is now and what we know, what should happen next?**

### Input

```json
{
  "entity_id": "user_<uuid>",
  "entity_type": "user|lead|project|dossier",
  "current_state": "qualifying|matching|negotiating|closing|inactive",
  "domain_scores": {
    "qualification": { "score": 85, "tier": "HOT" },
    "matching": { "score": 72, "matches_available": true },
    "conversation": { "last_interaction": "2026-07-14T18:00:00Z", "follow_up_due": false },
    "relationship": { "consent_granted": true },
    "commercial": { "visit_scheduled": false, "offer_pending": false }
  },
  "time_context": { "current_hour": 14, "sla_status": "within_sla" },
  "history": ["qualification.completed", "matching.search.performed"]
}
```

### Processing

```
1. Receive current state + all domain scores
2. Resolve priorities (urgency vs. dependency vs. SLA)
3. Check blocking conditions (missing consent, missing data, spam flag)
4. Compute NBA candidates from each domain
5. Select single NBA using priority matrix
6. Output next_action with explanation
```

### Priority Matrix

| Current State | Priority Domain | Next Action |
|--------------|----------------|-------------|
| `incoming` | Qualification | `qualify.initial` |
| `qualifying` | Qualification | `qualify.continue` |
| `qualified` | Matching | `search.match` |
| `matched` | Relationship | `relationship.introduce` |
| `introduced` | Commercial | `commercial.schedule_visit` |
| `visit_done` | Commercial | `commercial.follow_up` |
| `negotiating` | Negotiation | `negotiation.respond` |
| `closing` | Transaction | `transaction.guidance` |
| `inactive` | Conversation | `conversation.reengagement` |
| `blocked` | Security | `security.review` |

### Output

```json
{
  "next_action": "qualify.continue",
  "explanation": "Lead scored 85 (HOT) but missing budget. Continue qualification to collect budget before matching.",
  "priority_score": 0.92,
  "triggering_rule": "QUAL-002",
  "blocking_conditions": ["missing_budget"],
  "time_sensitivity": "normal"
}
```

### NBA Engine contract

| Aspect | Detail |
|--------|--------|
| **Input** | Current state + all domain scores + history + time context |
| **Processing** | Priority resolution → blocking check → candidate evaluation → single selection |
| **Output** | Single `next_action` with `explanation`, `priority_score`, `triggering_rule` |
| **Error state** | Cannot determine NBA → return `no_action_required` with reason |
| **Invariant** | NBA Engine ALWAYS outputs exactly one next_action (even if `no_action_required`) |

> **ARCHITECTURE_DECISION:** NBA priority matrix values (HIGH/MEDIUM/LOW) are architecture-defined default weights. They may be refined during implementation based on business performance data.

---

## 7. 17 Engines Mapping to Execution Layers

| # | Engine | Layer | Domain | Primary Responsibility |
|---|--------|-------|--------|----------------------|
| 1 | Workflow Engine | Domain Engine | Core | Orchestrate states, transitions, business events |
| 2 | Conversation Engine | Domain Engine | Conversation | Understand needs, manage dialogue, build messages |
| 3 | Qualification Engine | Domain Engine | Qualification | Transform free text into structured real estate data |
| 4 | Matching Engine | Domain Engine | Matching | Score and rank properties against needs |
| 5 | Rematching Engine | Domain Engine | Matching | Re-match after failed proposals (never from zero) |
| 6 | Dashboard Engine | Domain Engine | Admin | Display contextualized indicators and alerts |
| 7 | Notification Engine | Action Executor | Notifications | Diffuse alerts and notifications across channels |
| 8 | Geo Engine | Domain Engine | Geography | Normalize locations, calculate proximity, GPS scoring |
| 9 | Role Engine | Knowledge Registry | CRM | Manage identities, roles, permissions, organizations |
| 10 | Reporting Engine | Domain Engine | Admin | Calculate KPIs and generate official reports |
| 11 | Storage Lifecycle Manager | Domain Engine | Infrastructure | Organize storage, archiving, backup, restoration |
| 12 | Security Engine | Domain Engine | Security | Protect access, detect fraud, enforce consent |
| 13 | API Gateway | Action Executor | Infrastructure | Official entry point for all LAWIM APIs |
| 14 | Administration Engine | Domain Engine | Admin | Supervision, validation, internal administration |
| 15 | LAWIM AI | Domain Engine | AI | Recommendations, summaries, analysis (linguistic only) |
| 16 | Continuous Learning Engine | Audit & Learning | Learning | Prepare monthly human-validated learnings |
| 17 | Campay Payment Engine | Action Executor | Payments | Mobile Money payment module via Campay |

### Decision Engine is NOT in this list

The Decision Engine is the **mete-engine** that orchestrates all 17 engines. It is not a domain engine itself. It sits between the Rule Resolver and the Domain Engines, consuming resolved rules and producing decisions that tell each domain engine what to do.

```
                    ┌──────────────────────┐
                    │   Decision Engine     │ (meta-orchestrator)
                    └──────────┬───────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         ▼                     ▼                     ▼
   ┌──────────┐         ┌──────────┐         ┌──────────┐
   │Workflow  │         │Matching  │         │Qualif.   │  ... 17 engines
   │Engine    │         │Engine    │         │Engine    │
   └──────────┘         └──────────┘         └──────────┘
```
