"""Make the `code/` directory importable from the repository root."""

from __future__ import annotations

import sys
from pathlib import Path


def _add_code_directory() -> None:
    root = Path(__file__).resolve().parent
    code_dir = root / "code"
    if code_dir.is_dir():
        code_path = str(code_dir)
        if code_path not in sys.path:
            sys.path.insert(0, code_path)


_add_code_directory()
