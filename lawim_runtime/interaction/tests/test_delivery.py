from lawim_runtime.interaction.delivery import DeliveryManager, DeliveryStatus
from lawim_runtime.interaction.response_plan import InteractionResponsePlan, ResponseType


def test_delivery_empty_plan():
    dm = DeliveryManager()
    plan = InteractionResponsePlan(response_type=ResponseType.NO_RESPONSE)
    result = dm.deliver(plan, "whatsapp")
    assert result.status == DeliveryStatus.CANCELLED


def test_delivery_success():
    dm = DeliveryManager()
    plan = InteractionResponsePlan(
        response_type=ResponseType.GREETING,
        correlation_id="corr-1",
    )
    result = dm.deliver(plan, "telegram")
    assert result.status in (DeliveryStatus.SENT, DeliveryStatus.DELIVERED)
    assert result.provider_message_id != ""


def test_delivery_get_result():
    dm = DeliveryManager()
    plan = InteractionResponsePlan(response_type=ResponseType.SUCCESS)
    result = dm.deliver(plan, "whatsapp")
    fetched = dm.get_result(result.delivery_id)
    assert fetched is not None
    assert fetched.delivery_id == result.delivery_id


def test_delivery_count():
    dm = DeliveryManager()
    dm.deliver(InteractionResponsePlan(response_type=ResponseType.SUCCESS), "whatsapp")
    dm.deliver(InteractionResponsePlan(response_type=ResponseType.ERROR), "telegram")
    assert dm.count() == 2


def test_delivery_attempts():
    dm = DeliveryManager()
    plan = InteractionResponsePlan(response_type=ResponseType.GREETING)
    result = dm.deliver(plan, "web")
    assert len(result.attempts) >= 1
    assert result.attempts[0].status is not None
