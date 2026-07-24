from lawim_runtime.conversation.intent import IntentEngine


def test_intent_property_search():
    eng = IntentEngine()
    r = eng.detect("Je cherche un appartement à louer à Yaoundé")
    assert r.intent == "property_search"
    assert r.confidence > 0.3


def test_intent_visit():
    eng = IntentEngine()
    r = eng.detect("Je veux visiter ce logement")
    assert r.intent == "visit_request"


def test_intent_greeting():
    eng = IntentEngine()
    r = eng.detect("Bonjour")
    assert r.intent == "greeting"


def test_intent_support():
    eng = IntentEngine()
    r = eng.detect("J'ai besoin d'aide")
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
    r = eng.detect("Je veux payer mon loyer")
    assert r.intent == "payment"


def test_intent_owner_registration():
    eng = IntentEngine()
    r = eng.detect("Je veux publier mon bien")
    assert r.intent == "owner_registration"


def test_intent_llm_independent():
    """Intent engine must work without any LLM."""
    eng = IntentEngine()
    r = eng.detect("Je cherche un studio")
    assert r.intent in ("property_search", "information")
    assert r.confidence > 0
