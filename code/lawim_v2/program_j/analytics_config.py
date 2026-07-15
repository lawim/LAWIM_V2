from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AnalyticsConfig:
    marketing_analytics_enabled: bool = False
    analytics_dashboards_enabled: bool = False
    analytics_recalculation_enabled: bool = False
