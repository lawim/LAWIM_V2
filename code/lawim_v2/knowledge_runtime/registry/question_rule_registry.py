from __future__ import annotations

import logging
from typing import Any

from ..models.question_rule import QuestionRule
from .base import BaseRegistry
from .errors import DuplicateEntryError

logger = logging.getLogger(__name__)

VALID_RULE_TYPES: frozenset[str] = frozenset({
    "always_ask",
    "conditional_ask",
    "never_ask",
    "deduce_from_context",
    "defer_ask",
    "rule",
    "template",
    "ambiguity",
})


class QuestionRuleRegistry(BaseRegistry):
    def __init__(self) -> None:
        super().__init__()
        self._rules: list[QuestionRule] = []
        self._by_field: dict[str, list[QuestionRule]] = {}
        self._by_type: dict[str, list[QuestionRule]] = {}

    def register(self, item: QuestionRule) -> None:
        self._check_readonly()
        if item.rule_type not in VALID_RULE_TYPES:
            raise ValueError(
                f"Invalid question rule type '{item.rule_type}' for field '{item.field}'. "
                f"Must be one of {sorted(VALID_RULE_TYPES)}"
            )
        self._rules.append(item)
        if item.field not in self._by_field:
            self._by_field[item.field] = []
        self._by_field[item.field].append(item)
        if item.rule_type not in self._by_type:
            self._by_type[item.rule_type] = []
        self._by_type[item.rule_type].append(item)

    def lock(self) -> None:
        self._validate_unique_always_ask()
        self._lock()

    def _validate_unique_always_ask(self) -> None:
        seen: set[str] = set()
        for rule in self._by_type.get("always_ask", []):
            if rule.field in seen:
                raise DuplicateEntryError(
                    f"Duplicate always_ask field: {rule.field}",
                    identifier=rule.field,
                )
            seen.add(rule.field)

    def get_by_field(self, field: str) -> list[QuestionRule]:
        return list(self._by_field.get(field, []))

    def get_by_type(self, rule_type: str) -> list[QuestionRule]:
        return list(self._by_type.get(rule_type, []))

    def all(self) -> list[QuestionRule]:
        return list(self._rules)

    def count(self) -> int:
        return len(self._rules)

    def summary(self) -> dict[str, Any]:
        base = super().summary()
        base.update({
            "registrations": self.count(),
            "types": {t: len(r) for t, r in self._by_type.items()},
            "fields": len(self._by_field),
        })
        return base
