from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TrackingConfig:
    publication_tracking_enabled: bool = False
    attribution_engine_enabled: bool = False
    conversion_event_chain_enabled: bool = False
