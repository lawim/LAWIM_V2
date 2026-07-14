from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ActionType(str, Enum):
    CREATE_PROJECT = "CREATE_PROJECT"
    CREATE_DOSSIER = "CREATE_DOSSIER"
    SELECT_PROJECT = "SELECT_PROJECT"
    UPDATE_FACT = "UPDATE_FACT"
    REQUEST_CLARIFICATION = "REQUEST_CLARIFICATION"
    START_SEARCH = "START_SEARCH"
    RUN_MATCHING = "RUN_MATCHING"
    PRESENT_RESULTS = "PRESENT_RESULTS"
    CREATE_SEARCH_ALERT = "CREATE_SEARCH_ALERT"
    CREATE_RELATIONSHIP_PROPOSAL = "CREATE_RELATIONSHIP_PROPOSAL"
    REQUEST_CONSENT = "REQUEST_CONSENT"
    RECORD_CONSENT = "RECORD_CONSENT"
    CREATE_RELATIONSHIP = "CREATE_RELATIONSHIP"
    PRESENT_PARTICIPANTS = "PRESENT_PARTICIPANTS"
    REQUEST_VISIT = "REQUEST_VISIT"
    HANDOVER_TO_HUMAN = "HANDOVER_TO_HUMAN"
    CLOSE_PROJECT = "CLOSE_PROJECT"
    GREETING = "GREETING"
    PROVIDE_INFORMATION = "PROVIDE_INFORMATION"
    NOTHING = "NOTHING"


class ActionStatus(str, Enum):
    PENDING = "PENDING"
    EXECUTING = "EXECUTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"


@dataclass
class Action:
    action_id: str = ""
    action_type: str = ""
    status: ActionStatus = ActionStatus.PENDING
    parameters: dict | None = None
    result: dict | None = None
    error: str | None = None


@dataclass
class ActionResult:
    action: ActionType | None = None
    status: ActionStatus = ActionStatus.PENDING
    parameters: dict | None = None
    error: str | None = None
    result: dict | None = None
