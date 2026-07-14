from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..domain.conversation import Conversation


@dataclass
class LoopDetectionResult:
    loop_detected: bool = False
    loop_score: int = 0
    repeat_count: int = 0
    field: str | None = None
    action: str = "continue"  # "continue", "reformulate", "offer_options", "handover"
    reformulation_count: int = 0
    events: list[dict[str, Any]] | None = None


FIELD_REPEAT_TRACKING: dict[str, int] = {}
FIELD_REFORMULATION_COUNT: dict[str, int] = {}


def reset_field_tracking(field: str | None = None) -> None:
    if field:
        FIELD_REPEAT_TRACKING.pop(field, None)
        FIELD_REFORMULATION_COUNT.pop(field, None)
    else:
        FIELD_REPEAT_TRACKING.clear()
        FIELD_REFORMULATION_COUNT.clear()


def _is_input_matching_expected(user_message: str, expected_input: str | None) -> bool:
    if not expected_input:
        return False
    cleaned = user_message.strip().lower().rstrip("!.,?")
    expected = expected_input.strip().lower()
    return cleaned == expected or expected in cleaned


def detect_loop(
    conversation: Conversation,
    user_message: str,
    *,
    current_field: str | None = None,
    expected_input: str | None = None,
) -> LoopDetectionResult:
    field = current_field or conversation.last_question_field

    if field is None:
        return LoopDetectionResult()

    if not _is_input_matching_expected(user_message, expected_input):
        FIELD_REPEAT_TRACKING[field] = FIELD_REPEAT_TRACKING.get(field, 0) + 1
    else:
        FIELD_REPEAT_TRACKING[field] = 0
        FIELD_REFORMULATION_COUNT[field] = 0
        return LoopDetectionResult()

    repeat_count = FIELD_REPEAT_TRACKING[field]
    reformulation_count = FIELD_REFORMULATION_COUNT.get(field, 0)

    loop_score = _calculate_loop_score(repeat_count, reformulation_count, conversation)
    events: list[dict[str, Any]] = []

    if repeat_count == 1:
        return LoopDetectionResult(
            loop_detected=False,
            loop_score=loop_score,
            repeat_count=repeat_count,
            field=field,
            action="continue",
            reformulation_count=reformulation_count,
        )

    if repeat_count > 1 and repeat_count <= 2:
        FIELD_REFORMULATION_COUNT[field] = reformulation_count + 1
        events.append({
            "event": "clarification.repeated",
            "field": field,
            "repeat_count": repeat_count,
            "reformulation_count": reformulation_count + 1,
            "loop_score": loop_score,
        })
        return LoopDetectionResult(
            loop_detected=True,
            loop_score=loop_score,
            repeat_count=repeat_count,
            field=field,
            action="reformulate",
            reformulation_count=reformulation_count + 1,
            events=events,
        )

    if repeat_count > 2 and repeat_count <= 3:
        events.append({
            "event": "clarification.repeated",
            "field": field,
            "repeat_count": repeat_count,
            "loop_score": loop_score,
            "message": "offering alternatives to user",
        })
        return LoopDetectionResult(
            loop_detected=True,
            loop_score=loop_score,
            repeat_count=repeat_count,
            field=field,
            action="offer_options",
            reformulation_count=reformulation_count,
            events=events,
        )

    events.append({
        "event": "clarification.loop_exceeded",
        "field": field,
        "repeat_count": repeat_count,
        "loop_score": loop_score,
        "message": "handing over to human agent",
    })
    return LoopDetectionResult(
        loop_detected=True,
        loop_score=loop_score,
        repeat_count=repeat_count,
        field=field,
        action="handover",
        reformulation_count=reformulation_count,
        events=events,
    )


def _calculate_loop_score(
    repeat_count: int,
    reformulation_count: int,
    conversation: Conversation,
) -> int:
    base_score = repeat_count * 10
    reformulation_penalty = reformulation_count * 5

    context_penalty = 0
    if conversation.loop_detected:
        context_penalty += 15

    if conversation.last_question_field:
        if conversation.last_question_field in conversation.known_fields:
            context_penalty += 10

    total = base_score + reformulation_penalty + context_penalty
    return min(total, 100)


def update_conversation_loop_state(
    conversation: Conversation,
    result: LoopDetectionResult,
) -> None:
    conversation.loop_detected = result.loop_detected
    conversation.loop_score = result.loop_score
    conversation.question_repeat_count = result.repeat_count

    if result.action == "handover":
        conversation.human_handover_requested = True


def clear_field_repeat(field: str) -> None:
    FIELD_REPEAT_TRACKING.pop(field, None)
    FIELD_REFORMULATION_COUNT.pop(field, None)
