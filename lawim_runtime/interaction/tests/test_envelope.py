from lawim_runtime.interaction.envelope import InteractionEnvelope, MessageType, AttachmentRef
from lawim_runtime.interaction.gateway import InteractionGateway


def test_envelope_creation():
    env = InteractionEnvelope(
        channel="whatsapp",
        external_message_id="msg-001",
        external_user_id="237691234567",
        raw_sender="237691234567",
        raw_content="Je cherche un appartement",
        message_type=MessageType.TEXT,
    )
    assert env.interaction_id != ""
    assert env.channel == "whatsapp"
    assert env.external_message_id == "msg-001"
    assert env.raw_content == "Je cherche un appartement"
    assert env.message_type == MessageType.TEXT
    assert env.received_at != ""


def test_envelope_immutable():
    env = InteractionEnvelope(channel="telegram", raw_content="test")
    assert isinstance(env, object)


def test_gateway_validate():
    gateway = InteractionGateway()
    valid = InteractionEnvelope(channel="whatsapp", raw_content="hello")
    result = gateway.validate_envelope(valid)
    assert result.valid is True

    invalid = InteractionEnvelope(channel="", raw_content="")
    result = gateway.validate_envelope(invalid)
    assert result.valid is False


def test_gateway_prepare():
    gateway = InteractionGateway()
    env = gateway.prepare_envelope(
        channel="telegram",
        external_message_id="123",
        external_user_id="user1",
        raw_sender="user1",
        raw_content="Bonjour",
        message_type=MessageType.TEXT,
        correlation_id="corr-1",
    )
    assert env.channel == "telegram"
    assert env.external_message_id == "123"
    assert env.correlation_id == "corr-1"


def test_message_type_enum():
    assert MessageType.TEXT.value == "TEXT"
    assert MessageType.IMAGE.value == "IMAGE"
    assert MessageType.UNKNOWN.value == "UNKNOWN"
    assert len(MessageType) == 11
