from __future__ import annotations

from typing import TYPE_CHECKING

from .errors import DomainNotFoundError

if TYPE_CHECKING:
    from .runtime import DomainRuntime


class DomainRuntimeRegistry:
    def __init__(self) -> None:
        self._runtimes: dict[str, DomainRuntime] = {}
        self._action_to_runtime: dict[str, DomainRuntime] = {}

    def register(self, runtime: DomainRuntime) -> None:
        self._runtimes[runtime.runtime_name] = runtime
        for action in runtime.supported_actions:
            self._action_to_runtime[action] = runtime

    def resolve(self, action_code: str) -> DomainRuntime:
        runtime = self._action_to_runtime.get(action_code)
        if runtime is None:
            raise DomainNotFoundError(f"no domain runtime found for action_code '{action_code}'")
        return runtime

    def list_runtimes(self) -> list[DomainRuntime]:
        return list(self._runtimes.values())

    def count(self) -> int:
        return len(self._runtimes)
