from __future__ import annotations

from typing import Any

from .matrices import (
    ALL_MATRICES,
    MATRIX_INDEX,
    QualificationMatrix,
)


class MatrixValidationError(ValueError):
    pass


class DuplicateMatrixError(MatrixValidationError):
    pass


class MatrixRegistry:
    def __init__(self, matrices: list[QualificationMatrix] | None = None):
        self._matrices: dict[str, list[QualificationMatrix]] = {}
        self._by_intent: dict[str, list[QualificationMatrix]] = {}
        if matrices is not None:
            for m in matrices:
                self.register(m)
        else:
            self._load_defaults()

    def _load_defaults(self) -> None:
        for key, matrices in MATRIX_INDEX.items():
            for m in matrices:
                self._register_single(m)

    def _register_single(self, matrix: QualificationMatrix) -> None:
        key = self._key(matrix.intent, matrix.transaction_type, matrix.property_type)
        if key in self._matrices:
            raise DuplicateMatrixError(
                f"Duplicate matrix for intent={matrix.intent}, "
                f"transaction_type={matrix.transaction_type}, "
                f"property_type={matrix.property_type}"
            )
        self._matrices[key] = matrix
        self._by_intent.setdefault(matrix.intent, []).append(matrix)

    def register(self, matrix: QualificationMatrix) -> None:
        self._register_single(matrix)

    def unregister(self, intent: str, transaction_type: str, property_type: str) -> None:
        key = self._key(intent, transaction_type, property_type)
        removed = self._matrices.pop(key, None)
        if removed:
            intent_list = self._by_intent.get(intent, [])
            if removed in intent_list:
                intent_list.remove(removed)

    def get(
        self,
        intent: str,
        transaction_type: str | None = None,
        property_type: str | None = None,
    ) -> QualificationMatrix | None:
        if transaction_type is not None and property_type is not None:
            key = self._key(intent, transaction_type, property_type)
            return self._matrices.get(key)
        candidates = self._by_intent.get(intent, [])
        if not candidates:
            return None
        if transaction_type is None and property_type is None:
            return candidates[0] if candidates else None
        for m in candidates:
            if transaction_type and m.transaction_type != transaction_type:
                continue
            if property_type and m.property_type != property_type:
                continue
            return m
        return candidates[0] if candidates else None

    def get_by_intent(self, intent: str) -> list[QualificationMatrix]:
        return list(self._by_intent.get(intent, []))

    def all_matrices(self) -> list[QualificationMatrix]:
        return list(self._matrices.values())

    def all_intents(self) -> set[str]:
        return set(self._by_intent.keys())

    def count(self) -> int:
        return len(self._matrices)

    @staticmethod
    def _key(intent: str, transaction_type: str, property_type: str) -> str:
        return f"{intent}::{transaction_type}::{property_type}"

    @staticmethod
    def validate_matrix(matrix: QualificationMatrix) -> list[str]:
        errors: list[str] = []
        if not matrix.intent:
            errors.append("intent is required")
        if not matrix.transaction_type:
            errors.append("transaction_type is required")
        if not matrix.property_type:
            errors.append("property_type is required")
        if matrix.readiness_threshold < 0.0 or matrix.readiness_threshold > 1.0:
            errors.append("readiness_threshold must be between 0.0 and 1.0")
        for f in matrix.required_fields:
            if f not in matrix.field_priority and matrix.field_priority:
                errors.append(f"required field '{f}' missing from field_priority")
        for f in matrix.recommended_fields:
            if f not in matrix.field_priority and matrix.field_priority:
                errors.append(f"recommended field '{f}' missing from field_priority")
        for f in matrix.optional_fields:
            if f not in matrix.field_priority and matrix.field_priority:
                errors.append(f"optional field '{f}' missing from field_priority")
        all_known = set(matrix.required_fields) | set(matrix.recommended_fields) | set(matrix.optional_fields)
        for f in matrix.field_priority:
            if f not in all_known:
                errors.append(f"field_priority references '{f}' but it is not in required/recommended/optional")
        return errors

    def validate_all(self) -> dict[str, list[str]]:
        all_errors: dict[str, list[str]] = {}
        for key, matrix in self._matrices.items():
            errs = self.validate_matrix(matrix)
            if errs:
                all_errors[key] = errs
        return all_errors


_default_registry: MatrixRegistry | None = None


def get_registry() -> MatrixRegistry:
    global _default_registry
    if _default_registry is None:
        _default_registry = MatrixRegistry()
    return _default_registry


def reset_registry() -> None:
    global _default_registry
    _default_registry = None
