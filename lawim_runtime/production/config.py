from __future__ import annotations

import os
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class AppEnvironment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TEST = "test"


@dataclass
class ProductionConfig:
    env: AppEnvironment = AppEnvironment.DEVELOPMENT

    host: str = "127.0.0.1"
    port: int = 3000
    log_level: str = "info"
    public_base_url: str = "http://localhost:3000"

    db_driver: str = "sqlite"
    db_path: str = "data/runtime/lawim.sqlite3"
    database_url: str = ""
    db_pool_size: int = 10
    db_max_overflow: int = 20

    session_ttl_seconds: int = 604800
    max_upload_bytes: int = 5_242_880
    max_json_body_bytes: int = 1_048_576

    ai_intelligence_enabled: bool = False
    ai_extraction_enabled: bool = False
    ai_response_writer_enabled: bool = False
    ai_knowledge_enabled: bool = False
    ai_rag_enabled: bool = False
    ai_shadow_mode: bool = True
    ai_provider_calls_enabled: bool = False
    ai_budget_monthly_cents: int = 0
    ai_max_cost_per_call_cents: int = 10

    provider_openai_enabled: bool = False
    provider_openai_model: str = "gpt-4o-mini"
    provider_anthropic_enabled: bool = False
    provider_anthropic_model: str = "claude-3-haiku-20240307"
    provider_gemini_enabled: bool = False
    provider_gemini_model: str = "gemini-2.0-flash"
    provider_deepseek_enabled: bool = False
    provider_deepseek_model: str = "deepseek-chat"

    whatsapp_adapter_enabled: bool = False
    telegram_adapter_enabled: bool = False
    web_interaction_enabled: bool = False
    api_interaction_enabled: bool = False
    interaction_gateway_enabled: bool = False

    metrics_enabled: bool = True
    tracing_enabled: bool = False
    structured_logging: bool = True

    rate_limit_per_second: int = 10
    rate_limit_burst: int = 20

    def validate(self) -> list[str]:
        errors: list[str] = []
        if self.env == AppEnvironment.PRODUCTION:
            if not self.database_url and self.db_driver == "postgresql":
                errors.append("DATABASE_URL is required in production with PostgreSQL driver")
            if not self.public_base_url.startswith("https"):
                errors.append("PUBLIC_BASE_URL must use HTTPS in production")
            if self.ai_provider_calls_enabled and self.ai_budget_monthly_cents <= 0:
                errors.append("AI budget must be configured when provider calls are enabled")
        return errors


def load_from_env() -> ProductionConfig:
    cfg = ProductionConfig(
        env=AppEnvironment(os.getenv("APP_ENV", "development")),
        host=os.getenv("LAWIM_HOST", "127.0.0.1"),
        port=int(os.getenv("LAWIM_PORT", "3000")),
        log_level=os.getenv("LOG_LEVEL", "info"),
        public_base_url=os.getenv("PUBLIC_BASE_URL", "http://localhost:3000"),
        db_driver=os.getenv("LAWIM_DB_DRIVER", "sqlite"),
        db_path=os.getenv("LAWIM_DB_PATH", "data/runtime/lawim.sqlite3"),
        database_url=os.getenv("LAWIM_DATABASE_URL", ""),
        ai_intelligence_enabled=os.getenv("LROS_AI_INTELLIGENCE_ENABLED", "false").lower() == "true",
        ai_extraction_enabled=os.getenv("LROS_AI_EXTRACTION_ENABLED", "false").lower() == "true",
        ai_response_writer_enabled=os.getenv("LROS_AI_RESPONSE_WRITER_ENABLED", "false").lower() == "true",
        ai_shadow_mode=os.getenv("LROS_AI_SHADOW_MODE", "true").lower() == "true",
        ai_provider_calls_enabled=os.getenv("LROS_AI_PROVIDER_CALLS_ENABLED", "false").lower() == "true",
        ai_budget_monthly_cents=int(os.getenv("LROS_AI_BUDGET_MONTHLY_CENTS", "0")),
        metrics_enabled=os.getenv("LAWIM_METRICS_ENABLED", "true").lower() == "true",
    )
    validation_errors = cfg.validate()
    for err in validation_errors:
        logger.error("production config validation error: %s", err)
    return cfg
