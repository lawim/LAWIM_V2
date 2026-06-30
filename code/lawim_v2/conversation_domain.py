from __future__ import annotations

NEGOTIATION_STAGES = frozenset({"inquiry", "offer", "counter", "accepted", "declined", "closed"})
CONVERSATION_STATUSES = frozenset({"open", "closed", "archived"})

STATUS_TRANSITIONS: dict[str, frozenset[str]] = {
    "open": frozenset({"open", "closed", "archived"}),
    "closed": frozenset({"closed", "archived", "open"}),
    "archived": frozenset({"archived"}),
}

STAGE_TRANSITIONS: dict[str, frozenset[str]] = {
    "inquiry": frozenset({"inquiry", "offer", "declined", "closed"}),
    "offer": frozenset({"offer", "counter", "accepted", "declined", "closed"}),
    "counter": frozenset({"counter", "offer", "accepted", "declined", "closed"}),
    "accepted": frozenset({"accepted", "closed"}),
    "declined": frozenset({"declined", "closed"}),
    "closed": frozenset({"closed"}),
}


def normalize_negotiation_stage(stage: str) -> str:
    normalized = stage.strip().lower()
    if normalized not in NEGOTIATION_STAGES:
        raise ValueError(f"unsupported negotiation stage: {normalized}")
    return normalized


def validate_status_transition(current: str, nxt: str) -> None:
    current_norm = current.lower()
    next_norm = nxt.lower()
    allowed = STATUS_TRANSITIONS.get(current_norm, frozenset({next_norm}))
    if next_norm not in allowed:
        raise ValueError(f"invalid conversation status transition: {current_norm} -> {next_norm}")


def validate_stage_transition(current: str, nxt: str) -> None:
    current_norm = current.lower()
    next_norm = nxt.lower()
    allowed = STAGE_TRANSITIONS.get(current_norm, frozenset({next_norm}))
    if next_norm not in allowed:
        raise ValueError(f"invalid negotiation stage transition: {current_norm} -> {next_norm}")
