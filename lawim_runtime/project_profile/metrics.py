from __future__ import annotations

PROFILE_CREATED_TOTAL = "profile_created_total"
PROFILE_PATCH_RECEIVED_TOTAL = "profile_patch_received_total"
PROFILE_PATCH_APPLIED_TOTAL = "profile_patch_applied_total"
PROFILE_PATCH_REJECTED_TOTAL = "profile_patch_rejected_total"
PROFILE_FIELD_UPDATED_TOTAL = "profile_field_updated_total"
PROFILE_CONFLICT_DETECTED_TOTAL = "profile_conflict_detected_total"
PROFILE_CONFLICT_RESOLVED_TOTAL = "profile_conflict_resolved_total"
PROFILE_VALIDATION_FAILED_TOTAL = "profile_validation_failed_total"
PROFILE_SNAPSHOT_CREATED_TOTAL = "profile_snapshot_created_total"
PROFILE_RESTORE_TOTAL = "profile_restore_total"

ALL_METRICS: tuple[str, ...] = (
    PROFILE_CREATED_TOTAL,
    PROFILE_PATCH_RECEIVED_TOTAL,
    PROFILE_PATCH_APPLIED_TOTAL,
    PROFILE_PATCH_REJECTED_TOTAL,
    PROFILE_FIELD_UPDATED_TOTAL,
    PROFILE_CONFLICT_DETECTED_TOTAL,
    PROFILE_CONFLICT_RESOLVED_TOTAL,
    PROFILE_VALIDATION_FAILED_TOTAL,
    PROFILE_SNAPSHOT_CREATED_TOTAL,
    PROFILE_RESTORE_TOTAL,
)
