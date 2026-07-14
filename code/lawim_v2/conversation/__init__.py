from __future__ import annotations

from .domain.conversation import Conversation
from .domain.states import ConversationState, StateTransition, STATE_TRANSITIONS
from .domain.decisions import ConversationDecision
from .domain.facts import Fact, FactStatus, FactCollection
from .domain.message import NormalizedMessage
from .domain.project import ProjectInfo, ProjectStatus
from .domain.dossier import DossierInfo, DossierStatus
from .domain.intents import Intent, IntentCandidate
from .domain.actions import ActionType, Action, ActionStatus, ActionResult
from .domain.consent import ConsentRequest, ConsentDecision, ConsentStatus
from .domain.errors import ConversationError, DecisionError, StateError

__all__ = [
    "Conversation",
    "ConversationState",
    "StateTransition",
    "STATE_TRANSITIONS",
    "ConversationDecision",
    "Fact",
    "FactStatus",
    "FactCollection",
    "NormalizedMessage",
    "ProjectInfo",
    "ProjectStatus",
    "DossierInfo",
    "DossierStatus",
    "Intent",
    "IntentCandidate",
    "ActionType",
    "Action",
    "ActionStatus",
    "ActionResult",
    "ConsentRequest",
    "ConsentDecision",
    "ConsentStatus",
    "ConversationError",
    "DecisionError",
    "StateError",
]
