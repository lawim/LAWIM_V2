"""LAWIM_V2 executable baseline package entrypoint.

This top-level package bridges the repository root and the implementation code
stored under `code/lawim_v2` so the application can run directly from the
workspace without additional environment setup.
"""

from __future__ import annotations

from pathlib import Path
from pkgutil import extend_path

__all__ = ["__version__"]

__version__ = "0.1.0"

__path__ = extend_path(__path__, __name__)  # type: ignore[name-defined]

_code_package = Path(__file__).resolve().parent.parent / "code" / "lawim_v2"
if _code_package.is_dir():
    code_path = str(_code_package)
    if code_path not in __path__:
        __path__.append(code_path)
