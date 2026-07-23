from lawim_runtime.interaction.identity import IdentityResolver, IdentityStatus, ChannelIdentity


def test_resolve_anonymous():
    resolver = IdentityResolver()
    result = resolver.resolve("whatsapp", "+237600000", "+237600000")
    assert result.status == IdentityStatus.ANONYMOUS
    assert result.confidence == 0.0
    assert result.actor_id == ""
    assert result.channel_identity is not None


def test_resolve_known():
    resolver = IdentityResolver()
    resolver.link_channel_to_user("user-001", "whatsapp", "+237600000")
    result = resolver.resolve("whatsapp", "+237600000", "+237600000")
    assert result.status == IdentityStatus.RESOLVED
    assert result.user_id == "user-001"
    assert result.confidence == 1.0


def test_multi_channel_same_user():
    resolver = IdentityResolver()
    resolver.link_channel_to_user("user-001", "whatsapp", "+237600000")
    resolver.link_channel_to_user("user-001", "telegram", "12345")
    channels = resolver.get_user_channels("user-001")
    assert len(channels) == 2


def test_channel_identity_key():
    ci = ChannelIdentity(channel="whatsapp", external_user_id="+237600000")
    assert ci.identity_key == "whatsapp:+237600000"


def test_resolve_no_auto_merge():
    resolver = IdentityResolver()
    r1 = resolver.resolve("whatsapp", "+237600000", "+237600000")
    r2 = resolver.resolve("telegram", "54321", "54321")
    assert r1.identity_id != r2.identity_id
