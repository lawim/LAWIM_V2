from __future__ import annotations
import logging
from .simulator import Simulator
from .scenarios import SCENARIOS
from .dataset_builder import DatasetBuilder

LOGGER = logging.getLogger(__name__)


class Orchestrator:
    def __init__(self, lawim_pipeline=None):
        self.simulator = Simulator(lawim_pipeline=lawim_pipeline)
        self.dataset_builder = DatasetBuilder()

    def run_multi_agent(self, count: int = 1000, languages: list[str] | None = None) -> dict:
        LOGGER.info("Running multi-agent factory: %d conversations", count)
        scenarios = [s for s in SCENARIOS if languages is None or s.language in languages]
        results = self.simulator.simulate_all(scenarios * max(1, count // len(scenarios)))
        accepted = [r for r in results if r["accepted"]]
        dataset = self.dataset_builder.build(accepted)
        return {
            "generated": len(results),
            "accepted": len(accepted),
            "acceptance_rate": round(len(accepted) / max(len(results), 1) * 100, 1),
            "dataset_size": len(dataset),
        }

    def run_procedural(self, count: int = 10000) -> dict:
        LOGGER.info("Running procedural factory: %d conversations", count)
        results = self.simulator.simulate_all(SCENARIOS * (count // len(SCENARIOS) + 1))[:count]
        accepted = [r for r in results if r["accepted"]]
        dataset = self.dataset_builder.build(accepted)
        return {
            "generated": len(results),
            "accepted": len(accepted),
            "acceptance_rate": round(len(accepted) / max(len(results), 1) * 100, 1),
            "dataset_size": len(dataset),
        }
