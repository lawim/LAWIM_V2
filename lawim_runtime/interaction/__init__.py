from __future__ import annotations

from .envelope import InteractionEnvelope, MessageType
from .context import InteractionContext
from .identity import IdentityResolver, ChannelIdentity, IdentityResolutionResult, IdentityStatus
from .project_resolution import ProjectResolver, ProjectResolutionResult, ProjectResolutionStatus
from .session import InteractionSession, SessionManager, SessionStatus
from .normalization import MessageNormalizer, NormalizationResult
from .deduplication import InteractionDeduplicator, DeduplicationStatus
from .correlation import CorrelationManager
from .gateway import InteractionGateway
from .orchestrator import InteractionOrchestrator
from .response_plan import InteractionResponsePlan, ResponseType
from .delivery import DeliveryManager, DeliveryStatus, DeliveryAttempt, DeliveryResult

__all__ = [
    "InteractionEnvelope",
    "MessageType",
    "InteractionContext",
    "IdentityResolver",
    "ChannelIdentity",
    "IdentityResolutionResult",
    "IdentityStatus",
    "ProjectResolver",
    "ProjectResolutionResult",
    "ProjectResolutionStatus",
    "InteractionSession",
    "SessionManager",
    "SessionStatus",
    "MessageNormalizer",
    "NormalizationResult",
    "InteractionDeduplicator",
    "DeduplicationStatus",
    "CorrelationManager",
    "InteractionGateway",
    "InteractionOrchestrator",
    "InteractionResponsePlan",
    "ResponseType",
    "DeliveryManager",
    "DeliveryStatus",
    "DeliveryAttempt",
    "DeliveryResult",
]
