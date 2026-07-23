import pytest
from lawim_runtime.intelligence.providers.openai import OpenAIProvider
from lawim_runtime.intelligence.providers.anthropic import AnthropicProvider
from lawim_runtime.intelligence.providers.deepseek import DeepSeekProvider
from lawim_runtime.intelligence.providers.gemini import GeminiProvider
from lawim_runtime.intelligence.providers.base import AIProviderRequest


def test_openai_provider_init():
    p = OpenAIProvider()
    assert p.provider_name == "openai"
    assert not p.health()  # no API key
    resp = p.generate(AIProviderRequest())
    assert not resp.success
    assert "not configured" in resp.error


def test_anthropic_provider_init():
    p = AnthropicProvider()
    assert p.provider_name == "anthropic"
    assert not p.health()
    resp = p.generate(AIProviderRequest())
    assert not resp.success
    assert "not configured" in resp.error


def test_deepseek_provider_init():
    p = DeepSeekProvider()
    assert p.provider_name == "deepseek"
    assert not p.health()
    resp = p.generate(AIProviderRequest())
    assert not resp.success
    assert "not configured" in resp.error


def test_gemini_provider_init():
    p = GeminiProvider()
    assert p.provider_name == "gemini"
    assert not p.health()
    resp = p.generate(AIProviderRequest())
    assert not resp.success
    assert "not configured" in resp.error


def test_openai_provider_with_key():
    p = OpenAIProvider(api_key="sk-test")
    assert p.health()
    assert p.capabilities.model_name == "gpt-4o-mini"


def test_provider_capabilities():
    for provider_cls in [OpenAIProvider, AnthropicProvider, DeepSeekProvider, GeminiProvider]:
        p = provider_cls()
        caps = p.capabilities
        assert caps.provider == p.provider_name
        assert "fr" in caps.languages
        assert "en" in caps.languages
        assert caps.context_window > 0
