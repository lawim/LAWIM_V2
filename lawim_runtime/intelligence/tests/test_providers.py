from lawim_runtime.intelligence.providers import (
    DeterministicProvider,
    ProviderRegistry,
    ProviderPolicy,
    ModelRouter,
    AIProviderRequest,
)
from lawim_runtime.intelligence.providers.base import ModelCapability


def test_deterministic_provider():
    p = DeterministicProvider()
    assert p.provider_name == "deterministic"
    assert p.health()
    resp = p.generate(AIProviderRequest())
    assert resp.success
    assert resp.provider == "deterministic"


def test_provider_registry():
    reg = ProviderRegistry()
    reg.register("det", DeterministicProvider())
    assert reg.count() == 1
    assert reg.get("det") is not None
    assert reg.get("unknown") is None


def test_provider_policy_resolve():
    reg = ProviderRegistry()
    reg.register("det", DeterministicProvider())
    policy = ProviderPolicy(primary_provider="det")
    provider = reg.resolve(policy)
    assert provider is not None


def test_model_router():
    reg = ProviderRegistry()
    reg.register("det", DeterministicProvider())
    router = ModelRouter(reg)
    name = router.route("extraction")
    assert name is not None
