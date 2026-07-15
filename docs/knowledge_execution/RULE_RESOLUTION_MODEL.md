# Rule Resolution Model

**Component of:** Knowledge Execution Architecture (H1)
**Date:** 2026-07-15
**Status:** CANONICAL

---

## 1. Rule Structure

Every business rule in LAWIM is defined by this canonical structure:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | `string` | Yes | — | Unique rule identifier (e.g., `QUAL-002`, `MATCH-005`, `CONV-010`) |
| `domain` | `string` | Yes | — | Domain name: `qualification`, `matching`, `conversation`, `geography`, `crm`, `negotiation`, `language`, `security`, `property`, `constitution` |
| `knowledge_id` | `string` | Yes | — | Reference to Heritage Gold knowledge item (e.g., `GOLD-DM-021`) |
| `condition_expression` | `ConditionExpression` | Yes | — | Expression tree that must evaluate to `true` for the rule to fire |
| `priority` | `number` | Yes | `0.5` | Base priority (0.0–1.0). Higher = more urgent. |
| `action` | `Action` | Yes | — | The business action to execute when the rule fires |
| `fallback` | `FallbackAction` | No | `null` | What to do if execution of `action` fails |
| `audit_template` | `string` | No | `""` | Template for the audit log, with `{field}` placeholders |
| `version` | `string` | Yes | `"1.0"` | Semantic version (MAJOR.MINOR) |
| `effective_date` | `date` | Yes | — | ISO 8601 date from which this rule is active |
| `deprecation_date` | `date` | No | `null` | ISO 8601 date after which this rule is inactive |
| `tags` | `string[]` | No | `[]` | Tags for grouping and filtering |
| `owner` | `string` | No | `"system"` | Entity responsible for this rule |

### Rule example (resolved in memory)

```json
{
  "id": "QUAL-002",
  "domain": "qualification",
  "knowledge_id": "GOLD-DM-020",
  "condition_expression": {
    "operator": "and",
    "operands": [
      { "operator": "gte", "field": "qualification.score", "value": 80 },
      { "operator": "eq", "field": "actor.role", "value": "buyer" },
      { "operator": "exists", "field": "facts.city" }
    ]
  },
  "priority": 0.85,
  "action": {
    "type": "call_immediately",
    "params": { "template": "hot_lead_notification" },
    "target_engine": "conversation_engine"
  },
  "fallback": {
    "type": "send_listings",
    "params": { "max_results": 5 }
  },
  "audit_template": "Rule {rule_id} matched for lead {lead_id}: score={score}, action={action_type}",
  "version": "1.0",
  "effective_date": "2026-06-01",
  "deprecation_date": null,
  "tags": ["lead_scoring", "hot"],
  "owner": "domain_qualification"
}
```

### ConditionExpression

```json
{
  "operator": "and|or|not|eq|neq|gt|gte|lt|lte|in|not_in|contains|matches|exists",
  "field": "context.path.to.field",
  "value": "any|number|string|boolean|array",
  "operands": [ "ConditionExpression[] (for and/or/not)" ]
}
```

### Action

```json
{
  "type": "call_immediately|send_listings|request_budget|follow_up|ignore|notify_agent|transition_state|...",
  "params": { "key": "value" },
  "target_engine": "conversation_engine|workflow_engine|matching_engine|notification_engine|..."
}
```

### FallbackAction

```json
{
  "type": "retry|degrade|default_action|escalate",
  "params": {},
  "max_retries": 3,
  "escalation_target": "admin_dashboard"
}
```

---

## 2. Rule Loading Lifecycle

```
┌──────────┐   load    ┌──────────┐  validate  ┌──────────┐  index   ┌──────────┐  cache   ┌──────────┐
│  Source   │ ────────→ │  Parser  │ ─────────→ │  Schema  │ ───────→ │  Indexer │ ───────→ │  Cache   │
│  (Gold)   │           │          │            │ Checker  │          │          │          │          │
└──────────┘           └──────────┘            └──────────┘          └──────────┘          └──────────┘
                                                                                               │
                                                                                               ▼
                                                                                        ┌──────────┐
                                                                                        │ Resolver │
                                                                                        │ (runtime)│
                                                                                        └──────────┘
```

### Phase 1: Load

- Read rules from Heritage Gold sources (`docs/lawim_heritage_gold/RULE_INDEX.md` + domain-specific rule files)
- Parse into structured `Rule` objects

### Phase 2: Validate

| Check | Rule | Failure Action |
|-------|------|---------------|
| Schema conformance | All required fields present | Reject rule with error report |
| Type correctness | Field types match schema | Reject with type error |
| Domain existence | Domain is registered | Reject with `unknown_domain` |
| Action existence | `action.type` is a known action | Reject with `unknown_action` |
| Condition validity | Condition tree is well-formed | Reject with `malformed_condition` |
| Priority range | `0.0 ≤ priority ≤ 1.0` | Clamp to [0, 1] |

### Phase 3: Index

Build the following indices for O(1) rule lookup at runtime:

- **Domain index**: `domain → Rule[]` (primary lookup)
- **Trigger index**: `trigger_event → Rule[]` (event-driven lookup)
- **State index**: `workflow_state → Rule[]` (state-driven lookup)
- **Tag index**: `tag → Rule[]` (for filtering)
- **Effective date index**: `date → Rule[]` (temporal validity)

### Phase 4: Cache

- Store validated, indexed rules in memory
- Cache key: `{domain, trigger, state}`
- Cache invalidation: on rule change (version bump) or scheduled reload (every 5 minutes, configurable)
- Cache entry: `{ rules[], loaded_at, version_hash }`

### Phase 5: Resolve

- Called once per decision cycle
- Input: `(context, domain)` or `(context, trigger)`
- Output: `ResolvedRule`
- Full algorithm in Section 4

---

## 3. Condition Evaluation

### 3.1 Supported Operators

| Operator | Type | Description | Example |
|----------|------|-------------|---------|
| `eq` | Comparison | Field equals value | `field: "intent.type", value: "buy"` |
| `neq` | Comparison | Field does not equal value | `field: "actor.role", value: "spammer"` |
| `gt` | Comparison | Field greater than value | `field: "qualification.score", value: 80` |
| `gte` | Comparison | Field greater than or equal | `field: "facts.budget", value: 50000000` |
| `lt` | Comparison | Field less than value | `field: "time_context.sla_remaining", value: 3600` |
| `lte` | Comparison | Field less than or equal | `field: "match.score", value: 60` |
| `in` | Set membership | Field value in array | `field: "intent.type", value: ["buy", "rent"]` |
| `not_in` | Set exclusion | Field value not in array | `field: "actor.role", value: ["blocked", "spammer"]` |
| `contains` | String contains | Field contains substring | `field: "facts.city", value: "Douala"` |
| `matches` | Regex | Field matches regex pattern | `field: "facts.phone", value: "^237[0-9]{9}$"` |
| `exists` | Existence | Field is present and non-null | `field: "facts.budget"` |
| `and` | Logical AND | All operands must be true | `operands: [cond1, cond2, cond3]` |
| `or` | Logical OR | At least one operand true | `operands: [cond1, cond2]` |
| `not` | Logical NOT | Negates inner condition | `operands: [cond]` |

### 3.2 Supported Data Types

| Type | Examples | Operators |
|------|----------|-----------|
| `string` | `"Douala"`, `"buy"`, `"hot"` | `eq`, `neq`, `in`, `not_in`, `contains`, `matches` |
| `number` | `85`, `50000000`, `0.75` | `eq`, `neq`, `gt`, `gte`, `lt`, `lte`, `in`, `not_in` |
| `boolean` | `true`, `false` | `eq`, `neq` |
| `array` | `["buy", "rent"]`, `[1, 2, 3]` | `in`, `not_in`, `contains` |
| `null` | `null` | `exists` (returns false) |

### 3.3 Composite Conditions

Composite conditions use `and`, `or`, and `not` operators to build expression trees of arbitrary depth.

**Example: HOT lead with diaspora + city match**

```json
{
  "operator": "and",
  "operands": [
    { "operator": "gte", "field": "qualification.score", "value": 80 },
    {
      "operator": "or",
      "operands": [
        { "operator": "eq", "field": "facts.diaspora", "value": true },
        { "operator": "eq", "field": "facts.urgency", "value": "high" }
      ]
    },
    { "operator": "exists", "field": "facts.city" }
  ]
}
```

### 3.4 Short-Circuit Evaluation

Composite conditions use short-circuit evaluation:

| Operator | Short-circuit behavior |
|----------|----------------------|
| `and` | Returns `false` on first `false` operand; remaining operands are NOT evaluated |
| `or` | Returns `true` on first `true` operand; remaining operands are NOT evaluated |
| `not` | Always evaluates the single operand (no short-circuit possible) |

Short-circuit is critical when:
- Later conditions depend on fields that may not exist
- Later conditions are expensive (e.g., regex matching, cross-entity lookups)
- A condition has side effects (audit logging of matched fields)

---

## 4. Rule Resolver Algorithm

### Full Algorithm

```
FUNCTION resolve(context, domain) → ResolvedRule

  1. LOAD rules = RuleRegistry.getRulesByDomain(domain)
  2. FILTER rules = rules WHERE is_effective(rules, context.time_context.current_time)
  3. FILTER rules = rules WHERE matches_trigger(rules, context)
  4. FILTER rules = rules WHERE matches_state(rules, context.state.current_workflow, context.state.current_step)

  5. candidates = []
  6. FOR EACH rule IN filtered_rules:
       condition_result = ConditionEvaluator.evaluate(rule.condition_expression, context)
       IF condition_result == true:
         priority_score = PriorityResolver.compute(rule, context)
         candidates.append({ rule, priority_score, evaluation_status: "matched" })
       ELSE:
         rejections.append({ rule, reason: "condition_false", details: condition_result.debug_info })

  7. IF candidates IS EMPTY:
       RETURN no_match_fallback(context, domain)

  8. SORT candidates BY priority_score DESC

  9. conflicts = ConflictResolver.detect(candidates)
  10. IF conflicts IS NOT EMPTY:
        resolution = ConflictResolver.resolve(conflicts, candidates, context)
        selected = resolution.winner
        FOR EACH rejected IN resolution.rejected:
          rejections.append({ rule: rejected.rule, reason: rejected.reason, resolution: resolution })
      ELSE:
        selected = candidates[0]
        FOR EACH rejected IN candidates[1:]:
          rejections.append({ rule: rejected.rule, reason: "lower_priority" })

  11. RETURN ResolvedRule {
        selectedRule: selected.rule,
        candidates: candidates,
        conflicts: conflicts,
        rejections: rejections
      }
```

### Algorithm invariants

1. **Every rule with true conditions is a candidate** — no early cutoff.
2. **Every candidate gets a priority score** — no unranked rules.
3. **Conflicts must be explicitly resolved** — ties are not allowed.
4. **Fallback is always available** — `no_match_fallback` exists for every domain.

---

## 5. Conflict Detection

### 5.1 Overlapping Conditions

Detected when two or more rules have condition expressions that evaluate `true` for the same context, but produce different actions.

**Detection algorithm:**
```
FOR EACH pair (r1, r2) IN candidates:
  IF r1.condition_expression IS semantically_equal TO r2.condition_expression
    AND r1.action.type != r2.action.type:
      REPORT overlap(r1, r2)
```

### 5.2 Contradictory Actions

Detected when two rules match the same context and produce logically opposite actions.

**Detection algorithm:**
```
CONTRADICTION_MAP = {
  "call_immediately": "ignore",
  "apply_boost": "no_boost",
  "send_listings": "do_not_send",
  "request_budget": "skip_budget"
}

FOR EACH pair (r1, r2) IN candidates:
  IF r1.action.type == CONTRADICTION_MAP[r2.action.type]:
    REPORT contradiction(r1, r2)
```

### 5.3 Circular Dependencies

Detected when rule A's action triggers a state that makes rule B fire, and rule B's action triggers a state that makes rule A fire again (infinite loop risk).

**Detection algorithm:**
```
BUILD dependency_graph FROM rules:
  FOR EACH rule:
    IF rule.action.target_engine == "workflow_engine"
      AND rule.action.params contains "state_transition":
        ADD edge(rule.id → target_state.rules)

RUN cycle_detection(dependency_graph)
IF cycle found:
  REPORT circular(critical: cycle, rules: cycle_nodes)
```

### 5.4 Conflict Report Format

```json
{
  "conflict_id": "conflict_<uuid>",
  "type": "overlap|contradiction|circular",
  "severity": "info|warning|critical",
  "rules_involved": ["QUAL-002", "QUAL-009"],
  "shared_conditions": [
    { "operator": "gte", "field": "qualification.score", "value": 80 }
  ],
  "different_actions": [
    { "rule": "QUAL-002", "action": "call_immediately" },
    { "rule": "QUAL-009", "action": "send_listings" }
  ]
}
```

---

## 6. Resolution Strategies — Decision Tree

```
                    ┌──────────────────────────────┐
                    │    Multiple rules match       │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │  Any conflicts detected?      │
                    └──────┬──────────────┬────────┘
                           │              │
                        (yes)           (no) ──► Select highest priority
                           │
              ┌────────────▼────────────┐
              │  Conflict classification │
              └──────┬──────────┬───────┘
                     │          │
              ┌──────▼──┐  ┌───▼────────┐
              │ Overlap │  │ Contradict │  ┌───────────┐
              └──────┬──┘  │ or Circular│  │ Redundant │
                     │     └───┬────────┘  └─────┬─────┘
                     │         │                  │
          ┌──────────▼──┐  ┌───▼────────┐  ┌─────▼─────┐
          │ priority >  │  │ specificity│  │ Keep first │
          │ 0.05 gap?   │  │ diff > 0?  │  │ (by version│
          └──┬───────┬──┘  └──┬──────┬──┘  │ or ID)    │
             │      │         │      │     └───────────┘
          (yes)   (no)      (yes)  (no)
             │      │         │      │
             ▼      ▼         ▼      ▼
       ┌────────┐ ┌────────┐ ┌────┐ ┌────────┐
       │ Higher │ │ Specif │ │ More│ │ Recency │
       │ prio   │ │ check  │ │ spec│ │ check   │
       │ wins   │ │        │ │ wins│ │         │
       └────────┘ └───┬────┘ └────┘ └───┬────┘
                      │                  │
                   (tie)              (tie)
                      │                  │
                      └──────┬───────────┘
                             │
                  ┌──────────▼──────────┐
                  │  All strategies      │
                  │  exhausted →         │
                  │  ESCALATE            │
                  └─────────────────────┘
```

### Resolution Strategy Details

| Strategy | Rule | Example |
|----------|------|---------|
| **Priority-based** | Compare `priority * contextual_modifier`. Winner MUST exceed loser by at least `0.05`. If gap < 0.05, fall through to specificity. | `QUAL-002` (0.85) vs `QUAL-009` (0.60) → `QUAL-002` wins (gap 0.25 > 0.05) |
| **Specificity-based** | Count total atomic condition terms across the expression tree. More terms = more specific. Max depth also considered. | Rule A: `score > 80 AND intent == buy AND city exists` (3 terms) beats Rule B: `score > 80` (1 term) |
| **Recency-based** | Compare `effective_date`. Newer wins. If same, compare `version` (semver). Newer wins. | `QUAL-002 v1.0` (2026-06-01) vs `QUAL-002 v2.0` (2026-07-01) → v2.0 wins |
| **Escalation** | All strategies exhausted. Both rules marked as `unresolved_conflict`. Decision falls back to `escalation` policy. Admin alert triggered. | Report generated with full conflict details sent to admin dashboard |

---

## 7. Rule Versioning and Deprecation

### 7.1 Version Scheme

```
v{MAJOR}.{MINOR}
- MAJOR: Breaking change (condition changed, action changed, priority changed by > 0.2)
- MINOR: Non-breaking change (metadata update, audit template change, priority change ≤ 0.2)
```

### 7.2 Deprecation Lifecycle

```
┌──────────┐   effective_date   ┌──────────┐  deprecation_date  ┌────────────┐  removal_date  ┌────────┐
│  DRAFT   │ ───────────────→ │  ACTIVE  │ ─────────────────→ │ DEPRECATED │ ─────────────→ │ REMOVED│
│ (not in  │                  │ (in cache,│                   │ (in cache, │                │ (purged│
│  cache)  │                  │  resolves)│                   │  warns on  │                │  from  │
└──────────┘                  └──────────┘                   │  resolve)  │                │ cache) │
                                                              └────────────┘                └────────┘
```

| Phase | Behavior | Resolution in this phase |
|-------|----------|--------------------------|
| **DRAFT** | Not loaded into Rule Registry. Only accessible via testing hooks. | Never |
| **ACTIVE** | Loaded, indexed, cached. Participates in resolution normally. | Yes, if conditions match |
| **DEPRECATED** | Still loaded, still participates, but emits deprecation warning in audit. Resolution still possible. | Yes, with `deprecated: true` flag |
| **REMOVED** | Purged from cache. No longer available for resolution. | Never |

### 7.3 Grace Period

Deprecated rules MUST remain in ACTIVE resolution for at least 30 days before removal. This allows downstream consumers to migrate.

---

## 8. Rule Testing Hooks

### 8.1 Test API

```json
POST /_test/resolve
{
  "context": { /* full Input Contract */ },
  "domain": "qualification",
  "options": {
    "include_deprecated": false,
    "force_rules": ["QUAL-002"],
    "exclude_rules": [],
    "debug_conditions": true
  }
}
```

### 8.2 Test Response

```json
{
  "resolution": { /* full ResolvedRule */ },
  "debug": {
    "conditions_evaluated": 3,
    "condition_results": [
      { "expression": "score >= 80", "result": true, "duration_ms": 2 },
      { "expression": "intent == buy", "result": true, "duration_ms": 1 },
      { "expression": "city exists", "result": true, "duration_ms": 1 }
    ],
    "conflicts_checked": 1,
    "resolution_strategy": "priority",
    "total_duration_ms": 15
  }
}
```

### 8.3 Test Scenarios

| Hook | Purpose |
|------|---------|
| `resolve(context, domain)` | Full resolution pipeline |
| `evaluate(condition, context)` | Single condition evaluation |
| `detectConflict(candidates)` | Conflict detection only |
| `resolveConflict(candidates, strategy)` | Specific strategy |
| `compare(r1, r2, context)` | Head-to-head comparison |

### 8.4 Property-Based Testing

The following invariants MUST hold for every rule resolution:

1. **Determinism**: Same input → same output (test with 1000 iterations)
2. **Totality**: Every input produces exactly one resolved rule
3. **No silent rule**: Every matched rule appears in either `selected` or `rejected`
4. **No hidden winner**: The selected rule is always in `candidates`
5. **Priority monotonicity**: If r1.priority > r2.priority and no conflicts, r1 is always selected

---

## 9. Examples of Rule Resolution for Typical LAWIM Scenarios

### Example 1: HOT Lead → Call Immediately

**Context:**
- Intent: `buy`
- Qualification score: 85
- City: Douala (detected)
- Budget: 50M FCFA (detected)

**Matching rules:**

| Rule | Conditions | Priority | Action |
|------|-----------|----------|--------|
| QUAL-002 | `score >= 80 AND intent IN [buy,rent] AND city exists` | 0.85 | `call_immediately` |
| QUAL-003 | `score >= 60 AND score < 80` | 0.60 | `send_listings` |
| QUAL-009 | `score >= 60` | 0.60 | `send_listings` |

**Resolution:**
1. Load rules for `qualification` domain
2. Filter by effective date (all active)
3. Evaluate conditions:
   - QUAL-002: `85 >= 80` AND `buy IN [buy,rent]` AND `city exists` → **true**
   - QUAL-003: `85 >= 60` AND `85 < 80` → **false** (second condition fails)
   - QUAL-009: `85 >= 60` → **true**
4. Candidates: QUAL-002 (0.85), QUAL-009 (0.60)
5. Conflict check: overlap detected (same conditions, different action types)
6. Resolution: priority-based → QUAL-002 (0.85) beats QUAL-009 (0.60), gap 0.25 > 0.05
7. Selected: QUAL-002 → `call_immediately`

### Example 2: WARM Lead → Send Listings

**Context:**
- Intent: `rent`
- Qualification score: 72
- City: Yaoundé (detected)
- Neighborhood: Bastos (detected)

**Matching rules:**

| Rule | Conditions | Priority | Action |
|------|-----------|----------|--------|
| QUAL-002 | `score >= 80 AND intent IN [buy,rent] AND city exists` | 0.85 | `call_immediately` |
| QUAL-003 | `score >= 60 AND score < 80` | 0.60 | `send_listings` |
| QUAL-009 | `score >= 60` | 0.60 | `send_listings` |

**Resolution:**
1. QUAL-002: `72 >= 80` → **false** (fails)
2. QUAL-003: `72 >= 60` AND `72 < 80` → **true**
3. QUAL-009: `72 >= 60` → **true**
4. Candidates: QUAL-003 (0.60), QUAL-009 (0.60)
5. Conflict check: overlap detected (same conditions, both `send_listings`)
6. Resolution: specificity-based → QUAL-003 has 2 conditions vs QUAL-009 has 1 → QUAL-003 wins
7. Selected: QUAL-003 → `send_listings`

### Example 3: Diaspora Investor → Immediate Agent Assignment

**Context:**
- Intent: `invest`
- Diaspora flag: `true`
- City: Douala
- Country: `US` (from phone prefix)

**Matching rules:**

| Rule | Conditions | Priority | Action |
|------|-----------|----------|--------|
| QUAL-002 | `score >= 80 AND intent IN [buy,rent] AND city exists` | 0.85 | `call_immediately` |
| QUAL-008 | `intent == invest AND diaspora == true` | 0.90 | `assign_premium_agent` |
| QUAL-009 | `score >= 60` | 0.60 | `send_listings` |

**Resolution:**
1. QUAL-002: `score >= 80` → **false** (score not yet computed)
2. QUAL-008: `invest == invest` AND `true == true` → **true**
3. QUAL-009: `score >= 60` → **false** (score not yet computed)
4. Candidates: QUAL-008 (0.90)
5. No conflicts (single candidate)
6. Selected: QUAL-008 → `assign_premium_agent`

### Example 4: Anti-Flag → Block (Security Override)

**Context:**
- Intent: `buy`
- Security signals: high message frequency (12/min), duplicate query pattern
- Trust level: `new`

**Matching rules:**

| Rule | Conditions | Priority | Action |
|------|-----------|----------|--------|
| QUAL-002 | `score >= 80 AND intent IN [buy,rent] AND city exists` | 0.85 | `call_immediately` |
| SEC-001 | `messages_per_minute > 10` | 0.95 | `block_user` |

**Resolution:**
1. QUAL-002: `score >= 80` → **false** (score computation deferred due to security block)
2. SEC-001: `12 > 10` → **true**
3. Candidates: SEC-001 (0.95)
4. No conflicts (single candidate)
5. Selected: SEC-001 → `block_user`
6. Audit note: `QUAL-002 not evaluated: domain_qualification blocked by domain_security`

This demonstrates the **Safety Override** pattern: security rules can preempt domain rules when threats are detected. The Decision Engine processes security rules first, then falls through to other domains only if no security rule matches.

### Example 5: Conflict Escalation (Edge Case)

**Context:**
- Qualification score: 85
- Intent: `buy`
- Two contradictory rules are both active with identical priority

**Matching rules:**

| Rule | Conditions | Priority | Action |
|------|-----------|----------|--------|
| QUAL-002 | `score >= 80 AND intent IN [buy,rent]` | 0.85 | `call_immediately` |
| QUAL-002-B | `score >= 80 AND intent IN [buy,rent]` | 0.85 | `ignore` (contradictory update) |

**Resolution:**
1. Both conditions evaluate to true
2. Both have priority 0.85
3. Conflict: overlap with contradiction (call vs ignore for same input)
4. Specificity: both have 2 terms → tie
5. Recency: both have same effective_date → tie
6. All strategies exhausted → **ESCALATE**
7. Fallback: `escalate_to_admin`, both rules rejected
8. Decision engine selects `no_action_required` with `conflict_escalation` audit event
