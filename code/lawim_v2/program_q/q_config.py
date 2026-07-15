from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProgramQConfig:
    property_model_extensions_enabled: bool = False
    qualification_enhancements_enabled: bool = False
    geography_search_enabled: bool = False
    intent_detection_enabled: bool = False
    matching_scoring_enabled: bool = False
    architecture_open_points_enabled: bool = False
    cognitive_core_enabled: bool = False
