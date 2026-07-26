from __future__ import annotations

import json
from pathlib import Path

import pytest

from lawim_runtime.conversation.journey import (
    _detect_language,
    _response_lang,
)

_FIXTURE_PATH = Path(__file__).resolve().parent / "fixtures" / "pcm_v1_1_gold.json"
_GOLD: list[dict] = json.loads(_FIXTURE_PATH.read_text())


class _FakeState:
    def __init__(self, initial_lang: str = "fr"):
        self._conversation_lang = initial_lang


def _build_state(initial_lang: str):
    state = _FakeState(initial_lang)
    setattr(state, "_lang_established", True)
    return state


@pytest.mark.parametrize("scenario", _GOLD, ids=lambda s: s["scenario_id"])
def test_pcm_gold_scenario(scenario: dict) -> None:
    state = _build_state(scenario["initial_language"])
    for i, msg in enumerate(scenario["messages"]):
        detected = _detect_language(msg)
        expected_detected = scenario["expected_detected_languages"][i]
        expected_conv = scenario["expected_conversation_languages"][i]
        if expected_detected == "unknown":
            assert detected in ("unknown",), f"Turn {i}: expected unknown, got {detected} (msg={msg!r})"
        else:
            assert detected == expected_detected, (
                f"Turn {i}: expected detected={expected_detected}, got {detected} (msg={msg!r})"
            )
        conv_lang = _response_lang(state, msg)
        assert conv_lang == expected_conv, (
            f"Turn {i}: expected conv_lang={expected_conv}, got {conv_lang} (msg={msg!r})"
        )
        assert state._conversation_lang == expected_conv, (
            f"Turn {i}: state._conversation_lang={state._conversation_lang} != expected {expected_conv}"
        )


@pytest.mark.parametrize("scenario", _GOLD, ids=lambda s: s["scenario_id"])
def test_pcm_gold_no_false_positive_fr(scenario: dict) -> None:
    if scenario["initial_language"] != "fr":
        pytest.skip("FR-only check")
    if scenario["scenario_id"] == "switch-fr-en-pcm":
        pytest.skip("Explicit switch scenario")
    state = _build_state("fr")
    for msg in scenario["messages"]:
        conv = _response_lang(state, msg)
        assert conv in ("fr", "pcm"), f"FR scenario drifted to {conv}: {msg}"


def test_all_scenarios_have_required_fields() -> None:
    required = {"scenario_id", "messages", "expected_detected_languages",
                "expected_conversation_languages", "expected_response_languages"}
    for s in _GOLD:
        missing = required - set(s.keys())
        assert not missing, f"{s['scenario_id']}: missing {missing}"
        assert len(s["messages"]) == len(s["expected_detected_languages"]) == \
               len(s["expected_conversation_languages"]) == len(s["expected_response_languages"]), \
            f"{s['scenario_id']}: message/lang count mismatch"


def test_all_scenarios_have_valid_ids() -> None:
    ids = [s["scenario_id"] for s in _GOLD]
    assert len(ids) == len(set(ids)), "Duplicate scenario IDs"


def test_pcm_gold_scenarios_count() -> None:
    assert len(_GOLD) == 16, f"Expected 16 scenarios, got {len(_GOLD)}"
