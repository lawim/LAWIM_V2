# Program K — Learning Governance, Publication, Rollout, Monitoring (Final Bundle)

**Document ID:** LAWIM-PROGRAM-K-FINAL-V1
**Status:** CANONICAL — PROGRAM K COMPLETE
**Date:** 2026-07-15

---

## 1. Governance

### Risk Levels
LOW, MEDIUM, HIGH, CRITICAL

### Permissions (16)
learning.events.read, learning.datasets.read, learning.datasets.build, learning.analysis.read, learning.hypotheses.manage, learning.proposals.manage, learning.proposals.review, learning.proposals.approve, learning.experiments.manage, learning.publications.prepare, learning.publications.approve, learning.publications.execute, learning.rollouts.manage, learning.rollbacks.execute, learning.audit.read, learning.emergency_stop

### Policies
Each policy defines: risk_level, required_reviews, required_approvals, required_roles, prohibited_role_combinations.

## 2. Knowledge Evolution Packages

14 statuses: DRAFT → READY_FOR_REVIEW → UNDER_REVIEW → APPROVED → READY_FOR_PUBLICATION → PUBLISHING → PUBLISHED → PARTIALLY_ROLLED_OUT → FULLY_ROLLED_OUT → PAUSED → FAILED → ROLLED_BACK → ARCHIVED

Each package has 13 release gates that must all pass before publication:
SCHEMA_VALID, REFERENCES_VALID, UNIT_TESTS_PASS, INTEGRATION_TESTS_PASS, NON_REGRESSION_PASS, DATA_QUALITY_PASS, BIAS_CHECK_PASS, LEAKAGE_CHECK_PASS, RUNTIME_COMPATIBILITY_PASS, ROLLBACK_TESTED, APPROVALS_COMPLETE, FEATURE_FLAGS_READY, MONITORING_READY

## 3. Rollout

Strategies: INTERNAL_ONLY, PILOT_GROUP, PERCENTAGE, ROLE_BASED, AGENCY_BASED, CHANNEL_BASED, REGION_BASED, FULL

Stages: 0_PERCENT → INTERNAL → 1_PERCENT → 5_PERCENT → 10_PERCENT → 25_PERCENT → 50_PERCENT → 100_PERCENT

Deterministic assignment via SHA-256 hash of user ID.

## 4. Guardrails

Actions: WARN, PAUSE_ROLLOUT, STOP_ROLLOUT, ROLLBACK, REQUIRE_REVIEW

## 5. Monitoring and Drift

Drift types: DATA_DRIFT, FEATURE_DRIFT, OUTCOME_DRIFT, FEEDBACK_DRIFT, PERFORMANCE_DRIFT, CHANNEL_DRIFT, REGIONAL_DRIFT, LANGUAGE_DRIFT

Statuses: OPEN → ACKNOWLEDGED → UNDER_REVIEW → RESOLVED → FALSE_POSITIVE

## 6. Rollback

Preserves events and audit trail. Restores previous version, handles migrations, validates runtime.

## 7. Post-Publication Evaluation

Results: SUCCESS, PARTIAL_SUCCESS, INCONCLUSIVE, FAILED, ROLLED_BACK
