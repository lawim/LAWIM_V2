from __future__ import annotations


class RegistryError(ValueError):
    """Base error for all registry operations."""

    def __init__(self, message: str, code: str = "registry_error", details: dict | None = None):
        self.code = code
        self.details = details or {}
        super().__init__(message)


class RegistryNotFoundError(RegistryError):
    def __init__(self, message: str, identifier: str | None = None):
        super().__init__(message, code="registry_not_found", details={"identifier": identifier})


class RegistryValidationError(RegistryError):
    def __init__(self, message: str, validation_errors: list[str] | None = None):
        super().__init__(
            message, code="registry_validation_error", details={"validation_errors": validation_errors or []}
        )


class DuplicateEntryError(RegistryError):
    def __init__(self, message: str, identifier: str | None = None, existing_id: str | None = None):
        super().__init__(
            message,
            code="duplicate_entry",
            details={"identifier": identifier, "existing_id": existing_id},
        )


class AmbiguousAliasError(RegistryError):
    def __init__(self, message: str, alias: str | None = None, matches: list[str] | None = None):
        super().__init__(
            message,
            code="ambiguous_alias",
            details={"alias": alias, "matches": matches or []},
        )


class CycleDetectionError(RegistryValidationError):
    def __init__(self, message: str, cycle_path: list[str] | None = None):
        super().__init__(message, validation_errors=[message])
        self.code = "cycle_detected"
        self.details["cycle_path"] = cycle_path or []


class MissingParentError(RegistryValidationError):
    def __init__(self, message: str, child_id: str | None = None, missing_parent_id: str | None = None):
        super().__init__(message, validation_errors=[message])
        self.code = "missing_parent"
        self.details.update({"child_id": child_id, "missing_parent_id": missing_parent_id})


class SelectionError(RegistryError):
    def __init__(self, message: str, code: str = "selection_error", details: dict | None = None):
        super().__init__(message, code=code, details=details)


class AmbiguousSelectionError(SelectionError):
    def __init__(self, message: str, candidates: list[str] | None = None):
        super().__init__(
            message, code="ambiguous_selection", details={"candidates": candidates or []}
        )


class NoMatchError(SelectionError):
    def __init__(self, message: str, context: dict | None = None):
        super().__init__(message, code="no_match", details=context or {})


class TraceValidationError(RegistryValidationError):
    def __init__(self, message: str, trace_id: str | None = None, missing_links: list[str] | None = None):
        super().__init__(message, validation_errors=[message])
        self.code = "trace_validation_error"
        self.details.update({"trace_id": trace_id, "missing_links": missing_links or []})
