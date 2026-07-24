"""Verify the LLM contract has no business decision fields."""
from lawim_runtime.conversation.llm import LLMContract


def test_contract_no_business_decision():
    """The LLM contract must NOT contain any business decision field."""
    contract = LLMContract()
    forbidden = {"decision", "action", "status", "payment", "approve", "reject", "validate", "execute", "transition"}
    attrs = set(dir(contract))
    business_attrs = attrs & forbidden
    assert len(business_attrs) == 0, f"Contract contains business decision fields: {business_attrs}"


def test_contract_has_required_fields():
    contract = LLMContract()
    required = {"intent", "confidence", "entities", "missing_information", "summary", "needs_clarification"}
    attrs = {k for k in dir(contract) if not k.startswith("_")}
    assert required.issubset(attrs), f"Missing fields: {required - attrs}"


def test_contract_defaults():
    c = LLMContract()
    assert c.intent == ""
    assert c.confidence == 0.0
    assert c.entities == {}
    assert c.missing_information == []
    assert c.needs_clarification is False


def test_contract_llm_cannot_set_actions():
    """LLM output must not contain direct action fields."""
    llm_output = {
        "intent": "property_search",
        "confidence": 0.95,
        "entities": {"city": "Yaounde"},
        "missing_information": ["budget"],
        "summary": "User searches in Yaounde",
        "needs_clarification": False,
    }
    forbidden = {"action": "start_matching", "approved": True, "status": "qualified"}
    for k in forbidden:
        assert k not in llm_output, f"LLM output contains forbidden key: {k}"


def test_llm_does_not_decide_business():
    """LLM must NEVER contain business decision fields."""
    safe_keys = {"intent", "confidence", "entities", "missing_information", "summary", "needs_clarification"}
    unsafe = {"workflow", "payment", "approve", "transition", "status", "execute", "action", "decision"}
    assert len(safe_keys & unsafe) == 0, "Safe keys overlap with unsafe keys!"
