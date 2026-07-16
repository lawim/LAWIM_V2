from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProgramSConfig:
    analytics_persistence_enabled: bool = False
    learning_training_enabled: bool = False
    model_deployment_enabled: bool = False
    agent_production_enabled: bool = False
    marketplace_runtime_enabled: bool = False
    multi_tenant_enabled: bool = False
    white_label_enabled: bool = False
    digital_twin_enabled: bool = False
    predictive_intelligence_enabled: bool = False
    future_console_enabled: bool = False
