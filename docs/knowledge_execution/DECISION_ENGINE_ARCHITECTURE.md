# Decision Engine Architecture

**Component of:** Knowledge Execution Architecture (H1)
**Date:** 2026-07-15
**Status:** CANONICAL

---

## 1. Overview

The Decision Engine is the meta-orchestrator of the LAWIM execution pipeline. It sits between the Rule Resolver and the Domain Engines, consuming resolved rules and producing complete, traceable decisions with Next Best Action (NBA), explanation, audit trail, and fallback policy.

```
┌─────────────────────────────────────────────────────────────────┐
│                       DECISION ENGINE                           │
│                                                                 │
│  ┌─────────────────────┐  ┌───────────────────────────────┐   │
│  │ Knowledge Registry   │  │ Rule Registry                 │   │
│  │ ─ index all facts    │  │ ─ all rules indexed by domain │   │
│  │ ─ versioned models   │  │ ─ versioned + effective dates │   │
│  └──────────┬───────────┘  └──────────────┬────────────────┘   │
│             │                              │                    │
│             ▼                              ▼                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   Rule Resolver                          │   │
│  │  load → filter → evaluate → resolve conflicts → select  │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                           │                                     │
│                           ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Condition Evaluator                         │   │
│  │  evaluate(rule.conditions, context) → true/false        │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                           │                                     │
│                           ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Priority Resolver                           │   │
│  │  compute_priority(rule, context) → numeric score        │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                           │                                     │
│                           ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Conflict Resolver                           │   │
│  │  detect → classify → resolve (priority/specificity/     │   │
│  │  recency) → select winner                               │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                           │                                     │
│                           ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Decision Composer                           │   │
│  │  assemble decision record from resolved rule + context  │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                           │                                     │
│                           ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │           Next Best Action Resolver                      │   │
│  │  consume all domain scores → resolve priority →         │   │
│  │  select single NBA                                     │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                           │                                     │
│                           ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │           Decision Explanation Builder                   │   │
│  │  build human-readable explanation from resolved data    │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                           │                                     │
│                           ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │           Decision Audit Writer                          │   │
│  │  write immutable audit event for every decision         │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Component Specifications

### 2.1 Knowledge Registry

| Aspect | Detail |
|--------|--------|
| **Purpose** | Index, validate, version, and cache all Heritage Gold knowledge at startup |
| **Input** | Gold documents, model definitions, schema files |
| **Processing** | Parse → validate schema → assign version → build cross-reference graph → cache in memory |
| **Output** | `FactRegistry`, `ModelRegistry` — queryable interfaces |
| **Error states** | Schema validation failure → log + reject; version mismatch → reject with message; missing dependency → report graph gap |

### 2.2 Rule Registry

| Aspect | Detail |
|--------|--------|
| **Purpose** | Structured index of all Gold rules, versioned and queryable by domain, trigger, and effective date |
| **Input** | Heritage Gold `RULE_INDEX.md` + all domain-specific rule lists |
| **Processing** | Parse rules into `Rule` objects → index by domain → index by trigger event → index by effective date → validate dependencies |
| **Output** | `getRulesByDomain(domain): Rule[]`, `getRulesByTrigger(trigger): Rule[]`, `getRule(ruleId): Rule` |
| **Error states** | Rule not found → return null; circular dependency → throw `CircularDependencyError`; expired rule → return with `deprecated` flag |

### 2.3 Rule Resolver

| Aspect | Detail |
|--------|--------|
| **Purpose** | Given a context and domain, resolve the single winning rule from all applicable candidates |
| **Input** | `(context: Context, domain: Domain) → Rule[]` from Rule Registry |
| **Processing** | Load rules → filter by domain + trigger + state → evaluate conditions → resolve conflicts → select winner |
| **Output** | `ResolvedRule { selectedRule, candidates[], conflicts[], rejections[] }` |
| **Algorithm** | See `RULE_RESOLUTION_MODEL.md` for full algorithm |
| **Error states** | No rules match → `no_match` fallback; condition evaluation exception → reject with `evaluation_error`; conflict unresolvable → `conflict_escalation` |

### 2.4 Condition Evaluator

| Aspect | Detail |
|--------|--------|
| **Purpose** | Evaluate a rule's condition expression against the current context |
| **Input** | `(condition: ConditionExpression, context: Context) → boolean` |
| **Processing** | Parse condition AST → resolve operands (facts, state, scores) → evaluate operators → short-circuit composite conditions → return result |
| **Supported operators** | `eq`, `neq`, `gt`, `gte`, `lt`, `lte`, `in`, `not_in`, `contains`, `matches` (regex), `exists`, `and`, `or`, `not` |
| **Output** | `boolean` — true if condition matches, false otherwise |
| **Error states** | Unknown operator → return false + log warning; missing operand → return false + log; type mismatch → return false + log |

### 2.5 Priority Resolver

| Aspect | Detail |
|--------|--------|
| **Purpose** | Compute a numeric priority score for each matching rule to enable ordering and selection |
| **Input** | `(rule: Rule, context: Context) → number` |
| **Processing** | Base priority from rule definition → contextual modifiers (urgency, SLA, entity state) → dynamic boost (recency, specificity, domain weight) → clamp to [0, 1] |
| **Output** | `priorityScore: number` (higher = more urgent) |
| **Error states** | Priority overflow → clamp; missing modifier data → use default modifier (1.0) |

### 2.6 Conflict Resolver

| Aspect | Detail |
|--------|--------|
| **Purpose** | Detect and resolve conflicts between multiple matching rules |
| **Input** | `(candidates: Rule[]) → Resolution` |
| **Processing** | Detect overlaps → detect contradictions → detect circular dependencies → classify conflict type → apply resolution strategy → select winner |
| **Conflict types** | `overlap` (same condition, different actions), `contradiction` (opposite actions for same input), `circular` (A→B→A), `redundancy` (duplicate rules) |
| **Resolution strategies** | See Section 4 |
| **Output** | `Resolution { winner, rejected[], strategy_used, explanation }` |
| **Error states** | Unresolvable conflict → escalate with full conflict report |

### 2.7 Decision Composer

| Aspect | Detail |
|--------|--------|
| **Purpose** | Assemble the complete decision record from the resolved rule, context, and all intermediate data |
| **Input** | `(resolvedRule, context) → Decision` |
| **Processing** | Generate `decision_id` → stamp resolved rule → attach all candidates with rejection reasons → compute confidence → determine state transition → select response strategy → define business action → prepare NBA input |
| **Output** | `Decision` (see `DECISION_CONTRACT.md` for full schema) |
| **Error states** | Missing required field → fill with `unknown` + audit warning |

### 2.8 Next Best Action Resolver

| Aspect | Detail |
|--------|--------|
| **Purpose** | Consume all domain outputs and resolved rule to determine the single next best action |
| **Input** | `Decision` + all `domain_scores` from active domains |
| **Processing** | Score each candidate NBA → apply priority matrix → check blocking conditions → select single NBA → attach explanation |
| **Priority matrix** | See `GLOBAL_EXECUTION_ARCHITECTURE.md` §6 |
| **Output** | `NextAction { action, explanation, priority_score, triggering_rule, blocking_conditions[] }` |
| **Error states** | No NBA determinable → `no_action_required`; multiple NBAs tied → use priority score tiebreaker |

### 2.9 Decision Explanation Builder

| Aspect | Detail |
|--------|--------|
| **Purpose** | Build a human-readable, multi-language explanation of why this decision was made |
| **Input** | `Decision` with all resolved data |
| **Processing** | Select language template → insert selected rule name → insert rejection summaries → insert confidence → format for channel (short for WhatsApp, full for dashboard) |
| **Output** | `explanation: string` (localized, formatted) |
| **Error states** | Template not found → fallback to default language; missing variable → skip gracefully |

### 2.10 Decision Audit Writer

| Aspect | Detail |
|--------|--------|
| **Purpose** | Write an immutable, complete audit event for every decision cycle |
| **Input** | Full `Decision` + `EngineResult` + `ActionResult` |
| **Processing** | Compute audit hash → serialize full snapshot → write to audit store → emit `audit.recorded` event |
| **Output** | `AuditEvent { event_id, decision_id, timestamp, input_snapshot, decision_snapshot, outcome, hash }` |
| **Error states** | Audit store unavailable → buffer to local queue + retry; hash mismatch → log critical alert |

---

## 3. Rule Registry Structure

Each rule in the Registry follows this canonical structure:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `rule_id` | `string` | Yes | Unique identifier (e.g., `QUAL-002`, `MATCH-005`) |
| `domain` | `string` | Yes | Domain name (`qualification`, `matching`, `conversation`, etc.) |
| `knowledge_id` | `string` | Yes | Reference to Heritage Gold knowledge item (e.g., `GOLD-DM-021`) |
| `conditions` | `ConditionExpression` | Yes | The condition that must be true for this rule to fire |
| `priority` | `number` | Yes | Base priority (0.0–1.0) |
| `action` | `Action` | Yes | The business action to execute |
| `fallback` | `FallbackAction` | No | What to do if execution fails |
| `audit_template` | `string` | No | Template for audit log message |
| `version` | `string` | Yes | Semantic version of this rule |
| `effective_date` | `date` | Yes | Date from which this rule is active |
| `deprecation_date` | `date` | No | Date after which this rule is inactive |

### ConditionExpression

```json
{
  "operator": "and",
  "operands": [
    { "operator": "gte", "field": "qualification.score", "value": 80 },
    { "operator": "eq", "field": "intent.type", "value": "buy" },
    { "operator": "exists", "field": "facts.budget" }
  ]
}
```

### Action

```json
{
  "type": "call_immediately",
  "params": {
    "channel": "whatsapp",
    "template": "hot_lead_notification"
  },
  "target_engine": "conversation_engine"
}
```

---

## 4. Conflict Detection and Resolution Strategies

### 4.1 Conflict Types

| Type | Detection | Example |
|------|-----------|---------|
| **Overlap** | Same conditions trigger different actions | `score ≥ 80 → call_immediately` AND `score ≥ 80 → send_listings` |
| **Contradiction** | Same input produces opposite actions | `diaspora=true → apply_diaspora_boost` AND `diaspora=true → no_boost` |
| **Circular** | Rule A triggers Rule B which triggers Rule A | `lead.hot → qualify.urgent` AND `qualify.urgent → lead.hot` |
| **Redundancy** | Two rules with identical conditions and actions | Duplicate rules with different IDs |

### 4.2 Resolution Strategies

```
                    ┌─────────────────────────┐
                    │  Multiple rules match    │
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼─────────────┐
                    │  Is there a conflict?   │
                    └───────┬──────────┬──────┘
                            │          │
                       (yes)│          │(no) → select highest priority
                            ▼          │
              ┌─────────────────────┐   │
              │ Classify conflict   │   │
              └─────┬───────┬───────┘   │
                    │       │           │
              overlap│       │contradiction/circular
                    │       │           │
                    ▼       ▼           │
        ┌──────────────────────┐        │
        │ Priority-based       │        │
        │ → compare numeric    │        │
        │   priority scores    │        │
        │ → higher wins        │        │
        └──────────────────────┘        │
                    │                   │
                    ▼                   │
        ┌──────────────────────┐        │
        │ Specificity-based    │        │
        │ → compare condition  │        │
        │   specificity        │        │
        │ → more specific wins │        │
        └──────────────────────┘        │
                    │                   │
                    ▼                   │
        ┌──────────────────────┐        │
        │ Recency-based        │        │
        │ → compare version/   │        │
        │   effective date     │        │
        │ → newer wins         │        │
        └──────────────────────┘        │
                    │                   │
                    ▼                   ▼
        ┌──────────────────────────────────────┐
        │ If still tied → escalate to admin    │
        └──────────────────────────────────────┘
```

| Strategy | Algorithm | When to Use |
|----------|-----------|-------------|
| **Priority-based** | Compare `priority * contextual_modifier`. Higher wins. | Default strategy for overlap conflicts |
| **Specificity-based** | Count condition terms. More specific (more terms) wins. | When priorities are equal or within threshold (0.05) |
| **Recency-based** | Compare `effective_date` or `version`. Newer wins. | When priority and specificity are both tied |
| **Escalation** | Mark both as `conflict_escalation`, reject both, trigger admin alert. | All strategies exhausted |

### 4.3 Conflict Resolution Record

```json
{
  "conflict_id": "conflict_<uuid>",
  "type": "overlap",
  "rules_involved": ["QUAL-002", "QUAL-009"],
  "resolution_strategy": "priority",
  "winner": "QUAL-002",
  "explanation": "QUAL-002 (priority=0.85) beats QUAL-009 (priority=0.60) on base priority",
  "rejected": [
    { "rule_id": "QUAL-009", "reason": "lower_priority" }
  ]
}
```

---

## 5. Decision Composition and Explanation Building

### 5.1 Decision Composition Flow

```
ResolvedRule (from Rule Resolver)
        │
        ▼
Decision Composer:
  1. Generate decision_id ("dec_<uuid>")
  2. Assign selected_rule from ResolvedRule
  3. Attach all applicable_rules (all candidates that matched conditions)
  4. Attach rejected_rules with rejection reasons
  5. Compute confidence = selected_rule.priority * condition_match_confidence
  6. Determine state_transition from rule definition
  7. Select response_strategy from rule or context
  8. Define business_action from rule.action
  9. Build required_data list from missing context fields
  10. Prepare fallback_policy from rule.fallback or global default
```

### 5.2 Explanation Building

Templates by channel:
- **WhatsApp**: Short form (max 200 chars). E.g., "Based on your HOT lead score and interest in Douala, I'm prioritizing a call to discuss your search."
- **Dashboard**: Full form. E.g., "Decision dec_abc123: Rule QUAL-002 (HOT lead → call_immediately) selected. 2 rules matched, 1 rejected (QUAL-009: lower_priority 0.60 < 0.85). Confidence: 0.85."
- **API**: Structured JSON with both short and long explanations.

### 5.3 Confidence Computation

```
confidence = rule.base_priority
           * condition_match_confidence
           * data_completeness_factor
           * source_reliability_factor
```

Where:
- `condition_match_confidence` = 1.0 if all conditions evaluated successfully, 0.8 if partial data, 0.5 if inferred
- `data_completeness_factor` = ratio of required fields present to total required fields
- `source_reliability_factor` = from Heritage Gold confidence (HIGH=1.0, MEDIUM=0.8, LOW=0.5)

Threshold: if `confidence < 0.3`, the decision is marked as `low_confidence` and the fallback policy is activated.
