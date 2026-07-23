from __future__ import annotations

import hashlib
import logging
from typing import Any

from .registry import PromptTemplate, PromptVersion

logger = logging.getLogger(__name__)


class PromptRenderer:
    def render(self, template: PromptTemplate, variables: dict[str, Any]) -> str:
        version = template.active
        if not version:
            logger.warning("no active version for prompt %s", template.name)
            return ""

        system = self._render_template(version.system_template, variables, template.allowed_variables)
        user = self._render_template(version.user_template, variables, template.allowed_variables)

        return f"{system}\n\n{user}" if system else user

    def render_system(self, template: PromptTemplate, variables: dict[str, Any]) -> str:
        version = template.active
        if not version:
            return ""
        return self._render_template(version.system_template, variables, template.allowed_variables)

    def render_user(self, template: PromptTemplate, variables: dict[str, Any], input_text: str = "") -> str:
        version = template.active
        if not version:
            return ""
        context_vars = dict(variables)
        if input_text:
            context_vars["input_text"] = input_text
        return self._render_template(version.user_template, context_vars, template.allowed_variables)

    def _render_template(self, template: str, variables: dict[str, Any], allowed: tuple[str, ...]) -> str:
        result = template
        for key, value in variables.items():
            if allowed and key not in allowed:
                continue
            placeholder = "{{" + key + "}}"
            result = result.replace(placeholder, str(value))
        return result

    @staticmethod
    def compute_checksum(template: str) -> str:
        return hashlib.sha256(template.encode()).hexdigest()[:16]
