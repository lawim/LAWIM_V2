from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import re


SECRET_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bAIza[0-9A-Za-z_-]{20,}\b"),
    re.compile(r"\bAQ\.[0-9A-Za-z_-]{20,}\b"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._-]{20,}\b", re.IGNORECASE),
    re.compile(r"\b[0-9]{6,}@(?:c\.us|s\.whatsapp\.net)\b", re.IGNORECASE),
    re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b"),
)

PROMPT_INJECTION_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"ignore (?:all|previous|the) instructions", re.IGNORECASE),
    re.compile(r"reveal (?:the )?(?:system prompt|secret|keys?|tokens?)", re.IGNORECASE),
    re.compile(r"show (?:your )?(?:environment|env|instructions)", re.IGNORECASE),
    re.compile(r"print (?:your )?(?:system|developer) prompt", re.IGNORECASE),
    re.compile(r"exfiltrat", re.IGNORECASE),
)


@dataclass(frozen=True, slots=True)
class ResponseQuality:
    valid: bool
    complete: bool
    relevant: bool
    safe: bool
    well_formed: bool
    confidence_score: float
    reason: str = ""

    def to_dict(self) -> dict[str, object]:
        return {
            "valid": self.valid,
            "complete": self.complete,
            "relevant": self.relevant,
            "safe": self.safe,
            "well_formed": self.well_formed,
            "confidence_score": self.confidence_score,
            "reason": self.reason,
        }


def redact_sensitive_text(value: str | None) -> str:
    text = str(value or "")
    if not text:
        return ""
    redacted = text
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub("[redacted]", redacted)
    return redacted


def redact_sensitive_object(value: object) -> object:
    if isinstance(value, str):
        return redact_sensitive_text(value)
    if isinstance(value, dict):
        return {key: redact_sensitive_object(item) for key, item in value.items()}
    if isinstance(value, list):
        return [redact_sensitive_object(item) for item in value]
    if isinstance(value, tuple):
        return tuple(redact_sensitive_object(item) for item in value)
    return value


def looks_like_prompt_injection(text: str | None) -> bool:
    candidate = str(text or "")
    if not candidate:
        return False
    lowered = candidate.lower()
    if any(pattern.search(candidate) for pattern in PROMPT_INJECTION_PATTERNS):
        return True
    return any(token in lowered for token in ("system prompt", "developer prompt", "ignore instructions"))


def estimate_simple_token_count(text: str | None) -> int:
    candidate = str(text or "").strip()
    if not candidate:
        return 0
    return max(1, len(candidate) // 4)


def validate_response(text: str | None, *, max_chars: int = 4000) -> ResponseQuality:
    candidate = str(text or "").strip()
    if not candidate:
        return ResponseQuality(False, False, False, False, False, 0.0, "empty")
    safe = not any(pattern.search(candidate) for pattern in SECRET_PATTERNS)
    well_formed = len(candidate) <= max_chars and not candidate.startswith("{")
    complete = len(candidate) >= 12
    relevant = True
    confidence = 0.85 if safe and well_formed and complete else 0.45
    if not safe:
        return ResponseQuality(False, complete, relevant, False, well_formed, 0.0, "contains_secret")
    if not well_formed:
        return ResponseQuality(False, complete, relevant, safe, False, 0.35, "malformed")
    return ResponseQuality(True, complete, relevant, safe, True, confidence, "")


def stable_hash(value: str | None) -> str:
    return sha256(str(value or "").encode("utf-8")).hexdigest()
