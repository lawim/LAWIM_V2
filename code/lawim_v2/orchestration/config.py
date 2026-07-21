from __future__ import annotations

DEFAULT_CONNECT_TIMEOUT: float = 10.0
DEFAULT_READ_TIMEOUT: float = 20.0
DEFAULT_TOTAL_TIMEOUT: float = 30.0
DEFAULT_MAX_RETRIES: int = 1
DEFAULT_BACKOFF_SECONDS: float = 1.0
DEFAULT_CIRCUIT_BREAKER_THRESHOLD: int = 3
DEFAULT_CIRCUIT_BREAKER_RECOVERY_SECONDS: float = 60.0
DEFAULT_PROVIDER_CHAIN: list[str] = ["deepseek", "openai", "gemini_primary", "gemini_secondary", "internal"]
