from __future__ import annotations
from enum import Enum


class ProjectType(str, Enum):
    BUY = "BUY"
    RENT = "RENT"
    SELL = "SELL"
    LIST = "LIST"
    PUBLISH = "PUBLISH"
    DOCUMENT_REQUEST = "DOCUMENT_REQUEST"
    COMPLAINT = "COMPLAINT"
    CONSTRUCTION = "CONSTRUCTION"
    PROFESSIONAL_SERVICE = "PROFESSIONAL_SERVICE"
    OTHER = "OTHER"


class ProjectStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    QUALIFYING = "QUALIFYING"
    MATCHING = "MATCHING"
    VISIT_PENDING = "VISIT_PENDING"
    NEGOTIATING = "NEGOTIATING"
    TRANSACTION_PENDING = "TRANSACTION_PENDING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    ARCHIVED = "ARCHIVED"


class ProjectStage(str, Enum):
    INITIAL = "INITIAL"
    QUALIFICATION = "QUALIFICATION"
    SEARCH = "SEARCH"
    VISIT = "VISIT"
    NEGOTIATION = "NEGOTIATION"
    TRANSACTION = "TRANSACTION"
    POST_TRANSACTION = "POST_TRANSACTION"
    CLOSED = "CLOSED"


VALID_TRANSITIONS: dict[ProjectStatus, set[ProjectStatus]] = {
    ProjectStatus.DRAFT: {ProjectStatus.ACTIVE, ProjectStatus.CANCELLED},
    ProjectStatus.ACTIVE: {ProjectStatus.QUALIFYING, ProjectStatus.CANCELLED},
    ProjectStatus.QUALIFYING: {ProjectStatus.MATCHING, ProjectStatus.ACTIVE, ProjectStatus.CANCELLED},
    ProjectStatus.MATCHING: {ProjectStatus.VISIT_PENDING, ProjectStatus.QUALIFYING, ProjectStatus.CANCELLED},
    ProjectStatus.VISIT_PENDING: {ProjectStatus.NEGOTIATING, ProjectStatus.MATCHING, ProjectStatus.CANCELLED},
    ProjectStatus.NEGOTIATING: {ProjectStatus.TRANSACTION_PENDING, ProjectStatus.VISIT_PENDING, ProjectStatus.CANCELLED},
    ProjectStatus.TRANSACTION_PENDING: {ProjectStatus.COMPLETED, ProjectStatus.NEGOTIATING, ProjectStatus.CANCELLED},
    ProjectStatus.COMPLETED: {ProjectStatus.ARCHIVED},
    ProjectStatus.CANCELLED: set(),
    ProjectStatus.ARCHIVED: set(),
}


STAGE_MAP: dict[ProjectStatus, ProjectStage] = {
    ProjectStatus.DRAFT: ProjectStage.INITIAL,
    ProjectStatus.ACTIVE: ProjectStage.QUALIFICATION,
    ProjectStatus.QUALIFYING: ProjectStage.QUALIFICATION,
    ProjectStatus.MATCHING: ProjectStage.SEARCH,
    ProjectStatus.VISIT_PENDING: ProjectStage.VISIT,
    ProjectStatus.NEGOTIATING: ProjectStage.NEGOTIATION,
    ProjectStatus.TRANSACTION_PENDING: ProjectStage.TRANSACTION,
    ProjectStatus.COMPLETED: ProjectStage.POST_TRANSACTION,
    ProjectStatus.CANCELLED: ProjectStage.CLOSED,
    ProjectStatus.ARCHIVED: ProjectStage.CLOSED,
}
