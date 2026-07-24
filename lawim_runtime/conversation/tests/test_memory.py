from lawim_runtime.conversation.memory import ConversationMemory


def test_add_entry():
    mem = ConversationMemory()
    e = mem.add_entry("user", "Bonjour")
    assert e.role == "user"
    assert e.content == "Bonjour"
    assert mem._turn_count == 1


def test_update_preferences():
    mem = ConversationMemory()
    mem.update_preferences({"property_type": "apartment", "city": "Yaounde"})
    ctx = mem.get_context()
    assert ctx.preferences["property_type"] == "apartment"
    assert ctx.preferences["city"] == "Yaounde"


def test_qualification_state():
    mem = ConversationMemory()
    mem.set_qualification("QUALIFIED")
    ctx = mem.get_context()
    assert ctx.qualification_state == "QUALIFIED"


def test_optimized_context():
    mem = ConversationMemory()
    mem.add_entry("user", "Je cherche un appartement")
    mem.add_entry("assistant", "Quel budget?")
    mem.add_entry("user", "200 000 FCFA")
    mem.update_preferences({"property_type": "apartment", "budget_max": 200000})
    ctx = mem.get_optimized_context()
    assert "apartment" in ctx or "appartement" in ctx
    assert "200" in ctx


def test_reset():
    mem = ConversationMemory()
    mem.add_entry("user", "test")
    mem.set_qualification("QUALIFIED")
    mem.reset()
    assert mem._turn_count == 0
    assert mem._qualification_state == "INITIAL"


def test_short_term_limit():
    mem = ConversationMemory()
    for i in range(15):
        mem.add_entry("user", f"Message {i}")
    assert len(mem._short_term) <= 10


def test_summary_accumulation():
    mem = ConversationMemory()
    for i in range(15):
        mem.add_entry("user", f"Message numero {i}")
    ctx = mem.get_context()
    assert ctx.summary
