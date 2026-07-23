from lawim_runtime.interaction.adapters import ChannelDeliveryRequest, ChannelDeliveryResult


def test_delivery_request_creation():
    req = ChannelDeliveryRequest(
        channel="whatsapp",
        recipient_id="+237600000",
        text="Hello",
        correlation_id="corr-1",
    )
    assert req.channel == "whatsapp"
    assert req.recipient_id == "+237600000"
    assert req.text == "Hello"


def test_delivery_result_creation():
    result = ChannelDeliveryResult(
        success=True,
        provider_message_id="abc123",
        status_code=200,
    )
    assert result.success is True
    assert result.provider_message_id == "abc123"
