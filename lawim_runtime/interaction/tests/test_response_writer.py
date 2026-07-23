from lawim_runtime.interaction.response_writer import (
    DeterministicResponseWriter,
    ResponseWriterRequest,
)
from lawim_runtime.interaction.response_plan import InteractionResponsePlan, ResponseType


def test_writer_safe_fallback():
    writer = DeterministicResponseWriter()
    plan = InteractionResponsePlan(response_type=ResponseType.SAFE_FALLBACK)
    req = ResponseWriterRequest(response_plan=plan)
    result = writer.write(req)
    assert result.success
    assert "difficult\u00e9" in result.text


def test_writer_greeting():
    writer = DeterministicResponseWriter()
    plan = InteractionResponsePlan(response_type=ResponseType.GREETING)
    req = ResponseWriterRequest(response_plan=plan)
    result = writer.write(req)
    assert result.success
    assert "Bonjour" in result.text


def test_writer_handover():
    writer = DeterministicResponseWriter()
    plan = InteractionResponsePlan(response_type=ResponseType.HANDOVER)
    req = ResponseWriterRequest(response_plan=plan)
    result = writer.write(req)
    assert result.success
    assert "conseiller" in result.text


def test_writer_ask_missing_field():
    writer = DeterministicResponseWriter()
    plan = InteractionResponsePlan(
        response_type=ResponseType.ASK_MISSING_FIELD,
        selected_field="city",
    )
    req = ResponseWriterRequest(response_plan=plan)
    result = writer.write(req)
    assert result.success
    assert "city" in result.text or "city" in result.formatted_text


def test_writer_no_response():
    writer = DeterministicResponseWriter()
    plan = InteractionResponsePlan(response_type=ResponseType.NO_RESPONSE)
    req = ResponseWriterRequest(response_plan=plan)
    result = writer.write(req)
    assert result.text == ""


def test_writer_success():
    writer = DeterministicResponseWriter()
    plan = InteractionResponsePlan(
        response_type=ResponseType.SUCCESS,
        structured_facts={"message": "Visit confirmed for 2026-07-25"},
    )
    req = ResponseWriterRequest(response_plan=plan)
    result = writer.write(req)
    assert result.success
    assert "confirmed" in result.text


def test_writer_present_results():
    writer = DeterministicResponseWriter()
    plan = InteractionResponsePlan(
        response_type=ResponseType.PRESENT_RESULTS,
        structured_facts={"property": "Villa Diana", "price": "150 000 000 FCFA"},
    )
    req = ResponseWriterRequest(response_plan=plan)
    result = writer.write(req)
    assert result.success
    assert "Villa Diana" in result.text


def test_writer_wait():
    writer = DeterministicResponseWriter()
    plan = InteractionResponsePlan(response_type=ResponseType.WAIT)
    req = ResponseWriterRequest(response_plan=plan)
    result = writer.write(req)
    assert result.success
    assert "patiente" in result.text


def test_writer_no_plan():
    writer = DeterministicResponseWriter()
    req = ResponseWriterRequest()
    result = writer.write(req)
    assert result.success
    assert "difficult\u00e9" in result.text
