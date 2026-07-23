from lawim_runtime.intelligence.gateway import AIIntelligenceGateway, AIGatewayMode
from lawim_runtime.intelligence.request import AIRequest, AITaskType
from lawim_runtime.intelligence.result import AIResult, AIResultStatus


def _det_handler(req: AIRequest) -> AIResult:
    return AIResult(
        request_id=req.request_id,
        status=AIResultStatus.SUCCESS,
        task_type=req.task_type.value,
        structured_output={"field": "value"},
        correlation_id=req.correlation_id,
    )


def test_gateway_disabled():
    gw = AIIntelligenceGateway(mode=AIGatewayMode.DISABLED)
    req = AIRequest(task_type=AITaskType.FIELD_EXTRACTION, input_text="test")
    result = gw.process(req)
    assert result.status == AIResultStatus.UNAVAILABLE


def test_gateway_deterministic():
    gw = AIIntelligenceGateway(
        mode=AIGatewayMode.DETERMINISTIC,
        deterministic_handler=_det_handler,
    )
    req = AIRequest(task_type=AITaskType.FIELD_EXTRACTION, input_text="test")
    result = gw.process(req)
    assert result.status == AIResultStatus.SUCCESS
    assert result.structured_output == {"field": "value"}


def test_gateway_shadow():
    det_calls = []
    llm_calls = []

    def det(req):
        det_calls.append(req)
        return _det_handler(req)

    def llm(req):
        llm_calls.append(req)
        return AIResult(status=AIResultStatus.SUCCESS, task_type="test")

    gw = AIIntelligenceGateway(
        mode=AIGatewayMode.SHADOW,
        deterministic_handler=det,
        llm_handler=llm,
    )
    req = AIRequest(task_type=AITaskType.FIELD_EXTRACTION, input_text="test")
    result = gw.process(req)
    assert result.status == AIResultStatus.SUCCESS
    assert len(det_calls) == 1
    assert len(llm_calls) == 1


def test_gateway_canary_authorized():
    gw = AIIntelligenceGateway(
        mode=AIGatewayMode.CANARY,
        deterministic_handler=_det_handler,
        canary_check=lambda uid, pid: uid == "canary-user",
    )
    req = AIRequest(task_type=AITaskType.FIELD_EXTRACTION, metadata={"user_id": "canary-user"})
    result = gw.process(req)
    assert result.status == AIResultStatus.UNAVAILABLE


def test_gateway_primary_with_fallback():
    llm_calls = []

    def failing_llm(req):
        llm_calls.append(req)
        raise Exception("provider error")

    gw = AIIntelligenceGateway(
        mode=AIGatewayMode.PRIMARY_WITH_DETERMINISTIC_FALLBACK,
        deterministic_handler=_det_handler,
        llm_handler=failing_llm,
    )
    req = AIRequest(task_type=AITaskType.FIELD_EXTRACTION, input_text="test")
    result = gw.process(req)
    assert result.status == AIResultStatus.SUCCESS


def test_gateway_mode_property():
    gw = AIIntelligenceGateway(mode=AIGatewayMode.DETERMINISTIC)
    assert gw.mode == AIGatewayMode.DETERMINISTIC
    gw.set_mode(AIGatewayMode.SHADOW)
    assert gw.mode == AIGatewayMode.SHADOW
