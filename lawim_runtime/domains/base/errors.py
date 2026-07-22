from __future__ import annotations

from lawim_runtime.runtime.errors import RuntimeError


class DomainRuntimeError(RuntimeError):
    pass


class DomainValidationError(DomainRuntimeError):
    pass


class DomainExecutionError(DomainRuntimeError):
    pass


class DomainProviderRequiredError(DomainRuntimeError):
    pass


class DomainNotFoundError(DomainRuntimeError):
    pass
