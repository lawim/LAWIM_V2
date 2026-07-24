from lawim_runtime.conversation.adapters import OpenAIAdapter, DeepSeekAdapter, ClaudeAdapter, GeminiAdapter, MistralAdapter
from lawim_runtime.conversation.llm import DeterministicLLMAdapter, LLMContract


def test_deterministic_adapter():
    adapter = DeterministicLLMAdapter()
    assert adapter.provider_name == "deterministic"
    result = adapter.analyze("Je cherche un appartement")
    assert result.intent != ""
    assert result.confidence >= 0


def test_openai_adapter_no_key():
    adapter = OpenAIAdapter()
    assert adapter.provider_name == "openai"
    result = adapter.analyze("test")
    assert result.intent == "unknown"
    assert result.confidence == 0.0


def test_deepseek_adapter_no_key():
    adapter = DeepSeekAdapter()
    assert adapter.provider_name == "deepseek"
    result = adapter.analyze("test")
    assert result.confidence == 0.0


def test_claude_adapter_no_key():
    adapter = ClaudeAdapter()
    assert adapter.provider_name == "claude"
    result = adapter.analyze("test")
    assert result.intent == "unknown"


def test_gemini_adapter_no_key():
    adapter = GeminiAdapter()
    assert adapter.provider_name == "gemini"
    result = adapter.analyze("test")
    assert result.intent == "unknown"


def test_mistral_adapter_no_key():
    adapter = MistralAdapter()
    assert adapter.provider_name == "mistral"
    result = adapter.analyze("test")
    assert result.intent == "unknown"


def test_all_adapters_same_contract():
    adapters = [OpenAIAdapter, DeepSeekAdapter, ClaudeAdapter, GeminiAdapter, MistralAdapter, DeterministicLLMAdapter]
    for cls in adapters:
        a = cls()
        r = a.analyze("test")
        assert isinstance(r, LLMContract)
        assert hasattr(r, "intent")
        assert hasattr(r, "confidence")
        assert hasattr(r, "entities")
        assert hasattr(r, "missing_information")
        assert hasattr(r, "summary")
        assert hasattr(r, "needs_clarification")
