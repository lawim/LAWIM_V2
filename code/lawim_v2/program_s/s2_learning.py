from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable


# ── Event Bus ─────────────────────────────────────────────────────────────


@dataclass
class EventBusMessage:
    message_id: str = ""
    event_type: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    correlation_id: str = ""
    source: str = ""
    version: str = "1.0"
    timestamp: str = ""
    retry_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {"message_id": self.message_id, "event_type": self.event_type,
                "correlation_id": self.correlation_id, "source": self.source,
                "version": self.version}


class EventBus:
    def __init__(self):
        self._subscribers: dict[str, list[Callable]] = {}
        self._dead_letters: list[EventBusMessage] = []

    def publish(self, msg: EventBusMessage) -> None:
        msg.timestamp = datetime.now(timezone.utc).isoformat()
        for event_type, handlers in self._subscribers.items():
            if event_type == msg.event_type or event_type == "*":
                for handler in handlers:
                    try:
                        handler(msg)
                    except Exception:
                        msg.retry_count += 1
                        if msg.retry_count > 3:
                            self._dead_letters.append(msg)

    def subscribe(self, event_type: str, handler: callable) -> None:
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    def replay(self, messages: list[EventBusMessage]) -> None:
        for msg in messages:
            self.publish(msg)

    def dead_letters(self) -> list[EventBusMessage]:
        return list(self._dead_letters)


# ── Learning Persistence ──────────────────────────────────────────────────


@dataclass
class PersistedLearningEvent:
    event_id: str = ""
    event_type: str = ""
    source: str = ""
    actor_id: str = ""
    conversation_id: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    version: str = "1.0"
    timestamp: str = ""


@dataclass
class PersistedOutcome:
    outcome_id: str = ""
    outcome_type: str = ""
    status: str = ""
    actor_id: str = ""
    monetary_value: float = 0.0


@dataclass
class PersistedFeedback:
    feedback_id: str = ""
    origin: str = ""
    target: str = ""
    score: float = 0.0
    confidence: float = 1.0


# ── Feature Engineering ───────────────────────────────────────────────────


@dataclass
class TransformedFeature:
    feature_code: str = ""
    value: float | str = 0.0
    version: str = "1.0"

    def to_dict(self) -> dict[str, Any]:
        return {"feature_code": self.feature_code, "value": self.value, "version": self.version}


class FeatureEngineeringPipeline:
    def transform(self, raw: dict[str, Any]) -> list[TransformedFeature]:
        features: list[TransformedFeature] = []
        features.append(TransformedFeature("channel_code", raw.get("channel", "")))
        features.append(TransformedFeature("message_count", raw.get("message_count", 0)))
        features.append(TransformedFeature("response_time_min", raw.get("response_time_min", 0)))
        features.append(TransformedFeature("has_phone", 1 if raw.get("phone") else 0))
        features.append(TransformedFeature("has_email", 1 if raw.get("email") else 0))
        return features


# ── Training Pipeline ─────────────────────────────────────────────────────


class TrainingStatus(str, Enum):
    DRAFT = "DRAFT"
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    VALIDATING = "VALIDATING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"


@dataclass
class TrainingJob:
    job_id: str = ""
    name: str = ""
    model_type: str = ""
    dataset_ref: str = ""
    feature_codes: list[str] = field(default_factory=list)
    configuration: dict[str, Any] = field(default_factory=dict)
    status: TrainingStatus = TrainingStatus.DRAFT
    metrics: dict[str, float] = field(default_factory=dict)
    artifact_ref: str = ""
    created_at: str = ""
    completed_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"job_id": self.job_id, "name": self.name, "status": self.status.value,
                "metrics": self.metrics}


class TrainingPipeline:
    def __init__(self):
        self._jobs: list[TrainingJob] = []

    def submit(self, job: TrainingJob) -> TrainingJob:
        job.status = TrainingStatus.QUEUED
        job.created_at = datetime.now(timezone.utc).isoformat()
        self._jobs.append(job)
        return job

    def list(self) -> list[TrainingJob]:
        return list(self._jobs)


# ── Model Registry ────────────────────────────────────────────────────────


@dataclass
class ModelDefinition:
    model_id: str = ""
    name: str = ""
    version: str = "1.0.0"
    model_type: str = ""
    dataset_ref: str = ""
    feature_codes: list[str] = field(default_factory=list)
    checksum: str = ""
    metrics: dict[str, float] = field(default_factory=dict)
    bias_metrics: dict[str, float] = field(default_factory=dict)
    status: str = "DRAFT"
    approved_by: str = ""
    created_at: str = ""
    deployed_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"model_id": self.model_id, "name": self.name, "version": self.version,
                "status": self.status, "metrics": self.metrics}


class ModelRegistry:
    def __init__(self):
        self._models: list[ModelDefinition] = []

    def register(self, m: ModelDefinition) -> ModelDefinition:
        m.created_at = datetime.now(timezone.utc).isoformat()
        self._models.append(m)
        return m

    def list(self) -> list[ModelDefinition]:
        return list(self._models)

    def approve(self, model_id: str, approver: str) -> bool:
        for m in self._models:
            if m.model_id == model_id:
                m.status = "APPROVED"
                m.approved_by = approver
                return True
        return False


# ── Drift Detection ───────────────────────────────────────────────────────


@dataclass
class DriftDetectionResult:
    metric: str = ""
    baseline_value: float = 0.0
    current_value: float = 0.0
    drift_pct: float = 0.0
    threshold: float = 10.0
    drifted: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {"metric": self.metric, "baseline": self.baseline_value,
                "current": self.current_value, "drift_pct": round(self.drift_pct, 2),
                "drifted": self.drifted}


class DriftDetector:
    def check(self, metric: str, baseline: float, current: float,
               threshold_pct: float = 10.0) -> DriftDetectionResult:
        if baseline == 0:
            return DriftDetectionResult(metric=metric, drifted=False)
        drift = abs(current - baseline) / baseline * 100
        return DriftDetectionResult(metric=metric, baseline_value=baseline,
                                     current_value=current, drift_pct=drift,
                                     threshold=threshold_pct, drifted=drift > threshold_pct)
