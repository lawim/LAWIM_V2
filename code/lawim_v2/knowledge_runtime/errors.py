"""Structured error classes for the Knowledge Runtime."""

from __future__ import annotations


class KnowledgeError(RuntimeError):
    """Base exception for all Knowledge Runtime errors."""


class KnowledgeSourceNotFound(KnowledgeError):
    """Raised when a knowledge source file cannot be located."""

    def __init__(self, source_path: str, message: str | None = None) -> None:
        self.source_path = source_path
        super().__init__(message or f"Knowledge source not found: {source_path}")


class KnowledgeSchemaError(KnowledgeError):
    """Raised when a knowledge document fails schema validation."""

    def __init__(self, source_path: str, detail: str) -> None:
        self.source_path = source_path
        self.detail = detail
        super().__init__(f"Schema error in {source_path}: {detail}")


class KnowledgeReferenceError(KnowledgeError):
    """Raised when a cross-reference between knowledge entities is invalid."""

    def __init__(self, source_id: str, target_type: str, target_id: str, message: str | None = None) -> None:
        self.source_id = source_id
        self.target_type = target_type
        self.target_id = target_id
        super().__init__(message or f"Invalid reference from {source_id} to {target_type}:{target_id}")


class KnowledgeDuplicateError(KnowledgeError):
    """Raised when a duplicate knowledge identifier is detected."""

    def __init__(self, identifier: str, registry: str, message: str | None = None) -> None:
        self.identifier = identifier
        self.registry = registry
        super().__init__(message or f"Duplicate identifier '{identifier}' in {registry}")


class KnowledgeCircularReferenceError(KnowledgeError):
    """Raised when a circular reference (e.g. taxonomy hierarchy) is detected."""

    def __init__(self, chain: list[str], message: str | None = None) -> None:
        self.chain = chain
        super().__init__(message or f"Circular reference detected: {' -> '.join(chain)}")


class KnowledgeValidationError(KnowledgeError):
    """Raised when validation of knowledge data fails."""

    def __init__(self, message: str, details: list[dict[str, object]] | None = None) -> None:
        self.details = details or []
        super().__init__(message)


class KnowledgeNotLoadedError(KnowledgeError):
    """Raised when an operation is attempted before knowledge is loaded."""

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or "Knowledge runtime has not been loaded. Call load_all() first.")
