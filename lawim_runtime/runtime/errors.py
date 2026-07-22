from __future__ import annotations


class RuntimeError(Exception):
    pass


class EventError(RuntimeError):
    pass


class TransitionError(RuntimeError):
    pass


class ProjectNotFoundError(RuntimeError):
    pass


class EngineNotFoundError(RuntimeError):
    pass


class InvalidTransitionError(TransitionError):
    pass


class ValidationError(RuntimeError):
    pass


class PersistenceError(RuntimeError):
    pass


class ConcurrencyError(RuntimeError):
    pass
