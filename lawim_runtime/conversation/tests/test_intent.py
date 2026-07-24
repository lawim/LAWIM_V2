from lawim_runtime.conversation.intent import IntentEngine


def test_intent_property_search():
    eng = IntentEngine()
    r = eng.detect("Je cherche un appartement")
    assert r.intent == "property_search"
    assert r.confidence > 0.3


def test_intent_visit():
    eng = IntentEngine()
    r = eng.detect("Je veux visiter")
    assert r.intent == "visit_request"


def test_intent_greeting():
    eng = IntentEngine()
    r = eng.detect("Bonjour")
    assert r.intent == "greeting"


def test_intent_support():
    eng = IntentEngine()
    r = eng.detect("Aidez-moi")
    assert r.intent == "support"


def test_intent_empty():
    eng = IntentEngine()
    r = eng.detect("")
    assert r.intent == "unknown"
    assert r.confidence == 0.0


def test_intent_low_confidence():
    eng = IntentEngine()
    r = eng.detect("xyzabc")
    assert r.needs_clarification or r.confidence < 0.5


def test_intent_payment():
    eng = IntentEngine()
    r = eng.detect("Payer mon loyer")
    assert r.intent == "payment"


def test_intent_owner_registration():
    eng = IntentEngine()
    r = eng.detect("Publier mon bien")
    assert r.intent == "owner_registration"


def test_intent_llm_independent():
    eng = IntentEngine()
    r = eng.detect("Je cherche un studio")
    assert r.intent == "property_search"
    assert r.confidence > 0


def test_intent_bonjour_with_search():
    eng = IntentEngine()
    r = eng.detect("Bonjour je cherche un appartement")
    assert r.intent == "property_search"


def test_intent_english_search():
    eng = IntentEngine()
    r = eng.detect("I am looking for a flat for rent")
    assert r.intent == "property_search"
