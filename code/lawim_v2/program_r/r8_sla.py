from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class SLAPriority(str, Enum):
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"


SLA_TARGETS: dict[SLAPriority, int] = {
    SLAPriority.P0: 5,
    SLAPriority.P1: 30,
    SLAPriority.P2: 120,
    SLAPriority.P3: 1440,
}


@dataclass
class SLABreach:
    breach_id: str = ""
    entity_type: str = ""
    entity_id: str = ""
    sla_priority: SLAPriority = SLAPriority.P3
    threshold_minutes: int = 0
    actual_minutes: int = 0
    breached_at: str = ""
    status: str = "OPEN"

    def is_breached(self) -> bool:
        return self.actual_minutes > self.threshold_minutes


@dataclass
class SLABreachEscalation:
    tier: int = 1
    escalation_action: str = ""
    notify: list[str] = field(default_factory=list)

    @staticmethod
    def get_escalation_tiers() -> list[dict[str, Any]]:
        return [
            {"tier": 1, "action": "notify_agent", "notify": ["agent"]},
            {"tier": 2, "action": "notify_manager", "notify": ["manager"]},
            {"tier": 3, "action": "notify_admin", "notify": ["admin"]},
        ]


# ── Anti-Fraud ─────────────────────────────────────────────────────────────


@dataclass
class FraudSignal:
    signal_type: str = ""
    severity: int = 0
    description: str = ""
    detected_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"signal_type": self.signal_type, "severity": self.severity}


@dataclass
class AntiFraudEngine:
    def check_message(self, text: str) -> list[FraudSignal]:
        signals: list[FraudSignal] = []
        t = text.lower()
        spam_indicators = ["achetez maintenant", "offre unique", "gagnez",
                           "cliquez ici", "argent facile", "urgent investissement"]
        for indicator in spam_indicators:
            if indicator in t:
                signals.append(FraudSignal("spam_content", 30, f"Spam indicator: {indicator}"))
                break
        pricing_patterns = [r"\d{8,}", r"\d+[.,]\d{6,}"]
        import re
        for pattern in pricing_patterns:
            if re.search(pattern, t):
                signals.append(FraudSignal("suspicious_price", 25, "Suspicious price pattern"))
                break
        return signals

    def check_urgency(self, text: str) -> FraudSignal | None:
        t = text.lower()
        artificial = ["urgent absolument", "dernier jour", "offre limite",
                      "aujourd'hui seulement", "dépêchez-vous"]
        for phrase in artificial:
            if phrase in t:
                return FraudSignal("artificial_urgency", 15, f"Artificial urgency: {phrase}")
        return None


# ── Hold Silence ───────────────────────────────────────────────────────────


@dataclass
class HolderSilenceTracker:
    last_activity: str = ""
    silence_threshold_hours: int = 48
    reminder_intervals_hours: list[int] = field(default_factory=lambda: [24, 48, 72])

    def is_silent(self, hours_since_last: int) -> bool:
        return hours_since_last >= self.silence_threshold_hours

    def next_reminder(self, hours_since_last: int) -> int | None:
        for interval in self.reminder_intervals_hours:
            if hours_since_last < interval:
                return interval - hours_since_last
        return None
