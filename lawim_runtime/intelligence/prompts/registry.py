from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

logger = logging.getLogger(__name__)


class PromptStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    DEPRECATED = "DEPRECATED"
    DISABLED = "DISABLED"


@dataclass
class PromptVersion:
    version_id: str = field(default_factory=lambda: uuid4().hex[:16])
    version: str = "1.0"
    system_template: str = ""
    user_template: str = ""
    response_schema: dict[str, Any] | None = None
    checksum: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class PromptTemplate:
    prompt_id: str = field(default_factory=lambda: uuid4().hex[:16])
    name: str = ""
    task_type: str = ""
    description: str = ""
    status: PromptStatus = PromptStatus.DRAFT
    versions: list[PromptVersion] = field(default_factory=list)
    active_version: str = ""
    allowed_variables: tuple[str, ...] = ()
    language: str = "fr"
    provider_constraints: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def active(self) -> PromptVersion | None:
        for v in self.versions:
            if v.version == self.active_version:
                return v
        return None


class PromptRegistry:
    def __init__(self) -> None:
        self._templates: dict[str, PromptTemplate] = {}

    def register(self, template: PromptTemplate) -> None:
        self._templates[template.prompt_id] = template
        logger.info("prompt registered: %s (task=%s)", template.name, template.task_type)

    def get(self, prompt_id: str) -> PromptTemplate | None:
        return self._templates.get(prompt_id)

    def get_by_name(self, name: str) -> PromptTemplate | None:
        for t in self._templates.values():
            if t.name == name:
                return t
        return None

    def get_active(self, name: str) -> PromptVersion | None:
        template = self.get_by_name(name)
        if template and template.active_version:
            return template.active
        return None

    def list(self) -> list[PromptTemplate]:
        return list(self._templates.values())
