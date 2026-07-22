from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from math import pow
from random import uniform
from typing import Any


class BackoffStrategy(str, Enum):
    NONE = "NONE"
    FIXED = "FIXED"
    LINEAR = "LINEAR"
    EXPONENTIAL = "EXPONENTIAL"


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 1
    initial_delay: float = 1.0
    max_delay: float = 60.0
    backoff_strategy: BackoffStrategy = BackoffStrategy.EXPONENTIAL
    backoff_multiplier: float = 2.0
    jitter: float = 0.1
    retryable_error_types: tuple[str, ...] = (
        "TRANSIENT_FAILURE",
        "TIMEOUT_FAILURE",
        "DEPENDENCY_FAILURE",
        "CONCURRENCY_FAILURE",
        "EXTERNAL_UNKNOWN",
    )
    non_retryable_error_types: tuple[str, ...] = (
        "VALIDATION_FAILURE",
        "BUSINESS_FAILURE",
        "PERMANENT_FAILURE",
        "AUTHORIZATION_FAILURE",
        "CONFIGURATION_FAILURE",
        "INTERNAL_BUG",
    )
    retry_deadline: float = 300.0


@dataclass(frozen=True)
class RetryDecision:
    should_retry: bool = False
    delay_seconds: float = 0.0
    reason: str = ""


class RetryPolicyEvaluator:
    def __init__(self, policy: RetryPolicy) -> None:
        self._policy = policy

    @property
    def policy(self) -> RetryPolicy:
        return self._policy

    def decide(
        self,
        retry_count: int,
        error_category: str,
        elapsed_time: float = 0.0,
    ) -> RetryDecision:
        if error_category in self._policy.non_retryable_error_types:
            return RetryDecision(
                should_retry=False,
                reason=f"Error category '{error_category}' is non-retryable",
            )

        if retry_count >= self._policy.max_attempts:
            return RetryDecision(
                should_retry=False,
                reason=f"Max attempts ({self._policy.max_attempts}) reached",
            )

        if error_category not in self._policy.retryable_error_types:
            return RetryDecision(
                should_retry=False,
                reason=f"Error category '{error_category}' is not configured as retryable",
            )

        if elapsed_time >= self._policy.retry_deadline:
            return RetryDecision(
                should_retry=False,
                reason=f"Retry deadline ({self._policy.retry_deadline}s) exceeded",
            )

        delay = self.compute_delay(retry_count)
        return RetryDecision(
            should_retry=True,
            delay_seconds=delay,
            reason=f"Retry attempt {retry_count + 1}/{self._policy.max_attempts}",
        )

    def compute_delay(self, retry_count: int) -> float:
        strategy = self._policy.backoff_strategy
        if strategy == BackoffStrategy.NONE:
            return 0.0
        elif strategy == BackoffStrategy.FIXED:
            delay = self._policy.initial_delay
        elif strategy == BackoffStrategy.LINEAR:
            delay = self._policy.initial_delay * (
                1 + self._policy.backoff_multiplier * retry_count
            )
        elif strategy == BackoffStrategy.EXPONENTIAL:
            delay = self._policy.initial_delay * pow(
                self._policy.backoff_multiplier, retry_count
            )
        else:
            delay = self._policy.initial_delay

        delay = min(delay, self._policy.max_delay)

        if self._policy.jitter > 0.0:
            jitter_range = delay * self._policy.jitter
            delay += uniform(-jitter_range, jitter_range)
            delay = max(0.0, delay)

        return round(delay, 3)
