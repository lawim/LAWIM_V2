from __future__ import annotations

QUALIFICATION_EVALUATION_TOTAL = "qualification_evaluation_total"
QUALIFICATION_LATENCY_MS = "qualification_latency_ms"
DECISION_EVALUATION_TOTAL = "decision_evaluation_total"
DECISION_LATENCY_MS = "decision_latency_ms"
HANDOVER_REQUIRED_TOTAL = "handover_required_total"
PROJECT_BRAIN_UPDATE_TOTAL = "project_brain_update_total"

ALL_METRICS: tuple[str, ...] = (
    QUALIFICATION_EVALUATION_TOTAL,
    QUALIFICATION_LATENCY_MS,
    DECISION_EVALUATION_TOTAL,
    DECISION_LATENCY_MS,
    HANDOVER_REQUIRED_TOTAL,
    PROJECT_BRAIN_UPDATE_TOTAL,
)
