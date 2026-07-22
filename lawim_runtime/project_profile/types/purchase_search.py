from __future__ import annotations

from typing import Any

from ..profile import ProjectProfile


class PurchaseSearchProfile(ProjectProfile):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(profile_type="PURCHASE_SEARCH", **kwargs)
