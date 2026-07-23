from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from lawim_runtime.project_profile.candidate import CandidateUpdate
from lawim_runtime.project_profile.values import ExtractionMethod


@dataclass
class ExtractionResult:
    candidates: list[CandidateUpdate] = field(default_factory=list)
    raw_text: str = ""
    language_hint: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


class DeterministicExtractor:

    PATTERNS: dict[str, list[tuple[str, type, str]]] = {
        "property_type": [
            (r"\b(appartement|appart)\b", str, "apartment"),
            (r"\b(studio)\b", str, "studio"),
            (r"\b(maison|villa)\b", str, "house"),
            (r"\b(terrain)\b", str, "land"),
            (r"\b(bureau|local commercial)\b", str, "commercial"),
        ],
        "bedrooms": [
            (r"(\d+)\s*(?:chambres?|pi[èe]ces?|rooms?)", int, ""),
            (r"(?:chambres?|pi[èe]ces?|rooms?)\s*(\d+)", int, ""),
        ],
        "city": [
            (r"(?:à|a|near|in|at)\s+([A-Za-zéèêëàâùûüôöîïç\s-]+?)(?:[,.]|\s+(?:dans|avec|pour|budget|maximum|max|à|a)\b|$)", str, ""),
        ],
        "district": [
            (r"(?:à|a|near|in|at)\s+([A-Za-zéèêëàâùûüôöîïç\s-]+?)(?:[,.]|\s+(?:dans|avec|pour|budget|maximum|max|à|a)\b|$)", str, ""),
        ],
        "max_budget": [
            (r"(?:budget|maximum|max|jusqu[’']?[àa])\s*(?:de\s*)?(\d[\d\s]*)\s*(?:FCFA|francs?|fcfa|XOF|\€|euros?)", float, ""),
            (r"(\d[\d\s]*)\s*(?:FCFA|francs?|fcfa|XOF|\€|euros?)(?:\s*(?:de\s*)?(?:budget|maximum|max))?", float, ""),
        ],
        "min_budget": [
            (r"(?:à\s*partir\s*de|minimum|min)\s*(?:de\s*)?(\d[\d\s]*)\s*(?:FCFA|francs?|fcfa|XOF|\€|euros?)", float, ""),
        ],
        "move_in_date": [
            (r"(?:pour|en|dès|des|à partir du?|rentrée?|entrer?|emménager?)\s*(septembre|octobre|novembre|décembre|janvier|février|mars|avril|mai|juin|juillet|août)(?:\s*\d{4})?", str, ""),
            (r"(?:pour|en|dès|des)\s*(le\s*)?(\d{1,2}\s*(?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)(?:\s*\d{4})?)", str, ""),
        ],
        "availability": [
            (r"(?:disponible|libre|suis disponible)\s*(?:le|les|ce)?\s*(samedi|dimanche|lundi|mardi|mercredi|jeudi|vendredi)", str, ""),
        ],
    }

    def extract(self, text: str, project_id: str = "", correlation_id: str = "") -> ExtractionResult:
        candidates: list[CandidateUpdate] = []
        text_lower = text.lower()

        for field_name, patterns in self.PATTERNS.items():
            for pattern, value_type, default_value in patterns:
                match = re.search(pattern, text_lower)
                if match:
                    raw = match.group(1).strip()
                    try:
                        if value_type == int:
                            cleaned = re.sub(r'\s+', '', raw)
                            parsed = int(cleaned)
                        elif value_type == float:
                            cleaned = re.sub(r'\s+', '', raw)
                            parsed = float(cleaned)
                        else:
                            parsed = raw
                    except (ValueError, TypeError):
                        continue

                    candidates.append(CandidateUpdate(
                        project_id=project_id,
                        field_name=field_name,
                        raw_value=match.group(0),
                        proposed_value=parsed if default_value == "" else default_value,
                        confidence=0.8,
                        source_type=ExtractionMethod.DETERMINISTIC,
                        source_id="deterministic_extractor",
                        correlation_id=correlation_id,
                    ))
                    break

        return ExtractionResult(candidates=candidates, raw_text=text)
