from __future__ import annotations
from typing import Any
from ..runtime.errors import EngineNotFoundError


class RuntimeRegistry:
    def __init__(self) -> None:
        self._engines: dict[str, Any] = {}

    def register(self, name: str, engine: Any) -> None:
        self._engines[name] = engine

    def unregister(self, name: str) -> None:
        self._engines.pop(name, None)

    def get(self, name: str) -> Any:
        engine = self._engines.get(name)
        if engine is None:
            raise EngineNotFoundError(f"Engine '{name}' not registered")
        return engine

    def list(self) -> list[str]:
        return list(self._engines.keys())

    def get_all(self) -> list[Any]:
        return list(self._engines.values())

    def clear(self) -> None:
        self._engines.clear()
