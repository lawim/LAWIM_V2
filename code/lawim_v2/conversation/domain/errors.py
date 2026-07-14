from __future__ import annotations


class ConversationError(Exception):
    def __init__(self, message: str, code: str = "conversation_error", details: dict | None = None):
        self.code = code
        self.details = details or {}
        super().__init__(message)


class DecisionError(ConversationError):
    def __init__(self, message: str, decision_id: str | None = None):
        super().__init__(message, code="decision_error", details={"decision_id": decision_id})


class StateError(ConversationError):
    def __init__(self, message: str, current_state: str | None = None, event: str | None = None):
        super().__init__(
            message,
            code="state_error",
            details={"current_state": current_state, "event": event},
        )


class ExtractionError(ConversationError):
    def __init__(self, message: str, field: str | None = None):
        super().__init__(message, code="extraction_error", details={"field": field})


class ValidationError(ConversationError):
    def __init__(self, message: str, constraints: list[str] | None = None):
        super().__init__(message, code="validation_error", details={"constraints": constraints})
