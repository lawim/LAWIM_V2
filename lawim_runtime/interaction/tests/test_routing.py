from lawim_runtime.interaction.routing import InteractionModeRouter, InteractionMode
from lawim_runtime.interaction.envelope import InteractionEnvelope


def test_default_v2_only():
    router = InteractionModeRouter()
    assert router.mode == InteractionMode.V2_ONLY
    assert router.is_v3_active() is False


def test_v3_shadow():
    router = InteractionModeRouter(mode=InteractionMode.V3_SHADOW)
    assert router.is_v3_active() is True
    assert router.is_shadow() is True


def test_v3_only():
    router = InteractionModeRouter(mode=InteractionMode.V3_ONLY)
    assert router.is_v3_active() is True
    assert router.is_shadow() is False


def test_canary_user():
    router = InteractionModeRouter(mode=InteractionMode.V3_CANARY, canary_users={"user-001"})
    assert router.is_v3_active(user_id="user-001") is True
    assert router.is_v3_active(user_id="user-002") is False


def test_canary_channel():
    router = InteractionModeRouter(mode=InteractionMode.V3_CANARY, canary_channels={"telegram"})
    env = InteractionEnvelope(channel="telegram", raw_content="test")
    assert router.is_v3_active(envelope=env) is True
    env2 = InteractionEnvelope(channel="whatsapp", raw_content="test")
    assert router.is_v3_active(envelope=env2) is False


def test_v3_primary_with_v2_fallback():
    router = InteractionModeRouter(mode=InteractionMode.V3_PRIMARY_WITH_V2_FALLBACK)
    assert router.is_v3_active() is True
    assert router.is_shadow() is False
