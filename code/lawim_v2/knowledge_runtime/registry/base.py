from __future__ import annotations

import logging
from typing import Any, ClassVar

logger = logging.getLogger(__name__)


class BaseRegistry:
    _LOCKED: ClassVar[bool] = False

    def __init__(self) -> None:
        self._loaded = False

    def _lock(self) -> None:
        self._loaded = True

    def _check_readonly(self) -> None:
        if self._loaded:
            raise RuntimeError(f"{type(self).__name__} is immutable after loading")

    def __setattr__(self, name: str, value: Any) -> None:
        if name != "_loaded" and getattr(self, "_loaded", False):
            raise RuntimeError(f"{type(self).__name__} is immutable after loading")
        super().__setattr__(name, value)

    def __delattr__(self, name: str) -> None:
        raise RuntimeError(f"{type(self).__name__} does not support deletion")

    def summary(self) -> dict[str, Any]:
        return {"type": type(self).__name__, "loaded": self._loaded}
