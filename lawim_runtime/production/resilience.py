from __future__ import annotations

import time
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable

logger = logging.getLogger(__name__)


class CircuitState(str, Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5
    recovery_timeout_seconds: float = 30.0
    half_open_max_calls: int = 3


class CircuitBreaker:
    def __init__(self, name: str = "default", config: CircuitBreakerConfig | None = None) -> None:
        self._name = name
        self._config = config or CircuitBreakerConfig()
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time = 0.0
        self._half_open_calls = 0

    @property
    def state(self) -> CircuitState:
        return self._state

    def call(self, fn: Callable[[], Any]) -> Any:
        if self._state == CircuitState.OPEN:
            if time.time() - self._last_failure_time >= self._config.recovery_timeout_seconds:
                self._state = CircuitState.HALF_OPEN
                self._half_open_calls = 0
                logger.info("circuit breaker %s: half-open", self._name)
            else:
                raise RuntimeError(f"circuit breaker {self._name} is OPEN")

        if self._state == CircuitState.HALF_OPEN and self._half_open_calls >= self._config.half_open_max_calls:
            raise RuntimeError(f"circuit breaker {self._name}: too many half-open calls")

        try:
            if self._state == CircuitState.HALF_OPEN:
                self._half_open_calls += 1
            result = fn()
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self) -> None:
        self._failure_count = 0
        if self._state == CircuitState.HALF_OPEN:
            self._state = CircuitState.CLOSED
            logger.info("circuit breaker %s: closed (recovered)", self._name)

    def _on_failure(self) -> None:
        self._failure_count += 1
        self._last_failure_time = time.time()
        if self._failure_count >= self._config.failure_threshold:
            self._state = CircuitState.OPEN
            logger.warning("circuit breaker %s: OPEN (threshold=%d)", self._name, self._config.failure_threshold)

    def reset(self) -> None:
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._half_open_calls = 0


class RetryPolicy:
    def __init__(self, max_retries: int = 3, base_delay_seconds: float = 1.0, max_delay_seconds: float = 30.0) -> None:
        self.max_retries = max_retries
        self.base_delay_seconds = base_delay_seconds
        self.max_delay_seconds = max_delay_seconds

    def execute(self, fn: Callable[[], Any], should_retry: Callable[[Exception], bool] | None = None) -> Any:
        last_exception: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                return fn()
            except Exception as e:
                last_exception = e
                if should_retry and not should_retry(e):
                    raise
                if attempt < self.max_retries:
                    delay = min(self.base_delay_seconds * (2 ** attempt), self.max_delay_seconds)
                    logger.warning("retry attempt %d/%d failed: %s, retrying in %.1fs", attempt + 1, self.max_retries, e, delay)
                    time.sleep(delay)
        raise last_exception  # type: ignore[misc]


class RateLimiter:
    def __init__(self, max_per_second: int = 10, burst: int = 20) -> None:
        self._max_per_second = max_per_second
        self._burst = burst
        self._tokens = float(burst)
        self._last_refill = time.time()

    def acquire(self) -> bool:
        now = time.time()
        elapsed = now - self._last_refill
        self._tokens = min(self._burst, self._tokens + elapsed * self._max_per_second)
        self._last_refill = now
        if self._tokens >= 1:
            self._tokens -= 1
            return True
        return False
