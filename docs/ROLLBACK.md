# Rollback Plan

## Validation-only rollback approach

When a migration validation identifies a blocker:
1. Stop the migration preparation workflow.
2. Preserve the last known-good configuration.
3. Review failed validations and recommendations.
4. Re-run the audit after corrective action.
5. Continue only when the readiness score is acceptable.
