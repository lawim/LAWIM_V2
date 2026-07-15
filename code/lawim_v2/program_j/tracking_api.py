from __future__ import annotations

from typing import Any

from .tracking_config import TrackingConfig
from .tracking_models import ExternalChannelCode
from .tracking_services import TrackingResolutionService

_config = TrackingConfig()
_resolver = TrackingResolutionService()


def handle_tracking_get(path: str, query: dict[str, list[str]],
                         actor: dict[str, object]) -> dict[str, Any] | None:
    if not _config.publication_tracking_enabled:
        return {"status": "disabled", "message": "publication_tracking_enabled=false"}

    if path == "tracking/channels":
        return {
            "channels": [{"code": c.value, "name": c.name} for c in ExternalChannelCode],
            "count": len(ExternalChannelCode),
        }

    if path == "tracking/format":
        return {
            "format": "{CHANNEL_CODE}-LAWIM-{PUBLICATION_ID:06d}-{YEAR:04d}-{MONTH:02d}-{SEQ:03d}",
            "example_fb": "FB-LAWIM-000128-2026-06-001",
            "example_wa": "WA-LAWIM-000014-2026-06-014",
            "example_tg": "TG-LAWIM-000045-2026-07-003",
        }

    if path.startswith("tracking/validate/"):
        code = path.split("/")[-1]
        valid = _resolver.validate_tracking_code(code)
        parsed = _resolver.parse(code)
        return {"code": code, "valid": valid, "parsed": parsed}

    if path.startswith("tracking/resolve/"):
        code = path.split("/")[-1]
        parsed = _resolver.parse(code)
        return {"code": code, "parsed": parsed}

    return None


def handle_attribution_get(path: str, query: dict[str, list[str]],
                            actor: dict[str, object]) -> dict[str, Any] | None:
    if not _config.attribution_engine_enabled:
        return {"status": "disabled", "message": "attribution_engine_enabled=false"}

    if path == "attribution/models":
        from .tracking_models import AttributionModel
        return {"models": [m.value for m in AttributionModel]}

    return None


def handle_conversion_get(path: str, query: dict[str, list[str]],
                           actor: dict[str, object]) -> dict[str, Any] | None:
    if not _config.conversion_event_chain_enabled:
        return {"status": "disabled", "message": "conversion_event_chain_enabled=false"}

    if path == "conversion/taxonomy":
        from .tracking_models import TouchpointType
        return {"touchpoint_types": [t.value for t in TouchpointType]}

    return None
