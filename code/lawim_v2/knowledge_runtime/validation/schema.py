from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from ..errors import KnowledgeSchemaError

logger = logging.getLogger(__name__)


class SchemaValidator:
    def validate_json(self, path: str) -> None:
        p = Path(path)
        if not p.is_file():
            raise KnowledgeSchemaError(path, f"File not found: {path}")
        raw = p.read_bytes()
        try:
            json.loads(raw)
        except json.JSONDecodeError as exc:
            raise KnowledgeSchemaError(path, f"Invalid JSON: {exc}") from exc

    def validate_structure(self, path: str, expected_keys: set[str]) -> dict[str, Any]:
        p = Path(path)
        data = json.loads(p.read_bytes())
        if not isinstance(data, dict):
            raise KnowledgeSchemaError(path, f"Expected dict, got {type(data).__name__}")
        missing = expected_keys - set(data.keys())
        if missing:
            raise KnowledgeSchemaError(path, f"Missing keys: {missing}")
        return data
