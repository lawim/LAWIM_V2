from __future__ import annotations

from typing import Any, Callable

from ..definitions import ValueType
from ..registry import FieldRegistry
from .result import ValidationIssue, ValidationResult, ValidationStatus

ValidatorFunc = Callable[[str, Any, str], ValidationResult | None]

CODE_TYPE_MISMATCH = "TYPE_MISMATCH"
CODE_VALUE_NONE = "VALUE_NONE"
CODE_NEGATIVE_VALUE = "NEGATIVE_VALUE"
CODE_CUSTOM_FAILURE = "CUSTOM_FAILURE"


class ValidatorRegistry:
    def __init__(self) -> None:
        self._validators: dict[str, ValidatorFunc] = {}

    def register(self, name: str, func: ValidatorFunc) -> None:
        self._validators[name] = func

    def get(self, name: str) -> ValidatorFunc | None:
        return self._validators.get(name)

    def list(self) -> list[str]:
        return list(self._validators.keys())


class FieldValidator:
    def __init__(self, registry: FieldRegistry, validators: ValidatorRegistry) -> None:
        self._registry = registry
        self._validators = validators

    def validate(
        self, field_name: str, value: Any, profile_type: str = ""
    ) -> ValidationResult:
        result = ValidationResult(status=ValidationStatus.VALID)

        if value is None:
            result.issues.append(
                ValidationIssue(
                    field_name=field_name,
                    status=ValidationStatus.INVALID,
                    message="Value is None",
                    code=CODE_VALUE_NONE,
                )
            )
            return result

        if self._registry.has_field(field_name):
            definition = self._registry.get_field(field_name)
            type_errors = self._check_type(value, definition.value_type)
            for msg in type_errors:
                result.issues.append(
                    ValidationIssue(
                        field_name=field_name,
                        status=ValidationStatus.INVALID,
                        message=msg,
                        code=CODE_TYPE_MISMATCH,
                    )
                )

        if isinstance(value, (int, float)) and value < 0:
            result.issues.append(
                ValidationIssue(
                    field_name=field_name,
                    status=ValidationStatus.INVALID,
                    message="Negative value not allowed",
                    code=CODE_NEGATIVE_VALUE,
                )
            )

        custom_validator = self._validators.get(field_name)
        if custom_validator is not None:
            custom_result = custom_validator(field_name, value, profile_type)
            if custom_result is not None and not custom_result.is_valid:
                for issue in custom_result.issues:
                    result.issues.append(issue)
                result.status = ValidationStatus.INVALID

        return result

    def _check_type(
        self, value: Any, expected: ValueType
    ) -> list[str]:
        result: list[str] = []
        if expected == ValueType.INTEGER and not isinstance(value, int):
            result.append(f"Expected int, got {type(value).__name__}")
        elif expected == ValueType.FLOAT and not isinstance(value, (int, float)):
            result.append(f"Expected float, got {type(value).__name__}")
        elif expected == ValueType.BOOLEAN and not isinstance(value, bool):
            result.append(f"Expected bool, got {type(value).__name__}")
        elif expected == ValueType.STRING and not isinstance(value, str):
            result.append(f"Expected str, got {type(value).__name__}")
        return result
