from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import Any

from .learning_models import LearningEvent, OutcomeResult, FeedbackItem
from .learning_models_p2 import (
    DatasetCategory,
    DatasetStatus,
    FeatureDefinition,
    LearningDataset,
)


class LearningDatasetRegistry:
    def __init__(self) -> None:
        self._datasets: list[LearningDataset] = []

    def create(self, dataset: LearningDataset) -> LearningDataset:
        dataset.dataset_id = str(uuid.uuid4())
        dataset.created_at = datetime.now(timezone.utc).isoformat()
        self._datasets.append(dataset)
        return dataset

    def get(self, dataset_id: str) -> LearningDataset | None:
        for d in self._datasets:
            if d.dataset_id == dataset_id:
                return d
        return None

    def list(self, status: DatasetStatus | None = None) -> list[LearningDataset]:
        if status is None:
            return list(self._datasets)
        return [d for d in self._datasets if d.status == status]

    def count(self) -> int:
        return len(self._datasets)


class LearningDatasetBuilder:
    def build_dataset(self, dataset: LearningDataset,
                       events: list[LearningEvent],
                       outcomes: list[OutcomeResult] | None = None,
                       feedbacks: list[FeedbackItem] | None = None) -> LearningDataset:
        filtered = self._apply_filters(events, dataset)
        dataset.row_count = len(filtered)
        dataset.quality_status = "BUILDING"
        raw = json.dumps([e.to_dict() for e in filtered], sort_keys=True)
        dataset.checksum = hashlib.sha256(raw.encode()).hexdigest()
        dataset.status = DatasetStatus.READY
        return dataset

    def validate_dataset(self, dataset: LearningDataset) -> list[str]:
        issues: list[str] = []
        if dataset.row_count == 0:
            issues.append("Dataset is empty")
        if dataset.row_count < 10:
            issues.append(f"Dataset too small: {dataset.row_count} rows")
        return issues

    def _apply_filters(self, events: list[LearningEvent],
                        dataset: LearningDataset) -> list[LearningEvent]:
        from datetime import timedelta
        results = list(events)
        if dataset.filters:
            for key, val in dataset.filters.items():
                results = [e for e in results if self._match(e, key, val)]
        return results

    def _match(self, event: LearningEvent, key: str, value: Any) -> bool:
        v = getattr(event, key, None) or event.payload.get(key)
        if v is None:
            return False
        return str(v).lower() == str(value).lower()


# ── Feature Catalog ────────────────────────────────────────────────────────


_FEATURES: list[FeatureDefinition] = [
    FeatureDefinition("CHANNEL_CODE", "Channel code", "Canonical external channel code",
                       "channel", "string", "tracking_models.ExternalChannelCode",
                       "channel_code(event)", "1.0"),
    FeatureDefinition("CAMPAIGN_CODE", "Campaign code", "Campaign identifier",
                       "campaign", "string", "tracking_models.ExternalCampaign",
                       "campaign_code(event)", "1.0"),
    FeatureDefinition("PUBLICATION_CODE", "Publication tracking code",
                       "Canonical tracking code", "publication", "string",
                       "tracking_models.generate_tracking_code",
                       "tracking_code(event)", "1.0"),
    FeatureDefinition("ACTOR_ROLE_AT_EVENT", "Actor role at event time",
                       "Historical role of the actor when event occurred",
                       "actor", "string", "learning_models.LearningEvent",
                       "actor_role(event)", "1.0"),
    FeatureDefinition("LANGUAGE", "Language", "Language code (fr/en)",
                       "language", "string", "event.payload",
                       "payload.language", "1.0"),
    FeatureDefinition("CITY", "City", "City name", "geography", "string",
                       "event.payload", "payload.city", "1.0"),
    FeatureDefinition("LAWIM_ZONE", "LAWIM zone", "Geographic zone",
                       "geography", "string", "event.payload", "payload.lawim_zone", "1.0"),
    FeatureDefinition("PROPERTY_TYPE", "Property type", "Type of property",
                       "property", "string", "event.payload", "payload.property_type", "1.0"),
    FeatureDefinition("EXCHANGE_TYPE", "Exchange type", "Business exchange type",
                       "conversation", "string", "exchange_taxonomy.ExchangeType",
                       "exchange_type(event)", "1.0"),
    FeatureDefinition("MESSAGE_COUNT", "Message count", "Number of messages in conversation",
                       "conversation", "integer", "event.payload", "payload.message_count", "1.0"),
    FeatureDefinition("RESPONSE_TIME", "Response time", "Time to first response in minutes",
                       "conversation", "float", "event.payload", "payload.response_time_min", "1.0"),
    FeatureDefinition("QUALIFICATION_QUESTION_COUNT", "Qualification question count",
                       "Number of questions asked", "qualification", "integer",
                       "event.payload", "payload.question_count", "1.0"),
    FeatureDefinition("QUALIFICATION_DURATION", "Qualification duration",
                       "Duration in seconds", "qualification", "float",
                       "event.payload", "payload.duration_seconds", "1.0"),
    FeatureDefinition("MATCHING_COUNT", "Matching count", "Number of matchings created",
                       "matching", "integer", "event.payload", "payload.matching_count", "1.0"),
    FeatureDefinition("VISIT_COUNT", "Visit count", "Number of visits",
                       "visit", "integer", "event.payload", "payload.visit_count", "1.0"),
    FeatureDefinition("PAYMENT_STATUS", "Payment status", "Payment confirmation status",
                       "payment", "string", "event.payload", "payload.payment_status", "1.0",
                       bias_risk="MEDIUM"),
    FeatureDefinition("CONVERSION_OUTCOME", "Conversion outcome",
                       "Whether conversion was successful", "conversion", "boolean",
                       "event.payload", "payload.conversion_success", "1.0",
                       leakage_risk="HIGH"),
    FeatureDefinition("HANDOVER_COUNT", "Handover count", "Number of human handovers",
                       "conversation", "integer", "event.payload", "payload.handover_count", "1.0"),
    FeatureDefinition("FEEDBACK_SCORE", "Feedback score", "User satisfaction score",
                       "feedback", "float", "feedback_item", "feedback.score", "1.0",
                       missing_value_policy="IMPUTE_MEAN", bias_risk="MEDIUM"),
    FeatureDefinition("SATISFACTION_SCORE", "Satisfaction score",
                       "CRM satisfaction survey score", "feedback", "float",
                       "outcome_result", "outcome.satisfaction_score", "1.0",
                       missing_value_policy="IMPUTE_MEAN"),
]

_BY_CODE: dict[str, FeatureDefinition] = {f.feature_code: f for f in _FEATURES}


class FeatureCatalog:
    def get(self, code: str) -> FeatureDefinition | None:
        return _BY_CODE.get(code)

    def list_all(self) -> list[FeatureDefinition]:
        return list(_FEATURES)

    def count(self) -> int:
        return len(_FEATURES)

    def to_dict_list(self) -> list[dict[str, Any]]:
        return [f.to_dict() for f in _FEATURES]

    def get_by_domain(self, domain: str) -> list[FeatureDefinition]:
        return [f for f in _FEATURES if f.domain == domain]


feature_catalog = FeatureCatalog()


# ── Data Quality ────────────────────────────────────────────────────────────


class LearningDataQualityService:
    def check_dataset(self, dataset: LearningDataset,
                       events: list[LearningEvent],
                       outcomes: list[OutcomeResult] | None = None) -> list[dict[str, Any]]:
        issues: list[dict[str, Any]] = []
        if not events:
            issues.append({"type": "EMPTY", "severity": "ERROR", "message": "No events in dataset"})
        missing_actor = sum(1 for e in events if not e.actor_id)
        if missing_actor:
            issues.append({"type": "ORPHAN_EVENT", "severity": "WARNING",
                            "message": f"{missing_actor} events without actor_id"})
        if outcomes:
            linked = sum(1 for o in outcomes if any(e.event_id == o.event_id for e in events))
            if linked < len(outcomes):
                issues.append({"type": "UNLINKED_OUTCOME", "severity": "WARNING",
                                "message": f"{len(outcomes) - linked} outcomes not linked to events"})
        return issues

    def check_leakage(self, events: list[LearningEvent],
                       target_field: str = "conversion_success") -> list[dict[str, Any]]:
        issues: list[dict[str, Any]] = []
        future_targets = 0
        for e in events:
            val = e.payload.get(target_field)
            if val is not None:
                future_targets += 1
        if future_targets:
            issues.append({"type": "POTENTIAL_LEAKAGE", "severity": "WARNING",
                            "message": f"{future_targets} events contain target field {target_field}"})
        return issues
