from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lawim_runtime"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "code"))

from lawim_runtime.conversation.entity import EntityExtractionEngine
from lawim_runtime.conversation.intent import IntentEngine


def test_defect001_transaction_not_city():
    engine = EntityExtractionEngine()
    result = engine.extract("a louer")
    assert "city" not in result.entities, f"city must not be set from transaction word, got city={result.entities.get('city')}"
    assert result.entities.get("transaction_type") == "rent"


def test_defect001_transaction_not_city_variants():
    engine = EntityExtractionEngine()
    for msg in ["a louer", "à louer", "a acheter", "à acheter", "a vendre", "à vendre"]:
        result = engine.extract(msg)
        assert "city" not in result.entities, f"city must not be set from transaction word in '{msg}'"


def test_defect001_city_ok():
    engine = EntityExtractionEngine()
    result = engine.extract("a douala")
    assert result.entities.get("city") == "Douala"


def test_defect002_correction_with_jai_dit():
    engine = EntityExtractionEngine()
    result = engine.extract("voj'ai dit à louer")
    assert "city" not in result.entities, f"city must not be set from 'louer' in correction: got {result.entities.get('city')}"
    assert result.entities.get("transaction_type") == "rent"


def test_defect003_meuble():
    engine = EntityExtractionEngine()
    result = engine.extract("appartement meublé")
    assert result.entities.get("property_type") == "apartment"
    assert result.entities.get("furnished") is True, "furnished must be True for 'meublé'"


def test_defect003_meuble_variant():
    engine = EntityExtractionEngine()
    result = engine.extract("appartement meuble")
    assert result.entities.get("furnished") is True, "furnished must be True"


def test_defect003_meuble_full_sequence():
    engine = EntityExtractionEngine()
    result = engine.extract("j'ai besoin d'un appartement meublé")
    assert result.entities.get("property_type") == "apartment"
    assert result.entities.get("furnished") is True


def test_defect004_start_is_greeting():
    engine = IntentEngine()
    result = engine.detect("/start")
    assert result.intent == "greeting", f"/start should be greeting, got {result.intent}"


def test_defect004_bonjour_greeting():
    engine = IntentEngine()
    result = engine.detect("bonjour")
    assert result.intent == "greeting", f"bonjour should be greeting, got {result.intent}"


def test_defect005_nlonkak_as_district():
    engine = EntityExtractionEngine()
    result = engine.extract("a nlonkak")
    assert result.entities.get("district") == "Nlongkak", f"expected district Nlongkak, got {result.entities.get('district')}"
    assert "city" not in result.entities, "nlonkak should be district not city"
    assert result.entities.get("property_type") is None


def test_defect005_nlongkak_as_district():
    engine = EntityExtractionEngine()
    result = engine.extract("a nlongkak")
    assert result.entities.get("district") == "Nlongkak"
    assert "city" not in result.entities


def test_whatsapp_full_sequence_no_city_contamination():
    engine = EntityExtractionEngine()
    r1 = engine.extract("bonjour")
    assert "city" not in r1.entities
    r2 = engine.extract("j'ai besoin d'un appartement meublé")
    assert r2.entities.get("property_type") == "apartment"
    assert r2.entities.get("furnished") is True
    r3 = engine.extract("a louer")
    assert r3.entities.get("transaction_type") == "rent"
    assert "city" not in r3.entities, f"DEFECT-001: city must not be 'Louer', got {r3.entities.get('city')}"
    r4 = engine.extract("voj'ai dit à louer")
    assert "city" not in r4.entities
    assert r4.entities.get("transaction_type") == "rent"
    r5 = engine.extract("a obala")
    assert r5.entities.get("city") is not None, "obala should be recognized as city"
