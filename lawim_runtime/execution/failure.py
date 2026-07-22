from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class ErrorCategory(str, Enum):
    VALIDATION_FAILURE = "VALIDATION_FAILURE"
    BUSINESS_FAILURE = "BUSINESS_FAILURE"
    TRANSIENT_FAILURE = "TRANSIENT_FAILURE"
    PERMANENT_FAILURE = "PERMANENT_FAILURE"
    TIMEOUT_FAILURE = "TIMEOUT_FAILURE"
    DEPENDENCY_FAILURE = "DEPENDENCY_FAILURE"
    CONCURRENCY_FAILURE = "CONCURRENCY_FAILURE"
    AUTHORIZATION_FAILURE = "AUTHORIZATION_FAILURE"
    CONFIGURATION_FAILURE = "CONFIGURATION_FAILURE"
    EXTERNAL_UNKNOWN = "EXTERNAL_UNKNOWN"
    INTERNAL_BUG = "INTERNAL_BUG"

    @property
    def is_retryable(self) -> bool:
        return self in {
            ErrorCategory.TRANSIENT_FAILURE,
            ErrorCategory.TIMEOUT_FAILURE,
            ErrorCategory.DEPENDENCY_FAILURE,
            ErrorCategory.CONCURRENCY_FAILURE,
            ErrorCategory.EXTERNAL_UNKNOWN,
        }

    @property
    def is_permanent(self) -> bool:
        return self in {
            ErrorCategory.VALIDATION_FAILURE,
            ErrorCategory.BUSINESS_FAILURE,
            ErrorCategory.PERMANENT_FAILURE,
            ErrorCategory.AUTHORIZATION_FAILURE,
            ErrorCategory.CONFIGURATION_FAILURE,
            ErrorCategory.INTERNAL_BUG,
        }


@dataclass(frozen=True)
class ExecutionFailure:
    failure_id: str = field(default_factory=lambda: uuid4().hex[:16])
    execution_id: str = ""
    error_category: ErrorCategory = ErrorCategory.INTERNAL_BUG
    error_code: str = ""
    message: str = ""
    details: dict[str, Any] = field(default_factory=dict)
    cause: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    attempt_number: int = 0
    handler_name: str = ""
    recovery_hint: str = ""
    is_retryable: bool = False


class FailureClassifier:
    def classify(
        self,
        exception: Exception,
        execution_id: str = "",
        attempt_number: int = 0,
        handler_name: str = "",
    ) -> ExecutionFailure:
        category = self._categorize(exception)
        return ExecutionFailure(
            execution_id=execution_id,
            error_category=category,
            error_code=self._error_code(exception, category),
            message=str(exception) or category.value,
            details=self._extract_details(exception),
            cause=self._find_cause(exception),
            attempt_number=attempt_number,
            handler_name=handler_name,
            is_retryable=category.is_retryable,
        )

    def _categorize(self, exception: Exception) -> ErrorCategory:
        exc_name = type(exception).__name__
        exc_str = str(exception).lower()
        exc_mod = type(exception).__module__

        from ..runtime.errors import (
            ValidationError,
            TransitionError,
            InvalidTransitionError,
            ConcurrencyError,
            PersistenceError,
            ProjectNotFoundError,
            EngineNotFoundError,
            RuntimeError,
        )

        type_map: dict[type, ErrorCategory] = {
            ValidationError: ErrorCategory.VALIDATION_FAILURE,
            InvalidTransitionError: ErrorCategory.VALIDATION_FAILURE,
            TransitionError: ErrorCategory.VALIDATION_FAILURE,
            ConcurrencyError: ErrorCategory.CONCURRENCY_FAILURE,
            PersistenceError: ErrorCategory.DEPENDENCY_FAILURE,
            ProjectNotFoundError: ErrorCategory.BUSINESS_FAILURE,
            EngineNotFoundError: ErrorCategory.CONFIGURATION_FAILURE,
        }

        for exc_type, category in type_map.items():
            if isinstance(exception, exc_type):
                return category

        if "timeout" in exc_name.lower() or "timeout" in exc_str:
            return ErrorCategory.TIMEOUT_FAILURE
        if "permission" in exc_name.lower() or "authorization" in exc_str:
            return ErrorCategory.AUTHORIZATION_FAILURE
        if "not found" in exc_str or "not_found" in exc_str or "not found" in exc_name.lower():
            return ErrorCategory.BUSINESS_FAILURE
        if "connection" in exc_name.lower() or "connection" in exc_str:
            return ErrorCategory.DEPENDENCY_FAILURE
        if "lock" in exc_name.lower() or "concurrency" in exc_str:
            return ErrorCategory.CONCURRENCY_FAILURE
        if "validation" in exc_name.lower() or "invalid" in exc_name.lower():
            return ErrorCategory.VALIDATION_FAILURE
        if "config" in exc_name.lower() or "configuration" in exc_str:
            return ErrorCategory.CONFIGURATION_FAILURE
        if exc_name.lower() in ("valueerror", "typeerror", "keyerror", "indexerror", "attributeerror", "importerror", "modulenotfounderror"):
            return ErrorCategory.INTERNAL_BUG
        if "runtime" in exc_str:
            return ErrorCategory.TRANSIENT_FAILURE

        return ErrorCategory.EXTERNAL_UNKNOWN

    def _error_code(
        self, exception: Exception, category: ErrorCategory
    ) -> str:
        return f"{category.value}.{type(exception).__name__}"

    def _extract_details(self, exception: Exception) -> dict[str, Any]:
        details: dict[str, Any] = {
            "exception_type": type(exception).__name__,
            "exception_module": type(exception).__module__,
        }
        args = getattr(exception, "args", None)
        if args:
            details["args"] = [str(a) for a in args]
        return details

    def _find_cause(self, exception: Exception) -> str:
        cause = getattr(exception, "__cause__", None)
        if cause is not None:
            return f"{type(cause).__name__}: {cause}"
        context = getattr(exception, "__context__", None)
        if context is not None:
            return f"{type(context).__name__}: {context}"
        return ""
