"""ExpectedSpecLoader — charge la spécification Gold depuis les fichiers du corpus.

Garantie : ne JAMAIS charger depuis le même chemin que l'exécution runtime.
"""

import json
import os
from typing import Any, Dict, Optional


class ExpectedSpecLoader:
    """Loads expected specification from Gold Corpus conversation directory."""

    def __init__(self, spec_dir: str):
        self._spec_dir = spec_dir
        self._loaded_paths = {}

    def load_all(self) -> Dict[str, Any]:
        """Load all expected spec files from the spec directory."""
        spec = {}
        mappings = [
            ("expected_state.json", "expected_state"),
            ("expected_business.json", "expected_business"),
            ("expected_language.json", "expected_language"),
            ("expected_runtime.json", "expected_runtime"),
            ("expected_questions.json", "expected_questions"),
            ("expected_assertions.json", "expected_assertions"),
        ]
        for fname, key in mappings:
            path = os.path.join(self._spec_dir, fname)
            if os.path.isfile(path):
                with open(path) as f:
                    spec[key] = json.load(f)
                self._loaded_paths[key] = path

        conversation_path = os.path.join(self._spec_dir, "conversation.json")
        if os.path.isfile(conversation_path):
            with open(conversation_path) as f:
                spec["conversation"] = json.load(f)
            self._loaded_paths["conversation"] = conversation_path

        return spec

    @property
    def loaded_paths(self) -> Dict[str, str]:
        """Return mapping of spec key to file path."""
        return dict(self._loaded_paths)

    @property
    def spec_dir(self) -> str:
        return self._spec_dir

    def get_expected_intent(self, spec: Dict[str, Any]) -> str:
        return spec.get("expected_state", {}).get("intent", "")

    def get_expected_qualification(self, spec: Dict[str, Any]) -> str:
        return spec.get("expected_state", {}).get("qualification_status", "")

    def get_expected_slots(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        return spec.get("expected_state", {}).get("slots_filled", {})

    def get_expected_next_action(self, spec: Dict[str, Any]) -> str:
        return spec.get("expected_state", {}).get("next_action", "")

    def get_expected_business_action(self, spec: Dict[str, Any]) -> str:
        return spec.get("expected_business", {}).get("business_action", "")

    def get_expected_language(self, spec: Dict[str, Any]) -> str:
        return spec.get("expected_language", {}).get("responses_language", "")

    def get_assertions(self, spec: Dict[str, Any]) -> list:
        return spec.get("expected_assertions", {}).get("assertions", [])
