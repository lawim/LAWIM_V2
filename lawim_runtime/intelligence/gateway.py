from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable

from .request import AIRequest, AITaskType
from .result import AIResult, AIResultStatus

logger = logging.getLogger(__name__)


class AIGatewayMode(str, Enum):
    DISABLED = "AI_DISABLED"
    DETERMINISTIC = "AI_DETERMINISTIC"
    SHADOW = "AI_SHADOW"
    CANARY = "AI_CANARY"
    PRIMARY_WITH_DETERMINISTIC_FALLBACK = "AI_PRIMARY_WITH_DETERMINISTIC_FALLBACK"
    PRIMARY = "AI_PRIMARY"


ExtractionHandler = Callable[[AIRequest], AIResult]


class AIIntelligenceGateway:
    def __init__(
        self,
        mode: AIGatewayMode = AIGatewayMode.DETERMINISTIC,
        deterministic_handler: ExtractionHandler | None = None,
        llm_handler: ExtractionHandler | None = None,
        canary_check: Callable[[str, str], bool] | None = None,
    ) -> None:
        self._mode = mode
        self._deterministic = deterministic_handler
        self._llm = llm_handler
        self._canary_check = canary_check or (lambda uid, pid: False)

    def process(self, request: AIRequest) -> AIResult:
        if self._mode == AIGatewayMode.DISABLED:
            return AIResult(
                request_id=request.request_id,
                status=AIResultStatus.UNAVAILABLE,
                task_type=request.task_type.value,
                correlation_id=request.correlation_id,
            )

        if self._mode == AIGatewayMode.DETERMINISTIC:
            return self._call_deterministic(request)

        if self._mode == AIGatewayMode.SHADOW:
            det_result = self._call_deterministic(request)
            llm_result = self._call_llm_safe(request)
            return det_result

        if self._mode == AIGatewayMode.CANARY:
            uid = request.metadata.get("user_id", "")
            pid = request.project_id
            if self._canary_check(uid, pid):
                return self._call_llm_safe(request)
            return self._call_deterministic(request)

        if self._mode == AIGatewayMode.PRIMARY_WITH_DETERMINISTIC_FALLBACK:
            llm_result = self._call_llm_safe(request)
            if llm_result.status == AIResultStatus.SUCCESS:
                return llm_result
            return self._call_deterministic(request)

        if self._mode == AIGatewayMode.PRIMARY:
            return self._call_llm_safe(request)

        return self._call_deterministic(request)

    def _call_deterministic(self, request: AIRequest) -> AIResult:
        if self._deterministic:
            return self._deterministic(request)
        return AIResult(
            request_id=request.request_id,
            status=AIResultStatus.UNAVAILABLE,
            task_type=request.task_type.value,
            correlation_id=request.correlation_id,
        )

    def _call_llm_safe(self, request: AIRequest) -> AIResult:
        if self._llm:
            try:
                return self._llm(request)
            except Exception as e:
                logger.error("llm handler error: %s", e)
                return AIResult(
                    request_id=request.request_id,
                    status=AIResultStatus.FAILED,
                    task_type=request.task_type.value,
                    correlation_id=request.correlation_id,
                    metadata={"error": str(e)},
                )
        return AIResult(
            request_id=request.request_id,
            status=AIResultStatus.UNAVAILABLE,
            task_type=request.task_type.value,
            correlation_id=request.correlation_id,
        )

    @property
    def mode(self) -> AIGatewayMode:
        return self._mode

    def set_mode(self, mode: AIGatewayMode) -> None:
        self._mode = mode
