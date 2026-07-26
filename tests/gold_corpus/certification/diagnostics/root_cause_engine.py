"""Root cause engine for LAWIM certification.

Maps each assertion violation to the most likely responsible component.
"""

from typing import Any, Dict, List, Optional

COMPONENT_MAP = {
    "MEM-0001": {"component": "ConversationStateService", "confidence": 0.9},
    "MEM-0002": {"component": "ConversationStateService", "confidence": 0.85},
    "MEM-0003": {"component": "ProgramFEngineAdapter", "confidence": 0.85},
    "MEM-0004": {"component": "QualificationService", "confidence": 0.9},
    "MEM-0005": {"component": "ConversationStateService", "confidence": 0.85},
    "MEM-0006": {"component": "MemoryCompactionService", "confidence": 0.8},
    "MEM-0007": {"component": "ConversationStateService", "confidence": 0.75},
    "QLF-0001": {"component": "QualificationService", "confidence": 0.9},
    "QLF-0002": {"component": "ProgressiveWizard", "confidence": 0.85},
    "QLF-0003": {"component": "QualificationService", "confidence": 0.85},
    "BIZ-0001": {"component": "ConversationJourneyOrchestrator", "confidence": 0.85},
    "BIZ-0002": {"component": "ConversationJourneyOrchestrator", "confidence": 0.85},
    "BIZ-0003": {"component": "ConversationJourneyOrchestrator", "confidence": 0.8},
    "BIZ-0004": {"component": "HandoverContinuityService", "confidence": 0.9},
    "INT-0001": {"component": "ProgramFEngineAdapter", "confidence": 0.9},
    "INT-0002": {"component": "ConversationJourneyOrchestrator", "confidence": 0.8},
    "LANG-0001": {"component": "LanguagePolicy", "confidence": 0.9},
    "LANG-0002": {"component": "AIOrchestrator", "confidence": 0.95},
    "LANG-0003": {"component": "CommunicationService", "confidence": 0.9},
    "LANG-0004": {"component": "ConversationResponseValidator", "confidence": 0.85},
    "QST-0001": {"component": "ConversationResponseValidator", "confidence": 0.9},
    "QST-0002": {"component": "ProgressiveWizard", "confidence": 0.75},
    "QST-0003": {"component": "ConversationResponseValidator", "confidence": 0.85},
    "RUNTIME-0001": {"component": "ProviderOrchestrator", "confidence": 0.9},
    "RUNTIME-0002": {"component": "ProviderOrchestrator", "confidence": 0.8},
    "CHANNEL-0001": {"component": "ChannelAdapter", "confidence": 0.85},
    "IDEM-0001": {"component": "ConversationStateService", "confidence": 0.7},
    "IDEM-0002": {"component": "Runtime", "confidence": 0.6},
    "STATE-0001": {"component": "ConversationJourneyOrchestrator", "confidence": 0.9},
    "STATE-0002": {"component": "ConversationJourneyOrchestrator", "confidence": 0.85},
    "STATE-0003": {"component": "QualificationService", "confidence": 0.85},
}


def get_component(assertion_id: str) -> Dict[str, Any]:
    """Return the most likely responsible component for a given assertion."""
    entry = COMPONENT_MAP.get(assertion_id, {
        "component": "Unknown",
        "confidence": 0.5,
    })
    return dict(entry)


def analyze_root_causes(violations: List[Dict]) -> List[Dict]:
    """Analyze root causes for a list of violations."""
    results = []
    for v in violations:
        component_info = get_component(v["assertion_id"])
        results.append({
            "assertion_id": v["assertion_id"],
            "category": v["category"],
            "turn_number": v.get("turn_number"),
            "responsible_component": component_info["component"],
            "root_confidence": component_info["confidence"],
            "explanation": v.get("explanation"),
            "expected_correction": v.get("expected_correction"),
        })
    return results


def build_component_summary(root_causes: List[Dict]) -> Dict[str, int]:
    """Summarize violations by component."""
    summary = {}
    for rc in root_causes:
        comp = rc["responsible_component"]
        summary[comp] = summary.get(comp, 0) + 1
    return summary
