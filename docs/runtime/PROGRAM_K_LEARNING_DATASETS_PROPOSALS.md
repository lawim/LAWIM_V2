# Program K — Learning Datasets, Analysis and Proposals (Part 2)

**Document ID:** LAWIM-PROGRAM-K-PART2-V1
**Status:** CANONICAL
**Date:** 2026-07-15

---

## 1. Components Delivered

- Learning Dataset Registry + Builder (14 categories)
- Feature Catalog (20 features)
- Data Quality + Leakage Control
- Learning Analysis Engine (trends, cohorts)
- Learning Hypothesis Registry
- Proposal Engine + Human Validation Workflow
- Experiment Registry + Evaluation
- Knowledge Evolution Packages
- Versioning Registry
- 5 feature flags, all disabled by default

## 2. Dataset Catalog (14 categories)

CONVERSATION_QUALITY, QUALIFICATION_EFFECTIVENESS, MATCHING_EFFECTIVENESS, VISIT_CONVERSION, TRANSACTION_CONVERSION, PAYMENT_SUCCESS, CAMPAIGN_PERFORMANCE, PUBLICATION_PERFORMANCE, CHANNEL_PERFORMANCE, ACTOR_PERFORMANCE, RESPONSE_EFFECTIVENESS, HUMAN_HANDOVER, ABANDONMENT_ANALYSIS, CUSTOMER_SATISFACTION

## 3. Feature Catalog (20 features)

CHANNEL_CODE, CAMPAIGN_CODE, PUBLICATION_CODE, ACTOR_ROLE_AT_EVENT, LANGUAGE, CITY, LAWIM_ZONE, PROPERTY_TYPE, EXCHANGE_TYPE, MESSAGE_COUNT, RESPONSE_TIME, QUALIFICATION_QUESTION_COUNT, QUALIFICATION_DURATION, MATCHING_COUNT, VISIT_COUNT, PAYMENT_STATUS, CONVERSION_OUTCOME, HANDOVER_COUNT, FEEDBACK_SCORE, SATISFACTION_SCORE

## 4. Data Quality

Checks: missing data, duplicates, orphan events, unlinked outcomes, target leakage, bias risk, insufficient coverage.

## 5. Analysis Engine

Trend analysis (positive/negative/no_data), cohort comparison by any dimension, sorted by success rate.

## 6. Hypothesis Lifecycle

DRAFT → PROPOSED → APPROVED_FOR_EXPERIMENT → RUNNING → VALIDATED/INVALIDATED

## 7. Proposal Lifecycle

DRAFT → READY_FOR_REVIEW → APPROVED/REJECTED/EXPERIMENTAL → PUBLISHED → ROLLED_BACK

11 proposal types: MODIFY_QUESTION_ORDER, MODIFY_THRESHOLD, MODIFY_WEIGHT, ADD_RECOMMENDATION, REMOVE_RULE, ADAPT_CHANNEL, ADAPT_LANGUAGE, ADAPT_TERRITORY, ADAPT_PROPERTY_TYPE, ADAPT_HANDOVER, ADAPT_WORKFLOW

## 8. Human Validation

Each proposal requires at least one human review. Reviews record decision (APPROVE/REJECT/REQUEST_CHANGES/APPROVE_FOR_EXPERIMENT), risk assessment, and comments.

## 9. Experiment Lifecycle

DRAFT → SCHEDULED → RUNNING → COMPLETED/FAILED/ROLLED_BACK

Evaluation compares control vs treatment groups using success rate with minimum sample size check.

## 10. Evolution Packages

Versioned bundles of approved proposals with diff, migration requirements, feature flags, and rollback plan.

## 11. Feature Flags

| Flag | Default |
|------|---------|
| learning_dataset_builder_enabled | false |
| learning_analysis_enabled | false |
| learning_proposal_engine_enabled | false |
| learning_experiments_enabled | false |
| knowledge_evolution_packages_enabled | false |
