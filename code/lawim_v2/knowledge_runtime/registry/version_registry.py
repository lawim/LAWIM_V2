from __future__ import annotations

import logging
from typing import Any

from ..models.version import KnowledgeVersion
from .base import BaseRegistry

logger = logging.getLogger(__name__)


class KnowledgeVersionRegistry(BaseRegistry):
    def __init__(self) -> None:
        super().__init__()
        self._version: KnowledgeVersion | None = None

    def set_version(self, version: KnowledgeVersion) -> None:
        self._check_readonly()
        self._version = version

    def lock(self) -> None:
        self._lock()

    def get(self) -> KnowledgeVersion | None:
        return self._version

    def summary(self) -> dict[str, Any]:
        base = super().summary()
        if self._version:
            base["version"] = self._version.dict()
        else:
            base["version"] = None
        return base
