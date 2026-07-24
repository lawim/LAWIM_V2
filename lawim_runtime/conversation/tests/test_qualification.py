from lawim_runtime.conversation.qualification import QualificationEngine, QualificationLevel


def test_ready_for_decision():
    eng = QualificationEngine()
    r = eng.evaluate("property_search", {"transaction_type": "rent", "property_type": "apartment", "city": "Yaounde", "budget_max": 200000})
    assert r.level == QualificationLevel.READY_FOR_DECISION
    assert r.score == 100.0


def test_incomplete():
    eng = QualificationEngine()
    r = eng.evaluate("property_search", {})
    assert r.level == QualificationLevel.INCOMPLETE
    assert r.score == 0.0


def test_partial():
    eng = QualificationEngine()
    r = eng.evaluate("property_search", {"transaction_type": "rent", "city": "Yaounde"})
    assert r.level == QualificationLevel.PARTIAL
    assert len(r.missing_fields) > 0


def test_missing_fields():
    eng = QualificationEngine()
    r = eng.evaluate("property_search", {"city": "Yaounde"})
    assert "transaction_type" in r.missing_fields
    assert "property_type" in r.missing_fields
    assert "budget_max" in r.missing_fields


def test_unknown_intent():
    eng = QualificationEngine()
    r = eng.evaluate("unknown", {})
    assert r.level == QualificationLevel.QUALIFIED


def test_initial_state():
    eng = QualificationEngine()
    r = eng.evaluate("property_search", {}, {})
    assert r.level in (QualificationLevel.INITIAL, QualificationLevel.INCOMPLETE)
