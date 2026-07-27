from __future__ import annotations

import logging
import os
from pathlib import Path

import pytest


def test_services_pf_import_reads_flag():
    from lawim_v2.services import LawimServices
    source = Path(LawimServices.__module__.replace(".", "/") + ".py")
    if not source.is_file():
        source = Path(__file__).resolve().parent.parent / "code" / source
    content = source.read_text(encoding="utf-8")
    assert "PROGRAM_F_ENABLED" in content
    assert "logger.critical(\"Program F engine is required" in content
    assert "raise" in content
    assert "fallback disabled" not in content


def test_composition_root_produces_event_structure():
    expected_keys = {
        "event", "http_application", "conversation_engine",
        "orchestrator", "state_repository", "business_repository",
        "routing_mode", "program_f_enabled",
    }
    sample = {
        "event": "lawim_composition_root_ready",
        "http_application": "LawimRequestHandler",
        "conversation_engine": "ProgramFEngineAdapter",
        "orchestrator": "ConversationJourneyOrchestrator",
        "state_repository": "sqlite:///app/data/runtime/lawim.sqlite3",
        "business_repository": "sqlite:///app/data/runtime/lawim.sqlite3",
        "routing_mode": "standard",
        "program_f_enabled": True,
    }
    assert set(sample.keys()) == expected_keys


def test_services_inits_communication_with_pf_engine():
    content = Path("code/lawim_v2/services.py").read_text(encoding="utf-8")
    assert "program_f_engine=_conv_engine_pf" in content
