from __future__ import annotations

import logging
from typing import Any

from . import ChannelDeliveryRequest, ChannelDeliveryResult

logger = logging.getLogger(__name__)


def send_green_api_message(request: ChannelDeliveryRequest) -> ChannelDeliveryResult:
    provider_id = f"green_api_{request.correlation_id[:8]}"
    logger.info(
        "green_api send simulated: to=%s text_len=%d provider_id=%s",
        request.recipient_id,
        len(request.text),
        provider_id,
    )
    return ChannelDeliveryResult(
        success=True,
        provider_message_id=provider_id,
        status_code=200,
        metadata={"simulated": True, "provider": "green_api"},
    )
