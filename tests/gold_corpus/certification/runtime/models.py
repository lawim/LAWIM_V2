"""Data models for actual conversation runtime execution."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ActualTurn:
    turn_index: int
    user_input: str
    assistant_output: str = ""
    state_before: Dict[str, Any] = field(default_factory=dict)
    state_after: Dict[str, Any] = field(default_factory=dict)
    facts_before: Dict[str, Any] = field(default_factory=dict)
    facts_after: Dict[str, Any] = field(default_factory=dict)
    pending_before: str = ""
    pending_after: str = ""
    business_actions: List[str] = field(default_factory=list)
    duration_ms: float = 0.0
    error: Optional[str] = None
    intent_detected: str = ""
    intent_confidence: float = 0.0


@dataclass
class ActualConversationRun:
    conversation_id: str
    runtime_called: bool = False
    adapter_class: str = ""
    orchestrator_class: str = ""
    turns: List[ActualTurn] = field(default_factory=list)
    business_objects: List[str] = field(default_factory=list)
    runtime_errors: List[str] = field(default_factory=list)
    total_duration_ms: float = 0.0
    call_count: int = 0
