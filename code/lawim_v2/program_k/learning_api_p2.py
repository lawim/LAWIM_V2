from __future__ import annotations

from typing import Any

from .learning_config_p2 import LearningConfigP2
from .learning_datasets import LearningDatasetBuilder, LearningDatasetRegistry, LearningDataQualityService, feature_catalog
from .learning_analysis import (
    EvolutionPackageService,
    ExperimentEvaluationService,
    LearningAnalysisEngine,
    LearningExperimentService,
    LearningHypothesisService,
    LearningProposalEngine,
    VersionService,
)

_config = LearningConfigP2()
_dataset_reg = LearningDatasetRegistry()
_dataset_builder = LearningDatasetBuilder()
_data_quality = LearningDataQualityService()
_analysis = LearningAnalysisEngine()
_hypotheses = LearningHypothesisService()
_proposals = LearningProposalEngine()
_experiments = LearningExperimentService()
_evaluation = ExperimentEvaluationService()
_evolutions = EvolutionPackageService()
_versions = VersionService()


def handle_learning_p2_get(path: str, query: dict[str, list[str]],
                            actor: dict[str, object]) -> dict[str, Any] | None:
    if path == "learning/datasets":
        if not _config.learning_dataset_builder_enabled:
            return {"status": "disabled"}
        return {"datasets": [d.to_dict() for d in _dataset_reg.list()],
                "count": _dataset_reg.count()}

    if path == "learning/datasets/features":
        if not _config.learning_dataset_builder_enabled:
            return {"status": "disabled"}
        return {"features": feature_catalog.to_dict_list(), "count": feature_catalog.count()}

    if path.startswith("learning/datasets/features/"):
        code = path.split("/")[-1]
        f = feature_catalog.get(code.upper())
        if f is None:
            return {"error": "feature_not_found"}
        return {"feature": f.to_dict()}

    if path == "learning/analyses":
        if not _config.learning_analysis_enabled:
            return {"status": "disabled"}
        return {"analyses": ["outcome_trend", "cohort_comparison"]}

    if path == "learning/hypotheses":
        if not _config.learning_proposal_engine_enabled:
            return {"status": "disabled"}
        return {"hypotheses": [h.to_dict() for h in _hypotheses.list()]}

    if path == "learning/proposals":
        if not _config.learning_proposal_engine_enabled:
            return {"status": "disabled"}
        return {"proposals": [p.to_dict() for p in _proposals.list()]}

    if path == "learning/experiments":
        if not _config.learning_experiments_enabled:
            return {"status": "disabled"}
        return {"experiments": [e.to_dict() for e in _experiments.list()]}

    if path == "learning/evolution-packages":
        if not _config.knowledge_evolution_packages_enabled:
            return {"status": "disabled"}
        return {"packages": [p.to_dict() for p in _evolutions.list()]}

    if path == "learning/versions":
        return {"versions": [v.to_dict() for v in _versions.list_all()]}

    return None
