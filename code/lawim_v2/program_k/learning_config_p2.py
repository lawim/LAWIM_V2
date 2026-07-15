from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LearningConfigP2:
    learning_dataset_builder_enabled: bool = False
    learning_analysis_enabled: bool = False
    learning_proposal_engine_enabled: bool = False
    learning_experiments_enabled: bool = False
    knowledge_evolution_packages_enabled: bool = False
