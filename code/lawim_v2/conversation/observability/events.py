from __future__ import annotations

# Turn Memory
MEMORY_TURN_CREATED = "memory_turn_created"
MEMORY_CONVERSATION_LOADED = "memory_conversation_loaded"
MEMORY_CONVERSATION_UPDATED = "memory_conversation_updated"

# Case Memory
MEMORY_CASE_CREATED = "memory_case_created"
MEMORY_CASE_RESOLVED = "memory_case_resolved"
MEMORY_CASE_SWITCHED = "memory_case_switched"

# Slot Corrections
MEMORY_SLOT_CORRECTED = "memory_slot_corrected"

# State Conflicts
MEMORY_STATE_CONFLICT_DETECTED = "memory_state_conflict_detected"

# Cross-Channel Identity
MEMORY_CROSS_CHANNEL_IDENTITY_RESOLVED = "memory_cross_channel_identity_resolved"
MEMORY_CROSS_CHANNEL_CONSENT_REQUIRED = "memory_cross_channel_consent_required"
MEMORY_CROSS_CHANNEL_RESUMED = "memory_cross_channel_resumed"

# Summary
MEMORY_SUMMARY_REFRESHED = "memory_summary_refreshed"

# Handover
MEMORY_HANDOVER_SNAPSHOT_CREATED = "memory_handover_snapshot_created"

# Retention
MEMORY_RETENTION_APPLIED = "memory_retention_applied"
MEMORY_DELETED = "memory_deleted"
MEMORY_ANONYMIZED = "memory_anonymized"

# Metrics
METRIC_CONTEXT_LOSS = "memory_context_loss_total"
METRIC_WRONG_CASE_RESOLUTION = "memory_wrong_case_resolution_total"
METRIC_CROSS_CHANNEL_RESUME = "memory_cross_channel_resume_total"
METRIC_IDENTITY_CONFLICT = "memory_identity_conflict_total"
METRIC_STATE_VERSION_CONFLICT = "memory_state_version_conflict_total"
METRIC_SLOT_REGRESSION = "memory_slot_regression_total"
METRIC_DUPLICATE_CASE = "memory_duplicate_case_total"
METRIC_PROVIDER_CONTEXT_LEAK = "memory_provider_context_leak_total"
METRIC_RESUME_FAILURE = "memory_resume_failure_total"
