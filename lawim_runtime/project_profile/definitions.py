from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


class ValueType(str, Enum):
    STRING = "STRING"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    BOOLEAN = "BOOLEAN"
    ENUM = "ENUM"
    MONEY = "MONEY"
    DATE = "DATE"
    PERIOD = "PERIOD"
    SURFACE = "SURFACE"
    LIST = "LIST"
    DICT = "DICT"
    PHONE = "PHONE"
    EMAIL = "EMAIL"
    URL = "URL"


class MergeStrategy(str, Enum):
    REPLACE_ALWAYS = "REPLACE_ALWAYS"
    REPLACE_IF_HIGHER_CONFIDENCE = "REPLACE_IF_HIGHER_CONFIDENCE"
    REPLACE_IF_NEWER = "REPLACE_IF_NEWER"
    KEEP_EXISTING = "KEEP_EXISTING"
    APPEND_UNIQUE = "APPEND_UNIQUE"
    MERGE_SET = "MERGE_SET"
    MIN_VALUE = "MIN_VALUE"
    MAX_VALUE = "MAX_VALUE"
    USER_CONFIRMED_WINS = "USER_CONFIRMED_WINS"
    OPERATOR_WINS = "OPERATOR_WINS"
    SYSTEM_WINS = "SYSTEM_WINS"
    REQUIRE_CONFIRMATION = "REQUIRE_CONFIRMATION"


class ConflictStrategy(str, Enum):
    KEEP_CURRENT = "KEEP_CURRENT"
    ACCEPT_NEW = "ACCEPT_NEW"
    USE_HIGHER_CONFIDENCE = "USE_HIGHER_CONFIDENCE"
    USE_NEWER = "USE_NEWER"
    REQUIRE_CONFIRMATION = "REQUIRE_CONFIRMATION"


@dataclass(frozen=True)
class FieldDefinition:
    field_name: str = ""
    canonical_name: str = ""
    aliases: tuple[str, ...] = ()
    value_type: ValueType = ValueType.STRING
    required: bool = False
    required_for_stages: tuple[str, ...] = ()
    priority: int = 100
    description: str = ""
    display_label: str = ""
    allowed_values: tuple[str, ...] = ()
    default_value: Any = None
    normalizer: str = ""
    validators: tuple[str, ...] = ()
    merge_strategy: MergeStrategy = MergeStrategy.REPLACE_IF_HIGHER_CONFIDENCE
    conflict_strategy: ConflictStrategy = ConflictStrategy.USE_HIGHER_CONFIDENCE
    minimum_confidence: float = 0.5
    sensitive: bool = False
    repeatable: bool = False
    searchable: bool = False
    sortable: bool = False
    version: int = 1
    metadata: dict[str, Any] = field(default_factory=dict)
