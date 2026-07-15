from __future__ import annotations

from typing import Any

from .analytics_config import AnalyticsConfig
from .analytics_registry import get_metric, list_metrics, to_dict_list

_config = AnalyticsConfig()


def handle_analytics_get(path: str, query: dict[str, list[str]],
                          actor: dict[str, object]) -> dict[str, Any] | None:
    if not _config.marketing_analytics_enabled:
        return {"status": "disabled", "message": "marketing_analytics_enabled=false"}

    if path == "analytics/metrics":
        return {"metrics": to_dict_list(), "count": len(list_metrics())}

    if path.startswith("analytics/metrics/"):
        code = path.split("/")[-1]
        metric = get_metric(code.upper())
        if metric is None:
            return {"error": f"Unknown metric: {code}"}
        return {"metric": metric.to_dict()}

    if path == "analytics/dimensions":
        from .analytics_models import ANALYTICS_DIMENSIONS
        return {"dimensions": list(ANALYTICS_DIMENSIONS), "count": len(ANALYTICS_DIMENSIONS)}

    return None


def handle_analytics_dashboard_get(path: str, query: dict[str, list[str]],
                                    actor: dict[str, object]) -> dict[str, Any] | None:
    if not _config.analytics_dashboards_enabled:
        return {"status": "disabled", "message": "analytics_dashboards_enabled=false"}
    return None


def handle_analytics_recalculation_get(path: str, query: dict[str, list[str]],
                                        actor: dict[str, object]) -> dict[str, Any] | None:
    if not _config.analytics_recalculation_enabled:
        return {"status": "disabled", "message": "analytics_recalculation_enabled=false"}
    return None
