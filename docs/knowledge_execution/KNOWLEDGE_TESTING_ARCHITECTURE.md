# KNOWLEDGE TESTING ARCHITECTURE — Heritage Gold Rule Validation Framework

**Component of:** Knowledge Execution Architecture (H1)
**Date:** 2026-07-15
**Status:** CANONICAL

---

## 1. Test Pyramid

Every Heritage Gold rule is validated through an 8-layer test pyramid. Each layer targets a specific failure mode.

```
                    ┌─────────────┐
                    │  Audit Test │  ← Correct events produced
                    ├─────────────┤
                    │Idempotence  │  ← Same result × N applications
                    ├─────────────┤
                    │  Negative   │  ← Rule does NOT fire when conditions absent
                    ├─────────────┤
                    │  Channel    │  ← Rule works on WhatsApp, Telegram, Dashboard
                    ├─────────────┤
                    │   State     │  ← State transitions are valid
                    ├─────────────┤
                    │Integration  │  ← Rule + engine + data layer
                    ├─────────────┤
                    │ Behavioral  │  ← Rule within decision flow
                    ├─────────────┤
                    │   Unit      │  ← Condition evaluation in isolation
                    └─────────────┘
```

### Layer 1 — Unit Test
- **Scope:** Single rule's `condition_expression` evaluated in isolation.
- **Fixture:** Minimal context object with only the fields the rule inspects.
- **Assert:** Rule fires if and only if conditions match.
- **Tool:** `pytest` parameterized with `@pytest.mark.parametrize`.
- **Coverage:** Every rule with at least one nominal case.

### Layer 2 — Behavioral Test
- **Scope:** Rule within a decision flow (e.g., qualification pipeline → scoring → classification → routing).
- **Fixture:** Full `RuleContext` with engine state.
- **Assert:** Correct action type and parameters produced.
- **Tool:** Decision Engine test harness (mock engines).

### Layer 3 — Integration Test
- **Scope:** Rule execution against real data layer (database, file system, external API).
- **Fixture:** Populated test database with canonical data.
- **Assert:** State mutations and event emissions match expected.
- **Tool:** `pytest` + `testcontainers` (PostgreSQL) + mock channels.

### Layer 4 — State Transition Test
- **Scope:** Rule triggers a state machine transition; validate both source and target states.
- **Fixture:** Entity in every valid source state.
- **Assert:** Transition follows STATE_MACHINE_CATALOG.md; invalid transitions rejected.
- **Tool:** State machine test harness (`transition_contracts.py`).

### Layer 5 — Channel Test
- **Scope:** Rule output formatted and deliverable on every supported channel.
- **Fixture:** Channel adapter mock (WhatsApp, Telegram, Dashboard).
- **Assert:** Message format complies with channel constraints (e.g., WhatsApp 1024 chars, Dashboard rich UI).
- **Tool:** Channel simulator + format validator.

### Layer 6 — Negative Test
- **Scope:** Rule does NOT fire when one or more conditions are absent or at boundary.
- **Fixture:** Context deliberately missing fields, wrong types, or out-of-range values.
- **Assert:** No action produced, no state mutated, no event emitted.
- **Tool:** Same harness as unit test; `assert_no_rule_fired()`.

### Layer 7 — Idempotence Test
- **Scope:** Rule applied N times produces identical state.
- **Fixture:** Context oscillating between states.
- **Assert:** `apply(apply(context)) == apply(context)`.
- **Tool:** Rule engine with replay guard.

### Layer 8 — Audit Test
- **Scope:** Rule execution produces the correct audit event with required fields.
- **Fixture:** Full execution trace.
- **Assert:** `audit_template` rendered correctly; all placeholders resolved; event stored in audit log.
- **Tool:** Audit log collector + `jsonschema` validation.

---

## 2. Test Automation Framework

### Framework Requirements

| Requirement | Specification |
|-------------|---------------|
| Language | Python 3.11+ |
| Test runner | pytest 8.x |
| Parameterization | `@pytest.mark.parametrize` for all combinatorial cases |
| Fixtures | `conftest.py` per domain, shared in `tests/conftest.py` |
| Mocking | `unittest.mock` / `pytest-mock` |
| Database | `testcontainers-postgres` or ephemeral PostgreSQL |
| State machine | Custom `state_machine_test_harness` |
| Audit | JSON Schema validator + audit log collector |
| Channels | Channel simulator with format contracts |
| Coverage | `pytest-cov` + custom rule coverage plugin |
| CI | GitHub Actions matrix (unit, integration, smoke) |

### Directory Structure

```
tests/
├── conftest.py                    # Shared fixtures (RuleEngine, DB, Channels)
├── rules/
│   ├── test_constitution.py       # CONST-001 to CONST-010
│   ├── test_property.py           # PROP-001 to PROP-011
│   ├── test_matching.py           # MATCH-001 to MATCH-034
│   ├── test_geography.py          # GEO-001 to GEO-011
│   ├── test_qualification.py      # QUAL-001 to QUAL-019
│   ├── test_conversation.py       # CONV-001 to CONV-023
│   ├── test_negotiation.py        # NEGO-001 to NEGO-014
│   ├── test_crm.py                # CRM-001 to CRM-015
│   ├── test_language.py           # LANG-001 to LANG-014
│   └── test_security.py           # SEC-001 to SEC-007
├── contracts/
│   ├── test_rule_contracts.py     # Validates every rule test conforms to RULE_TEST_CONTRACT.md
│   └── test_acceptance_matrix.py  # Validates ACCEPTANCE_TEST_MATRIX.md coverage
├── audit/
│   ├── test_audit_events.py       # Audit event schema validation
│   └── test_audit_trail.py        # Full audit trail reconstruction
├── performance/
│   ├── test_rule_latency.py       # Per-rule P99 latency
│   ├── test_pipeline_throughput.py# Qualification/matching pipeline throughput
│   └── test_concurrent_rules.py   # Concurrent rule execution
├── channels/
│   ├── test_whatsapp_format.py    # WhatsApp message format
│   ├── test_telegram_format.py    # Telegram message format
│   └── test_dashboard_format.py   # Dashboard UI format
├── regression/
│   ├── test_rules_stable.py       # No rule silently changes behavior
│   └── test_rule_idempotence.py   # Batch idempotence tests
└── environments/
    ├── conftest_unit.py           # Unit test fixtures (no DB)
    ├── conftest_integration.py    # Integration test fixtures (DB)
    └── conftest_stress.py         # Performance fixtures
```

---

## 3. Test Data Management

### Fixture Types

| Fixture | Scope | Source | Refresh |
|---------|-------|--------|---------|
| `rule_definitions` | session | `RULE_RESOLUTION_MODEL.md` / rule JSON files | On rule change |
| `state_machines` | session | `STATE_MACHINE_CATALOG.md` | On state change |
| `canonical_properties` | session | `tests/data/canonical_properties.json` | Versioned |
| `canonical_users` | session | `tests/data/canonical_users.json` | Versioned |
| `canonical_leads` | session | `tests/data/canonical_leads.json` | Versioned |
| `canonical_matches` | session | `tests/data/canonical_matches.json` | Versioned |
| `canonical_conversations` | session | `tests/data/canonical_conversations.json` | Versioned |
| `canonical_audit_events` | session | `tests/data/canonical_audit_events.json` | Versioned |
| `mock_channel_adapters` | function | Channel contract files | Per test |
| `empty_db` | function | Fresh migration | Per test class |

### Fixture Content Requirements

Each fixture file must contain:
- **Valid cases:** Entities that satisfy every rule condition.
- **Boundary cases:** Entities at the edge of rule thresholds (e.g., budget at ±tolerance limit, score at 59/60 boundary).
- **Negative cases:** Entities that deliberately miss conditions (e.g., no budget, wrong city, incompatible type).
- **Idempotence cases:** Entities designed to be processed multiple times without side effects.
- **Multi-channel cases:** Same entity payload formatted per channel contract.

### Fixture Naming Convention

```
tests/data/
├── {domain}/
│   ├── valid/
│   │   ├── case_{rule_id}_{scenario}.json
│   │   └── ...
│   ├── boundary/
│   │   ├── case_{rule_id}_{boundary_type}.json
│   │   └── ...
│   └── negative/
│       ├── case_{rule_id}_{missing_field}.json
│       └── ...
├── state_machines/
│   ├── property_lifecycle.json
│   ├── user_states.json
│   └── ...
└── audit/
    ├── expected_events_{rule_id}.json
    └── ...
```

---

## 4. Test Environment Requirements

### Environment Matrix

| Environment | Database | External APIs | Channels | Purpose |
|-------------|----------|---------------|----------|---------|
| `unit` | None | None | None | Unit + behavioral tests |
| `integration` | Ephemeral PostgreSQL | Mocked | Mocked | Integration + state transition |
| `channel` | None | None | Simulator | Channel format validation |
| `staging` | Full replica (anonymized) | Sandbox | Real (test numbers) | Pre-release validation |
| `production_like` | Full replica | Sandbox + limited real | Real | Smoke + canary |

### CI/CD Pipeline Integration

```
┌──────────┐    ┌───────────┐    ┌───────────┐    ┌──────────┐
│  Commit  │───▶│ Unit      │───▶│Integration│───▶│ Channel  │
│          │    │ (3 min)   │    │ (8 min)   │    │ (4 min)  │
└──────────┘    └───────────┘    └───────────┘    └──────────┘
                                                      │
                                                      ▼
                                              ┌──────────┐
                                              │ Staging  │
                                              │(15 min)  │
                                              └──────────┘
                                                      │
                                                      ▼
                                              ┌──────────┐
                                              │ Prod-like│
                                              │ (5 min)  │
                                              └──────────┘
```

- **Pre-merge:** Unit + Integration + Channel gates.
- **Post-merge:** Staging full suite.
- **Nightly:** Full regression + performance.
- **On-demand:** Prod-like smoke.

---

## 5. Coverage Tracking and Reporting

### Coverage Metrics

| Metric | Target | Tool |
|--------|--------|------|
| Rule coverage (% of rules with test contracts) | 100% | Custom `rule_coverage.py` |
| Test type coverage (nominal/negative/idempotence/audit) | Per ACCEPTANCE_TEST_MATRIX.md | `pytest --rule-coverage` |
| Condition branch coverage | ≥90% | `pytest-cov` + condition instrumenter |
| State transition coverage | 100% of valid transitions | State machine test harness |
| Channel coverage | 100% of active channels | Channel format validator |
| Audit event coverage | 100% of rule IDs | Audit log schema checker |

### Coverage Report Format

```json
{
  "generated_at": "2026-07-16T00:00:00Z",
  "summary": {
    "total_rules": 158,
    "with_contract": 158,
    "coverage_pct": 100.0,
    "test_types": {
      "nominal": { "required": 158, "implemented": 158, "pct": 100.0 },
      "negative": { "required": 120, "implemented": 118, "pct": 98.3 },
      "idempotence": { "required": 80, "implemented": 78, "pct": 97.5 },
      "audit": { "required": 100, "implemented": 99, "pct": 99.0 }
    }
  },
  "missing": [
    { "rule_id": "NEGO-007", "missing_test_types": ["idempotence", "audit"] }
  ],
  "domains": {
    "constitution": { "total": 10, "covered": 10 },
    "property": { "total": 11, "covered": 11 },
    "matching": { "total": 34, "covered": 34 },
    "geography": { "total": 11, "covered": 11 },
    "qualification": { "total": 19, "covered": 19 },
    "conversation": { "total": 23, "covered": 23 },
    "negotiation": { "total": 14, "covered": 14 },
    "crm": { "total": 15, "covered": 15 },
    "language": { "total": 14, "covered": 14 },
    "security": { "total": 7, "covered": 7 }
  }
}
```

### Reporting Pipeline

1. `pytest --rule-coverage=report.json` generates per-rule coverage.
2. CI compares against `ACCEPTANCE_TEST_MATRIX.md` requirements.
3. Coverage regressions block merge.
4. Weekly trend report posted to team channel.

---

## 6. Regression Test Strategy

### Trigger Conditions

| Event | Action |
|-------|--------|
| Rule definition change | Re-run all tests for that rule + all dependent rules |
| Engine code change | Re-run all tests for rules consumed by that engine |
| New rule added | Add contracts + all 8 pyramid layers |
| Rule deprecated | Remove tests after grace period (1 sprint) |
| Fixture data change | Re-run all tests referencing changed fixtures |
| External dependency update | Full regression suite |

### Regression Test Selection

- **Touch-point analysis:** Map rule_id → engine → file dependencies.
- **Selective execution:** Only re-run test files touching changed dependency paths.
- **Full regression:** Nightly run of entire test suite.

### Regression Suite Contents

| Suite | Triggers | Duration | Frequency |
|-------|----------|----------|-----------|
| Smoke (top 20 HIGH rules) | Every commit | 2 min | Per commit |
| Critical (all HIGH rules) | Every PR | 5 min | Per PR |
| Extended (HIGH + MEDIUM) | Merge to main | 12 min | Per merge |
| Full (ALL rules) | Nightly, pre-release | 30 min | Daily |

---

## 7. Performance Test Requirements

### Per-Rule Latency

| Metric | Threshold | Measurement |
|--------|-----------|-------------|
| P50 condition evaluation | < 5 ms | `timeit` over 1000 iterations |
| P95 condition evaluation | < 15 ms | `timeit` over 1000 iterations |
| P99 condition evaluation | < 50 ms | `timeit` over 1000 iterations |
| P50 full rule execution | < 20 ms | Including action dispatch |
| P95 full rule execution | < 60 ms | Including action dispatch |
| P99 full rule execution | < 200 ms | Including action dispatch |

### Pipeline Throughput

| Pipeline | Minimum TPS | Target TPS | Measured |
|----------|-------------|------------|----------|
| Qualification (incoming→routing) | 10/s | 50/s | Locust |
| Matching (intent→results) | 5/s | 20/s | Locust |
| Conversation (message→response) | 20/s | 100/s | Locust |
| Geography (location→resolution) | 30/s | 150/s | Locust |
| CRM scoring | 50/s | 200/s | Locust |

### Concurrent Rule Execution

| Scenario | Rules Fired | Concurrency | Max Duration |
|----------|-------------|-------------|--------------|
| Single lead qualification | 5-8 | 1 | 100 ms |
| Batch of 10 leads | 50-80 | 10 | 500 ms |
| 100 simultaneous messages | 200-400 | 100 | 2 s |
| Peak-hour CRM scoring | 500-800 | 50 | 1 s |

### Performance Test Fixtures

- Use `tests/performance/fixtures/` with scaled data (1000+ properties, 500+ users, 200+ leads).
- Each performance test records metrics to `tests/performance/reports/` for trend analysis.
- Performance regression threshold: >20% degradation from baseline triggers alert.

---

## 8. Test Implementation Rules

1. Every rule test MUST be traceable to `RULE_TEST_CONTRACT.md` via `test_id`.
2. Every rule test MUST be traceable to `ACCEPTANCE_TEST_MATRIX.md` via `rule_id`.
3. Test names MUST follow pattern: `test_{rule_id}_{test_type}_{scenario}` (e.g., `test_QUAL_001_nominal_hot_lead`).
4. Test data MUST use canonical fixtures; no inline magic values.
5. Audit tests MUST validate the complete event payload against JSON schema.
6. Negative tests MUST verify no side effects (state unchanged, no event emitted).
7. Idempotence tests MUST repeat execution exactly 3 times and assert identical final state.
8. Channel tests MUST run on all active channels defined in `CONST-004`/`CONST-005`.
9. Performance tests MUST run against a dedicated environment (not shared with functional tests).
10. Every PR MUST include test contract updates if rules changed.

---

## 9. Tools and Dependencies

| Tool | Version | Purpose |
|------|---------|---------|
| pytest | ≥8.0 | Test runner |
| pytest-cov | ≥5.0 | Coverage |
| pytest-xdist | ≥3.5 | Parallel execution |
| pytest-timeout | ≥2.2 | Test timeout guard |
| testcontainers | ≥4.0 | Ephemeral PostgreSQL |
| jsonschema | ≥4.20 | Audit event validation |
| locust | ≥2.20 | Load testing |
| deepdiff | ≥7.0 | Idempotence assertion |
| freezegun | ≥1.5 | Time-dependent rule tests |
| responses | ≥0.25 | HTTP API mocking |
