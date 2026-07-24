from lawim_runtime.conversation.engine import ConversationEngine
from lawim_runtime.conversation.llm import DeterministicLLMAdapter


def test_process_basic():
    engine = ConversationEngine()
    result = engine.process("Bonjour")
    assert result.intent is not None
    assert result.entities is not None
    assert result.memory is not None
    assert result.qualification is not None
    assert result.error == ""


def test_process_empty():
    engine = ConversationEngine()
    result = engine.process("")
    assert result.error == "empty_input"


def test_process_property_search():
    engine = ConversationEngine()
    result = engine.process("Je cherche un appartement à louer à Yaoundé avec un budget de 200 000 FCFA")
    assert result.intent.intent == "property_search"
    assert result.entities.entities.get("property_type") == "apartment"
    assert result.entities.entities.get("city") == "Yaounde"
    assert result.response_type in ("ASK_MISSING_FIELDS", "CONFIRM_AND_ASK", "READY_FOR_PROCESSING")


def test_process_with_llm():
    llm = DeterministicLLMAdapter()
    engine = ConversationEngine(llm_adapter=llm)
    result = engine.process("Je cherche une maison")
    assert result.intent is not None
    assert result.llm_analysis is not None


def test_assistant_response_added():
    engine = ConversationEngine()
    engine.process("Bonjour")
    engine.add_assistant_response("Bonjour, que cherchez-vous?")
    ctx = engine._memory.get_context()
    assert len(ctx.short_term) == 2


def test_full_conversation_flow():
    engine = ConversationEngine()
    r1 = engine.process("Bonjour")
    assert r1.intent.intent == "greeting"
    engine.add_assistant_response("Bonjour! Que cherchez-vous?")
    r2 = engine.process("Je cherche un appartement à louer à Yaoundé")
    assert r2.intent.intent == "property_search"
    assert r2.entities.entities.get("property_type") == "apartment"
    assert r2.entities.entities.get("city") == "Yaounde"
    engine.add_assistant_response("Quel est votre budget?")
    r3 = engine.process("200 000 FCFA")
    assert r3.entities.entities.get("budget_max") == 200000
    ctx = engine._memory.get_context()
    assert ctx.turn_count >= 3
