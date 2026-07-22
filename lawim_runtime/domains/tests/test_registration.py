from lawim_runtime.domains.registration import register_domain_runtimes, _ShadowHandler
from lawim_runtime.domains.config import DomainRuntimeConfig, DEFAULT_DOMAIN_CONFIG
from lawim_runtime.execution.registry import ActionHandlerRegistry
from lawim_runtime.domains.base.request import DomainRuntimeRequest


def test_register_all_domains():
    registry = ActionHandlerRegistry()
    config = DomainRuntimeConfig(
        matching_enabled=True,
        visit_enabled=True,
        crm_enabled=True,
        notification_enabled=True,
        document_enabled=True,
        verification_enabled=True,
        transaction_enabled=True,
        payment_enabled=True,
        shadow_mode=False,
    )
    register_domain_runtimes(registry, config)
    assert registry.count() == 8
    assert registry.has_handler_for("START_MATCHING") is True
    assert registry.has_handler_for("CREATE_VISIT_REQUEST") is True
    assert registry.has_handler_for("CREATE_OR_UPDATE_LEAD") is True
    assert registry.has_handler_for("PREPARE_NOTIFICATION") is True
    assert registry.has_handler_for("REQUEST_DOCUMENT") is True
    assert registry.has_handler_for("START_VERIFICATION") is True
    assert registry.has_handler_for("PREPARE_TRANSACTION") is True
    assert registry.has_handler_for("CREATE_PAYMENT_INTENT") is True


def test_shadow_mode_returns_simulated():
    registry = ActionHandlerRegistry()
    config = DomainRuntimeConfig(shadow_mode=True)
    register_domain_runtimes(registry, config)
    assert registry.count() == 8
    handler = registry.resolve_handler("START_MATCHING")
    assert isinstance(handler, _ShadowHandler)

    shadow_result = handler.execute(None)
    assert shadow_result["status"] == "SIMULATED"
    assert "shadow mode" in shadow_result.get("message", "")


def test_feature_flags_disabled():
    registry = ActionHandlerRegistry()
    config = DomainRuntimeConfig(
        matching_enabled=False,
        visit_enabled=False,
        crm_enabled=False,
        notification_enabled=False,
        document_enabled=False,
        verification_enabled=False,
        transaction_enabled=False,
        payment_enabled=False,
        shadow_mode=False,
    )
    register_domain_runtimes(registry, config)
    assert registry.count() == 0


def test_feature_flags_enabled():
    registry = ActionHandlerRegistry()
    config = DomainRuntimeConfig(
        matching_enabled=True,
        shadow_mode=False,
    )
    register_domain_runtimes(registry, config)
    assert registry.count() == 1
    assert registry.has_handler_for("START_MATCHING") is True
    assert registry.has_handler_for("CREATE_VISIT_REQUEST") is False
